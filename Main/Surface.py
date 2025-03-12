import Elements
import pygame

def getQuizElements(answerCommand, nextQuestionCommand, prevQuestionCommand, question, answers):
    ansLetters = ["A", "B", "C", "D"]
    surfaceElements = []

    questionTextBox = Elements.TextBox(text=Elements.Text(text=question[0], fontSize=80, fontColor="white"), backgroundColor="blue", sizeScale=(.9, .2), positionScale=(0, 0.05), align="top", anchor="top")
    surfaceElements.append(questionTextBox)

    image = Elements.Image(image=question[1], factor="height", sizeScale=(0, 0.3), positionScale=(0, 0.3), align="top", anchor="top")
    surfaceElements.append(image)

    y = 0.65
    for i in range(4):
        if i == 2:
            y+=.15
        answer = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text=answers[i][0], fontSize=80, fontColor="white"), command=lambda ans=ansLetters[i]: answerCommand(ans), sizeScale=(.4, .125), positionScale=(0.075+i%2*0.5,y))
        surfaceElements.append(answer)

        ansLetter = Elements.TextBox(text=Elements.Text(text=ansLetters[i], fontSize=80, fontColor="white"), backgroundColor="gray", sizeScale=(.05, .125), positionScale=(0.025+i%2*0.5, y))
        surfaceElements.append(ansLetter)

    nextQuestionTextBox = Elements.TextBox(text=Elements.Text("Następne", fontSize=40), positionScale=(0.9, 0.4), positionOffset=(-15,0), sizeScale=(.1,.05))
    nextQuestionImage = Elements.Image(file="Main\\img\\arrowright.png", factor="height", positionScale=(0.9, 0.45), sizeScale=(0,0.075))
    nextQuestionButton = Elements.Button(command=nextQuestionCommand, positionScale=(0.9,0.4), positionOffset=(-15,0), sizeOffset=(nextQuestionImage.size[0]+nextQuestionTextBox.size[0], nextQuestionImage.size[1]+nextQuestionTextBox.size[1]))

    surfaceElements.append(nextQuestionButton)
    surfaceElements.append(nextQuestionTextBox)
    surfaceElements.append(nextQuestionImage)

    prevQuestionTextBox = Elements.TextBox(text=Elements.Text("Poprzednie", fontSize=40), positionScale=(0.025, 0.4), positionOffset=(-15,0), sizeScale=(.1,.05))
    prevQuestionImage = Elements.Image(file="Main\\img\\arrowleft.png", factor="height", positionScale=(0.025, 0.45), sizeScale=(0,0.075))
    prevQuestionButton = Elements.Button(command=prevQuestionCommand, positionScale=(0.025,0.4), positionOffset=(-15,0), sizeOffset=(prevQuestionImage.size[0]+prevQuestionTextBox.size[0], prevQuestionImage.size[1]+prevQuestionTextBox.size[1]))
    surfaceElements.append(prevQuestionButton)
    surfaceElements.append(prevQuestionTextBox)
    surfaceElements.append(prevQuestionImage)

    return surfaceElements

def getStartingElements():
    surfaceElements = []

def getEndingElements(totalTime):
    surfaceElements = []

    timeTextBox = Elements.TextBox(text=Elements.Text(text=f"Twój czas to: {totalTime}!", fontSize=80, fontColor="white"), backgroundColor="black", sizeScale=(.5, .2), positionScale=(0.25, 0.4), align="center", anchor="center")
    surfaceElements.append(timeTextBox)
    infoTextBox = Elements.TextBox(text=Elements.Text(text="Twoje odpowiedzi oraz icc czas udzielenia został wysłany nauczycielowi", fontSize=40, fontColor="white"), backgroundColor="black", sizeScale=(.8, .1), positionScale=(0.1, 0.6), align="center", anchor="center")
    surfaceElements.append(infoTextBox)

    return surfaceElements

