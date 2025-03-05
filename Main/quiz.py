import pygame
import elements

surfaceElements = []

def main():
    pygame.init()

    screen = pygame.display.set_mode((1500, 1000))
    clock = pygame.time.Clock()
    running = True

    createQuizElements()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")

        for element in surfaceElements:
            element.tick()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def createQuizElements():
    clearSurfaceElements()

    quizFrame = elements.Rect(color="blue", sizeScale=(.9, .2), positionScale=(0, 0.05), align="top", anchor="top")
    surfaceElements.append(quizFrame)

    image = elements.Image("https://www.pygame.org/docs/_static/pygame_tiny.png", "height", sizeScale=(0, 0.3), positionScale=(0, 0.3), align="top", anchor="top")
    surfaceElements.append(image)

def clearSurfaceElements():
    surfaceElements.clear()

main()