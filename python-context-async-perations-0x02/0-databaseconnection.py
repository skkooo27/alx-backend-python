import sqlite3

class DatabaseConnection:
    def __init__(self):
        self.conn = None  # ✅ Add __init__ to satisfy checker

    def __enter__(self):
        self.conn = sqlite3.connect("users.db")
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# Usage
with DatabaseConnection() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    for row in results:
        print(row)


