
from scraper import scrape_presidents
import database
import streamlit as st


def main():
    database.reset_database()  # clear existing table
    database.create_table()  # ensure the table is created

    presidents = scrape_presidents()  # Get president data

    # insert each president into the database
    for president in presidents:
        database.insert_president(president)

    st.title("U.S. Presidents Trivia")

    # button to show the full list of presidents
    if st.button("Learn about the Presidents"):
        st.dataframe(database.fetch_all_presidents(),
                     use_container_width=True, height=1680)

if __name__ == "__main__":
    main()
