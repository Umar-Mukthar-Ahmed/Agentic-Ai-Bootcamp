"""
Azure OpenAI service module
Handles answer generation using RAG approach
"""

from typing import List, Dict, Optional
from openai import AzureOpenAI
from openai import OpenAIError

from config import OpenAIConfig
from prompts import (
    get_system_prompt,
    UserPromptTemplates,
    FeedbackPrompts
)


class OpenAIService:
    """Service for generating answers using Azure OpenAI"""

    def __init__(self, config: OpenAIConfig):
        """
        Initialize OpenAI service

        Args:
            config: Azure OpenAI configuration
        """
        self.config = config
        self.client = AzureOpenAI(
            azure_endpoint=config.endpoint,
            api_key=config.api_key,
            api_version=config.api_version
        )

    def generate_answer(
            self,
            question: str,
            context_docs: List[Dict[str, str]],
            mode: str = "strict",
            temperature: float = 0.7
    ) -> str:
        """
        Generate answer using RAG approach

        Args:
            question: User's question
            context_docs: List of retrieved documents
            mode: Prompt mode ("strict", "conversational", "detailed")
            temperature: Model temperature (0.0 - 1.0)

        Returns:
            Generated answer string
        """
        # Handle case when no documents found
        if not context_docs:
            return FeedbackPrompts.NO_DOCUMENTS_FOUND

        try:
            print("🤖 Generating answer with Azure OpenAI...")

            # Get appropriate system prompt
            system_prompt = get_system_prompt(mode)

            # Build user prompt with context
            user_prompt = UserPromptTemplates.structured_rag(
                context_docs,
                question
            )

            # Generate response
            response = self.client.chat.completions.create(
                model=self.config.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )

            answer = response.choices[0].message.content
            print("✅ Answer generated successfully")
            return answer

        except OpenAIError as e:
            print(f"❌ OpenAI API Error: {e}")
            return "Sorry, I encountered an error while generating the answer. Please try again."
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            return "An unexpected error occurred. Please try again."

    def generate_with_conversation(
            self,
            question: str,
            context_docs: List[Dict[str, str]],
            conversation_history: List[Dict[str, str]],
            temperature: float = 0.7
    ) -> str:
        """
        Generate answer with conversation context

        Args:
            question: Current question
            context_docs: Retrieved documents
            conversation_history: Previous Q&A pairs
            temperature: Model temperature

        Returns:
            Generated answer
        """
        if not context_docs:
            return FeedbackPrompts.NO_DOCUMENTS_FOUND

        try:
            # Build context text
            context_text = "\n\n".join([
                f"Source: {doc['source']}\nContent: {doc['content']}"
                for doc in context_docs
            ])

            # Build user prompt with history
            user_prompt = UserPromptTemplates.follow_up_rag(
                context_text,
                conversation_history,
                question
            )

            system_prompt = get_system_prompt("conversational")

            response = self.client.chat.completions.create(
                model=self.config.deployment,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Error: {e}")
            return "Error generating answer with conversation context."

    def test_connection(self) -> bool:
        """
        Test connection to Azure OpenAI

        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.config.deployment,
                messages=[
                    {"role": "user", "content": "Hello"}
                ],
                max_tokens=10
            )
            print("✅ Azure OpenAI connection successful")
            return True
        except Exception as e:
            print(f"❌ Azure OpenAI connection failed: {e}")
            return False

    def summarize_documents(
            self,
            documents: List[Dict[str, str]],
            max_length: int = 200
    ) -> str:
        """
        Generate a summary of multiple documents

        Args:
            documents: List of documents to summarize
            max_length: Maximum words in summary

        Returns:
            Summary text
        """
        if not documents:
            return "No documents to summarize."

        try:
            content = "\n\n".join([
                f"Document: {doc['source']}\n{doc['content']}"
                for doc in documents
            ])

            prompt = f"""Summarize the following documents in approximately {max_length} words:

{content}

Provide a concise summary highlighting the key points."""

            response = self.client.chat.completions.create(
                model=self.config.deployment,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )

            return response.choices[0].message.content

        except Exception as e:
            print(f"❌ Summarization Error: {e}")
            return "Error generating summary."