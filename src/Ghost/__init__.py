import pygame

class Ghost:
    def __init__(self, x, y, speed, image_path):
        """
        Initialize a Ghost object.

        Args:
            x (int): X-coordinate of the ghost's starting position.
            y (int): Y-coordinate of the ghost's starting position.
            speed (int): Speed at which the ghost moves horizontally.
            image_path (str): Path to the ghost's image file.
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()

    def move(self):
        """
        Move the ghost horizontally.

        The ghost's position is updated based on its speed.
        """
        self.x += self.speed  # Move horizontally 

    def draw(self, screen):
        """
        Draw the ghost on the screen.

        Args:
            screen (pygame.Surface): The surface on which the ghost is drawn.
        """
        screen.blit(self.image, (self.x, self.y))

# Example usage:
pygame.init()

# Set up game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()

# Create a ghost object
ghost_image_path = "path_to_ghost_image.png"
ghost = Ghost(100, 300, 2, ghost_image_path)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game objects
    ghost.move()

    # Draw everything
    SCREEN.fill((255, 255, 255))  # Fill the screen with white color
    ghost.draw(SCREEN)  # Draw the ghost

    pygame.display.flip()  # Update the display
    CLOCK.tick(60)  # Limit frames per second

# Clean up
pygame.quit()
