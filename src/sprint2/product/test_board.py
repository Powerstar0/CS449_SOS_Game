import pytest
from unittest.mock import patch, MagicMock
from tkinter import StringVar
from tkinter import *
from Game_Logic import BoardLogic, Player


class TestBoard:
    @pytest.fixture
    def setup_boardlogic(self):
        root = Tk()
        blue = Player()
        red = Player()
        logic = BoardLogic(blue, red)
        return logic


    def test_correct_board_size(self, setup_boardlogic):
        """ Test that a board is made with valid board size AC 1.1"""
        logic = setup_boardlogic
        logic.board_size = 5

        # Mock the Board class to avoid actually creating a GUI board
        with patch("Board.Board", return_value="MockBoard") as mock_board:
            result = logic.new_board()

        mock_board.assert_called_once_with(5, logic.cell_update)
        assert result == "MockBoard"


    def test_board_too_small(self, setup_boardlogic):
        """ Tests error response when board size is too small AC 1.2"""
        logic = setup_boardlogic
        logic.board_size = 2

        with patch("tkinter.messagebox.showerror") as mock_error:
            result = logic.new_board()

        mock_error.assert_called_once_with(title="Error", message="Board size must be greater than 2")
        assert result is None


    def test_board_too_large(self, setup_boardlogic):
        """ Tests error response when board size is too large AC 1.3"""
        logic = setup_boardlogic
        logic.board_size = 10

        with patch("tkinter.messagebox.showerror") as mock_error:
            result = logic.new_board()

        mock_error.assert_called_once_with(title="Error", message="Board size must be less than 9")
        assert result is None


    def test_board_noninteger_size_input(self, setup_boardlogic):
        """ Tests error response when board size is not an integer AC 1.4"""
        logic = setup_boardlogic
        logic.board_size = "abc"  # invalid type

        with patch("tkinter.messagebox.showerror") as mock_error:
            result = logic.new_board()

        mock_error.assert_called_once()
        args, kwargs = mock_error.call_args
        assert "Invalid input" in kwargs["message"]
        assert result is None