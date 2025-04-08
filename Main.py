
from scraper import scrape_presidents
import database
import streamlit as st


def main():
    database.reset_database()
    database.create_table()  # Ensure table exists

    presidents = scrape_presidents()  # Get president data

    for president in presidents:
        database.insert_president(president)  # Store in DB

    st.title("U.S. Presidents Trivia")

    if st.button("Learn about the Presidents"):
        database.create_table()
        st.dataframe(database.fetch_all_presidents(),
                     use_container_width=True, height=1680)


if __name__ == "__main__":
    main()
