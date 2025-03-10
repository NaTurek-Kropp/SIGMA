import pygame
import Elements
import Data
import Surface

surfaceElements = []
Questions = Data.GetQuestionsDataFixed("Data\pytania.txt")
Answers = Data.Answers(Data.NumOfQuestions("Data\pytania.txt"))
question = 0
answer = ""
images = []

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
    surfaceElements.clear()
    
    match surface:
        case "quiz":
            questionImage = [Questions[0][question], images[0][question]]
            answerImage = [Questions[1][question], images[1][question]]
            surfaceElements = Surface.getQuizElements(answerFunc, nextQuestion, previousQuestion, questionImage, answerImage)
        case "starting":
            surfaceElements = Surface.getStartingElements()
        case "ending":
            surfaceElements = Surface.getEndingElements()

def answerFunc(newAnswer):
    global answer
    answer = newAnswer

def nextQuestion():
    global question
    global answer

    Answers.AppendAnswer(question, answer)
    question+=1
    answer = ""
    
    createSurface("quiz")

def previousQuestion():
    global question
    global answer

    Answers.AppendAnswer(question, answer)
    question-=1
    answer = ""

    createSurface("quiz")

def preloadAllImages():
    questions = []
    for i in Questions[0]:
        if not i[1]: continue
        questions.append(Elements.PreloadImage(i[1]))

    answers = []
    for qa in Questions[1]:
        currAnswers = []
        for i in qa:
            if not i[1]: continue
            currAnswers.append(Elements.PreloadImage(i[1]))
        answers.append(currAnswers)

    images.append(questions)
    images.append(answers)

preloadAllImages()

main()