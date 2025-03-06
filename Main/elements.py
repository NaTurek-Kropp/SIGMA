import pygame
import requests
import Data
from io import BytesIO
from typing import Literal, Callable

class Rect():
    def __init__(self, *, color="white", sizeScale=(0,0), sizeOffset=(0,0), positionScale=(0,0), positionOffset=(0,0), align: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft", anchor: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft"):
        if not pygame.display.get_surface(): return
        self.surface = pygame.display.get_surface()
        self.color = color
        self.align = align
        self.anchor = anchor

        surfaceSize = self.surface.get_size()
        self.size = getSize(surfaceSize, sizeScale, sizeOffset)
        self.position = getPosition(surfaceSize, positionScale, positionOffset, self.size, self.align, self.anchor)

    def tick(self):
        pygame.draw.rect(self.surface, self.color, self.position + self.size)

class Text():
    def __init__(self, text: str, font, fontSize: int=10, fontColor="black", backgroundColor=None):
        self.font = pygame.font.Font(font, fontSize)
        self.text = self.font.render(text, True, fontColor, backgroundColor)

class Image():
    def __init__(self, *, url, factor: Literal["height", "width", None], sizeScale=(0,0), sizeOffset=(0,0), positionScale=(0,0), positionOffset=(0,0), align: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft", anchor: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft"):
        if not pygame.display.get_surface(): return
        self.surface = pygame.display.get_surface()
        self.factor = factor
        self.align = align
        self.anchor = anchor

        surfaceSize = self.surface.get_size()
        self.size = getSize(surfaceSize, sizeScale, sizeOffset)
        self.position = getPosition(surfaceSize, positionScale, positionOffset, self.size, self.align, self.anchor)

        self.imageUrl = url
        self.loadImage()

        self.position = getPosition(surfaceSize, positionScale, positionOffset, self.size, self.align, self.anchor)

    def loadImage(self):
        response = requests.get(self.imageUrl)
        self.image = pygame.image.load(BytesIO(response.content))
        
        imageSize = self.image.get_size()
        
        if self.factor == "height":
            scaleFactor = imageSize[0] / imageSize[1]
            self.image = pygame.transform.scale(self.image, (self.size[1]*scaleFactor, self.size[1]))
        elif self.factor == "width":
            scaleFactor = imageSize[1] / imageSize[0]
            self.image = pygame.transform.scale(self.image, (self.size[0], self.size[0]*scaleFactor))
        else:
            self.image = pygame.transform.scale(self.image, self.size)

        self.size = self.image.get_size()

    def tick(self):
        self.surface.blit(self.image, self.position)

class Button(): #nonexistend function -> Callable !
    def __init__(self, *, color="white", text: Text, command: Callable, sizeScale=(0,0), sizeOffset=(0,0), positionScale=(0,0), positionOffset=(0,0), align: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft", anchor: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft"):
        self.surface = pygame.display.get_surface()
        self.color = color
        self.align = align
        self.anchor = anchor
        self.text = text
        self.command = command

        surfaceSize = self.surface.get_size()
        self.size = getSize(surfaceSize, sizeScale, sizeOffset)
        self.position = getPosition(surfaceSize, positionScale, positionOffset, self.size, self.align, self.anchor)

    def tick(self):
        pygame.draw.rect(self.surface, self.color, self.position + self.size)

def getSize(surfaceSize, sizeScale, sizeOffset):
    return (surfaceSize[0]*(sizeScale[0]+sizeOffset[0]), surfaceSize[1]*(sizeScale[1]+sizeOffset[1]))

def getPosition(surfaceSize, positionScale, positionOffset, size, align, anchor):
    align = getAlignAnchor(surfaceSize, align)
    anchor = getAlignAnchor(size, anchor)
    print(anchor)
    return (align[0]-anchor[0]+surfaceSize[0]*positionScale[0]+positionOffset[0], align[1]-anchor[1]+surfaceSize[1]*positionScale[1]+positionOffset[1])

def getAlignAnchor(surfaceSize, alignAnchor: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]):
    match alignAnchor:
        case "topleft":
            return (0,0)
        case "top":
            return (surfaceSize[0]*.5, 0)
        case "topright":
            return (surfaceSize[0], 0)
        case "left":
            return (0, surfaceSize[1]*.5)
        case "center":
            return (surfaceSize[0]*.5, surfaceSize[1]*.5)
        case "right":
            return (surfaceSize[0], surfaceSize[1]*.5)
        case "bottomleft":
            return (0, surfaceSize[1])
        case "bottom":
            return (surfaceSize[0]*.5, surfaceSize[1])
        case "bottomright":
            return (surfaceSize[0], surfaceSize[1])