import streamlit as st
import random
import database
import utils

st.title("Guess the President")

# Store a random president in session state
if "answer" not in st.session_state:
    result = database.fetch_random_president()
    if result:
        correct_name, picture_url = result
        wrong_names = database.fetch_wrong_presidents(correct_name)
        options = wrong_names + [correct_name]
        random.shuffle(options)

        st.session_state.answer = {
            "name": correct_name,
            "picture": picture_url,
            "choices": options
        }

if "answer" in st.session_state:
    st.image(st.session_state.answer["picture"], width=300)

# Show radio buttons with the shuffled options
    user_guess = st.radio("Who is this President?",
                          st.session_state.answer["choices"])

# Submit button
    if st.button("Submit Guess"):
        if user_guess == st.session_state.answer["name"]:
            st.success("Correct! 🎉")
            utils.display_chatbot(st.session_state.answer["name"])

        else:
            st.error(
                f"Incorrect. The correct answer "
                f"was {st.session_state.answer['name']}.")

# Try another button
if st.button("Try Another"):
    result = database.fetch_random_president()
    if result:
        correct_name, picture_url = result
        wrong_names = database.fetch_wrong_presidents(correct_name)
        options = wrong_names + [correct_name]
        random.shuffle(options)

        st.session_state.answer = {
            "name": correct_name,
            "picture": picture_url,
            "choices": options
        }
