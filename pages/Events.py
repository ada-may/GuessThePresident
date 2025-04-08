import streamlit as st
import database
from api import get_events_for_president
import pandas as pd
import utils


def build_events_dataframe(terms):
    events_list = []
    for term_data in terms:
        term_events = term_data.get("events", {})
        for year, events in term_events.items():
            for event in events:
                events_list.append({"Year": year, "Event": event})
    return pd.DataFrame(events_list)


selected_president = st.selectbox(
    "Select a President:", database.fetch_president_names(),
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
                st.write(
                    f"**Number:** {term_data.get('number', 'Unknown')}")
                st.write(f"**Term:** {term_data.get('term', 'Unknown')}")

            df_events = build_events_dataframe(terms)

            if not df_events.empty:
                st.dataframe(df_events, use_container_width=True, height=1000)

            else:
                st.warning("No events found for this term.")
        else:
            st.warning("No terms found for this president.")

    utils.display_chatbot(selected_president)
