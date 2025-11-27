import sqlite3
import csv


# Create/open a database file
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create the users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        age INTEGER
    )
    """)

# Insert data from CSV file
with open("user_data.csv", newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute(
            "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
            (row["name"], row["email"], row["age"])
        )

# Save changes and close
conn.commit()
conn.close()