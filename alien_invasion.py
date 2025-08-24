import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
### does the order of imports matter?


class AlienInvasion:
    # this is the overall class to mange the game assets and behavior
    def __init__(self):

        pygame.init()
        self.settings= Settings()
        #--- this chunck is for making the game playable in full screen
        self.fullscreen = False  # Start in windowed mode by default
        self.settings.screen_width = 1200
        self.settings.screen_height = 800
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #---
        pygame.display.set_caption("Alien Invasion")
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        self.stats= GameStats(self)# create an instance to store game statistics
        self.ship= Ship(self)
        self.bullets= pygame.sprite.Group()

        self.aliens= pygame.sprite.Group()
        self.create_fleet()
        # set the background color
        self.bg_color= (230, 230, 230)

        # initialize the game, and create game resources
        self.clock = pygame.time.Clock()
        # start Alien Invasion in an inactive state
        self.game_active= False
        self.play_button = Button(self, "Play") # make the play button
        

    def run_game(self):
        # start the amin loop for the game
        while True:
            self._check_events()
            if self.game_active: # as long as game_active is True
                self.ship.update()
                self.update_bullets()
                print(len(self.bullets))
                self.update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        # respond to keypresses and mouse events
        # watch for keyboard and mouse
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN: # when the pygame detects a MOUSEBUTTONDOWN event, it means the player clicked on a button
                    mouse_pos = pygame.mouse.get_pos() # the mouse.get_pos returns a tuple, containing the mouse cursor's x and y coordinates when the mouse is clicked
                    self.check_play_button(mouse_pos) # send the values of the cursor's coordinates stored in get_pos to the method check_play_button
                elif event.type == pygame.KEYDOWN:
                    self.check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self.check_keyup_events(event)


    def check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)# take notice of the cursor when it clicks in the button's rect and store this incident to button_clicked
        if button_clicked and not self.game_active: # if the button is clicked while the game is active (the not game_active is because the default value of the game_active is False(inactive) and here we want to check that it's not True (active))
            self.stats.reset_stats() # reset the game statistics
            self.game_active= True
            # get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # create a new fleet and center the ship
            self.create_fleet()
            self.ship.center_ship()

    def toggle_fullscreen(self):
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
            self.fullscreen = True
        else:
            self.settings.screen_width = 1200
            self.settings.screen_height = 800
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            self.fullscreen = False
        # fix the ship's position after resizing
        self.ship.center_ship()

    def check_keydown_events(self, event):
        # respond to keypresses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right= True
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left= True
            elif event.key ==pygame.K_q:
                sys.exit()
            elif event.key == pygame.K_SPACE:
                self.fire_bullet()
            elif event.key == pygame.K_f:
                self.toggle_fullscreen()
    
    def check_keyup_events(self, event):
        # respond to key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                self.ship.moving_right= False
            elif event.key == pygame.K_LEFT:
                self.ship.moving_left= False

    def fire_bullet(self):
        # create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet= Bullet(self)
            self.bullets.add(new_bullet)

    def update_bullets(self):
        # update position of bullets and get rid of old bullets
        self.bullets.update()
            # get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <=0:
                self.bullets.remove(bullet)
        self.check_bullet_alien_collisions()
        
        
    def check_bullet_alien_collisions(self):
        """REspond to bullet-alien collisions"""
        # check for any bullets that have hit aliens
        # if so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide( self.bullets, self.aliens, True, True)
        # remove any bullets and aliens that have collided
        if not self.aliens:
            self.bullets.empty() # destroy existing bullets 
            self.create_fleet() # create new fleet


    def update_aliens(self):
        """Check if the fleet is at an edge, then update the positions of all aliens in the fleet"""
        self.check_fleet_edges() # check if the fleet reached the edge via the check_fleet_edges method
        self.aliens.update() # call the update method in the alien class to update the positon of the aliens after movement
        # look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens): # if any alien hits the ship, consider it a collision
            print("Ship hit!!!")
            self.ship_hit() # after the ship gets hit, the method resets the stats
            # look for aliens hitting the bottom of the screen
            self.check_aliens_bottom()


    def _update_screen(self):
        # update images on the screen, and flip to the new screen
        # redraw the screen during each pass through the loo
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()
        # make the most recently drawn screen visible
        pygame.display.flip()

    def create_fleet(self):
        """Create the fleet of aliens"""

        # Create an alien and keep adding aliens until there's no room left
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height # set current_x to be the width of the alien and current_y to be the height of the alien
        # Keep adding aliens as long as there's enough space for two alien's height as one space will be filled with an alien and the next is the empty space between the rows of aliens
        while current_y < (self.settings.screen_height - 3 * alien_height):
        # Keep adding aliens as long as there's enough space for two alien's width as one space will be filled with an alien and the next is the empty space betwee teh columns of aliens
            while current_x < (self.settings.screen_width -2 * alien_width): 
                self.create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # Finished a row; reset x value, and increment y value
            current_x = alien_width # Why do we need to write this line of code again?
            current_y += 2 * alien_height # Set the width of the space between aliens to be the width of the alien
    
    def check_fleet_edges(self):
        """Respond appropiately if any aliens have reached an edge"""
        for alien in self.aliens.sprites():
            if alien.check_edges(): # when the aliens reach the edges
                self.change_fleet_direction() # move the aliens per the specified movements in the change_fleet_direction method
                break
    
    def change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction"""
        for alien in self.aliens.sprites(): # for every alien in the list of aliens, change its position
            alien.rect.y += self.settings.fleet_drop_speed # make the entire line of aliens drop downward according to the set speed for dropping down the screen
        self.settings.fleet_direction *= -1 # move the aliens to the left once they're dropped

    def create_alien(self, x_position, y_position): # this method takes as argument the x-value which specifies where the alien should be placed
        """Create an alien and place it in the row"""
        new_alien =Alien(self) # create a new alien
        new_alien.x = x_position # add a space the width of an alien to be placed after the current alien
        new_alien.rect.x = x_position # set the the rect of the new alien to be the same size and position of the added alien
        new_alien.rect.y = y_position # set the the rect of the new alien to be the same size and position of the added alien
        self.aliens.add(new_alien) # add the new alien to the list (fleet) of aliens


    def ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0: # as long as the amount of ships left is bigger than 0, do the following:
            self.stats.ships_left -=1 # decrement the number of ships left
            # get rid of any remaning bullets and aliens
            self.bullets.empty()
            self.aliens.empty()
            # create a new fleet and center the ship
            self.create_fleet()
            self.ship.center_ship()
            # pause
            sleep(0.5)
        else: # once the player runs out of lives, end the game
            self.game_active= False

    
    def check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.sceen_height:
                # treat it the same as if the ship got hit
                self.ship_hit()
                break

if __name__ == '__main__':
    # make a game instance, and run the game
    ai= AlienInvasion()
    ai.run_game()
