import pygame, os

class Bullet(pygame.sprite.Sprite):
    """ Class for Bullet sprite objects that inherits from the pygame Sprite class """

    VELOCITY = 5

    def __init__(self, pos):
        """ Input: pos- tuple of ints 
        
            Initializer for Bullet objects that sets the image, mask and rect of the object with the position
            from the pos argument
        """
        super().__init__()
        self.image = pygame.image.load(os.path.join("assets", "graphics", "bullet.png")).convert_alpha()
        self.rect = self.image.get_rect(midbottom=pos)
        self.mask = pygame.mask.from_surface(self.image)

    def handle_movement(self):
        """ Subtracts the bullets's velocity from its y position to move it up the screen """
        self.rect.y -= self.VELOCITY

    def destroy(self):
        """ Destroys the Bullet object """
        self.kill()

    def update(self):
        """ Updates the state of the bullets by calling the handle_movement() and destroy() methods as needed """
        self.handle_movement()
        # destroy bullets that go beyond the top of the screen
        if self.rect.y < -10:
            self.destroy()
