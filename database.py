import sqlite3

DATABASE_NAME = "presidents.db"


def create_table():
    """Creates the presidents table if it does not exist."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS presidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number INTEGER,
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


def insert_president(data):
    """Inserts a new president into the table."""
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

    return records


def fetch_president_by_name(name):
    """Fetch a president by their name."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM presidents WHERE name = ?", (name,))
    record = cursor.fetchone()
    conn.close()
    return record


def clear_table():
    """Deletes all records from the presidents table."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM presidents")
    conn.commit()
    conn.close()


# Run this when the script is executed directly
if __name__ == "__main__":
    create_table()
    print("Database and table are set up!")
    print("All Presidents:")
    for pres in fetch_all_presidents():
        print(pres)
