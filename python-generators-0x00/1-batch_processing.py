#!/usr/bin/env python3
"""
1-batch_processing.py
Process user_data in batches using Python generators.
"""

import seed


def stream_users_in_batches(batch_size):
    """Yield user records in batches from MySQL database."""
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
            yield rows                 # ✅ yields the batch instead of returning it
            offset += batch_size
    finally:
        cursor.close()
        connection.close()


def batch_processing(batch_size):
    """Filter users older than 25 from each batch and print them."""
    for batch in stream_users_in_batches(batch_size):   # loop 1
        for user in batch:                              # loop 2
            if user["age"] > 25:
                print(user)                             # ✅ prints directly, no return
