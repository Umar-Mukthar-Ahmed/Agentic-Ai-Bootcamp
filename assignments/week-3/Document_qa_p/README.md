# 📚 Company Policy Q&A System

A professional Retrieval Augmented Generation (RAG) system built with Azure AI Search and Azure OpenAI for answering questions about company policy documents.

## 🏗️ Architecture

```
User Question
     ↓
[Azure AI Search] ← Retrieves relevant documents (user-filtered)
     ↓
[Context + Question]
     ↓
[Azure OpenAI] ← Generates accurate answer
     ↓
Answer to User
```

## 📁 Project Structure

```
company-policy-qa/
├── src/
│   ├── config.py              # Configuration management
│   ├── prompts.py             # Reusable prompt library
│   ├── search_service.py      # Azure AI Search operations
│   ├── openai_service.py      # Azure OpenAI operations
│   ├── rag_service.py         # Main RAG orchestrator
│   └── main.py                # Application entry point with menu
│
├── .env                       # Environment variables (create from .env.example)
├── .env.example               # Template for environment variables
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## ✨ Features

- **User-Specific Filtering**: Each user only sees documents in their folder
- **Multiple Query Modes**: 
  - Single question mode
  - Interactive Q&A session
  - Batch question processing
  - Search all documents (no filter)
- **Flexible Prompt Modes**:
  - Strict (default): Only answers from documents
  - Conversational: Friendly tone with clear limitations
  - Detailed: Comprehensive analysis-style responses
- **Safety First**: Explicitly states when information is not found
- **Professional UI**: Clean menu-driven interface with emojis

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Azure subscription with:
  - Azure Storage Account (with blob container)
  - Azure AI Search service (with indexed documents)
  - Azure OpenAI service

### Installation

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**:
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` with your Azure credentials:
   - `STORAGE_ACCOUNT_URL`: Your Azure Storage account URL
   - `CONTAINER_NAME`: Container name (e.g., "studentpdfs")
   - `SEARCH_ENDPOINT`: Azure AI Search endpoint
   - `SEARCH_API_KEY`: Azure AI Search admin key
   - `OPENAI_ENDPOINT`: Azure OpenAI endpoint
   - `OPENAI_API_KEY`: Azure OpenAI API key
   - `OPENAI_DEPLOYMENT`: Your GPT model deployment name

4. **Run the application**:
   ```bash
   python src/main.py
   ```

## 📖 Usage Examples

### Single Question Mode

```
👤 Enter your username: Mukthar
❓ Enter your question: What is the remote work policy?

💡 ANSWER
According to the company policy document, employees are allowed to work 
remotely up to 2 days per week with manager approval...

📚 SOURCES
[1] HR_Policy_2024.pdf
```

### Interactive Mode

```
🤖 Welcome to the Company Policy Q&A Assistant
👤 Logged in as: Mukthar

❓ Your question: What are the sick leave rules?
💡 ANSWER: Employees are entitled to 10 sick days per year...

❓ Your question: exit
👋 Thank you!
```

### Batch Mode

Process multiple questions at once:
```
📝 Enter your questions:
  1. What is vacation policy?
  2. What are working hours?
  3. What is dress code?
  
🔄 Processing 3 questions...
```

## 🎯 How User Filtering Works

The system uses **server-side filtering** in Azure AI Search to ensure each user only sees their documents:

1. Documents are organized by username in the blob container:
   ```
   studentpdfs/
   ├── Mukthar/
   │   ├── policy1.pdf
   │   └── policy2.pdf
   ├── Vijeth/
   │   ├── handbook.pdf
   │   └── guidelines.pdf
   ```

2. The system builds an OData filter:
   ```python
   metadata_storage_path >= 'https://.../studentpdfs/Mukthar/'
   AND metadata_storage_path < 'https://.../studentpdfs/Mukthar/~'
   ```

3. Azure AI Search returns only documents matching that user's folder

## 🔧 Configuration Options

### In `config.py`:

- `default_top_k`: Number of documents to retrieve (default: 3)
- `default_temperature`: Model creativity (0.0-1.0, default: 0.7)

### Prompt Modes:

- **Strict**: Maximum safety, only answers from documents
- **Conversational**: Friendly tone, acknowledges limitations
- **Detailed**: Comprehensive analysis with structured responses

## 🛠️ Development

### Adding New Features

1. **New prompt templates**: Add to `prompts.py`
2. **New search strategies**: Extend `search_service.py`
3. **New generation methods**: Extend `openai_service.py`
4. **New menu options**: Add to `main.py`

### Code Style

- Uses type hints throughout
- Dataclasses for configuration
- Comprehensive error handling
- Clear logging with emojis for user feedback

## 📊 System Testing

Run system diagnostics:
```
Select option: 5 (Test System Connection)

🔧 Testing System Components...
✅ Azure AI Search connection successful
✅ Azure OpenAI connection successful
📄 Total documents in index: 28
```

## ⚠️ Important Notes

1. **No Hallucination Policy**: The system will NOT make up answers. If information isn't in documents, it clearly states this.

2. **Shared Index**: All students share one Azure AI Search index but documents are filtered by username/folder.

3. **Security**: The system filters by `metadata_storage_path` which is set during indexing.

4. **Rate Limits**: Be mindful of Azure OpenAI rate limits when doing batch queries.

## 🐛 Troubleshooting

### "No documents found"
- Check that your username matches your folder name exactly
- Verify the indexer has run and processed your files
- Check container name in `.env`

### "Connection failed"
- Verify all API keys in `.env`
- Check Azure service endpoints are correct
- Ensure services are in the same region

### "Configuration Error"
- Run: `python -c "from src.config import AppConfig; AppConfig.load().validate()"`
- This will show which environment variables are missing

## 📝 Assignment Checklist

- [x] Documents uploaded to Azure Storage
- [x] Azure AI Search index created and populated
- [x] User-specific filtering implemented
- [x] System explicitly states when info not found
- [x] Clean separation of concerns (search, generation, orchestration)
- [x] Professional code structure
- [x] Comprehensive error handling
- [x] User-friendly interface

## 🤝 Contributing

This is an assignment project. For production use, consider adding:
- Authentication/authorization
- Conversation history persistence
- Advanced caching
- Monitoring and logging
- Unit tests
- API endpoint (FastAPI/Flask)

## 📄 License

Educational project for Azure AI learning purposes.

---

**Created for**: Azure AI Document Q&A Assignment  
**Technologies**: Azure AI Search, Azure OpenAI, Python 3.8+  
**Last Updated**: January 2026