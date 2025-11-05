import time
import tkinter
from tkinter import messagebox
from tkinter import *


class Player:
    def __init__(self, player_type="Human"):
        # Set scores to 0
        self.score = IntVar(value=0)
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
        blue_player.score.set(0)
        self.red_player = red_player
        red_player.score.set(0)
        # Set variable for the current turn
        self.turn = StringVar(value="Current Turn: Blue")
        # Create Board Placeholder
        self.board = Board(self.board_size, self.cell_update)
        # Cell matrix placeholder
        self.cell_matrix = None
        # Store all the complete SOS button sequences
        self.complete_sos_list = []

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
            self.win_condition()
            self.turn.set(value="Current Turn: Red")
        # Red turn
        else:
            # Adds the symbol and disable the button to prevent any further changes
            cell.config(text=self.red_player.symbol, state=DISABLED, font=("Helvetica", 40))
            self.check_sos()
            self.win_condition()
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
                    if [self.cell_matrix[i][j], self.cell_matrix[i+1][j], self.cell_matrix[i+2][j]] not in self.complete_sos_list:
                        print("SOS")
                        # Add sequence to completed list
                        self.complete_sos_list.append([self.cell_matrix[i][j], self.cell_matrix[i+1][j], self.cell_matrix[i+2][j]])


        # SOS Check For Vertical SOS
        for i in range(self.board_size):
            for j in range(self.board_size - 2):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i][j + 1]['text'] == 'O' and self.cell_matrix[i][j + 2]['text'] == 'S':
                    if [self.cell_matrix[i][j], self.cell_matrix[i][j + 1], self.cell_matrix[i][j + 2]] not in self.complete_sos_list:
                        print("SOS")
                        # Add sequence to completed list
                        self.complete_sos_list.append([self.cell_matrix[i][j], self.cell_matrix[i][j+1], self.cell_matrix[i][j+2]])


        # SOS Check For Left Diagonal SOS
        for i in range(self.board_size - 2):
            for j in range(self.board_size - 2):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i + 1][j + 1]['text'] == 'O' and \
                        self.cell_matrix[i + 2][j + 2]['text'] == 'S':
                    if [self.cell_matrix[i][j], self.cell_matrix[i + 1][j + 1],
                        self.cell_matrix[i + 2][j + 2]] not in self.complete_sos_list:
                        print("SOS")
                        # Add sequence to completed list
                        self.complete_sos_list.append([self.cell_matrix[i][j], self.cell_matrix[i + 1][j + 1], self.cell_matrix[i + 2][j + 2]])


        # SOS Check For Right Diagonal SOS
        for i in range(self.board_size - 2):
            for j in range(2, self.board_size):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i + 1][j - 1]['text'] == 'O' and \
                        self.cell_matrix[i + 2][j - 2]['text'] == 'S':
                    if [self.cell_matrix[i][j], self.cell_matrix[i + 1][j - 1],
                        self.cell_matrix[i + 2][j - 2]] not in self.complete_sos_list:
                        print("SOS")
                        # Add sequence to completed list
                        self.complete_sos_list.append(
                            [self.cell_matrix[i][j], self.cell_matrix[i + 1][j - 1], self.cell_matrix[i + 2][j - 2]])


    def win_condition(self):
        """ Placeholder for derived classes """
        return False

    def disable_buttons(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.cell_matrix[i][j].config(state=DISABLED)

    def filled_cells(self):
        # Check to see if all cells are disabled
        game_complete = True
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.cell_matrix[i][j]["state"] == tkinter.DISABLED:
                    pass
                else:
                    game_complete = False
                    break
        return game_complete




class SimpleSOSGame(SOSGameBase):
    def __init__(self, base_game, blue_player, red_player):
        # Initialize base game template
        super().__init__(blue_player, red_player)
        # Updates base game parameters with what was given
        super().__dict__.update(base_game.__dict__)

    def win_condition(self):
        """ First to complete SOS"""
        if self.complete_sos_list:
            self.disable_buttons()
            messagebox.showerror(title="Game Over",
                                 message=f"{self.turn.get()[13:]} wins")
        elif self.filled_cells():
            self.disable_buttons()
            messagebox.showerror(title="Game Over", message="Tie")


class GeneralSOSGame(SOSGameBase):
    def __init__(self, base_game, blue_player, red_player):
        # Initialize base game template
        super().__init__(blue_player, red_player)
        # Updates base game parameters with what was given
        super().__dict__.update(base_game.__dict__)

    def win_condition(self):
        """ Win condition for general SOS"""
        # If cells are disabled, determine winner based on score
        if self.filled_cells():
            if self.blue_player.score.get() > self.red_player.score.get():
                print("Blue Player won")
                messagebox.showerror(title="Game Over",
                                     message=" Blue wins")
            elif self.blue_player.score.get() == self.red_player.score.get():
                print("Tie")
                messagebox.showerror(title="Game Over",
                                     message=f"Tie")
            else:
                print("Red Player won")
                messagebox.showerror(title="Game Over",
                                     message=f"Red wins")
            return True
        return False


    def check_sos(self):
        """ Overload check_sos method"""
        old_sos_list = self.complete_sos_list.copy()
        super().check_sos()
        points_scored = len(self.complete_sos_list) - len(old_sos_list)
        if self.turn.get() == "Current Turn: Blue":
            new_score = self.blue_player.score.get() + points_scored
            self.blue_player.score.set(new_score)
            if points_scored == 0:
                self.turn.set(value="Current Turn: Red")
        else:
            new_score = self.red_player.score.get() + points_scored
            self.red_player.score.set(new_score)
            if points_scored == 0:
                self.turn.set(value="Current Turn: Blue")


    def cell_update(self, cell):
        """ Updates cell with symbol """
        # Blue turn
        turn = self.turn.get()
        if turn == "Current Turn: Blue":
            # Adds the symbol and disable the button to prevent any further changes
            cell.config(text=self.blue_player.symbol, state=DISABLED, font=("Helvetica", 40))
            self.check_sos()
            if self.win_condition():
                self.disable_buttons()
        # Red turn
        else:
            # Adds the symbol and disable the button to prevent any further changes
            cell.config(text=self.red_player.symbol, state=DISABLED, font=("Helvetica", 40))
            self.check_sos()
            if self.win_condition():
                self.disable_buttons()




