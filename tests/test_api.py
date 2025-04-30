from unittest.mock import patch, MagicMock
import api

@patch("api.requests.get")
def test_get_events_success(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"events": [
        {"content": "Event 1"}, {"content": "Event 2"}]}
    mock_get.return_value = mock_response
    result = api.get_events(2020)
    assert result == {"events": [
        {"content": "Event 1"}, {"content": "Event 2"}]}
    mock_get.assert_called_once_with("https://events.historylabs.io/year/2020")

@patch("api.requests.get")
def test_get_events_failure(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response
    mock_response.json.return_value = None
    result = api.get_events(2020)
    assert result is None
    mock_get.assert_called_once_with("https://events.historylabs.io/year/2020")

@patch("api.get_events")
@patch("api.parse_term_dates")
def test_get_events_for_term(mock_parse_term_dates, mock_get_events):
    mock_parse_term_dates.return_value = (2020, 2024)
    mock_get_events.side_effect = [
        {"events": [{"content": "Event 1"}, {
            "content": "Event 2"}]},
        {"events": [{"content": "Event A"}]},
        {"events": [{"content": "Event B"}]},
        {"events": [{"content": "Event C"}]},
        {"events": [{"content": "Event D"}]},
    ]
    result = api.get_events_for_term("2020-2024")
    assert result == {
        2020: ["Event 1", "Event 2"],
        2021: ["Event A"],
        2022: ["Event B"],
        2023: ["Event C"]
    }

@patch("api.scrape_presidents")
@patch("api.get_events_for_term")
def test_get_events_for_president(mock_get_events_for_term,
                                  mock_scrape_presidents):
    mock_scrape_presidents.return_value = [
        {"name": "Abraham Lincoln", "number": 16, "term": "1861-1865"},
        {"name": "Theodore Roosevelt", "number": 26, "term": "1901-1909"}
    ]
    mock_get_events_for_term.side_effect = [
        {1861: ["Event 1"]},
        {1901: ["Event A"]},
    ]
    result = api.get_events_for_president("Abraham Lincoln")
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

@patch("api.scrape_presidents")
def test_get_events_for_president_not_found(mock_scrape_presidents):
    mock_scrape_presidents.return_value = [
        {"name": "Abraham Lincoln", "number": 16, "term": "1861-1865"},
        {"name": "Theodore Roosevelt", "number": 26, "term": "1901-1909"}
    ]
    result = api.get_events_for_president("George Washington")
    assert result is None
    mock_scrape_presidents.assert_called_once()

@patch("api.requests.get")
def test_get_events_empty_response(mock_get):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"events": []}
    mock_get.return_value = mock_response
    result = api.get_events(2020)
    assert result == {"events": []}
    mock_get.assert_called_once_with("https://events.historylabs.io/year/2020")

def test_get_events_invalid_year():
    result = api.get_events("not_a_year")
    assert result is None

def mock_parse_term_dates(term, just_years=True):
    start_str, end_str = term.split("-")
    start_year = int(start_str.strip())
    if "Incumbent" in end_str:
        end_year = start_year + 1
    else:
        end_year = int(end_str.strip())
    if just_years:
        return start_year, end_year
    else:
        start = f"{start_year}-01-01"
        end = f"{end_year}-01-01" if end_str != "Incumbent" else "2026-01-01"
        return start, end

@patch("api.parse_term_dates", side_effect=mock_parse_term_dates)
@patch("api.get_events")
def test_get_events_for_term_incumbent(mock_get_events, mock_parse_term_dates):
    term = "2020-Incumbent"
    mock_get_events.return_value = {"events": [{"content": "Event 1"}]}
    result = api.get_events_for_term(term)
    expected_result = {2020: ["Event 1"]}
    assert result == expected_result
    mock_get_events.assert_called_once_with(2020)
    mock_parse_term_dates.assert_called_once_with(term, True)
