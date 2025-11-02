#!/usr/bin/env python3
"""
2-lazy_paginate.py
Implements lazy pagination with generators.
"""

import seed


def paginate_users(page_size, offset):
    """
    Fetches a single page of users from the database.

    Args:
        page_size (int): number of records per page
        offset (int): starting point in the dataset

    Returns:
        list: a list of user dictionaries
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset};")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator that lazily yields pages of user data.

    Args:
        page_size (int): number of records per page

    Yields:
        list: list of user dictionaries (one page per yield)
    """
    offset = 0
    while True:  # only one loop allowed
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
