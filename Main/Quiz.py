import pygame
import Elements
import Data
import Surface
import Sub.Time as Time
import Send
from ProjectData import Settings
import threading
import Main.X.Online as Online
import subprocess

global surfaceElements, Questions, Answers, question, answer, images, timer, surfaceId, key
surfaceElements = []
surfaceId = 0
Questions = None
Answers = None
question = 0
answer = ""
images = []
timer = None
key = ""

def main():
    global key
    subprocess.run(["python3", "Main/MAILtestexctractor.py"], shell=True)
    pygame.init()
    screen = pygame.display.set_mode((1500, 1000))
    clock = pygame.time.Clock()
    running = True
    createSurface("starting")

    Settings.EditSubSetting("user-name", "example name")

    while running:
        screen.fill("white")  # Clear screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for element in surfaceElements:
                    if isinstance(element, Elements.Button) and element.getRect().collidepoint(mousePos):
                        element.pressed()
                    elif isinstance(element, Elements.InputBox):
                        element.handle_event(event) 
            elif event.type == pygame.KEYDOWN:
                for element in surfaceElements:
                    if isinstance(element, Elements.InputBox):
                        element.handle_event(event) 

        for element in surfaceElements:
            if hasattr(element, 'tick') and callable(getattr(element, 'tick')):
                element.tick()  # Update elements

        for element in surfaceElements:
            if hasattr(element, 'draw') and callable(getattr(element, 'draw')):
                if surfaceId == 1 and isinstance(element, Elements.InputBox):
                    element.draw()  # Draw elements
                    Settings.EditSubSetting("user-name", element.text) 
                if surfaceId == 0 and isinstance(element, Elements.InputBox):
                    element.draw()
                    key = element.text
                    
        pygame.display.update()  # Only update changed parts
        clock.tick(60)

    pygame.quit()

def createSurface(surface_name: str):
    global surfaceElements, timer, question, answer, surfaceId, key
    surfaceElements.clear()

    match surface_name:
        case "starting":
            surfaceId = 0
            surfaceElements = Surface.getStartingElements(lambda: getTest(key), lambda: createSurface("lobby"))
        case "login":
            surfaceId = 1
            surfaceElements = Surface.getLoginElements(lambda: createSurface("quiz"))
        case "quiz":
            surfaceId = 2
            # if Online.online:
            #     Online.setRound()
            
            questionImage = [Questions[0][question][0], images[0][question]]
            answerImage = []
            timer = Time.StartTimer()
            
            for indx, ans in enumerate(Questions[1][question]):
                img = images[1][question][indx] if images[1][question] else None
                answerImage.append([ans[0], img])

            surfaceElements = Surface.getQuizElements(answerFunc, nextQuestion, previousQuestion, questionImage, answerImage, question == len(Answers.Answers())-1, question == 0)
        #    if Online.online:
        #        Online.start_game_online()
        #        threading.Thread(target=Online.check_submit_updates, daemon=True).start()

        # case "lobby":
        #     Online.create_lobby()
        #     surfaceElements = Surface.getLobbyElements(Online.lobby_code, [], lambda: createSurface("quiz"), lambda: Online.isOnline(True))

        # case "update-lobby":
        #     surfaceElements = Surface.getLobbyElements(Online.lobby_code, Online.get_lobby_members(), lambda: createSurface("quiz"), lambda: Online.isOnline(True))
        case "ending":
            surfaceId = 3
            threading.Thread(target=sendEmail, daemon=True).start()
            totalTime = round(sum(Time.TimeStamps()))
            surfaceElements = Surface.getEndingElements(totalTime)

from Main import MAILtestexctractor as ms
def getTest(keycode):
    global Questions
    global Answers
    Questions = ms.get_test_by_keycode(keycode)
    Answers = ms.NumOfQuestionsFromKeycode(keycode)
    preloadAllImages()
    createSurface("login")

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
        # if Online.online:
        #     Online.sendEmails()
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

def sendEmail():
    Send.send_email(Settings.GetSetting("email-adress"), Time.TimeStamps(), Answers.Answers(), Settings.GetSubSetting("user-name"), Settings.GetSetting("test-title"), Settings.GetSetting("class"))

main()