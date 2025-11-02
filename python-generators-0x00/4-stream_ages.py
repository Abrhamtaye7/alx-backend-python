#!/usr/bin/env python3
"""
4-stream_ages.py
Compute the average user age using a generator for memory efficiency.
"""

import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = seed.connect_to_prodev()
    if not connection:
        raise ConnectionError("Failed to connect to ALX_prodev database.")

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data;")

        # Only one loop to yield ages
        for row in cursor:
            yield int(row["age"])  # yield each age
    finally:
        cursor.close()
        connection.close()


def average_age():
    """
    Calculate and print the average age of users using the generator.
    """
    total_age = 0
    count = 0

    for age in stream_user_ages():  # loop 1
        total_age += age
        count += 1

    if count == 0:
        print("No users found.")
        return

    avg = total_age / count
    print(f"Average age of users: {avg:.2f}")

