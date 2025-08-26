import pygame

class Ship:
    # a class to manage the ship
    def __init__(self, ai_game):
        # initialize the ship and set its starting position
        self.screen = ai_game.screen # set the Pygame screen surface using the instance ai_game
        # get_rect is a function that provides a rectangle object, its size is the size of the screen we set in settings
        # get_rect represent the whole screen, not just its size but also its position and edges, this allows us to control the movement of elements that appear on the screen
        # it handles the maths for us as it automatically calculates the values of the position of items relative to the edges of the screen 
        self.screen_rect = ai_game.screen.get_rect() 
        self.settings= ai_game.settings # implement the settings we set in the Settings class

        # load the ship image and get its rect
        original_image =pygame.image.load('/Users/lama/Documents/Alien_Invasion/ship6_0.png') # load the image 
        self.image= pygame.transform.scale(original_image, (100, 78)) # change the dimensions of the original image
        self.rect = self.image.get_rect() # get_rect boxes the image in a rectangle for easier and accessable navigations

        # start each new ship at the bottom center of the screen
        self.rect.midbottom= self.screen_rect.midbottom
        self.x = float(self.rect.x) # get_rect uses integers but we're working with floats for precise measurements and smoother movements
        # movement flag; start with a ship that's not moving
        self.moving_right= False
        self.moving_left= False

    def update(self):
        # update the ship's position based on the movement flag
        if self.moving_right and self.rect.right < self.screen_rect.right: # make sure that the ship does not move outside the right edges of the screen
            self.x += self.settings.ship_speed # update the ship's position after each press of the right arrow key
        if self.moving_left and self.rect.left >0: # make sure the ship doesn't move ouside the left edge of the screen
            self.x -= self.settings.ship_speed # update the ship's position after each press of the left arrow key
        self.rect.x= self.x # update the actual postion of the ship (self.x) based on the float value we're tracking
        
    def blitme(self):
        # draw the ship at its current location
        # blit() function, short for bit block transfer, draws an image (surface) onto another surface
        self.screen.blit(self.image, self.rect) # it draws the image at the position stored in self.rect after each postion change

    def center_ship(self):
        """Center the ship on the screen"""
        self.rect.midbottom = self.screen.get_rect().midbottom # places the ship at the middle bottom part of the screen
        self.x = float(self.rect.x) # reset the self.x attribute after centering the ship to track the ship's exact position again 
