from tkinter import *
from tkinter import ttk
import Game_Logic


class Board(Canvas):
    def __init__(self, num_of_rows_and_columns, cell_update_function):
        """ Initialize the number of rows and columns """

        # Inherit methods of Canvas class in Tkinter while providing some arguments
        super().__init__(height=450, width=450, borderwidth=0, highlightbackground="black")

        # Initialize row and column number variable
        self.num_of_rows_and_columns = num_of_rows_and_columns

        # Initialize game type (default = simple)
        self.game_type = "Simple"

        # Create pixel instance for cell size later (needed for pixel sizing of buttons)
        self.pixel = PhotoImage()

        # Matrix to store cells
        self.cell_matrix = []

        # cell update function
        self.cell_update_function = cell_update_function

        # Start Board
        self.new_game()

    # Start a new game
    def new_game(self):
        # Call the draw function
        self.paint_component()

    def paint_component(self):
        """ Draws the board based on the number of rows and columns specified """

        # Get the height and width of widget
        height = self.winfo_reqheight()
        width = self.winfo_reqwidth()

        # Get the column width and height based off of the number of columns and rows
        col_width = width / self.num_of_rows_and_columns
        row_height = height / self.num_of_rows_and_columns

        # Draw each row
        for i in range(self.num_of_rows_and_columns):
            self.create_line(0, row_height * i, col_width * self.num_of_rows_and_columns, row_height * i)

        # Draw each column
        for i in range(self.num_of_rows_and_columns):
            self.create_line(col_width * i, 0, col_width * i, row_height * self.num_of_rows_and_columns)

        # Add Buttons to each empty cell
        for row in range(self.num_of_rows_and_columns):
            row_buttons = []
            for column in range(self.num_of_rows_and_columns):
                cell_button = Button(self, text='', width=col_width, height=row_height, relief="solid",
                                     image=self.pixel, compound="center", )
                cell_button.config(command=lambda b=cell_button: self.cell_update_function(b))
                row_buttons.append(cell_button)
                button_window = self.create_window(row * row_height + (row_height / 2),
                                                   column * col_width + (col_width / 2), anchor='center',
                                                   window=cell_button)
            self.cell_matrix.append(row_buttons)

    def set_game_mode(self, game_mode):
        self.game_type = game_mode


