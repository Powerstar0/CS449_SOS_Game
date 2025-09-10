from tkinter import *


class Board(Canvas):
    def __init__(self, num_rows, num_columns):
        """ Initialize the number of rows and columns """
        # Inherit methods of Canvas class in Tkinter
        super().__init__(height=450, width=450, borderwidth=0, highlightbackground="black")
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.paint_component()

    def paint_component(self):
        """ Draws the board based on the number of rows and columns specified """
        height = self.winfo_reqheight()
        width = self.winfo_reqwidth()
        print(height, width)

        col_width = width / self.num_columns
        row_height = height / self.num_rows

        for i in range(self.num_rows):
            self.create_line(0, row_height * i, col_width * self.num_columns, row_height * i)

        for i in range(self.num_columns):
            self.create_line(col_width * i, 0, col_width * i, row_height * self.num_rows)



