import Elements
import pygame

buttons = {}
buttonColor = pygame.Color(0,128,0)

def getQuizElements(answerCommand, nextQuestionCommand, prevQuestionCommand, question, answers, isLastQuestion=False):
    ansLetters = ["A", "B", "C", "D"]
    surfaceElements = []
    buttons.clear()

    questionTextBox = Elements.TextBox(text=Elements.Text(text=question[0], fontSize=80, fontColor="white"), backgroundColor="blue", sizeScale=(.9, .2), positionScale=(0, 0.05), align="top", anchor="top")
    surfaceElements.append(questionTextBox)

    image = Elements.Image(image=question[1], factor="height", sizeScale=(0, 0.3), positionScale=(0, 0.3), align="top", anchor="top")
    surfaceElements.append(image)

    y = 0.65
    for i in range(4):
        if i == 2:
            y+=.15
        
        answerButton = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text=answers[i][0], fontSize=80, fontColor="white"), command=lambda ans=ansLetters[i]: answerQuestion(ans, answerCommand), sizeScale=(.4, .125), positionScale=(0.075+i%2*0.5,y))
        buttons[ansLetters[i]] = answerButton

        if answers[i][1]:
            ansImage = Elements.Image(image=answers[i][1], positionScale=(0.075+i%2*0.5+0.4,y), sizeScale=(0, .125), factor="height", anchor="topright")
            answerButton.size = (answerButton.size[0]-ansImage.size[0], answerButton.size[1])
            answerButton.renderText()
            surfaceElements.append(ansImage)

        ansLetter = Elements.TextBox(text=Elements.Text(text=ansLetters[i], fontSize=80, fontColor="white"), backgroundColor="gray", sizeScale=(.05, .125), positionScale=(0.025+i%2*0.5, y))
        surfaceElements.append(answerButton)
        surfaceElements.append(ansLetter)

    nextQuestionTextBox = Elements.TextBox(text=Elements.Text("Następne", fontSize=40), positionScale=(0.9, 0.4), positionOffset=(-15,0), sizeScale=(.1,.05))
    if isLastQuestion:
        nextQuestionTextBox.text = Elements.Text("Zakończ", fontSize=40)
        nextQuestionTextBox.renderText()
    nextQuestionImage = Elements.Image(image=Elements.PreloadImage(file="Main\\img\\arrowright.png"), factor="height", positionScale=(0.9, 0.45), sizeScale=(0,0.075))
    nextQuestionButton = Elements.Button(command=nextQuestionCommand, positionScale=(0.9,0.4), positionOffset=(-15,0), sizeOffset=(nextQuestionImage.size[0]+nextQuestionTextBox.size[0], nextQuestionImage.size[1]+nextQuestionTextBox.size[1]))
    surfaceElements.append(nextQuestionButton)
    surfaceElements.append(nextQuestionTextBox)
    surfaceElements.append(nextQuestionImage)

    prevQuestionTextBox = Elements.TextBox(text=Elements.Text("Poprzednie", fontSize=40), positionScale=(0.025, 0.4), positionOffset=(-15,0), sizeScale=(.1,.05))
    prevQuestionImage = Elements.Image(image=Elements.PreloadImage(file="Main\\img\\arrowleft.png"), factor="height", positionScale=(0.025, 0.45), sizeScale=(0,0.075))
    prevQuestionButton = Elements.Button(command=prevQuestionCommand, positionScale=(0.025,0.4), positionOffset=(-15,0), sizeOffset=(prevQuestionImage.size[0]+prevQuestionTextBox.size[0], prevQuestionImage.size[1]+prevQuestionTextBox.size[1]))
    surfaceElements.append(prevQuestionButton)
    surfaceElements.append(prevQuestionTextBox)
    surfaceElements.append(prevQuestionImage)

    return surfaceElements

def answerQuestion(answer, answerCommand):
    setSelectedAnswer(answer)
    answerCommand(answer)

def setSelectedAnswer(answer):
    if not answer or not buttons[answer]: return
    for i in buttons.values():
        i.color = buttonColor
    buttons[answer].color -= pygame.Color(0,40,0)

def getStartingElements(startLocalCommand, startRoomCommand):
    surfaceElements = []

    startButton = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text="Start Local", fontSize=80, fontColor="white"), command=startLocalCommand, sizeScale=(.3, .125), positionScale=(0.35, 0.4))
    surfaceElements.append(startButton)

    startRoomButton = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text="Start Room", fontSize=80, fontColor="white"), command=startRoomCommand, sizeScale=(.3, .125), positionScale=(0.35, 0.55))
    surfaceElements.append(startRoomButton)

    exitButton = Elements.Button(color=pygame.Color(255,0,0), text=Elements.Text(text="Exit", fontSize=80, fontColor="white"), command=lambda: print("Exit button pressed"), sizeScale=(.3, .125), positionScale=(0.35, 0.7))
    surfaceElements.append(exitButton)

    return surfaceElements


def getEndingElements(totalTime):
    surfaceElements = []

    timeTextBox = Elements.TextBox(text=Elements.Text(text=f"Twój czas to: {totalTime} sek!", fontSize=80, fontColor="white"), backgroundColor="black", sizeScale=(.5, .2), positionScale=(0, -0.1), align="center", anchor="center")
    surfaceElements.append(timeTextBox)
    infoTextBox = Elements.TextBox(text=Elements.Text(text="Twoje odpowiedzi oraz czas udzielenia został wysłany nauczycielowi", fontSize=40, fontColor="white"), backgroundColor="black", sizeScale=(.8, .1), positionScale=(0, 0.1), align="center", anchor="center")
    surfaceElements.append(infoTextBox)

    return surfaceElements


def getLobbyElements(code, members):
    surfaceElements = []
    titleTextBox = Elements.TextBox(text=Elements.Text(text="Lobby", fontSize=80, fontColor="white"), backgroundColor="blue", sizeScale=(.5, .2), positionScale=(0, 0.05), align="top", anchor="top")
    surfaceElements.append(titleTextBox)
    
    lobbyInfoTextBox = Elements.TextBox(text=Elements.Text(text=f"{code}", fontSize=40, fontColor="white"), backgroundColor="blue", sizeScale=(.8, .1), positionScale=(0, 0.3), align="top", anchor="top")
    surfaceElements.append(lobbyInfoTextBox)

    membersList = members

    y = 0.5
    for member in membersList:
        memberTextBox = Elements.TextBox(text=Elements.Text(text=member, fontSize=40, fontColor="yellow"), backgroundColor="green", sizeScale=(.8, .05), positionScale=(0, y), align="top", anchor="top")
        surfaceElements.append(memberTextBox)
        y += 0.1

    return surfaceElements
