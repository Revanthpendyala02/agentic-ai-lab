import os
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, "..", ".env")
INPUT_FILE = os.path.join(BASE_DIR, "input.txt")

load_dotenv(ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Gemini API key not found!")
    exit()


GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.5-flash:generateContent"
)


def ask_gemini(prompt):

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(
        GEMINI_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:

        print("Gemini Error:")
        print(response.text)

        return None

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8"
) as file:

    document = file.read()


# =========================
# STEP 1
# =========================

prompt1 = f"""
Read the following document.

Extract the most important facts, ideas,
applications, benefits, and challenges.

Do not write a final summary.
Return only important points.

Document:

{document}
"""

step1 = ask_gemini(prompt1)

if step1 is None:
    exit()

print("\nSTEP 1 - KEY INFORMATION")
print("=========================")
print(step1)


# =========================
# STEP 2
# =========================

prompt2 = f"""
Organize the following extracted information
into clear categories.

Create sections such as:

- Main Idea
- Applications
- Benefits
- Challenges

Do not add information that is not present.

Extracted Information:

{step1}
"""

step2 = ask_gemini(prompt2)

if step2 is None:
    exit()

print("\nSTEP 2 - ORGANIZED INFORMATION")
print("===============================")
print(step2)


# =========================
# STEP 3
# =========================

prompt3 = f"""
Create a clear and concise final summary
using the organized information below.

The summary should:

- Be easy to understand
- Include the main idea
- Mention important applications
- Mention major benefits
- Mention important challenges
- Avoid unnecessary details
- Do not introduce new information

Organized Information:

{step2}
"""

step3 = ask_gemini(prompt3)

if step3 is None:
    exit()

print("\nSTEP 3 - FINAL SUMMARY")
print("=======================")
print(step3)