import utils
import altair as alt
import pandas as pd
import streamlit as st
from scraper import scrape_presidents


def prepare_duartion_data(df):
    duration_df = utils.calculate_durations(df)

    bins = [0, 4, 8, 12]
    labels = ["1-4", "5-8", "9-12"]

    duration_df["Years Served Group"] = pd.cut(
        duration_df["Years in Office"],
        bins=bins,
        labels=labels,
        right=True,
        include_lowest=True
    )
    return duration_df


def get_binned_counts(duration_df):
    binned_counts = duration_df["Years Served Group"].value_counts(
    ).sort_index().reset_index()
    binned_counts.columns = ["Years Served Group", "Number of Presidents"]
    return binned_counts


def plot_years_served_chart(binned_counts):
    return alt.Chart(binned_counts).mark_bar().encode(
        x=alt.X("Years Served Group", title="Years Served"),
        y=alt.Y("Number of Presidents", title="Number of Presidents"),
        tooltip=["Years Served Group", "Number of Presidents"]
    ).properties(height=400)


def get_party_counts(df):
    return df.groupby("party").size().reset_index(name="count")


def plot_party_pie_chart(party_counts):
    return alt.Chart(party_counts).mark_arc().encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="party", type="nominal",
                        legend=alt.Legend(title="Party")),
        tooltip=["party", "count"]
    )


def parse_term_dates(df):
    df[["Start", "End"]] = df["term"].apply(
        lambda t: pd.Series(utils.parse_term_dates(t)))
    df["Start"] = pd.to_datetime(df["Start"])
    df["End"] = pd.to_datetime(df["End"])
    return df


def plot_timeline(df):
    return alt.Chart(df).mark_bar().encode(
        y=alt.Y("name:N", sort="-x", title=None, axis=None),
        x=alt.X("Start:T", title="Start of Term"),
        x2="End:T",
        tooltip=["name", "Start", "End"]
    ).properties(height=200)


df = pd.DataFrame(scrape_presidents())

st.subheader("Presidents by Years Served")
st.altair_chart(plot_years_served_chart(
    get_binned_counts(prepare_duartion_data(df))), use_container_width=True)

st.subheader("Presidents by Political Party")
st.altair_chart(plot_party_pie_chart(
    get_party_counts(df)), use_container_width=True)

st.subheader("Presidents Timeline")
st.altair_chart(plot_timeline(parse_term_dates(df)), use_container_width=True)
