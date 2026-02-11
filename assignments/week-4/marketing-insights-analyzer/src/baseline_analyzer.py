"""
Baseline rule-based feedback analyzer using VADER, spaCy, and NRC Lexicon.
Provides fast, cost-free analysis using traditional NLP techniques.
"""

import json
import time
import re
from nltk.sentiment import SentimentIntensityAnalyzer


class BaselineInsightsAnalyzer:
    """Rule-based feedback analyzer using NLTK VADER"""

    def __init__(self):
        """Initialize NLP components"""
        # VADER for sentiment analysis
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except LookupError:
            import nltk
            nltk.download('vader_lexicon', quiet=True)
            self.sentiment_analyzer = SentimentIntensityAnalyzer()

        # spaCy for advanced NLP (optional)
        self.nlp = None
        try:
            import spacy
            self.nlp = spacy.load("en_core_web_sm")
        except:
            pass  # spaCy is optional

        # Theme keywords mapping
        self.theme_keywords = {
            'delivery': ['delivery', 'shipping', 'delivered', 'arrive', 'arrived', 'ship', 'late', 'on time'],
            'packaging': ['packaging', 'package', 'packed', 'box', 'wrap', 'damaged packaging'],
            'customer_support': ['support', 'service', 'help', 'representative', 'chat', 'staff', 'team'],
            'product_quality': ['quality', 'product', 'item', 'defect', 'broken', 'damaged', 'excellent'],
            'pricing': ['price', 'pricing', 'cost', 'expensive', 'value', 'money', 'cheap', 'affordable'],
            'website': ['website', 'site', 'app', 'interface', 'navigate', 'navigation', 'ui', 'mobile'],
            'checkout': ['checkout', 'payment', 'purchase', 'buying', 'cart', 'crash'],
            'returns': ['return', 'refund', 'replacement', 'exchange'],
            'technical': ['crash', 'bug', 'technical', 'error', 'loading', 'slow', 'freeze']
        }

        # Complaint indicators
        self.complaint_indicators = {
            'too', 'very', 'extremely', 'terrible', 'worst', 'never', 'again',
            'not', 'poor', 'bad', 'issue', 'problem', 'broken', 'damaged',
            'disappointed', 'frustrating', 'unhelpful', 'slow'
        }

        # Positive indicators
        self.positive_indicators = {
            'excellent', 'great', 'good', 'love', 'loved', 'best', 'amazing',
            'wonderful', 'perfect', 'fantastic', 'helpful', 'fast', 'quick',
            'easy', 'friendly', 'impressed', 'exceeded', 'recommend'
        }

    def calculate_sentiment(self, text):
        """Calculate sentiment using VADER"""
        scores = self.sentiment_analyzer.polarity_scores(text)
        compound = scores['compound']

        if compound >= 0.05:
            sentiment = 'positive'
        elif compound <= -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return sentiment, round(compound, 3)

    def extract_themes(self, text):
        """Extract themes using keyword matching"""
        text_lower = text.lower()
        detected_themes = []

        for theme, keywords in self.theme_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                detected_themes.append(theme)

        return detected_themes

    def extract_complaints(self, text, sentiment):
        """Extract potential complaints from text"""
        complaints = []
        sentences = re.split(r'[.!?]', text)

        for sentence in sentences:
            sentence_lower = sentence.lower()
            if any(indicator in sentence_lower for indicator in self.complaint_indicators):
                if len(sentence.strip()) > 10:
                    complaints.append(sentence.strip())

        return complaints[:5]

    def extract_positive_aspects(self, text, sentiment):
        """Extract positive aspects from text"""
        if sentiment == 'negative':
            return []

        positive_aspects = []
        sentences = re.split(r'[.!?]', text)

        for sentence in sentences:
            words = set(re.findall(r'\b\w+\b', sentence.lower()))
            if words & self.positive_indicators:
                if len(sentence.strip()) > 10:
                    positive_aspects.append(sentence.strip())

        return positive_aspects[:5]

    def generate_improvements(self, themes, sentiment):
        """Generate improvement suggestions based on detected themes"""
        improvement_map = {
            'delivery': 'Improve delivery speed and tracking',
            'packaging': 'Enhance packaging quality and protection',
            'customer_support': 'Increase support team capacity and training',
            'product_quality': 'Implement stricter quality control measures',
            'pricing': 'Review pricing strategy and offer competitive rates',
            'website': 'Improve website usability and navigation',
            'checkout': 'Streamline checkout process',
            'returns': 'Simplify returns and refund process',
            'technical': 'Fix technical bugs and improve system stability'
        }

        improvements = []
        for theme in themes:
            if theme in improvement_map:
                improvements.append(improvement_map[theme])

        return improvements[:5]

    def assess_urgency(self, sentiment, complaints):
        """Assess urgency level based on sentiment and complaints"""
        if sentiment == 'negative' and len(complaints) >= 2:
            return 'high'
        elif sentiment == 'negative' or len(complaints) >= 1:
            return 'medium'
        else:
            return 'low'

    def detect_emotion(self, text):
        """Detect customer emotion using keyword matching"""
        text_lower = text.lower()

        if any(word in text_lower for word in ['terrible', 'worst', 'angry', 'hate']):
            return 'angry'
        elif any(word in text_lower for word in ['frustrat', 'annoying', 'annoyed']):
            return 'frustrated'
        elif any(word in text_lower for word in ['love', 'great', 'excellent', 'amazing', 'perfect']):
            return 'satisfied'
        else:
            return 'neutral'

    def analyze_feedback(self, feedback_text, feedback_id):
        """Analyze a single feedback using rule-based approach"""
        try:
            start_time = time.time()

            # Perform analysis
            sentiment, sentiment_score = self.calculate_sentiment(feedback_text)
            themes = self.extract_themes(feedback_text)
            complaints = self.extract_complaints(feedback_text, sentiment)
            positive_aspects = self.extract_positive_aspects(feedback_text, sentiment)
            improvements = self.generate_improvements(themes, sentiment)
            urgency = self.assess_urgency(sentiment, complaints)
            emotion = self.detect_emotion(feedback_text)

            processing_time = time.time() - start_time

            return {
                'feedback_id': feedback_id,
                'original_feedback': feedback_text,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score,
                'key_themes': themes,
                'complaints': complaints,
                'positive_aspects': positive_aspects,
                'improvement_suggestions': improvements,
                'urgency_level': urgency,
                'customer_emotion': emotion,
                'processing_time_seconds': round(processing_time, 4)
            }

        except Exception as e:
            return {
                'feedback_id': feedback_id,
                'error': str(e),
                'original_feedback': feedback_text
            }

    def analyze_batch(self, feedback_list):
        """Analyze multiple feedback entries"""
        results = []

        print(f"\n⚙️ Starting Baseline Analysis...")
        print(f"Processing {len(feedback_list)} feedback entries...\n")

        for idx, item in enumerate(feedback_list, 1):
            print(f"Analyzing feedback {idx}/{len(feedback_list)}...", end=" ")

            result = self.analyze_feedback(item['feedback'], item['id'])
            results.append(result)

            print("✓")

        print(f"\n✅ Analysis Complete!")
        print("Cost: $0.00 (No API costs)")

        return results

    def save_results(self, results, filepath):
        """Save results to JSON file"""
        import os
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Results saved to: {filepath}")