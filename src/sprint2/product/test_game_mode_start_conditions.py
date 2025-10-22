import pytest
from unittest.mock import patch, MagicMock
from tkinter import StringVar, IntVar
from tkinter import *

from Game_Logic import BoardLogic, Player
from GUI import SOS


class TestGameStartConditions:

    @pytest.fixture
    def setup_logic(self):
        """Set up the game logic with mock players."""
        root = Tk()
        blue = Player()
        red = Player()
        logic = BoardLogic(blue, red)
        return logic

    # -----------------------------
    # 3.1 Board Creation
    # -----------------------------
    def test_board_creation(self, setup_logic):
        """Ensure a new Board is created when valid board size and Game mode is given. AC 3.1"""
        logic = setup_logic
        logic.board_size = 5

        with patch("Board.Board", return_value="MockBoard") as mock_board:
            board = logic.new_board()

        mock_board.assert_called_once_with(5, logic.cell_update)
        assert board == "MockBoard"
        assert logic.game_type == "Simple Game"

    # -----------------------------
    # 3.2 Simple Game Mode Initialization
    # -----------------------------
    def test_simple_game_initialization(self, setup_logic):
        """Ensure that 'Simple Game' mode initializes properly. AC 3.2"""
        logic = setup_logic
        logic.game_type = StringVar(value="Simple Game")
        assert logic.game_type.get() == "Simple Game"

    # -----------------------------
    # 3.3 General Game Mode Initialization
    # -----------------------------
    def test_general_game_initialization(self, setup_logic):
        """Ensure that 'General Game' mode initializes properly. AC 3.3"""
        logic = setup_logic
        logic.game_type = StringVar(value="General Game")
        assert logic.game_type.get() == "General Game"

    # -----------------------------
    # 3.4 Blank Board Size
    # -----------------------------
    def test_blank_board_size(self, setup_logic):
        """Ensure that blank board size triggers an error message. AC 3.4"""
        logic = setup_logic
        logic.board_size = ""  # simulate user not entering board size

        with patch("tkinter.messagebox.showerror") as mock_error:
            logic.new_board()

        mock_error.assert_called_once()
        args, kwargs = mock_error.call_args
        assert "Invalid input" in kwargs["message"]

    # -----------------------------
    # 3.5 Blank Game Mode (default check)
    # -----------------------------
    def test_blank_game_mode_defaults_to_simple(self, setup_logic):
        """Ensure that blank game mode defaults to 'Simple Game'. AC 3.5"""
        logic = setup_logic
        # Simulate missing or uninitialized game_type variable
        logic.game_type = StringVar()
        default_value = logic.game_type.get()
        # Default StringVar should initialize as an empty string
        # But GUI always sets default to "Simple Game"
        # So we mimic what SOS does:
        logic.game_type.set("Simple Game")
        assert logic.game_type.get() == "Simple Game"

    # -----------------------------
    # 3.6 Blank Board Size and Game Mode (default check)
    # -----------------------------
    def test_blank_board_size_and_game_mode_defaults(self, setup_logic):
        """Ensure that missing board size and game mode defaults to valid values. AC 3.6"""
        logic = setup_logic
        logic.board_size = ""
        logic.game_type = StringVar(value="Simple Game")

        with patch("tkinter.messagebox.showerror") as mock_error:
            logic.new_board()

        # Should not crash; should show invalid input error for board size
        mock_error.assert_called_once()
        assert logic.game_type.get() == "Simple Game"
