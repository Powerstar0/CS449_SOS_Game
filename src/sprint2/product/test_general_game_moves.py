import pytest
import tkinter as tk
from Game_Logic import BoardLogic, Player  # Adjust import if needed


@pytest.fixture
def general_game_logic():
    """Fixture to create a headless general game instance."""
    root = tk.Tk()
    root.withdraw()  # Prevent GUI from showing
    blue = Player()
    red = Player()
    logic = BoardLogic(blue, red)
    return logic


class TestGeneralGameMoves:
    """Unit tests for General SOS Game move logic without GUI popping up."""

    def test_6_1_valid_move_placement(self, general_game_logic):
        """6.1: Valid move placement for Blue and Red should display symbol and disable button."""
        logic = general_game_logic

        # Blue's turn
        logic.blue_player.symbol = "S"
        logic.turn.set("Current Turn: Blue")
        cell_blue = tk.Button(text="", state=tk.NORMAL)
        logic.cell_update(cell_blue)

        assert cell_blue.cget("text") == "S", "Blue's symbol should appear on the board."
        assert cell_blue.cget("state") == tk.DISABLED, "Button should be disabled after move."
        assert logic.turn.get() == "Current Turn: Red", "Turn should pass to Red."

        # Red's turn
        logic.red_player.symbol = "O"
        cell_red = tk.Button(text="", state=tk.NORMAL)
        logic.cell_update(cell_red)

        assert cell_red.cget("text") == "O", "Red's symbol should appear on the board."
        assert cell_red.cget("state") == tk.DISABLED, "Button should be disabled after move."
        assert logic.turn.get() == "Current Turn: Blue", "Turn should pass back to Blue."

    def test_6_2_invalid_move_on_occupied_square(self, general_game_logic):
        """6.2: Occupied squares cannot be overwritten."""
        logic = general_game_logic

        # Blue moves first
        logic.blue_player.symbol = "S"
        logic.turn.set("Current Turn: Blue")
        cell = tk.Button(text="", state=tk.NORMAL)
        logic.cell_update(cell)
        prev_text = cell.cget("text")

        # Attempt to overwrite the same cell
        try:
            logic.cell_update(cell)
        except Exception as e:
            pytest.fail(f"cell_update() raised exception on occupied cell: {e}")

        assert cell.cget("text") == prev_text, "Occupied cell should not be overwritten."
        assert cell.cget("state") == tk.DISABLED, "Occupied cell must remain disabled."

    def test_6_6_turn_passing(self, general_game_logic):
        """6.6: Turn alternates after each valid move."""
        logic = general_game_logic
        logic.blue_player.symbol = "S"
        logic.red_player.symbol = "O"

        # Blue's move
        logic.turn.set("Current Turn: Blue")
        cell1 = tk.Button(text="", state=tk.NORMAL)
        logic.cell_update(cell1)
        assert logic.turn.get() == "Current Turn: Red", "After Blue's move, it should be Red's turn."

        # Red's move
        cell2 = tk.Button(text="", state=tk.NORMAL)
        logic.cell_update(cell2)
        assert logic.turn.get() == "Current Turn: Blue", "After Red's move, it should be Blue's turn again."
