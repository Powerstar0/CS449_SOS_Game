import time
import tkinter
from tkinter import messagebox
from tkinter import *
from Board import Board
import random

class Player:
    def __init__(self, player_type="Human"):
        # Set scores to 0
        self.score = IntVar(value=0)
        # Define the player type
        self.player_type = "Human"
        # Start players off with a default S symbol
        self.symbol = 'S'

    def symbol_update(self, symbol):
        """ Updates symbol for a player"""
        self.symbol = symbol

    def player_update(self, player_type):
        self.player_type = player_type


class ComputerPlayer(Player):
    def __init__(self, base_player):
        super().__init__()
        super().__dict__.update(base_player.__dict__)
        self.difficulty = "Simple"
        self.player_type = "Computer"
        # Updates base game parameters with what was given

    def move_selector(self, board_size, matrix_list):
        if self.sos_identification(board_size, matrix_list):
            return self.sos_identification(board_size, matrix_list)
        return self.make_random_move(board_size, matrix_list)

    def make_random_move(self, board_size, matrix_list):
        """ Makes a random valid move """
        row = random.randint(0, board_size - 1)
        col = random.randint(0, board_size - 1)
        while matrix_list[row][col]["state"] == tkinter.DISABLED:
            row = random.randint(0, board_size - 1)
            col = random.randint(0, board_size - 1)
        if random.randint(0, 1) == 0:
            self.symbol = 'S'
        else:
            self.symbol = 'O'
        return matrix_list[row][col]

    def sos_identification(self, board_size, matrix_list):
        """ Identifies and makes a completing move if an SOS can be made """
        # SOS Check For Horizontal SOS
        for i in range(board_size - 2):
            for j in range(board_size):
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i + 1][j]['text'] == 'O' and matrix_list[i + 2][j][
                    "state"] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i + 2][j]
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i + 2][j]['text'] == 'S' and matrix_list[i + 1][j]['state'] != tkinter.DISABLED:
                    self.symbol = 'O'
                    return matrix_list[i + 1][j]
                if matrix_list[i + 1][j]['text'] == 'O' and matrix_list[i + 2][j]['text'] == 'S' and matrix_list[i][j]['state'] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i][j]

        # SOS Check for Vertical SOS
        for i in range(board_size):
            for j in range(board_size - 2):
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i][j + 1]['text'] == 'O' and matrix_list[i][j + 2][
                    "state"] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i][j + 2]
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i][j + 2]['text'] == 'S' and matrix_list[i][j + 1]['state'] != tkinter.DISABLED:
                    self.symbol = 'O'
                    return matrix_list[i][j + 1]
                if matrix_list[i][j + 1]['text'] == 'O' and matrix_list[i][j + 2]['text'] == 'S' and matrix_list[i][j]['state'] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i][j]

        # SOS Check for left diagonal SOS
        for i in range(board_size - 2):
            for j in range(board_size - 2):
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i + 1][j + 1]['text'] == 'O' and matrix_list[i + 2][j + 2][
                    "state"] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i + 2][j + 2]
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i + 2][j + 2]['text'] == 'S' and matrix_list[i + 1][j + 1]['state'] != tkinter.DISABLED:
                    self.symbol = 'O'
                    return matrix_list[i + 1][j + 1]
                if matrix_list[i + 1][j + 1]['text'] == 'O' and matrix_list[i + 2][j + 2]['text'] == 'S' and matrix_list[i][j]['state'] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i][j]

        # SOS Check for right diagonal SOS
        for i in range(board_size - 2):
            for j in range(2, board_size):
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i + 1][j - 1]['text'] == 'O' and \
                        matrix_list[i + 2][j - 2][
                            "state"] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i + 2][j - 2]
                if matrix_list[i][j]['text'] == 'S' and matrix_list[i + 2][j - 2]['text'] == 'S' and \
                        matrix_list[i + 1][j - 1]['state'] != tkinter.DISABLED:
                    self.symbol = 'O'
                    return matrix_list[i + 1][j - 1]
                if matrix_list[i + 1][j - 1]['text'] == 'O' and matrix_list[i + 2][j - 2]['text'] == 'S' and \
                        matrix_list[i][j]['state'] != tkinter.DISABLED:
                    self.symbol = 'S'
                    return matrix_list[i][j]
        return False

    def complete_sequence(self):
        pass


class SOSGameBase:
    def __init__(self, blue_player, red_player, board_size=3):
        # Default board size of 3
        self.board_size = board_size
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
        # Signals end of game
        self.game_over = False

    def new_board(self):
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
                                 message="Invalid input for board size, must enter a number greater than 2 and less "
                                         "than 10")

    def cell_update(self, cell):
        """ Updates cell with symbol """
        turn = self.turn.get()
        # Blue turn
        if turn == "Current Turn: Blue":
            # Adds the symbol and disable the button to prevent any further changes
            cell.config(text=self.blue_player.symbol, state=DISABLED, font=("Helvetica", 40))
            self.check_sos()
            if not self.win_condition():
                self.turn.set(value="Current Turn: Red")
                if self.red_player.player_type == "Computer":
                    self.cell_update(self.red_player.move_selector(self.board_size, self.cell_matrix))

        # Red turn
        else:
            # Adds the symbol and disable the button to prevent any further changes
            cell.config(text=self.red_player.symbol, state=DISABLED, font=("Helvetica", 40))
            self.check_sos()
            if not self.win_condition():
                self.turn.set(value="Current Turn: Blue")
                if self.blue_player.player_type == "Computer":
                    self.cell_update(self.blue_player.move_selector(self.board_size, self.cell_matrix))

    def set_game_type(self, game_type):
        """ Sets game type """
        self.game_type = game_type

    def check_sos(self):
        """ Checks if an SOS has been completed """

        # SOS Check For Horizontal SOS
        for i in range(self.board_size - 2):
            for j in range(self.board_size):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i + 1][j]['text'] == 'O' and \
                        self.cell_matrix[i + 2][j]['text'] == 'S':
                    if [self.cell_matrix[i][j], self.cell_matrix[i + 1][j],
                        self.cell_matrix[i + 2][j]] not in self.complete_sos_list:
                        # Add sequence to completed list
                        self.complete_sos_list.append(
                            [self.cell_matrix[i][j], self.cell_matrix[i + 1][j], self.cell_matrix[i + 2][j]])
                        # Color sequence
                        self.color_sequence(self.cell_matrix[i][j], self.cell_matrix[i + 1][j],
                                            self.cell_matrix[i + 2][j])

        # SOS Check For Vertical SOS
        for i in range(self.board_size):
            for j in range(self.board_size - 2):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i][j + 1]['text'] == 'O' and \
                        self.cell_matrix[i][j + 2]['text'] == 'S':
                    if [self.cell_matrix[i][j], self.cell_matrix[i][j + 1],
                        self.cell_matrix[i][j + 2]] not in self.complete_sos_list:
                        # Add sequence to completed list
                        self.complete_sos_list.append(
                            [self.cell_matrix[i][j], self.cell_matrix[i][j + 1], self.cell_matrix[i][j + 2]])
                        # Color sequence
                        self.color_sequence(self.cell_matrix[i][j], self.cell_matrix[i][j + 1],
                                            self.cell_matrix[i][j + 2])

        # SOS Check For Left Diagonal SOS
        for i in range(self.board_size - 2):
            for j in range(self.board_size - 2):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i + 1][j + 1]['text'] == 'O' and \
                        self.cell_matrix[i + 2][j + 2]['text'] == 'S':
                    if [self.cell_matrix[i][j], self.cell_matrix[i + 1][j + 1],
                        self.cell_matrix[i + 2][j + 2]] not in self.complete_sos_list:
                        # Add sequence to completed list
                        self.complete_sos_list.append(
                            [self.cell_matrix[i][j], self.cell_matrix[i + 1][j + 1], self.cell_matrix[i + 2][j + 2]])
                        # Color sequence
                        self.color_sequence(self.cell_matrix[i][j], self.cell_matrix[i + 1][j + 1],
                                            self.cell_matrix[i + 2][j + 2])

        # SOS Check For Right Diagonal SOS
        for i in range(self.board_size - 2):
            for j in range(2, self.board_size):
                if self.cell_matrix[i][j]['text'] == 'S' and self.cell_matrix[i + 1][j - 1]['text'] == 'O' and \
                        self.cell_matrix[i + 2][j - 2]['text'] == 'S':
                    if [self.cell_matrix[i][j], self.cell_matrix[i + 1][j - 1],
                        self.cell_matrix[i + 2][j - 2]] not in self.complete_sos_list:
                        # Add sequence to completed list
                        self.complete_sos_list.append(
                            [self.cell_matrix[i][j], self.cell_matrix[i + 1][
                                j - 1], self.cell_matrix[i + 2][j - 2]])
                        # Color sequence
                        self.color_sequence(self.cell_matrix[i][j], self.cell_matrix[i + 1][j - 1],
                                            self.cell_matrix[i + 2][j - 2])

    def win_condition(self):
        """ Placeholder for derived classes """
        return False

    def disable_buttons(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.cell_matrix[i][j].config(state=DISABLED)

    def filled_cells(self):
        """ # Check to see if all cells are disabled """
        game_complete = True
        print("checking filled cells")
        while game_complete:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if self.cell_matrix[i][j]["state"] == tkinter.DISABLED:
                        pass
                    else:
                        game_complete = False
                        print(game_complete)
            print(game_complete)
        return game_complete

    def color_sequence(self, cell1, cell2, cell3):
        """ Colors the sequence of cells """
        button_list = [cell1, cell2, cell3]
        for cell in button_list:
            if cell.cget("disabledforeground") == "SystemDisabledText":
                # Default is "SystemDisabledText" since the system hasn't assigned the disabledforeground a color yet
                if self.turn.get() == "Current Turn: Blue":
                    cell.config(disabledforeground='blue')
                elif self.turn.get() == "Current Turn: Red":
                    cell.config(disabledforeground='red')
            else:
                # Turn a button purple if turn and color don't match
                if (self.turn.get() == "Current Turn: Blue") and (cell.cget("disabledforeground") == "red"):
                    cell.config(disabledforeground='purple')
                if (self.turn.get() == "Current Turn: Red") and (cell.cget("disabledforeground") == "blue"):
                    cell.config(disabledforeground='purple')

    def start_game(self):
        """ Only applicable to Computer games """
        if self.blue_player.player_type == "Computer":
            if self.turn.get() == "Current Turn: Blue":
                self.cell_update(self.blue_player.move_selector(self.board_size, self.cell_matrix))


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
            messagebox.showinfo(title="Game Over",
                                message=f"{self.turn.get()[13:]} wins")
            self.game_over = True
            return True
        elif self.filled_cells():
            self.disable_buttons()
            messagebox.showinfo(title="Game Over", message="Tie")
            self.game_over = True
            return True
        return False


class GeneralSOSGame(SOSGameBase):
    def __init__(self, base_game, blue_player, red_player):
        # Initialize base game template
        super().__init__(blue_player, red_player)
        # Updates base game parameters with what was given
        super().__dict__.update(base_game.__dict__)
        self.counter = 0

    def win_condition(self):
        """ Win condition for general SOS"""
        # If cells are disabled, determine winner based on score
        if self.filled_cells():
            print("Filled cells found")
            if self.blue_player.score.get() > self.red_player.score.get():
                print("Blue Player won")
                messagebox.showinfo(title="Game Over",
                                    message=" Blue wins")
            elif self.blue_player.score.get() == self.red_player.score.get():
                print("Tie")
                messagebox.showinfo(title="Game Over",
                                    message=f"Tie")
            else:
                print("Red Player won")
                messagebox.showinfo(title="Game Over",
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
                if self.red_player.player_type == "Computer":
                    self.cell_update(self.red_player.move_selector(self.board_size, self.cell_matrix))
            elif self.blue_player.player_type == "Computer":
                self.cell_update(self.blue_player.move_selector(self.board_size, self.cell_matrix))

        else:
            new_score = self.red_player.score.get() + points_scored
            self.red_player.score.set(new_score)
            if points_scored == 0:
                self.turn.set(value="Current Turn: Blue")
                if self.blue_player.player_type == "Computer":
                    self.cell_update(self.blue_player.move_selector(self.board_size, self.cell_matrix))
            elif self.red_player.player_type == "Computer":
                self.cell_update(self.red_player.move_selector(self.board_size, self.cell_matrix))

    def cell_update(self, cell):
        self.counter += 1
        print(self.counter)
        """ Updates cell with symbol """
        # Blue turn
        turn = self.turn.get()
        if self.win_condition():
            print("win condition found")
            self.disable_buttons()
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
