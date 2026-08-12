import sqlite3

conn = sqlite3.connect("sales.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    city TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    amount REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
)
""")

cursor.execute("""
INSERT OR IGNORE INTO customers VALUES
(1, 'Alice', 'Hyderabad'),
(2, 'Bob', 'Chennai'),
(3, 'John', 'Bangalore')
""")

cursor.execute("""
INSERT OR IGNORE INTO orders VALUES
(101, 1, '2025-01-10', 5000),
(102, 1, '2025-05-15', 8000),
(103, 2, '2025-02-20', 15000),
(104, 3, '2025-03-12', 7000)
""")

conn.commit()
conn.close()

print("Database created successfully!")