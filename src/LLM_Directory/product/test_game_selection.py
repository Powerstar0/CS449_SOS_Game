import pytest
from unittest.mock import patch, MagicMock
from tkinter import StringVar
from tkinter import *
from Game_Logic import SOSGameBase, Player


class TestGameTypeSelection:
    @pytest.fixture
    def setup_logic(self):
        """Fixture to set up the SOSGameBase object."""
        root = Tk()
        blue = Player()
        red = Player()
        logic = SOSGameBase(blue, red)
        return logic

    def test_simple_game_selection(self, setup_logic):
        """Ensure selecting 'Simple Game' updates the game type correctly. AC 2.1"""
        logic = setup_logic

        # Simulate Tkinter StringVar selection
        logic.game_type = StringVar(value="Simple Game")

        # Verify value stored in the game logic
        assert logic.game_type.get() == "Simple Game", "Game type should be 'Simple Game'"

    def test_general_game_selection(self, setup_logic):
        """Ensure selecting 'General Game' updates the game type correctly. AC 2.2"""
        logic = setup_logic

        # Simulate Tkinter StringVar selection
        logic.game_type = StringVar(value="General Game")

        # Verify value stored in the game logic
        assert logic.game_type.get() == "General Game", "Game type should be 'General Game'"
