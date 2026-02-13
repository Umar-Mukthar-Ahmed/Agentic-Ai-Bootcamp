# Customer Support Response Generator

An AI-powered system that generates professional customer support responses using Azure OpenAI.

## 📋 Project Details

**Project Name:** Customer Support Response Generator  
**Purpose:** Automated customer support response generation with reusable prompt templates  
**Technology:** Python, Azure OpenAI API  
**Author:** Umar Mukthar  
**Date:** January 2026

## 📁 Project Structure

```
customer-support-generator/
│
├── src/
│   ├── prompt_library.py       # 3 reusable prompt templates
│   └── main.py                 # Main application with Azure OpenAI integration
│
├── .env                        # Azure OpenAI credentials (not committed to git)
├── .gitignore                  # Git ignore file
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Features

### Three Prompt Templates:

1. **General Support Template**
   - Handles standard customer inquiries
   - Variables: customer_query, product_name, tone

2. **Issue Resolution Template**
   - Addresses specific issue types (billing, technical, delivery, account)
   - Variables: customer_query, issue_type, product_name

3. **Empathy-First Template**
   - De-escalates emotional customers
   - Variables: customer_query, customer_emotion, product_name

### Key Features:
- Dynamic variable injection
- Enterprise-grade constraints (no false promises, professional tone)
- Word limit enforcement (120-150 words)
- Compatible with latest Azure OpenAI models

## ⚙️ Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI Credentials

Edit the `.env` file:
```
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-5.2-chat
```

### 3. Run the Application
```bash
python src/main.py
```

## 📦 Dependencies

- `openai` - Azure OpenAI Python SDK
- `python-dotenv` - Environment variable management

## 🔒 Security

- Never commit `.env` file to version control
- Keep your Azure OpenAI API key secure
- The `.gitignore` file prevents accidental credential commits

## 📄 License

Educational project - Week 4 Assignment