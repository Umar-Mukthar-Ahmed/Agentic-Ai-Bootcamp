"""
Main application entry point for Company Policy Q&A System
Provides interactive menu for different operations
"""

import sys
from typing import Optional

from config import AppConfig
from rag_service import RAGService


def print_header():
    """Print application header"""
    print("\n" + "="*70)
    print(" 📚  COMPANY POLICY Q&A SYSTEM  ".center(70))
    print("    Powered by Azure AI Search + OpenAI".center(70))
    print("="*70 + "\n")


def print_menu():
    """Print main menu options"""
    print("\n" + "─"*70)
    print("MAIN MENU".center(70))
    print("─"*70)
    print("  1️⃣  Single Question (User-Specific)")
    print("  2️⃣  Interactive Q&A Session (User-Specific)")
    print("  3️⃣  Search All Documents (No User Filter)")
    print("  4️⃣  Batch Questions")
    print("  5️⃣  Test System Connection")
    print("  6️⃣  View System Info")
    print("  0️⃣  Exit")
    print("─"*70)


def get_username() -> str:
    """Get username from user input"""
    username = input("👤 Enter your username/folder name: ").strip()
    if not username:
        print("⚠️  Username cannot be empty!")
        return get_username()
    return username


def single_question_mode(rag_service: RAGService):
    """Handle single question mode"""
    username = get_username()
    question = input("❓ Enter your question: ").strip()

    if not question:
        print("⚠️  Question cannot be empty!")
        return

    # Advanced options
    print("\n⚙️  Advanced Options (press Enter for defaults):")
    top_k_input = input(f"   Number of documents to retrieve [default: 3]: ").strip()
    top_k = int(top_k_input) if top_k_input.isdigit() else None

    print("   Mode: 1=Strict, 2=Conversational, 3=Detailed [default: 1]")
    mode_input = input("   Select mode: ").strip()
    mode_map = {"1": "strict", "2": "conversational", "3": "detailed"}
    mode = mode_map.get(mode_input, "strict")

    # Execute query
    result = rag_service.ask_question(
        username=username,
        question=question,
        top_k=top_k,
        mode=mode
    )

    # Display results
    print("\n" + "💡 ANSWER ".center(70, "="))
    print(result.answer)

    if result.source_documents:
        print("\n" + "📚 SOURCE DOCUMENTS ".center(70, "="))
        for i, doc in enumerate(result.source_documents, 1):
            source_file = doc['source'].split('/')[-1]
            print(f"\n[{i}] {source_file}")
            content_preview = doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
            print(f"    {content_preview}")

    print("\n" + "="*70)


def interactive_mode(rag_service: RAGService):
    """Handle interactive Q&A session"""
    username = get_username()
    rag_service.interactive_qa(username)


def search_all_mode(rag_service: RAGService):
    """Search across all documents without user filtering"""
    question = input("❓ Enter your question: ").strip()

    if not question:
        print("⚠️  Question cannot be empty!")
        return

    result = rag_service.ask_question_all_docs(question)

    # Display results
    print("\n" + "💡 ANSWER ".center(70, "="))
    print(result.answer)

    if result.source_documents:
        print("\n" + "📚 SOURCE DOCUMENTS ".center(70, "="))
        for i, doc in enumerate(result.source_documents, 1):
            # Extract username from path
            path_parts = doc['source'].split('/')
            username = path_parts[-2] if len(path_parts) > 1 else "Unknown"
            source_file = path_parts[-1]

            print(f"\n[{i}] {source_file} (from {username})")
            content_preview = doc['content'][:200] + "..." if len(doc['content']) > 200 else doc['content']
            print(f"    {content_preview}")

    print("\n" + "="*70)


def batch_mode(rag_service: RAGService):
    """Handle batch questions"""
    username = get_username()

    print("\n📝 Enter your questions (one per line, empty line to finish):")
    questions = []
    i = 1
    while True:
        q = input(f"  {i}. ").strip()
        if not q:
            break
        questions.append(q)
        i += 1

    if not questions:
        print("⚠️  No questions entered!")
        return

    print(f"\n🔄 Processing {len(questions)} questions...")
    results = rag_service.batch_questions(username, questions)

    # Display summary
    print("\n" + "📊 BATCH RESULTS ".center(70, "="))
    for i, (question, result) in enumerate(zip(questions, results), 1):
        print(f"\n{'─'*70}")
        print(f"Q{i}: {question}")
        print(f"{'─'*70}")
        print(result.answer)
        if result.source_documents:
            sources = [doc['source'].split('/')[-1] for doc in result.source_documents]
            print(f"\n📚 Sources: {', '.join(sources)}")

    print("\n" + "="*70)


def test_system(rag_service: RAGService):
    """Test system connectivity"""
    rag_service.test_system()
    input("\nPress Enter to continue...")


def view_system_info(config: AppConfig):
    """Display system configuration info"""
    print("\n" + "ℹ️  SYSTEM INFORMATION ".center(70, "="))
    print(f"\n📦 Storage Container: {config.storage.container_name}")
    print(f"🔍 Search Index: {config.search.index_name}")
    print(f"🤖 OpenAI Model: {config.openai.deployment}")
    print(f"🎯 Default Top K: {config.default_top_k}")
    print(f"🌡️  Default Temperature: {config.default_temperature}")
    print("\n" + "="*70)
    input("\nPress Enter to continue...")


def main():
    """Main application loop"""
    # Load configuration
    config = AppConfig.load()

    # Validate configuration
    is_valid, errors = config.validate()
    if not is_valid:
        print("\n❌ Configuration Error!")
        print("Please check your .env file. Missing:")
        for error in errors:
            print(f"  • {error}")
        sys.exit(1)

    # Initialize RAG service
    rag_service = RAGService(config)

    # Show header
    print_header()
    print("✅ System initialized successfully!")

    # Main menu loop
    while True:
        try:
            print_menu()
            choice = input("\n🎯 Select an option: ").strip()

            if choice == "1":
                single_question_mode(rag_service)
            elif choice == "2":
                interactive_mode(rag_service)
            elif choice == "3":
                search_all_mode(rag_service)
            elif choice == "4":
                batch_mode(rag_service)
            elif choice == "5":
                test_system(rag_service)
            elif choice == "6":
                view_system_info(config)
            elif choice == "0":
                print("\n👋 Thank you for using the Company Policy Q&A System!")
                print("="*70 + "\n")
                break
            else:
                print("\n⚠️  Invalid option. Please try again.")

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            print("Please try again or contact support.\n")


if __name__ == "__main__":
    main()