import pytest
import tkinter as tk
import json
from unittest.mock import MagicMock, patch
from gui_file import SOSGame 

@pytest.fixture
def mock_game_setup():
    """Creates a mock tkinter interface and dialog components for testing SOS Game initialization"""
    with patch('tkinter.tk') as MockTK, \
        patch('tkinter.messagebox') as MockMessageBox, \
        patch('tkinter.filedialog') as MockFileDialog, \
        patch('gui_file.SimpleMode', autospec=True) as MockSimpleMode, \
        patch('gui_file.GeneralMode') as MockGeneralMode:

        # Make a mock tk instance that are called for initialization
        mock_root = MockTK.return_value
        mock_root.winfo_children.return_value =[] 

        game_app = SOSGame()

        # stick mocks to the fixture for better access
        game_app.MOCKTK = MockTK
        game_app.MockMessageBox = MockMessageBox
        game_app.MockFileDialog = MockFileDialog
        game_app.MockSimpleMode = MockSimpleMode
        game_app.MockGeneralMode = MockGeneralMode
        
        yield game_app

@pytest.fixture
def mock_active_game(mock_game_setup):
    """Sets up the mock SOS game with an active game state"""

    game_app = mock_game_setup

    # Game object for Simple mode with a board size of 3
    mock_game = MagicMock()
    mock_game.board.board_size = 3
    mock_game.game_mode = "Simple Game"
    mock_game.move_history = [
        (0, 0, "S", "Blue"),
        (1, 1, "O", "Red"),
        (0, 1, "S", "Blue")
    ]

    # create a SOS game instance 
    game_app.game = mock_game

    # make a mock game window 
    game_app.game_window = MagicMock(spec=tk.Tk)
    game_app.turn_label = MagicMock(spec=tk.Label)
    game_app.board_buttons = [[MagicMock(spec=tk.Button) for _ in range(3)] for _ in range(3)]

    return game_app

def text_record_saves_correct_data(mock_active_game):
    """Makes sure that the record_game writes out the right game state data to the file"""

    game_app = mock_active_game

    # Mock the file dialog save
    DUMMY_PATH = "/tmp/text_game.txt"
    game_app.MockFileDialog.asksaveasfilename.return_value = DUMMY_PATH

    # check if the data is written in file 
    with patch("builtins.open", new_call=MagicMock) as mock_open:
        mock_file = mock_open.return_value.__enter___.return_value
        
        game_app.record_game()

        # check if file dialog was called
        game_app.MockFileDialog.asksaveasfilename.assert_called_once()
        
        # check open was called with the right dummy path and mode 
        mock_open.assert_called_with(DUMMY_PATH, 'w')

        # check if the json.dump was called with the right data 
        expected_data = {
            "board_size": 3,
            "game_mode": "Simple Game",
            "move_history": [(0, 0, 'S', 'Blue'), (1, 1, 'O', 'Red'), (0, 1, 'S', 'Blue')]
        }

        # load the data for comparisons 
        written_data = "".join(call.args[0] for call in mock_file.write.call_args_list)
        written_dict = json.loads(written_data)
        
        assert written_dict["board_size"] == expected_data["board_size"]
        assert written_dict["game_mode"] == expected_data["game_mode"]
        assert written_dict["move_history"] == expected_data["move_history"]