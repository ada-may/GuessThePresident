from dateutil import parser
import streamlit as st
from openai import AzureOpenAI
import pandas as pd


def parse_term_dates(term, just_years=False):
    """Converts a president's term string into dates"""
    start_str, end_str = term.split(
        "-")  # split the string by the "-" to start and end
    # strip whitespace and parse start date
    start = parser.parse(start_str.strip())

    # if the term is still going on
    if "Incumbent" in end_str.strip():
        end = parser.parse("2026-01-01")  # placeholder date for ongoing term
    else:
        end = parser.parse(end_str.strip())  # parse end date normally
    # if the user set just_years to true
    if just_years:
        return start.year, end.year  # then just return the years
    return start, end  # return full dates


def display_chatbot(president_name):
    """Make a chatbot to get more information about a president"""

    # input text box pre-filled witha a sample prompt about the
    # specific president
    user_input = st.text_area(
        "Ask the chatbot to learn more",
        f"I want to learn more about {president_name}.")

    # button labeled "Go" that the user must click to send input to the chatbot
    go_button = st.button("Go")

    # output section label for chatbot messages
    st.write("Chatbot: ")

    # text input in sidebar for the user to securely enter their API key
    api_key = st.sidebar.text_input("Enter your OpenAI API key")

    if api_key:
        # if the user entered an API key, initialize the Azure OpenAI client
        client = AzureOpenAI(
            api_key=api_key,
            api_version="2024-02-15-preview",
            azure_endpoint="https://streamlit-oai.openai.azure.com/"
        )

        # if go was pressed
        if go_button:
            stream = client.chat.completions.create(
                model="gpt-35-turbo-16k",
                messages=[{"role": "system", "content": "You are a friendly"
                           " chatbot teaching about presidents"},
                          {"role": "user", "content": user_input}],
                stream=True,
            )
            st.write_stream(stream)  # display the streamed response in the UI
    else:
        # show a warning if the user hasn't entered an API key yet
        st.sidebar.warning("Please enter your OpenAI API key in the sidebar.")


def calculate_durations(df):
    """calculates the durations of a presidency"""
    durations = []  # list to store one dictionary per president
    # loop through each row of the dataframe
    for _, row in df.iterrows():
        # get start and end years of the term
        start, end = parse_term_dates(row["term"], True)
        if start and end:
            # create a dictionary with president's name, term years, and
            # duration
            durations.append({
                "Name": row["name"],
                "Start": start,
                "End": end,
                "Years in Office": end - start  # subtract to get num of years
            })
    # converts the list of dictionaries to a dataframe
    return pd.DataFrame(durations)
