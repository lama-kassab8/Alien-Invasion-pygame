
class Settings:
    # a class to store all settings for alien Invasion
    def __init__(self):
        # screen settings
        self.screen_width= 1200 # set the width of the game's window to 1200 pixels
        self.screen_height= 800 # set the height of the game's window to 800 pixels
        self.bg_color= (230, 230, 230) # make the backgroud color light grey
        # ship settings
        self.ship_speed= 6.5 # set the speed of the ship's movement to 6.5 pixels per frame, since it's a 60 fps game, the ship moves 390 pixels per second
        self.ship_limit = 3 # limit the number of ships to three, so the player has 3 lives to spare before game is over.
        # bullet settings
        self.bullet_speed= 14.0 # set the speed of the bullet's movement to 14 pixels per frame, meaning a bullet moves 840 pixels per second
        self.bullet_width= 3 # set the width of the created bullet
        self.bullet_height= 15 # set the height of the created bullet
        self.bullet_color= (60,60,60) # set the color of the bullet to dark grey
        self.bullets_allowed= 3 # limit the number of bullets a player can shoot
        # Alien settings
        self.alien_speed = 2.0 #set the speed of the alien to move 2 pixels per frame
        self.fleet_drop_speed = 10 # set the speed of the fleet of alien when it moves downward to 10 pixels per frame
        # Fleet_direction of 1 represents moving to the right
        self.fleet_direction = 1
