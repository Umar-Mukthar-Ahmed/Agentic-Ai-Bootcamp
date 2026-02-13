"""
RAG Service - Main orchestrator for Retrieval Augmented Generation
Combines search and OpenAI services into a cohesive pipeline
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

from config import AppConfig
from search_service import SearchService
from openai_service import OpenAIService


@dataclass
class RAGResult:
    """Result from RAG pipeline"""
    answer: str
    source_documents: List[Dict[str, str]]
    metadata: Dict[str, any]


class RAGService:
    """Main RAG service orchestrating the complete pipeline"""

    def __init__(self, config: AppConfig):
        """
        Initialize RAG service with all components

        Args:
            config: Application configuration
        """
        self.config = config
        self.search_service = SearchService(config.search, config.storage)
        self.openai_service = OpenAIService(config.openai)

    def ask_question(
            self,
            username: str,
            question: str,
            top_k: Optional[int] = None,
            mode: str = "strict",
            temperature: Optional[float] = None
    ) -> RAGResult:
        """
        Complete RAG pipeline: Search → Retrieve → Generate

        Args:
            username: User's folder name for filtering
            question: User's question
            top_k: Number of documents to retrieve (default from config)
            mode: Generation mode ("strict", "conversational", "detailed")
            temperature: Model temperature (default from config)

        Returns:
            RAGResult containing answer, sources, and metadata
        """
        # Use defaults from config if not provided
        top_k = top_k or self.config.default_top_k
        temperature = temperature or self.config.default_temperature

        print("\n" + "=" * 60)
        print(f"👤 User: {username}")
        print(f"❓ Question: {question}")
        print("=" * 60)

        # Step 1: Search for relevant documents
        documents = self.search_service.search_user_documents(
            username=username,
            query=question,
            top_k=top_k
        )

        # Step 2: Generate answer using retrieved documents
        answer = self.openai_service.generate_answer(
            question=question,
            context_docs=documents,
            mode=mode,
            temperature=temperature
        )

        # Step 3: Package results
        result = RAGResult(
            answer=answer,
            source_documents=documents,
            metadata={
                "username": username,
                "question": question,
                "num_sources": len(documents),
                "mode": mode,
                "temperature": temperature
            }
        )

        return result

    def ask_question_all_docs(
            self,
            question: str,
            top_k: Optional[int] = None,
            mode: str = "strict",
            temperature: Optional[float] = None
    ) -> RAGResult:
        """
        Ask question across ALL documents (no user filtering)

        Args:
            question: User's question
            top_k: Number of documents to retrieve
            mode: Generation mode
            temperature: Model temperature

        Returns:
            RAGResult with answer and sources
        """
        top_k = top_k or self.config.default_top_k
        temperature = temperature or self.config.default_temperature

        print("\n" + "=" * 60)
        print(f"❓ Question (All Documents): {question}")
        print("=" * 60)

        # Search all documents
        documents = self.search_service.search_all_documents(
            query=question,
            top_k=top_k
        )

        # Generate answer
        answer = self.openai_service.generate_answer(
            question=question,
            context_docs=documents,
            mode=mode,
            temperature=temperature
        )

        return RAGResult(
            answer=answer,
            source_documents=documents,
            metadata={
                "question": question,
                "num_sources": len(documents),
                "mode": mode,
                "scope": "all_documents"
            }
        )

    def interactive_qa(self, username: str):
        """
        Interactive Q&A session with a user

        Args:
            username: User's folder name
        """
        print("\n" + "🤖 " + "=" * 58)
        print("   Welcome to the Company Policy Q&A Assistant")
        print("=" * 60)
        print(f"👤 Logged in as: {username}")
        print("\nType 'exit' or 'quit' to end the session")
        print("=" * 60 + "\n")

        conversation_history = []

        while True:
            try:
                question = input("❓ Your question: ").strip()

                if not question:
                    continue

                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Thank you for using the Q&A Assistant!")
                    break

                # Get answer
                result = self.ask_question(
                    username=username,
                    question=question
                )

                # Display results
                self._display_result(result)

                # Store in history
                conversation_history.append({
                    "question": question,
                    "answer": result.answer
                })

                print("\n" + "-" * 60 + "\n")

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}\n")

    def _display_result(self, result: RAGResult):
        """Display RAG result in a formatted way"""
        print("\n" + "💡 ANSWER ".center(60, "="))
        print(result.answer)

        if result.source_documents:
            print("\n" + "📚 SOURCES ".center(60, "="))
            for i, doc in enumerate(result.source_documents, 1):
                source = doc['source'].split('/')[-1]  # Get filename only
                print(f"\n[{i}] {source}")

        print("\n" + "=" * 60)

    def test_system(self) -> bool:
        """
        Test all system components

        Returns:
            True if all tests pass, False otherwise
        """
        print("\n🔧 Testing System Components...")
        print("-" * 60)

        search_ok = self.search_service.test_connection()
        openai_ok = self.openai_service.test_connection()

        print("-" * 60)

        if search_ok and openai_ok:
            print("✅ All systems operational!")

            # Show index stats
            doc_count = self.search_service.get_document_count()
            print(f"📄 Total documents in index: {doc_count}")

            return True
        else:
            print("❌ System check failed. Please verify your configuration.")
            return False

    def batch_questions(
            self,
            username: str,
            questions: List[str]
    ) -> List[RAGResult]:
        """
        Process multiple questions in batch

        Args:
            username: User's folder name
            questions: List of questions

        Returns:
            List of RAGResults
        """
        results = []

        print(f"\n📋 Processing {len(questions)} questions for {username}...")

        for i, question in enumerate(questions, 1):
            print(f"\n[{i}/{len(questions)}] {question}")
            result = self.ask_question(username, question)
            results.append(result)

        return results