import sqlite3
import pandas as pd
import random

DATABASE_NAME = "presidents.db"


def create_table():
    """Creates the presidents table if it does not exist,
    with 'number' as the primary key."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presidents (
            number INTEGER PRIMARY KEY,
            picture TEXT,
            name TEXT UNIQUE,
            birth_death TEXT,
            term TEXT,
            party TEXT,
            election TEXT,
            vice_president TEXT
        )
    ''')
    conn.commit()
    conn.close()


def fetch_all_presidents():
    """Fetch all records from the presidents table
    as a list of dictionaries."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select all columns but without the `id` column, as you've made `number`
    #  the primary key
    cursor.execute(
        "SELECT number, picture, name, birth_death, term, party, election,"
        " vice_president FROM presidents")

    records = cursor.fetchall()
    conn.close()
    # Convert the list of tuples to a list of dictionaries
    columns = ["Number", "Picture", "Name", "Birth & Death",
               "Term", "Party", "Election", "Vice President"]
    df = pd.DataFrame(records, columns=columns)
    return df.drop(columns=["Picture"])


def fetch_president_names():
    """Fetch a president by their name."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM presidents ORDER BY number")
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names


def insert_president(president):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT OR IGNORE INTO presidents
        (number, picture, name, birth_death, term, party, election,
                   vice_president)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        president.get("number"),
        president.get("picture"),
        president.get("name"),
        president.get("birth_death"),
        president.get("term"),
        president.get("party"),
        president.get("election"),
        president.get("vice_president")
    )
    )
    conn.commit()
    conn.close()


def fetch_random_president():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, picture FROM presidents")
    presidents = cursor.fetchall()
    conn.close()

    if presidents:
        return random.choice(presidents)  # returns (name, picture)
    else:
        return None


def fetch_wrong_presidents(correct_name, count=3):
    """Fetches a list of 'count' wrong president names (not
    including the correct one)."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM presidents WHERE name != ? ORDER BY "
        "RANDOM() LIMIT ?", (correct_name, count))
    wrong_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return wrong_names
