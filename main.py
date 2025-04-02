from database import create_table
from api import scrape_presidents
from database import insert_president


def main():
    create_table()  # Ensure table exists

    presidents = scrape_presidents()  # Get president data

    for president in presidents:
        insert_president(president)  # Store in DB


if __name__ == "__main__":
    main()
