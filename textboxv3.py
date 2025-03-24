import pygame

class InputBox:
    def __init__(self, font, window, x, y, width, height):
        self.font = font
        self.window = window
        self.text = ""
        self.input_active = True
        self.rect = pygame.Rect(x, y, width, height)
        self.color_active = (0, 0, 0)
        self.color_inactive = (200, 200, 200)
        self.color = self.color_inactive

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is inside the input box
            if self.rect.collidepoint(event.pos):
                self.input_active = True
                self.color = self.color_active
            else:
                self.input_active = False
                self.color = self.color_inactive
        elif event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                self.input_active = False
                self.color = self.color_inactive
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode

    def draw(self):
        self.window.fill(0)
        # Draw the input box
        pygame.draw.rect(self.window, self.color, self.rect, 2)
        # Render the text
        text_surf = self.font.render(self.text, True, self.color_active)
        self.window.blit(text_surf, (self.rect.x + 5, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))
        pygame.display.flip()


pygame.init()
window = pygame.display.set_mode((500, 200))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 50)

# Create an InputBox with position and size
input_box = InputBox(font, window, x=50, y=75, width=400, height=50)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        input_box.handle_event(event)

    input_box.draw()

pygame.quit()
exit()