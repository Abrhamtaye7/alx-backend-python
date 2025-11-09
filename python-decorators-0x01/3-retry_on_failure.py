import sqlite3
import functools
import time

# Task 1 decorator to handle database connections
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper

# Task 3 decorator: retry on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    attempts += 1
                    print(f"[RETRY] Attempt {attempts}/{retries} failed: {e}")
                    time.sleep(delay)
            # If all retries fail, raise the last exception
            raise Exception(f"All {retries} retries failed for function {func.__name__}")
        return wrapper
    return decorator

# Example usage
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# Attempt to fetch users with automatic retry
users = fetch_users_with_retry()
print(users)
