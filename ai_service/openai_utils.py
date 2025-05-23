import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Set up Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Set it as an environment variable.")

genai.configure(api_key=GEMINI_API_KEY)

def generate_summary(book_title, book_content):
    try:
        prompt = (
            f"Summarize the following book titled '{book_title}':\n\n"
            f"{book_content}\n\nSummary:"
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "Summary generation failed."
    except Exception as e:
        print(f"Gemini API error: {e}")
        return "Summary generation failed."

