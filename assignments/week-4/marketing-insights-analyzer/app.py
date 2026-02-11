"""
Marketing Insights Analyzer - Streamlit Web Application
========================================================
A professional web interface for comparing Azure OpenAI vs Baseline
feedback analysis approaches.
"""

import streamlit as st
import nltk
import sys
import subprocess
import os


# ============================================================================
# DEPENDENCY MANAGEMENT FOR STREAMLIT CLOUD
# ============================================================================

@st.cache_resource
def download_dependencies():
    """Download required NLP models on first run (Streamlit Cloud compatible)"""
    try:
        # Configure SSL for NLTK downloads
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context

        # Download NLTK data
        nltk.download('vader_lexicon', quiet=True)

        # Download spaCy model
        try:
            import spacy
            spacy.load("en_core_web_sm")
        except OSError:
            subprocess.check_call([
                sys.executable, "-m", "spacy", "download", "en_core_web_sm", "--quiet"
            ])

        return True
    except Exception as e:
        st.warning(f"Note: Some NLP features may be limited. Error: {str(e)}")
        return False


# Run dependency check
if 'dependencies_loaded' not in st.session_state:
    with st.spinner("🔄 Loading NLP models (first time only)..."):
        st.session_state.dependencies_loaded = download_dependencies()

# ============================================================================
# IMPORTS
# ============================================================================

import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import time

# Import custom modules
from src.azure_analyzer import AzureInsightsAnalyzer
from src.baseline_analyzer import BaselineInsightsAnalyzer
from src.comparison import ResultsComparison
from src.config import Config

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Marketing Insights Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# CUSTOM STYLING
# ============================================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background-color: #1e4620;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #014451;
        border-left: 5px solid #17a2b8;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #664d03;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if 'azure_results' not in st.session_state:
    st.session_state.azure_results = None
if 'baseline_results' not in st.session_state:
    st.session_state.baseline_results = None
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False

# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:
    st.markdown("### 📊 Marketing Insights Analyzer")
    st.divider()

    # Navigation
    page = st.radio(
        "Navigation",
        ["🏠 Home", "🔬 Quick Test", "📊 Run Analysis", "📈 View Results", "🔍 Compare", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.divider()

    # Configuration Status
    st.markdown("### ⚙️ Configuration")

    if Config.is_configured():
        st.success("✅ Azure OpenAI Connected")
        config_info = Config.get_config_info()
        with st.expander("ℹ️ Config Details"):
            st.json(config_info)
    else:
        st.error("❌ Azure Not Configured")
        st.info("Add secrets in Streamlit Cloud or create .env locally")

    st.divider()

    # Quick Stats
    st.markdown("### 📊 Quick Stats")

    try:
        with open(Config.DATA_PATH, 'r') as f:
            feedback_data = json.load(f)
        st.metric("Total Feedbacks", len(feedback_data))
    except:
        st.metric("Total Feedbacks", "N/A")

    if st.session_state.analysis_complete:
        st.metric("Analysis Status", "✅ Complete")
    else:
        st.metric("Analysis Status", "⏳ Pending")

# ============================================================================
# MAIN CONTENT - HOME PAGE
# ============================================================================

if page == "🏠 Home":
    st.markdown('<div class="main-header">📊 Marketing Insights Analyzer</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <h3>🎯 Project Overview</h3>
        <p>Compare <strong>AI-powered (Azure OpenAI)</strong> vs <strong>Rule-based (Baseline)</strong> 
        approaches for customer feedback analysis.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🤖 Azure OpenAI")
        st.markdown("""
        - Context-aware sentiment analysis
        - Intelligent theme extraction
        - Actionable suggestions
        - Emotional tone detection
        - Urgency assessment
        """)
        st.info("**Best for:** Complex feedback, nuanced analysis")

    with col2:
        st.markdown("### ⚙️ Baseline")
        st.markdown("""
        - Keyword-based matching
        - Pattern detection
        - Rule-based classification
        - Generic suggestions
        - Zero-cost operation
        """)
        st.info("**Best for:** High volume, budget constraints")

    st.divider()

    st.markdown("### 🚀 How It Works")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        #### 1️⃣ Input
        - Customer reviews
        - Survey responses
        - Support tickets
        - Social media feedback
        """)

    with col2:
        st.markdown("""
        #### 2️⃣ Process
        - Azure OpenAI analysis
        - Baseline analysis
        - Parallel processing
        """)

    with col3:
        st.markdown("""
        #### 3️⃣ Output
        - Sentiment scores
        - Key themes
        - Suggestions
        - Comparison metrics
        """)

    st.divider()
    st.success("👉 **Get Started:** Try '🔬 Quick Test' for a single review or '📊 Run Analysis' for batch processing!")

# ============================================================================
# QUICK TEST PAGE
# ============================================================================

elif page == "🔬 Quick Test":
    st.markdown('<div class="main-header">🔬 Quick Test - Single Review Analysis</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-box">
        <p>Test a single customer review and see <strong>real-time comparison</strong> between approaches.</p>
    </div>
    """, unsafe_allow_html=True)

    # Example reviews
    st.markdown("### 💡 Example Reviews")

    example_reviews = {
        "😊 Positive": "Excellent product quality! Fast shipping and great customer service. Highly recommended!",
        "😐 Neutral": "The product is okay, but the website is confusing. Checkout needs improvement.",
        "😠 Negative": "Terrible experience. Item arrived broken and support was unhelpful. Won't buy again.",
        "😏 Sarcastic": "Oh great, another late delivery. Just what I needed! Support was 'incredibly helpful' too.",
        "🤔 Complex": "Product quality is amazing, but delivery took 3 weeks. Support tried to help but couldn't track my package."
    }

    with st.expander("📝 Click to see examples", expanded=False):
        for label, review in example_reviews.items():
            st.markdown(f"**{label}**")
            st.code(review, language=None)

    st.divider()

    # Input area
    st.markdown("### ✍️ Enter Customer Review")

    review_text = st.text_area(
        "Type or paste a customer review:",
        value="",
        height=150,
        placeholder="Example: The delivery was late and the packaging was damaged...",
        key="review_input"
    )

    # Analyze button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        analyze_button = st.button("🚀 Analyze Review", type="primary", use_container_width=True)

    if analyze_button and review_text.strip():
        st.markdown("---")
        st.markdown("### 📊 Analysis Results")

        col_azure, col_baseline = st.columns(2)

        # Azure Analysis
        with col_azure:
            st.markdown("#### 🤖 Azure OpenAI Analysis")

            if not Config.is_configured():
                st.error("❌ Azure OpenAI not configured. Please add your credentials in Streamlit secrets.")
            else:
                with st.spinner("Analyzing with Azure AI..."):
                    try:
                        azure_analyzer = AzureInsightsAnalyzer()
                        azure_result = azure_analyzer.analyze_feedback(review_text, 1)

                        if 'error' in azure_result:
                            st.error(f"❌ Error: {azure_result['error']}")
                        else:
                            # Sentiment card
                            sentiment_color = {
                                'positive': '#28a745',
                                'neutral': '#ffc107',
                                'negative': '#dc3545'
                            }.get(azure_result.get('sentiment', 'neutral'), '#6c757d')

                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, {sentiment_color} 0%, {sentiment_color}dd 100%); 
                                        padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
                                <h3 style="margin: 0; color: white;">
                                    {azure_result.get('sentiment', 'N/A').upper()}
                                </h3>
                                <p style="margin: 0; opacity: 0.9;">
                                    Score: {azure_result.get('sentiment_score', 0)}
                                </p>
                            </div>
                            """, unsafe_allow_html=True)

                            # Key Themes
                            st.markdown("**🎯 Key Themes:**")
                            themes = azure_result.get('key_themes', [])
                            if themes:
                                for theme in themes:
                                    st.markdown(f"• {theme}")
                            else:
                                st.markdown("• No themes detected")

                            # Complaints
                            st.markdown("**😟 Complaints:**")
                            complaints = azure_result.get('complaints', [])
                            if complaints:
                                for complaint in complaints:
                                    st.markdown(f"• {complaint}")
                            else:
                                st.markdown("• No complaints")

                            # Positive Aspects
                            st.markdown("**😊 Positive Aspects:**")
                            positives = azure_result.get('positive_aspects', [])
                            if positives:
                                for positive in positives:
                                    st.markdown(f"• {positive}")
                            else:
                                st.markdown("• None mentioned")

                            # Improvements
                            st.markdown("**💡 Improvement Suggestions:**")
                            suggestions = azure_result.get('improvement_suggestions', [])
                            if suggestions:
                                for suggestion in suggestions:
                                    st.markdown(f"• {suggestion}")
                            else:
                                st.markdown("• No suggestions")

                            # Metadata
                            st.markdown("**📊 Additional Insights:**")
                            st.markdown(f"• **Urgency:** {azure_result.get('urgency_level', 'N/A')}")
                            st.markdown(f"• **Emotion:** {azure_result.get('customer_emotion', 'N/A')}")
                            st.markdown(f"• **Processing Time:** {azure_result.get('processing_time_seconds', 0):.3f}s")
                            tokens = azure_result.get('tokens_used', {}).get('total', 0)
                            st.markdown(f"• **Tokens Used:** {tokens}")
                            cost = (tokens / 1000 * 0.03)
                            st.markdown(f"• **Estimated Cost:** ${cost:.5f}")

                    except Exception as e:
                        st.error(f"❌ Azure analysis failed: {str(e)}")

        # Baseline Analysis
        with col_baseline:
            st.markdown("#### ⚙️ Baseline Analysis")

            with st.spinner("Analyzing with Baseline..."):
                try:
                    baseline_analyzer = BaselineInsightsAnalyzer()
                    baseline_result = baseline_analyzer.analyze_feedback(review_text, 1)

                    if 'error' in baseline_result:
                        st.error(f"❌ Error: {baseline_result['error']}")
                    else:
                        # Sentiment card
                        sentiment_color = {
                            'positive': '#28a745',
                            'neutral': '#ffc107',
                            'negative': '#dc3545'
                        }.get(baseline_result.get('sentiment', 'neutral'), '#6c757d')

                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, {sentiment_color} 0%, {sentiment_color}dd 100%); 
                                    padding: 1rem; border-radius: 10px; color: white; margin-bottom: 1rem;">
                            <h3 style="margin: 0; color: white;">
                                {baseline_result.get('sentiment', 'N/A').upper()}
                            </h3>
                            <p style="margin: 0; opacity: 0.9;">
                                Score: {baseline_result.get('sentiment_score', 0)}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)

                        # Key Themes
                        st.markdown("**🎯 Key Themes:**")
                        themes = baseline_result.get('key_themes', [])
                        if themes:
                            for theme in themes:
                                st.markdown(f"• {theme}")
                        else:
                            st.markdown("• No themes detected")

                        # Complaints
                        st.markdown("**😟 Complaints:**")
                        complaints = baseline_result.get('complaints', [])
                        if complaints:
                            for complaint in complaints:
                                st.markdown(f"• {complaint}")
                        else:
                            st.markdown("• No complaints")

                        # Positive Aspects
                        st.markdown("**😊 Positive Aspects:**")
                        positives = baseline_result.get('positive_aspects', [])
                        if positives:
                            for positive in positives:
                                st.markdown(f"• {positive}")
                        else:
                            st.markdown("• None mentioned")

                        # Improvements
                        st.markdown("**💡 Improvement Suggestions:**")
                        suggestions = baseline_result.get('improvement_suggestions', [])
                        if suggestions:
                            for suggestion in suggestions:
                                st.markdown(f"• {suggestion}")
                        else:
                            st.markdown("• No suggestions")

                        # Metadata
                        st.markdown("**📊 Additional Insights:**")
                        st.markdown(f"• **Urgency:** {baseline_result.get('urgency_level', 'N/A')}")
                        st.markdown(f"• **Emotion:** {baseline_result.get('customer_emotion', 'N/A')}")
                        st.markdown(f"• **Processing Time:** {baseline_result.get('processing_time_seconds', 0):.4f}s")
                        st.markdown(f"• **Cost:** $0.00")

                except Exception as e:
                    st.error(f"❌ Baseline analysis failed: {str(e)}")

        # Comparison summary
        if 'azure_result' in locals() and 'baseline_result' in locals():
            if 'error' not in azure_result and 'error' not in baseline_result:
                st.markdown("---")
                st.markdown("### 🔍 Quick Comparison")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    sentiment_match = azure_result.get('sentiment') == baseline_result.get('sentiment')
                    if sentiment_match:
                        st.success("✅ Sentiment Match")
                    else:
                        st.warning("⚠️ Sentiment Differs")

                with col2:
                    azure_time = azure_result.get('processing_time_seconds', 0)
                    baseline_time = baseline_result.get('processing_time_seconds', 0.001)
                    speed_ratio = azure_time / baseline_time if baseline_time > 0 else 0
                    st.info(f"⚡ Baseline {speed_ratio:.0f}x faster")

                with col3:
                    azure_cost = azure_result.get('tokens_used', {}).get('total', 0) / 1000 * 0.03
                    st.metric("💰 Azure Cost", f"${azure_cost:.5f}")

                with col4:
                    azure_themes = len(azure_result.get('key_themes', []))
                    baseline_themes = len(baseline_result.get('key_themes', []))
                    st.metric("🎯 Themes", f"{azure_themes} vs {baseline_themes}")

    elif analyze_button:
        st.warning("⚠️ Please enter a customer review to analyze.")

# ============================================================================
# RUN ANALYSIS PAGE
# ============================================================================

elif page == "📊 Run Analysis":
    st.markdown('<div class="main-header">📊 Run Batch Analysis</div>', unsafe_allow_html=True)

    # Display sample data
    st.markdown("### 📝 Sample Feedback Data")

    try:
        with open(Config.DATA_PATH, 'r') as f:
            feedback_data = json.load(f)

        df_preview = pd.DataFrame(feedback_data)
        st.dataframe(df_preview, use_container_width=True, height=300)

        st.info(f"📊 **{len(feedback_data)} feedback entries** loaded and ready for analysis")

    except Exception as e:
        st.error(f"❌ Error loading feedback data: {str(e)}")
        st.stop()

    st.divider()

    # Analysis controls
    st.markdown("### 🎮 Analysis Controls")

    col1, col2 = st.columns([3, 1])

    with col1:
        st.markdown("""
        Click the button below to start batch analysis:
        1. 🤖 Run Azure OpenAI analysis
        2. ⚙️ Run baseline analysis
        3. 📊 Generate comparison metrics
        4. 💾 Save results
        """)

    with col2:
        analyze_button = st.button("🚀 Start Analysis", type="primary", use_container_width=True)

    if analyze_button:
        if not Config.is_configured():
            st.error("❌ Azure OpenAI not configured. Analysis cannot proceed.")
            st.info("Please add your Azure credentials in Streamlit Cloud settings → Secrets")
            st.stop()

        # Create results directory
        Path("data/results").mkdir(parents=True, exist_ok=True)

        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()

        try:
            # Phase 1: Azure OpenAI
            status_text.markdown("### 🤖 Phase 1: Azure OpenAI Analysis")
            progress_bar.progress(10)

            azure_expander = st.expander("📊 Azure Analysis Progress", expanded=True)

            with azure_expander:
                azure_progress = st.progress(0)
                azure_status = st.empty()

                azure_analyzer = AzureInsightsAnalyzer()
                results = []
                total_tokens = 0

                for idx, item in enumerate(feedback_data):
                    azure_status.text(f"Analyzing feedback {idx + 1}/{len(feedback_data)}...")

                    result = azure_analyzer.analyze_feedback(item['feedback'], item['id'])
                    results.append(result)

                    if 'tokens_used' in result:
                        total_tokens += result['tokens_used']['total']

                    azure_progress.progress((idx + 1) / len(feedback_data))
                    time.sleep(0.3)

                st.session_state.azure_results = results
                azure_analyzer.save_results(results, Config.AZURE_RESULTS_PATH)

                st.success(f"✅ Azure analysis complete! Total tokens: {total_tokens}")

            progress_bar.progress(60)

            # Phase 2: Baseline
            status_text.markdown("### ⚙️ Phase 2: Baseline Analysis")
            progress_bar.progress(65)

            baseline_expander = st.expander("📊 Baseline Analysis Progress", expanded=True)

            with baseline_expander:
                baseline_progress = st.progress(0)
                baseline_status = st.empty()

                baseline_analyzer = BaselineInsightsAnalyzer()
                baseline_results = []

                for idx, item in enumerate(feedback_data):
                    baseline_status.text(f"Analyzing feedback {idx + 1}/{len(feedback_data)}...")

                    result = baseline_analyzer.analyze_feedback(item['feedback'], item['id'])
                    baseline_results.append(result)

                    baseline_progress.progress((idx + 1) / len(feedback_data))

                st.session_state.baseline_results = baseline_results
                baseline_analyzer.save_results(baseline_results, Config.BASELINE_RESULTS_PATH)

                st.success("✅ Baseline analysis complete! Cost: $0.00")

            progress_bar.progress(90)

            # Mark complete
            st.session_state.analysis_complete = True

            progress_bar.progress(100)
            status_text.markdown("### ✅ Analysis Complete!")

            st.balloons()
            st.success("🎉 **Both analyses completed!** Go to 'View Results' to see the output.")

        except Exception as e:
            st.error(f"❌ **Analysis failed:** {str(e)}")
            st.exception(e)

# ============================================================================
# VIEW RESULTS PAGE
# ============================================================================

elif page == "📈 View Results":
    st.markdown('<div class="main-header">📈 Analysis Results</div>', unsafe_allow_html=True)

    if not st.session_state.analysis_complete:
        st.warning("⚠️ **No analysis results available.** Run the analysis first.")
        st.stop()

    tab1, tab2 = st.tabs(["🤖 Azure OpenAI Results", "⚙️ Baseline Results"])

    with tab1:
        st.markdown("### 🤖 Azure OpenAI Analysis Results")

        if st.session_state.azure_results:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            total_tokens = sum(r.get('tokens_used', {}).get('total', 0) for r in st.session_state.azure_results)
            avg_time = sum(r.get('processing_time_seconds', 0) for r in st.session_state.azure_results) / len(
                st.session_state.azure_results)
            estimated_cost = (total_tokens / 1000) * 0.03

            with col1:
                st.metric("Total Feedbacks", len(st.session_state.azure_results))
            with col2:
                st.metric("Total Tokens", f"{total_tokens:,}")
            with col3:
                st.metric("Avg Time/Feedback", f"{avg_time:.3f}s")
            with col4:
                st.metric("Estimated Cost", f"${estimated_cost:.4f}")

            st.divider()

            # Sentiment distribution
            sentiments = [r.get('sentiment', 'unknown') for r in st.session_state.azure_results]
            sentiment_counts = pd.Series(sentiments).value_counts()

            fig_sentiment = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Distribution",
                color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)

            st.divider()

            # Detailed results
            st.markdown("### 📋 Detailed Results")

            results_df = pd.DataFrame([
                {
                    'ID': r['feedback_id'],
                    'Sentiment': r.get('sentiment', 'N/A'),
                    'Score': r.get('sentiment_score', 0),
                    'Themes': ', '.join(r.get('key_themes', [])),
                    'Urgency': r.get('urgency_level', 'N/A'),
                    'Emotion': r.get('customer_emotion', 'N/A'),
                    'Tokens': r.get('tokens_used', {}).get('total', 0)
                }
                for r in st.session_state.azure_results
            ])

            st.dataframe(results_df, use_container_width=True, height=400)

            # Download
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="azure_results.csv",
                mime="text/csv"
            )

    with tab2:
        st.markdown("### ⚙️ Baseline Analysis Results")

        if st.session_state.baseline_results:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            avg_time = sum(r.get('processing_time_seconds', 0) for r in st.session_state.baseline_results) / len(
                st.session_state.baseline_results)

            with col1:
                st.metric("Total Feedbacks", len(st.session_state.baseline_results))
            with col2:
                st.metric("Total Cost", "$0.00")
            with col3:
                st.metric("Avg Time/Feedback", f"{avg_time:.4f}s")
            with col4:
                st.metric("Speed Advantage", "~1000x faster")

            st.divider()

            # Sentiment distribution
            sentiments = [r.get('sentiment', 'unknown') for r in st.session_state.baseline_results]
            sentiment_counts = pd.Series(sentiments).value_counts()

            fig_sentiment = px.pie(
                values=sentiment_counts.values,
                names=sentiment_counts.index,
                title="Sentiment Distribution",
                color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
            )
            st.plotly_chart(fig_sentiment, use_container_width=True)

            st.divider()

            # Detailed results
            st.markdown("### 📋 Detailed Results")

            results_df = pd.DataFrame([
                {
                    'ID': r['feedback_id'],
                    'Sentiment': r.get('sentiment', 'N/A'),
                    'Score': r.get('sentiment_score', 0),
                    'Themes': ', '.join(r.get('key_themes', [])),
                    'Urgency': r.get('urgency_level', 'N/A'),
                    'Emotion': r.get('customer_emotion', 'N/A')
                }
                for r in st.session_state.baseline_results
            ])

            st.dataframe(results_df, use_container_width=True, height=400)

            # Download
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name="baseline_results.csv",
                mime="text/csv"
            )

# ============================================================================
# COMPARE APPROACHES PAGE
# ============================================================================

elif page == "🔍 Compare":
    st.markdown('<div class="main-header">🔍 Approach Comparison</div>', unsafe_allow_html=True)

    if not st.session_state.analysis_complete:
        st.warning("⚠️ **No comparison data available.** Please run the analysis first.")
        st.stop()

    # Load comparison
    comparison = ResultsComparison(
        Config.AZURE_RESULTS_PATH,
        Config.BASELINE_RESULTS_PATH
    )

    metrics = comparison.calculate_metrics()

    if not metrics:
        st.error("❌ Unable to load comparison data.")
        st.stop()

    # Comparison table
    st.markdown("### 📊 Performance Metrics Comparison")

    comparison_df = pd.DataFrame(metrics).T
    st.dataframe(comparison_df, use_container_width=True)

    st.divider()

    # Visual comparisons
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### ⏱️ Processing Speed")

        fig_speed = go.Figure(data=[
            go.Bar(
                x=['Azure OpenAI', 'Baseline'],
                y=[
                    metrics['Azure OpenAI']['Avg Processing Time (s)'],
                    metrics['Baseline']['Avg Processing Time (s)']
                ],
                marker_color=['#0078d4', '#107c10'],
                text=[
                    f"{metrics['Azure OpenAI']['Avg Processing Time (s)']:.4f}s",
                    f"{metrics['Baseline']['Avg Processing Time (s)']:.4f}s"
                ],
                textposition='auto',
            )
        ])
        fig_speed.update_layout(
            yaxis_title="Seconds per Feedback",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_speed, use_container_width=True)

    with col2:
        st.markdown("#### 💰 Cost Comparison")

        fig_cost = go.Figure(data=[
            go.Bar(
                x=['Azure OpenAI', 'Baseline'],
                y=[
                    metrics['Azure OpenAI']['Estimated Cost ($)'],
                    metrics['Baseline']['Estimated Cost ($)']
                ],
                marker_color=['#0078d4', '#107c10'],
                text=[
                    f"${metrics['Azure OpenAI']['Estimated Cost ($)']:.4f}",
                    "$0.00"
                ],
                textposition='auto',
            )
        ])
        fig_cost.update_layout(
            yaxis_title="Total Cost (USD)",
            showlegend=False,
            height=400
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    st.divider()

    # Sentiment comparison
    st.markdown("### 📈 Sentiment Distribution Comparison")

    col1, col2 = st.columns(2)

    sentiment_comp = comparison.sentiment_comparison()

    with col1:
        azure_sent = sentiment_comp.get('Azure OpenAI', {})
        if azure_sent:
            fig1 = px.pie(
                values=list(azure_sent.values()),
                names=list(azure_sent.keys()),
                title="Azure OpenAI Sentiment",
                color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
            )
            st.plotly_chart(fig1, use_container_width=True)

    with col2:
        baseline_sent = sentiment_comp.get('Baseline', {})
        if baseline_sent:
            fig2 = px.pie(
                values=list(baseline_sent.values()),
                names=list(baseline_sent.keys()),
                title="Baseline Sentiment",
                color_discrete_sequence=['#28a745', '#ffc107', '#dc3545']
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # Key findings
    st.markdown("### 🔑 Key Findings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="success-box">
            <h4>✅ Azure OpenAI Advantages</h4>
            <ul>
                <li><strong>Context-aware:</strong> Understands nuance and sarcasm</li>
                <li><strong>Rich insights:</strong> Detailed suggestions</li>
                <li><strong>Adaptable:</strong> Learns from context</li>
                <li><strong>Enterprise-ready:</strong> Scalable and consistent</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>✅ Baseline Advantages</h4>
            <ul>
                <li><strong>Ultra-fast:</strong> 1000x faster processing</li>
                <li><strong>Zero cost:</strong> No API fees</li>
                <li><strong>Predictable:</strong> Consistent rules</li>
                <li><strong>Simple:</strong> Easy to maintain</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Recommendations
    st.markdown("### 💡 Recommendations")

    st.markdown("""
    #### 🎯 Use Case Recommendations

    **Choose Azure OpenAI when:**
    - Feedback is complex and nuanced
    - Quality insights are priority over cost
    - Context understanding is critical
    - Budget allows for AI investment (~$0.007/feedback)

    **Choose Baseline when:**
    - Processing millions of simple feedbacks
    - Real-time / instant response required
    - Zero-cost constraint is mandatory
    - Patterns are straightforward and known

    **Hybrid Approach (Recommended):**
    - Use Baseline for initial filtering (fast, free)
    - Route complex cases to Azure OpenAI
    - Best of both worlds: Cost-efficient + High quality
    """)

    # Download comparison report
    st.divider()

    if st.button("📥 Generate & Download Full Report"):
        with st.spinner("Generating comprehensive report..."):
            report_text = comparison.generate_detailed_report()

            st.download_button(
                label="📄 Download Report (TXT)",
                data=report_text,
                file_name="comparison_report.txt",
                mime="text/plain"
            )

            st.success("✅ Report generated successfully!")

# ============================================================================
# ABOUT PAGE
# ============================================================================

elif page == "ℹ️ About":
    st.markdown('<div class="main-header">ℹ️ About This Project</div>', unsafe_allow_html=True)

    st.markdown("""
    ## 📚 Project Information

    **Title:** Marketing Insights Analyzer  
    **Type:** Enterprise AI System Design & Implementation  
    **Purpose:** Compare AI-powered vs Traditional approaches for customer feedback analysis

    ---

    ## 🎯 Objectives

    This project demonstrates:

    1. **Azure OpenAI Integration** - Production-ready AI implementation
    2. **Baseline Development** - Traditional rule-based approach
    3. **Comparative Analysis** - Metrics-driven evaluation
    4. **Enterprise Thinking** - Cost, speed, accuracy trade-offs

    ---

    ## 🏗️ System Architecture
```
    Customer Feedback (Unstructured Text)
            ↓
    ┌─────────────────────────────┐
    │   Dual Processing Pipeline   │
    ├─────────────────────────────┤
    │  • Azure OpenAI (GPT-4)     │
    │  • Rule-Based Baseline      │
    └─────────────────────────────┘
            ↓
    Structured Insights (JSON)
            ↓
    ┌─────────────────────────────┐
    │  Comparison & Visualization  │
    └─────────────────────────────┘
```

    ---

    ## 📊 Output Capabilities

    Both systems extract:
    - ✅ **Sentiment** (positive/neutral/negative)
    - ✅ **Key Themes** (delivery, support, quality, etc.)
    - ✅ **Complaints** identification
    - ✅ **Positive Aspects** detection
    - ✅ **Improvement Suggestions**
    - ✅ **Urgency Level** assessment
    - ✅ **Customer Emotion** detection

    ---

    ## 🔧 Technology Stack

    - **AI Platform:** Azure OpenAI (GPT-4)
    - **Language:** Python 3.10+
    - **UI Framework:** Streamlit
    - **Visualization:** Plotly, Matplotlib
    - **Data Processing:** Pandas
    - **NLP Libraries:** NLTK (VADER), spaCy, NRCLex
    - **Configuration:** python-dotenv

    ---

    ## 📈 Key Metrics Tracked

    1. **Accuracy** - Quality of insights
    2. **Speed** - Processing time per feedback
    3. **Cost** - Token usage and API costs
    4. **Consistency** - Result reliability
    5. **Scalability** - Performance at scale

    ---

    ## 🎓 Learning Outcomes

    This project teaches:
    - Production AI system design
    - Cost-performance trade-off analysis
    - Baseline comparison methodology
    - Enterprise decision frameworks
    - Azure OpenAI implementation
    - Professional UI development with Streamlit

    ---

    ## 🚀 Deployment

    This app is deployed on **Streamlit Community Cloud** and demonstrates:
    - Cloud-native configuration management
    - Dependency management for NLP models
    - Production-ready error handling
    - Scalable architecture

    ---

    ## 📞 Configuration

    **Azure OpenAI Setup:**

    For Streamlit Cloud, add these secrets in your app settings:
```toml
    AZURE_OPENAI_ENDPOINT = "https://your-endpoint.openai.azure.com/"
    AZURE_OPENAI_KEY = "your-api-key"
    AZURE_OPENAI_DEPLOYMENT = "gpt-4"
```

    For local development, create a `.env` file with the same variables.

    ---

    ## 📄 License

    Educational project for academic purposes.

    ---

    ## 👨‍💻 Developer

    Built with ❤️ for enterprise AI education

    **Features:**
    - Real-time analysis
    - Interactive comparison
    - Professional visualizations
    - Export capabilities
    """)

    st.divider()

    # System info
    with st.expander("🔧 System Information"):
        st.json({
            "Python Version": sys.version.split()[0],
            "Streamlit Version": st.__version__,
            "Config Source": Config.get_config_info()['source'],
            "Azure Configured": Config.is_configured(),
            "Dependencies Loaded": st.session_state.get('dependencies_loaded', False)
        })

    st.info("💡 **Pro Tip:** This UI makes your assignment more impressive and easier to present!")

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    📊 Marketing Insights Analyzer | Enterprise AI System | Powered by Azure OpenAI & Streamlit
</div>
""", unsafe_allow_html=True)