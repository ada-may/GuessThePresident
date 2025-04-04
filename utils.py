from dateutil import parser
import streamlit as st
from openai import AzureOpenAI
import pandas as pd


def extract_years(term):
    """Extracts the start and end year from a term string."""
    try:
        start_date, end_date = term.split(" - ")
        start_year = parser.parse(start_date).year

        # If the end date is "Incumbent", set it to 2026
        if end_date.strip() == "Incumbent":
            end_year = 2026
        else:
            end_year = parser.parse(end_date).year

        return start_year, end_year
    except ValueError as e:
        print(f"Error parsing term '{term}': {e}")
        return None, None


def parse_term_dates(term):
    start_str, end_str = term.split(" - ")
    start = parser.parse(start_str)
    end = parser.parse(end_str if end_str != "Incumbent" else "2026-01-01")
    return start, end


def display_side_bar():
    # sidebar for API settings
    st.sidebar.header('Settings')


def display_chatbot(president_name, openai_api_key=st.sidebar
                    .text_input('OpenAI API Key'), openai_api_endpoint=st.
                    sidebar.text_input('OpenAI API Endpoint')):
    # chatbot
    user_input = st.text_area(
        "Ask the chatbot to learn more",
        f"I want to learn more about {president_name}.")
    suggestion = st.button("Get Suggestion")  # button
    st.write("💬 Chatbot: ")

    client = AzureOpenAI(
        api_key=openai_api_key,
        api_version="2024-02-15-preview",
        azure_endpoint=openai_api_endpoint
    )

    # ensure client is initialized if API key is provided
    if openai_api_key and openai_api_endpoint and suggestion:
        stream = client.chat.completions.create(
            model="gpt-35-turbo-16k",
            messages=[{"role": "system", "content": "You are a friendly chatbot teaching about presidents"},
                      {"role": "user", "content": user_input}],
            stream=True,
        )
        st.write_stream(stream)


def calculate_durations(df):
    durations = []
    for _, row in df.iterrows():
        start, end = utils.extract_years(row["Term"])
        if start and end:
            durations.append({
                "Name": row["Name"],
                "Start": start,
                "End": end,
                "Years in Office": end - start
            })
    return pd.DataFrame(durations)
