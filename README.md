# Guess the President - click [here](https://guessthepresident.streamlit.app/) to open the app!

## Overview
**Guess the President** is a fun and interactive Streamlit web app all about U.S. presidents. It shows a table with information on every president, lets you see events from their time in office, and includes cool charts to help you explore the data. There is also a guessing game where you try to figure out the president from a photo—hints included if you need them. There’s also a built-in ChatGPT helper to give you clues, and teach you more about the presidents.

## Features
- A fun quiz where you guess the president from a photo, with hints if needed
- Information and events are pulled using web scraping and APIs
- Built-in ChatGPT assistant for clues and to learn more about the historical figures
- Clean and easy-to-use Streamlit interface
- Tested with unit tests and GitHub Actions for test coverage tracking

## Deployed App
You can deploy your app to Streamlit Cloud:
1. Push the repo to GitHub  
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and click “New App”  
3. Choose `ada-may/guessthepresident`  
4. Set the main file to `Main.py`  
5. Add your API key under **Secrets**  
6. Click Deploy

## ChatGPT Integration
This project uses OpenAI’s GPT API to:
- Help users guess based on hints  
- Provide more information on specified presidents 
### How It Works:
In `utils.py`, prompts are sent to `display_chatbot` OpenAI API using the `openai` library, and responses are shown in Streamlit UI blocks.

## Dependencies & Installation
### Required Python packages
This project depends on the following Python libraries:
- `streamlit` – Web app framework for Python
- `openai` – Access to OpenAI's language models
- `beautifulsoup4` – HTML parsing and web scraping
- `requests` – Handling HTTP requests
- `pandas` – Data analysis and manipulation
- `altair` – Declarative charting library for data visualization
- `pytest` – Unit testing framework
- `pytest-cov` – Test coverage reporting for pytest
- `toml` – Working with `.toml` config files (used for settings)

### Dependencies
```
streamlit
openai
beautifulsoup4
requests
pandas
pytest
pytest-cov
altair
toml
```

### How to Run the App Locally
1. **Clone the Repository**  
   ```
   git clone https://github.com/ada-may/guessthepresident.git
   cd guessthepresident
   ```
2. **Create and Activate a Virtual Environment (on Windows)**  
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install Dependencies**  
   ```
   pip install -r requirements.txt --no-warn-script-location
   ```
4. **Add API Secrets**
   Create a file named `secrets.toml` inside a folder called `.streamlit` in your project directory:
   ```
   mkdir .streamlit
   echo "AZURE_OPENAI_API_KEY = "your_openai_api_key" AZURE_OPENAI_ENDPOINT = "your_openai_endpoint" > .streamlit/secrets.toml
   ```
5. **Run the App**
   ```
   streamlit run Main.py
   ```

## Running Tests
```
pytest -v.
```
Tests are located in `/tests`.

[![Tests](https://github.com/ada-may/GuessThePresident/actions/workflows/python-tests.yml/badge.svg)](https://github.com/ada-may/GuessThePresident/actions/workflows/python-tests.yml)

