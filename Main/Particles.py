import pygame

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (30, 30, 30)
FPS = 60
SPAWN_INTERVAL = 1000  # Time in milliseconds between new circles
CIRCLE_THICKNESS = 10  # Thickness of the circle outline

# Circle class
class ExpandingCircle:
    def __init__(self, x, y, growth_rate=.5):
        self.x = x
        self.y = y
        self.radius = 10
        self.growth_rate = growth_rate
        self.color = (255, 255, 255)

    def update(self):
        self.radius += self.growth_rate

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius, CIRCLE_THICKNESS)

# Main function
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Expanding Circles Animation")
    clock = pygame.time.Clock()
    circles = []
    running = True
    last_spawn_time = pygame.time.get_ticks()
    
    while running:
        screen.fill(BACKGROUND_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Add new circle at set intervals
        current_time = pygame.time.get_ticks()
        if current_time - last_spawn_time >= SPAWN_INTERVAL:
            circles.append(ExpandingCircle(WIDTH // 2, HEIGHT // 2))
            last_spawn_time = current_time
        
        for circle in circles[:]:
            circle.update()
            circle.draw(screen)
            if circle.radius > max(WIDTH, HEIGHT):
                circles.remove(circle)

        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
