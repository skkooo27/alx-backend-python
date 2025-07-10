import sqlite3

# Connect to or create the users.db file
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create the 'users' table if it doesn't already exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT
)
''')

# Insert some users if they don’t exist yet
cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'John Doe', 'john@example.com')")
cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Jane Doe', 'jane@example.com')")

# Save (commit) and close the connection
conn.commit()
conn.close()

print("✅ Database and users table set up successfully.")
