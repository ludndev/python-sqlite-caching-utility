import sqlite3
import os
import hashlib
from datetime import datetime, timedelta
from config import *


def create_database_if_not_exists(db_file):
    """
    Create the SQLite database file if it doesn't exist.

    Args:
    - db_file (str): The path to the SQLite database file.
    """
    if not os.path.exists(db_file):
        conn = sqlite3.connect(db_file)
        conn.close()
        logging.info(f"SQLite database file created: {db_file}")


def connect_to_database(db_file):
    """
    Open a connection to the SQLite database.

    Args:
    - db_file (str): The path to the SQLite database file.

    Returns:
    - sqlite3.Connection: A connection to the SQLite database.
    """
    conn = sqlite3.connect(db_file)
    logging.info("Connection to database established")
    return conn


def create_table_if_not_exists(conn, table_name, table_schema):
    """
    Create a table if it doesn't exist.

    Args:
    - conn (sqlite3.Connection): A connection to the SQLite database.
    - table_name (str): The name of the table to create.
    - table_schema (str): The schema definition for the table.
    """
    cursor = conn.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    table_exists = cursor.fetchone()
    if not table_exists:
        cursor.execute(f"CREATE TABLE {table_name} ({table_schema})")
        logging.info(f"Table '{table_name}' created")


def close_connection(conn):
    """
    Close the connection to the SQLite database.

    Args:
    - conn (sqlite3.Connection): A connection to the SQLite database.
    """
    conn.commit()
    conn.close()
    logging.info("Connection to database closed")


def init():
    """
    Initialize the SQLite database and return a connection.

    Returns:
    - sqlite3.Connection: A connection to the SQLite database.
    """
    # Define the SQLite database file path
    db_file = 'database.sqlite'

    # Create the database file if it doesn't exist
    create_database_if_not_exists(db_file)

    # Connect to the SQLite database
    conn = connect_to_database(db_file)

    # Define table schemas
    table_schema = ("hash TEXT PRIMARY KEY, "
                    "data TEXT, "
                    "created_at TEXT DEFAULT CURRENT_TIMESTAMP, "
                    "updated_at TEXT DEFAULT CURRENT_TIMESTAMP")

    # Create tables if they don't exist
    create_table_if_not_exists(conn, 'cache', table_schema)

    # Return conn
    return conn


def cache_data(url, data):
    """
    Cache data in the database.

    Args:
    - url (str): The URL associated with the data.
    - data (list or dict): The data to cache.
    """
    # Init connection to the SQLite database
    conn = init()

    # Check if data is not None and is a valid type (list or dictionary)
    if data is None or not isinstance(data, (list, dict)):
        raise ValueError("Data must be a list or dictionary and cannot be None.")

    # Generate a hash from the URL
    url_hash = hashlib.sha256(url.encode()).hexdigest()

    # Check if a record with the same hash exists in the cache table
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cache WHERE hash=?", (url_hash,))
    existing_record = cursor.fetchone()

    if existing_record:
        # Check if the record was updated less than CACHE_DAY day ago
        last_updated = datetime.strptime(existing_record[2], "%Y-%m-%d %H:%M:%S.%f")
        if datetime.now() - last_updated < timedelta(days=CACHE_DAY):
            logging.info(f"Data for URL {url} already cached and updated less than {CACHE_DAY} day ago. Skipping update.")
            return

    # Convert data to string for storage
    data_str = str(data)

    if existing_record:
        # Update the existing record
        cursor.execute(
            "UPDATE cache SET data=?, updated_at=? WHERE hash=?",
            (data_str,
             datetime.now(),
             url_hash))
        logging.info(f"Data for URL {url} updated successfully.")
    else:
        # Insert a new record
        cursor.execute(
            "INSERT INTO cache (hash, data, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (url_hash,
             data_str,
             datetime.now(),
             datetime.now()))
        logging.info(f"Data for URL {url} cached successfully.")

    # Commit changes to the database
    conn.commit()
    close_connection(conn)


def get_data(url):
    """
        Retrieve data from the cache table using URL.

        Args:
        - url (str): The URL associated with the data.

        Returns:
        - list or dict or None: The cached data or None if not found.
    """
    # Init connection to the SQLite database
    conn = init()

    # Generate a hash from the URL
    url_hash = hashlib.sha256(url.encode()).hexdigest()

    # Check if a record with the hash exists in the cache table
    cursor = conn.cursor()
    cursor.execute("SELECT data FROM cache WHERE hash=?", (url_hash,))
    record = cursor.fetchone()

    if record:
        close_connection(conn)
        return eval(record[0])  # Convert string data back to its original type
    else:
        logging.info(f"No data found for the given URL: {url}")
        close_connection(conn)
        return None
