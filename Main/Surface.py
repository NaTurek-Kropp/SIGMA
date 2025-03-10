import Elements
import pygame

def getQuizElements(answerCommand, question, answers):
    ansLetters = ["A", "B", "C", "D"]
    surfaceElements = []

    questionTextBox = Elements.TextBox(text=Elements.Text(text=question[0], fontSize=80, fontColor="white"), backgroundColor="blue", sizeScale=(.9, .2), positionScale=(0, 0.05), align="top", anchor="top")
    surfaceElements.append(questionTextBox)

    image = Elements.Image(url=question[1], factor="height", sizeScale=(0, 0.3), positionScale=(0, 0.3), align="top", anchor="top")
    surfaceElements.append(image)

    y = 0.65
    for i in range(4):
        if i == 2:
            y+=.15
        answer = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text=answers[i][0], fontSize=80, fontColor="white"), command=lambda ans=ansLetters[i]: answerCommand(ans), sizeScale=(.4, .125), positionScale=(0.075+i%2*0.5,y))
        surfaceElements.append(answer)

        ansLetter = Elements.TextBox(text=Elements.Text(text=ansLetters[i], fontSize=80, fontColor="white"), backgroundColor="gray", sizeScale=(.05, .125), positionScale=(0.025+i%2*0.5, y))
        surfaceElements.append(ansLetter)

    nextQuestionButton = Elements.Image(file="img/arrowright.png", positionScale=(0.05, 0.5), sizeScale=(0.05,0.05))
    surfaceElements.append(nextQuestionButton)

    return surfaceElements

def getStartingElements():
    surfaceElements = []

def getEndingElements():
    surfaceElements = []