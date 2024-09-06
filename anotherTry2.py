import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# User defines number of rows and columns
rows = int(input("Enter number of rows: "))
cols = int(input("Enter number of columns: "))

# Load image
image_path = "dalicanva.jpg"
image = pygame.image.load(image_path)

# Define screen size and setup
screen_width, screen_height = image.get_width(), image.get_height()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Puzzle Game")


# Function to create puzzle piece shapes (custom shapes)
def create_puzzle_pieces(image, rows, cols):
    piece_width = image.get_width() // cols
    piece_height = image.get_height() // rows

    pieces = []
    for row in range(rows):
        for col in range(cols):
            # Create a surface for each puzzle piece with transparency support
            piece = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)
            piece.blit(image, (0, 0), (col * piece_width, row * piece_height, piece_width, piece_height))

            # Create mask for puzzle shape
            mask = pygame.Surface((piece_width, piece_height), pygame.SRCALPHA)
            mask.fill((0, 0, 0, 0))  # Make the surface transparent

            # Define your puzzle piece shapes here
            # You can add tabs and indentations using bezier curves or arcs
            # Here's a very basic example of how to draw tabs and cutouts
            # You can customize this to be more intricate
            pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, piece_width, piece_height))  # Full rectangle
            # Add tabs and cutouts using arcs or bezier curves:
            if col > 0:
                pygame.draw.circle(mask, (0, 0, 0, 0), (0, piece_height // 2), piece_height // 5)  # Left cutout
            if row > 0:
                pygame.draw.circle(mask, (0, 0, 0, 0), (piece_width // 2, 0), piece_width // 5)  # Top cutout
            if col < cols - 1:
                pygame.draw.circle(mask, (255, 255, 255, 255), (piece_width, piece_height // 2),
                                   piece_height // 5)  # Right tab
            if row < rows - 1:
                pygame.draw.circle(mask, (255, 255, 255, 255), (piece_width // 2, piece_height),
                                   piece_width // 5)  # Bottom tab

            # Apply the mask to the puzzle piece
            piece.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)

            piece_rect = piece.get_rect()

            # Append the shaped puzzle piece and its rect to the pieces list
            pieces.append((piece, piece_rect))

    return pieces


# Main game loop
def game_loop():
    pieces = create_puzzle_pieces(image, rows, cols)

    # Shuffle pieces just once before entering the game loop
    random.shuffle(pieces)

    # Random initial placement of the pieces
    for i, (piece, rect) in enumerate(pieces):
        rect.topleft = (random.randint(0, screen_width - rect.width), random.randint(0, screen_height - rect.height))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        # Display puzzle pieces in their shuffled positions
        for piece, rect in pieces:
            screen.blit(piece, rect.topleft)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game_loop()
