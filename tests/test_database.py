import pytest
import sqlite3
import database
import pandas as pd


DATABASE_NAME = "presidents.db"


@pytest.fixture(scope="module")
def setup_database():
    """Create the database and table before tests run."""
    # Create the table if it doesn't exist
    database.create_table()
    yield
    # Cleanup after tests (drop table after tests)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS presidents")
    conn.commit()
    conn.close()


def test_create_table(setup_database):
    """Test if the table is created successfully."""
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(presidents)")
    columns = [column[1] for column in cursor.fetchall()]
    conn.close()

    expected_columns = [
        "number", "picture", "name", "birth_death", "term", "party", "election", "vice_president"
    ]
    assert columns == expected_columns


def test_insert_president(setup_database):
    """Test inserting a president into the table."""
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

    # Verify if the president was inserted
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM presidents WHERE name = ?",
                   ("George Washington",))
    result = cursor.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == "George Washington"


def test_fetch_all_presidents(setup_database):
    """Test fetching all presidents."""
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
    result = database.fetch_all_presidents()

    assert isinstance(result, pd.DataFrame)
    assert "Number" in result.columns
    assert "Name" in result.columns
    assert len(result) > 0  # There should be at least one row


def test_fetch_president_names(setup_database):
    """Test fetching president names."""
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


def test_fetch_random_president(setup_database):
    """Test fetching a random president."""
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


def test_fetch_wrong_presidents(setup_database):
    """Test fetching wrong president names."""
    president = {
        "number": 5,
        "picture": "image_url",
        "name": "James Monroe",
        "birth_death": "1758-1831",
        "term": "1817-1825",
        "party": "Democratic-Republican",
        "election": "1816",
        "vice_president": "Daniel D. Tompkins"
    }
    database.insert_president(president)

    wrong_presidents = database.fetch_wrong_presidents("James Monroe", count=2)

    assert isinstance(wrong_presidents, list)
    assert len(wrong_presidents) == 2
    assert "James Monroe" not in wrong_presidents


@pytest.mark.parametrize("president, expected_name", [
    ({"number": 6, "picture": "image_url", "name": "John Quincy Adams", "birth_death": "1767-1848",
      "term": "1825-1829", "party": "Democratic-Republican", "election": "1824", "vice_president": "Daniel D. Tompkins"},
     "John Quincy Adams"),
])
def test_insert_president_parametrized(setup_database, president, expected_name):
    """Test inserting a president using parameterized test."""
    database.insert_president(president)

    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM presidents WHERE name = ?",
                   (expected_name,))
    result = cursor.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == expected_name
