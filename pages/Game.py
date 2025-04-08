import streamlit as st
import random
import database
import utils


def initialize_session_state():
    # set default session state values if they don't exist
    st.session_state.setdefault("correct_count", 0)
    st.session_state.setdefault("incorrect_count", 0)
    st.session_state.setdefault("answer", {})
    st.session_state.setdefault("hint", None)


def load_new_question():
    # load a new random president and generate choices
    result = database.fetch_random_president()
    if result:
        correct_name, picture_url, hint, hint_column = result[
            "name"], result["picture"], result["hint"], result["hint_column"]
        wrong_names = database.fetch_wrong_presidents(correct_name)
        options = wrong_names + [correct_name]
        random.shuffle(options)
        # store all question-related info in session state
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
    # display hint if available
    if st.session_state.hint:
        st.write(
            f"**Hint** {st.session_state.answer['hint_column']}:"
            f" {st.session_state.hint}")
    else:
        st.warning("No hint available")


def submit_guess(user_guess):
    # evaluate the user's guess and give feedback
    answer_data = st.session_state.answer
    if user_guess == "Select an option":
        st.warning("Please select a president")
    elif user_guess == answer_data["name"]:
        answer_data["feedback"] = ("success", "Correct!")
        st.session_state.correct_count += 1
        answer_data["guessed"] = True
    else:
        answer_data["feedback"] = (
            "error", "Incorrect. The correct answer was"
            f" {answer_data['name']}.")
        st.session_state.incorrect_count += 1
        answer_data["guessed"] = True


def display_feedback():
    # display message based on guess
    feedback = st.session_state.answer.get("feedback")
    if feedback:
        msg_type, msg_text = feedback
        if msg_type == "success":
            st.success(msg_text)
        else:
            st.error(msg_text)


# UI starts here
st.title("Guess the President")
initialize_session_state()

# load a question if none exists yet
if not st.session_state.answer:
    load_new_question()

answer_data = st.session_state.answer

# show president image
st.image(st.session_state.answer["picture"], width=300)

# hint button
if st.button("Get a Hint"):
    show_hint()

# try another button
if st.button("Try Another"):
    load_new_question()
    st.rerun()

# show current score
st.write("Your score:")
st.write(
    f"Correct: {st.session_state.correct_count} "
    f"| Incorrect: {st.session_state.incorrect_count}")

# show radio options for guessing
options_with_placeholder = ["Select an option"] + answer_data["choices"]
user_guess = st.radio("Who is this President?",
                      options_with_placeholder, index=0, key="guess_radio")

# submit guess button
if not answer_data["guessed"] and st.button("Submit Guess"):
    submit_guess(user_guess)

# if guessed, show feedback and call chatbot
if answer_data.get("guessed"):
    display_feedback()
    utils.display_chatbot(answer_data["name"])
