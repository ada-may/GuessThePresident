from api import scrape_presidents
import database
import utils
import streamlit as st


def main():
    database.create_table()  # Ensure table exists

    presidents = scrape_presidents()  # Get president data

    for president in presidents:
        database.insert_president(president)  # Store in DB

    st.title("U.S. Presidents Trivia")

    utils.display_side_bar()

    if st.button("Learn about the Presidents"):
        database.create_table()
        st.dataframe(database.fetch_all_presidents())


if __name__ == "__main__":
    main()
