from unittest.mock import patch
import pandas as pd
from utils import parse_term_dates, display_chatbot, calculate_durations


def test_parse_term_dates_with_years_only():
    term = "2020-2024"
    start_year, end_year = parse_term_dates(term, just_years=True)
    assert start_year == 2020
    assert end_year == 2024


def test_parse_term_dates_with_incumbent():
    term = "January 20, 2021 - Incumbent"
    start, end = parse_term_dates(term, just_years=True)
    assert start == 2021
    assert end == 2026


def test_parse_term_dates_without_just_years():
    term = "2020-2024"
    start, end = parse_term_dates(term, just_years=False)
    assert start.year == 2020
    assert end.year == 2024


def test_parse_term_dates_with_incumbent_full_date():
    term = "2020-Incumbent"
    start, end = parse_term_dates(term, just_years=False)
    assert start.year == 2020
    assert end.year == 2026


def test_parse_term_dates_with_full_date_range():
    term = "March 4, 1913 - March 4, 1921"
    start, end = parse_term_dates(term, just_years=False)
    assert start.year == 1913
    assert end.year == 1921
    assert start.month == 3  # March
    assert end.month == 3  # March
    assert start.day == 4  # Start day is 4
    assert end.day == 4  # End day is 4


def test_parse_term_dates_with_different_months():
    term = "March 4, 1921 - August 2, 1923"
    start, end = parse_term_dates(term, just_years=False)
    assert start.year == 1921
    assert end.year == 1923
    assert start.month == 3  # March
    assert end.month == 8  # August
    assert start.day == 4  # Start day is 4
    assert end.day == 2  # End day is 2

def test_parse_term_dates_with_only_years():
    term = "1913 - 1921"
    start_year, end_year = parse_term_dates(term, just_years=True)
    assert start_year == 1913
    assert end_year == 1921

@patch("utils.AzureOpenAI")
@patch("utils.st")
def test_display_chatbot_for_hint(mock_st, mock_azure):
    mock_st.secrets = {
        "AZURE_OPENAI_API_KEY": "fake_key",
        "AZURE_OPENAI_ENDPOINT": "https://fake.endpoint"
    }
    display_chatbot("Abraham Lincoln", need_hint=True)
    mock_azure.assert_called_once_with(
        api_key="fake_key",
        azure_endpoint="https://fake.endpoint",
        api_version="2024-02-15-preview"
    )
    mock_st.text_area.assert_not_called()
    mock_st.button.asser_not_called()

@patch("utils.AzureOpenAI")
@patch("utils.st")
def test_display_chatbot_not_for_hint(mock_st, mock_azure):
    mock_st.secrets = {
        "AZURE_OPENAI_API_KEY": "fake_key",
        "AZURE_OPENAI_ENDPOINT": "https://fake.endpoint"
    }
    mock_st.text_area.return_value = "Tell me more"
    mock_st.button.return_value = True
    display_chatbot("George Washington", need_hint=False)
    mock_st.text_area.assert_called_once_with(
        "Ask the chatbot to learn more", "I want to learn more about George Washington."
    )
    mock_st.button.assert_called_once_with("Go")
    mock_azure.assert_called_once()

def test_calculate_durations():
    data = {
        "name": ["George Washington", "Thomas Jefferson", "Abraham Lincoln"],
        "term": ["1789-1797", "1801-1809", "1861-1865"]
    }
    df = pd.DataFrame(data)
    with patch("utils.parse_term_dates", side_effect=lambda term, just_years:
               (int(term.split("-")[0]), int(term.split("-")[1]))):
        result_df = calculate_durations(df)
    assert result_df.shape == (3, 4)
    assert result_df["Years in Office"].iloc[0] == 8  # 1797 - 1789
    assert result_df["Years in Office"].iloc[1] == 8  # 1809 - 1801
    assert result_df["Years in Office"].iloc[2] == 4  # 1865 - 1861
    assert set(result_df.columns) == {
        "Name", "Start", "End", "Years in Office"}
    george_washington = result_df[result_df["Name"] == "George Washington"]
    assert george_washington["Start"].iloc[0] == 1789
    assert george_washington["End"].iloc[0] == 1797
    assert george_washington["Years in Office"].iloc[0] == 8
