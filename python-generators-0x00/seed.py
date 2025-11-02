#!/usr/bin/env python3
"""
seed.py
Functions:
- connect_db() -> connection to MySQL server (no database selected)
- create_database(connection) -> creates ALX_prodev if not exists
- connect_to_prodev() -> returns connection bound to ALX_prodev
- create_table(connection) -> creates user_data table
- insert_data(connection, csv_path) -> reads CSV and inserts rows
"""

import os
import csv
import uuid
import sqlite3

# Try to import MySQL driver; if it's missing we'll fall back to SQLite
try:
    import mysql.connector
    from mysql.connector import errorcode
    MYSQL_DRIVER = True
except Exception:
    mysql = None
    errorcode = None
    MYSQL_DRIVER = False

# Read DB config from environment with sensible defaults
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", 3306))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"


def connect_db():
    """
    Connect to MySQL server (no default database).
    Returns a mysql.connector connection object or None on fail.
    """
    if not MYSQL_DRIVER:
        return None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            autocommit=False,  # commit manually
        )
        return conn
    except mysql.connector.Error as err:
        print(f"[connect_db] MySQL connection error: {err}")
        return None


def create_database(connection):
    """
    Create the ALX_prodev database if it doesn't exist.
    """
    cursor = connection.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        connection.commit()
        # optional: set default character set and collation if needed
        print(f"Database {DB_NAME} created or already exists")
    except mysql.connector.Error as err:
        print(f"[create_database] Failed creating database: {err}")
        raise
    finally:
        cursor.close()


def connect_to_prodev():
    """
    Connect to the ALX_prodev database and return the connection.
    """
    if not MYSQL_DRIVER:
        return None
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            autocommit=False,
        )
        return conn
    except mysql.connector.Error as err:
        print(f"[connect_to_prodev] MySQL connection error: {err}")
        return None


### SQLite fallback implementations ###

def connect_sqlite_db(db_path=None):
    """Return a sqlite3 connection to a local file (fallback)."""
    if db_path is None:
        db_path = os.path.join(os.path.dirname(__file__), "ALX_prodev.sqlite")
    conn = sqlite3.connect(db_path)
    return conn


def create_table_sqlite(connection):
    """Create the user_data table in SQLite."""
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id TEXT NOT NULL PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL
    );
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        connection.commit()
        print(f"Table {TABLE_NAME} created successfully (sqlite)")
    finally:
        cursor.close()


def insert_data_sqlite(connection, csv_path):
    """Insert rows from CSV into SQLite user_data table."""
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    insert_sql = f"""
    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (?, ?, ?, ?)
    """

    cursor = connection.cursor()
    inserted = 0
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = []
            for row in reader:
                uid = row.get("user_id") or str(uuid.uuid4())
                name = row.get("name", "").strip()
                email = row.get("email", "").strip()
                age_raw = row.get("age", "").strip()
                if not name or not email or not age_raw:
                    continue
                try:
                    age = int(float(age_raw))
                except ValueError:
                    continue
                rows.append((uid, name, email, age))

            if rows:
                cursor.executemany(insert_sql, rows)
                inserted = cursor.rowcount
                connection.commit()
        print(f"Inserted/checked {len(rows)} rows (rowcount: {inserted}) (sqlite)")
    finally:
        cursor.close()


def create_table(connection):
    """
    Create user_data table if it does not exist.
    user_id stored as CHAR(36) (UUID string), PRIMARY KEY.
    age stored as DECIMAL(5,0) per requirement (but int-like values).
    """
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        user_id CHAR(36) NOT NULL,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL(5,0) NOT NULL,
        PRIMARY KEY (user_id),
        INDEX idx_user_id (user_id)
    ) ENGINE=InnoDB;
    """
    cursor = connection.cursor()
    try:
        cursor.execute(create_table_sql)
        connection.commit()
        print(f"Table {TABLE_NAME} created successfully")
    except mysql.connector.Error as err:
        print(f"[create_table] Error creating table: {err}")
        raise
    finally:
        cursor.close()


def insert_data(connection, csv_path):
    """
    Insert rows from CSV into user_data table.
    CSV expected columns: user_id,name,email,age
    If user_id is missing/empty for a row, generate a UUID.
    Duplicate primary keys will be ignored using ON DUPLICATE KEY UPDATE user_id=user_id (no-op).
    """
    # make sure file exists
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    insert_sql = f"""
    INSERT INTO {TABLE_NAME} (user_id, name, email, age)
    VALUES (%s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE user_id = user_id;  -- no-op to skip duplicates
    """

    cursor = connection.cursor()
    inserted = 0
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = []
            for row in reader:
                uid = row.get("user_id") or str(uuid.uuid4())
                name = row.get("name", "").strip()
                email = row.get("email", "").strip()
                age_raw = row.get("age", "").strip()
                if not name or not email or not age_raw:
                    # skip incomplete rows; you may want to log them
                    continue
                # convert age to numeric (DECIMAL field)
                try:
                    # allow integer-like values
                    age = int(float(age_raw))
                except ValueError:
                    # skip rows with invalid age
                    continue
                rows.append((uid, name, email, age))

            # execute many for efficiency
            if rows:
                cursor.executemany(insert_sql, rows)
                inserted = cursor.rowcount
                connection.commit()
        print(f"Inserted/checked {len(rows)} rows (rowcount: {inserted})")
    except mysql.connector.Error as err:
        connection.rollback()
        print(f"[insert_data] DB error: {err}")
        raise
    finally:
        cursor.close()


if __name__ == "__main__":
    # Example usage when running the script directly
    csv_file = os.path.join(os.path.dirname(__file__), "user_data.csv")

    # Try MySQL path first (if the driver is available)
    if MYSQL_DRIVER:
        conn = connect_db()
        if conn:
            try:
                create_database(conn)
            finally:
                conn.close()

            conn = connect_to_prodev()
            if conn:
                try:
                    create_table(conn)
                    if os.path.exists(csv_file):
                        insert_data(conn, csv_file)
                    else:
                        print(f"CSV file not found: {csv_file} -- table created only (mysql)")
                finally:
                    conn.close()
                print("Done (mysql)")
                raise SystemExit(0)
            else:
                print(f"Could not connect to database {DB_NAME}, falling back to SQLite")
        else:
            print("MySQL server not available, falling back to SQLite")

    # Fallback to SQLite if MySQL isn't available or failed
    conn = connect_sqlite_db()
    try:
        create_table_sqlite(conn)
        if os.path.exists(csv_file):
            insert_data_sqlite(conn, csv_file)
        else:
            print(f"CSV file not found: {csv_file} -- table created only (sqlite)")
    finally:
        conn.close()

    print("Done (sqlite)")