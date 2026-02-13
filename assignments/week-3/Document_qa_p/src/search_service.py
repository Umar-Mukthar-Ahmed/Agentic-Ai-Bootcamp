"""
Azure AI Search service module
Handles document search and retrieval with user-specific filtering
"""

from typing import List, Dict, Optional
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.core.exceptions import AzureError

from config import SearchConfig, StorageConfig


class SearchService:
    """Service for searching documents in Azure AI Search"""

    def __init__(self, search_config: SearchConfig, storage_config: StorageConfig):
        """
        Initialize search service

        Args:
            search_config: Azure AI Search configuration
            storage_config: Azure Storage configuration (for building filters)
        """
        self.config = search_config
        self.storage_config = storage_config
        self.client = SearchClient(
            endpoint=search_config.endpoint,
            index_name=search_config.index_name,
            credential=AzureKeyCredential(search_config.api_key)
        )

    def search_user_documents(
            self,
            username: str,
            query: str,
            top_k: int = 3
    ) -> List[Dict[str, str]]:
        """
        Search documents with user-specific filtering

        Args:
            username: Username for folder-based filtering
            query: Search query
            top_k: Number of results to return

        Returns:
            List of document dictionaries with 'content' and 'source' keys
        """
        try:
            print(f"🔍 Searching for '{query}' in {username}'s documents...")

            # Build user-specific filter
            filter_expression = self._build_user_filter(username)
            print(f"📁 Filter: {filter_expression}")

            # Execute search
            results = self.client.search(
                search_text=query,
                filter=filter_expression,
                select=["content", "metadata_storage_path"],
                top=top_k
            )

            # Process results
            documents = []
            for result in results:
                documents.append({
                    "content": result.get("content", ""),
                    "source": result.get("metadata_storage_path", "Unknown")
                })

            print(f"✅ Found {len(documents)} relevant document(s)")
            return documents

        except AzureError as e:
            print(f"❌ Azure Search Error: {e}")
            return []
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return []

    def search_all_documents(
            self,
            query: str,
            top_k: int = 3,
            filter_expression: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Search across all documents (no user filtering)

        Args:
            query: Search query
            top_k: Number of results to return
            filter_expression: Optional custom OData filter

        Returns:
            List of document dictionaries
        """
        try:
            print(f"🔍 Searching all documents for '{query}'...")

            results = self.client.search(
                search_text=query,
                filter=filter_expression,
                select=["content", "metadata_storage_path"],
                top=top_k
            )

            documents = []
            for result in results:
                documents.append({
                    "content": result.get("content", ""),
                    "source": result.get("metadata_storage_path", "Unknown")
                })

            print(f"✅ Found {len(documents)} document(s)")
            return documents

        except Exception as e:
            print(f"❌ Search Error: {e}")
            return []

    def _build_user_filter(self, username: str) -> str:
        """
        Build OData filter expression for user-specific documents

        Args:
            username: Username/folder name

        Returns:
            OData filter expression string
        """
        # Build the user's folder URL prefix
        user_folder_prefix = (
            f"{self.storage_config.account_url}/"
            f"{self.storage_config.container_name}/"
            f"{username}/"
        )

        # Use tilde (~) as upper bound for range query
        # This ensures we only get files within the user's folder
        upper_bound = user_folder_prefix + "~"

        # OData filter: path >= 'prefix' AND path < 'prefix~'
        filter_expression = (
            f"metadata_storage_path ge '{user_folder_prefix}' and "
            f"metadata_storage_path lt '{upper_bound}'"
        )

        return filter_expression

    def get_document_count(self) -> int:
        """
        Get total number of documents in the index

        Returns:
            Document count
        """
        try:
            results = self.client.search(
                search_text="*",
                include_total_count=True,
                top=0
            )
            return results.get_count() or 0
        except Exception as e:
            print(f"❌ Error getting document count: {e}")
            return 0

    def test_connection(self) -> bool:
        """
        Test connection to Azure AI Search

        Returns:
            True if connection successful, False otherwise
        """
        try:
            self.get_document_count()
            print("✅ Azure AI Search connection successful")
            return True
        except Exception as e:
            print(f"❌ Azure AI Search connection failed: {e}")
            return False