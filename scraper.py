import requests
from bs4 import BeautifulSoup
import re

# wikipedia page containing the list of presidents
URL = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"


def clean_text(text):
    """Remove footnotes, unwanted characters, and extra spaces from text."""
    text = re.sub(r'\[.*?\]', '',
                  text)  # Remove all footnotes inside square brackets
    text = text.replace("\u00a0", " ").replace(
        "\u2013", "-")  # Normalize spaces and dashes
    text = re.sub(r'\s+', ' ', text).strip()  # Collapse multiple spaces
    text = re.sub(r'\(.*?\)', '', text)  # Remove text inside parentheses
    return text.strip() or "N/A"  # return the clean text or n/a


def clean_vice_president(vp_text):
    """Cleans and formats vice president names."""
    # Ensure spacing before years
    return clean_text(re.sub(r'(?<=\D)(\d{4})', r' \1', vp_text))


def extract_birth_death(tag):
    """Extracts birth and death years properly."""
    if not tag:
        return "N/A"

    text = tag.get_text(strip=True)
    # extract birth and death year
    match = re.search(r'(b\.)?\s*(\d{4})\s*[\u2013-]?\s*(\d{4})?', text)
    if match:
        birth_year = match.group(2)
        death_year = match.group(3)
        # return the years
        if death_year:
            return f"{birth_year} - {death_year}"
        else:
            return f"born in {birth_year}"
    return "N/A"


def format_term(term):
    """Formats the term date range."""
    term = term.replace("\u2013", "-")  # normalize \u2013 to hyphens
    if "-" in term:
        # trim spaces around each part of the date range
        return " - ".join(
            part.strip() for part in term.split("-")
        )
    return term.strip()


def clean_election(election):
    """Cleans and formats election years."""
    election = election.replace("\u00a0", " ").replace(
        "\u2013", " ")  # normalize spacing
    # add spacing between concatenated election years
    return re.sub(r'(\d{4})(?=\d{4})', r'\1 ', election).strip() or "N/A"


def scrape_presidents():
    # send request to wikipedia page
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []

    # parse the html with beautifulsoup
    soup = BeautifulSoup(response.text, "html.parser")

    # finf the first table
    table = soup.find("table", class_="wikitable")
    if not table:
        print("Could not find the presidents table.")
        return []

    # make a list to store the presidents
    presidents = []

    # skip the header row and loop over each table row
    for president in table.find_all("tr")[1:]:
        cols = president.find_all(["th", "td"])
        if len(cols) < 7:
            continue  # skip rows that don't have enough columns
        try:
            # what number president they are
            number = clean_text(cols[0].get_text(strip=True))

            # image of the president
            img_tag = cols[1].find("img")
            picture = "https:" + img_tag["src"]

            # name of the president
            name_tag = cols[2].find("b") or cols[2]
            name = clean_text(name_tag.get_text(strip=True))

            # birth/death of the president
            birth_death_tag = cols[2].find("span", style="font-size: 85%;")
            birth_death = extract_birth_death(birth_death_tag)

            # dates of their term
            term = format_term(clean_text(cols[3].get_text(strip=True)))

            # if a row has extra style columns, then drop the column
            if cols[4].has_attr("style"):
                cols.pop(4)

            # president's political party
            party = clean_text(cols[4].get_text(strip=True))

            # election year(s)
            election = clean_election(cols[5].get_text(strip=True))

            # vice president(s)
            vice_president_tag = cols[6] if len(cols) > 6 else None
            vice_president = clean_vice_president(
                clean_text(vice_president_tag.get_text(separator=" ")))

            # append this president's data as a dictionary
            presidents.append({
                "number": number,
                "picture": picture,
                "name": name,
                "birth_death": birth_death,
                "term": term,
                "party": party,
                "election": election,
                "vice_president": vice_president
            })

        except Exception as e:
            # print any row specific error but keep processing
            print(f"error: {e}")
            continue

    # return the list of presidents
    return presidents
