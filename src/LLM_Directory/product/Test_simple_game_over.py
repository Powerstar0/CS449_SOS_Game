# test_simple_game_over.py
import pytest
from unittest.mock import patch, MagicMock
from tkinter import IntVar, StringVar, Tk, DISABLED
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
    """Create a SimpleSOSGame instance with a real board for testing game over conditions"""
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


class TestSimpleGameOver:
    """Tests for simple game over conditions"""

    def test_ac_5_1_win_by_blue(self, simple_game, mock_tk_root):
        """AC 5.1: A win by blue
        Verify that blue player wins when they complete an SOS sequence
        """
        simple_game.blue_player.symbol = 'S'
        simple_game.red_player.symbol = 'O'

        # Create an SOS sequence with blue player completing it
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

            # Verify game over message shows Blue wins
            mock_msgbox.showinfo.assert_called_once()
            call_args = mock_msgbox.showinfo.call_args
            assert "Blue wins" in str(call_args) or "Blue" in str(call_args)

            # Verify game_over flag is set
            assert simple_game.game_over == True

            # Verify all buttons are disabled
            for i in range(simple_game.board_size):
                for j in range(simple_game.board_size):
                    assert simple_game.cell_matrix[i][j]['state'] == DISABLED

    def test_ac_5_1_win_by_red(self, simple_game, mock_tk_root):
        """AC 5.1: A win by red
        Verify that red player wins when they complete an SOS sequence
        """
        simple_game.blue_player.symbol = 'O'
        simple_game.red_player.symbol = 'S'

        # Create an SOS sequence with red player completing it
        with patch("Game_Logic.messagebox") as mock_msgbox:
            # Blue plays 'O' at (0,0)
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[0][0])

            # Red plays 'S' at (1,0)
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[1][0])

            # Blue plays 'O' at (0,1)
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[0][1])

            # Red plays 'S' at (2,0) - completes SOS vertically (S-O-S from positions red, blue, red)
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[2][0])

            # Verify game over message shows Red wins
            mock_msgbox.showinfo.assert_called()
            call_args = mock_msgbox.showinfo.call_args
            assert "Red wins" in str(call_args) or "Red" in str(call_args)

            # Verify game_over flag is set
            assert simple_game.game_over == True

    def test_ac_5_2_draw_game(self, simple_game, mock_tk_root):
        """AC 5.2: A draw game
        Verify that game ends in a draw when board is full with no SOS sequences
        """
        # Fill the board without creating any SOS sequences
        # Pattern that avoids SOS:
        # S O S
        # O S O
        # O S S

        with patch("Game_Logic.messagebox") as mock_msgbox:
            # Row 0
            simple_game.blue_player.symbol = 'S'
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[0][0])  # S

            simple_game.red_player.symbol = 'O'
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[0][1])  # O

            simple_game.blue_player.symbol = 'S'
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[0][2])  # S

            # Row 1
            simple_game.red_player.symbol = 'O'
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[1][0])  # O

            simple_game.blue_player.symbol = 'S'
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[1][1])  # S

            simple_game.red_player.symbol = 'O'
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[1][2])  # O

            # Row 2
            simple_game.blue_player.symbol = 'O'
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[2][0])  # O

            simple_game.red_player.symbol = 'S'
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[2][1])  # S

            simple_game.blue_player.symbol = 'S'
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[2][2])  # S (last move)

            # Verify no SOS sequences were formed
            assert len(simple_game.complete_sos_list) == 0

            # Verify game over message shows Tie
            mock_msgbox.showinfo.assert_called()
            call_args = mock_msgbox.showinfo.call_args
            assert "Tie" in str(call_args) or "Draw" in str(call_args)

            # Verify game_over flag is set
            assert simple_game.game_over == True

            # Verify all cells are filled
            for i in range(simple_game.board_size):
                for j in range(simple_game.board_size):
                    assert simple_game.cell_matrix[i][j]['text'] in ['S', 'O']
                    assert simple_game.cell_matrix[i][j]['state'] == DISABLED

    def test_ac_5_3_continuing_game(self, simple_game, mock_tk_root):
        """AC 5.3: A continuing game
        Verify that game continues when moves are made but no win/draw condition is met
        """
        simple_game.blue_player.symbol = 'S'
        simple_game.red_player.symbol = 'O'

        with patch("Game_Logic.messagebox") as mock_msgbox:
            # Make a few moves that don't complete SOS or fill the board

            # Blue plays 'S' at (0,0)
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[0][0])

            # Verify game is not over
            assert simple_game.game_over == False

            # Verify no game over message
            mock_msgbox.showinfo.assert_not_called()

            # Red plays 'O' at (1,1)
            simple_game.turn.set("Current Turn: Red")
            simple_game.cell_update(simple_game.cell_matrix[1][1])

            # Verify game is still not over
            assert simple_game.game_over == False

            # Blue plays 'S' at (2,2)
            simple_game.turn.set("Current Turn: Blue")
            simple_game.cell_update(simple_game.cell_matrix[2][2])

            # Verify game continues
            assert simple_game.game_over == False

            # Verify no SOS sequences formed
            assert len(simple_game.complete_sos_list) == 0

            # Verify board is not full (empty cells still exist)
            empty_cells = 0
            for i in range(simple_game.board_size):
                for j in range(simple_game.board_size):
                    if simple_game.cell_matrix[i][j]['text'] == '':
                        empty_cells += 1
            assert empty_cells > 0

            # Verify turns are still alternating
            assert simple_game.turn.get() == "Current Turn: Red"

            # Verify no game over message was shown
            mock_msgbox.showinfo.assert_not_called()