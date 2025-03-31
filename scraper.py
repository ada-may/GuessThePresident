import requests
from bs4 import BeautifulSoup
import json
import html
import re

URL = "https://en.wikipedia.org/wiki/List_of_presidents_of_the_United_States"

def clean_text(text):
    """Remove footnotes, unwanted characters, and parentheses from the given text."""
    text = re.sub(r'\[\w+]', '', text)  # Remove footnotes like [i], [j], etc.
    text = text.replace("\u00a0", " ")  # Replace non-breaking spaces with normal spaces
    text = text.replace("\u2013", "-")  # Replace en dashes with hyphens
    text = re.sub(r'\s+', ' ', text).strip()  # Replace multiple spaces with a single space
    text = re.sub(r'\(.*?\)', '', text)  # Remove parentheses and everything inside them
    return text if text else "N/A"


def clean_vice_president(vp_text):
    """Formats the vice president text for better readability."""
    vp_text = re.sub(r'\[.*?\]', '', vp_text)  # Remove footnotes
    vp_text = vp_text.replace("\u00a0", " ")  # Replace non-breaking spaces
    vp_text = vp_text.replace("\u2013", "-")  # Normalize dashes
    vp_text = re.sub(r'(?<=\D)(\d{4})', r' \1', vp_text)  # Ensure spacing before years
    return vp_text.strip()

def format_term(term):
    """Formats the term dates for better readability."""
    try:
        term = term.replace("\u2013", "-")
        if "-" in term:
            start_date, end_date = term.split("-")
            return f"{start_date.strip()} - {end_date.strip()}"
        return term.strip()
    except Exception as e:
        print(f"Error formatting term: {e}")
        return term

def clean_election(election):
    """Fixes election formatting issues."""
    election = election.replace("\u00a0", " ")
    election = election.replace("\u2013", " ")
    election = re.sub(r'(\d{4})(?=\d{4})', r'\1 ', election)  # Ensure spacing between years
    election = re.sub(r'\s+', ' ', election).strip()
    return election if election else "N/A"


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
        cols = president.find_all(["th","td"])
        if len(cols) < 7:
            continue
        try:
            number = clean_text(cols[0].get_text(strip=True)) if cols[0] else "N/A"

            img_tag = cols[1].find("img") if cols[1] else None
            picture = "https:" + img_tag["src"] if img_tag else "No Image"

            name_tag = cols[2].find("b") if cols[2] else None
            name = clean_text(name_tag.get_text(strip=True)) if name_tag else "Unknown"

            birth_death_tag = cols[2].find("span", style="font-size: 85%") or cols[2].find("span")
            birth_death = clean_text(birth_death_tag.get_text(strip=True)) if birth_death_tag else "N/A"
            
            term = format_term(clean_text(cols[3].get_text(strip=True))) if cols[3] else "N/A"

            if cols[4].has_attr("style"):
                cols.pop(4)
            party = clean_text(cols[4].get_text(strip=True)) if cols[4] else "N/A"

            election = clean_election(cols[5].get_text(strip=True)) if cols[5] else "N/A"

            vice_president_tag = cols[6] if len(cols) > 6 else None
            vice_president = clean_vice_president(clean_text(vice_president_tag.get_text(separator=" "))) if vice_president_tag else "N/A"

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


presidents = scrape_presidents()
print(json.dumps(presidents, indent=4))