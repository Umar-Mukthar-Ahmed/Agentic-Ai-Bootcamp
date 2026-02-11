"""
Configuration management for the application.
Handles both local (.env) and Streamlit Cloud (secrets) configurations.
"""

import os


class Config:
    """Application configuration"""

    # Try to load from Streamlit secrets first (for cloud deployment)
    try:
        import streamlit as st
        AZURE_OPENAI_ENDPOINT = st.secrets.get("AZURE_OPENAI_ENDPOINT", "")
        AZURE_OPENAI_KEY = st.secrets.get("AZURE_OPENAI_KEY", "")
        AZURE_OPENAI_DEPLOYMENT = st.secrets.get("AZURE_OPENAI_DEPLOYMENT", "gpt-4")
        _config_source = "Streamlit Secrets"
    except Exception:
        # Fallback to environment variables (for local development)
        try:
            from dotenv import load_dotenv
            load_dotenv()
            _config_source = "Environment Variables"
        except ImportError:
            _config_source = "Environment Variables (no dotenv)"

        AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        AZURE_OPENAI_KEY = os.getenv("AZURE_OPENAI_KEY", "")
        AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4")

    # Azure API version
    AZURE_API_VERSION = "2024-02-15-preview"

    # File paths
    DATA_PATH = "data/sample_feedback.json"
    AZURE_RESULTS_PATH = "data/results/azure_results.json"
    BASELINE_RESULTS_PATH = "data/results/baseline_results.json"

    @classmethod
    def is_configured(cls):
        """Check if Azure OpenAI is properly configured"""
        return bool(cls.AZURE_OPENAI_ENDPOINT and cls.AZURE_OPENAI_KEY)

    @classmethod
    def get_config_info(cls):
        """Get configuration information for debugging"""
        return {
            "source": cls._config_source,
            "endpoint_set": bool(cls.AZURE_OPENAI_ENDPOINT),
            "key_set": bool(cls.AZURE_OPENAI_KEY),
            "deployment": cls.AZURE_OPENAI_DEPLOYMENT
        }