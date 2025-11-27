import time
import sqlite3 
import functools
import json

CACHE_TTL = 10  # Time-to-live for cached result in seconds
CACHE_FILE = "query_cache.json"

# Load cache from file at startup and make it available as the variable dictionary query_cache
try:
    with open(CACHE_FILE, "r") as f:
        query_cache = json.load(f)  # {"query": [result, timestamp]}
except (FileNotFoundError, json.JSONDecodeError):  # If the file doesn't exist or is empty
    # Initialize an empty cache
    query_cache = {}

def save_cache():
    """Saves the updated cache to the file for persistence"""
    with open(CACHE_FILE, "w") as f:
        # indent=4 makes the JSON pretty-printed with 4 spaces per indent
        json.dump(query_cache, f, indent=4, default=str)


def cache_query(func):
    """A decorator that caches the results of database queries"""
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Get the current time
        now = time.time()

        # Check if the query result is already cached
        if query in query_cache:
            timestamp, result = query_cache[query]
            # Check if the cached result is still valid
            if now - timestamp < CACHE_TTL:  # If the cache is recent (less than CACHE_TTL seconds old)
                return result
        
        # If not cached, execute the query and cache the result
        result = func(conn, query, *args, **kwargs)
        # Only update the result and timestamp in the cache for this query
        query_cache[query] = (now, result)
        # Save the updated cache to the file for persistence
        save_cache()

        return result
    return wrapper

"""
# Without cache persistence
CACHE_TTL = 10  # Time-to-live for cached result in seconds

query_cache = {}  # stores for each key query: (timestamp, result)

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Get the current time
        now = time.time()

        # Check if the query result is already cached
        if query in query_cache:
            timestamp, result = query_cache[query]
            # Check if the cached result is still valid
            if now - timestamp < CACHE_TTL:  # If the cache is recent (less than CACHE_TTL seconds old)
                return result
        
        # If not cached, execute the query and cache the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = (now, result)
        return result
    return wrapper
"""

def with_db_connection(func):
    """A decorator that automatically handles opening and closing database connections""" 
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("users.db")
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

first_user = fetch_users_with_cache(query="SELECT * FROM users WHERE id=1")