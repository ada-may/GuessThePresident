import database
import altair as alt
import pandas as pd
import streamlit as st
from scraper import scrape_presidents

df = scrape_presidents()
duration_df = database.calculate_durations(df)

bins = [0, 4, 8, 12]  # You can expand this if needed
labels = ["1-4", "5-8", "9-12"]

duration_df["Years Served Group"] = pd.cut(
    duration_df["Years in Office"], bins=bins, labels=labels, right=True,
    include_lowest=True
)

# Step 3: Count how many presidents fall into each bin
binned_counts = duration_df["Years Served Group"].value_counts(
).sort_index().reset_index()
binned_counts.columns = ["Years Served Group", "Number of Presidents"]

# Step 4: Plot bar chart
st.subheader("Presidents by Years Served Group")

grouped_chart = alt.Chart(binned_counts).mark_bar().encode(
    x=alt.X("Years Served Group", title="Years Served"),
    y=alt.Y("Number of Presidents", title="Number of Presidents"),
    tooltip=["Years Served Group", "Number of Presidents"]
).properties(height=400)

st.altair_chart(grouped_chart, use_container_width=True)

party_counts = df.groupby("Party").size().reset_index(name="Count")

pie_chart = alt.Chart(party_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field="Count", type="quantitative"),
    color=alt.Color(field="Party", type="nominal",
                    legend=alt.Legend(title="Party")),
    tooltip=["Party", "Count"]
).properties(
    title="Distribution of U.S. Presidents by Political Party"
)

# Show in Streamlit
st.subheader("Presidents by Political Party")
st.altair_chart(pie_chart, use_container_width=True)





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
