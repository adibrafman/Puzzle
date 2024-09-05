import tkinter as tk
from tkinter import filedialog, PhotoImage
import random

# Configuration
GRID_SIZE = 5  # Number of rows and columns in the puzzle
PIECE_SIZE = 100  # Size of each puzzle piece (in pixels)


class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Puzzle Game")
        self.canvas = tk.Canvas(root, width=GRID_SIZE * PIECE_SIZE, height=GRID_SIZE * PIECE_SIZE)
        self.canvas.pack()
        self.pieces = []
        self.positions = {}
        self.selected_piece = None
        self.load_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.load_button.pack(pady=20)

    def upload_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("GIF Images", "*.gif")])
        if file_path:
            # Load and split the image into pieces
            self.image = PhotoImage(file=file_path)
            self.split_image()
            self.shuffle_pieces()
            self.draw_pieces()

    def split_image(self):
        # Split the image into GRID_SIZE x GRID_SIZE pieces
        self.pieces = []
        piece_width = self.image.width() // GRID_SIZE
        piece_height = self.image.height() // GRID_SIZE
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                # Create each piece as a new PhotoImage by subsampling the image
                # Use 'subsample' and 'zoom' for scaling purposes if exact cropping is not feasible
                piece = tk.PhotoImage(width=piece_width, height=piece_height)

                # Copy part of the image onto the piece
                piece.tk.call(piece, 'copy', self.image, '-from',
                              col * piece_width, row * piece_height,
                              (col + 1) * piece_width, (row + 1) * piece_height,
                              '-to', 0, 0)

                self.pieces.append(piece)

                # Store positions for possible use
                self.positions[piece] = (col * piece_width, row * piece_height)

    def shuffle_pieces(self):
        # Shuffle the pieces to random positions
        random.shuffle(self.pieces)

    def draw_pieces(self):
        # Draw the pieces on the canvas
        self.canvas.delete("all")
        for piece in self.pieces:
            x, y = self.positions[piece]
            self.canvas.create_image(x, y, anchor='nw', image=piece, tags="piece")
        self.canvas.tag_bind("piece", "<Button-1>", self.on_piece_click)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.on_piece_drag)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>", self.on_piece_release)

    def on_piece_click(self, event):
        # Find the piece under the click
        piece = self.canvas.find_closest(event.x, event.y)
        self.selected_piece = piece

    def on_piece_drag(self, event):
        # Move the selected piece with the mouse
        if self.selected_piece:
            self.canvas.coords(self.selected_piece, event.x, event.y)

    def on_piece_release(self, event):
        # Release the piece and snap it to the grid
        if self.selected_piece:
            closest_piece = self.canvas.find_closest(event.x, event.y)[0]
            current_coords = self.canvas.coords(closest_piece)
            snapped_coords = (round(current_coords[0] / PIECE_SIZE) * PIECE_SIZE,
                              round(current_coords[1] / PIECE_SIZE) * PIECE_SIZE)
            self.canvas.coords(closest_piece, snapped_coords)
            self.selected_piece = None


# Create the main window and start the game
root = tk.Tk()
game = PuzzleGame(root)
root.mainloop()
