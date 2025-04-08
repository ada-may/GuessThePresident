import pytest
import sqlite3
import database
import os
import pandas as pd


DATABASE_NAME = "presidents.db"


@pytest.fixture(autouse=True)
def setup_database():
    if os.path.exists(database.DATABASE_NAME):
        os.remove(database.DATABASE_NAME)
    database.create_table()
    yield
    if os.path.exists(database.DATABASE_NAME):
        os.remove(database.DATABASE_NAME)


def test_create_table():
    conn = sqlite3.connect(database.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(presidents)")
    columns = [column[1] for column in cursor.fetchall()]
    conn.close()
    expected_columns = [
        "number", "picture", "name", "birth_death", "term", "party",
        "election", "vice_president"
    ]
    assert columns == expected_columns


def test_insert_president():
    president = {
        "number": 1,
        "picture": "image_url",
        "name": "George Washington",
        "birth_death": "1732-1799",
        "term": "1789-1797",
        "party": "None",
        "election": "1788",
        "vice_president": "John Adams"
    }
    database.insert_president(president)
    conn = sqlite3.connect(database.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM presidents WHERE name = ?",
                   ("George Washington",))
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result[0] == "George Washington"


def test_fetch_all_presidents():
    president = {
        "number": 2,
        "picture": "image_url",
        "name": "John Adams",
        "birth_death": "1735-1826",
        "term": "1797-1801",
        "party": "Federalist",
        "election": "1796",
        "vice_president": "Thomas Jefferson"
    }
    database.insert_president(president)
    df = database.fetch_all_presidents()
    assert isinstance(df, pd.DataFrame)
    assert "Number" in df.columns
    assert "Name" in df.columns
    assert len(df) > 0


def test_fetch_president_names():
    president = {
        "number": 3,
        "picture": "image_url",
        "name": "Thomas Jefferson",
        "birth_death": "1743-1826",
        "term": "1801-1809",
        "party": "Democratic-Republican",
        "election": "1800",
        "vice_president": "Aaron Burr"
    }
    database.insert_president(president)
    result = database.fetch_president_names()
    assert "Thomas Jefferson" in result
    assert isinstance(result, list)
    assert len(result) > 0


def test_fetch_random_president():
    president = {
        "number": 4,
        "picture": "image_url",
        "name": "James Madison",
        "birth_death": "1751-1836",
        "term": "1809-1817",
        "party": "Democratic-Republican",
        "election": "1808",
        "vice_president": "George Clinton"
    }
    database.insert_president(president)
    result = database.fetch_random_president()
    assert result is not None
    assert "name" in result
    assert "hint" in result
    assert "hint_column" in result


def test_fetch_wrong_presidents():
    correct_president = {
        "number": 5,
        "picture": "image_url",
        "name": "James Monroe",
        "birth_death": "1758-1831",
        "term": "1817-1825",
        "party": "Democratic-Republican",
        "election": "1816",
        "vice_president": "Daniel D. Tompkins"
    }
    wrong_president_1 = {
        "number": 6,
        "picture": "image_url",
        "name": "John Quincy Adams",
        "birth_death": "1767-1848",
        "term": "1825-1829",
        "party": "Democratic-Republican",
        "election": "1824",
        "vice_president": "John C. Calhoun"
    }
    wrong_president_2 = {
        "number": 7,
        "picture": "image_url",
        "name": "Andrew Jackson",
        "birth_death": "1767-1845",
        "term": "1829-1837",
        "party": "Democratic",
        "election": "1828",
        "vice_president": "Martin Van Buren"
    }
    database.insert_president(correct_president)
    database.insert_president(wrong_president_1)
    database.insert_president(wrong_president_2)
    wrong_names = database.fetch_wrong_presidents("James Monroe", count=2)
    assert isinstance(wrong_names, list)
    assert len(wrong_names) == 2
    assert "James Monroe" not in wrong_names


@pytest.mark.parametrize("president, expected_name", [
    ({"number": 6,
      "picture": "image_url",
      "name": "John Quincy Adams",
      "birth_death": "1767-1848",
      "term": "1825-1829",
      "party": "Democratic-Republican",
      "election": "1824",
      "vice_president": "Daniel D. Tompkins"},
     "John Quincy Adams"),
])
def test_insert_president_parametrized(president, expected_name):
    database.insert_president(president)
    conn = sqlite3.connect(database.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM presidents WHERE name = ?",
                   (president["name"],))
    result = cursor.fetchone()
    conn.close()
    assert result is not None
    assert result[0] == expected_name


def count_records_in_presidents():
    conn = sqlite3.connect(database.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM presidents")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def test_reset_database_when_table_exists():
    president = {
        "number": 1,
        "picture": "image_url",
        "name": "George Washington",
        "birth_death": "1732-1799",
        "term": "1789-1797",
        "party": "None",
        "election": "1788",
        "vice_president": "John Adams"
    }
    database.insert_president(president)
    assert count_records_in_presidents() > 0
    database.reset_database()
    assert count_records_in_presidents() == 0


def test_reset_database_when_table_does_not_exist():
    conn = sqlite3.connect(database.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS presidents")
    conn.commit()
    conn.close()
    conn = sqlite3.connect(database.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE "
        "type='table' AND name='presidents'")
    table_exists = cursor.fetchone()
    conn.close()
    assert table_exists is None
    database.reset_database()
    conn = sqlite3.connect(database.DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE"
        " type='table' AND name='presidents'")
    table_exists = cursor.fetchone()
    conn.close()
    assert table_exists is not None
    assert count_records_in_presidents() == 0


def test_empty_database_after_reset():
    president = {
        "number": 1,
        "picture": "image_url",
        "name": "George Washington",
        "birth_death": "1732-1799",
        "term": "1789-1797",
        "party": "None",
        "election": "1788",
        "vice_president": "John Adams"
    }
    database.insert_president(president)
    assert count_records_in_presidents() > 0
    database.reset_database()
    assert count_records_in_presidents() == 0
