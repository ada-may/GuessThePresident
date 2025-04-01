import requests
from scraper import scrape_presidents
from dateutil import parser
import json


# converts a georgian date to the hebrew date
def get_hebrew_date(gy, gm, gd):
    base_url = "https://www.hebcal.com/converter"  # API endpoint
    params = {"cfg": "json", "gy": gy, "gm": gm, "gd": gd,
              "g2h": 1, "strict": 1}  # request parameters
    try:
        response = requests.get(base_url, params=params)  # send get request

        data = response.json()
        formatted_data = {
            # format georgian date
            "Gregorian Date": f"{gy}-{gm:02d}-{gd:02d}",
            "Hebrew Year": data.get("hy", "N/A"),  # get hebrew year
            "Hebrew Month": data.get("hm", "N/A"),  # get hebrew month
            "Hebrew Day": data.get("hd", "N/A")  # get hebrew day
        }
        return formatted_data
    except Exception as e:
        print(f"Error fetching Hebrew date: {e}")
        return None


def convert_to_date(date_str):
    """Converts a date string (e.g., 'March 4, 1913') to a datetime object."""
    try:
        # Use dateutil's parser to convert the date string to a datetime object
        return parser.parse(date_str)
    except ValueError as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None


def process_presidents_and_get_hebrew_dates():
    """Process the presidents and get their Hebrew start and end dates."""
    presidents = scrape_presidents()  # Get the list of presidents

    for president in presidents:
        term = president["term"]  # Get the term (start and end dates)

        # Split the term into start and end dates
        try:
            start_date_str, end_date_str = term.split(" - ")

            # Convert the date strings to datetime objects
            start_date = convert_to_date(start_date_str)
            end_date = convert_to_date(end_date_str)

            # If conversion failed, skip this president
            if not start_date or not end_date:
                print(
                    f"Skipping president {president['name']} due to "
                    "invalid date format.")
                continue

            # Get the Hebrew start date for the president's term
            start_hebrew = get_hebrew_date(
                start_date.year, start_date.month, start_date.day)
            end_hebrew = get_hebrew_date(
                end_date.year, end_date.month, end_date.day)

            if start_hebrew and end_hebrew:
                print(
                    f"Events for {president['name']} ({start_date} -"
                    "{end_date}):")
                print(
                    f"Start Hebrew Date: {json.dumps(start_hebrew, indent=4)}")
                print(f"End Hebrew Date: {json.dumps(end_hebrew, indent=4)}")
                print("-" * 40)  # Separator for clarity

        except ValueError as e:
            print(f"Error processing term for {president['name']}: {e}")


process_presidents_and_get_hebrew_dates()
