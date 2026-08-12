import os
import requests
import sqlite3
from dotenv import load_dotenv
from rag import retrieve

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Gemini API key not found!")
    exit()

question = input("Enter your question: ")

# STEP 1: RETRIEVE CONTEXT

context = retrieve(question)

print("\nRetrieved Context:")
print("------------------")
print(context)

# STEP 2: CREATE PROMPT

prompt = f"""
You are an expert SQLite SQL generator.

Use the retrieved database information below to answer the user's question.

Retrieved information:
{context}

User question:
{question}

Rules:

1. Return ONLY the SQL query.
2. Do not use markdown.
3. Do not explain the query.
4. Use only tables and columns present in the retrieved information.
5. Follow the relationships and business rules.
6. Generate valid SQLite SQL.
"""

# STEP 3: SEND TO GEMINI

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.5-flash:generateContent"

headers = {
    "Content-Type": "application/json",
    "x-goog-api-key": api_key
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

try:

    print("\nGenerating SQL...")

    response = requests.post(
        url,
        headers=headers,
        json=data,
        timeout=120
    )

    if response.status_code != 200:
        print("\nGemini API Error:")
        print(response.text)
        exit()

    result = response.json()

    # STEP 4: GET GENERATED SQL

    sql = result["candidates"][0]["content"]["parts"][0]["text"]

    sql = sql.replace("```sql", "")
    sql = sql.replace("```", "")
    sql = sql.strip()

    print("\nGenerated SQL:")
    print(sql)

    # STEP 5: EXECUTE SQL

    conn = sqlite3.connect("sales.db")
    cursor = conn.cursor()

    cursor.execute(sql)

    results = cursor.fetchall()

    columns = [
        description[0]
        for description in cursor.description
    ]

    conn.close()

    # STEP 6: DISPLAY RESULT

    print("\nQuery Result:")
    print("------------------")

    print(" | ".join(columns))

    print("------------------")

    for row in results:
        print(" | ".join(str(value) for value in row))

except sqlite3.Error as e:

    print("\nDatabase Error:")
    print(e)

except requests.exceptions.Timeout:

    print("\nGemini request timed out.")
    print("Please try running the program again.")

except requests.exceptions.RequestException as e:

    print("\nConnection Error:")
    print(e)

except Exception as e:

    print("\nError:")
    print(e)