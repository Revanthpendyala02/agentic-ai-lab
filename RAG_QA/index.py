import os
import json
import requests
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENV_FILE = os.path.join(BASE_DIR, "..", ".env")
DOCUMENT_FOLDER = os.path.join(BASE_DIR, "documents")
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


documents = []

for filename in os.listdir(DOCUMENT_FOLDER):

    if filename.endswith(".txt"):

        filepath = os.path.join(
            DOCUMENT_FOLDER,
            filename
        )

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read().strip()

        print("Indexing:", filename)
        print("Characters:", len(text))

        if not text:
            print("WARNING: File is empty!")
            continue

        embedding = create_embedding(text)

        if embedding is not None:

            documents.append({
                "filename": filename,
                "text": text,
                "embedding": embedding
            })

            print("Embedding created successfully.")

        print()


if not documents:
    print("No documents were successfully indexed.")
    exit()

with open(
    INDEX_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        documents,
        file
    )

print("================================")
print("Indexing completed successfully!")
print("Documents indexed:", len(documents))
print("Index saved to:", INDEX_FILE)
print("================================")