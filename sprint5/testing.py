import pytest
import tkinter as tk
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