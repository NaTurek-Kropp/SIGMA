import pygame
import Elements
import Data
import Surface
import Sub.Time as Time
import Send
from ProjectData import Settings
import threading
import Main.X.Online as Online

global surfaceElements, Questions, Answers, question, answer, images, timer
surfaceElements = []
Questions = Data.GetQuestionsDataFixed("ProjectData\\pytania.txt")
Answers = Data.Answers(Data.NumOfQuestions("ProjectData\\pytania.txt"))
question = 0
answer = ""
images = []
timer = None

def main():
    pygame.init()
    screen = pygame.display.set_mode((1500, 1000))
    clock = pygame.time.Clock()
    running = True
    createSurface("starting")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for button in surfaceElements:
                    if isinstance(button, Elements.Button) and button.getRect().collidepoint(mousePos):
                        button.pressed()
        
        screen.fill("white")
        for element in surfaceElements:
            element.tick()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def createSurface(surface_name: str):
    global surfaceElements, timer, question, answer
    surfaceElements.clear()

    if surface_name == "quiz":
        if Online.online:
            Online.setRound()
        
        questionImage = [Questions[0][question][0], images[0][question]]
        answerImage = []
        timer = Time.StartTimer()
        
        for indx, ans in enumerate(Questions[1][question]):
            img = images[1][question][indx] if images[1][question] else None
            answerImage.append([ans[0], img])

        surfaceElements = Surface.getQuizElements(answerFunc, nextQuestion, previousQuestion, questionImage, answerImage, question == len(Answers.Answers())-1)
    #    if Online.online:
    #        Online.start_game_online()
    #        threading.Thread(target=Online.check_submit_updates, daemon=True).start()
    
    #elif surface_name == "lobby":
    #    Online.create_lobby()
    #    surfaceElements = Surface.getLobbyElements(Online.lobby_code, [], lambda: createSurface("quiz"), lambda: Online.isOnline(True))

    #elif surface_name == "update-lobby":
    #    surfaceElements = Surface.getLobbyElements(Online.lobby_code, Online.get_lobby_members(), lambda: createSurface("quiz"), lambda: Online.isOnline(True))

    elif surface_name == "starting":
        surfaceElements = Surface.getStartingElements(lambda: createSurface("quiz"), lambda: createSurface("lobby"))

    elif surface_name == "ending":
        totalTime = round(sum(Time.TimeStamps()))
        surfaceElements = Surface.getEndingElements(totalTime)
        sendEmail(['', ''])

def answerFunc(newAnswer):
    global answer
    answer = newAnswer

def nextQuestion():
    global question, answer
    Answers.AppendAnswer(question, answer)
    Time.EndTimer(timer, question)
    if len(Answers.Answers()) - 1 > question:
        question += 1
        answer = Answers.Answers()[question]
        if Online.online:
            Online.setRound()
        createSurface("quiz")
        Surface.setSelectedAnswer(answer)
    else:
        if Online.online:
            Online.sendEmails()
        createSurface("ending")

def previousQuestion():
    global question, answer
    if question > 0:
        Time.EndTimer(timer, question)
        Answers.AppendAnswer(question, answer)
        question -= 1
        answer = Answers.Answers()[question]
        createSurface("quiz")
        Surface.setSelectedAnswer(answer)

def preloadAllImages():
    questions_images = [Elements.PreloadImage(q[1]) for q in Questions[0] if q[1]]
    answers_images = [[Elements.PreloadImage(a[1]) for a in qa if a[1]] for qa in Questions[1]]
    images.append(questions_images)
    images.append(answers_images)

def sendEmail(name):
    Send.send_email(Settings.GetSetting("email-adress"), Time.TimeStamps(), Answers.Answers(), name)

preloadAllImages()
main()