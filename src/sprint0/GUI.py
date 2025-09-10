from tkinter import ttk
from Board import *


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
        game_type = IntVar()
        ttk.Radiobutton(top_frame, variable=game_type, value=1, text="Simple Game").pack(side=LEFT, anchor=NW)
        ttk.Radiobutton(top_frame, variable=game_type, value=2, text="General Game").pack(side=LEFT, anchor=NW)

        # Prompt to ask user for board size in upper right
        Text(top_frame, height=1, width=2).pack(side=RIGHT)
        # Board size prompt label
        ttk.Label(top_frame, text="Board Size").pack(side=RIGHT)

        # Left Frame
        left_frame = ttk.Frame(root)
        left_frame.pack(side=LEFT, fill=Y)

        # Blue player options (label and radio buttons) on left side
        ttk.Label(left_frame, text="Blue Player").pack(side=TOP)
        blue_player_type = IntVar()
        blue_player_choice = IntVar()
        ttk.Radiobutton(left_frame, variable=blue_player_type, value=1, text="Human").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=blue_player_choice, value=1, text="S").pack(side=TOP)
        ttk.Radiobutton(left_frame, variable=blue_player_choice, value=2, text="O").pack(side=TOP)
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
        ttk.Button(right_frame, text="New Game").pack(side=BOTTOM)

        # Bottom Frame
        bottom_frame = ttk.Frame(root)
        bottom_frame.pack(side=BOTTOM, fill=X)

        # Current Turn on bottom center
        ttk.Label(bottom_frame, text="Current turn: blue (or red)").pack(side=BOTTOM)

        # Create game board in center
        s = Board(5, 5)
        s.place(anchor=CENTER, relx=.5, rely=.5)

        # Execute GUI
        root.mainloop()


# Main
if __name__ == '__main__':
    # Create SOS game object
    game = SOS()
