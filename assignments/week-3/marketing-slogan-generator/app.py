"""
Marketing Slogan Generator - Streamlit Web App
==============================================
A beautiful, user-friendly web interface for generating marketing slogans
using Azure OpenAI and reusable prompt templates.
"""

import streamlit as st
import os
from openai import AzureOpenAI
from src.prompt_library import (
    professional_slogan_prompt,
    creative_slogan_prompt,
    audience_focused_prompt
)

# Page configuration
st.set_page_config(
    page_title="AI Marketing Slogan Generator",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .slogan-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #17a2b8;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_azure_client():
    """
    Initialize and cache the Azure OpenAI client.
    Uses Streamlit secrets for secure credential storage.
    """
    try:
        endpoint = st.secrets["AZURE_OPENAI_ENDPOINT"]
        api_key = st.secrets["AZURE_OPENAI_KEY"]
        api_version = st.secrets["AZURE_OPENAI_API_VERSION"]

        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        return client
    except Exception as e:
        st.error(f"Error initializing Azure OpenAI client: {str(e)}")
        return None


def generate_slogan(prompt: str) -> str:
    """
    Send a prompt to Azure OpenAI and retrieve the response.

    Args:
        prompt: The complete prompt string from our prompt library

    Returns:
        Generated slogan text from the API
    """
    client = get_azure_client()

    if client is None:
        return "ERROR: Could not initialize Azure OpenAI client. Please check your configuration."

    try:
        deployment = st.secrets["AZURE_OPENAI_DEPLOYMENT"]

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional marketing expert who creates concise, impactful slogans."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_completion_tokens=16384
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error generating slogan: {str(e)}"


def main():
    """
    Main Streamlit application
    """

    # Header
    st.markdown('<h1 class="main-header">🎯 AI Marketing Slogan Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Create compelling marketing slogans powered by Azure OpenAI</p>',
                unsafe_allow_html=True)

    # Sidebar for configuration
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/3176/3176369.png", width=100)
        st.title("⚙️ Configuration")

        # Check if secrets are configured
        try:
            _ = st.secrets["AZURE_OPENAI_ENDPOINT"]
            st.markdown('<div class="success-box">✅ Azure OpenAI Connected</div>', unsafe_allow_html=True)
        except:
            st.markdown('<div class="info-box">⚠️ Please configure Azure OpenAI secrets</div>', unsafe_allow_html=True)
            st.info("Go to Streamlit Cloud Settings → Secrets to add your Azure OpenAI credentials")

        st.markdown("---")

        st.markdown("### 📖 About")
        st.markdown("""
        This tool uses advanced AI to generate:
        - **Professional** slogans
        - **Creative** taglines
        - **Audience-focused** messages

        Perfect for marketers, entrepreneurs, and creative professionals!
        """)

        # st.markdown("---")
        # st.markdown("### 🔗 Resources")
        # st.markdown("[📚 Documentation](https://github.com)")
        # st.markdown("[💡 Prompt Engineering Tips](https://docs.anthropic.com)")

        st.markdown("---")
        st.markdown("Made with ❤️ by **Umar Mukthar Ahmed**")

    # Main content area with tabs
    tab1, tab2, tab3 = st.tabs(["🚀 Generate Slogans", "🎨 Examples", "ℹ️ How It Works"])

    with tab1:
        st.markdown("## Create Your Marketing Slogans")

        # Input form
        col1, col2 = st.columns(2)

        with col1:
            product_name = st.text_input(
                "Product/Service Name",
                placeholder="e.g., EcoBottle Pro",
                help="Enter the name of your product or service"
            )

            target_audience = st.text_input(
                "Target Audience",
                placeholder="e.g., environmentally conscious millennials",
                help="Describe your ideal customer demographic"
            )

        with col2:
            tone = st.selectbox(
                "Tone",
                ["professional", "friendly", "bold", "playful", "sophisticated", "casual"],
                help="Select the communication style for your slogans"
            )

            prompt_style = st.selectbox(
                "Prompt Style",
                ["Professional", "Creative", "Audience-Focused"],
                help="Choose the approach for slogan generation"
            )

        # Generate button
        st.markdown("<br>", unsafe_allow_html=True)

        col_button1, col_button2, col_button3 = st.columns([1, 1, 1])
        with col_button2:
            generate_button = st.button("🎯 Generate Slogans", type="primary", use_container_width=True)

        # Generation logic
        if generate_button:
            if not product_name or not target_audience:
                st.warning("⚠️ Please fill in both Product Name and Target Audience fields.")
            else:
                # Show loading spinner
                with st.spinner("🤖 AI is crafting your perfect slogans..."):
                    # Select appropriate prompt
                    if prompt_style == "Professional":
                        prompt = professional_slogan_prompt(product_name, target_audience, tone)
                        icon = "💼"
                    elif prompt_style == "Creative":
                        prompt = creative_slogan_prompt(product_name, target_audience, tone)
                        icon = "🎨"
                    else:
                        prompt = audience_focused_prompt(product_name, target_audience, tone)
                        icon = "👥"

                    # Generate slogans
                    result = generate_slogan(prompt)

                    # Display results
                    st.markdown("---")
                    st.markdown(f"## {icon} Your {prompt_style} Slogans")

                    st.markdown(f'<div class="slogan-box">{result}</div>', unsafe_allow_html=True)

                    # Download button
                    st.download_button(
                        label="📥 Download Slogans",
                        data=f"Product: {product_name}\nAudience: {target_audience}\nTone: {tone}\nStyle: {prompt_style}\n\n{result}",
                        file_name=f"slogans_{product_name.replace(' ', '_')}.txt",
                        mime="text/plain"
                    )

                    # Show prompt (expandable)
                    with st.expander("🔍 View the AI Prompt Used"):
                        st.code(prompt, language="text")

    with tab2:
        st.markdown("## 🎨 Example Slogans")

        st.markdown("### Sample Output: EcoBottle Pro")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("#### 💼 Professional")
            st.markdown("""
            <div class="slogan-box">
            <strong>Slogan 1:</strong> Drink Clean, Live Green<br><br>
            <strong>Slogan 2:</strong> Your Daily Dose of Sustainability<br><br>
            <strong>Slogan 3:</strong> Eco-Friendly Hydration, Simplified<br><br>
            <em>These slogans emphasize environmental benefits with an approachable tone.</em>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("#### 🎨 Creative")
            st.markdown("""
            <div class="slogan-box">
            <strong>Slogan 1:</strong> Hydration Meets Revolution<br><br>
            <strong>Slogan 2:</strong> Bottle the Future<br><br>
            <strong>Slogan 3:</strong> Sip Smarter, Planet Happier<br><br>
            <em>Bold and innovative approach to environmental messaging.</em>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("#### 👥 Audience-Focused")
            st.markdown("""
            <div class="slogan-box">
            <strong>Slogan 1:</strong> Because Your Values Matter<br><br>
            <strong>Slogan 2:</strong> Join the Hydration Movement<br><br>
            <strong>Slogan 3:</strong> Your Choice, Our Planet<br><br>
            <em>Resonates with environmentally conscious millennials.</em>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        st.info("💡 **Tip:** Try different combinations of tone and style to find the perfect message for your brand!")

    with tab3:
        st.markdown("## ℹ️ How It Works")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 🎯 The Process")
            st.markdown("""
            1. **Input Variables**
               - You provide product name, target audience, and tone

            2. **Prompt Engineering**
               - Your inputs are injected into expertly crafted prompt templates
               - Templates follow Role-Task-Constraints pattern

            3. **AI Generation**
               - Azure OpenAI processes the prompt
               - Generates 3 unique, compelling slogans

            4. **Refinement**
               - Each slogan is crafted to be memorable and concise
               - Follows marketing best practices
            """)

        with col2:
            st.markdown("### 🎨 Three Prompt Styles")
            st.markdown("""
            **💼 Professional**
            - Strategic and polished
            - Best for: Enterprise, B2B, professional services

            **🎨 Creative**
            - Bold and innovative
            - Best for: Startups, lifestyle brands, tech products

            **👥 Audience-Focused**
            - Empathetic and relatable
            - Best for: Non-profits, health & wellness, education
            """)

        st.markdown("---")

        st.markdown("### 🔑 Key Features")

        feature_col1, feature_col2, feature_col3 = st.columns(3)

        with feature_col1:
            st.markdown("""
            **✅ Reusable Templates**
            - Same quality for all products
            - Consistent output standards
            """)

        with feature_col2:
            st.markdown("""
            **⚡ Fast Generation**
            - Results in seconds
            - Powered by Azure OpenAI
            """)

        with feature_col3:
            st.markdown("""
            **🎨 Multiple Styles**
            - 3 different approaches
            - 6 tone options
            """)

        st.markdown("---")

        st.markdown("### 📚 Prompt Engineering Principles")

        st.code("""
# Every prompt includes:

1. ROLE: "You are an expert marketing copywriter..."
   → Sets the AI's expertise and perspective

2. TASK: "Create 3 compelling marketing slogans..."
   → Clear instructions on what to produce

3. CONSTRAINTS: "Each slogan must be 3-8 words..."
   → Boundaries that ensure quality
        """, language="python")


if __name__ == "__main__":
    main()
