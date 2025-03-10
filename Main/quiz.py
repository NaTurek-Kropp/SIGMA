import pygame
import Elements
import Data
import Surface

surfaceElements = []
Answers = Data.Answers()

def main():
    pygame.init()

    screen = pygame.display.set_mode((1500, 1000))
    clock = pygame.time.Clock()
    running = True

    createSurface("quiz")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()

                for button in surfaceElements:
                    if not isinstance(button, Elements.Button): continue
                    if button.getRect().collidepoint(mousePos):
                        button.pressed()

        screen.fill("white")

        for element in surfaceElements:
            element.tick()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def createSurface(surface: str):
    global surfaceElements
    
    match surface:
        case "quiz":
            surfaceElements = Surface.getQuizElements(answer)
        case "starting":
            surfaceElements = Surface.getStartingElements()
        case "ending":
            surfaceElements = Surface.getEndingElements()

def answer(answer):
    global Answers
    Answers.appendAnswer(answer)
    print(answer)

main()