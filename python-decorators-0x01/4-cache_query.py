import sqlite3
import functools
import time

# Dictionary to store cached query results
query_cache = {}

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

# Task 4 decorator: cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("[CACHE] Returning cached result")
            return query_cache[query]

        # Execute the function and cache its result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Result cached")
        return result
    return wrapper

# Example usage
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute the query and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
