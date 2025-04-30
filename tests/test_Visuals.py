import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pages')))
import Visuals
import pandas as pd
import utils
from pandas.testing import assert_frame_equal
import altair as alt

def test_prepare_duration_data(monkeypatch):
    sample_data = pd.DataFrame({
        "name": ["A", "B", "C"],
        "term": ["2001-2005", "2001-2009", "1993-2001"]
    })

    def mock_calculate_durations(df):
        return pd.DataFrame({
            "name": ["A", "B", "C"],
            "Years in Office": [4, 8, 8]
        })
    monkeypatch.setattr(utils, "calculate_durations", mock_calculate_durations)
    result = Visuals.prepare_duration_data(sample_data)
    assert list(result.columns) == ["name", "Years in Office", "Years Served Group"]
    assert result["Years Served Group"].tolist() == ["1-4", "5-8", "5-8"]

def test_get_binned_counts():
    input_df = pd.DataFrame({
        "Years Served Group": pd.Categorical(["1-4", "5-8", "5-8"], categories=["1-4", "5-8", "9-12"], ordered=True)
    })
    result = Visuals.get_binned_counts(input_df)
    expected = pd.DataFrame({
        "Years Served Group": pd.Categorical(["1-4", "5-8", "9-12"], categories=["1-4", "5-8", "9-12"], ordered=True),
        "Number of Presidents": [1, 2, 0]
    })
    assert_frame_equal(result, expected)

def test_get_party_counts():
    df = pd.DataFrame({
        "name": ["A", "B", "C", "D"],
        "party": ["Democrat", "Republican", "Democrat", "Independent"]
    })
    result = Visuals.get_party_counts(df)
    expected = pd.DataFrame({
        "party": ["Democrat", "Independent", "Republican"],
        "count": [2, 1, 1]
    })
    assert_frame_equal(result.sort_values("party").reset_index(drop=True),
                       expected.sort_values("party").reset_index(drop=True))

def test_parse_term_dates(monkeypatch):
    df = pd.DataFrame({
        "name": ["X", "Y"],
        "term": ["2001-2005", "2009-2017"]
    })

    def mock_parse_term_dates(term):
        return {
            "2001-2005": ("2001-01-20", "2005-01-20"),
            "2009-2017": ("2009-01-20", "2017-01-20")
        }[term]
    monkeypatch.setattr(utils, "parse_term_dates", mock_parse_term_dates)
    result = Visuals.parse_term_dates(df.copy())
    assert result["Start"].dt.year.tolist() == [2001, 2009]
    assert result["End"].dt.year.tolist() == [2005, 2017]

def test_plot_years_served_chart():
    df = pd.DataFrame({
        "Years Served Group": ["1-4", "5-8", "9-12"],
        "Number of Presidents": [3, 5, 2]
    })
    chart = Visuals.plot_years_served_chart(df)
    assert isinstance(chart, alt.Chart)
    assert chart.mark == "bar"
    assert chart.data.equals(df)
    assert "Years Served Group" in chart.encoding.x.shorthand
    assert "Number of Presidents" in chart.encoding.y.shorthand

def test_plot_timeline():
    df = pd.DataFrame({
        "name": ["A", "B"],
        "Start": pd.to_datetime(["2001-01-20", "2009-01-20"]),
        "End": pd.to_datetime(["2005-01-20", "2017-01-20"])
    })
    chart = Visuals.plot_timeline(df)
    assert isinstance(chart, alt.Chart)
    assert chart.mark == "bar"
    assert chart.data.equals(df)
    assert "Start" in chart.encoding.x.shorthand
    assert chart.encoding.x2.shorthand == 'End:T'
    assert "name" in chart.encoding.y.shorthand
