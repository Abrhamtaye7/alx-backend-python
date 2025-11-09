import sqlite3
import functools

# Decorator to handle database connections automatically
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open the database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the function
            result = func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed after function execution
            conn.close()
        return result
    return wrapper

# Example usage
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch a user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)
