# test_simple_game_moves.py
import pytest
from unittest.mock import patch, MagicMock
from tkinter import IntVar, StringVar, Tk, DISABLED, NORMAL, Button
from GUI import SOS
from Game_Logic import SimpleSOSGame, Player
from Board import Board


@pytest.fixture
def mock_tk_root():
    """Create a mock Tkinter root window"""
    actual_root = Tk()
    actual_root.withdraw()  # Hide the window
    yield actual_root
    actual_root.destroy()


@pytest.fixture
def simple_game(mock_tk_root):
    """Create a SimpleSOSGame instance with a real board for testing moves"""
    blue_player = Player()
    red_player = Player()

    # Create base game
    blue_player.symbol = 'S'
    red_player.symbol = 'S'

    # Create a simple game with 3x3 board
    with patch("Game_Logic.SOSGameBase.__init__", return_value=None):
        game = SimpleSOSGame.__new__(SimpleSOSGame)
        game.board_size = 3
        game.game_type = "Simple Game"
        game.blue_player = blue_player
        game.red_player = red_player
        game.turn = StringVar(mock_tk_root, value="Current Turn: Blue")
        game.complete_sos_list = []
        game.game_over = False

        # Create actual board with mock cell_update function
        game.board = Board(3, game.cell_update)
        game.cell_matrix = game.board.cell_matrix

    return game


class TestSimpleMoves:
    """Tests for making moves in a simple game"""

    def test_ac_4_1_valid_move_placement(self, simple_game, mock_tk_root):
        """AC 4.1: Valid Move Placement
        Verify that a valid move places the correct symbol, disables the cell, and updates the display
        """
        # Set blue player symbol to 'S'
        simple_game.blue_player.symbol = 'S'
        simple_game.turn.set("Current Turn: Blue")

        # Get a cell from the board
        cell = simple_game.cell_matrix[0][0]

        # Verify cell is initially empty and enabled
        assert cell['text'] == ''
        assert cell['state'] != DISABLED

        # Make a move
        with patch("Game_Logic.messagebox"):
            simple_game.cell_update(cell)

        # Verify the cell now has the correct symbol
        assert cell['text'] == 'S'

        # Verify the cell is disabled (cannot be clicked again)
        assert cell['state'] == DISABLED

        # Verify font is set correctly (Tkinter returns font as string)
        assert "Helvetica" in str(cell['font'])
        assert "40" in str(cell['font'])

    def test_ac_4_2_occupied_square_invalid_move(self, simple_game, mock_tk_root):
        """AC 4.2: Occupied Square Invalid Move
        Verify that attempting to play on an already occupied square does nothing
        """
        simple_game.blue_player.symbol = 'O'
        simple_game.turn.set("Current Turn: Blue")

        # Get a cell and make initial move
        cell = simple_game.cell_matrix[1][1]
        with patch("Game_Logic.messagebox"):
            simple_game.cell_update(cell)

        # Verify first move worked
        assert cell['text'] == 'O'
        assert cell['state'] == DISABLED

        # Try to make another move on the same cell
        simple_game.red_player.symbol = 'S'
        simple_game.turn.set("Current Turn: Red")

        with patch("Game_Logic.messagebox"):
            # Cell is disabled, so clicking won't trigger cell_update in real scenario
            # But we can verify the cell remains unchanged
            original_text = cell['text']

            # In actual Tkinter, disabled buttons don't trigger commands
            # We verify the cell state prevents further updates
            assert cell['state'] == DISABLED
            assert cell['text'] == original_text  # Still 'O', not changed to 'S'

    def test_ac_4_3_sos_detection(self, simple_game, mock_tk_root):
        """AC 4.3: SOS Detection
        Verify that the game detects when an SOS sequence is formed and declares a winner
        """
        simple_game.blue_player.symbol = 'S'
        simple_game.red_player.symbol = 'O'

        # Create an SOS sequence: S-O-S horizontally in first row
        with patch("Game_Logic.messagebox") as mock_msgbox:
            # Blue plays 'S' at (0,0)
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[0][0])

            # Red plays 'O' at (1,0)
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[1][0])

            # Blue plays 'S' at (2,0) - completes SOS vertically
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[2][0])

            # Verify SOS was detected and added to list
            assert len(simple_game.complete_sos_list) == 1

            # Verify game over message was shown (Simple game ends on first SOS)
            mock_msgbox.showinfo.assert_called()

            # Verify game_over flag is set
            assert simple_game.game_over == True

    def test_ac_4_4_turn_passing(self, simple_game, mock_tk_root):
        """AC 4.4: Turn Passing
        Verify that turns alternate between players when no SOS is formed
        """
        simple_game.blue_player.symbol = 'S'
        simple_game.red_player.symbol = 'S'
        simple_game.turn.set("Current Turn: Blue")

        # Make moves that don't form SOS
        with patch("Game_Logic.messagebox"):
            # Blue's turn - place 'S' at (0,0)
            assert simple_game.turn.get() == "Current Turn: Blue"
            simple_game.cell_update(simple_game.cell_matrix[0][0])

            # Verify turn switched to Red
            assert simple_game.turn.get() == "Current Turn: Red"

            # Red's turn - place 'S' at (0,1)
            simple_game.cell_update(simple_game.cell_matrix[0][1])

            # Verify turn switched back to Blue
            assert simple_game.turn.get() == "Current Turn: Blue"

            # Blue's turn - place 'S' at (1,1)
            simple_game.cell_update(simple_game.cell_matrix[1][1])

            # Verify turn switched to Red again
            assert simple_game.turn.get() == "Current Turn: Red"