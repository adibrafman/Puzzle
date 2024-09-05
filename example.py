import pygame
import os

# Pygame setup
pygame.init()

# Load the image you want to cut the puzzle shape from
image_path = "dalicanva.jpg"  # Replace this with the path to your image
puzzle_mask_path = "puzzle_shape.png"  # The mask of the puzzle shape

# Ensure the window is centered
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Set up the screen
screen = pygame.display.set_mode((1280, 720))

# Load the image and the puzzle mask
image = pygame.image.load(image_path).convert_alpha()  # Ensure transparency
mask = pygame.image.load(puzzle_mask_path).convert_alpha()  # The mask should have transparency

# Resize both the image and mask to the same size
image = pygame.transform.scale(image, (300, 300))  # Resize the image if necessary
mask = pygame.transform.scale(mask, (300, 300))  # Resize the mask to match the image size

# Create a new surface for the masked image
masked_image = pygame.Surface((300, 300), pygame.SRCALPHA)

# Apply the mask to the image
for x in range(mask.get_width()):
    for y in range(mask.get_height()):
        mask_pixel = mask.get_at((x, y))
        if mask_pixel[3] > 0:  # Non-transparent pixel
            image_pixel = image.get_at((x, y))
            masked_image.set_at((x, y), image_pixel)

# Display the masked image on the screen
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))  # Clear the screen with a white background
    screen.blit(masked_image, (100, 100))  # Blit the masked image at a position
    pygame.display.flip()  # Update the display

# Quit Pygame
pygame.quit()