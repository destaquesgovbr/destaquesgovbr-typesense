#!/usr/bin/env python3
"""
CLI para deletar coleções do Typesense.

ATENÇÃO: Esta operação é irreversível!

Usage:
    # Listar coleções
    python scripts/delete_collection.py --list

    # Deletar com confirmação interativa
    python scripts/delete_collection.py --collection news

    # Deletar sem confirmação (para automação)
    python scripts/delete_collection.py --collection news --confirm
"""

import argparse
import logging
import sys

from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

from typesense_dgb import delete_collection, get_client, list_collections


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Deleta uma coleção do Typesense",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Listar todas as coleções
  python delete_collection.py --list

  # Deletar com confirmação interativa
  python delete_collection.py --collection news

  # Deletar sem confirmação (para automação)
  python delete_collection.py --collection news --confirm
        """,
    )

    parser.add_argument(
        "--collection",
        type=str,
        help="Nome da coleção a deletar",
    )

    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Pula prompt de confirmação (use com cuidado!)",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="Lista todas as coleções disponíveis",
    )

    return parser.parse_args()


def main() -> None:
    """Main function."""
    try:
        args = parse_arguments()

        client = get_client()

        if args.list:
            list_collections(client)
            return

        if not args.collection:
            logger.error("Erro: argumento --collection é obrigatório")
            logger.info("Use --list para ver coleções disponíveis")
            sys.exit(1)

        logger.info("=" * 80)
        logger.info("Deleção de Coleção Typesense")
        logger.info("=" * 80)

        success = delete_collection(client, args.collection, args.confirm)

        if success:
            logger.info("=" * 80)
            logger.info("Deleção de coleção concluída com sucesso!")
            logger.info("=" * 80)
            sys.exit(0)
        else:
            logger.error("Falha na deleção da coleção")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("\nOperação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
