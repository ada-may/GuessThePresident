import streamlit as st
import random
import database
import utils


def initialize_session_state():
    st.session_state.setdefault("correct_count", 0)
    st.session_state.setdefault("incorrect_count", 0)
    st.session_state.setdefault("answer", {})
    st.session_state.setdefault("hint", None)


def load_new_question():
    result = database.fetch_random_president()
    if result:
        correct_name, picture_url, hint, hint_column = result[
            "name"], result["picture"], result["hint"], result["hint_column"]
        wrong_names = database.fetch_wrong_presidents(correct_name)
        options = wrong_names + [correct_name]
        random.shuffle(options)
        st.session_state.answer = {
            "name": correct_name,
            "picture": picture_url,
            "choices": options,
            "guessed": False,
            "feedback": None,
            "hint": hint,
            "hint_column": hint_column
        }
        st.session_state.hint = hint


def show_hint():
    if st.session_state.hint:
        st.write(
            f"**Hint** {st.session_state.answer['hint_column']}:"
            f" {st.session_state.hint}")
    else:
        st.warning("No hint available")


def submit_guess(user_guess):
    answer_data = st.session_state.answer
    if user_guess == "Select an option":
        st.warning("Please select a president")
    elif user_guess == answer_data["name"]:
        answer_data["feedback"] = ("success", "Correct!")
        st.session_state.correct_count += 1
    else:
        answer_data["feedback"] = (
            "error", f"Incorrect. The correct answer was {answer_data['name']}.")
        st.session_state.incorrect_count += 1
    answer_data["guessed"] = True
    st.rerun()


def display_feedback():
    feedback = st.session_state.answer.get("feedback")
    if feedback:
        msg_type, msg_text = feedback
        if msg_type == "success":
            st.success(msg_text)
        else:
            st.error(msg_text)


st.title("Guess the President")
initialize_session_state()

if not st.session_state.answer:
    load_new_question()

answer_data = st.session_state.answer
st.image(st.session_state.answer["picture"], width=300)

if st.button("Get a Hint"):
    show_hint()

if st.button("Try Another"):
    load_new_question()
    st.rerun()

st.write("Your score:")
st.write(
    f"Correct: {st.session_state.correct_count} "
    f"| Incorrect: {st.session_state.incorrect_count}")
options_with_placeholder = ["Select an option"] + answer_data["choices"]
user_guess = st.radio("Who is this President?",
                      options_with_placeholder, index=0, key="guess_radio")


if not answer_data["guessed"] and st.button("Submit Guess"):
    submit_guess(user_guess)

if answer_data.get("guessed"):
    display_feedback()
    utils.display_chatbot(answer_data["name"])
