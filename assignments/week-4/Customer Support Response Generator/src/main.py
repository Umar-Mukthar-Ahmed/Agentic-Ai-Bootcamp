"""
main_interactive.py

Interactive Customer Support Response Generator
User-driven prompt selection and input
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI
from prompt_library import PromptLibrary

load_dotenv()


class CustomerSupportGenerator:
    """
    Main system that uses Azure OpenAI to generate customer support responses.
    """

    def __init__(self):
        """Initialize the Azure OpenAI client using environment variables."""
        self.azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        if not all([self.azure_endpoint, self.api_key, self.deployment_name]):
            raise ValueError(
                "Missing Azure OpenAI credentials. "
                "Please check your .env file."
            )

        self.client = AzureOpenAI(
            azure_endpoint=self.azure_endpoint,
            api_key=self.api_key,
            api_version="2024-02-15-preview"
        )

        self.prompt_library = PromptLibrary()

        print("✓ Azure OpenAI client initialized successfully")
        print(f"✓ Using deployment: {self.deployment_name}\n")

    def generate_response(self, prompt, temperature=None, max_tokens=300):
        """Call Azure OpenAI API with the constructed prompt."""
        try:
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

            if temperature is not None:
                api_params["temperature"] = temperature

            response = self.client.chat.completions.create(**api_params)
            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def handle_general_query(self, customer_query, product_name, tone="professional"):
        """Use Template 1: General Support Response"""
        prompt = self.prompt_library.general_support_prompt(
            customer_query=customer_query,
            product_name=product_name,
            tone=tone
        )
        return self.generate_response(prompt)

    def handle_specific_issue(self, customer_query, issue_type, product_name):
        """Use Template 2: Issue Resolution Response"""
        prompt = self.prompt_library.issue_resolution_prompt(
            customer_query=customer_query,
            issue_type=issue_type,
            product_name=product_name
        )
        return self.generate_response(prompt)

    def handle_emotional_customer(self, customer_query, customer_emotion, product_name):
        """Use Template 3: Empathy-First Response"""
        prompt = self.prompt_library.empathy_first_prompt(
            customer_query=customer_query,
            customer_emotion=customer_emotion,
            product_name=product_name
        )
        return self.generate_response(prompt)


def print_header(title):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def get_user_choice(prompt, valid_options):
    """Get validated user input from a list of options"""
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        print(f"❌ Invalid choice. Please select from: {', '.join(valid_options)}\n")


def get_text_input(prompt):
    """Get non-empty text input from user"""
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print("❌ Input cannot be empty. Please try again.\n")


def interactive_mode():
    """Run the interactive user-driven support generator"""

    print_header("INTERACTIVE CUSTOMER SUPPORT RESPONSE GENERATOR")

    try:
        generator = CustomerSupportGenerator()

        while True:
            print_header("SELECT PROMPT TEMPLATE")
            print("Available Templates:")
            print("  1. General Support Query")
            print("  2. Specific Issue Resolution (Billing, Technical, etc.)")
            print("  3. Empathy-First Response (Emotional Customer)")
            print("  4. Exit")
            print()

            choice = get_user_choice(
                "Enter your choice (1-4): ",
                ["1", "2", "3", "4"]
            )

            if choice == "4":
                print("\n👋 Thank you for using Customer Support Generator!")
                break

            # Get common inputs
            print()
            customer_query = get_text_input("Enter customer query/message: ")
            product_name = get_text_input("Enter product/service name: ")

            # Template-specific logic
            if choice == "1":
                # General Support
                print("\nSelect tone:")
                print("  1. Professional")
                print("  2. Friendly")
                tone_choice = get_user_choice("Enter choice (1-2): ", ["1", "2"])
                tone = "professional" if tone_choice == "1" else "friendly"

                print("\n⏳ Generating response...\n")
                response = generator.handle_general_query(
                    customer_query=customer_query,
                    product_name=product_name,
                    tone=tone
                )

            elif choice == "2":
                # Specific Issue
                print("\nSelect issue type:")
                print("  1. Billing")
                print("  2. Technical")
                print("  3. Delivery")
                print("  4. Account")
                issue_choice = get_user_choice("Enter choice (1-4): ", ["1", "2", "3", "4"])
                issue_types = {
                    "1": "billing",
                    "2": "technical",
                    "3": "delivery",
                    "4": "account"
                }
                issue_type = issue_types[issue_choice]

                print("\n⏳ Generating response...\n")
                response = generator.handle_specific_issue(
                    customer_query=customer_query,
                    issue_type=issue_type,
                    product_name=product_name
                )

            elif choice == "3":
                # Empathy-First
                print("\nSelect customer emotion:")
                print("  1. Frustrated")
                print("  2. Angry")
                print("  3. Confused")
                print("  4. Disappointed")
                emotion_choice = get_user_choice("Enter choice (1-4): ", ["1", "2", "3", "4"])
                emotions = {
                    "1": "frustrated",
                    "2": "angry",
                    "3": "confused",
                    "4": "disappointed"
                }
                customer_emotion = emotions[emotion_choice]

                print("\n⏳ Generating response...\n")
                response = generator.handle_emotional_customer(
                    customer_query=customer_query,
                    customer_emotion=customer_emotion,
                    product_name=product_name
                )

            # Display response
            print_header("AI-GENERATED RESPONSE")
            print(response)
            print("\n" + "-" * 80)

            # Ask if user wants to continue
            print("\n")
            continue_choice = get_user_choice(
                "Generate another response? (y/n): ",
                ["y", "n", "Y", "N"]
            )

            if continue_choice.lower() == "n":
                print("\n👋 Thank you for using Customer Support Generator!")
                break

    except ValueError as e:
        print(f"\n❌ Configuration Error: {e}")
        print("\nPlease ensure your .env file contains:")
        print("  - AZURE_OPENAI_ENDPOINT")
        print("  - AZURE_OPENAI_API_KEY")
        print("  - AZURE_OPENAI_DEPLOYMENT_NAME\n")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}\n")


def main():
    """Entry point - runs interactive mode"""
    interactive_mode()


if __name__ == "__main__":
    main()