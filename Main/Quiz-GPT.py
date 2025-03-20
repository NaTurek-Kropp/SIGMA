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

# Global variables
surfaceElements = []
Questions = Data.GetQuestionsDataFixed("ProjectData\\pytania.txt")
Answers = Data.Answers(Data.NumOfQuestions("ProjectData\\pytania.txt"))
question = 0
answer = ""
images = []
timer = None
online = False 
isInLobby = False 

# Lobby-related globals (set when lobby is created)
lobby_id = None
lobby_code = None
lobby_data = None
lobby_thread = None

def main():
    """Initialize pygame and run the main event loop."""
    pygame.init()
    screen = pygame.display.set_mode((1500, 1000))
    clock = pygame.time.Clock()
    running = True

    # Start with the 'starting' surface
    createSurface("starting")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                for button in surfaceElements:
                    if not isinstance(button, Elements.Button):
                        continue
                    if button.getRect().collidepoint(mousePos):
                        button.pressed()

        screen.fill("white")
        for element in surfaceElements:
            element.tick()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def createSurface(surface_name: str):
    """
    Creates the appropriate interface/screen based on the 'surface_name' parameter.
    Options include: 'starting', 'lobby', 'update-lobby', 'quiz', and 'ending'.
    """
    global surfaceElements, timer, isInLobby, lobby_id

    # Clear any previous elements
    surfaceElements.clear()

    if surface_name == "quiz":
        if online:
            # For online mode, update the round first
            setRound()
        
        # Get current question and corresponding image
        questionImage = [Questions[0][question][0], images[0][question]]
        answerImage = []
        timer = Time.StartTimer()  # Start timer for the question

        # Prepare answer images
        indx = 0
        for ans in Questions[1][question]:
            img = None
            if images[1][question] != []:
                img = images[1][question][indx]
            answerImage.append([ans[0], img])
            indx += 1

        if not online:
            surfaceElements = Surface.getQuizElements(answerFunc, nextQuestion, previousQuestion, questionImage, answerImage, question == len(Answers.Answers())-1)
        else:
            isInLobby = False
            surfaceElements = Surface.getOnlineQuizElements(answerFunc, nextQuestion, previousQuestion, questionImage, answerImage, question == len(Answers.Answers())-1)
            # Start game on server and launch thread to check if all answers are submitted
            start_game_online()
            threading.Thread(target=check_submit_updates, daemon=True).start()

    elif surface_name == "lobby":
        global lobby_data, lobby_code, lobby_thread
        isInLobby = True
        # Create a new lobby on the server
        response = requests.post('https://powarznastrona.pythonanywhere.com/create_lobby')
        if response.status_code == 201:
            lobby_data = response.json()
            lobby_id = lobby_data['lobby_id']
            lobby_code = lobby_data['lobby_code']
            print(f"Lobby created with ID: {lobby_id} and code: {lobby_code}")

            # Start thread to update lobby members
            lobby_thread = threading.Thread(target=check_lobby_updates, daemon=True)
            lobby_thread.start()
        else:
            print("Failed to create lobby")
        # Get lobby elements with a button to start the quiz and toggle online mode
        surfaceElements = Surface.getLobbyElements(lobby_code, [], lambda: createSurface("quiz"), lambda: isOnline(True))

    elif surface_name == "update-lobby":
        # Update lobby interface with current members
        response = requests.get('https://powarznastrona.pythonanywhere.com/get_lobby_members', params={'lobby_id': lobby_id})
        members = response.json().get('members', [])
        surfaceElements = Surface.getLobbyElements(lobby_code, members, lambda: createSurface("quiz"), lambda: isOnline(True))

    elif surface_name == "starting":
        # Starting page with options for lobby or direct quiz
        surfaceElements = Surface.getStartingElements(lambda: createSurface("quiz"), lambda: createSurface("lobby"))

    elif surface_name == "ending":
        # Ending screen: calculate total time and show final elements
        totalTime = sum(Time.TimeStamps())
        totalTime = round(totalTime)
        surfaceElements = Surface.getEndingElements(totalTime)
        sendEmail(['', ''])  # Sends email (replace parameters as needed)

def isOnline(isonline: bool):
    """Toggle online mode."""
    global online
    online = isonline

def answerFunc(newAnswer):
    """Callback to store answer."""
    global answer
    answer = newAnswer

def nextQuestion():
    """
    Callback for moving to the next question.
    Saves the current answer, stops the timer, then loads the next question or the ending screen.
    """
    global question, answer

    Answers.AppendAnswer(question, answer)
    Time.EndTimer(timer, question)
    if len(Answers.Answers()) - 1 > question:
        question += 1
        answer = Answers.Answers()[question]
        if online:
            setRound()
        createSurface("quiz")
        Surface.setSelectedAnswer(answer)
    else:
        if online:
            sendEmails()
        createSurface("ending")

def previousQuestion():
    """
    Callback for going back to the previous question.
    Saves the current answer, stops the timer, and loads the previous question.
    """
    global question, answer
    if question <= 0:
        return

    Time.EndTimer(timer, question)
    Answers.AppendAnswer(question, answer)
    question -= 1
    answer = Answers.Answers()[question]
    createSurface("quiz")
    Surface.setSelectedAnswer(answer)

def preloadAllImages():
    """Preload all images used for questions and answers."""
    questions_images = []
    for q in Questions[0]:
        if not q[1]:
            continue
        questions_images.append(Elements.PreloadImage(q[1]))

    answers_images = []
    for qa in Questions[1]:
        currAnswers = []
        for a in qa:
            if not a[1]:
                continue
            currAnswers.append(Elements.PreloadImage(a[1]))
        answers_images.append(currAnswers)

    images.append(questions_images)
    images.append(answers_images)

def sendEmail(name):
    """Send email with quiz results."""
    Send.send_email(Settings.GetSetting("email-adress"), Time.TimeStamps(), Answers.Answers(), name)

def sendEmails():
    """
    Get all lobby member objects from the server and send emails to each member.
    Note: The server response is assumed to have a 'members' key containing the list.
    """
    response = requests.get('https://powarznastrona.pythonanywhere.com/get_lobby_member_objects', params={'lobby_id': lobby_id})
    if response.status_code == 200:
        members_data = response.json()
        # Expecting members_data to contain a key "members" which is a list of member objects
        for member in members_data.get('members', []):
            Send.send_email(Settings.GetSetting("email-adress"), Time.TimeStamps(), member.get('answers', []), member.get('name', ''))
    else:
        print("Failed to retrieve lobby member objects for emails.")

def setRound():
    """Inform the server to update the round state."""
    data = {'lobby_id': lobby_id}
    requests.post('https://powarznastrona.pythonanywhere.com/setRound', json=data)

def start_game_online():
    """Start the online game on the server."""
    data = {'lobby_id': lobby_id}
    response = requests.post('https://powarznastrona.pythonanywhere.com/start_game', json=data)
    if response.status_code == 200:
        print("Online game started successfully.")
    else:
        print("Failed to start online game.")

def check_submit_updates():
    """
    Poll the server for submission updates.
    Once all members have submitted, automatically trigger the next question.
    """
    while True:
        response = requests.get('https://powarznastrona.pythonanywhere.com/all_members_submitted', params={'lobby_id': lobby_id})
        if response.status_code == 200:
            submitted_data = response.json()
            print("Submission status:", submitted_data)
            if submitted_data.get('all_submitted'):
                nextQuestion()
        time.sleep(5)

def check_lobby_updates():
    """
    Continuously poll the lobby for member updates.
    If the lobby data changes, update the lobby screen.
    """
    global lobby_data
    while isInLobby:
        response = requests.get('https://powarznastrona.pythonanywhere.com/get_lobby_members', params={'lobby_id': lobby_id})
        if response.status_code == 200:
            new_lobby_data = response.json()
            if new_lobby_data != lobby_data:
                lobby_data = new_lobby_data
                createSurface("update-lobby")
        time.sleep(5)

# Preload images and start the game loop
preloadAllImages()
main()
