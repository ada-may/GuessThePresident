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


def display_chatbot(president_name, need_hint=False):
    """Make a chatbot to get more information about a president or give a hint"""
    # if the user entered an API key, initialize the Azure OpenAI client
    client = AzureOpenAI(
        api_key=st.secrets["AZURE_OPENAI_API_KEY"],
        azure_endpoint=st.secrets["AZURE_OPENAI_ENDPOINT"],
        api_version="2024-02-15-preview"
    )

    # decide the user prompt based on hint mode
    if need_hint:
        prompt = f"Give a hint about {president_name} without saying his name"
        run_chat = True
    else:
        # input text box pre-filled witha a sample prompt about the specific president
        prompt = st.text_area(
            "Ask the chatbot to learn more",
            f"I want to learn more about {president_name}.")

        # button labeled "Go" that the user must click to send input to the chatbot
        run_chat = st.button("Go")

    # if go was pressed
    if run_chat:
        stream = client.chat.completions.create(
            model="gpt-35-turbo-16k",
            messages=[{"role": "system", "content": "You are a friendly"
                       " chatbot teaching about presidents"},
                      {"role": "user", "content": prompt}
                      ],
            stream=True,
        )
        st.write_stream(stream)  # display the streamed response in the UI


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
