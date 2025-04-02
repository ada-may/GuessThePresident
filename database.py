import sqlite3

DATABASE_NAME = "presidents.db"


def create_table():
    """Creates the presidents table if it does not exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presidents (
            id INTEGER PRIMARY KEY,
            number INTEGER,
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


def insert_president(data):
    """Inserts a president into the table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO presidents (number, picture, name, birth_death, term,
                   party, election, vice_president)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (data["number"], data["picture"], data["name"], data["birth_death"],
          data["term"], data["party"], data["election"],
          data["vice_president"]))
    conn.commit()
    conn.close()


def fetch_all_presidents():
    """Fetch all records from the presidents table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM presidents")
    records = cursor.fetchall()
    conn.close()

    for record in records:
        print(record)  # Print each row


fetch_all_presidents()
