# flake8: noqa

import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import database
import utils
import streamlit as st


st.title("U.S. Presidents Trivia")


utils.display_side_bar()

if st.button("Learn about the Presidents"):
    database.create_table()
    st.dataframe(database.fetch_all_presidents())
