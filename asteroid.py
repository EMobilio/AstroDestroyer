import pygame, os, random

class Asteroid(pygame.sprite.Sprite):
    """ Class for Asteroid sprite objects that inherits from the pygame Sprite class """

    def __init__(self, velocity):
        """ Input: velocity- int
         
            Initializer for Asteroid objects that randomly chooses an image, sets the rect, mask,
            and the velocity with the given argument
        """
        super().__init__()
        type = random.choice(["asteroid_1.png", "asteroid_2.png", "asteroid_3.png", "asteroid_4.png"])
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", type)).convert_alpha(), (100, 100))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottomleft = (random.randint(0, 800 - self.rect.width), random.randint(-450, -50))
        self.velocity = velocity

    def handle_movement(self):
        """ Adds the asteroid's velocity to its y position to move it down the screen """
        self.rect.y += self.velocity

    def destroy(self):
        """ Destroys the Asteroid object """
        self.kill()

    def update(self):
        """ Updates the state of the asteroids by calling the handle_movement() and destroy() methods as needed """
        self.handle_movement()
        # destroy asteroids that go beyond the bottom of the screen
        if self.rect.y > 900:
            self.destroy()