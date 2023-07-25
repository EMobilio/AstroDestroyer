import pygame, os
from sys import exit
from player import *

# Constants
WIDTH = 800
HEIGHT = 900
FPS = 60

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstroDestroyer")
clock = pygame.time.Clock()
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "SpaceBackGround.jpg")), (800, 900))

# Sprites
player = pygame.sprite.GroupSingle()
player.add(Player())

def draw_screen():
    """ Draws the current state of the screen """
    screen.blit(bg, (0, 0))
    player.draw(screen)
    player.update()
    pygame.display.update()

def main():
    """ Main game loop """
    run = True

    while run:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


        draw_screen()
        clock.tick(FPS)

if __name__ == "__main__":
    main()