"""
Azure OpenAI-based feedback analyzer using GPT-4.
Provides context-aware, intelligent analysis of customer feedback.
"""

import json
import time
from openai import AzureOpenAI
from src.config import Config


class AzureInsightsAnalyzer:
    """Azure OpenAI-powered feedback analyzer"""

    def __init__(self):
        """Initialize Azure OpenAI client"""
        if not Config.is_configured():
            raise ValueError(
                "Azure OpenAI is not configured. Please set up your credentials in "
                "Streamlit secrets (cloud) or .env file (local)."
            )

        self.client = AzureOpenAI(
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT,
            api_key=Config.AZURE_OPENAI_KEY,
            api_version=Config.AZURE_API_VERSION
        )
        self.deployment = Config.AZURE_OPENAI_DEPLOYMENT

    def create_analysis_prompt(self, feedback_text):
        """Create structured prompt for Azure OpenAI analysis"""
        prompt = f"""You are an expert marketing analyst specializing in customer feedback analysis.

Analyze the following customer feedback and return ONLY a valid JSON response with this exact structure:

{{
  "sentiment": "<positive|neutral|negative>",
  "sentiment_score": <number between -1 and 1>,
  "key_themes": ["theme1", "theme2", "theme3"],
  "complaints": ["complaint1", "complaint2"],
  "positive_aspects": ["positive1", "positive2"],
  "improvement_suggestions": ["suggestion1", "suggestion2"],
  "urgency_level": "<low|medium|high>",
  "customer_emotion": "<satisfied|neutral|frustrated|angry>"
}}

Instructions:
- sentiment: Overall sentiment (positive, neutral, or negative)
- sentiment_score: Numeric score from -1 (very negative) to +1 (very positive)
- key_themes: Main topics mentioned (max 5)
- complaints: Specific issues raised (max 5)
- positive_aspects: Things the customer liked (max 5)
- improvement_suggestions: Actionable recommendations (max 5)
- urgency_level: How urgently this needs attention
- customer_emotion: Detected emotional state

Customer Feedback:
"{feedback_text}"

Return only valid JSON, no additional text or explanation."""
        return prompt

    def analyze_feedback(self, feedback_text, feedback_id):
        """Analyze a single customer feedback using Azure OpenAI"""
        try:
            start_time = time.time()

            # Call Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional marketing analyst. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": self.create_analysis_prompt(feedback_text)
                    }
                ],
                temperature=0.3,
                max_tokens=800,
                response_format={"type": "json_object"}
            )

            processing_time = time.time() - start_time

            # Parse the JSON response
            analysis = json.loads(response.choices[0].message.content)

            # Add metadata
            analysis['feedback_id'] = feedback_id
            analysis['original_feedback'] = feedback_text
            analysis['processing_time_seconds'] = round(processing_time, 3)
            analysis['tokens_used'] = {
                'prompt': response.usage.prompt_tokens,
                'completion': response.usage.completion_tokens,
                'total': response.usage.total_tokens
            }

            return analysis

        except Exception as e:
            return {
                'feedback_id': feedback_id,
                'error': str(e),
                'original_feedback': feedback_text
            }

    def analyze_batch(self, feedback_list):
        """Analyze multiple feedback entries"""
        results = []
        total_tokens = 0

        print(f"\n🤖 Starting Azure OpenAI Analysis...")
        print(f"Processing {len(feedback_list)} feedback entries...\n")

        for idx, item in enumerate(feedback_list, 1):
            print(f"Analyzing feedback {idx}/{len(feedback_list)}...", end=" ")

            result = self.analyze_feedback(item['feedback'], item['id'])
            results.append(result)

            if 'tokens_used' in result:
                total_tokens += result['tokens_used']['total']
                print(f"✓ ({result['tokens_used']['total']} tokens)")
            else:
                print("✗ Error")

            # Small delay to avoid rate limits
            time.sleep(0.3)

        print(f"\n✅ Analysis Complete!")
        print(f"Total tokens used: {total_tokens}")
        print(f"Estimated cost (GPT-4): ${(total_tokens / 1000) * 0.03:.4f}")

        return results

    def save_results(self, results, filepath):
        """Save analysis results to JSON file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Results saved to: {filepath}")