import pygame
import elements
import Data

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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()

                for button in surfaceElements:
                    if not isinstance(button, elements.Button): continue
                    if button.getRect().collidepoint(mousePos):
                        print(mousePos, button)
                        button.pressed()

        screen.fill("white")

        for element in surfaceElements:
            element.tick()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def answer(answer):
    Data.Answers.appendAnswer(answer)

def createQuizElements():
    clearSurfaceElements()

    quizFrame = elements.Rect(color="blue", sizeScale=(.9, .2), positionScale=(0, 0.05), align="top", anchor="top")
    surfaceElements.append(quizFrame)

    image = elements.Image(url="https://www.pygame.org/docs/_static/pygame_tiny.png", factor="height", sizeScale=(0, 0.3), positionScale=(0, 0.3), align="top", anchor="top")
    surfaceElements.append(image)

    button1 = elements.Button(color="red", text=elements.Text("A", "arial", 50), command=lambda: answer("A"), sizeScale=(.4, .125), positionScale=(0.05, 0.7))
    button2 = elements.Button(color="red", text=elements.Text("B", "arial", 50), command=lambda: answer("B"), sizeScale=(.4, .125), positionScale=(0.55, 0.7))
    button3 = elements.Button(color="red", text=elements.Text("C", "arial", 50), command=lambda: answer("C"), sizeScale=(.4, .125), positionScale=(0.05, 0.85))
    button4 = elements.Button(color="red", text=elements.Text("D", "arial", 50), command=lambda: answer("D"), sizeScale=(.4, .125), positionScale=(0.55, 0.85))
    surfaceElements.append(button1)
    surfaceElements.append(button2)
    surfaceElements.append(button3)
    surfaceElements.append(button4)

def clearSurfaceElements():
    surfaceElements.clear()

main()