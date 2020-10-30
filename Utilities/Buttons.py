import pygame
from Utilities.Constants import Colors


class Button:
    def __init__(self, x, y, width, height, border_width, text, colors, function=None, enabled=True):
        # self.x, self.y = x, y
        # self.width, self.height = width, height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.colors = [pygame.Color(color) for color in colors]
        self.function = function
        self.border_width = border_width

        self.font = pygame.font.Font(None, 32)

        self.enabled = enabled
        self.hovering = False

        self.click_buffer = 10

    def hover(self, mouse_pos):
        if self.rect.collidepoint(*mouse_pos):
            self.hovering = True
        else:
            self.hovering = False

    def draw(self, window):
        if self.click_buffer > 0:
            self.click_buffer -= 1
        if self.enabled:
            if not self.hovering:
                pygame.draw.rect(window, self.colors[1], self.rect)
                pygame.draw.rect(window, self.colors[0], self.rect, self.border_width)
            else:
                pygame.draw.rect(window, self.colors[2], self.rect)
                pygame.draw.rect(window, self.colors[1], self.rect, self.border_width)

            text = self.font.render(self.text, True, Colors.White)
            window.blit(text, (
                self.rect.x + self.rect.width // 2 - text.get_width() // 2,
                self.rect.y + self.rect.height // 2 - text.get_height() // 2
            ))

    def toggle(self, enabled):
        self.enabled = enabled
        self.click_buffer = 20

    def click(self, click_pos):
        if self.rect.collidepoint(*click_pos) and self.click_buffer == 0:
            self.click_buffer = 10
            if self.function is not None:
                self.function()
