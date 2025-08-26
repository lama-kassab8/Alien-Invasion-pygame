import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet"""
    def __init__(self, ai_game):
        """Initialize the alien and set its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings= ai_game.settings # create a settings attribute to access the alien's speed 

        # Load the alien image and set its rect attribute
        original_alien = pygame.image.load('/Users/lama/Documents/Alien_Invasion/ALIEN1_0.png')
        self.image= pygame.transform.scale(original_alien, (68, 90))
        self.rect= self.image.get_rect()

        # Start each new alien new the top left of the screen
        self.rect.x = self.rect.width 
        self.rect.y= self.rect.height

        #Store the alien's exact horizontal postion
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if alien is at the edge of the screen"""
        screen_rect= self.screen.get_rect()
        # stop moving the aliens when the aliens reach the right edge of the screen or when they reach the left edge of the screen
        return (self.rect.right >= screen_rect.right) or (self.rect.left <=0) 

    def update(self):
        """Move the alien to the right"""
        # why are we multiplying here? how does this allow motion to the right or left? 
        self.x += self.settings.alien_speed * self.settings.fleet_direction # update the horizontal position of the alien according to where it is after moving to the right  or left in the set speed
        self.rect.x = self.x # use the position of the alien to update the position of the alien's rect
