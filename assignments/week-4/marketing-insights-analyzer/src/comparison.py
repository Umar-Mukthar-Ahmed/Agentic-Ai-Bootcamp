"""
Comparison and reporting module for Azure vs Baseline analysis results.
Generates metrics, visualizations, and detailed reports.
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


class ResultsComparison:
    """Compare Azure OpenAI and Baseline analysis results"""

    def __init__(self, azure_results_path, baseline_results_path):
        """Load results from both analyzers"""
        self.azure_results = self.load_results(azure_results_path)
        self.baseline_results = self.load_results(baseline_results_path)

    def load_results(self, filepath):
        """Load results from JSON file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def calculate_metrics(self):
        """Calculate comparison metrics"""
        if not self.azure_results or not self.baseline_results:
            return {}

        metrics = {
            'Azure OpenAI': {
                'Total Feedbacks': len(self.azure_results),
                'Avg Processing Time (s)': round(
                    sum(r.get('processing_time_seconds', 0) for r in self.azure_results) / len(self.azure_results), 4
                ),
                'Total Tokens': sum(
                    r.get('tokens_used', {}).get('total', 0) for r in self.azure_results
                ),
                'Estimated Cost ($)': round(
                    sum(r.get('tokens_used', {}).get('total', 0) for r in self.azure_results) / 1000 * 0.03, 4
                ),
                'Avg Themes per Feedback': round(
                    sum(len(r.get('key_themes', [])) for r in self.azure_results) / len(self.azure_results), 2
                ),
                'Avg Suggestions per Feedback': round(
                    sum(len(r.get('improvement_suggestions', [])) for r in self.azure_results) / len(
                        self.azure_results), 2
                )
            },
            'Baseline': {
                'Total Feedbacks': len(self.baseline_results),
                'Avg Processing Time (s)': round(
                    sum(r.get('processing_time_seconds', 0) for r in self.baseline_results) / len(
                        self.baseline_results), 4
                ),
                'Total Tokens': 0,
                'Estimated Cost ($)': 0.00,
                'Avg Themes per Feedback': round(
                    sum(len(r.get('key_themes', [])) for r in self.baseline_results) / len(self.baseline_results), 2
                ),
                'Avg Suggestions per Feedback': round(
                    sum(len(r.get('improvement_suggestions', [])) for r in self.baseline_results) / len(
                        self.baseline_results), 2
                )
            }
        }

        return metrics

    def sentiment_comparison(self):
        """Compare sentiment distribution"""
        azure_sentiments = [r.get('sentiment', 'unknown') for r in self.azure_results]
        baseline_sentiments = [r.get('sentiment', 'unknown') for r in self.baseline_results]

        azure_dist = pd.Series(azure_sentiments).value_counts().to_dict()
        baseline_dist = pd.Series(baseline_sentiments).value_counts().to_dict()

        return {
            'Azure OpenAI': azure_dist,
            'Baseline': baseline_dist
        }

    def generate_comparison_table(self):
        """Generate pandas DataFrame with metrics"""
        metrics = self.calculate_metrics()
        if not metrics:
            return pd.DataFrame()
        return pd.DataFrame(metrics).T

    def plot_comparison(self, output_dir='data/results'):
        """Create comparison visualizations"""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        metrics = self.calculate_metrics()
        if not metrics:
            return

        sentiment_comp = self.sentiment_comparison()

        # Create figure
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Azure OpenAI vs Baseline: Performance Comparison',
                     fontsize=16, fontweight='bold')

        # 1. Processing Time
        ax1 = axes[0, 0]
        methods = list(metrics.keys())
        times = [metrics[m]['Avg Processing Time (s)'] for m in methods]
        colors = ['#0078D4', '#107C10']
        ax1.bar(methods, times, color=colors, alpha=0.7, edgecolor='black')
        ax1.set_ylabel('Seconds')
        ax1.set_title('Average Processing Time per Feedback')
        ax1.grid(axis='y', alpha=0.3)

        # 2. Cost
        ax2 = axes[0, 1]
        costs = [metrics[m]['Estimated Cost ($)'] for m in methods]
        ax2.bar(methods, costs, color=colors, alpha=0.7, edgecolor='black')
        ax2.set_ylabel('USD ($)')
        ax2.set_title('Total Processing Cost')
        ax2.grid(axis='y', alpha=0.3)

        # 3. Sentiment - Azure
        ax3 = axes[1, 0]
        azure_sent = sentiment_comp.get('Azure OpenAI', {})
        if azure_sent:
            ax3.pie(azure_sent.values(), labels=azure_sent.keys(), autopct='%1.1f%%',
                    colors=['#28A745', '#FFC107', '#DC3545'], startangle=90)
        ax3.set_title('Azure OpenAI: Sentiment Distribution')

        # 4. Sentiment - Baseline
        ax4 = axes[1, 1]
        baseline_sent = sentiment_comp.get('Baseline', {})
        if baseline_sent:
            ax4.pie(baseline_sent.values(), labels=baseline_sent.keys(), autopct='%1.1f%%',
                    colors=['#28A745', '#FFC107', '#DC3545'], startangle=90)
        ax4.set_title('Baseline: Sentiment Distribution')

        plt.tight_layout()
        output_path = f'{output_dir}/comparison_charts.png'
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        print(f"\n📊 Charts saved to: {output_path}")
        plt.close()

    def generate_detailed_report(self, output_path='data/results/comparison_report.txt'):
        """Generate detailed text report"""
        metrics = self.calculate_metrics()
        if not metrics:
            return "No results to compare."

        sentiment_comp = self.sentiment_comparison()

        report = []
        report.append("=" * 80)
        report.append("MARKETING INSIGHTS ANALYZER - COMPARISON REPORT")
        report.append("=" * 80)
        report.append("")

        report.append("1. PERFORMANCE METRICS")
        report.append("-" * 80)
        df = self.generate_comparison_table()
        report.append(df.to_string())
        report.append("")

        report.append("2. SENTIMENT ANALYSIS COMPARISON")
        report.append("-" * 80)
        report.append(f"Azure OpenAI: {sentiment_comp.get('Azure OpenAI', {})}")
        report.append(f"Baseline:     {sentiment_comp.get('Baseline', {})}")
        report.append("")

        report.append("3. KEY FINDINGS")
        report.append("-" * 80)

        azure_time = metrics['Azure OpenAI']['Avg Processing Time (s)']
        baseline_time = metrics['Baseline']['Avg Processing Time (s)']
        if baseline_time > 0:
            speed_ratio = azure_time / baseline_time
            report.append(f"• Speed: Baseline is {speed_ratio:.0f}x faster than Azure OpenAI")

        report.append(f"• Cost: Azure OpenAI costs ${metrics['Azure OpenAI']['Estimated Cost ($)']} vs Baseline $0.00")
        report.append(f"• Richness: Azure provides {metrics['Azure OpenAI']['Avg Suggestions per Feedback']} "
                      f"suggestions vs {metrics['Baseline']['Avg Suggestions per Feedback']} from Baseline")
        report.append("")

        report.append("4. RECOMMENDATIONS")
        report.append("-" * 80)
        report.append("• Azure OpenAI: Best for comprehensive, context-aware analysis")
        report.append("• Baseline: Best for quick, cost-effective preliminary screening")
        report.append("• Hybrid Approach: Use Baseline for filtering, Azure for deep analysis")
        report.append("")

        report_text = "\n".join(report)

        # Save to file
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)

        print(f"\n📄 Report saved to: {output_path}")
        return report_text