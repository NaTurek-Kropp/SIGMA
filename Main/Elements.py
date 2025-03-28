import pygame
import requests
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
    def __init__(self, text: str, font=pygame.font.get_default_font(), fontSize: int=10, fontColor="black", backgroundColor=None):
        self.font = pygame.font.SysFont(font, fontSize) or pygame.font.Font(font, fontSize)
        self.text = text
        self.fontColor = fontColor
        self.backgroundColor = backgroundColor

    def render(self):
        return self.font.render(self.text, True, self.fontColor, self.backgroundColor)
class PreloadImage():
    def __init__(self, url=None, file=None):
        self.image = None
        self.url = url
        self.file = file
        self.loadImage()

    def loadImage(self):
        if self.url:
            try:
                response = requests.get(self.url, timeout=5)
                response.raise_for_status()
                self.image = pygame.image.load(BytesIO(response.content))
            except (requests.RequestException, pygame.error) as e:
                print(f"Nie udało sie wczytać obrazu z linku: {e}")
        elif self.file:
            try:
                self.image = pygame.image.load(self.file)
            except pygame.error as e:
                print(f"Nie udało sie wczytać obrazu z pliku: {e}")

    def getImage(self):
        return self.image

class Image():
    def __init__(self, *, image: PreloadImage, factor: Literal["height", "width", None], sizeScale=(0,0), sizeOffset=(0,0), positionScale=(0,0), positionOffset=(0,0), align: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft", anchor: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft"):
        if not pygame.display.get_surface(): return
        self.surface = pygame.display.get_surface()
        self.factor = factor
        self.align = align
        self.anchor = anchor
        self.image = image.getImage()
        self.positionScale = positionScale
        self.positionOffset = positionOffset

        surfaceSize = self.surface.get_size()
        self.size = getSize(surfaceSize, sizeScale, sizeOffset)
        self.resizeFactor()

        self.position = getPosition(surfaceSize, positionScale, positionOffset, self.size, self.align, self.anchor)

    def resizeFactor(self):
        if not self.image: return
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

    def changeSize(self, sizeScale=(0,0), sizeOffset=(0,0)):
        surfaceSize = self.surface.get_size()
        self.size = getSize(surfaceSize, sizeScale, sizeOffset)
        self.resizeFactor()

        self.position = getPosition(surfaceSize, self.positionScale, self.positionOffset, self.size, self.align, self.anchor)

    def tick(self):
        if not self.image: return
        self.surface.blit(self.image, self.position)

class Button():
    def __init__(self, *, color="white", text: Text=None, command: Callable=None, sizeScale=(0,0), sizeOffset=(0,0), positionScale=(0,0), positionOffset=(0,0), align: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft", anchor: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft"):
        self.surface = pygame.display.get_surface()
        self.color = color
        self.align = align
        self.anchor = anchor
        self.command = command

        surfaceSize = self.surface.get_size()
        self.size = getSize(surfaceSize, sizeScale, sizeOffset)
        self.position = getPosition(surfaceSize, positionScale, positionOffset, self.size, self.align, self.anchor)

        self.text = text
        if self.text:
            self.textrender = text.render()
            self.textRect = self.textrender.get_rect()
            self.textRect.center = getCenter(self.size, self.position)

    def getRect(self):
        return pygame.Rect(self.position, self.size)

    def renderText(self):
        if not self.text: return
        self.textrender = self.text.render()
        self.textRect = self.textrender.get_rect()
        self.textRect.center = getCenter(self.size, self.position)

    def tick(self):
        pygame.draw.rect(self.surface, self.color, self.position + self.size)

        if self.text:
            self.surface.blit(self.textrender, self.textRect)

    def pressed(self):
        if self.command:
            self.command()

class TextBox():
    def __init__(self, *, backgroundColor="white", text: Text, sizeScale=(0,0), sizeOffset=(0,0), positionScale=(0,0), positionOffset=(0,0), align: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft", anchor: Literal["topleft", "top", "topright", "left", "center", "right", "bottomleft", "bottom", "bottomright"]="topleft"):
        self.surface = pygame.display.get_surface()
        self.backgroundColor = backgroundColor
        self.align = align
        self.anchor = anchor
        self.text = text

        surfaceSize = self.surface.get_size()
        self.size = getSize(surfaceSize, sizeScale, sizeOffset)
        self.position = getPosition(surfaceSize, positionScale, positionOffset, self.size, self.align, self.anchor)

        self.renderText()

    def tick(self):
        pygame.draw.rect(self.surface, self.backgroundColor, self.position + self.size)
        
        if not self.text: return
        self.surface.blit(self.textrender, self.textRect)

    def renderText(self):
        if not self.text: return
        self.textrender = self.text.render()
        self.textRect = self.textrender.get_rect()
        self.textRect.center = getCenter(self.size, self.position)

class InputBox:
    def __init__(self, font, window, x, y, width, height, active_color=(0, 0, 0), inactive_color=(100, 100, 100)):
        self.font = font
        self.window = window
        self.text = ""
        self.rect = pygame.Rect(x, y, width, height)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = inactive_color
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on mouse click position
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.active_color if self.active else self.inactive_color

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                pass  # Do nothing on Enter
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self):
        # Draw the input box
        pygame.draw.rect(self.window, self.color, self.rect, 2)
        # Render the text
        text_surf = self.font.render(self.text, True, self.color)
        self.window.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def getText(self):
        return self.text

def getSize(surfaceSize, sizeScale, sizeOffset):
    return (surfaceSize[0]*(sizeScale[0])+sizeOffset[0], surfaceSize[1]*(sizeScale[1])+sizeOffset[1])

def getPosition(surfaceSize, positionScale, positionOffset, size, align, anchor):
    align = getAlignAnchor(surfaceSize, align)
    anchor = getAlignAnchor(size, anchor)
    return (align[0]-anchor[0]+surfaceSize[0]*positionScale[0]+positionOffset[0], align[1]-anchor[1]+surfaceSize[1]*positionScale[1]+positionOffset[1])

def getCenter(size, position):
    return (position[0]+size[0]/2, position[1]+size[1]/2)

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


