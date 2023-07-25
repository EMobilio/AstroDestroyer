import pygame, os

class Player(pygame.sprite.Sprite):
    """ Class for Player sprite objects that inherits from the pygame Sprite class """

    VELOCITY = 5

    def __init__(self):
        """ Initializer for Player objects which sets the frames, the frame_index, the rectangle,
            and the current player image
        """
        super().__init__()
        ship_frame_1 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "ship_frame_1.png")), (100, 100))
        ship_frame_2 = pygame.transform.scale(pygame.image.load(os.path.join("assets", "ship_frame_2.png")), (100, 100))
        self.ship_frames = [ship_frame_1, ship_frame_2]
        self.frame_index = 0
        self.image = self.ship_frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom=(400, 880))

    def change_animation(self):
        """ Marginally increments the frame_index attribute, assigning it a value of 0 when 
            it exceeds the index range of ship_frames, and sets the image attribute to one of
            the frames in ship_frames based on the integer floor of the frame_index value to create
            a fire animation effect
        """
        self.frame_index += 0.1
        if self.frame_index >= len(self.ship_frames):
            self.frame_index = 0
        self.image = self.ship_frames[int(self.frame_index)]

    def handle_movement(self):
        """ Checks the keys pressed by the user and updates the position of the Player accordingly """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.VELOCITY
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.VELOCITY
            

    def update(self):
        """ Updates the state of the player by calling the change_animation() and handle_movement()
            methods
        """
        self.change_animation()
        self.handle_movement()