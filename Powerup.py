
import constants as const
import Character
import Level
import pygame
from pathlib import Path

class Powerup(pygame.sprite.Sprite):

    '''
    This is the object for all powerups
    '''

    def __init__(self, powerupType, x, y):
        super().__init__()

        self.powerupType = powerupType
        self.x = x
        self.y = y
        self.resx = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        self.resy = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE

        if self.powerupType == const.POWERUP_RANGE:
            imageFile = str(Path.cwd() / "graphics" / "powerup_range.png")
        elif self.powerupType == const.POWERUP_COUNT:
            imageFile = str(Path.cwd() / "graphics" / "powerup_count.png")
        elif self.powerupType == const.POWERUP_BOOT:
            imageFile = str(Path.cwd() / "graphics" / "powerup_boot.png")
        else:
            raise RuntimeError(str(powerupType) + ' is not a valid kind of powerup')

        self.image = pygame.image.load(imageFile).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.resx
        self.rect.y = self.resy


    def update(self):
        pass

    def pickUp(self, player):
        '''This method is called when a PC occupies the same space as a powerup.
        This returns the value of the powerup'''
        return self.powerupType
    
    def destroy(self):
        '''This method is called when a powerup would be destroyed for any reason'''
        pass
