import streamlit as st
import database
from api import get_events_for_president
import pandas as pd
import utils


def build_events_dataframe(terms):
    # convert nested event data into a flat DataFrame
    events_list = []
    for term_data in terms:
        term_events = term_data.get("events", {})
        for year, events in term_events.items():
            for event in events:
                events_list.append({"Year": year, "Event": event})
    return pd.DataFrame(events_list)


def fetch_president_data(president_name):
    # get detailed data for a specific president
    data = get_events_for_president(president_name)
    if data and isinstance(data, dict):
        return data
    return None


def extract_terms(president_data):
    # extract the list of terms from president data
    return president_data.get("terms", []) if president_data else []


def display_term_info(terms):
    # show basic term information
    for term_data in terms:
        st.write(f"**Number:** {term_data.get('number', 'Unknown')}")
        st.write(f"**Term:** {term_data.get('term', 'Unknown')}")


def display_events_dataframe(terms):
    # build and display a DataFrame of events
    df_events = build_events_dataframe(terms)
    if not df_events.empty:
        st.dataframe(df_events, use_container_width=True, height=1000)
    else:
        st.warning("No events found for this term.")


def show_president_events(president_name):
    # main function to display all data for a selected president
    st.subheader(f"Events for {president_name}")
    data = fetch_president_data(president_name)

    if data:
        st.write(f"**President:** {data.get('name', 'Unknown')}")
        terms = extract_terms(data)
        if terms:
            display_term_info(terms)
            display_events_dataframe(terms)
        else:
            st.warning("No terms found for this president.")
        utils.display_chatbot(president_name)

if __name__ == "__main__":
    # UI: President selector and event display
    selected_president = st.selectbox(
        "Select a President:", database.fetch_president_names(),
        placeholder="Choose a president")

    if selected_president:
        show_president_events(selected_president)
