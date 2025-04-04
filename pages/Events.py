import streamlit as st
import database
from api import get_events_for_president
import pandas as pd

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
