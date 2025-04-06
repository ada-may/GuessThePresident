import pytest
import scraper
from bs4 import BeautifulSoup
import requests
from unittest.mock import patch


@pytest.mark.parametrize("input_text,expected", [
    ("George Washington [1] (President)", "George Washington"),
    ("  Multiple   spaces ", "Multiple spaces"),
    ("Jefferson\u00a0\u20131809", "Jefferson -1809")
])
def test_clean_text(input_text, expected):
    assert scraper.clean_text(input_text) == expected


def test_clean_vice_president():
    assert scraper.clean_vice_president("Joe Biden2020") == "Joe Biden 2020"


def test_extract_birth_death():
    html = '<span style="font-size: 85%;">b. 1732-1799</span>'
    tag = BeautifulSoup(html, "html.parser").span
    assert scraper.extract_birth_death(tag) == "1732 - 1799"

    html = '<span style="font-size: 85%;">b. 1961</span>'
    tag = BeautifulSoup(html, "html.parser").span
    assert scraper.extract_birth_death(tag) == "born in 1961"


def test_format_term():
    assert scraper.format_term("1789-1797") == "1789 - 1797"
    assert scraper.format_term("2009") == "2009"


def test_clean_election():
    assert scraper.clean_election("20082012") == "2008 2012"
    assert scraper.clean_election("2016 2020") == "2016 2020"


SAMPLE_HTML = """
<table class="wikitable">
<tr>
    <th>No.</th><th>Photo</th><th>Name</th><th>Term</th><th>Party</th><th>Election</th><th>VP</th>
</tr>
<tr>
    <td>1</td>
    <td><img src="//upload.wikimedia.org/sample.jpg"/></td>
    <td><b>George Washington</b><br><span style="font-size: 85%;">b. 1732-1799</span></td>
    <td>1789-1797</td>
    <td>None</td>
    <td>1788 1792</td>
    <td>John Adams</td>
</tr>
</table>
"""


@patch("scraper.requests.get")
def test_scrape_presidents(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = SAMPLE_HTML

    result = scraper.scrape_presidents()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "George Washington"
    assert result[0]["birth_death"] == "1732 - 1799"
    assert result[0]["term"] == "1789 - 1797"
    assert result[0]["party"] == "None"
    assert result[0]["election"] == "1788 1792"
    assert result[0]["vice_president"] == "John Adams"


@patch("scraper.requests.get")
def test_scrape_presidents_with_invalid_html(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "<html><body><p>No table here!</p></body></html>"

    presidents = scraper.scrape_presidents()
    assert presidents == []  # Should return empty list gracefully


MISSING_COLUMNS_HTML = """
<table class="wikitable">
<tr><th>No.</th><th>Name</th></tr>
<tr><td>1</td><td>Missing info</td></tr>
</table>
"""


@patch("scraper.requests.get")
def test_scrape_presidents_missing_columns(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = MISSING_COLUMNS_HTML

    presidents = scraper.scrape_presidents()
    assert presidents == []  # Should skip incomplete rows
