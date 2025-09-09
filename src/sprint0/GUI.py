from tkinter import *
from tkinter import ttk


class SOS:
    def __init__(self):
        """ Initialize SOS game and GUI """
        # Creates window and sizes it
        root = Tk()
        root.geometry("800x600")
        root.title("SOS Game")
        root.configure(bg="white")
        # Creates a grid frame from widget
        frame = ttk.Frame(root, padding=10)
        frame.grid()
        # SOS Label in top left
        ttk.Label(frame, text="SOS").grid(column=0, row=0)
        # Variable ensures only one game type is selected
        game_type = IntVar()
        ttk.Radiobutton(frame, variable=game_type, value=1, text="Simple Game").grid(column=1, row=0)
        ttk.Radiobutton(frame, variable=game_type, value=2, text="General Game").grid(column=2, row=0)
        # Board Size Prompt
        ttk.Label(frame, text="Board Size").grid(column=3, row=0, padx=(420,0))
        # Get user board size here
        Text(frame, height=1, width=2).grid(column=4, row=0)
        # Blue player options
        ttk.Radiobutton()
        # Execute GUI
        root.mainloop()


# Main
if __name__ == '__main__':
    # Create SOS game object
    game = SOS()
