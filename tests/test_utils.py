from unittest.mock import patch
import pandas as pd
from utils import parse_term_dates, calculate_durations


def test_parse_term_dates_with_years_only():
    term = "2020-2024"
    start_year, end_year = parse_term_dates(term, just_years=True)
    assert start_year == 2020
    assert end_year == 2024


def test_parse_term_dates_with_incumbent():
    term = "2020-Incumbent"
    start_year, end_year = parse_term_dates(term, just_years=True)
    assert start_year == 2020
    assert end_year == 2026  # Assuming the end year is the next year


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


def test_parse_term_dates_with_incumbent():
    term = "January 20, 2021 - Incumbent"
    start, end = parse_term_dates(term, just_years=True)
    assert start == 2021
    assert end == 2026  # Assuming the end year is set to 2026 for "Incumbent"


def test_parse_term_dates_with_only_years():
    term = "1913 - 1921"
    start_year, end_year = parse_term_dates(term, just_years=True)
    assert start_year == 1913
    assert end_year == 1921


def test_calculate_durations():
    # Sample data for testing
    data = {
        "name": ["George Washington", "Thomas Jefferson", "Abraham Lincoln"],
        "term": ["1789-1797", "1801-1809", "1861-1865"]
    }
    df = pd.DataFrame(data)

    # Mock parse_term_dates to return predefined start and end years
    with patch("utils.parse_term_dates", side_effect=lambda term, just_years:
               (int(term.split("-")[0]), int(term.split("-")[1]))):
        result_df = calculate_durations(df)

    # Check if the result has the correct structure (3 rows, 4 columns)
    assert result_df.shape == (3, 4)

    # Check that "Years in Office" are correct
    assert result_df["Years in Office"].iloc[0] == 8  # 1797 - 1789
    assert result_df["Years in Office"].iloc[1] == 8  # 1809 - 1801
    assert result_df["Years in Office"].iloc[2] == 4  # 1865 - 1861

    # Check that the columns contain the correct names
    assert set(result_df.columns) == {
        "Name", "Start", "End", "Years in Office"}

    # Check the data for a specific president (George Washington)
    george_washington = result_df[result_df["Name"] == "George Washington"]
    assert george_washington["Start"].iloc[0] == 1789
    assert george_washington["End"].iloc[0] == 1797
    assert george_washington["Years in Office"].iloc[0] == 8
