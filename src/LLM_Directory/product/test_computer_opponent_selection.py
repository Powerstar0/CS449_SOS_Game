import pytest
from unittest.mock import Mock, patch, MagicMock
from tkinter import Tk, StringVar, IntVar
from Game_Logic import Player, ComputerPlayer, SOSGameBase, SimpleSOSGame, GeneralSOSGame
from GUI import SOS


@pytest.fixture(scope="function")
def tk_root():
    """Create a Tkinter root window for tests that need it"""
    root = Tk()
    yield root
    try:
        root.destroy()
    except:
        pass


class TestAC81_ComputerOpponentSelection:
    """
    AC 8.1 Computer Opponent Selection
    Given the user wants to change the player type
    When the user selects the computer opponent radio button
    Then the GUI must show that a computer opponent is selected
    And the human player button is deselected
    And the player type is set to computer opponent
    """

    def test_blue_player_computer_selection_updates_player_type(self, tk_root):
        """Test that selecting computer opponent updates blue player type"""
        # Arrange
        player = Player()
        assert player.player_type == "Human"

        # Act
        player.player_update("Computer")

        # Assert
        assert player.player_type == "Computer"

    def test_red_player_computer_selection_updates_player_type(self, tk_root):
        """Test that selecting computer opponent updates red player type"""
        # Arrange
        player = Player()
        assert player.player_type == "Human"

        # Act
        player.player_update("Computer")

        # Assert
        assert player.player_type == "Computer"

    def test_human_player_button_deselected_when_computer_selected(self, tk_root):
        """Test that human selection is overridden when computer is selected"""
        # Arrange
        player = Player()
        player.player_update("Human")
        assert player.player_type == "Human"

        # Act
        player.player_update("Computer")

        # Assert
        assert player.player_type == "Computer"
        assert player.player_type != "Human"

    def test_computer_player_type_persists(self, tk_root):
        """Test that computer player type persists after selection"""
        # Arrange
        player = Player()

        # Act
        player.player_update("Computer")

        # Assert
        assert player.player_type == "Computer"

        # Verify it stays computer even after multiple checks
        assert player.player_type == "Computer"
        assert player.player_type == "Computer"

    def test_player_type_toggle_between_human_and_computer(self, tk_root):
        """Test toggling between human and computer player types"""
        # Arrange
        player = Player()

        # Act & Assert - Start as Human
        assert player.player_type == "Human"

        # Switch to Computer
        player.player_update("Computer")
        assert player.player_type == "Computer"

        # Switch back to Human
        player.player_update("Human")
        assert player.player_type == "Human"

        # Switch to Computer again
        player.player_update("Computer")
        assert player.player_type == "Computer"

    def test_both_players_can_be_computer(self, tk_root):
        """Test that both blue and red players can be set to computer"""
        # Arrange
        blue_player = Player()
        red_player = Player()

        # Act
        blue_player.player_update("Computer")
        red_player.player_update("Computer")

        # Assert
        assert blue_player.player_type == "Computer"
        assert red_player.player_type == "Computer"

    def test_one_human_one_computer_configuration(self, tk_root):
        """Test mixed configuration of human and computer players"""
        # Arrange
        blue_player = Player()
        red_player = Player()

        # Act
        blue_player.player_update("Human")
        red_player.player_update("Computer")

        # Assert
        assert blue_player.player_type == "Human"
        assert red_player.player_type == "Computer"


class TestAC82_GameInitializationWithComputerOpponents:
    """
    AC 8.2 Game initialization with computer opponent(s)
    Given the user selects the "new game" button
    When a valid board size is selected
    And a valid game mode is selected
    And one or two computer players are selected
    Then the game should start successfully
    """

    @pytest.fixture
    def blue_player(self, tk_root):
        """Create a blue player"""
        return Player()

    @pytest.fixture
    def red_player(self, tk_root):
        """Create a red player"""
        return Player()

    def test_game_starts_with_valid_board_simple_game_one_computer(self, blue_player, red_player):
        """Test game starts with valid board size, simple game, and one computer player"""
        # Arrange
        board_size = 5
        blue_player.player_update("Human")
        red_player.player_update("Computer")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        game.set_game_type("Simple Game")
        simple_game = SimpleSOSGame(game, blue_player, red_player)
        red_player = ComputerPlayer(red_player)
        board = simple_game.new_board()

        # Assert
        assert simple_game.board_size == 5
        assert simple_game.game_type == "Simple Game"
        assert simple_game.blue_player.player_type == "Human"
        assert red_player.player_type == "Computer"
        assert board is not None
        assert simple_game.cell_matrix is not None

    def test_game_starts_with_valid_board_general_game_one_computer(self, blue_player, red_player):
        """Test game starts with valid board size, general game, and one computer player"""
        # Arrange
        board_size = 6
        blue_player.player_update("Computer")
        red_player.player_update("Human")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        game.set_game_type("General Game")
        general_game = GeneralSOSGame(game, blue_player, red_player)
        blue_player = ComputerPlayer(blue_player)
        board = general_game.new_board()

        # Assert
        assert general_game.board_size == 6
        assert general_game.game_type == "General Game"
        assert blue_player.player_type == "Computer"
        assert general_game.red_player.player_type == "Human"
        assert board is not None
        assert general_game.cell_matrix is not None

    def test_game_starts_with_two_computer_players_simple_game(self, blue_player, red_player):
        """Test game starts with two computer players in simple game"""
        # Arrange
        board_size = 4
        blue_player.player_update("Computer")
        red_player.player_update("Computer")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        game.set_game_type("Simple Game")
        simple_game = SimpleSOSGame(game, blue_player, red_player)
        blue_computer = ComputerPlayer(blue_player)
        red_computer = ComputerPlayer(red_player)
        board = simple_game.new_board()

        # Assert
        assert simple_game.board_size == 4
        assert simple_game.game_type == "Simple Game"
        assert blue_computer.player_type == "Computer"
        assert red_computer.player_type == "Computer"
        assert board is not None
        assert simple_game.cell_matrix is not None

    def test_game_starts_with_two_computer_players_general_game(self, blue_player, red_player):
        """Test game starts with two computer players in general game"""
        # Arrange
        board_size = 7
        blue_player.player_update("Computer")
        red_player.player_update("Computer")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        game.set_game_type("General Game")
        general_game = GeneralSOSGame(game, blue_player, red_player)
        blue_computer = ComputerPlayer(blue_player)
        red_computer = ComputerPlayer(red_player)
        board = general_game.new_board()

        # Assert
        assert general_game.board_size == 7
        assert general_game.game_type == "General Game"
        assert blue_computer.player_type == "Computer"
        assert red_computer.player_type == "Computer"
        assert board is not None
        assert general_game.cell_matrix is not None

    @pytest.mark.parametrize("board_size,game_type", [
        (3, "Simple Game"),
        (4, "Simple Game"),
        (5, "Simple Game"),
        (6, "General Game"),
        (7, "General Game"),
        (8, "General Game"),
        (9, "General Game"),
    ])
    def test_game_starts_with_various_valid_configurations(self, tk_root, board_size, game_type):
        """Test game starts successfully with various valid board sizes and game types"""
        # Arrange
        blue_player = Player()
        red_player = Player()
        blue_player.player_update("Computer")
        red_player.player_update("Human")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        game.set_game_type(game_type)

        if game_type == "Simple Game":
            game_instance = SimpleSOSGame(game, blue_player, red_player)
        else:
            game_instance = GeneralSOSGame(game, blue_player, red_player)

        blue_computer = ComputerPlayer(blue_player)
        board = game_instance.new_board()

        # Assert
        assert game_instance.board_size == board_size
        assert game_instance.game_type == game_type
        assert blue_computer.player_type == "Computer"
        assert board is not None
        assert game_instance.cell_matrix is not None
        assert len(game_instance.cell_matrix) == board_size
        assert len(game_instance.cell_matrix[0]) == board_size

    def test_game_initialization_sets_correct_initial_state(self, blue_player, red_player):
        """Test that game initialization sets correct initial state with computer players"""
        # Arrange
        board_size = 5
        blue_player.player_update("Computer")
        red_player.player_update("Computer")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        blue_computer = ComputerPlayer(blue_player)
        red_computer = ComputerPlayer(red_player)
        board = game.new_board()

        # Assert
        assert game.board_size == 5
        assert blue_computer.player_type == "Computer"
        assert red_computer.player_type == "Computer"
        assert game.turn.get() == "Current Turn: Blue"
        assert blue_computer.score.get() == 0
        assert red_computer.score.get() == 0
        assert game.complete_sos_list == []
        assert game.game_over == False

    def test_computer_player_inherits_from_base_player(self, blue_player):
        """Test that ComputerPlayer properly inherits from Player"""
        # Arrange
        blue_player.player_update("Computer")
        blue_player.symbol_update("O")

        # Act
        computer_player = ComputerPlayer(blue_player)

        # Assert
        assert computer_player.player_type == "Computer"
        assert computer_player.symbol == "O"
        assert hasattr(computer_player, 'score')
        assert hasattr(computer_player, 'symbol_update')
        assert hasattr(computer_player, 'player_update')

    @patch('tkinter.messagebox.showerror')
    def test_game_does_not_start_with_invalid_board_size_too_small(self, mock_error, blue_player, red_player):
        """Test that game shows error with board size < 3"""
        # Arrange
        board_size = 2
        blue_player.player_update("Computer")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        board = game.new_board()

        # Assert
        mock_error.assert_called_once()
        assert "Board size must be greater than 2" in str(mock_error.call_args)

    @patch('tkinter.messagebox.showerror')
    def test_game_does_not_start_with_invalid_board_size_too_large(self, mock_error, blue_player, red_player):
        """Test that game shows error with board size > 9"""
        # Arrange
        board_size = 10
        blue_player.player_update("Computer")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        board = game.new_board()

        # Assert
        mock_error.assert_called_once()
        assert "Board size must be less than 10" in str(mock_error.call_args)

    def test_computer_player_can_make_moves(self, blue_player):
        """Test that computer player has move-making capability"""
        # Arrange
        blue_player.player_update("Computer")
        computer = ComputerPlayer(blue_player)

        # Act & Assert
        assert hasattr(computer, 'move_selector')
        assert hasattr(computer, 'make_random_move')
        assert hasattr(computer, 'make_sos_move')
        assert callable(computer.move_selector)
        assert callable(computer.make_random_move)
        assert callable(computer.make_sos_move)

    def test_game_board_matrix_created_correctly_with_computer_players(self, blue_player, red_player):
        """Test that board matrix is created correctly when computer players are involved"""
        # Arrange
        board_size = 5
        blue_player.player_update("Computer")
        red_player.player_update("Computer")

        # Act
        game = SOSGameBase(blue_player, red_player, board_size)
        board = game.new_board()

        # Assert
        assert game.cell_matrix is not None
        assert len(game.cell_matrix) == board_size
        for row in game.cell_matrix:
            assert len(row) == board_size
            for cell in row:
                assert cell is not None

    def test_simple_game_with_computer_has_correct_win_condition(self, blue_player, red_player):
        """Test that simple game with computer players uses correct win condition"""
        # Arrange
        board_size = 3
        blue_player.player_update("Computer")
        red_player.player_update("Human")

        # Act
        base_game = SOSGameBase(blue_player, red_player, board_size)
        simple_game = SimpleSOSGame(base_game, blue_player, red_player)
        board = simple_game.new_board()  # Must create board before checking win condition

        # Assert
        assert hasattr(simple_game, 'win_condition')
        assert callable(simple_game.win_condition)
        # Initially no winner
        assert simple_game.win_condition() == False

    def test_general_game_with_computer_has_correct_win_condition(self, blue_player, red_player):
        """Test that general game with computer players uses correct win condition"""
        # Arrange
        board_size = 3
        blue_player.player_update("Human")
        red_player.player_update("Computer")

        # Act
        base_game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(base_game, blue_player, red_player)
        board = general_game.new_board()  # Must create board before checking win condition

        # Assert
        assert hasattr(general_game, 'win_condition')
        assert callable(general_game.win_condition)
        # Initially no winner
        assert general_game.win_condition() == False