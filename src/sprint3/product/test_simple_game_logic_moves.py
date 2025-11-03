import pytest
from tkinter import Tk, Button, DISABLED, NORMAL
from GUI import Player, SOSGameBase  # Adjust import path as needed

class TestSimpleMoves:
    @pytest.fixture
    def board_logic(self):
        """Fixture to create a SOSGameBase instance with mock players."""
        root = Tk()
        root.withdraw()  # Prevent GUI from popping up
        blue = Player()
        red = Player()
        logic = SOSGameBase(blue, red)
        return logic


    def test_ac41_valid_move_placement(self, board_logic):
        """AC 4.1: Valid move placement (S or O) is displayed and disables the cell. AC 4.1"""
        # Blue starts
        board_logic.blue_player.symbol = "S"
        board_logic.turn.set("Current Turn: Blue")

        cell = Button(text="", state=NORMAL)
        board_logic.cell_update(cell)

        # Check if the cell now shows 'S' and is disabled
        assert cell.cget("text") == "S", "Cell should show Blue's symbol 'S'"
        assert cell.cget("state") == DISABLED, "Cell should be disabled after placement"
        assert board_logic.turn.get() == "Current Turn: Red", "Turn should pass to Red after Blue's move"

        # Now test Red's turn
        board_logic.red_player.symbol = "O"
        next_cell = Button(text="", state=NORMAL)
        board_logic.cell_update(next_cell)

        assert next_cell.cget("text") == "O", "Cell should show Red's symbol 'O'"
        assert next_cell.cget("state") == DISABLED, "Cell should be disabled after placement"
        assert board_logic.turn.get() == "Current Turn: Blue", "Turn should pass back to Blue after Red's move"


    def test_ac42_prevent_overwriting(self, board_logic):
        """AC 4.2: Once a cell is occupied, it cannot be overwritten. AC 4.2"""
        board_logic.blue_player.symbol = "S"
        board_logic.turn.set("Current Turn: Blue")

        # Create a button and make Blue play on it
        cell = Button(text="", state=NORMAL)
        board_logic.cell_update(cell)

        # Try calling again — since the button is DISABLED, nothing should change
        old_text = cell.cget("text")
        board_logic.cell_update(cell)

        assert cell.cget("text") == old_text, "Occupied cell should not be overwritten"
        assert cell.cget("state") == DISABLED, "Cell should remain disabled"


    def test_ac44_turn_passing(self, board_logic):
        """AC 4.4: Turn alternates after every valid move. AC 4.4"""
        board_logic.blue_player.symbol = "S"
        board_logic.red_player.symbol = "O"
        board_logic.turn.set("Current Turn: Blue")

        # Blue moves
        first_cell = Button(text="", state=NORMAL)
        board_logic.cell_update(first_cell)
        assert board_logic.turn.get() == "Current Turn: Red", "Turn should pass to Red"

        # Red moves
        second_cell = Button(text="", state=NORMAL)
        board_logic.cell_update(second_cell)
        assert board_logic.turn.get() == "Current Turn: Blue", "Turn should pass back to Blue"
