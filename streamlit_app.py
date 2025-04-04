import streamlit as st
import utils
import database

st.title("U.S. Presidents Trivia")

st.page_link("home.py", label="Home")
st.page_link("streamlit_pages/game.py", label="Play a guessing game")
st.page_link("streamlit_pages/events.py", label="Learn about events")
st.page_link("streamlit_pages/statistics.py", label="See statistics")

utils.display_side_bar()

if st.button("Learn about the Presidents"):
    database.create_table()
    st.dataframe(database.fetch_all_presidents())

'''can't get this timeline working
df[["Start", "End"]] = df["Term"].apply(
    lambda t: pd.Series(parse_term_dates(t)))

# Create Gantt-style timeline
timeline = alt.Chart(duration_df).mark_bar().encode(
    y=alt.Y("Name:N", sort="-x", title="President"),
    x=alt.X("Start:T", title="Start of Term"),
    x2="End:T",
    color=alt.Color("Party:N", legend=alt.Legend(title="Party")),
    tooltip=["Name", "Start", "End", "Party"]
).properties(
    title="Presidential Timeline",
    height=800
)

st.altair_chart(timeline, use_container_width=True)
'''
