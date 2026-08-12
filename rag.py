import os


KNOWLEDGE_FOLDER = "knowledge"


def load_documents():
    documents = {}

    for filename in os.listdir(KNOWLEDGE_FOLDER):

        if filename.endswith(".txt"):

            filepath = os.path.join(
                KNOWLEDGE_FOLDER,
                filename
            )

            with open(
                filepath,
                "r",
                encoding="utf-8"
            ) as file:

                documents[filename] = file.read()

    return documents


def retrieve(question):
    documents = load_documents()

    question = question.lower()

    selected = []

    # Customer-related questions
    if "customer" in question or "spent" in question:
        if "customers.txt" in documents:
            selected.append(documents["customers.txt"])

    # Order-related questions
    if (
        "order" in question
        or "spent" in question
        or "amount" in question
        or "revenue" in question
    ):
        if "orders.txt" in documents:
            selected.append(documents["orders.txt"])

    # Business rules
    if (
        "spent" in question
        or "revenue" in question
        or "total" in question
    ):
        if "business_rules.txt" in documents:
            selected.append(documents["business_rules.txt"])

    return "\n\n".join(selected)

if __name__ == "__main__":

    question = input("Enter your question: ")

    context = retrieve(question)

    print("\nRetrieved Context:")
    print("------------------")
    print(context)