import pygame
from config import *

class Player:
    def __init__(self, x, y, color, player_id):
        self.x = x
        self.y = y
        self.color = color
        self.id = player_id
        self.chat_message = ""
        self.chat_timer = 0
    
    def move(self, dx, dy):
        self.x += dx * PLAYER_SPEED
        self.y += dy * PLAYER_SPEED
        
        self.x = max(0, min(SCREEN_WIDTH - PLAYER_SIZE, self.x))
        self.y = max(0, min(SCREEN_HEIGHT - PLAYER_SIZE, self.y))
    
    def draw(self, screen, show_chat=True):
        pygame.draw.circle(screen, self.color, 
                          (int(self.x + PLAYER_SIZE // 2), int(self.y + PLAYER_SIZE // 2)), 
                          PLAYER_SIZE // 2)
        pygame.draw.circle(screen, (255, 255, 255), 
                          (int(self.x + PLAYER_SIZE // 2), int(self.y + PLAYER_SIZE // 2)), 
                          PLAYER_SIZE // 2, 2)
        
        if show_chat and self.chat_message and self.chat_timer > 0:
            font = pygame.font.Font(None, 24)
            text = font.render(self.chat_message, True, (255, 255, 255))
            text_bg = pygame.Rect(self.x - 10, self.y - 30, text.get_width() + 20, text.get_height() + 10)
            pygame.draw.rect(screen, (30, 30, 30), text_bg, border_radius=5)
            screen.blit(text, (self.x, self.y - 25))
    
    def set_chat(self, message):
        self.chat_message = message
        self.chat_timer = 180
    
    def update(self):
        if self.chat_timer > 0:
            self.chat_timer -= 1
    
    def update_from_dict(self, data):
        if data:
            self.x = data.get("x", self.x)
            self.y = data.get("y", self.y)
            chat_msg = data.get("chat", "")
            if chat_msg and chat_msg != self.chat_message:
                self.set_chat(chat_msg)