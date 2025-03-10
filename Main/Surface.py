import Elements
import pygame

def getQuizElements(answerCommand):
    surfaceElements = []

    questionTextBox = Elements.TextBox(text=Elements.Text(text="Pytanie", fontSize=80, fontColor="white"), backgroundColor="blue", sizeScale=(.9, .2), positionScale=(0, 0.05), align="top", anchor="top")
    surfaceElements.append(questionTextBox)

    image = Elements.Image(url="https://world-schools.com/wp-content/uploads/2023/01/IMG-Academy-cover-WS.webp", factor="height", sizeScale=(0, 0.3), positionScale=(0, 0.3), align="top", anchor="top")
    surfaceElements.append(image)

    button1 = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text="A", fontSize=80, fontColor="white"), command=lambda: answerCommand("A"), sizeScale=(.4, .125), positionScale=(0.05, 0.65))
    button2 = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text="B", fontSize=80, fontColor="white"), command=lambda: answerCommand("B"), sizeScale=(.4, .125), positionScale=(0.55, 0.65))
    button3 = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text="C", fontSize=80, fontColor="white"), command=lambda: answerCommand("C"), sizeScale=(.4, .125), positionScale=(0.05, 0.8))
    button4 = Elements.Button(color=pygame.Color(0,128,0), text=Elements.Text(text="D", fontSize=80, fontColor="white"), command=lambda: answerCommand("D"), sizeScale=(.4, .125), positionScale=(0.55, 0.8))
    surfaceElements.append(button1)
    surfaceElements.append(button2)
    surfaceElements.append(button3)
    surfaceElements.append(button4)

    return surfaceElements

def getStartingElements():
    surfaceElements = []

def getEndingElements():
    surfaceElements = []