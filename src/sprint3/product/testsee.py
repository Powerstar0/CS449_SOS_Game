import pytest
from unittest.mock import Mock, patch, MagicMock
from tkinter import IntVar, StringVar, DISABLED, NORMAL
from Game_Logic import Player, SOSGameBase, SimpleSOSGame, GeneralSOSGame


class TestNewGameAcceptanceCriteria:
    """Test suite for User Story 3: Start a new game of chosen board size and game mode"""

    @pytest.fixture
    def players(self):
        """Fixture to create blue and red players"""
        blue_player = Player("Human")
        red_player = Player("Human")
        return blue_player, red_player

    @pytest.fixture
    def mock_board(self):
        """Fixture to mock the Board class"""
        with patch('Game_Logic.Board') as mock:
            mock_instance = Mock()
            mock_instance.cell_matrix = [[Mock() for _ in range(3)] for _ in range(3)]
            mock.return_value = mock_instance
            yield mock

    # AC 3.1: Board Creation
    def test_board_creation_with_valid_size(self, players, mock_board):
        """AC 3.1: Test that a board is created with valid board size (3-9)"""
        blue_player, red_player = players

        # Test board size 3
        game = SOSGameBase(blue_player, red_player, board_size=3)
        assert game.board_size == 3
        assert game.board is not None

        # Test board size 5
        game = SOSGameBase(blue_player, red_player, board_size=5)
        assert game.board_size == 5

        # Test board size 9
        game = SOSGameBase(blue_player, red_player, board_size=9)
        assert game.board_size == 9

    def test_board_creation_calls_board_constructor(self, players, mock_board):
        """AC 3.1: Verify Board constructor is called with correct parameters"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=5)

        # Verify Board was instantiated with correct size and cell_update function
        mock_board.assert_called()
        call_args = mock_board.call_args
        assert call_args[0][0] == 5  # board_size
        assert callable(call_args[0][1])  # cell_update_function

    # AC 3.2: Simple Game Mode Initialization
    def test_simple_game_mode_initialization(self, players, mock_board):
        """AC 3.2: Test that Simple Game mode initializes correctly"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=4)

        # Create SimpleSOSGame from base game
        simple_game = SimpleSOSGame(base_game, blue_player, red_player)

        # Verify game type and properties are preserved
        assert simple_game.board_size == 4
        assert simple_game.blue_player == blue_player
        assert simple_game.red_player == red_player
        assert simple_game.game_over == False
        assert simple_game.complete_sos_list == []
        assert isinstance(simple_game, SimpleSOSGame)

    def test_simple_game_win_condition_behavior(self, players, mock_board):
        """AC 3.2: Test Simple Game has correct win condition (first SOS wins)"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        simple_game = SimpleSOSGame(base_game, blue_player, red_player)

        # Initially no win condition met
        assert simple_game.win_condition() == False

        # Add an SOS to complete list
        simple_game.complete_sos_list.append([Mock(), Mock(), Mock()])

        # Mock messagebox to avoid GUI popup
        with patch('Game_Logic.messagebox.showinfo'):
            result = simple_game.win_condition()
            assert result == True
            assert simple_game.game_over == True

    # AC 3.3: General Game Mode Initialization
    def test_general_game_mode_initialization(self, players, mock_board):
        """AC 3.3: Test that General Game mode initializes correctly"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=6)

        # Create GeneralSOSGame from base game
        general_game = GeneralSOSGame(base_game, blue_player, red_player)

        # Verify game type and properties are preserved
        assert general_game.board_size == 6
        assert general_game.blue_player == blue_player
        assert general_game.red_player == red_player
        assert general_game.game_over == False
        assert general_game.complete_sos_list == []
        assert isinstance(general_game, GeneralSOSGame)

    def test_general_game_scoring_behavior(self, players, mock_board):
        """AC 3.3: Test General Game tracks scores correctly"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        general_game = GeneralSOSGame(base_game, blue_player, red_player)

        # Verify scores start at 0
        assert blue_player.score.get() == 0
        assert red_player.score.get() == 0

        # Scores should be tracked throughout the game
        blue_player.score.set(3)
        red_player.score.set(2)
        assert blue_player.score.get() == 3
        assert red_player.score.get() == 2

    # AC 3.4: Blank Board Size
    @patch('Game_Logic.messagebox.showerror')
    def test_blank_board_size_shows_error(self, mock_error, players, mock_board):
        """AC 3.4: Test that blank/invalid board size shows error message"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Set board size to None (simulating blank input)
        game.board_size = None
        game.new_board()

        # Verify error message was shown
        mock_error.assert_called_once()
        assert "Invalid input" in mock_error.call_args[1]['message']

    @patch('Game_Logic.messagebox.showerror')
    def test_invalid_board_size_type_shows_error(self, mock_error, players, mock_board):
        """AC 3.4: Test that non-numeric board size shows error"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Set board size to invalid string
        game.board_size = "abc"
        game.new_board()

        # Verify error message was shown
        mock_error.assert_called_once()
        assert "Invalid input" in mock_error.call_args[1]['message']

    @patch('Game_Logic.messagebox.showerror')
    def test_board_size_too_small_shows_error(self, mock_error, players, mock_board):
        """AC 3.4: Test that board size < 3 shows appropriate error"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Set board size to 2 (too small)
        game.board_size = 2
        game.new_board()

        # Verify error message was shown
        mock_error.assert_called_once()
        assert "greater than 2" in mock_error.call_args[1]['message']

    @patch('Game_Logic.messagebox.showerror')
    def test_board_size_too_large_shows_error(self, mock_error, players, mock_board):
        """AC 3.4: Test that board size > 9 shows appropriate error"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Set board size to 10 (too large)
        game.board_size = 10
        game.new_board()

        # Verify error message was shown
        mock_error.assert_called_once()
        assert "less than 10" in mock_error.call_args[1]['message']

    # AC 3.5: Blank Game Mode
    def test_blank_game_mode_defaults_to_simple(self, players, mock_board):
        """AC 3.5: Test that blank game mode defaults to Simple Game"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Game should default to Simple Game
        assert game.game_type == "Simple Game"

    def test_game_mode_can_be_set(self, players, mock_board):
        """AC 3.5: Test that game mode can be explicitly set"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Set to General Game
        game.set_game_type("General Game")
        assert game.game_type == "General Game"

        # Set back to Simple Game
        game.set_game_type("Simple Game")
        assert game.game_type == "Simple Game"

    # AC 3.6: Blank Board Size and Game Mode
    def test_blank_board_size_and_game_mode_uses_defaults(self, players, mock_board):
        """AC 3.6: Test that both blank board size and game mode use defaults"""
        blue_player, red_player = players

        # Create game without specifying board_size (uses default)
        game = SOSGameBase(blue_player, red_player)

        # Should default to board size 3 and Simple Game
        assert game.board_size == 3
        assert game.game_type == "Simple Game"

    @patch('Game_Logic.messagebox.showerror')
    def test_invalid_board_size_with_default_game_mode(self, mock_error, players, mock_board):
        """AC 3.6: Test invalid board size with default game mode shows error"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player)  # defaults to Simple Game

        # Try to create board with invalid size
        game.board_size = 1
        game.new_board()

        mock_error.assert_called_once()
        assert "greater than 2" in mock_error.call_args[1]['message']

    # AC 3.7: New Game when Ongoing Game
    def test_new_game_when_ongoing_game_resets_board(self, players, mock_board):
        """AC 3.7: Test that starting new game when game is ongoing creates fresh board"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Simulate ongoing game by adding some SOS sequences
        game.complete_sos_list.append([Mock(), Mock(), Mock()])
        game.turn.set("Current Turn: Red")
        blue_player.score.set(2)

        # Start new board
        old_board = game.board
        game.board_size = 4
        new_board = game.new_board()

        # Board should be recreated
        assert new_board is not None
        mock_board.assert_called()  # Board constructor called again

    def test_new_game_preserves_scores_until_reset(self, players, mock_board):
        """AC 3.7: Test that new board can be created without automatic score reset"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Set some scores
        blue_player.score.set(5)
        red_player.score.set(3)

        # Create new board (scores aren't automatically reset in new_board method)
        game.board_size = 5
        game.new_board()

        # Scores remain (would need explicit reset in calling code)
        assert blue_player.score.get() == 5
        assert red_player.score.get() == 3

    def test_new_game_when_ongoing_resets_game_state(self, players, mock_board):
        """AC 3.7: Test that new game resets game state variables"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Simulate game in progress
        game.complete_sos_list.append([Mock(), Mock(), Mock()])
        game.game_over = True
        game.turn.set("Current Turn: Red")

        # Create a new game instance (simulating "New Game" button)
        new_base = SOSGameBase(blue_player, red_player, board_size=3)
        new_game = SimpleSOSGame(new_base, blue_player, red_player)

        # New game should have fresh state
        assert new_game.complete_sos_list == []
        assert new_game.game_over == False
        assert new_game.turn.get() == "Current Turn: Blue"

    def test_new_game_with_different_size_during_ongoing_game(self, players, mock_board):
        """AC 3.7: Test starting new game with different board size during ongoing game"""
        blue_player, red_player = players
        game = SOSGameBase(blue_player, red_player, board_size=3)

        # Simulate ongoing game
        game.complete_sos_list.append([Mock(), Mock(), Mock()])

        # Change board size and create new board
        game.board_size = 7
        new_board = game.new_board()

        # New board should be created with new size
        assert new_board is not None
        assert game.board_size == 7

        # Verify Board was called with new size
        last_call_args = mock_board.call_args_list[-1]
        assert last_call_args[0][0] == 7


class TestPlayerInitialization:
    """Additional tests for Player class initialization"""

    def test_player_default_initialization(self):
        """Test player initializes with correct defaults"""
        player = Player()
        assert player.player_type == "Human"
        assert player.score.get() == 0
        assert player.symbol == 'S'

    def test_player_symbol_update(self):
        """Test player symbol can be updated"""
        player = Player()
        player.symbol_update('O')
        assert player.symbol == 'O'

        player.symbol_update('S')
        assert player.symbol == 'S'


class TestGameInitialization:
    """Tests for game initialization and setup"""

    @patch('Game_Logic.Board')
    def test_game_initializes_with_correct_defaults(self, mock_board):
        """Test game initialization sets all properties correctly"""
        blue = Player()
        red = Player()
        game = SOSGameBase(blue, red, board_size=5)

        assert game.board_size == 5
        assert game.game_type == "Simple Game"
        assert game.blue_player == blue
        assert game.red_player == red
        assert game.turn.get() == "Current Turn: Blue"
        assert game.complete_sos_list == []
        assert game.game_over == False
        assert blue.score.get() == 0
        assert red.score.get() == 0

    @patch('Game_Logic.Board')
    def test_simple_game_inherits_base_properties(self, mock_board):
        """Test SimpleSOSGame properly inherits from base game"""
        blue = Player()
        red = Player()
        base = SOSGameBase(blue, red, board_size=4)
        base.game_type = "Simple Game"

        simple = SimpleSOSGame(base, blue, red)

        assert simple.board_size == base.board_size
        assert simple.game_type == base.game_type
        assert simple.blue_player == base.blue_player
        assert simple.red_player == base.red_player

    @patch('Game_Logic.Board')
    def test_general_game_inherits_base_properties(self, mock_board):
        """Test GeneralSOSGame properly inherits from base game"""
        blue = Player()
        red = Player()
        base = SOSGameBase(blue, red, board_size=6)
        base.game_type = "General Game"

        general = GeneralSOSGame(base, blue, red)

        assert general.board_size == base.board_size
        assert general.game_type == base.game_type
        assert general.blue_player == base.blue_player
        assert general.red_player == base.red_player


class TestGameOutcomes:
    """Test suite for User Story 5: Game outcome scenarios"""

    @pytest.fixture
    def players(self):
        """Fixture to create blue and red players"""
        blue_player = Player("Human")
        red_player = Player("Human")
        return blue_player, red_player

    @pytest.fixture
    def mock_board(self):
        """Fixture to mock the Board class"""
        with patch('Game_Logic.Board') as mock:
            mock_instance = Mock()
            mock_instance.cell_matrix = [[Mock() for _ in range(3)] for _ in range(3)]
            mock.return_value = mock_instance
            yield mock

    def setup_mock_cells(self, game, symbols):
        """Helper to setup mock cells with specific symbols"""
        for i in range(game.board_size):
            for j in range(game.board_size):
                if i < len(symbols) and j < len(symbols[i]):
                    game.cell_matrix[i][j].configure_mock(**{
                        'text': symbols[i][j],
                        '__getitem__': lambda self, key: getattr(self, key)
                    })
                    game.cell_matrix[i][j].__getitem__ = lambda key, cell=game.cell_matrix[i][j]: cell.cget(
                        key) if key == 'text' else Mock()

    # AC 5.1: A win by blue/red
    @patch('Game_Logic.messagebox.showinfo')
    def test_simple_game_blue_wins(self, mock_msgbox, players, mock_board):
        """AC 5.1: Test that blue player wins in Simple Game when completing first SOS"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Set turn to blue
        game.turn.set("Current Turn: Blue")

        # Blue completes an SOS
        game.complete_sos_list.append([Mock(), Mock(), Mock()])

        # Check win condition
        result = game.win_condition()

        # Verify blue wins
        assert result == True
        assert game.game_over == True
        mock_msgbox.assert_called_once()
        assert "Blue wins" in mock_msgbox.call_args[1]['message']

    @patch('Game_Logic.messagebox.showinfo')
    def test_simple_game_red_wins(self, mock_msgbox, players, mock_board):
        """AC 5.1: Test that red player wins in Simple Game when completing first SOS"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Set turn to red
        game.turn.set("Current Turn: Red")

        # Red completes an SOS
        game.complete_sos_list.append([Mock(), Mock(), Mock()])

        # Check win condition
        result = game.win_condition()

        # Verify red wins
        assert result == True
        assert game.game_over == True
        mock_msgbox.assert_called_once()
        assert "Red wins" in mock_msgbox.call_args[1]['message']

    @patch('Game_Logic.messagebox.showinfo')
    def test_general_game_blue_wins_by_score(self, mock_msgbox, players, mock_board):
        """AC 5.1: Test that blue player wins in General Game with higher score"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = GeneralSOSGame(base_game, blue_player, red_player)

        # Setup cell matrix
        game.cell_matrix = [[Mock(state=DISABLED) for _ in range(3)] for _ in range(3)]

        # Set scores - blue has more
        blue_player.score.set(5)
        red_player.score.set(2)

        # Check win condition (all cells filled)
        result = game.win_condition()

        # Verify blue wins
        assert result == True
        mock_msgbox.assert_called_once()
        assert "Blue wins" in mock_msgbox.call_args[1]['message']

    @patch('Game_Logic.messagebox.showinfo')
    def test_general_game_red_wins_by_score(self, mock_msgbox, players, mock_board):
        """AC 5.1: Test that red player wins in General Game with higher score"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = GeneralSOSGame(base_game, blue_player, red_player)

        # Setup cell matrix
        game.cell_matrix = [[Mock(state=DISABLED) for _ in range(3)] for _ in range(3)]

        # Set scores - red has more
        blue_player.score.set(3)
        red_player.score.set(7)

        # Check win condition (all cells filled)
        result = game.win_condition()

        # Verify red wins
        assert result == True
        mock_msgbox.assert_called_once()
        assert "Red wins" in mock_msgbox.call_args[1]['message']

    # AC 5.2: A draw game
    @patch('Game_Logic.messagebox.showinfo')
    def test_simple_game_draw_no_sos(self, mock_msgbox, players, mock_board):
        """AC 5.2: Test draw in Simple Game when board is full with no SOS"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Setup fully filled board with no SOS
        game.cell_matrix = [[Mock(state=DISABLED) for _ in range(3)] for _ in range(3)]

        # No SOS sequences
        game.complete_sos_list = []

        # Check win condition
        result = game.win_condition()

        # Verify it's a tie
        assert result == True
        assert game.game_over == True
        mock_msgbox.assert_called_once()
        assert "Tie" in mock_msgbox.call_args[1]['message']

    @patch('Game_Logic.messagebox.showinfo')
    def test_general_game_draw_equal_scores(self, mock_msgbox, players, mock_board):
        """AC 5.2: Test draw in General Game when both players have equal scores"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = GeneralSOSGame(base_game, blue_player, red_player)

        # Setup fully filled board
        game.cell_matrix = [[Mock(state=DISABLED) for _ in range(3)] for _ in range(3)]

        # Set equal scores
        blue_player.score.set(4)
        red_player.score.set(4)

        # Check win condition
        result = game.win_condition()

        # Verify it's a tie
        assert result == True
        mock_msgbox.assert_called_once()
        assert "Tie" in mock_msgbox.call_args[1]['message']

    # AC 5.3: A continuing game
    def test_simple_game_continues_without_sos(self, players, mock_board):
        """AC 5.3: Test that Simple Game continues when no SOS is formed"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Setup partially filled board with some empty cells
        game.cell_matrix = [[Mock(state=NORMAL) for _ in range(3)] for _ in range(3)]
        for i in range(2):
            for j in range(2):
                game.cell_matrix[i][j].state = DISABLED

        # No SOS sequences yet
        game.complete_sos_list = []

        # Check win condition
        result = game.win_condition()

        # Game should continue
        assert result == False
        assert game.game_over == False

    def test_general_game_continues_with_empty_cells(self, players, mock_board):
        """AC 5.3: Test that General Game continues when cells remain"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=4)
        game = GeneralSOSGame(base_game, blue_player, red_player)

        # Setup partially filled board
        game.cell_matrix = [[Mock(state=NORMAL) for _ in range(4)] for _ in range(4)]
        # Fill some cells
        for i in range(2):
            for j in range(4):
                game.cell_matrix[i][j].state = DISABLED

        # Some SOS sequences completed
        blue_player.score.set(2)
        red_player.score.set(1)

        # Check win condition
        result = game.win_condition()

        # Game should continue
        assert result == False

    def test_game_continues_after_turn_switch(self, players, mock_board):
        """AC 5.3: Test that game continues and turn switches properly"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Setup game state
        game.cell_matrix = [[Mock(state=NORMAL) for _ in range(3)] for _ in range(3)]
        game.turn.set("Current Turn: Blue")

        # Simulate a move without forming SOS
        mock_cell = game.cell_matrix[0][0]
        mock_cell.cget = Mock(return_value="SystemDisabledText")
        mock_cell.config = Mock()

        blue_player.symbol = 'S'
        game.cell_update(mock_cell)

        # Verify turn switched to red (no SOS formed)
        assert game.turn.get() == "Current Turn: Red"
        assert game.game_over == False

    def test_general_game_continues_after_scoring(self, players, mock_board):
        """AC 5.3: Test that General Game continues after player scores"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=5)
        game = GeneralSOSGame(base_game, blue_player, red_player)

        # Setup partially filled board
        game.cell_matrix = [[Mock(state=NORMAL) for _ in range(5)] for _ in range(5)]
        for i in range(2):
            for j in range(5):
                game.cell_matrix[i][j].state = DISABLED

        # Blue scores some points
        blue_player.score.set(3)
        red_player.score.set(1)

        # Game should not be over
        result = game.win_condition()
        assert result == False

        # Verify game can continue
        assert game.game_over == False

    def test_filled_cells_detection_partial_board(self, players, mock_board):
        """AC 5.3: Test filled_cells correctly detects partially filled board"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Setup partially filled board
        game.cell_matrix = [[Mock() for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                if i < 2:
                    game.cell_matrix[i][j].configure_mock(**{"state": DISABLED})
                else:
                    game.cell_matrix[i][j].configure_mock(**{"state": NORMAL})

        # Should return False (not all cells filled)
        result = game.filled_cells()
        assert result == False

    def test_filled_cells_detection_full_board(self, players, mock_board):
        """AC 5.3: Test filled_cells correctly detects fully filled board"""
        blue_player, red_player = players
        base_game = SOSGameBase(blue_player, red_player, board_size=3)
        game = SimpleSOSGame(base_game, blue_player, red_player)

        # Setup fully filled board
        game.cell_matrix = [[Mock(state=DISABLED) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                game.cell_matrix[i][j].configure_mock(**{"state": DISABLED})

        # Should return True (all cells filled)
        result = game.filled_cells()
        assert result == True