import pygame, os, random
from sys import exit
from player import *
from bullet import *
from asteroid import *
from title import *

# Game constants
WIDTH = 800
HEIGHT = 900
FPS = 60

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Math operator lambda functions
OPS = {"+": lambda x, y: x+y,
       "-": lambda x, y: x-y,
       "*": lambda x, y: x*y,
       "//": lambda x, y: x//y}

# Math difficulty constants
LEVEL_1 = 1
LEVEL_2 = 2
LEVEL_3 = 3
LEVEL_4 = 4
LEVEL_5 = 5

# Pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstroDestroyer")
clock = pygame.time.Clock()
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "SpaceBackGround.jpg")), (800, 900))
score = 0

# Sprites and groups
title = pygame.sprite.GroupSingle()
title.add(Title(WIDTH, HEIGHT))
player = pygame.sprite.GroupSingle()
player.add(Player())
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
asteroids.add(Asteroid(2))
asteroids.add(Asteroid(2))
asteroids.add(Asteroid(2))
asteroids.add(Asteroid(2))
asteroids.add(Asteroid(2))
asteroids.add(Asteroid(2))

# Images and text
game_font = pygame.font.SysFont("arial", 24)
start_message = game_font.render("PRESS SPACE TO START", False, WHITE)
health_bar = pygame.Rect((30, 30), (player.sprite.health, 30))
health_frame = pygame.Rect((28, 28), (154, 34))
heart = pygame.image.load(os.path.join("assets", "heart.png")).convert_alpha()
bullet_image = pygame.image.load(os.path.join("assets", "bullet.png")).convert_alpha()

def generate_problem(difficulty_level):
    """ Input: difficulty_level- int
        

    """
    if difficulty_level == 1:
        i, j = 1, 20
        k, l = 1, 20
        op_choices = ["+", "-"]
    elif difficulty_level == 2:
        i, j = 30, 50
        k, l = 10, 50
        op_choices = ["+", "-"]
    elif difficulty_level == 3:
        i, j = 10, 20
        k, l = 2, 10
        op_choices = ["*", "//"]
    elif difficulty_level == 4:
        i, j = 30, 100
        k, l = 2, 20
        op_choices = ["*", "//"]
    else:
        i, j = 100, 200
        k, l = 10, 20
        op_choices = ["*", "*", "//"]

    a = random.randint(i, j)
    b = random.randint(k, l)
    op = random.choice(op_choices)
    answer = OPS[op](a, b)
    string = str(a) + " " + op + " " + str(b)
    return (string, answer)

def check_player_collision():
    if pygame.sprite.spritecollide(player.sprite, asteroids, False):
        if pygame.sprite.spritecollide(player.sprite, asteroids, True, pygame.sprite.collide_mask):
            return True
    
    return False

def check_bullet_collision():
    if pygame.sprite.groupcollide(bullets, asteroids, False, False):
        if pygame.sprite.groupcollide(bullets, asteroids, True, True, pygame.sprite.collide_mask):
            return True
        
    return False

    
def draw_screen(game_active):
    """ Draws the current state of the screen """
    screen.blit(bg, (0, 0))
    if game_active:
        player.draw(screen)
        player.update()
        bullets.draw(screen)
        bullets.update()
        asteroids.draw(screen)
        asteroids.update()
        pygame.draw.rect(screen, RED, health_bar)
        pygame.draw.rect(screen, WHITE, health_frame, 2)
        for life in range(player.sprite.lives):
            screen.blit(heart, (28 + 40*life, 70))
        score_text = game_font.render(f"Score: {score}", False, WHITE)
        screen.blit(score_text, (28, 74 + heart.get_height()))
        screen.blit(bullet_image, (28, 78 + heart.get_height() + score_text.get_height()))
        ammo_text = game_font.render(f"x {player.sprite.bullets}", False, WHITE)
        screen.blit(ammo_text, (37 + bullet_image.get_width(), 78 + heart.get_height() + score_text.get_height()))
    else:
        title.draw(screen)
        title.update(HEIGHT)
        screen.blit(start_message, (WIDTH/2 - start_message.get_width()/2, HEIGHT/3 + 100))

    pygame.display.update()

def main():
    """ Main game loop """
    run = True
    game_active = False
    global score

    while run:
        # Event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            
            if game_active:
                # check for player shots
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.sprite.bullets > 0:
                        bullet = Bullet((player.sprite.rect.x + player.sprite.rect.width/2, player.sprite.rect.y + 5))
                        bullets.add(bullet)
                        player.sprite.bullets -= 1
            else:
                # check for game start
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_active = True
                        pygame.time.delay(300)

        if game_active:
            # check and handle player and bullet collisions
            if check_player_collision() == True:
                player.sprite.health -= 30
                if player.sprite.health == 0:
                    player.sprite.lives -= 1
                    if player.sprite.lives == 0:
                        game_active = False
                    else:
                        player.sprite.health = 150

                health_bar.width = player.sprite.health

            if check_bullet_collision() == True:
                score += 10

        draw_screen(game_active)
        clock.tick(FPS)

if __name__ == "__main__":
    main()