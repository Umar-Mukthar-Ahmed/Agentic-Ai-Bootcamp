# Marketing Slogan Generator

A professional AI-powered tool that generates creative marketing slogans using Azure OpenAI and reusable prompt templates.

---

## 📁 Project Structure

```
marketing-slogan-generator/
│
├── src/
│   ├── prompt_library.py      # Reusable prompt templates
│   └── main.py                # Main application with menu
│
├── .env                       # Azure OpenAI credentials
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Azure OpenAI

Create a `.env` file in the project root:

```env
AZURE_OPENAI_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_KEY=your-actual-api-key
AZURE_OPENAI_DEPLOYMENT=gpt-5.2-chat
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

### 3. Run the Application

```bash
python src/main.py
```

---

## 🎯 Features

### Menu Options

When you run the program, you'll see:

1. **Run Demo** - See example slogans for "EcoBottle Pro"
2. **Interactive Mode** - Generate slogans for your own product
3. **Exit** - Close the application

### Three Slogan Styles

1. **Professional Approach**
   - Strategic and polished
   - Best for: Enterprise products, professional services

2. **Creative Approach**
   - Bold and innovative
   - Best for: Startups, lifestyle brands, tech products

3. **Audience-Focused Approach**
   - Empathetic and relatable
   - Best for: Non-profits, health & wellness, education

---

## 💡 How It Works

### 1. Prompt Templates (`prompt_library.py`)

Three reusable functions that create structured prompts:

```python
professional_slogan_prompt(product_name, target_audience, tone)
creative_slogan_prompt(product_name, target_audience, tone)
audience_focused_prompt(product_name, target_audience, tone)
```

Each template follows the **Role-Task-Constraints** pattern:
- **Role**: Who the AI should act as (marketing expert, creative director, etc.)
- **Task**: What to create (3 compelling slogans)
- **Constraints**: Requirements (word limits, tone, no false claims)

### 2. Variable Injection

Variables are dynamically inserted into prompts:

```python
product_name = "SmartWatch Elite"
target_audience = "fitness enthusiasts aged 25-40"
tone = "bold"

prompt = professional_slogan_prompt(product_name, target_audience, tone)
```

The same template works for ANY product by changing these variables!

### 3. Azure OpenAI Integration (`main.py`)

The `generate_slogan()` function sends prompts to Azure OpenAI:

```python
def generate_slogan(prompt: str) -> str:
    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key
    )
    
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": "You are a professional marketing expert..."},
            {"role": "user", "content": prompt}
        ],
        max_completion_tokens=16384
    )
    
    return response.choices[0].message.content
```

---

## 📝 Example Usage

### Demo Mode Output

```
======================================================================
MARKETING SLOGAN GENERATOR
======================================================================

INPUT VARIABLES:
  Product: EcoBottle Pro
  Target Audience: environmentally conscious millennials
  Tone: friendly

======================================================================
PROFESSIONAL APPROACH
======================================================================

Slogan 1: Drink Clean, Live Green
Slogan 2: Your Daily Dose of Sustainability
Slogan 3: Eco-Friendly Hydration, Simplified

Brief Explanation: These slogans emphasize environmental benefits while 
maintaining an approachable, friendly tone that resonates with millennials.
```

### Interactive Mode

```
Enter product name: SmartWatch Elite
Enter target audience: fitness enthusiasts aged 25-40

Available tones: professional, friendly, bold, playful
Enter desired tone: bold

Available prompt styles:
  1. Professional (strategic and polished)
  2. Creative (bold and innovative)
  3. Audience-Focused (empathetic and relatable)

Select prompt style (1-3): 2

======================================================================
CREATIVE APPROACH
======================================================================

[Generated slogans appear here]
```

---

## 🎓 Key Concepts

### Why Reusable Prompts Matter

✅ **Consistency** - Same quality standards for all products  
✅ **Efficiency** - Write once, use everywhere  
✅ **Scalability** - Handle multiple products easily  
✅ **Maintainability** - Update one template, improve all outputs

### Role-Task-Constraints Pattern

Every prompt includes:

1. **Role**: "You are an expert marketing copywriter..."
   - Sets the AI's expertise and perspective

2. **Task**: "Create 3 compelling marketing slogans..."
   - Clear instructions on what to produce

3. **Constraints**: "Each slogan must be 3-8 words..."
   - Boundaries that ensure quality and appropriateness

---

## 🔧 Customization

### Adding New Prompt Styles

Edit `prompt_library.py` and add a new function:

```python
def your_new_prompt(product_name: str, target_audience: str, tone: str) -> str:
    prompt = f"""You are a [role]...
    
    Product: {product_name}
    Target Audience: {target_audience}
    Desired Tone: {tone}
    
    Requirements:
    1. [Your constraint]
    2. [Your constraint]
    ...
    """
    return prompt
```

Then import and use it in `main.py`.

### Changing API Parameters

In `main.py`, modify the `generate_slogan()` function:

```python
response = client.chat.completions.create(
    model=deployment,
    messages=[...],
    max_completion_tokens=16384  # Adjust as needed
)
```

---

## 📦 Dependencies

- `openai>=1.0.0` - Azure OpenAI Python SDK
- `python-dotenv>=1.0.0` - Environment variable management

---

## 🛠️ Troubleshooting

### Error: "Missing Azure OpenAI configuration"
- Check that your `.env` file exists in the project root
- Verify all four variables are set correctly

### Error: "Unsupported value: temperature"
- This is already fixed - the code uses only supported parameters

### No output or slow response
- Check your internet connection
- Verify your Azure OpenAI endpoint is active
- Ensure you have sufficient API quota

---

## 📚 Learning Outcomes

This project demonstrates:

1. **Prompt Engineering** - Creating effective, reusable prompts
2. **Variable Injection** - Dynamic content generation
3. **API Integration** - Professional Azure OpenAI usage
4. **Clean Code** - Separation of concerns and maintainability
5. **User Experience** - Menu-driven interface design

---

## 🎯 Next Steps

Potential enhancements:

- Save generated slogans to a file
- Compare multiple slogan variations side-by-side
- Add more tone options (playful, serious, humorous)
- Batch process multiple products from a CSV file
- Add slogan rating/feedback system

---

## 📄 License

This project is for educational purposes.

---

## 👤 Author

Umar Mukthar  
AI Engineering Course - Week 3 Assignment

---

**Made with ❤️ using Azure OpenAI and Python**
