import pygame, os, random

class Asteroid(pygame.sprite.Sprite):
    """ Class for Asteroid sprite objects that inherits from the pygame Sprite class """

    def __init__(self, velocity):
        """ Input: velocity- int
         
            Initializer for Asteroid objects that randomly chooses an image, sets the rect, mask,
            and the velocity with the given argument. Also sets a sound for when an asteroid goes
            off screen and points are lost
        """
        super().__init__()
        type = random.choice(["asteroid_1.png", "asteroid_2.png", "asteroid_3.png", "asteroid_4.png", "asteroid_5.png", "asteroid_6.png"])
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "graphics", type)).convert_alpha(), (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (random.randint(0, 800 - self.rect.width), random.randint(-500, 0))
        self.velocity = velocity
        self.point_loss_sound = pygame.mixer.Sound(os.path.join("assets", "audio", "point_loss.mp3"))

    def handle_movement(self):
        """ Adds the asteroid's velocity to its y position to move it down the screen """
        self.rect.y += self.velocity

    def destroy(self):
        """ Destroys the Asteroid object """
        self.kill()

    def update(self, player):
        """ Input: player- GroupSingle sprite group

            Updates the state of the asteroids by calling the handle_movement() and destroy() methods as needed.
            If an asteroid moves beyond the bottom of the screen, it is destroyed and the player score is reduced
            by 15
        """
        self.handle_movement()
        # destroy asteroids that go beyond the bottom of the screen
        if self.rect.y > 900:
            player.sprite.score -= 15
            self.point_loss_sound.play()
            self.destroy()