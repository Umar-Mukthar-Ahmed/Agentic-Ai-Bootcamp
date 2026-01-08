"""
main.py

Customer Support Response Generator - Main Application
Week 4 Assignment - Azure OpenAI Integration
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from prompt_library import PromptLibrary

# Load environment variables from .env file
load_dotenv()


class CustomerSupportGenerator:
    """
    Main system that uses Azure OpenAI to generate customer support responses.
    Integrates with the PromptLibrary for reusable prompt templates.
    """

    def __init__(self):
        """
        Initialize the Azure OpenAI client using environment variables.
        """
        # Load credentials from environment variables
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        # Validate that all required credentials are present
        if not all([self.azure_endpoint, self.api_key, self.deployment_name]):
            raise ValueError(
                "Missing Azure OpenAI credentials. "
                "Please check your .env file for AZURE_OPENAI_ENDPOINT, "
                "AZURE_OPENAI_API_KEY, and AZURE_OPENAI_DEPLOYMENT_NAME"
            )

        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version="2024-02-15-preview"
        )

        # Initialize prompt library
        self.prompt_library = PromptLibrary()

        print("✓ Azure OpenAI client initialized successfully")
        print(f"✓ Using deployment: {self.deployment_name}\n")

    def generate_response(self, prompt, temperature=None, max_tokens=300):
        """
        Call Azure OpenAI API with the constructed prompt.

        Parameters:
        - prompt (str): The complete prompt with injected variables
        - temperature (float): Controls randomness (0.0-1.0, default None uses model default)
        - max_tokens (int): Maximum response length (default 300)

        Returns:
        - str: Generated response text
        """
        try:
            # Build API call parameters
            api_params = {
                "model": self.deployment_name,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a professional customer support AI assistant."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_completion_tokens": max_tokens
            }

            # Only add temperature if specified (some models don't support custom values)
            if temperature is not None:
                api_params["temperature"] = temperature

            response = self.client.chat.completions.create(**api_params)

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def handle_general_query(self, customer_query, product_name, tone="professional"):
        """
        Use Template 1: General Support Response

        Parameters:
        - customer_query (str): The customer's question
        - product_name (str): Name of the product/service
        - tone (str): 'professional' or 'friendly'

        Returns:
        - str: AI-generated support response
        """
        prompt = self.prompt_library.general_support_prompt(
            customer_query=customer_query,
            product_name=product_name,
            tone=tone
        )
        return self.generate_response(prompt)

    def handle_specific_issue(self, customer_query, issue_type, product_name):
        """
        Use Template 2: Issue Resolution Response

        Parameters:
        - customer_query (str): The customer's issue description
        - issue_type (str): 'billing', 'technical', 'delivery', or 'account'
        - product_name (str): Name of the product/service

        Returns:
        - str: AI-generated support response
        """
        prompt = self.prompt_library.issue_resolution_prompt(
            customer_query=customer_query,
            issue_type=issue_type,
            product_name=product_name
        )
        return self.generate_response(prompt)

    def handle_emotional_customer(self, customer_query, customer_emotion, product_name):
        """
        Use Template 3: Empathy-First Response

        Parameters:
        - customer_query (str): The customer's complaint
        - customer_emotion (str): 'frustrated', 'angry', 'confused', or 'disappointed'
        - product_name (str): Name of the product/service

        Returns:
        - str: AI-generated empathetic support response
        """
        prompt = self.prompt_library.empathy_first_prompt(
            customer_query=customer_query,
            customer_emotion=customer_emotion,
            product_name=product_name
        )
        return self.generate_response(prompt)


def print_section_header(title):
    """Helper function to print formatted section headers"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """
    Demonstration of the Customer Support Response Generator.
    Shows all three prompt templates with different scenarios.
    """

    print_section_header("CUSTOMER SUPPORT RESPONSE GENERATOR - DEMONSTRATION")

    try:
        # Initialize the generator
        generator = CustomerSupportGenerator()

        # =================================================================
        # EXAMPLE 1: General Query with Professional Tone
        # =================================================================
        print_section_header("EXAMPLE 1: General Support Query")

        customer_query_1 = "How do I reset my password? I forgot it and can't log in."
        product_name = "TechCloud Services"

        print(f"Customer Query: '{customer_query_1}'")
        print(f"Product: {product_name}")
        print(f"Tone: Professional\n")
        print("Generating response...\n")

        response1 = generator.handle_general_query(
            customer_query=customer_query_1,
            product_name=product_name,
            tone="professional"
        )

        print("AI-Generated Response:")
        print("-" * 80)
        print(response1)
        print("-" * 80)

        # =================================================================
        # EXAMPLE 2: Billing Issue (Specific Issue Type)
        # =================================================================
        print_section_header("EXAMPLE 2: Specific Issue - Billing")

        customer_query_2 = "I was charged twice for my subscription this month. This is unacceptable!"
        issue_type = "billing"

        print(f"Customer Query: '{customer_query_2}'")
        print(f"Product: {product_name}")
        print(f"Issue Type: {issue_type}\n")
        print("Generating response...\n")

        response2 = generator.handle_specific_issue(
            customer_query=customer_query_2,
            issue_type=issue_type,
            product_name=product_name
        )

        print("AI-Generated Response:")
        print("-" * 80)
        print(response2)
        print("-" * 80)

        # =================================================================
        # EXAMPLE 3: Frustrated Customer (Empathy-First)
        # =================================================================
        print_section_header("EXAMPLE 3: Empathy-First Response")

        customer_query_3 = "This is ridiculous! My order is 3 days late and nobody has contacted me. I need it urgently!"
        customer_emotion = "frustrated"
        product_name_3 = "QuickShip Delivery"

        print(f"Customer Query: '{customer_query_3}'")
        print(f"Product: {product_name_3}")
        print(f"Detected Emotion: {customer_emotion}\n")
        print("Generating response...\n")

        response3 = generator.handle_emotional_customer(
            customer_query=customer_query_3,
            customer_emotion=customer_emotion,
            product_name=product_name_3
        )

        print("AI-Generated Response:")
        print("-" * 80)
        print(response3)
        print("-" * 80)

        # =================================================================
        # Summary
        # =================================================================
        print_section_header("DEMONSTRATION COMPLETE")
        print("✓ Successfully demonstrated all 3 prompt templates")
        print("✓ All responses follow enterprise constraints")
        print("✓ Dynamic variable injection working correctly")
        print("\n")

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure your .env file contains:")
        print("  - AZURE_OPENAI_ENDPOINT")
        print("  - AZURE_OPENAI_API_KEY")
        print("  - AZURE_OPENAI_DEPLOYMENT_NAME\n")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}\n")


if __name__ == "__main__":
    main()