"""
Typesense DGB - Módulo para indexação e busca de notícias do governo brasileiro.

Este módulo fornece funcionalidades para:
- Conexão com servidores Typesense
- Criação e gerenciamento de coleções
- Download e processamento do dataset govbrnews
- Indexação de documentos
"""

from typesense_dgb.client import get_client, wait_for_typesense
from typesense_dgb.collection import (
    COLLECTION_NAME,
    COLLECTION_SCHEMA,
    create_collection,
    delete_collection,
    list_collections,
)
from typesense_dgb.dataset import download_and_process_dataset
from typesense_dgb.indexer import index_documents, prepare_document
from typesense_dgb.utils import calculate_published_week

__version__ = "1.0.0"
__all__ = [
    # Client
    "get_client",
    "wait_for_typesense",
    # Collection
    "COLLECTION_NAME",
    "COLLECTION_SCHEMA",
    "create_collection",
    "delete_collection",
    "list_collections",
    # Dataset
    "download_and_process_dataset",
    # Indexer
    "index_documents",
    "prepare_document",
    # Utils
    "calculate_published_week",
]
