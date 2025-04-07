import requests
from scraper import scrape_presidents
from utils import parse_term_dates


def get_events(year):
    # API url for the given year
    URL = f"https://events.historylabs.io/year/{year}"
    try:
        response = requests.get(URL)  # make a request to get the events
        response.raise_for_status()  # raise an error for bad status codes
        return response.json()  # return the data from the response
    except requests.exceptions.RequestException as e:
        # if any errors occur during the request
        print(f"Error fetching events for {year}: {e}")
        return None


def get_events_for_term(term):
    # parse the start and end years of the term
    start_year, end_year = parse_term_dates(term, True)

    # Create an empty dictionary to hold events for each year
    events_by_year = {}

    # Loop through the range of years from the start to end
    #  of the term (excluding the end year)
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
    # return the dictionary of events by year
    return events_by_year


def get_events_for_president(president_name):
    # scrape the list of all presidents and their info
    presidents = scrape_presidents()
    # filter the list to find presidents matching the given name
    matching_presidents = [
        pres for pres in presidents if pres["name"] == president_name]
    # if no matches are found
    if not matching_presidents:
        return None
    # prepare the result dictionary with the president's name
    result = {"name": president_name, "terms": []}
    # loop through each matching president entry (to handle multiple terms)
    for president in matching_presidents:
        # create a dictionary for the term and events
        term_events = {
            "number": president["number"],  # term number
            "term": president["term"],  # date of term
            "events": get_events_for_term(president["term"])  # events by year
        }
        # add the term info to the result
        result["terms"].append(term_events)
    # return the full result with all terms and events
    return result
