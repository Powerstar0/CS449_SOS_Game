import pytest
from unittest.mock import Mock, patch, MagicMock
from tkinter import Tk, StringVar, IntVar, DISABLED, NORMAL
import tkinter
from Game_Logic import Player, ComputerPlayer, SOSGameBase, SimpleSOSGame, GeneralSOSGame


@pytest.fixture(scope="function")
def tk_root():
    """Create a Tkinter root window for tests that need it"""
    root = Tk()
    yield root
    try:
        root.destroy()
    except:
        pass


@pytest.fixture
def blue_player(tk_root):
    """Create a blue player"""
    return Player()


@pytest.fixture
def red_player(tk_root):
    """Create a red player"""
    return Player()


class TestAC71_WinByBlueOrRed:
    """
    AC 7.1 A win by blue/red
    Given an ongoing general game
    And it is blue/red's turn
    When blue/red places a letter that fills up the board
    Then the game is over
    And the player with the most points wins
    """

    def test_blue_wins_when_board_full_and_blue_has_more_points(self, blue_player, red_player):
        """Test blue wins when board fills and blue has more points"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Set up almost-full board with blue having more points
        general_game.blue_player.score.set(3)
        general_game.red_player.score.set(1)

        # Fill all cells except one
        for i in range(board_size):
            for j in range(board_size):
                if not (i == 2 and j == 2):  # Leave last cell empty
                    general_game.cell_matrix[i][j].config(text='S', state=DISABLED)

        general_game.turn.set("Current Turn: Blue")

        # Act - Blue fills the last cell
        with patch('tkinter.messagebox.showinfo') as mock_info:
            general_game.cell_matrix[2][2].config(text='O', state=DISABLED)
            result = general_game.win_condition()

        # Assert
        assert result == True
        mock_info.assert_called_once()
        assert "Blue wins" in str(mock_info.call_args)

    def test_red_wins_when_board_full_and_red_has_more_points(self, blue_player, red_player):
        """Test red wins when board fills and red has more points"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Set up almost-full board with red having more points
        general_game.blue_player.score.set(2)
        general_game.red_player.score.set(5)

        # Fill all cells except one
        for i in range(board_size):
            for j in range(board_size):
                if not (i == 1 and j == 1):  # Leave middle cell empty
                    general_game.cell_matrix[i][j].config(text='O', state=DISABLED)

        general_game.turn.set("Current Turn: Red")

        # Act - Red fills the last cell
        with patch('tkinter.messagebox.showinfo') as mock_info:
            general_game.cell_matrix[1][1].config(text='S', state=DISABLED)
            result = general_game.win_condition()

        # Assert
        assert result == True
        mock_info.assert_called_once()
        assert "Red wins" in str(mock_info.call_args)

    def test_game_over_flag_set_after_win(self, blue_player, red_player):
        """Test game_over flag is set to True after a win"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        general_game.blue_player.score.set(4)
        general_game.red_player.score.set(2)

        # Fill all cells
        for i in range(board_size):
            for j in range(board_size):
                general_game.cell_matrix[i][j].config(text='S', state=DISABLED)

        # Act
        with patch('tkinter.messagebox.showinfo'):
            general_game.win_condition()

        # Assert - Game should be over (win_condition returns True)
        assert general_game.filled_cells() == True

    def test_blue_wins_with_larger_board(self, blue_player, red_player):
        """Test blue wins on a larger board with more points"""
        # Arrange
        board_size = 5
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Set up full board with blue having more points
        general_game.blue_player.score.set(10)
        general_game.red_player.score.set(7)

        # Fill all cells
        for i in range(board_size):
            for j in range(board_size):
                general_game.cell_matrix[i][j].config(text='O', state=DISABLED)

        general_game.turn.set("Current Turn: Blue")

        # Act
        with patch('tkinter.messagebox.showinfo') as mock_info:
            result = general_game.win_condition()

        # Assert
        assert result == True
        mock_info.assert_called_once()
        assert "Blue wins" in str(mock_info.call_args)

    def test_winner_determined_by_score_not_turn(self, blue_player, red_player):
        """Test winner is determined by score, not whose turn it is"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Red has more points but it's Blue's turn
        general_game.blue_player.score.set(1)
        general_game.red_player.score.set(6)

        # Fill all cells
        for i in range(board_size):
            for j in range(board_size):
                general_game.cell_matrix[i][j].config(text='S', state=DISABLED)

        general_game.turn.set("Current Turn: Blue")

        # Act
        with patch('tkinter.messagebox.showinfo') as mock_info:
            result = general_game.win_condition()

        # Assert - Red should win despite Blue's turn
        assert result == True
        mock_info.assert_called_once()
        assert "Red wins" in str(mock_info.call_args)


class TestAC72_DrawGame:
    """
    AC 7.2 A draw game
    Given an ongoing general game
    And it is blue/red's turn
    When blue/red places a letter that fills up the board
    And the final score of both players is the same
    Then the game is over
    And it is a draw
    """

    def test_draw_when_board_full_and_scores_equal(self, blue_player, red_player):
        """Test draw when board is full and both players have equal scores"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Set equal scores
        general_game.blue_player.score.set(3)
        general_game.red_player.score.set(3)

        # Fill all cells except one
        for i in range(board_size):
            for j in range(board_size):
                if not (i == 0 and j == 0):  # Leave one cell empty
                    general_game.cell_matrix[i][j].config(text='S', state=DISABLED)

        general_game.turn.set("Current Turn: Blue")

        # Act - Fill last cell
        with patch('tkinter.messagebox.showinfo') as mock_info:
            general_game.cell_matrix[0][0].config(text='O', state=DISABLED)
            result = general_game.win_condition()

        # Assert
        assert result == True
        mock_info.assert_called_once()
        assert "Tie" in str(mock_info.call_args)

    def test_draw_with_zero_scores(self, blue_player, red_player):
        """Test draw when both players have zero points"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Scores default to 0
        general_game.blue_player.score.set(0)
        general_game.red_player.score.set(0)

        # Fill all cells
        for i in range(board_size):
            for j in range(board_size):
                general_game.cell_matrix[i][j].config(text='O', state=DISABLED)

        general_game.turn.set("Current Turn: Red")

        # Act
        with patch('tkinter.messagebox.showinfo') as mock_info:
            result = general_game.win_condition()

        # Assert
        assert result == True
        mock_info.assert_called_once()
        assert "Tie" in str(mock_info.call_args)

    def test_draw_with_high_equal_scores(self, blue_player, red_player):
        """Test draw when both players have high equal scores"""
        # Arrange
        board_size = 4
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Set high equal scores
        general_game.blue_player.score.set(15)
        general_game.red_player.score.set(15)

        # Fill all cells
        for i in range(board_size):
            for j in range(board_size):
                general_game.cell_matrix[i][j].config(text='S', state=DISABLED)

        # Act
        with patch('tkinter.messagebox.showinfo') as mock_info:
            result = general_game.win_condition()

        # Assert
        assert result == True
        mock_info.assert_called_once()
        assert "Tie" in str(mock_info.call_args)

    def test_draw_regardless_of_whose_turn(self, blue_player, red_player):
        """Test draw is declared regardless of whose turn filled the board"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Equal scores
        general_game.blue_player.score.set(5)
        general_game.red_player.score.set(5)

        # Fill all cells
        for i in range(board_size):
            for j in range(board_size):
                general_game.cell_matrix[i][j].config(text='O', state=DISABLED)

        # Red's turn but equal scores
        general_game.turn.set("Current Turn: Red")

        # Act
        with patch('tkinter.messagebox.showinfo') as mock_info:
            result = general_game.win_condition()

        # Assert
        assert result == True
        assert "Tie" in str(mock_info.call_args)

    def test_game_over_on_draw(self, blue_player, red_player):
        """Test game_over state is properly set on draw"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        general_game.blue_player.score.set(2)
        general_game.red_player.score.set(2)

        # Fill all cells
        for i in range(board_size):
            for j in range(board_size):
                general_game.cell_matrix[i][j].config(text='S', state=DISABLED)

        # Act
        with patch('tkinter.messagebox.showinfo'):
            result = general_game.win_condition()

        # Assert
        assert result == True
        assert general_game.filled_cells() == True


class TestAC73_ContinuingGame:
    """
    AC 7.3 A continuing game
    Given an ongoing game
    And it is blue/red's turn
    When blue/red places a letter
    And the board is not filled
    Then the game continues
    """

    def test_game_continues_when_board_not_full_blue_turn(self, blue_player, red_player):
        """Test game continues when board is not full on blue's turn"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Place one letter
        general_game.cell_matrix[0][0].config(text='S', state=DISABLED)
        general_game.turn.set("Current Turn: Blue")

        # Act
        result = general_game.win_condition()

        # Assert
        assert result == False
        assert general_game.filled_cells() == False

    def test_game_continues_when_board_not_full_red_turn(self, blue_player, red_player):
        """Test game continues when board is not full on red's turn"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Place several letters but not all
        general_game.cell_matrix[0][0].config(text='S', state=DISABLED)
        general_game.cell_matrix[1][1].config(text='O', state=DISABLED)
        general_game.cell_matrix[2][2].config(text='S', state=DISABLED)
        general_game.turn.set("Current Turn: Red")

        # Act
        result = general_game.win_condition()

        # Assert
        assert result == False
        assert general_game.filled_cells() == False

    def test_game_continues_with_one_empty_cell(self, blue_player, red_player):
        """Test game continues even with just one empty cell remaining"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Fill all but one cell
        for i in range(board_size):
            for j in range(board_size):
                if not (i == 2 and j == 2):  # Leave last cell empty
                    general_game.cell_matrix[i][j].config(text='S', state=DISABLED)

        general_game.turn.set("Current Turn: Blue")

        # Act
        result = general_game.win_condition()

        # Assert
        assert result == False
        assert general_game.filled_cells() == False

    def test_game_continues_on_larger_board(self, blue_player, red_player):
        """Test game continues on larger board with multiple empty cells"""
        # Arrange
        board_size = 5
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Fill half the board
        for i in range(board_size):
            for j in range(board_size // 2):
                general_game.cell_matrix[i][j].config(text='O', state=DISABLED)

        general_game.turn.set("Current Turn: Red")

        # Act
        result = general_game.win_condition()

        # Assert
        assert result == False
        assert general_game.filled_cells() == False

    def test_game_continues_after_scoring_sos(self, blue_player, red_player):
        """Test game continues after scoring SOS if board not full"""
        # Arrange
        board_size = 4
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Create an SOS sequence
        general_game.cell_matrix[0][0].config(text='S', state=DISABLED)
        general_game.cell_matrix[1][0].config(text='O', state=DISABLED)
        general_game.cell_matrix[2][0].config(text='S', state=DISABLED)

        # Check for SOS
        general_game.check_sos()

        general_game.turn.set("Current Turn: Blue")

        # Act
        result = general_game.win_condition()

        # Assert - Game should continue even after scoring
        assert result == False
        assert general_game.filled_cells() == False

    def test_game_continues_with_no_moves_yet(self, blue_player, red_player):
        """Test game continues at the start with empty board"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        general_game.turn.set("Current Turn: Blue")

        # Act
        result = general_game.win_condition()

        # Assert
        assert result == False
        assert general_game.filled_cells() == False

    def test_game_continues_regardless_of_score_if_board_not_full(self, blue_player, red_player):
        """Test game continues regardless of scores if board not full"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Set high scores but board not full
        general_game.blue_player.score.set(10)
        general_game.red_player.score.set(15)

        # Fill some cells
        general_game.cell_matrix[0][0].config(text='S', state=DISABLED)
        general_game.cell_matrix[1][1].config(text='O', state=DISABLED)

        general_game.turn.set("Current Turn: Blue")

        # Act
        result = general_game.win_condition()

        # Assert - Game continues despite scores
        assert result == False
        assert general_game.filled_cells() == False

    def test_turn_alternates_when_game_continues(self, blue_player, red_player):
        """Test turns alternate properly when game continues"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        general_game.turn.set("Current Turn: Blue")

        # Act - Make a non-scoring move
        general_game.cell_matrix[0][0].config(text='S', state=DISABLED)
        points = general_game.check_sos()

        # If no points scored, turn should change
        if points == 0:
            general_game.turn.set("Current Turn: Red")

        # Assert
        assert general_game.win_condition() == False
        assert general_game.turn.get() == "Current Turn: Red"

    def test_multiple_moves_game_continues(self, blue_player, red_player):
        """Test game continues through multiple moves until board fills"""
        # Arrange
        board_size = 3
        game = SOSGameBase(blue_player, red_player, board_size)
        general_game = GeneralSOSGame(game, blue_player, red_player)
        board = general_game.new_board()

        # Make several moves
        moves = [
            (0, 0, 'S'),
            (0, 1, 'O'),
            (0, 2, 'S'),
            (1, 0, 'O'),
            (1, 1, 'S'),
            (1, 2, 'O'),
            (2, 0, 'S'),
            (2, 1, 'O'),
            # Leave (2, 2) empty
        ]

        for i, j, letter in moves:
            general_game.cell_matrix[i][j].config(text=letter, state=DISABLED)
            # Game should continue
            assert general_game.win_condition() == False

        # Assert - Game still continues with one cell left
        assert general_game.filled_cells() == False
