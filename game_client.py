import pygame
import sys
import threading
import time
from config import *
from player import Player
from network import NetworkClient

class GameClient:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Virtual Coworking Space - Client")
        self.clock = pygame.time.Clock()
        
        self.network = NetworkClient()
        self.connected = False
        self.player_id = 0
        self.local_player = None
        self.other_players = {}
        self.chat_input = ""
        self.chat_active = False
        self.proximity_radius = CHAT_RADIUS
        self.in_proximity = False
        self.nearby_player = None
        
        self.connect_to_server()
        
        if self.connected:
            self.init_players()
    
    def connect_to_server(self):
        print("Connecting to server...")
        if self.network.connect():
            self.connected = True
            self.player_id = self.network.player_id
            print(f"Connected to server as Player {self.player_id}!")
        else:
            print("Failed to connect to server. Make sure server is running.")
    
    def init_players(self):
        colors = {1: PLAYER1_COLOR, 2: PLAYER2_COLOR}
        self.local_player = Player(100, 100, colors.get(self.player_id, PLAYER1_COLOR), self.player_id)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if not self.chat_active:
                    if event.key == pygame.K_1 and self.local_player:
                        self.local_player.set_chat("Hello!")
                    elif event.key == pygame.K_2 and self.local_player:
                        self.local_player.set_chat("How are you?")
                    elif event.key == pygame.K_3 and self.local_player:
                        self.local_player.set_chat("Let's work together!")
                    elif event.key == pygame.K_4 and self.local_player:
                        self.local_player.set_chat("Goodbye!")
                    elif event.key == pygame.K_t:
                        self.chat_active = True
                        self.chat_input = ""
                else:
                    if event.key == pygame.K_RETURN:
                        if self.chat_input.strip() and self.local_player:
                            self.local_player.set_chat(self.chat_input)
                        self.chat_active = False
                        self.chat_input = ""
                    elif event.key == pygame.K_ESCAPE:
                        self.chat_active = False
                        self.chat_input = ""
                    elif event.key == pygame.K_BACKSPACE:
                        self.chat_input = self.chat_input[:-1]
                    else:
                        if len(self.chat_input) < 30:
                            self.chat_input += event.unicode
        
        return True
    
    def update(self):
        if not self.connected:
            return
        
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if not self.chat_active:
            if keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_s]:
                dy = 1
        
        if self.local_player:
            self.local_player.move(dx, dy)
            self.local_player.update()
            
            players_data = self.network.send_update(
                self.local_player.x, 
                self.local_player.y, 
                self.local_player.chat_message if self.local_player.chat_timer > 0 else ""
            )
            
            if players_data:
                self.update_other_players(players_data)
                self.check_proximity()
    
    def update_other_players(self, players_data):
        colors = {1: PLAYER1_COLOR, 2: PLAYER2_COLOR}
        
        for pid, data in players_data.items():
            pid = int(pid)
            if pid == self.player_id:
                continue
            
            if pid not in self.other_players:
                self.other_players[pid] = Player(
                    data.get("x", 100), 
                    data.get("y", 100), 
                    colors.get(pid, (200, 200, 200)), 
                    pid
                )
            else:
                self.other_players[pid].update_from_dict(data)
                self.other_players[pid].update()
    
    def check_proximity(self):
        self.in_proximity = False
        self.nearby_player = None
        
        if not self.local_player:
            return
        
        for pid, player in self.other_players.items():
            distance = ((self.local_player.x - player.x) ** 2 + (self.local_player.y - player.y) ** 2) ** 0.5
            if distance < self.proximity_radius:
                self.in_proximity = True
                self.nearby_player = pid
                break
    
    def draw(self):
        self.screen.fill((0, 0, 0))
        
        for y in range(0, SCREEN_HEIGHT, GRASS_TILE_SIZE):
            for x in range(0, SCREEN_WIDTH, GRASS_TILE_SIZE):
                shade = 20 if (x // GRASS_TILE_SIZE + y // GRASS_TILE_SIZE) % 2 == 0 else 0
                color = (GRASS_COLOR[0] - shade, GRASS_COLOR[1] - shade, GRASS_COLOR[2] - shade)
                pygame.draw.rect(self.screen, color, (x, y, GRASS_TILE_SIZE, GRASS_TILE_SIZE))
        
        if self.local_player:
            self.local_player.draw(self.screen, show_chat=True)
            
            for pid, player in self.other_players.items():
                distance = ((self.local_player.x - player.x) ** 2 + (self.local_player.y - player.y) ** 2) ** 0.5
                in_range = distance < self.proximity_radius
                player.draw(self.screen, show_chat=in_range)
                
                if in_range:
                    pygame.draw.circle(self.screen, (255, 255, 255, 100), 
                                     (int(self.local_player.x + PLAYER_SIZE // 2), 
                                      int(self.local_player.y + PLAYER_SIZE // 2)), 
                                     self.proximity_radius, 1)
        
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        font = pygame.font.Font(None, 28)
        
        status_text = f"Player {self.player_id}" if self.connected else "Not connected"
        status_surf = font.render(status_text, True, (255, 255, 255))
        self.screen.blit(status_surf, (10, 10))
        
        players_text = f"Players: {1 + len(self.other_players)}/2"
        players_surf = font.render(players_text, True, (255, 255, 255))
        self.screen.blit(players_surf, (10, 40))
        
        proximity_text = "In chat range!" if self.in_proximity else "Not in chat range"
        proximity_color = (100, 255, 100) if self.in_proximity else (255, 100, 100)
        proximity_surf = font.render(proximity_text, True, proximity_color)
        self.screen.blit(proximity_surf, (10, 70))
        
        controls_text = "WASD: Move | 1-4: Quick messages | T: Type chat"
        controls_surf = font.render(controls_text, True, (200, 200, 200))
        self.screen.blit(controls_surf, (10, SCREEN_HEIGHT - 30))
        
        if self.chat_active:
            pygame.draw.rect(self.screen, (30, 30, 30), 
                           (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 50, 300, 40), border_radius=5)
            chat_prompt = font.render("Chat: " + self.chat_input, True, (255, 255, 255))
            self.screen.blit(chat_prompt, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT - 45))
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = GameClient()
    game.run()