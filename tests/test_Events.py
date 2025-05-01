import pages.Events as Events
import pytest
from unittest.mock import patch
import pandas as pd

def test_build_events_dataframe():
    terms = [
        {
            "events": {
                "1789": ["Inaugurated as president"],
                "1790": ["First State of the Union"]
            }
        }
    ]
    df = Events.build_events_dataframe(terms)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert df.iloc[0]["Year"] == "1789"
    assert df.iloc[0]["Event"] == "Inaugurated as president"

def test_extract_terms():
    data = {"terms": [{"term": "1789-1793"}]}
    terms = Events.extract_terms(data)
    assert isinstance(terms, list)
    assert terms[0]["term"] == "1789-1793"

@patch("pages.Events.get_events_for_president")
def test_fetch_president_data(mock_api):
    mock_api.return_value = {"name": "George Washington", "terms": []}
    data = Events.fetch_president_data("George Washington")
    assert data["name"] == "George Washington"

@patch("pages.Events.st")
def test_display_term_info(mock_st):
    terms = [{"number": 1, "term": "1789-1793"}]
    Events.display_term_info(terms)
    mock_st.write.assert_any_call("**Number:** 1")
    mock_st.write.assert_any_call("**Term:** 1789-1793")

@patch("pages.Events.st")
def test_display_events_dataframe(mock_st):
    terms = [{"events": {"1789": ["Inaugurated"]}}]
    Events.display_events_dataframe(terms)
    assert mock_st.dataframe.called

@patch("pages.Events.st")
def test_display_events_dataframe_empty(mock_st):
    terms = [{"events": {}}]
    Events.display_events_dataframe(terms)
    mock_st.warning.assert_called_once_with("No events found for this term.")

@patch("pages.Events.utils.display_chatbot")
@patch("pages.Events.fetch_president_data")
@patch("pages.Events.st")
def test_show_president_events(mock_st, mock_fetch, mock_chatbot):
    mock_fetch.return_value = {
        "name": "George Washington",
        "terms": [
            {"number": 1, "term": "1789-1793", "events": {"1789": ["Inaugurated"]}}
        ]
    }
    Events.show_president_events("George Washington")
    mock_st.subheader.assert_called_once_with("Events for George Washington")
    mock_st.write.assert_any_call("**President:** George Washington")
    mock_chatbot.assert_called_once_with("George Washington")
