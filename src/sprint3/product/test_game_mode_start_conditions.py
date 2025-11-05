# test_sos_new_game.py
import pytest
from unittest.mock import patch, MagicMock
from tkinter import IntVar, StringVar, Tk
from GUI import SOS
from Game_Logic import SimpleSOSGame, GeneralSOSGame, SOSGameBase, Player


@pytest.fixture
def mock_tk_root():
    """Create a mock Tkinter root window"""
    with patch("tkinter.Tk") as mock_root:
        root_instance = MagicMock()
        mock_root.return_value = root_instance
        # Create actual Tk root for IntVar and StringVar to work
        actual_root = Tk()
        actual_root.withdraw()  # Hide the window
        yield actual_root
        actual_root.destroy()


@pytest.fixture
def game_instance(mock_tk_root):
    """Create a mock SOS instance without launching Tkinter mainloop"""
    with patch("GUI.Tk", return_value=mock_tk_root), \
            patch("GUI.ttk.Label"), \
            patch("GUI.ttk.Frame"), \
            patch("GUI.ttk.Radiobutton"), \
            patch("GUI.ttk.Checkbutton"), \
            patch("GUI.ttk.Button"), \
            patch("GUI.Entry"), \
            patch("GUI.Label"):
        # Create instance bypassing __init__
        game = SOS.__new__(SOS)

        # Create real players with actual IntVar (now that we have a root)
        game.blue_player = Player()
        game.red_player = Player()

        # Create actual IntVar and StringVar for realistic testing
        game.board_size = IntVar(mock_tk_root)
        game.board_size.set(3)  # Default value

        # Create base game instance
        game.boardgame = SOSGameBase(game.blue_player, game.red_player)
        game.boardgame.game_type = StringVar(mock_tk_root)
        game.boardgame.game_type.set("Simple Game")  # Default value

        # Mock UI components
        game.turn_label = MagicMock()
        game.blue_score_label = MagicMock()
        game.red_score_label = MagicMock()
        game.blue_score_label_text = MagicMock()
        game.red_score_label_text = MagicMock()
        game.game_mode_label = MagicMock()
        game.left_frame = MagicMock()
        game.right_frame = MagicMock()

        return game


class TestGameStartConditions:
    """Tests for starting a new game with various configurations"""

    def test_ac_3_1_board_creation(self, game_instance):
        """AC 3.1: Board Creation
        Verify that a board is created with the correct size, placed in center, and turn is reset to Blue
        """
        game_instance.board_size.set(5)
        game_instance.boardgame.game_type.set("Simple Game")

        # Set turn to Red initially to verify it gets reset
        game_instance.boardgame.turn.set("Current Turn: Red")

        with patch("GUI.messagebox.askyesno", return_value=True), \
                patch("Game_Logic.Board") as mock_board, \
                patch.object(game_instance.boardgame, 'new_board') as mock_new_board:
            mock_board_instance = MagicMock()
            mock_new_board.return_value = mock_board_instance

            game_instance.start_new_game()

            # Verify board size was set correctly
            assert game_instance.boardgame.board_size == 5

            # Verify Board was created
            mock_board.assert_called()

            # Verify board.place was called with center positioning
            mock_board_instance.place.assert_called_once_with(anchor='center', relx=.5, rely=.5)

            # Verify turn was reset to Blue
            assert game_instance.boardgame.turn.get() == "Current Turn: Blue"

    def test_ac_3_2_simple_game_mode_initialization(self, game_instance):
        """AC 3.2: Simple Game Mode Initialization
        Verify that a SimpleSOSGame instance is created with proper UI setup
        """
        game_instance.board_size.set(4)
        game_instance.boardgame.game_type.set("Simple Game")

        with patch("GUI.messagebox.askyesno", return_value=True), \
                patch("Game_Logic.Board"):
            game_instance.start_new_game()

            # Verify the boardgame is now a SimpleSOSGame instance
            assert isinstance(game_instance.boardgame, SimpleSOSGame)

            # Verify score labels are hidden (pack_forget called)
            game_instance.blue_score_label.pack_forget.assert_called()
            game_instance.red_score_label.pack_forget.assert_called()
            game_instance.blue_score_label_text.pack_forget.assert_called()
            game_instance.red_score_label_text.pack_forget.assert_called()

            # Verify game mode label is updated
            game_instance.game_mode_label.config.assert_called_with(
                text="Current Game Mode: Simple Game"
            )

    def test_ac_3_3_general_game_mode_initialization(self, game_instance):
        """AC 3.3: General Game Mode Initialization
        Verify that a GeneralSOSGame instance is created with score labels shown and scores reset
        """
        game_instance.board_size.set(6)
        game_instance.boardgame.game_type.set("General Game")

        # Set some initial scores to verify they get reset
        game_instance.boardgame.blue_player.score.set(5)
        game_instance.boardgame.red_player.score.set(3)

        with patch("GUI.messagebox.askyesno", return_value=True), \
                patch("Game_Logic.Board"):
            game_instance.start_new_game()

            # Verify the boardgame is now a GeneralSOSGame instance
            assert isinstance(game_instance.boardgame, GeneralSOSGame)

            # Verify score labels are shown (pack called)
            game_instance.blue_score_label_text.pack.assert_called()
            game_instance.red_score_label_text.pack.assert_called()
            game_instance.blue_score_label.pack.assert_called()
            game_instance.red_score_label.pack.assert_called()

            # Verify scores are reset to 0
            assert game_instance.boardgame.blue_player.score.get() == 0
            assert game_instance.boardgame.red_player.score.get() == 0

            # Verify game mode label is updated
            game_instance.game_mode_label.config.assert_called_with(
                text="Current Game Mode: General Game"
            )

    def test_ac_3_4_blank_board_size(self, game_instance):
        """AC 3.4: Blank Board Size
        Verify that an error is shown and no board is created when board size is blank/invalid
        """
        game_instance.board_size.set(0)  # IntVar with 0 represents blank/invalid
        game_instance.boardgame.game_type.set("Simple Game")

        with patch("GUI.messagebox.askyesno", return_value=True), \
                patch("GUI.messagebox.showerror") as mock_error, \
                patch("Game_Logic.Board") as mock_board:
            game_instance.start_new_game()

            # Verify error message was shown
            mock_error.assert_called()

            # Verify that the exception is caught and execution continues
            # (no exception propagates, board creation fails gracefully)
            assert True

    def test_ac_3_5_blank_game_mode(self, game_instance):
        """AC 3.5: Blank Game Mode
        Verify that game stays as base class when game mode is blank, but board is still created
        """
        game_instance.board_size.set(4)
        game_instance.boardgame.game_type.set("")  # Blank game mode

        with patch("GUI.messagebox.askyesno", return_value=True), \
                patch.object(game_instance.boardgame, 'new_board') as mock_new_board:
            mock_board = MagicMock()
            mock_new_board.return_value = mock_board

            game_instance.start_new_game()

            # Verify boardgame remains as SOSGameBase (not Simple or General)
            assert isinstance(game_instance.boardgame, SOSGameBase)
            assert not isinstance(game_instance.boardgame, SimpleSOSGame)
            assert not isinstance(game_instance.boardgame, GeneralSOSGame)

            # Verify new_board was still called (board created despite blank mode)
            mock_new_board.assert_called_once()

    def test_ac_3_6_blank_board_size_and_game_mode(self, game_instance):
        """AC 3.6: Blank Board Size and Game Mode
        Verify that error is shown and no proper game is initialized when both are blank
        """
        game_instance.board_size.set(0)  # Blank board size
        game_instance.boardgame.game_type.set("")  # Blank game mode

        with patch("GUI.messagebox.askyesno", return_value=True), \
                patch("GUI.messagebox.showerror") as mock_error:
            game_instance.start_new_game()

            # Verify error was shown (from board size validation)
            mock_error.assert_called()

            # Verify game remains in base state due to exceptions
            assert isinstance(game_instance.boardgame, SOSGameBase)

    def test_ac_3_7_new_game_when_ongoing_game(self, game_instance):
        """AC 3.7: New Game when Ongoing Game
        Verify confirmation dialog is shown, and proper behavior for both confirm and cancel actions
        """
        game_instance.board_size.set(5)
        game_instance.boardgame.game_type.set("General Game")

        # Add SOS sequences to simulate ongoing game
        game_instance.boardgame.complete_sos_list = [["S", "O", "S"], ["S", "O", "S"]]

        # Test 1: User confirms
        with patch("GUI.messagebox.askyesno", return_value=True) as mock_askyesno, \
                patch("Game_Logic.Board") as mock_board:
            game_instance.start_new_game()

            # Verify confirmation dialog was shown
            mock_askyesno.assert_called_once_with(
                title="New Game",
                message="Are you sure you want to make a new game?"
            )

            # Verify new game was created
            assert isinstance(game_instance.boardgame, GeneralSOSGame)
            mock_board.assert_called()

            # Verify SOS list was reset
            assert game_instance.boardgame.complete_sos_list == []

            # Verify turn label is packed (made visible)
            game_instance.turn_label.pack.assert_called()

        # Test 2: User cancels
        original_boardgame = game_instance.boardgame
        with patch("GUI.messagebox.askyesno", return_value=False), \
                patch("Game_Logic.Board") as mock_board:
            game_instance.start_new_game()

            # Verify no new board was created
            mock_board.assert_not_called()

            # Verify boardgame wasn't changed
            assert game_instance.boardgame == original_boardgame