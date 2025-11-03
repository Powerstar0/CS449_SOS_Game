from tkinter import messagebox
from tkinter import *


class Player:
    def __init__(self, player_type="Human"):
        # Set scores to 0
        self.score = 0
        # Define the player type
        self.player_type = player_type
        # Start players off with a default S symbol
        self.symbol = 'S'

    def symbol_update(self, symbol):
        """ Updates symbol for a player"""
        self.symbol = symbol


class SOSGameBase:
    def __init__(self, blue_player, red_player):
        from Board import Board
        # Default board size of 3
        self.board_size = 3
        # Default game type of simple
        self.game_type = "Simple Game"
        # Define blue and red players
        self.blue_player = blue_player
        self.red_player = red_player
        # Set variable for the current turn
        self.turn = StringVar(value="Current Turn: Blue")
        self.board = Board(self.board_size, self.cell_update)
        self.cell_matrix = None

    def new_board(self):
        from Board import Board
        """ Creates a new board with specified user size"""
        try:
            # If board size is correct (n > 2 and n < 10)
            if 2 < self.board_size < 10:
                # Make the board and pass cell function and game mode
                self.board = Board(self.board_size, self.cell_update)
                self.cell_matrix = self.board.cell_matrix
                return self.board
            # If board size is n < 3 (too small)
            elif self.board_size < 3:
                messagebox.showerror(title="Error", message="Board size must be greater than 2")
            # If board size is n > 10 (too large)
            elif self.board_size > 9:
                messagebox.showerror(title="Error", message="Board size must be less than 10")
        except (Exception,):
            # If an invalid input is entered (blank and non-integers)
            messagebox.showerror(title="Error",
                                 message="Invalid input for board size, must enter a number greater than 3 and less "
                                         "than 9")

    def cell_update(self, cell):
        """ Updates cell with symbol """
        # Blue turn
        turn = self.turn.get()
        if turn == "Current Turn: Blue":
            # Adds the symbol and disable the button to prevent any further changes
            cell.config(text=self.blue_player.symbol, state=DISABLED, font=("Helvetica", 40))
            self.check_sos()
            self.turn.set(value="Current Turn: Red")
        # Red turn
        else:
            # Adds the symbol and disable the button to prevent any further changes
            cell.config(text=self.red_player.symbol, state=DISABLED, font=("Helvetica", 40))
            self.check_sos()
            self.turn.set(value="Current Turn: Blue")

    def set_game_type(self, game_type):
        """ Sets game type """
        self.game_type = game_type

    def check_sos(self):
        """ Checks if an SOS has been completed """

        # SOS Check For Horizontal SOS
        for i in range(self.board_size - 2):
            for j in range(self.board_size):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i+1][j]['text'] == 'O' and self.cell_matrix[i+2][j]['text'] == 'S':
                    print("SOS")
                    self.board.draw_sos_line(i)




class SimpleSOSGame(SOSGameBase):
    def __init__(self, base_game, blue_player, red_player):
        # Initialize base game template
        super().__init__(blue_player, red_player)
        # Updates base game parameters with what was given
        super().__dict__.update(base_game.__dict__)





class GeneralSOSGame(SOSGameBase):
    def __init__(self, base_game, blue_player, red_player):
        # Initialize base game template
        super().__init__(blue_player, red_player)
        # Updates base game parameters with what was given
        super().__dict__.update(base_game.__dict__)
