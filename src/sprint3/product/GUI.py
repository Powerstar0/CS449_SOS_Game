# Main
from Game_Logic import *
from tkinter import ttk


class SOS:
    def __init__(self):
        """ Initialize SOS game GUI """

        self.current_turn = 0

        # Creates window
        root = Tk()
        root.geometry("800x600")
        root.title("SOS Game")
        # No ability to resize since component size don't scale
        root.resizable(width=False, height=False)

        # Create blue and red player classes
        blue_player = Player()
        red_player = Player()

        # Top Frame
        top_frame = ttk.Frame(root)
        top_frame.pack(side=TOP, fill=X, pady=(0, 50))

        # SOS Label in top left
        ttk.Label(top_frame, text="SOS").pack(side=LEFT)

        # Create the board game logic instance (containing function to make the board)
        self.boardgame = SOSGameBase(blue_player, red_player)

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
        self.left_frame = ttk.Frame(root)
        self.left_frame.pack(side=LEFT, fill=Y)

        # Blue player options (label and radio buttons) on left side

        ttk.Label(self.left_frame, text="Blue Player").pack(side=TOP)
        blue_player_type = StringVar(value="Human")
        blue_player_choice = StringVar(value='S')
        ttk.Radiobutton(self.left_frame, variable=blue_player_type, value="Human", text="Human").pack(side=TOP)
        ttk.Radiobutton(self.left_frame, variable=blue_player_choice, value='S', text="S",
                        command=lambda symbol='S': blue_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(self.left_frame, variable=blue_player_choice, value='O', text="O",
                        command=lambda symbol='O': blue_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(self.left_frame, variable=blue_player_type, value="Computer", text="Computer").pack(side=TOP)

        # Record game checkbox on bottom left
        ttk.Checkbutton(self.left_frame, text="Record").pack(side=BOTTOM)

        # Right Frame
        self.right_frame = ttk.Frame(root)
        self.right_frame.pack(side=RIGHT, fill=Y)

        # Red player options (label and radio buttons) on right side
        ttk.Label(self.right_frame, text="Red Player").pack(side=TOP)
        red_player_type = StringVar(value="Human")
        red_player_choice = StringVar(value='S')
        ttk.Radiobutton(self.right_frame, variable=red_player_type, value="Human", text="Human").pack(side=TOP)
        ttk.Radiobutton(self.right_frame, variable=red_player_choice, value='S', text="S",
                        command=lambda symbol='S': red_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(self.right_frame, variable=red_player_choice, value='O', text="O",
                        command=lambda symbol='O': red_player.symbol_update(symbol)).pack(side=TOP)
        ttk.Radiobutton(self.right_frame, variable=red_player_type, value="Computer", text="Computer").pack(side=TOP)

        # Replay Button on bottom right
        ttk.Button(self.right_frame, text="Replay").pack(side=BOTTOM)

        # New Game Button on bottom right
        ttk.Button(self.right_frame, text="New Game", command=self.start_new_game).pack(side=BOTTOM)

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

        self.blue_score_label_text = Label(self.left_frame, text="Blue Player Score:")
        self.blue_score_label = ttk.Label(self.left_frame, textvariable=self.boardgame.blue_player.score)

        self.red_score_label_text = Label(self.right_frame, text="Red Player Score:")
        self.red_score_label = ttk.Label(self.right_frame, textvariable=self.boardgame.red_player.score)

        # Execute GUI
        root.mainloop()

    def start_new_game(self):
        """ Starts a new game """
        # Sets board size based on radio buttons
        self.boardgame.turn.set("Current Turn: Blue")
        self.boardgame.board_size = self.board_size.get()
        self.turn_label.pack(side=BOTTOM)
        # Hide Player score labels
        self.blue_score_label.pack_forget()
        self.red_score_label.pack_forget()
        self.blue_score_label_text.pack_forget()
        self.red_score_label_text.pack_forget()
        try:
            # Reset SOS sequence list
            self.boardgame.complete_sos_list = []
            # Convert the Base Game Template to either Simple Game
            if self.boardgame.game_type.get() == "Simple Game":
                self.boardgame = SimpleSOSGame(self.boardgame, self.boardgame.blue_player, self.boardgame.red_player)
            # Convert the Base Game Template to either General Game
            elif self.boardgame.game_type.get() == "General Game":
                self.boardgame = GeneralSOSGame(self.boardgame, self.boardgame.blue_player, self.boardgame.red_player)
                self.blue_score_label_text.pack(side=TOP)
                self.red_score_label_text.pack(side=TOP)
                self.blue_score_label.pack(side=TOP)
                self.red_score_label.pack(side=TOP)

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
