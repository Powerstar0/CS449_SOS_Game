# Main
from Game_Logic import *
from tkinter import ttk


class SOS:
    def __init__(self):
        """ Initialize SOS game GUI """

        # Create blue and red player classes
        blue_player = Player()
        red_player = Player()


        self.current_turn = 0

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

        # Create the board game logic instance (containing function to make the board)
        self.boardgame = BoardLogic(blue_player, red_player)

        # Radio buttons for game type next to SOS label
        self.boardgame.game_type = StringVar(value="Simple Game")
        ttk.Radiobutton(top_frame, variable=self.boardgame.game_type, value="Simple Game", text="Simple Game").pack(
            side=LEFT,
            anchor=NW)
        ttk.Radiobutton(top_frame, variable=self.boardgame.game_type, value="General Game", text="General Game").pack(
            side=LEFT,
            anchor=NW)

        # Prompt to ask user for board size in upper right
        self.board_size = IntVar(value=3)
        Entry(top_frame, width=2, textvariable=self.board_size).pack(side=RIGHT)

        # Board size prompt label
        Label(top_frame, text="Board Size").pack(side=RIGHT)

        # Left Frame
        left_frame = ttk.Frame(root)
        left_frame.pack(side=LEFT, fill=Y)

        # Blue player options (label and radio buttons) on left side

        ttk.Label(left_frame, text="Blue Player").pack(side=TOP)
        blue_player_type = StringVar(value="Human")
        blue_player_choice = StringVar(value='S')
        ttk.Radiobutton(left_frame, variable=blue_player_type, value="Human", text="Human").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=blue_player_choice, value='S', text="S",
                        command=lambda symbol='S': blue_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=blue_player_choice, value='O', text="O",
                        command=lambda symbol='O': blue_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=blue_player_type, value="Computer", text="Computer").pack(side=TOP)

        # Record game checkbox on bottom left
        ttk.Checkbutton(left_frame, text="Record").pack(side=BOTTOM)

        # Right Frame
        right_frame = ttk.Frame(root)
        right_frame.pack(side=RIGHT, fill=Y)

        # Red player options (label and radio buttons) on right side
        ttk.Label(right_frame, text="Red Player").pack(side=TOP)
        red_player_type = StringVar(value="Human")
        red_player_choice = StringVar(value='S')
        ttk.Radiobutton(right_frame, variable=red_player_type, value="Human", text="Human").pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_choice, value='S', text="S", command=lambda symbol='S': red_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_choice, value='O', text="O", command=lambda symbol='O': red_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(right_frame, variable=red_player_type, value="Computer", text="Computer").pack(side=TOP)

        # Replay Button on bottom right
        ttk.Button(right_frame, text="Replay").pack(side=BOTTOM)

        # New Game Button on bottom right
        ttk.Button(right_frame, text="New Game", command=self.start_new_game).pack(side=BOTTOM)

        # Bottom Frame
        self.bottom_frame = ttk.Frame(root)
        self.bottom_frame.pack(side=BOTTOM, fill=X)

        # Current Turn on bottom center
        self.turn_label = ttk.Label(self.bottom_frame, textvariable=self.boardgame.turn)

        # Current game mode placeholder variable
        self.game_mode_label = ttk.Label(self.bottom_frame)
        self.game_mode_label.pack(side=BOTTOM)

        # Board Attribute
        self.sos_board = None

        # Execute GUI
        root.mainloop()

    def start_new_game(self):
        """ Starts a new game """
        # Sets board size based on radio buttons
        self.boardgame.turn.set("Current Turn: Blue")
        self.boardgame.board_size = self.board_size.get()
        self.turn_label.pack(side=BOTTOM)
        try:
            # Create board instance
            board = self.boardgame.new_board()
            # Center the game board
            board.place(anchor=CENTER, relx=.5, rely=.5)
            # Displays current game mode
            self.game_mode_label.config(text=f"Current Game Mode: {self.boardgame.game_type.get()}")
        except (Exception,):
            # If any errors occur, skip execution
            pass



# Main
if __name__ == '__main__':
    # Create SOS game object
    game = SOS()
