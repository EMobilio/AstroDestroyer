import pygame, os, random

class Asteroid(pygame.sprite.Sprite):

    def __init__(self, velocity):
        super().__init__()
        type = random.choice(["asteroid_1.png", "asteroid_2.png", "asteroid_3.png", "asteroid_4.png"])
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", type)).convert_alpha(), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.inflate_ip(0, -40)
        self.rect.bottomleft = (random.randint(0, 800 - self.rect.width), random.randint(-450, -50))
        self.velocity = velocity

    def handle_movement(self):
        self.rect.y += self.velocity

    def destroy(self):
        self.kill()

    def update(self):
        self.handle_movement()
        if self.rect.y > 900:
            self.destroy()