from tkinter import *
from tkinter import ttk, messagebox

from Board import Board


class SOS:
    def __init__(self):
        """ Initialize SOS game GUI """

        # Creates window
        root = Tk()
        root.geometry("800x600")
        root.title("SOS Game")
        # No ability to resize since component size don't scale
        root.resizable(width=False, height=False)

        # Top Frame
        top_frame = ttk.Frame(root)
        top_frame.pack(side=TOP, fill=X, pady=(0, 50))

        # SOS Label in top left
        ttk.Label(top_frame, text="SOS").pack(side=LEFT)

        # Radio buttons for game type next to SOS label
        self.game_type = StringVar(value="")
        ttk.Radiobutton(top_frame, variable=self.game_type, value="Simple Game", text="Simple Game").pack(side=LEFT,
                                                                                                          anchor=NW)
        ttk.Radiobutton(top_frame, variable=self.game_type, value="General Game", text="General Game").pack(side=LEFT,
                                                                                                            anchor=NW)

        # Prompt to ask user for board size in upper right
        # Default value of 3
        self.board_size = IntVar(value=3)
        Entry(top_frame, width=2, textvariable=self.board_size).pack(side=RIGHT)

        # Board size prompt label
        Label(top_frame, text="Board Size").pack(side=RIGHT)

        # Left Frame
        left_frame = ttk.Frame(root)
        left_frame.pack(side=LEFT, fill=Y)

        # Blue player options (label and radio buttons) on left side

        ttk.Label(left_frame, text="Blue Player").pack(side=TOP)
        blue_player_type = IntVar()
        self.blue_player_choice = StringVar()
        ttk.Radiobutton(left_frame, variable=blue_player_type, value=1, text="Human").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=self.blue_player_choice, value='S', text="S").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=self.blue_player_choice, value='O', text="O").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=blue_player_type, value=2, text="Computer").pack(side=TOP)

        # Record game checkbox on bottom left
        ttk.Checkbutton(left_frame, text="Record").pack(side=BOTTOM)

        # Right Frame
        right_frame = ttk.Frame(root)
        right_frame.pack(side=RIGHT, fill=Y)

        # Red player options (label and radio buttons) on right side
        ttk.Label(right_frame, text="Red Player").pack(side=TOP)
        red_player_type = IntVar()
        red_player_choice = IntVar()
        ttk.Radiobutton(right_frame, variable=red_player_type, value=1, text="Human").pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_choice, value=1, text="S").pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_choice, value=2, text="O").pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_type, value=2, text="Computer").pack(side=TOP)

        # Replay Button on bottom right
        ttk.Button(right_frame, text="Replay").pack(side=BOTTOM)

        # New Game Button on bottom right
        ttk.Button(right_frame, text="New Game", command=self.start_new_game).pack(side=BOTTOM)

        # Bottom Frame
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # Current Turn on bottom center
        ttk.Label(self.bottom_frame, text="Current turn:").pack(side=BOTTOM)
        ttk.Label(self.bottom_frame, textvariable=self.game_type).pack(side=BOTTOM)

        # Board Attribute
        self.sos_board = None

        # Execute GUI
        root.mainloop()

    def new_board(self):
        """ Creates a new board with specified user size"""
        try:
            if 2 < self.board_size.get() < 10:
                self.sos_board = Board(self.board_size.get(), self.cell_update)
                self.sos_board.place(anchor=CENTER, relx=.5, rely=.5)
            elif self.board_size.get() < 3:
                messagebox.showerror(title="Error", message="Board size must be greater than 2")
            elif self.board_size.get() > 9:
                messagebox.showerror(title="Error", message="Board size must be less than 9")
        except:
            messagebox.showerror(title="Error", message="Invalid input for board size, must be only numbers")

    def start_new_game(self):
        """ Starts a new game """
        self.new_board()

    def cell_update(self, cell):
        """ Updates cell with symbol"""
        symbol = self.blue_player_choice.get()
        cell.config(text=symbol, state=DISABLED, font=("Helvetica", 40))


# Main
if __name__ == '__main__': from tkinter import *
from tkinter import ttk, messagebox

from Board import Board


class SOS:
    def __init__(self):
        """ Initialize SOS game GUI """

        # Creates window
        root = Tk()
        root.geometry("800x600")
        root.title("SOS Game")
        # No ability to resize since component size don't scale
        root.resizable(width=False, height=False)

        # Top Frame
        top_frame = ttk.Frame(root)
        top_frame.pack(side=TOP, fill=X, pady=(0, 50))

        # SOS Label in top left
        ttk.Label(top_frame, text="SOS").pack(side=LEFT)

        # Radio buttons for game type next to SOS label
        self.game_type = StringVar(value="Simple Game")
        ttk.Radiobutton(top_frame, variable=self.game_type, value="Simple Game", text="Simple Game").pack(side=LEFT,
                                                                                                          anchor=NW)
        ttk.Radiobutton(top_frame, variable=self.game_type, value="General Game", text="General Game").pack(side=LEFT,
                                                                                                            anchor=NW)

        # Prompt to ask user for board size in upper right
        # Default value of 3
        self.board_size = IntVar(value=3)
        Entry(top_frame, width=2, textvariable=self.board_size).pack(side=RIGHT)

        # Board size prompt label
        Label(top_frame, text="Board Size").pack(side=RIGHT)

        # Left Frame
        left_frame = ttk.Frame(root)
        left_frame.pack(side=LEFT, fill=Y)

        # Blue player options (label and radio buttons) on left side

        ttk.Label(left_frame, text="Blue Player").pack(side=TOP)
        blue_player_type = IntVar(value=1)
        self.blue_player_choice = StringVar(value='S')
        ttk.Radiobutton(left_frame, variable=blue_player_type, value=1, text="Human").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=self.blue_player_choice, value='S', text="S").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=self.blue_player_choice, value='O', text="O").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=blue_player_type, value=2, text="Computer").pack(side=TOP)

        # Record game checkbox on bottom left
        ttk.Checkbutton(left_frame, text="Record").pack(side=BOTTOM)

        # Right Frame
        right_frame = ttk.Frame(root)
        right_frame.pack(side=RIGHT, fill=Y)

        # Red player options (label and radio buttons) on right side
        ttk.Label(right_frame, text="Red Player").pack(side=TOP)
        red_player_type = IntVar()
        red_player_choice = IntVar()
        ttk.Radiobutton(right_frame, variable=red_player_type, value=1, text="Human").pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_choice, value=1, text="S").pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_choice, value=2, text="O").pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_type, value=2, text="Computer").pack(side=TOP)

        # Replay Button on bottom right
        ttk.Button(right_frame, text="Replay").pack(side=BOTTOM)

        # New Game Button on bottom right
        ttk.Button(right_frame, text="New Game", command=self.start_new_game).pack(side=BOTTOM)

        # Bottom Frame
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # Current Turn on bottom center
        self.current_turn = ttk.Label(self.bottom_frame, text="Current turn:")
        self.current_turn.pack(side=BOTTOM)

        # Current game mode placeholder variable
        self.game_mode_label = ttk.Label(self.bottom_frame)
        self.game_mode_label.pack(side=BOTTOM)

        # Board Attribute
        self.sos_board = None

        # Execute GUI
        root.mainloop()

    def new_board(self):
        """ Creates a new board with specified user size"""
        try:
            # If board size is correct (n > 2 and n < 10)
            if 2 < self.board_size.get() < 10:
                # Make the board and pass cell function and game mode
                self.sos_board = Board(self.board_size.get(), self.cell_update, self.game_type.get())
                # Center the game board
                self.sos_board.place(anchor=CENTER, relx=.5, rely=.5)
            # If board size is n < 3 (too small)
            elif self.board_size.get() < 3:
                messagebox.showerror(title="Error", message="Board size must be greater than 2")
            # If board size is n > 10 (too large)
            elif self.board_size.get() > 9:
                messagebox.showerror(title="Error", message="Board size must be less than 9")
        # If an invalid input is entered (blank and non-integers)
        except:
            messagebox.showerror(title="Error", message="Invalid input for board size, must enter a number greater "
                                                        "than 3 and less than 9")

    def set_gamemode(self):
        """ Sets the game mode UI to the selected game mode """
        self.game_mode_label.config(text=f"Current Game Mode: {self.game_type.get()}")

    def start_new_game(self):
        """ Starts a new game """
        self.new_board()
        self.set_gamemode()
        self.current_turn.config(text="Current turn: Blue")

    def cell_update(self, cell):
        """ Updates cell with symbol"""
        symbol = self.blue_player_choice.get()
        # Adds the symbol ad disable the button to prevent any further changes
        cell.config(text=symbol, state=DISABLED, font=("Helvetica", 40))


# Main
if __name__ == '__main__':
    # Create SOS game object
    game = SOS()
