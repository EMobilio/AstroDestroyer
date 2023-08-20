import pygame, os, random
from sys import exit
from player import Player
from bullet import Bullet
from asteroid import Asteroid
from title import Title

# Game constants
WIDTH = 800
HEIGHT = 900
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (160, 160, 160)
LIGHT_GRAY = (224, 224, 244)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
LIGHT_BLUE = (0, 102, 204)

# Math operator lambda functions
OPS = {"+": lambda x, y: x+y,
       "-": lambda x, y: x-y,
       "*": lambda x, y: x*y,
       "/": lambda x, y: x/y}

# Pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AstroDestroyer")
clock = pygame.time.Clock()
asteroid_timer = pygame.USEREVENT + 1
problem_timer = pygame.USEREVENT + 2

# Sprites and groups
title = pygame.sprite.GroupSingle()
title.add(Title(WIDTH, HEIGHT))
player = pygame.sprite.GroupSingle()
player.add(Player())
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()

# Surfaces
bg = pygame.transform.scale(pygame.image.load(os.path.join("assets", "SpaceBackGround.jpg")), (800, 900))
game_font = pygame.font.SysFont("arial", 24)
problem_font = pygame.font.SysFont("arial", 36)
answer_font = pygame.font.SysFont("arial", 16)
highscore_font = pygame.font.SysFont("arial", 44)
game_over_image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "game_over.png")).convert_alpha(), (594, 78))
start_message = game_font.render("PRESS SPACE TO START", False, WHITE)
retry_message = game_font.render("PRESS SPACE TO RETRY", False, WHITE)
new_highscore_message = highscore_font.render("NEW HIGH SCORE!", False, GREEN)
health_bar = pygame.Rect((30, 30), (player.sprite.health, 30))
health_frame = pygame.Rect((28, 28), (154, 34))
heart = pygame.image.load(os.path.join("assets", "heart.png")).convert_alpha()
bullet_image = pygame.image.load(os.path.join("assets", "bullet.png")).convert_alpha()
math_window = pygame.Rect((0, 0), (400, 200))
math_window.center = (WIDTH/2, HEIGHT/2)
input_bar = pygame.Rect((0, 0), (100, 25))
input_bar.center = (WIDTH/2, HEIGHT/2)
input_border = pygame.Rect((0, 0), (102, 27))
input_border.center = (WIDTH/2, HEIGHT/2)


def load_highscore():
    """ Opens highscore.txt in a+ mode (creates it if it doesn't exist) and reads and returns
        the player's high score, or 0 if there is no high score yet
    """
    with open("highscore.txt", "a+") as file:
        file.seek(0)
        highscore = file.read()

    if highscore == '':
        return 0

    return int(highscore)


def update_highscore(score):
    """ Input: score- int
    
        Opens highscore.txt in w mode and writes the given score to it, repalcing the old one
    """
    with open("highscore.txt", "w") as file:
        file.write(str(score))


def handle_highscore(score):
    """ Input: score- int
     
        Gets the current high score using load_highscore() and compares it to the given score,
        updating the high score using updating_highscore() if the given score is greater. Returns
        a tuple containing the given score, the current highscore (as determined in the function), and
        a boolean value indicating whether there is a new high score
    """
    new_highscore = False
    highscore = load_highscore()
    if score > highscore:
        new_highscore = True
        update_highscore(score)
        highscore = score

    return (score, highscore, new_highscore)


def generate_problem(difficulty_level):
    """ Input: difficulty_level- int
        
        Generates a random math equation with operations and number sizes based on the difficulty_level
        argument and returns a string representation of the problem and the answer in a tuple
    """
    # choose integer ranges and operations based on difficulty_level
    if difficulty_level == 1:
        i, j = 1, 20
        k, l = 1, 20
        op_choices = ["+", "-"]
    elif difficulty_level == 2:
        i, j = 30, 50
        k, l = 10, 50
        op_choices = ["+", "-"]
    elif difficulty_level == 3:
        i, j = 10, 30
        k, l = 5, 10
        op_choices = ["*", "/"]
    elif difficulty_level == 4:
        i, j = 30, 100
        k, l = 5, 20
        op_choices = ["*", "/"]
    else:
        i, j = 100, 200
        k, l = 10, 20
        op_choices = ["*", "*", "/"]

    a = random.randint(i, j)
    b = random.randint(k, l)
    op = random.choice(op_choices)
    # if division problem, keep generating integers until they divide evenly
    if op == "/":
        while (a % b != 0):
            a = random.randint(i, j)
            b = random.randint(k, l)
    answer = int(OPS[op](a, b))
    string = str(a) + " " + op + " " + str(b)
    return (string, answer)


def math_problem(difficulty_level):
    """ Input: difficulty_level- int

        Calls generate_problem() to generate a math problem based on difficulty_level and starts a new
        loop to display the problem on the screen and handle user input, checking whether the user gave
        the correct answer and displaying appropriate messages and updating the player's bullet count if
        they did
    """
    problem = generate_problem(difficulty_level)
    problem_text = problem_font.render(f"What is {problem[0]}?", False, BLACK)
    problem_pause = True
    answered = False
    user_answer = ""

    while problem_pause:
        # event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()

            # check for digit, delete and return input 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_answer = user_answer[:-1]

                if (len(user_answer) < 10 and 
                    event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_MINUS]):
                    user_answer += event.unicode

                if event.key == pygame.K_RETURN and user_answer != "":
                    answered = True
                    
        # draw the math window
        pygame.draw.rect(screen, GRAY, math_window, border_radius=20)
        screen.blit(problem_text, (WIDTH/2 - problem_text.get_width()/2, HEIGHT/2 - problem_text.get_height()/2 - 50))
        pygame.draw.rect(screen, LIGHT_GRAY, input_bar)
        pygame.draw.rect(screen, LIGHT_BLUE, input_border, 1)
        answer_text = answer_font.render(user_answer, False, BLACK)
        screen.blit(answer_text, (WIDTH/2 - input_bar.width/2 + 2, HEIGHT/2 - answer_text.get_height()/2))

        # once the user submits an answer, update the window and game variables accordingly and break the loop
        if answered:
            if int(user_answer) == problem[1]:
                player.sprite.bullets += 40
                message = "Correct!"
                color  = GREEN
                new_bullet_text = problem_font.render("+40", False, GREEN)
                screen.blit(new_bullet_text, (WIDTH/2 - new_bullet_text.get_width()/2 + math_window.width/4, HEIGHT/2 - new_bullet_text.get_height()/2 + math_window.height/4))
                screen.blit(pygame.transform.scale(bullet_image, (22, 44)), (WIDTH/2 + math_window.width/4 + new_bullet_text.get_width()/2 + 3, HEIGHT/2 - 2*bullet_image.get_height()/2 + math_window.height/4))
            else:
                message = "Incorrect"
                color = RED
            
            message_text = problem_font.render(message, False, color)
            if message == "Incorrect": x_pos = WIDTH/2 - message_text.get_width()/2 
            else: x_pos = WIDTH/2 - message_text.get_width()/2 - math_window.width/4
            screen.blit(message_text, (x_pos, HEIGHT/2 - message_text.get_height()/2 + math_window.height/4))
            pygame.display.update()
            pygame.time.delay(2000)
            break

        pygame.display.update()
        clock.tick(FPS)


def check_player_collision():
    """ Returns True if any asteroids are colliding with the player, destroying any that are, and False otherwise """
    # first check using rect collision detection to avoid constant mask detection and improve performance
    if pygame.sprite.spritecollide(player.sprite, asteroids, False):
        if pygame.sprite.spritecollide(player.sprite, asteroids, True, pygame.sprite.collide_mask):
            return True
    
    return False


def check_bullet_collision():
    """ Returns True if any sprites in the bullets and asteroids groups are colliding, destroying
        any that are, and False otherwise 
    """
    # first check using rect collision detection to avoid constant mask detection and improve performance
    if pygame.sprite.groupcollide(bullets, asteroids, False, False):
        if pygame.sprite.groupcollide(bullets, asteroids, True, True, pygame.sprite.collide_mask):
            return True
        
    return False


def reset_game():
    """ Resets the game variables to their initial state """
    player.sprite.lives = 3
    player.sprite.health = 150
    player.sprite.bullets = 30
    player.sprite.rect.midbottom = (400, 880)
    player.sprite.score = 0
    health_bar.width = player.sprite.health
    pygame.time.set_timer(asteroid_timer, 1500)
    asteroids.empty()
    bullets.empty()
    pygame.time.delay(300)


def draw_screen(game_active, game_over, **kwargs):
    """ Inputs: game_active- boolean
                game_over- boolean
                **kwargs- will contain integers values for the last score and the high score and
                          a boolean indicating if there is a new high score
    
        Draws the current state of the screen based on the arguments
    """
    screen.blit(bg, (0, 0))
    # draw the main game screen
    if game_active:
        player.draw(screen)
        player.update()
        bullets.draw(screen)
        bullets.update()
        asteroids.draw(screen)
        asteroids.update(player)
        pygame.draw.rect(screen, RED, health_bar)
        pygame.draw.rect(screen, WHITE, health_frame, 2)
        for life in range(player.sprite.lives):
            screen.blit(heart, (28 + 40*life, 70))
        score_text = game_font.render(f"Score: {player.sprite.score}", False, WHITE)
        screen.blit(score_text, (28, 74 + heart.get_height()))
        screen.blit(bullet_image, (28, 78 + heart.get_height() + score_text.get_height()))
        ammo_text = game_font.render(f"x {player.sprite.bullets}", False, WHITE)
        screen.blit(ammo_text, (37 + bullet_image.get_width(), 78 + heart.get_height() + score_text.get_height()))
    # draw the game over screen
    elif game_over:
        screen.blit(game_over_image, (WIDTH/2 - game_over_image.get_width()/2, HEIGHT/4))
        score_text = problem_font.render(f"Score: {kwargs['score']}", False, WHITE)
        highscore_text = problem_font.render(f"High Score: {kwargs['highscore']}", False, WHITE)
        screen.blit(score_text, (WIDTH/2 - highscore_text.get_width()/2, HEIGHT/3 + 70))
        screen.blit(highscore_text, (WIDTH/2 - highscore_text.get_width()/2, HEIGHT/3 + 80 + score_text.get_height()))
        screen.blit(retry_message, (WIDTH/2 - retry_message.get_width()/2, HEIGHT/3 + 130 + score_text.get_height() + highscore_text.get_height()))
        if kwargs['new_highscore'] == True:
            screen.blit(new_highscore_message, (WIDTH/2 - new_highscore_message.get_width()/2, HEIGHT/3 + 300))
    # draw the title screen
    else:
        title.draw(screen)
        title.update(HEIGHT)
        screen.blit(start_message, (WIDTH/2 - start_message.get_width()/2, HEIGHT/3 + 100))

    pygame.display.update()


def main():
    """ Main game loop """
    run = True
    game_active = False
    game_over = False
    new_highscore = False
    score = 0
    highscore = 0

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

                # check for asteroid spawn event; increase asteroid speed as score increases
                if event.type == asteroid_timer:
                    if player.sprite.score < 0:
                        asteroids.add(Asteroid(1))
                    else:
                        asteroids.add(Asteroid(1 + player.sprite.score//250))
 
                # check for problem generation event; increase problem difficulty as score increases
                if event.type == problem_timer:
                    if player.sprite.score < 0:
                        math_problem(1)
                    else:
                        math_problem(min(1 + player.sprite.score // 500, 5))
                    pygame.time.set_timer(problem_timer, 45000)

            else:
                # check for game start
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.time.delay(300)
                        game_active = True
                        game_over = False
                        pygame.time.set_timer(asteroid_timer, 1500)
                        pygame.time.set_timer(problem_timer, 45000)

        if game_active:
            # check and handle player collisions
            if check_player_collision() == True:
                player.sprite.health -= 30
                if player.sprite.health == 0:
                    player.sprite.lives -= 1
                    # reset game variables when out of lives, otherwise reset health for new life
                    if player.sprite.lives == 0:
                        health_bar.width = player.sprite.health
                        draw_screen(game_active, game_over)
                        score, highscore, new_highscore = handle_highscore(player.sprite.score)
                        game_active = False
                        game_over = True
                        reset_game()
                        pygame.time.delay(1000)
                    else:
                        player.sprite.health = 150
                health_bar.width = player.sprite.health

            # check and handle bullet collisions
            if check_bullet_collision() == True:
                player.sprite.score += 10
                # speed up the asteroid timer with every 250 points earned
                if (player.sprite.score % 250 == 0 or player.sprite.score % 250 == 5) and player.sprite.score != 0:
                    draw_screen(game_active, game_over)
                    pygame.time.set_timer(asteroid_timer, max(1500 - 100*(player.sprite.score//250), 500))

            # reset game if no more ammo
            if player.sprite.bullets == 0 and not bullets:
                draw_screen(game_active, game_over)
                score, highscore, new_highscore = handle_highscore(player.sprite.score)
                game_active = False
                game_over = True
                reset_game()
                pygame.time.delay(1000)

        # if player lost, call draw_screen with scoring arguments
        if game_over:
            draw_screen(game_active, game_over, score=score, highscore=highscore, new_highscore=new_highscore)
        else:
            draw_screen(game_active, game_over)
        clock.tick(FPS)

if __name__ == "__main__":
    main()