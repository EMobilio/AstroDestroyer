import pygame, os

class Title(pygame.sprite.Sprite):

    def __init__(self, screen_w, screen_h):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "title.png")).convert_alpha(), (730, 70))
        self.rect = self.image.get_rect(center=(screen_w/2, screen_h/3))
        self.velocity = -1

    def update(self, screen_h):
        if self.rect.center[1] <= screen_h/3 - 10:
            self.velocity = 1
        elif self.rect.center[1] >= screen_h/3:
            self.velocity = -1

        if self.velocity > 0:
            pygame.time.delay(70)
        else:
            pygame.time.delay(50)

        self.rect.y += self.velocity
