import re
from typing import Tuple, Optional
import markdown


class TextFilterAI:
    def __init__(self):
        self.allowed_chars = set(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,?!\"':;() ")
        self.special_chars = set("@$#%^&{}[]|\\/<>~")

    def detect_tone(self, message: str) -> str:
        message = message.lower()
        if any(word in message for word in ["please", "thank you", "help"]):
            return "friendly"
        elif any(word in message for word in ["help!", "fix", "problem", "mess"]):
            return "frustrated"
        elif any(word in message for word in ["kindly", "request"]):
            return "formal"
        elif any(word in message for word in ["hey", "hi"]):
            return "casual"
        return "neutral"

    def generate_greeting(self, tone: str, has_text: bool) -> str:
        greetings = {
            "friendly": ("Hello! I will now clean and improve your text. Let's make it perfect! I'll start the cleaning process now.",
                         "Hello! I will now clean and improve your text. Let's make it perfect! Please provide the text so I can start."),
            "frustrated": ("Oops! Let me help you fix it right away. I'll start cleaning the text now. Thank you for your patience!",
                           "Oops! Let me help you fix it right away. Could you share the text with me? Thank you for your patience!"),
            "formal": ("Hello! I will now clean and improve your text as per your request. Let's ensure it's perfect! I'll proceed with the cleaning now.",
                       "Hello! I will now clean and improve your text as per your request. Let's ensure it's perfect! Please provide the text so I can begin."),
            "casual": ("Hey there! I'll clean this up for you and make it look great! Let's do this! I'm ready to start cleaning now.",
                       "Hey there! I'll clean this up for you and make it look great! Let's do this! Please provide the text, and I'll get started."),
            "neutral": ("Hello! I will now clean and improve your text. Let's make it perfect! I'll proceed with cleaning now.",
                        "Oops! There's a problem with your input. Please share the correct input.")
        }
        return greetings[tone][0 if has_text else 1]

    def calculate_special_char_density(self, text: str) -> float:
        special_chars_count = sum(
            1 for char in text if char in self.special_chars)
        return (special_chars_count / len(text)) * 100 if text else 0

    def validate_input(self, text: Optional[str]) -> Tuple[bool, str]:
        if not text:
            return False, "ERROR: Please provide text"
        if len(text) > 10000:
            return False, "ERROR: Text is too long. Please shorten it"
        density = self.calculate_special_char_density(text)
        # if density > 5:
        #     return True, f"WARNING: High number of special characters found ({density:.2f}%). Proceed with cleaning? (Yes/No)"
        return True, ""

    def clean_text(self, text: str) -> str:
        # Remove disallowed characters
        cleaned = ''.join(
            char if char in self.allowed_chars else ' ' for char in text)

        # Fix multiple spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)

        # Fix excessive punctuation
        cleaned = re.sub(r'!+', '!', cleaned)
        cleaned = re.sub(r'\?+', '?', cleaned)
        cleaned = re.sub(r'\.+', '.', cleaned)

        return cleaned.strip()

    def format_output(self, original: str, cleaned: str) -> str:
        markdown_output = "# Text Cleaning Report\n\n"

        # 1. Validation Report
        markdown_output += "## Validation Report\n"
        special_chars_found = [
            char for char in original if char in self.special_chars]
        extra_spaces = len(re.findall(r'\s{2,}', original))
        has_proper_case = any(c.isupper() for c in original)

        markdown_output += f"- Special Characters Found: {len(special_chars_found)}\n"
        markdown_output += f"- Extra Spaces Detected: {extra_spaces}\n"
        markdown_output += f"- Sentence Case: {'Preserved' if has_proper_case else 'No uppercase letters found'}\n\n"

        # 2. Density Report
        density = self.calculate_special_char_density(original)
        markdown_output += "## Density Report\n"
        markdown_output += f"Special character density: {density:.2f}%\n\n"

        # 3. Original and Cleaned Text
        markdown_output += "## Original Text\n"
        markdown_output += f"```\n{original}\n```\n\n"
        markdown_output += "## Cleaned Text\n"
        markdown_output += f"```\n{cleaned}\n```\n\n"

        # 4. Step-by-Step Fixes
        markdown_output += "## Step-by-Step Fixes Applied\n"

        # Count removed special characters
        removed_chars = set(original) - self.allowed_chars
        if removed_chars:
            markdown_output += f"- Special Characters Removed: <font color='red'>{', '.join(removed_chars)}</font>\n"

        # Count space fixes
        original_spaces = len(re.findall(r'\s+', original))
        cleaned_spaces = len(re.findall(r'\s+', cleaned))
        if original_spaces != cleaned_spaces:
            markdown_output += f"- Fixed Extra Spaces: <font color='orange'>{original_spaces} spaces → {cleaned_spaces} spaces</font>\n"

        # Count punctuation fixes
        orig_excl = len(re.findall(r'!+', original))
        clean_excl = len(re.findall(r'!', cleaned))
        if orig_excl != clean_excl:
            markdown_output += f"- Reduced Exclamation Marks: {orig_excl} → {clean_excl}\n"

        # 5. User Feedback Request
        markdown_output += "\n## Feedback\n"
        markdown_output += "Please rate the text filtering process (1-5 stars): ⭐⭐⭐⭐⭐\n"

        return markdown_output

    def process_feedback(self, rating: int) -> str:
        if not 1 <= rating <= 5:
            return "Invalid rating. Please provide a rating between 1 and 5."

        if rating <= 2:
            return "Sorry for the inconvenience! How can I improve the text filtering process for you?"
        elif rating >= 4:
            return "Thank you! I'm glad you found it helpful. Let me know if you need further improvements!"
        return "Thank you for your feedback!"


def main():
    filter_ai = TextFilterAI()

    # Example usage
    message = "Please help me clean this text!"
    text = "Hey!!! This text is FULL of issues!!! We have @#$%{}/ symbols, extra spaces, and TOO MANY CAPS!!!!! Please fix it!!!"

    # Detect tone and generate greeting
    tone = filter_ai.detect_tone(message)
    greeting = filter_ai.generate_greeting(tone, bool(text))

    # Validate input
    is_valid, validation_message = filter_ai.validate_input(text)
    if not is_valid:
        print(validation_message)
        return

    # Clean and format text
    cleaned_text = filter_ai.clean_text(text)
    output = filter_ai.format_output(text, cleaned_text)

    # Print results
    print(greeting)
    print("\n" + output)

    # Get feedback
    try:
        rating = int(input("Enter your rating (1-5): "))
        feedback_response = filter_ai.process_feedback(rating)
        print(feedback_response)
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
