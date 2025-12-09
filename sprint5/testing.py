import pytest
from unittest.mock import MagicMockk, patch
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
    