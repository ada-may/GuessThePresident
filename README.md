# Guess the President

[![Tests Passing](https://github.com/ada-may/guessthepresident/actions/workflows/python-app.yml/badge.svg)](https://github.com/ada-may/guessthepresident/actions)

## Overview

**Guess the President** is a Python Streamlit web app that displays and quizzes users on historical events associated with U.S. Presidents. It pulls data using web scraping and APIs, and includes a built-in ChatGPT-powered assistant to provide additional context, suggest presidents, and guide users in exploring U.S. history.

---

## Features

- Interactive quiz based on real historical presidential events
- Web scraping and API-based event collection
- ChatGPT assistant integration for suggestions and explanations
- Simple and clean Streamlit interface
- Unit tests and test coverage with GitHub Actions

---

## Environment Setup
1. **Clone the Repository**  
   ```bash
   git clone https://github.com/ada-may/guessthepresident.git
   cd guessthepresident
   ```

2. **Create and Activate a Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Your OpenAI API Key**  
   Create a `.env` file in the root directory and add:
   ```ini
   OPENAI_API_KEY=your-api-key-here
   ```

---

## Run the App Locally

```bash
streamlit run app.py
```

Other pages (like `events.py`) are located in the `/pages` directory.

---

## Deployed App

You can deploy your app to Streamlit Cloud:

1. Push the repo to GitHub  
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud) and click “New App”  
3. Choose `ada-may/guessthepresident`  
4. Set the main file to `app.py`  
5. Add your API key under **Secrets**  
6. Click Deploy

> Example: https://guessthepresident.streamlit.app _(Add link once deployed)_

---

## ChatGPT Integration

This project uses OpenAI’s GPT API to:

- Help users guess based on hints  
- Suggest presidents based on event clues  
- Provide deeper context on selected topics  

### How It Works:

In `chatbot.py`, prompts are sent to the OpenAI API using the `openai` library, and responses are shown in Streamlit UI blocks.

---

## Dependencies

```
streamlit
openai
python-dotenv
beautifulsoup4
requests
pandas
pytest
pytest-cov
```

Install with:

```bash
pip install -r requirements.txt
```
---

## Running Tests

```bash
pytest -v.
```

Tests are located in `/tests`, and GitHub Actions automatically runs them on every push.

---