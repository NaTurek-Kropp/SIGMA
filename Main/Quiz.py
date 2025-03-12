import pygame
import Elements
import Data
import Surface
import Sub.Time as Time

surfaceElements = []
Questions = Data.GetQuestionsDataFixed("ProjectData\pytania.txt")
Answers = Data.Answers(Data.NumOfQuestions("ProjectData\pytania.txt"))
question = 0
answer = ""
images = []
timer = None

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
    global timer
    surfaceElements.clear()
    
    match surface:
        case "quiz":
            questionImage = [Questions[0][question][0], images[0][question]]
            answerImage = []
            timer = Time.StartTimer()

            for ans in Questions[1][question]:
                answerImage.append([ans[0], images[1][question]])

            surfaceElements = Surface.getQuizElements(answerFunc, nextQuestion, previousQuestion, questionImage, answerImage, question == len(Answers.Answers())-1)
        case "starting":
            surfaceElements = Surface.getStartingElements()
        case "ending":
            totalTime = 0
            for i in Time.TimeStamps():
                totalTime += i
            totalTime = round(totalTime)
            
            surfaceElements = Surface.getEndingElements(totalTime)

def answerFunc(newAnswer):
    global answer
    answer = newAnswer

def nextQuestion():
    global question
    global answer

    Answers.AppendAnswer(question, answer)
    Time.EndTimer(timer, question)
    if len(Answers.Answers())-1 > question:
        question+=1
        answer = Answers.Answers()[question]

        createSurface("quiz")
        Surface.setSelectedAnswer(answer)
    else:
        createSurface("ending")

def previousQuestion():
    global question
    global answer

    if question <= 0: return

    Time.EndTimer(timer, question)

    Answers.AppendAnswer(question, answer)
    question-=1
    answer = Answers.Answers()[question]

    createSurface("quiz")
    Surface.setSelectedAnswer(answer)

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