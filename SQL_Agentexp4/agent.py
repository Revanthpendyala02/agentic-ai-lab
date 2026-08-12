import sqlite3
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "sales.db"
)


def list_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
    """)

    tables = cursor.fetchall()

    conn.close()

    return [table[0] for table in tables]


def get_schema():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    tables = list_tables()

    schema = {}

    for table in tables:

        cursor.execute(f"PRAGMA table_info({table})")

        columns = cursor.fetchall()

        schema[table] = [
            column[1]
            for column in columns
        ]

    conn.close()

    return schema


def execute_sql(sql):

    sql = sql.strip().lower()

    if not sql.startswith("select"):
        return {
            "error": "Only SELECT queries are allowed."
        }

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:

        cursor.execute(sql)

        rows = cursor.fetchall()

        columns = [
            description[0]
            for description in cursor.description
        ]

        return {
            "columns": columns,
            "rows": rows
        }

    except Exception as e:

        return {
            "error": str(e)
        }

    finally:

        conn.close()

        def ask_agent(question, context):

            prompt = f"""
        You are a SQL database agent.

        You have access to these tools:

        1. LIST_TABLES
        2. GET_SCHEMA
        3. EXECUTE_SQL

        Your job is to answer the user's question.

        You must work step by step.

        Return ONLY one of these formats:

        LIST_TABLES

        GET_SCHEMA

        EXECUTE_SQL: <SQL query>

        FINAL: <final answer>

        User question:
        {question}

        Previous observations:
        {context}
        """

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text.strip()