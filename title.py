import pygame, os

class Title(pygame.sprite.Sprite):
    """ Class for Title sprite objects that inherits from the pygame Sprite class """

    def __init__(self, screen_w, screen_h):
        """ Inputs: screen_w- int
                    screen_h- int
                    
            Initializes Title objects with the title image, a rect positioned using the given screen_w
            and screen_h (width and height of the screen) arguments, and an initial velocity
        """
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("assets", "graphics", "title.png")).convert_alpha(), (730, 70))
        self.rect = self.image.get_rect(center=(screen_w/2, screen_h/3))
        self.velocity = -1

    def update(self, screen_h):
        """ Inputs: screen_h- int

            Updates the state of the Title by checking which direction it should move, updating the
            velocity accordingly, and adding the velocity to the rect's y position
        """
        # checking if the title should move up or down
        if self.rect.center[1] <= screen_h/3 - 10:
            self.velocity = 1
        elif self.rect.center[1] >= screen_h/3:
            self.velocity = -1

        # create a delay to slow down the animation
        if self.velocity > 0:
            pygame.time.delay(70)
        else:
            pygame.time.delay(50)

        self.rect.y += self.velocity
