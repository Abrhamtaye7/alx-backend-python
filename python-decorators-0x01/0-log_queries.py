import sqlite3
import functools
from datetime import datetime


def log_queries(func):
    """ Decorator to log SQL queries to query.log """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query from args or kwargs
        query = kwargs['query'] if 'query' in kwargs else args[0]
        # Get the current timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Make the log entry
        log_entry = f"[{timestamp}] {func.__name__}: {query}\n"

        # Append the log entry to query.log
        with open('query.log', 'a') as log_file:
            log_file.write(log_entry)
        
        # Print the log entry to the console
        print(log_entry.strip())
        
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")