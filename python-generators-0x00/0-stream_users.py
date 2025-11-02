#!/usr/bin/env python3
"""
0-stream_users.py
Generator function that streams rows from MySQL user_data table one by one.
"""

import seed  # reuse our seed.py connection utilities

def stream_users():
    """
    Generator that yields each row from user_data as a dictionary.
    Only one loop is used.

    Yields:
        dict: A single user's data (user_id, name, email, age)
    """
    connection = seed.connect_to_prodev()
    if not connection:
        raise ConnectionError("Failed to connect to ALX_prodev database.")

    try:
        # dictionary=True makes each row a dict automatically
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data;")

        # one loop only
        for row in cursor:
            yield row

    finally:
        cursor.close()
        connection.close()
