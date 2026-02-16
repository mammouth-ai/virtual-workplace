import pygame
import sys
from config import *
from player import Player

def draw_grass(screen):
    for y in range(0, SCREEN_HEIGHT, GRASS_TILE_SIZE):
        for x in range(0, SCREEN_WIDTH, GRASS_TILE_SIZE):
            shade = 20 if (x // GRASS_TILE_SIZE + y // GRASS_TILE_SIZE) % 2 == 0 else 0
            color = (GRASS_COLOR[0] - shade, GRASS_COLOR[1] - shade, GRASS_COLOR[2] - shade)
            pygame.draw.rect(screen, color, (x, y, GRASS_TILE_SIZE, GRASS_TILE_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Virtual Coworking Space")
    clock = pygame.time.Clock()
    
    player1 = Player(100, 100, PLAYER1_COLOR, 1)
    player2 = Player(400, 300, PLAYER2_COLOR, 2)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player1.set_chat("Hello!")
                elif event.key == pygame.K_RETURN:
                    player2.set_chat("Hi there!")
        
        keys = pygame.key.get_pressed()
        dx1, dy1 = 0, 0
        if keys[pygame.K_a]:
            dx1 = -1
        if keys[pygame.K_d]:
            dx1 = 1
        if keys[pygame.K_w]:
            dy1 = -1
        if keys[pygame.K_s]:
            dy1 = 1
        player1.move(dx1, dy1)
        
        dx2, dy2 = 0, 0
        if keys[pygame.K_LEFT]:
            dx2 = -1
        if keys[pygame.K_RIGHT]:
            dx2 = 1
        if keys[pygame.K_UP]:
            dy2 = -1
        if keys[pygame.K_DOWN]:
            dy2 = 1
        player2.move(dx2, dy2)
        
        player1.update()
        player2.update()
        
        screen.fill((0, 0, 0))
        draw_grass(screen)
        player1.draw(screen)
        player2.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()