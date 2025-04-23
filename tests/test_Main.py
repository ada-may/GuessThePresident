import Main
from unittest.mock import patch

@patch("Main.database.fetch_all_presidents")
@patch("Main.st.dataframe")
@patch("Main.st.button")
@patch("Main.st.title")
@patch("Main.database.insert_president")
@patch("Main.scrape_presidents")
@patch("Main.database.create_table")
@patch("Main.database.reset_database")
def test_main(mock_reset, mock_create, mock_scrape, mock_insert, mock_title, mock_button, mock_df, mock_fetch):
    mock_scrape.return_value = [
        {"name": "George Washington", "years": "1789-1797"}
    ]
    mock_button.return_value = True
    mock_fetch.return_value = [{"name": "George Washington", "years": "1789-1797"}]
    Main.main()
    mock_reset.assert_called_once()
    mock_create.assert_called_once()
    mock_insert.assert_called_once_with({"name": "George Washington", "years": "1789-1797"})
    mock_title.assert_called_once_with("U.S. Presidents Trivia")
    mock_button.assert_called_once_with("Learn about the Presidents")
    mock_df.assert_called_once_with(
        [{"name": "George Washington", "years": "1789-1797"}],
        use_container_width=True, height=1680
    )
