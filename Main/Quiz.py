import pygame
import Elements
import Data
import Surface
import Sub.Time as Time
import Send
from ProjectData import Settings
import requests
import threading
import time

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

    createSurface("starting")

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

            indx = 0
            for ans in Questions[1][question]:
                image = None
                if images[1][question] != []:
                    image = images[1][question][indx]
                answerImage.append([ans[0], image])

            surfaceElements = Surface.getQuizElements(answerFunc, nextQuestion, previousQuestion, questionImage, answerImage, question == len(Answers.Answers())-1)
        case "lobby":
            global lobby_data, lobby_code, lobby_id
            response = requests.post('http://127.0.0.1:5000/create_lobby')
            if response.status_code == 201:
                lobby_data = response.json()
                lobby_id = lobby_data['lobby_id']
                lobby_code = lobby_data['lobby_code']
                print(f"Lobby created with ID: {lobby_id} and code: {lobby_code}")
                def check_lobby_updates(lobby_data, lobby_id, interval=5):
                    while True:
                        response = requests.get(f'http://127.0.0.1:5000/get_lobby_members', params={'lobby_id': lobby_id})
                        if response.status_code == 200:
                            print(response)
                            new_lobby_data = response.json()
                            if new_lobby_data != lobby_data:
                                lobby_data = new_lobby_data
                                createSurface("update-lobby")
                        time.sleep(interval)

                thread = threading.Thread(target=check_lobby_updates, args=(lobby_data, lobby_id,))
                thread.daemon = True
                thread.start()
            else:
                print("Failed to create lobby")
            surfaceElements = Surface.getLobbyElements(lobby_code, [])
        case "update-lobby":
            data = requests.get(f'http://127.0.0.1:5000/get_lobby_members', params={'lobby_id': lobby_id})
            members = data.json().get('members', [])
            print(members)
            surfaceElements = Surface.getLobbyElements(lobby_code, members)
        case "starting":
            surfaceElements = Surface.getStartingElements(lambda: createSurface("quiz"), lambda: createSurface("lobby"))
        case "ending":
            totalTime = 0
            for i in Time.TimeStamps():
                totalTime += i
            totalTime = round(totalTime)
            surfaceElements = Surface.getEndingElements(totalTime)
            
            sendEmail()

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

def sendEmail():
    Send.send_email(Settings.GetSetting("email-adress"), Time.TimeStamps(), Answers.Answers(), ["Bratosz", "Turczewski"])

preloadAllImages()
main()