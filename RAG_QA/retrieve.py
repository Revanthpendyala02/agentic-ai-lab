import os
import json
import requests
import math
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, "..", ".env")
INDEX_FILE = os.path.join(BASE_DIR, "index.json")

load_dotenv(ENV_FILE)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("Gemini API key not found!")
    exit()

EMBEDDING_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-embedding-001:embedContent"
)


def create_embedding(text):

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": API_KEY
    }

    data = {
        "content": {
            "parts": [
                {
                    "text": text
                }
            ]
        }
    }

    response = requests.post(
        EMBEDDING_URL,
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:
        print("Embedding Error:")
        print(response.text)
        return None

    result = response.json()

    return result["embedding"]["values"]


def cosine_similarity(vector1, vector2):

    dot_product = 0
    magnitude1 = 0
    magnitude2 = 0

    for i in range(len(vector1)):

        dot_product += vector1[i] * vector2[i]

        magnitude1 += vector1[i] ** 2
        magnitude2 += vector2[i] ** 2

    magnitude1 = math.sqrt(magnitude1)
    magnitude2 = math.sqrt(magnitude2)

    if magnitude1 == 0 or magnitude2 == 0:
        return 0

    return dot_product / (magnitude1 * magnitude2)


def retrieve(question, top_k=2):

    # Load indexed documents

    with open(
        INDEX_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        documents = json.load(file)

    # Create embedding for question

    question_embedding = create_embedding(question)

    if question_embedding is None:
        return []

    results = []

    # Compare question with every document

    for document in documents:

        score = cosine_similarity(
            question_embedding,
            document["embedding"]
        )

        results.append({
            "filename": document["filename"],
            "text": document["text"],
            "score": score
        })

    # Sort by similarity

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    question = input("Enter your question: ")

    results = retrieve(question)

    print("\nRetrieved Documents:")
    print("====================")

    for result in results:

        print("\nFile:", result["filename"])

        print(
            "Similarity:",
            round(result["score"], 4)
        )

        print("\nContent:")

        print(result["text"])