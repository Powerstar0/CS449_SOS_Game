from tkinter import *


class Board(Canvas):
    def __init__(self, num_of_rows_and_columns, cell_update_function):
        """ Initialize the number of rows and columns """

        # Inherit methods of Canvas class in Tkinter while providing some arguments
        super().__init__(height=450, width=450, borderwidth=0, highlightbackground="black")

        # Initialize row and column number variable
        self.num_of_rows_and_columns = num_of_rows_and_columns

        # Create pixel instance for cell size later (needed for pixel sizing of buttons)
        self.pixel = PhotoImage()

        # Matrix to store cells
        self.cell_matrix = []

        # cell update function
        self.cell_update_function = cell_update_function

        # Start Board
        self.new_game()

        self.column_width = 0
        self.row_height = 0

        self.overlay = None

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
        self.col_width = width / self.num_of_rows_and_columns
        self.row_height = height / self.num_of_rows_and_columns

        # Add Buttons to each empty cell
        for row in range(self.num_of_rows_and_columns):
            # Store buttons in matrix for game logic
            row_buttons = []
            for column in range(self.num_of_rows_and_columns):
                # Create cell button
                cell_button = Button(self, text='', width=self.col_width, height=self.row_height, relief="solid",
                                     image=self.pixel, compound="center")
                # Call the cell update function when clicked
                cell_button.config(command=lambda b=cell_button: self.cell_update_function(b))
                # Add button to the row button
                row_buttons.append(cell_button)
                # Create the window for the button in each cell location
                button_window = self.create_window(row * self.row_height + (self.row_height / 2),
                                   column * self.col_width + (self.col_width / 2), anchor='center',
                                   window=cell_button)
                self.tag_lower(button_window)
            # Add row buttons to overall matrix
            self.cell_matrix.append(row_buttons)

        # Overlay Canvas to draw the winning line
        self.overlay = Canvas(self,
                              width=self.winfo_width(),
                              height=self.winfo_height(),
                              bg=self['bg'],
                              highlightthickness=0)

        # Embed overlay in the Canvas above buttons
        self.overlay_window = self.create_window(0, 0, anchor='nw', window=self.overlay)

        self.overlay.create_line(10, 30, self.winfo_width() - 10, 30, width=6, fill="red")

    def draw_sos_line(self, row):
        line = self.create_line(0, self.row_height * row , self.col_width * self.num_of_rows_and_columns, self.row_height * row, fill="red")
        line_id = self.create_line(10, 10, 290, 290, width=5, fill="red")
        self.tag_raise(line_id)


