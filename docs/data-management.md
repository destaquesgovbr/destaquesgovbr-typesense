# Typesense Data Management

Este documento descreve os workflows e scripts disponíveis para gerenciar os dados no Typesense em produção.

## Visão Geral

O projeto possui três formas de gerenciar dados no Typesense:

1. **Daily Incremental Load** - Carregamento incremental diário automático
2. **Full Data Reload** - Recarregamento completo manual (workflow dispatcher)
3. **Scripts CLI** - Scripts Python para operações manuais

## 1. Carregamento Incremental Diário

### Descrição
Workflow que executa automaticamente todos os dias às 10:00 AM UTC (7:00 AM horário de Brasília) para carregar notícias dos últimos 7 dias.

### Workflow
`.github/workflows/typesense-daily-load.yml`

### Execução Manual
Você pode executar manualmente via GitHub Actions:
1. Acesse: Actions → "Typesense Daily Incremental Load" → "Run workflow"
2. Opcionalmente, especifique o número de dias para carregar (padrão: 7)

### Comportamento
- Modo: `incremental`
- Ação: `upsert` (atualiza documentos existentes ou insere novos)
- Não deleta dados existentes
- Atualiza o cache do portal automaticamente após sucesso

## 2. Recarregamento Completo (Full Reload)

### ⚠️ OPERAÇÃO DESTRUTIVA

Este workflow **deleta completamente** a collection existente e recarrega todos os dados do zero.

### Quando Usar
- Após mudanças no schema da collection
- Para resolver problemas de dados corrompidos
- Para sincronizar com alterações no dataset do HuggingFace
- Para limpar dados inconsistentes

### Workflow
`.github/workflows/typesense-full-reload.yml`

### Como Executar

1. **Acesse o GitHub Actions**
   ```
   Repository → Actions → "Typesense Full Data Reload" → "Run workflow"
   ```

2. **Preencha os Parâmetros**
   - **confirm_deletion**: Digite exatamente `DELETE` (em maiúsculas) para confirmar
   - **skip_portal_refresh**: (Opcional) Marque para não atualizar o cache do portal

3. **Confirme e Execute**
   - Clique em "Run workflow"
   - O workflow irá:
     1. Deletar a collection `news` existente
     2. Recriar a collection com o schema atualizado
     3. Carregar todos os dados do HuggingFace
     4. Verificar a integridade dos dados
     5. Atualizar o cache do portal (se não foi pulado)

### Tempo de Execução
- Estimado: 15-30 minutos (depende do tamanho do dataset)

## 3. Scripts CLI

Para operações manuais ou debugging, você pode executar os scripts Python diretamente.

### Pré-requisitos
```bash
# Instalar dependências
pip install -r requirements.txt
pip install -e .

# Configurar variáveis de ambiente
export TYPESENSE_HOST=your-host
export TYPESENSE_PORT=8108
export TYPESENSE_API_KEY=your-api-key
```

### 3.1. Deletar Collection

```bash
# Listar todas as collections
python scripts/delete_collection.py --list

# Deletar com confirmação interativa
python scripts/delete_collection.py --collection news

# Deletar sem confirmação (para automação)
python scripts/delete_collection.py --collection news --confirm
```

### 3.2. Carregar Dados

```bash
# Carregamento completo (apenas em collection vazia)
python scripts/load_data.py --mode full

# Carregamento completo com força (sobrescreve dados existentes)
python scripts/load_data.py --mode full --force

# Carregamento incremental (últimos 7 dias)
python scripts/load_data.py --mode incremental --days 7

# Carregamento incremental (últimos 30 dias)
python scripts/load_data.py --mode incremental --days 30
```

## Variáveis de Ambiente

### Secrets do GitHub (para workflows)
- `TYPESENSE_HOST`: Endereço IP ou hostname do servidor Typesense
- `TYPESENSE_API_KEY`: API key com permissões de escrita
- `GCP_WORKLOAD_IDENTITY_PROVIDER`: Provider de identidade do GCP
- `GCP_SERVICE_ACCOUNT`: Service account do GCP

### Arquivo .env (para scripts locais)
```bash
TYPESENSE_HOST=your-typesense-host
TYPESENSE_PORT=8108
TYPESENSE_API_KEY=your-api-key-here
```

## Troubleshooting

### Erro: "Collection already exists"
**Solução**: Use o workflow "Typesense Full Data Reload" ou delete manualmente com `delete_collection.py`

### Erro: "Full mode on non-empty collection"
**Solução**:
- Use `--force` flag: `--mode full --force`
- Ou delete a collection primeiro e execute novamente

### Erro: "Typesense not ready"
**Solução**:
1. Verifique se o servidor Typesense está rodando
2. Confirme que o host e porta estão corretos
3. Teste a conectividade: `curl http://<host>:8108/health`

### Erro: "Authentication failed"
**Solução**:
1. Verifique se `TYPESENSE_API_KEY` está configurada corretamente
2. Confirme que a API key tem permissões de escrita

## Monitoramento

### Verificar Status da Collection
```bash
python scripts/delete_collection.py --list
```

### Logs do Workflow
- Acesse: Actions → [nome do workflow] → [execução específica]
- Todos os logs são salvos e podem ser inspecionados

## Backup e Recuperação

O projeto **não possui backup automático** para reduzir custos, pois:
- Os dados podem ser recriados do dataset do HuggingFace a qualquer momento
- Use o workflow "Full Data Reload" para restaurar dados do zero

## Melhores Práticas

1. **Use Incremental Load para atualizações diárias**
   - Mais rápido e eficiente
   - Não afeta dados existentes

2. **Use Full Reload apenas quando necessário**
   - Operação destrutiva
   - Requer confirmação explícita
   - Causa downtime temporário

3. **Teste em ambiente de desenvolvimento primeiro**
   - Configure uma instância Typesense local com Docker
   - Valide mudanças de schema antes de aplicar em produção

4. **Monitore os logs dos workflows**
   - Verifique se os carregamentos estão sendo bem-sucedidos
   - Investigue falhas imediatamente

## Arquitetura

```
HuggingFace Dataset (nitaibezerra/govbrnews)
           ↓
    GitHub Actions Workflow
           ↓
    Python Scripts (typesense_dgb)
           ↓
   Typesense Collection (news)
           ↓
    Cloud Run Portal (API)
```
