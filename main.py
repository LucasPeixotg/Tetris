import random
import pygame
from shapes import shapes, shapes_colors

block_size = 40
screen_width = 10
screen_height = 15

pygame.init()
screen = pygame.display.set_mode((screen_width*block_size, screen_height*block_size))

def main():
    run = True

    while run:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # GAME LOGIC
        
        # GAME SCREEN
        pygame.draw.rect(screen, (0,0,0), (0,0,screen_width*block_size, screen_height*block_size))

        pygame.display.update()

main()