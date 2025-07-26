import sys
import pygame
from settings import Settings

class AlienInvasion:
    # this is the overall class to mange the game assets and behavior
    def __init__(self):

        pygame.init()
        self.screen= pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Alien Invasion")
        # set the background color
        self.bg_color= (230, 230, 230)

        # initialize the game, and create game resources
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.setting.screen_width, self.settings.screen_height))

    def run_game(self):
        # start the amin loop for the game
        while True:
            # watch for keyboard and mouse
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    sys.exit()
            # redraw the screen during each pass through the loo
            self.screen.fill(self.settings.bg_color)

            # make the most recently drawn screen visible
            pygame.display.flip()
            self.clock.tick(60)



if __name__ == '__main__':
    # make a game instance, and run the game
    ai= AlienInvasion()
    ai.run_game()
