import pygame
import Elements
import Data
import Surface

surfaceElements = []
Questions = Data.GetQuestionsDataFixed("Data\pytania.txt")
Answers = Data.Answers(Data.NumOfQuestions("Data\pytania.txt"))
question = 0

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
            surfaceElements = Surface.getQuizElements(answer, Questions[0][question], Questions[1][question])
        case "starting":
            surfaceElements = Surface.getStartingElements()
        case "ending":
            surfaceElements = Surface.getEndingElements()

def answer(answer):
    global Answers
    global question
    Answers.AppendAnswer(question, answer)

def nextQuestion():
    global question
    question+=1
    createSurface("quiz")

def previousQuestion():
    global question
    question-=1
    createSurface("quiz")

main()