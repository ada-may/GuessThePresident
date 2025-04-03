import streamlit as st
from database import fetch_all_presidents

st.title("President Information")

# Fetch data from the database
data = fetch_all_presidents()

# Display each president's information individually
for president in data:
    st.write(f"**{president['Name']}**")
    st.write(f"**Number**: {president['Number']}")
    st.write(f"**Birth & Death**: {president['Birth & Death']}")
    st.write(f"**Term**: {president['Term']}")
    st.write(f"**Party**: {president['Party']}")
    st.write(f"**Election**: {president['Election']}")
    st.write(f"**Vice President**: {president['Vice President']}")
    st.write("---")
