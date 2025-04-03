import requests
from scraper import scrape_presidents
from dateutil import parser
import json


def get_events(year):
    """Fetches historical events for a given year."""
    URL = f"https://events.historylabs.io/year/{year}"
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Assuming the API returns JSON
    except requests.exceptions.RequestException as e:
        print(f"Error fetching events for {year}: {e}")
        return None


def extract_years(term):
    """Extracts the start and end year from a term string."""
    try:
        start_date, end_date = term.split(" - ")
        start_year = parser.parse(start_date).year

        # If the end date is "Incumbent", set it to 2026
        if end_date.strip() == "Incumbent":
            end_year = 2026
        else:
            end_year = parser.parse(end_date).year

        return start_year, end_year
    except ValueError as e:
        print(f"Error parsing term '{term}': {e}")
        return None, None


def get_events_for_term(term):
    """Gets all events for years between the start and end of a term."""
    start_year, end_year = extract_years(term)
    print(f"Extracted years: {start_year} to {end_year}")  # Debugging step
    if start_year and end_year:
        events = {}
        for year in range(start_year, end_year):  # Ensure full range is included
            print(f"Fetching events for {year}")  # Debugging step
            events[year] = get_events(year)
        return events
    return None


def process_presidents_and_get_events():
    """Process the presidents and fetch historical events for their term years."""
    presidents = scrape_presidents()  # Get the list of presidents
    all_events = {}

    for president in presidents:
        term = president["term"]
        events = get_events_for_term(term)

        if events:
            # Ensures uniqueness
            unique_key = f"{president['name']} - {president['number']}"
            all_events[unique_key] = {
                "term": term,
                "events": events
            }

            with open("presidents_events.json", "w", encoding="utf-8") as f:
                json.dump(all_events, f, indent=4)


process_presidents_and_get_events()
