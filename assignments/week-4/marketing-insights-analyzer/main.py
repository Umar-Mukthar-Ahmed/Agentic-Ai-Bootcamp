"""
Marketing Insights Analyzer - Command Line Interface
====================================================
CLI version for running batch analysis without the web interface.
"""

import json
import os
from pathlib import Path
from src.config import Config
from src.azure_analyzer import AzureInsightsAnalyzer
from src.baseline_analyzer import BaselineInsightsAnalyzer
from src.comparison import ResultsComparison


def create_directories():
    """Create necessary directories for results"""
    Path("data/results").mkdir(parents=True, exist_ok=True)
    print("✅ Project directories created")


def load_feedback_data():
    """Load sample feedback data from JSON"""
    try:
        with open(Config.DATA_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} feedback entries")
        return data
    except FileNotFoundError:
        print(f"❌ Error: Could not find {Config.DATA_PATH}")
        return []


def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("MARKETING INSIGHTS ANALYZER - CLI VERSION")
    print("=" * 80 + "\n")

    # Step 1: Setup
    print("📁 Step 1: Setting up project structure...")
    create_directories()

    # Step 2: Load data
    print("\n📊 Step 2: Loading feedback data...")
    feedback_data = load_feedback_data()

    if not feedback_data:
        print("❌ No feedback data available. Exiting.")
        return

    # Step 3: Check Azure configuration
    print("\n🔧 Step 3: Checking Azure OpenAI configuration...")
    if not Config.is_configured():
        print("❌ Azure OpenAI is not configured!")
        print("Please set up your credentials:")
        print("  - Create a .env file with AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_KEY")
        print("  - Or set environment variables")

        # Continue with baseline only
        print("\n⚠️ Continuing with Baseline analysis only...\n")

        # Step 4: Baseline Analysis
        print("⚙️ Step 4: Running Baseline Analysis...")
        baseline_analyzer = BaselineInsightsAnalyzer()
        baseline_results = baseline_analyzer.analyze_batch(feedback_data)
        baseline_analyzer.save_results(baseline_results, Config.BASELINE_RESULTS_PATH)

        print("\n" + "=" * 80)
        print("✅ BASELINE ANALYSIS COMPLETE!")
        print("=" * 80)
        print(f"\nGenerated file: {Config.BASELINE_RESULTS_PATH}")
        return

    print("✅ Azure OpenAI configured successfully")

    # Step 4: Azure OpenAI Analysis
    print("\n🤖 Step 4: Running Azure OpenAI Analysis...")
    try:
        azure_analyzer = AzureInsightsAnalyzer()
        azure_results = azure_analyzer.analyze_batch(feedback_data)
        azure_analyzer.save_results(azure_results, Config.AZURE_RESULTS_PATH)
    except Exception as e:
        print(f"❌ Azure analysis failed: {str(e)}")
        print("Please check your Azure credentials")
        return

    # Step 5: Baseline Analysis
    print("\n⚙️ Step 5: Running Baseline Analysis...")
    baseline_analyzer = BaselineInsightsAnalyzer()
    baseline_results = baseline_analyzer.analyze_batch(feedback_data)
    baseline_analyzer.save_results(baseline_results, Config.BASELINE_RESULTS_PATH)

    # Step 6: Comparison
    print("\n📊 Step 6: Generating Comparison Report...")
    comparison = ResultsComparison(
        Config.AZURE_RESULTS_PATH,
        Config.BASELINE_RESULTS_PATH
    )

    # Generate comparison table
    comparison_df = comparison.generate_comparison_table()
    print("\n" + "=" * 80)
    print("COMPARISON TABLE")
    print("=" * 80)
    print(comparison_df)

    # Generate visualizations
    print("\n📊 Generating visualizations...")
    comparison.plot_comparison()

    # Generate detailed report
    print("\n📄 Generating detailed report...")
    comparison.generate_detailed_report()

    print("\n" + "=" * 80)
    print("✅ ANALYSIS COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print(f"  • Azure results: {Config.AZURE_RESULTS_PATH}")
    print(f"  • Baseline results: {Config.BASELINE_RESULTS_PATH}")
    print("  • Comparison charts: data/results/comparison_charts.png")
    print("  • Detailed report: data/results/comparison_report.txt")
    print("\n💡 Tip: Run 'streamlit run app.py' for the interactive web interface!\n")


if __name__ == "__main__":
    main()