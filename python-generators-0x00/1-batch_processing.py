#!/usr/bin/env python3
"""
1-batch_processing.py
Process user_data in batches using Python generators.
"""

import seed


def stream_users_in_batches(batch_size):
    """
    Generator that fetches and yields users in batches of 'batch_size'.

    Args:
        batch_size (int): number of records per batch.

    Yields:
        list: batch of user dictionaries.
    """
    connection = seed.connect_to_prodev()
    if not connection:
        raise ConnectionError("Failed to connect to ALX_prodev database.")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total FROM user_data;")
        total_rows = cursor.fetchone()["total"]

        offset = 0
        while offset < total_rows:
            cursor.execute(f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset};")
            rows = cursor.fetchall()
            if not rows:
                break
            yield rows
            offset += batch_size
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users by filtering those older than 25 years.

    Args:
        batch_size (int): number of records per batch.
    """
    for batch in stream_users_in_batches(batch_size):  # loop 1
        for user in batch:  # loop 2
            if user["age"] > 25:
                print(user)
