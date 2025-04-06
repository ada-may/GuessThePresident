import requests
from scraper import scrape_presidents
from utils import parse_term_dates


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


def get_events_for_term(term):
    """Gets all events for years between the start and end of a term."""
    start_year, end_year = parse_term_dates(term, True)

    # Create an empty dictionary to hold events for each year
    events_by_year = {}

    # Loop through the range of years from the start to end of the term
    for year in range(start_year, end_year):
        # Fetch events for the given year
        data = get_events(year)

        # Ensure we have events data before trying to process it
        if data and "events" in data:
            # Extract only the 'content' from each event and store it in a list
            events_by_year[year] = [event["content"]
                                    for event in data["events"]]
        else:
            # If no events are found, store an empty list
            events_by_year[year] = []

    return events_by_year


def get_events_for_president(president_name):
    """Process the presidents and fetch historical events for their
    term years."""
    presidents = scrape_presidents()
    matching_presidents = [
        pres for pres in presidents if pres["name"] == president_name]

    if not matching_presidents:
        return None

    result = {"name": president_name, "terms": []}

    for president in matching_presidents:
        term_events = {
            "number": president["number"],
            "term": president["term"],
            "events": get_events_for_term(president["term"])
        }
        result["terms"].append(term_events)

    return result


# print(json.dumps(get_events_for_president("Donald Trump"), indent=4))
