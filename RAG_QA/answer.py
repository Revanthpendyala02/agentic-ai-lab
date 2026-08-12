import os
import requests
from dotenv import load_dotenv
from retrieve import retrieve

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, "..", ".env")

load_dotenv(ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Gemini API key not found!")
    exit()


GENERATE_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.5-flash:generateContent"
)


def generate_answer(question, retrieved_documents):

    context = ""

    for document in retrieved_documents:

        context += (
            "\n\nDocument: "
            + document["filename"]
            + "\n"
            + document["text"]
        )

    prompt = f"""
You are a helpful question-answering assistant.

Answer the user's question using ONLY the provided documents.

If the answer cannot be found in the documents,
say that the information is not available.

Do not make up information.

User Question:
{question}

Retrieved Documents:
{context}

Give a clear and concise answer.
"""

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
        GENERATE_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:

        print("\nGemini Error:")
        print(response.text)

        return None

    result = response.json()

    return result["candidates"][0]["content"]["parts"][0]["text"]


if __name__ == "__main__":

    question = input("Enter your question: ")

    retrieved_documents = retrieve(
        question,
        top_k=2
    )

    print("\nRetrieved Documents:")
    print("====================")

    for document in retrieved_documents:

        print(
            document["filename"],
            "->",
            round(document["score"], 4)
        )

    answer = generate_answer(
        question,
        retrieved_documents
    )

    print("\nFinal Answer:")
    print("=============")

    if answer:
        print(answer)