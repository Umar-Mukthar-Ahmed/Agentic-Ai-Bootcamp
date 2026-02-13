"""
Prompt library for Azure OpenAI RAG System
Contains reusable system and user prompts
"""


class SystemPrompts:
    """System prompts for different scenarios"""

    STRICT_RAG = """You are a helpful AI assistant that answers questions about company policies.

IMPORTANT RULES:
1. Answer ONLY using the provided context documents
2. If the answer is NOT in the context, you MUST say "I don't have that information in the provided documents"
3. Never make up or guess information
4. Be concise and accurate
5. Cite the source document when possible

This approach builds trust with users by being honest about limitations."""

    CONVERSATIONAL_RAG = """You are a friendly AI assistant helping employees find information in company policy documents.

Guidelines:
- Use the provided context to answer questions
- If information is missing, clearly state "This information is not available in the documents I have access to"
- Be professional but approachable
- If you're uncertain, express that uncertainty
- Suggest related topics that might be helpful"""

    DETAILED_RAG = """You are an expert policy analyst assistant.

Your task:
1. Analyze the provided context carefully
2. Provide comprehensive answers with relevant details
3. Structure your response clearly
4. If information is incomplete, state what IS available and what ISN'T
5. Never fabricate information
6. Always maintain professional tone"""


class UserPromptTemplates:
    """Templates for constructing user prompts"""

    @staticmethod
    def basic_rag(context: str, question: str) -> str:
        """Basic RAG prompt with context and question"""
        return f"""Context from company documents:
{context}

Question: {question}

Please answer based only on the context provided above."""

    @staticmethod
    def structured_rag(context_docs: list[dict], question: str) -> str:
        """Structured RAG prompt with source citations"""
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            source = doc.get('source', 'Unknown')
            content = doc.get('content', '')
            context_parts.append(f"[Document {i}]\nSource: {source}\nContent: {content}")

        context_text = "\n\n".join(context_parts)

        return f"""I have found the following relevant documents:

{context_text}

Question: {question}

Please provide an answer based on these documents. If citing information, refer to the document number."""

    @staticmethod
    def follow_up_rag(context: str, previous_qa: list[dict], current_question: str) -> str:
        """RAG prompt that maintains conversation history"""
        history = "\n".join([
            f"Q: {qa['question']}\nA: {qa['answer']}"
            for qa in previous_qa
        ])

        return f"""Previous conversation:
{history}

Current context:
{context}

New question: {current_question}

Answer the new question using the context, keeping in mind the previous conversation."""


class FeedbackPrompts:
    """Prompts for user feedback and clarification"""

    NO_DOCUMENTS_FOUND = """I couldn't find any relevant documents to answer your question.

This could mean:
- The information might not be in the uploaded policy documents
- Try rephrasing your question with different keywords
- Check if you're asking about the right topic

Would you like to try a different question?"""

    AMBIGUOUS_QUESTION = """Your question could be interpreted in multiple ways. Could you please clarify:

{clarification_options}

This will help me provide a more accurate answer."""

    @staticmethod
    def partial_answer(available_info: str) -> str:
        """When only partial information is available"""
        return f"""Based on the available documents, I can tell you:

{available_info}

However, I don't have complete information to fully answer your question. The documents don't contain details about all aspects you're asking about."""


# Convenience function to get default prompt
def get_default_system_prompt() -> str:
    """Returns the default system prompt (STRICT_RAG)"""
    return SystemPrompts.STRICT_RAG


def get_system_prompt(mode: str = "strict") -> str:
    """
    Get system prompt by mode

    Args:
        mode: "strict", "conversational", or "detailed"

    Returns:
        System prompt string
    """
    mode_map = {
        "strict": SystemPrompts.STRICT_RAG,
        "conversational": SystemPrompts.CONVERSATIONAL_RAG,
        "detailed": SystemPrompts.DETAILED_RAG
    }
    return mode_map.get(mode.lower(), SystemPrompts.STRICT_RAG)