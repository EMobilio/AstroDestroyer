import pygame, os

class Bullet(pygame.sprite.Sprite):

    VELOCITY = 5

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "bullet.png"))
        self.rect = self.image.get_rect(midbottom=pos)

    def handle_movement(self):
        self.rect.y -= self.VELOCITY

    def destroy(self):
        if self.rect.y < -15:
            self.kill()

    def update(self):
        self.handle_movement()
        self.destroy()
