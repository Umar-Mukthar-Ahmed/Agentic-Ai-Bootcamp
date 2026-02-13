"""
Configuration module for Azure AI Search + OpenAI RAG System
Handles environment variables and application settings
"""

import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()


@dataclass
class StorageConfig:
    """Azure Storage Account configuration"""
    account_url: str
    container_name: str

    @classmethod
    def from_env(cls):
        return cls(
            account_url=os.getenv("STORAGE_ACCOUNT_URL", ""),
            container_name=os.getenv("CONTAINER_NAME", "studentpdfs")
        )


@dataclass
class SearchConfig:
    """Azure AI Search configuration"""
    endpoint: str
    index_name: str
    api_key: str

    @classmethod
    def from_env(cls):
        return cls(
            endpoint=os.getenv("SEARCH_ENDPOINT", ""),
            index_name=os.getenv("SEARCH_INDEX_NAME", "doc-index"),
            api_key=os.getenv("SEARCH_API_KEY", "")
        )


@dataclass
class OpenAIConfig:
    """Azure OpenAI configuration"""
    endpoint: str
    api_key: str
    deployment: str
    api_version: str

    @classmethod
    def from_env(cls):
        return cls(
            endpoint=os.getenv("OPENAI_ENDPOINT", ""),
            api_key=os.getenv("OPENAI_API_KEY", ""),
            deployment=os.getenv("OPENAI_DEPLOYMENT", "gpt-4.1"),
            api_version=os.getenv("OPENAI_API_VERSION", "2024-02-15-preview")
        )


@dataclass
class AppConfig:
    """Main application configuration"""
    storage: StorageConfig
    search: SearchConfig
    openai: OpenAIConfig

    # Application settings
    default_top_k: int = 3
    default_temperature: float = 0.7

    @classmethod
    def load(cls):
        """Load all configurations from environment"""
        return cls(
            storage=StorageConfig.from_env(),
            search=SearchConfig.from_env(),
            openai=OpenAIConfig.from_env()
        )

    def validate(self) -> tuple[bool, list[str]]:
        """Validate that all required configurations are set"""
        errors = []

        if not self.storage.account_url:
            errors.append("STORAGE_ACCOUNT_URL is not set")
        if not self.storage.container_name:
            errors.append("CONTAINER_NAME is not set")
        if not self.search.endpoint:
            errors.append("SEARCH_ENDPOINT is not set")
        if not self.search.api_key:
            errors.append("SEARCH_API_KEY is not set")
        if not self.openai.endpoint:
            errors.append("OPENAI_ENDPOINT is not set")
        if not self.openai.api_key:
            errors.append("OPENAI_API_KEY is not set")

        return len(errors) == 0, errors