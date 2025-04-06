import pytest
from unittest.mock import patch, MagicMock
import api

# Test the get_events function


@patch("api.requests.get")
def test_get_events_success(mock_get):
    # Mock the response object
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"events": [
        {"content": "Event 1"}, {"content": "Event 2"}]}
    mock_get.return_value = mock_response

    result = api.get_events(2020)

    # Check if the result is what we expect
    assert result == {"events": [
        {"content": "Event 1"}, {"content": "Event 2"}]}
    mock_get.assert_called_once_with("https://events.historylabs.io/year/2020")


@patch("api.requests.get")
def test_get_events_failure(mock_get):
    # Mock the response object for failure case
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    mock_response.json.return_value = None
    result = api.get_events(2020)

    # The function should return None on failure
    assert result is None
    mock_get.assert_called_once_with("https://events.historylabs.io/year/2020")


# Test get_events_for_term function
@patch("api.get_events")
@patch("api.parse_term_dates")
def test_get_events_for_term(mock_parse_term_dates, mock_get_events):
    # Mock get_events to return sample data
    mock_parse_term_dates.return_value = (2020, 2024)
    # Mock get_events to return data for each year in the range
    mock_get_events.side_effect = [
        {"events": [{"content": "Event 1"}, {
            "content": "Event 2"}]},  # for 2020
        {"events": [{"content": "Event A"}]},  # for 2021
        {"events": [{"content": "Event B"}]},  # for 2022
        {"events": [{"content": "Event C"}]},  # for 2023
        {"events": [{"content": "Event D"}]},  # for 2024
    ]

    result = api.get_events_for_term("2020-2024")

    assert result == {
        2020: ["Event 1", "Event 2"],
        2021: ["Event A"],
        2022: ["Event B"],
        2023: ["Event C"]
    }


# Test get_events_for_president function
@patch("api.scrape_presidents")
@patch("api.get_events_for_term")
def test_get_events_for_president(mock_get_events_for_term, mock_scrape_presidents):
    # Mock scrape_presidents to return a list of presidents
    mock_scrape_presidents.return_value = [
        {"name": "Abraham Lincoln", "number": 16, "term": "1861-1865"},
        {"name": "Theodore Roosevelt", "number": 26, "term": "1901-1909"}
    ]

    # Mock get_events_for_term to return data for the given terms
    mock_get_events_for_term.side_effect = [
        {1861: ["Event 1"]},  # Events for Lincoln
        {1901: ["Event A"]},  # Events for Roosevelt
    ]

    result = api.get_events_for_president("Abraham Lincoln")

    # Check the expected result for Abraham Lincoln
    expected_result = {
        "name": "Abraham Lincoln",
        "terms": [
            {
                "number": 16,
                "term": "1861-1865",
                "events": {1861: ["Event 1"]}
            }
        ]
    }

    assert result == expected_result
    mock_get_events_for_term.assert_called_once_with("1861-1865")
    mock_scrape_presidents.assert_called_once()

# Test for president not found


@patch("api.scrape_presidents")
def test_get_events_for_president_not_found(mock_scrape_presidents):
    # Mock scrape_presidents to return a list of presidents
    mock_scrape_presidents.return_value = [
        {"name": "Abraham Lincoln", "number": 16, "term": "1861-1865"},
        {"name": "Theodore Roosevelt", "number": 26, "term": "1901-1909"}
    ]

    result = api.get_events_for_president("George Washington")

    # George Washington is not in the list of mock presidents
    assert result is None
    mock_scrape_presidents.assert_called_once()


@patch("api.requests.get")
def test_get_events_empty_response(mock_get):
    # Mock the response object with an empty events list
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"events": []}
    mock_get.return_value = mock_response

    result = api.get_events(2020)

    # The function should return an empty list if no events are found
    assert result == {"events": []}
    mock_get.assert_called_once_with("https://events.historylabs.io/year/2020")


def test_get_events_invalid_year():
    # Passing a string instead of an integer
    result = api.get_events("not_a_year")

    # The function should ideally return None or handle the error gracefully
    assert result is None


def mock_parse_term_dates(term, just_years=True):
    start_str, end_str = term.split("-")
    start_year = int(start_str.strip())

    if "Incumbent" in end_str:
        # If "Incumbent" is in the end part of the term, return the next year as the end year
        end_year = start_year + 1
    else:
        end_year = int(end_str.strip())

    # If just_years is True, return only the years
    if just_years:
        return start_year, end_year
    # Otherwise, return the full datetime objects (or just the start and end years)
    else:
        start = f"{start_year}-01-01"
        end = f"{end_year}-01-01" if end_str != "Incumbent" else "2026-01-01"
        return start, end


@patch("api.parse_term_dates", side_effect=mock_parse_term_dates)
@patch("api.get_events")
def test_get_events_for_term_incumbent(mock_get_events, mock_parse_term_dates):
    # Simulate a president whose term is "2020-incumbent"
    term = "2020-Incumbent"

    # Mock get_events to return sample event data for 2020
    mock_get_events.return_value = {"events": [{"content": "Event 1"}]}

    result = api.get_events_for_term(term)

    # Since the term ends with "incumbent", we expect it to be treated as a single year (2020)
    expected_result = {2020: ["Event 1"]}

    # Assert that the result matches the expected outcome
    assert result == expected_result
    mock_get_events.assert_called_once_with(2020)
    mock_parse_term_dates.assert_called_once_with(term, True)
