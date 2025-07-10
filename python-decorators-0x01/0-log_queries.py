#!/usr/bin/env python3
import sqlite3
import functools

def log_queries():
    """Decorator to log SQL queries before execution."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            query = kwargs.get("query") or (args[0] if args else "")
            print(f"Executing SQL Query: {query}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Test the function
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print(users)
