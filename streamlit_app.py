import streamlit as st
from database import fetch_all_presidents, create_table, fetch_president_names, fetch_random_president, fetch_wrong_presidents
from api import get_events_for_president
import pandas as pd
import random
import altair as alt
from utils import extract_years
import utils

st.title("U.S. Presidents Trivia")

utils.display_side_bar()

df = fetch_all_presidents()

if st.button("Learn about the Presidents"):
    create_table()
    st.dataframe(df)

if st.button("See events from a specific president's term"):
    selected_president = st.selectbox(
        "Select a President:", fetch_president_names(),
        placeholder="Choose a president")

    if selected_president:
        st.subheader(f"Events for {selected_president}")

        # Fetch events using your API function
        president_data = get_events_for_president(selected_president)

        if president_data and isinstance(president_data, dict):
            st.write(f"**President:** {president_data.get('name', 'Unknown')}")

            terms = president_data.get("terms", [])

            if terms:
                for term_data in terms:
                    st.write("---")
                    st.write(
                        f"**Number:** {term_data.get('number', 'Unknown')}")
                    st.write(f"**Term:** {term_data.get('term', 'Unknown')}")

                    # Convert event data to DataFrame and display
                    events_dict = term_data.get("events", {})

                    if events_dict:
                        events_list = []
                        for year, events in events_dict.items():
                            if events:
                                for event in events:
                                    events_list.append(
                                        {"Year": year, "Event": event})

                        if events_list:
                            df_events = pd.DataFrame(events_list)
                            st.dataframe(df_events)
                        else:
                            st.warning("No events found for this term.")
                    else:
                        st.warning("No events found for this term.")
            else:
                st.warning("No terms found for this president.")
if st.button("Play a game to guess the president"):
    st.title("Guess the President (Quiz Edition)")

    # Store a random president in session state
    if "answer" not in st.session_state:
        result = fetch_random_president()
        if result:
            correct_name, picture_url = result
            wrong_names = fetch_wrong_presidents(correct_name)
            options = wrong_names + [correct_name]
            random.shuffle(options)

            st.session_state.answer = {
                "name": correct_name,
                "picture": picture_url,
                "choices": options
            }

    # Display the picture
    st.image(st.session_state.answer["picture"], width=300)

    # Show radio buttons with the shuffled options
    user_guess = st.radio("Who is this President?",
                          st.session_state.answer["choices"])

    # Submit button
    if st.button("Submit Guess"):
        if user_guess == st.session_state.answer["name"]:
            st.success("Correct! 🎉")
            utils.display_chatbot(st.session_state.answer["name"])

        else:
            st.error(
                f"Incorrect. The correct answer was {st.session_state.answer['name']}.")

    # Try another button
    if st.button("Try Another"):
        result = fetch_random_president()
        if result:
            correct_name, picture_url = result
            wrong_names = fetch_wrong_presidents(correct_name)
            options = wrong_names + [correct_name]
            random.shuffle(options)

            st.session_state.answer = {
                "name": correct_name,
                "picture": picture_url,
                "choices": options
            }


def calculate_durations(df):
    durations = []
    for _, row in df.iterrows():
        start, end = extract_years(row["Term"])
        if start and end:
            durations.append({
                "Name": row["Name"],
                "Start": start,
                "End": end,
                "Years in Office": end - start
            })
    return pd.DataFrame(durations)


if st.button("See charts"):
    duration_df = calculate_durations(df)

    bins = [0, 4, 8, 12]  # You can expand this if needed
    labels = ["1-4", "5-8", "9-12"]

    duration_df["Years Served Group"] = pd.cut(
        duration_df["Years in Office"], bins=bins, labels=labels, right=True, include_lowest=True
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
