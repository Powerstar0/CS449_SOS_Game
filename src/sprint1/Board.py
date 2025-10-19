from tkinter import *


class Board(Canvas):
    def __init__(self, num_of_rows_and_columns):
        """ Initialize the number of rows and columns """

        # Inherit methods of Canvas class in Tkinter while providing some arguments
        super().__init__(height=450, width=450, borderwidth=0, highlightbackground="black")

        # Initialize row and column number variable
        self.num_of_rows_and_columns = num_of_rows_and_columns

        # Initialize game type (default = simple)
        self.game_type = "Simple"

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
