import requests
from bs4 import BeautifulSoup
import re

URL = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"


def clean_text(text):
    """Remove footnotes, unwanted characters, and extra spaces from text."""
    text = re.sub(r'\[.*?\]', '',
                  text)  # Remove all footnotes inside square brackets
    text = text.replace("\u00a0", " ").replace(
        "\u2013", "-")  # Normalize spaces and dashes
    text = re.sub(r'\s+', ' ', text).strip()  # Collapse multiple spaces
    text = re.sub(r'\(.*?\)', '', text)  # Remove text inside parentheses
    return text or "N/A"


def clean_vice_president(vp_text):
    """Cleans and formats vice president names."""
    # Ensure spacing before years
    return clean_text(re.sub(r'(?<=\D)(\d{4})', r' \1', vp_text))


def extract_birth_death(tag):
    """Extracts birth and death years properly."""
    if not tag:
        return "N/A"

    text = tag.get_text(strip=True)
    # Match birth and death year
    match = re.search(r'(b\.)?\s*(\d{4})\s*[\u2013-]?\s*(\d{4})?', text)
    if match:
        birth_year = match.group(2)
        death_year = match.group(3)

        if death_year:
            return f"{birth_year} - {death_year}"
        else:
            return f"born in {birth_year}"
    return "N/A"


def format_term(term):
    """Formats the term date range."""
    term = term.replace("\u2013", "-")
    if "-" in term:
        return " - ".join(
            part.strip() for part in term.split("-")
        )
    return term.strip()


def clean_election(election):
    """Cleans and formats election years."""
    election = election.replace("\u00a0", " ").replace("\u2013", " ")
    return re.sub(r'(\d{4})(?=\d{4})', r'\1 ', election).strip() or "N/A"


def scrape_presidents():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to retrieve data")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="wikitable")
    if not table:
        print("Could not find the presidents table.")
        return []

    presidents = []

    for president in table.find_all("tr")[1:]:
        cols = president.find_all(["th", "td"])
        if len(cols) < 7:
            continue
        try:
            number = clean_text(cols[0].get_text(strip=True))

            img_tag = cols[1].find("img")
            picture = "https:" + img_tag["src"]

            name_tag = cols[2].find("b") or cols[2]
            name = clean_text(name_tag.get_text(strip=True))

            birth_death_tag = cols[2].find("span", style="font-size: 85%;")
            birth_death = extract_birth_death(birth_death_tag)
            term = format_term(clean_text(cols[3].get_text(strip=True)))

            if cols[4].has_attr("style"):
                cols.pop(4)
            party = clean_text(cols[4].get_text(strip=True))

            election = clean_election(cols[5].get_text(strip=True))

            vice_president_tag = cols[6] if len(cols) > 6 else None
            vice_president = clean_vice_president(
                clean_text(vice_president_tag.get_text(separator=" ")))

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
            print(f"error: {e}")
            continue

    return presidents

