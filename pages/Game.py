import streamlit as st
import random
import database
import utils

st.title("Guess the President")

if "correct_count" not in st.session_state:
    st.session_state.correct_count = 0

if "incorrect_count" not in st.session_state:
    st.session_state.incorrect_count = 0

if "answer" not in st.session_state:
    st.session_state.answer = {}


def load_new_question():
    result = database.fetch_random_president()
    if result:
        correct_name, picture_url = result
        wrong_names = database.fetch_wrong_presidents(correct_name)
        options = wrong_names + [correct_name]
        random.shuffle(options)
        st.session_state.answer = {
            "name": correct_name,
            "picture": picture_url,
            "choices": options,
            "guessed": False,
            "feedback": None
        }


# Try another button
if st.button("Try Another"):
    load_new_question()
    st.rerun()


if "answer" not in st.session_state or not st.session_state.answer:
    load_new_question()


answer_data = st.session_state.answer
st.image(st.session_state.answer["picture"], width=300)

st.write("Your score:")
st.write(f"Correct: {st.session_state.correct_count} | Incorrect: {st.session_state.incorrect_count}")
options_with_placeholder = ["Select an option"] + answer_data["choices"]
user_guess = st.radio("Who is this President?",
                      options_with_placeholder, index=0, key="guess_radio")


if not answer_data["guessed"]:
    if st.button("Submit Guess"):
        if user_guess == "Select an option":
            st.warning("Please select a president")
        elif user_guess == answer_data["name"]:
            answer_data["feedback"] = ("success", "Correct!")
            answer_data["guessed"] = True
            st.session_state.correct_count += 1
        else:
            answer_data["feedback"] = (
                "error", f"Incorrect. The correct answer was {answer_data['name']}.")
            answer_data["guessed"] = True
            st.session_state.incorrect_count += 1
        st.rerun()

if answer_data.get("guessed") and answer_data.get("feedback"):
    msg_type, msg_text = answer_data["feedback"]
    if msg_type == "success":
        st.success(msg_text)
    else:
        st.error(msg_text)

    # Chatbot or extra info after guessing
    utils.display_chatbot(answer_data["name"])
