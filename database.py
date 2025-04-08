import sqlite3
import pandas as pd
import random

DATABASE_NAME = "presidents.db"  # name of the databse file


def create_table():
    """Creates the presidents table if it does not exist,
    with 'number' as the primary key."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presidents (
            number INTEGER PRIMARY KEY,
            picture TEXT,
            name TEXT,
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
    as a list of dictionaries (except the picture links)."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select all columns but without the `id` column, as you've made `number`
    #  the primary key
    cursor.execute(
        "SELECT number, picture, name, birth_death, term, party, election,"
        " vice_president FROM presidents")
    # fetch all rows as a list of tuples
    records = cursor.fetchall()
    conn.close()
    # define column names for DataFrame
    columns = ["Number", "Picture", "Name", "Birth & Death",
               "Term", "Party", "Election", "Vice President"]
    df = pd.DataFrame(records, columns=columns)  # create DataFrame
    # drop picture column because it is not needed for display
    return df.drop(columns=["Picture"])


def fetch_president_names():
    """Fetch a president by their name."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM presidents ORDER BY number")
    # convert the rows into a list of names
    names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return names


def insert_president(president):
    """Insert a new president into the database"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Check if the president already exists
    cursor.execute("SELECT 1 FROM presidents WHERE number = ?",
                   (president.get("number"),))
    if cursor.fetchone():
        conn.close()
        return  # Skip inserting if the president exists

    cursor.execute('''
        INSERT INTO presidents
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
    """Fetch one random president and return a hint about them"""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Select all relevant columns for hint purposes
    cursor.execute(
        "SELECT name, picture, birth_death AS [Birth/Death], term, party,"
        " election as [Election Date], vice_president as [Vice President] "
        "FROM presidents")
    # get all records from the query
    presidents = cursor.fetchall()
    conn.close()

    if presidents:
        # Randomly pick a president
        president = random.choice(presidents)

        # Randomly choose a hint column
        hint_columns = ['Birth/Death', 'term', 'party',
                        'Election Date', 'Vice President']
        hint_column = random.choice(hint_columns)

        # Create a dictionary to return both name, picture, and hint
        president_info = {
            'name': president[0],
            'picture': president[1],
            # Offset by 2 because of name and pic
            'hint': president[hint_columns.index(hint_column) + 2],
            'hint_column': hint_column  # which column the hint is from
        }

        return president_info
    else:
        return None


def fetch_wrong_presidents(correct_name, count=3):
    """Fetches a list of 3 wrong president names (not
    including the correct one)."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    # select random names from the database, excluding the correct name
    cursor.execute(
        "SELECT name FROM presidents WHERE name != ? ORDER BY "
        "RANDOM() LIMIT ?", (correct_name, count))
    # return only the names as a list
    wrong_names = [row[0] for row in cursor.fetchall()]
    conn.close()
    return wrong_names


def reset_database():
    """Reset the database by deleting all records from the tables."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Create the presidents table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presidents (
            number INTEGER PRIMARY KEY,
            picture TEXT,
            name TEXT,
            birth_death TEXT,
            term TEXT,
            party TEXT,
            election TEXT,
            vice_president TEXT
        )
    ''')
    # Delete all rows from the presidents table
    cursor.execute("DELETE FROM presidents")
    conn.commit()
    conn.close()
