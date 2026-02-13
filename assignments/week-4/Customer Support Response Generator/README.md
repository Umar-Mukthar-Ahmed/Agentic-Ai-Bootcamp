# 🎯 AI Marketing Slogan Generator - Streamlit App

A beautiful, production-ready web application for generating marketing slogans using Azure OpenAI and advanced prompt engineering techniques.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)

## ✨ Features

- 🎨 **Three Prompt Styles**: Professional, Creative, and Audience-Focused
- 🎭 **Six Tone Options**: Professional, Friendly, Bold, Playful, Sophisticated, Casual
- 💡 **Real-time Generation**: Powered by Azure OpenAI GPT models
- 📥 **Download Results**: Save generated slogans as text files
- 🔍 **Transparent**: View the exact prompts used for generation
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI API access
- Git

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd marketing-slogan-streamlit
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Configure Azure OpenAI credentials**

Create a `.streamlit/secrets.toml` file:

```toml
AZURE_OPENAI_ENDPOINT = "https://your-endpoint.cognitiveservices.azure.com/"
AZURE_OPENAI_KEY = "your-actual-api-key"
AZURE_OPENAI_DEPLOYMENT = "gpt-4"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"
```

4. **Run the app**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🌐 Deploy to Streamlit Community Cloud

### Step-by-Step Deployment Guide

#### 1. Prepare Your GitHub Repository

1. **Create a new GitHub repository**
   - Go to [GitHub](https://github.com/new)
   - Name it: `marketing-slogan-generator`
   - Make it public
   - Don't initialize with README (we already have one)

2. **Push your code to GitHub**
```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Streamlit marketing slogan generator"

# Add remote (replace with your GitHub username)
git remote add origin https://github.com/YOUR-USERNAME/marketing-slogan-generator.git

# Push to GitHub
git branch -M main
git push -u origin main
```

#### 2. Deploy on Streamlit Community Cloud

1. **Go to Streamlit Community Cloud**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create a new app**
   - Click "New app" button
   - Select your repository: `YOUR-USERNAME/marketing-slogan-generator`
   - Set main file path: `app.py`
   - Choose branch: `main`

3. **Configure Secrets**
   - Click "Advanced settings" before deploying
   - In the "Secrets" section, paste your configuration:

```toml
AZURE_OPENAI_ENDPOINT = "https://your-endpoint.cognitiveservices.azure.com/"
AZURE_OPENAI_KEY = "your-actual-api-key"
AZURE_OPENAI_DEPLOYMENT = "gpt-4"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"
```

4. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for the app to build and start
   - Your app will be live at: `https://YOUR-USERNAME-marketing-slogan-generator.streamlit.app`

#### 3. Update Secrets Later (if needed)

1. Go to your app on Streamlit Cloud
2. Click the menu (⋮) → Settings
3. Select "Secrets" tab
4. Edit and save

## 📁 Project Structure

```
marketing-slogan-streamlit/
│
├── app.py                      # Main Streamlit application
├── src/
│   ├── __init__.py
│   └── prompt_library.py       # Reusable prompt templates
│
├── .streamlit/
│   └── config.toml             # Streamlit theme configuration
│
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## 🎨 Usage Guide

### 1. Generate Slogans Tab

1. Enter your **Product/Service Name** (e.g., "EcoBottle Pro")
2. Describe your **Target Audience** (e.g., "environmentally conscious millennials")
3. Select a **Tone** (professional, friendly, bold, etc.)
4. Choose a **Prompt Style**:
   - **Professional**: Strategic and polished
   - **Creative**: Bold and innovative
   - **Audience-Focused**: Empathetic and relatable
5. Click **"Generate Slogans"**
6. Download your results with the **Download** button

### 2. Examples Tab

View sample outputs to understand what each prompt style produces.

### 3. How It Works Tab

Learn about the prompt engineering techniques and AI process behind the scenes.

## 🔧 Customization

### Adding New Tone Options

Edit `app.py` and add to the tone selectbox:

```python
tone = st.selectbox(
    "Tone",
    ["professional", "friendly", "bold", "playful", "YOUR_NEW_TONE"],
    help="Select the communication style for your slogans"
)
```

### Modifying Prompt Templates

Edit `src/prompt_library.py` to customize the prompt logic:

```python
def professional_slogan_prompt(product_name: str, target_audience: str, tone: str = "professional") -> str:
    # Your custom prompt template
    prompt = f"""Your custom instructions here..."""
    return prompt
```

### Changing Theme Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor="#YOUR_COLOR"
backgroundColor="#YOUR_COLOR"
secondaryBackgroundColor="#YOUR_COLOR"
```

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Error initializing Azure OpenAI client"
- **Solution**: Check that all secrets are configured correctly in Streamlit Cloud settings

**Issue**: "Module not found" error
- **Solution**: Ensure all files are committed to GitHub and `requirements.txt` is correct

**Issue**: App is slow or timing out
- **Solution**: Azure OpenAI API might be rate-limited. Wait a few moments and try again

**Issue**: Changes not reflecting after deployment
- **Solution**: Streamlit Cloud caches aggressively. Click "Reboot app" in the menu (⋮)

## 📊 API Usage & Costs

- Each slogan generation makes 1 API call to Azure OpenAI
- Typical usage: ~500-1000 tokens per request
- Monitor your Azure OpenAI usage in the Azure Portal
- Set spending limits to control costs

## 🔒 Security Best Practices

✅ **Never commit secrets to GitHub**
- Always use Streamlit's secrets management
- Add `.streamlit/secrets.toml` to `.gitignore`

✅ **Use environment variables for sensitive data**
- Keep API keys in Streamlit Cloud secrets
- Rotate keys regularly

✅ **Monitor API usage**
- Check Azure portal for unusual activity
- Set up billing alerts

## 📈 Future Enhancements

- [ ] Add slogan rating/voting system
- [ ] Save favorite slogans to a database
- [ ] A/B testing comparison feature
- [ ] Multi-language support
- [ ] Export to different formats (PDF, CSV, JSON)
- [ ] Integration with social media platforms
- [ ] Batch processing from CSV upload
- [ ] Slogan analytics and insights

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is for educational purposes.

## 👨‍💻 Author

**Umar Mukthar Ahmed**
- AI Engineering Course - Week 3 Assignment
- Enhanced with Streamlit UI for production deployment

## 🙏 Acknowledgments

- Azure OpenAI for the GPT models
- Streamlit for the amazing web framework
- The open-source community

---

**Made with ❤️ using Azure OpenAI, Python, and Streamlit**

🔗 **Live Demo**: [Your Streamlit App URL here]