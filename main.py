import tkinter as tk
from tkinter import filedialog, PhotoImage
import random

# Configuration
GRID_SIZE = 2  # Number of rows and columns in the puzzle
PIECE_SIZE = 100  # Size of each puzzle piece (in pixels)
max_width, max_height = 800, 800  # Adjust as needed
THRESHOLD = 50  # Threshold for win condition


class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Puzzle Game")
        self.canvas = tk.Canvas(root, width=GRID_SIZE * PIECE_SIZE, height=GRID_SIZE * PIECE_SIZE)
        self.canvas.pack()
        self.pieces = []
        self.real_positions = {}
        self.current_positions = {}
        self.canvas_items = {}
        self.selected_piece = None
        self.load_button = tk.Button(root, text="Upload Image", command=self.upload_image)
        self.load_button.pack(pady=20)
        self.valid_positions = self.create_valid_positions()
        self.is_winning = False

    def create_valid_positions(self):
        # Create a list of valid positions (top-left corners of each grid cell)
        valid_positions = []
        for x in range(max_width):
            for y in range(max_height):
                valid_positions.append((x, y))
        return valid_positions

    def upload_image(self):
        # Prompt user to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
        if not file_path:
            return

        # Load the image using Tkinter's PhotoImage
        original_image = tk.PhotoImage(file=file_path)

        # Resize the image while maintaining the aspect ratio
        scale_factor = min(max_width / original_image.width(), max_height / original_image.height())
        new_width = int(original_image.width() * scale_factor)
        new_height = int(original_image.height() * scale_factor)

        # Create a new PhotoImage for the resized image
        resized_image = tk.PhotoImage(width=new_width, height=new_height)

        # Copy and resize the original image into the resized image
        resized_image.tk.call(resized_image, 'copy', original_image, '-from',
                                0, 0, original_image.width(), original_image.height(),
                                '-to', 0, 0)
        # Update the canvas size to match the resized image
        self.canvas.config(width=new_width, height=new_height)
        self.image = self.crop_image(resized_image, new_width, new_height)
        self.split_image()
        self.shuffle_pieces()
        self.draw_pieces()

    def crop_image(self, image, width, height):
        # Create a new PhotoImage object for the cropped image
        cropped_image = tk.PhotoImage(width=width, height=height)

        # Copy the cropped region into the new image
        cropped_image.tk.call(cropped_image, 'copy', image, '-from',
                              0, 0, width, height,
                              '-to', 0, 0)
        return cropped_image

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

                # Store real_positions for possible use
                self.real_positions[piece] = (col * piece_width, row * piece_height)

    def shuffle_pieces(self):
        # Get a list of real_positions
        positions = list(self.real_positions.values())

        # Shuffle the real_positions
        random.shuffle(positions)

        # Assign the shuffled real_positions back to the pieces
        # This keeps the pieces in their original order but randomizes where they are placed
        for i, piece in enumerate(self.pieces):
            self.current_positions[piece] = positions[i]

    def draw_pieces(self):
        if self.is_winning:
            self.canvas.delete("all")
            self.canvas.create_text(300, 300, text="You Win!", font=("Helvetica", 100), fill="green")
            return
        # Draw the pieces on the canvas
        self.canvas.delete("all")
        self.canvas_items.clear()
        for piece in self.pieces:
            x, y = self.current_positions[piece]
            item_id = self.canvas.create_image(x, y, anchor='nw', image=piece, tags="piece")
            self.canvas_items[item_id] = piece
        self.canvas.tag_bind("piece", "<Button-1>", self.on_piece_click)
        self.canvas.tag_bind("piece", "<B1-Motion>", self.on_piece_drag)
        self.canvas.tag_bind("piece", "<ButtonRelease-1>", self.on_piece_release)

    def on_piece_click(self, event):
        # Find the piece under the click
        piece = self.canvas.find_closest(event.x, event.y)
        self.selected_piece = piece[0]
        self.canvas.tag_raise(self.selected_piece)

    def on_piece_drag(self, event):
        # Move the selected piece with the mouse
        if self.selected_piece:
            self.canvas.coords(self.selected_piece, event.x, event.y)

    def on_piece_release(self, event):
        # Release the piece and snap it to the nearest valid position
        if self.selected_piece:
            piece_coords = event.x, event.y
            closest_position = min(self.valid_positions, key=lambda pos: self.distance(pos, piece_coords))
            self.canvas.coords(self.selected_piece, closest_position)
            arg = self.canvas_items[self.selected_piece]
            self.pieces.remove(arg)
            self.pieces.append(arg)
            self.current_positions[arg] = closest_position
            self.selected_piece = None
            self.check_win()
            self.draw_pieces()

    def distance(self, pos1, pos2):
        # Calculate the Euclidean distance between two points
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def check_win(self):
        # Check if the pieces are in the correct positions
        if all(self.distance(self.current_positions[piece], self.real_positions[piece]) < THRESHOLD
               for piece in self.pieces):
            self.is_winning = True


# Create the main window and start the game
root = tk.Tk()
game = PuzzleGame(root)
root.mainloop()
