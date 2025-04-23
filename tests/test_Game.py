import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../pages')))
import Game
from types import SimpleNamespace
import pytest
from unittest.mock import MagicMock, patch

class MockSessionState(SimpleNamespace):
    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def setdefault(self, key, default=None):
        if not hasattr(self, key):
            setattr(self, key, default)
        return getattr(self, key)
    
@patch.object(Game, "st")
def test_initialize_session_state(mock_st):
    mock_st.session_state = MockSessionState()
    mock_st.session_state["correct_count"] = 0
    mock_st.session_state["incorrect_count"] = 0
    mock_st.session_state["answer"] = {}
    mock_st.session_state["hint"] = None
    mock_st.session_state["show_ai_hint"] = False
    Game.initialize_session_state()
    assert mock_st.session_state["correct_count"] == 0
    assert mock_st.session_state["incorrect_count"] == 0
    assert isinstance(mock_st.session_state["answer"], dict)
    assert mock_st.session_state["hint"] is None
    assert mock_st.session_state["show_ai_hint"] is False

@patch.object(Game, "st")
@patch("Game.database.fetch_random_president")
@patch("Game.database.fetch_wrong_presidents")
def test_load_new_question(mock_wrong, mock_fetch, mock_st):
    mock_st.session_state = MockSessionState()
    mock_fetch.return_value = {
        "name": "George Washington",
        "picture": "http://image.jpg",
        "hint": "First president",
        "hint_column": "Fun Fact"
    }
    mock_wrong.return_value = ["John Adams", "Thomas Jefferson"]
    mock_st.session_state["answer"] = {}
    mock_st.session_state["hint"] = None
    mock_st.session_state["show_ai_hint"] = False
    Game.load_new_question()
    answer = mock_st.session_state["answer"]
    assert answer["name"] == "George Washington"
    assert len(answer["choices"]) == 3
    assert "George Washington" in answer["choices"]
    assert mock_st.session_state["hint"] == "First president"
    assert mock_st.session_state["show_ai_hint"] is False

@patch.object(Game, "st")
def test_show_hint_with_hint(mock_st):
    # Set up mock session state
    mock_st.session_state = MockSessionState(
        hint="Here is a hint",
        answer={"hint_column": "Fun Fact", "hint": "Here is a hint"}
    )
    with patch.object(mock_st, "write") as mock_write:
        Game.show_hint()
        mock_write.assert_called_once_with("**Hint** Fun Fact: Here is a hint")

@patch.object(Game, "st")
def test_submit_guess_correct(mock_st):
    mock_st.session_state = MockSessionState()
    mock_st.session_state["correct_count"] = 0
    mock_st.session_state["incorrect_count"] = 0
    mock_st.session_state["answer"] = {
        "name": "George Washington",
        "guessed": False
    }
    Game.submit_guess("George Washington")
    assert mock_st.session_state["correct_count"] == 1
    assert mock_st.session_state["answer"]["guessed"] is True
    assert mock_st.session_state["answer"]["feedback"][0] == "success"

@patch.object(Game, "st")
def test_submit_guess_incorrect(mock_st):
    mock_st.session_state = MockSessionState()
    mock_st.session_state["correct_count"] = 0
    mock_st.session_state["incorrect_count"] = 0
    mock_st.session_state["answer"] = {
        "name": "George Washington",
        "guessed": False
    }
    Game.submit_guess("John Adams")
    assert mock_st.session_state["incorrect_count"] == 1
    assert mock_st.session_state["answer"]["guessed"] is True
    assert mock_st.session_state["answer"]["feedback"][0] == "error"

@patch.object(Game, "st")
def test_display_feedback_success(mock_st):
    mock_st.session_state = MockSessionState(
        answer={"feedback": ("success", "Great job!")}
    )
    with patch.object(mock_st, "success") as mock_success:
        Game.display_feedback()
        mock_success.assert_called_once_with("Great job!")

@patch.object(Game, "st")
def test_display_feedback_error(mock_st):
    mock_st.session_state = MockSessionState(
        answer={"feedback": ("error", "Oops!")}
    )
    with patch.object(mock_st, "error") as mock_error:
        Game.display_feedback()
        mock_error.assert_called_once_with("Oops!")

@patch.object(Game, "st")
@patch.object(Game.utils, "display_chatbot")
def test_ai_hint_logic(mock_chatbot, mock_st):
    mock_st.session_state = MockSessionState(
        answer={"name": "George Washington"},
        show_ai_hint=True
    )
    Game.utils.display_chatbot("George Washington", True)
    mock_chatbot.assert_called_once_with("George Washington", True)

@patch.object(Game, "st")
@patch.object(Game, "load_new_question")
def test_try_another_button(mock_load, mock_st):
    mock_st.session_state = MockSessionState(answer={})
    with patch.object(mock_st, "button", side_effect=[False, False, True, False, False, False]):
        Game.initialize_session_state()
        Game.load_new_question()
        assert mock_load.called

@patch.object(Game, "st")
def test_submit_guess_button_logic(mock_st):
    mock_st.session_state = MockSessionState(
        answer={"name": "George Washington", "choices": ["George Washington"], "guessed": False}
    )
    with patch.object(mock_st, "button", side_effect=[False, False, False, False, True]), \
         patch.object(Game, "submit_guess") as mock_submit:
        mock_st.radio.return_value = "George Washington"
        Game.submit_guess("George Washington")
        assert mock_submit.called

@patch.object(Game, "st")
@patch.object(Game, "show_hint")
def test_get_a_hint_button_calls_show_hint(mock_show_hint, mock_st):
    mock_st.session_state = MockSessionState(
        answer={
            "name": "George Washington",
            "picture": "http://fakeurl.com/image.jpg",
            "choices": ["George Washington", "John Adams"],
            "guessed": False,
            "feedback": None,
            "hint": "First President",
            "hint_column": "Fun Fact"
        },
        hint="First President",
        correct_count=0,
        incorrect_count=0,
        show_ai_hint=False,
        guess_radio="George Washington"
    )
    mock_st.session_state.get = lambda key, default=None: getattr(mock_st.session_state, key, default)
    mock_st.button.side_effect = lambda label: label == "Get a Hint"
    with patch.object(mock_st, "write"):
        Game.render_game_ui()
    mock_show_hint.assert_called_once()
