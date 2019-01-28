import constants as const
import Level
import Wall
import Bomb
import random
import math
from pathlib import Path
import pygame


class Character(pygame.sprite.Sprite):

    '''
    This class encompasess all characters (Player and Enemy)
    PlayerCharacter and Emeny are subclasses
    '''

    def __init__(self, x, y, facing, speed, kind):
        '''Constructor'''
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.xres = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE#init this by running self.x through the grid_to_res conversion function
        self.yres = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE#same but for y
        self.speed = speed
        self.facing = facing
        self.kind = kind
        self.state = const.STATE_IDLE
        #if kind == const.PC:
            #self.Player = self.PlayerCharacter()
        #elif kind == const.ENEMY:
            #self.Enemy = self.Enemy()
        #else:
            #raise RuntimeError(kind + ' is not a valid kind of character')
        
        
    def move(self, direction, level):
        '''
        Controls movement of a character. Takes a direcetion as input, if character
        is able to move in that direction, will update the character's position and 
        facing. Else, will just update facing.
        ''' 
        layout = level.layout
        self.facing = direction
        pathBlocked = False

        
        if direction == const.UP:
            if self.y > 0 and not isinstance(layout[self.y - 1][self.x], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_DOWN):
                self.y -= 1
                self.state = const.STATE_MOVING_UP
            else:
                pathBlocked = True
        elif direction == const.DOWN:
            if self.y < const.MAP_HEIGHT - 1 and not isinstance(layout[self.y + 1][self.x], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_UP):
                self.y += 1
                self.state = const.STATE_MOVING_DOWN
            else:
                pathBlocked = True
        elif direction == const.LEFT:
            if self.x > 0 and not isinstance(layout[self.y][self.x - 1], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_RIGHT):
                self.x -= 1
                self.state = const.STATE_MOVING_LEFT
            else:
                pathBlocked = True
        elif direction == const.RIGHT:
            if self.x < const.MAP_WIDTH - 1 and not isinstance(layout[self.y][self.x + 1], Wall.Wall) and (self.state == const.STATE_IDLE or self.state == const.STATE_MOVING_LEFT):
                self.x += 1
                self.state = const.STATE_MOVING_RIGHT
            else:
                pathBlocked = True

        if self.kind == const.PC and not pathBlocked:
            self.changeDirection(direction)
        return pathBlocked

        #checks if able to move in direction
        #if no, stays in same square, but update self.facing
        #if yes, move to correct square and update self.facing
        
        
    def update(self, level, player = None):
        '''
        Updates character position when a character is moving towards a grid position
        '''
        if self.kind == const.ENEMY and self.state == const.STATE_IDLE:
            if self.logic == const.RANDOM:
                self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
                self.move(self.direction, level)
            elif self.logic == const.BASIC:
                pathBlocked = self.move(self.direction, level)
                if pathBlocked or random.randint(0, 50) > 45:   #enemy walks until path blocked, or randomly decides to turn
                    self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
                    self.move(self.direction, level)
            elif self.logic == const.ADVANCED and player != None:
                if abs(self.x - player.x) < const.ADVANCED_ENEMY_RANGE and abs(self.y - player.y) < const.ADVANCED_ENEMY_RANGE:
                    self.pursuePlayer = True
                    self.speed = const.SPEED_HIGH
                if self.pursuePlayer:
                    self.advancedMovement(level, player)
                else:
                    pathBlocked = self.move(self.direction, level)
                    if pathBlocked or random.randint(0, 50) > 45:   #enemy walks until path blocked, or randomly decides to turn
                        self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
                        self.move(self.direction, level)
        
        xDest = const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE
        yDest = const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE
        
        if self.state == const.STATE_MOVING_UP:
            if self.yres > yDest:
                self.yres -= self.speed
            else:
                self.yres = yDest
                self.state = const.STATE_IDLE
                
        if self.state == const.STATE_MOVING_DOWN:
            if self.yres < yDest:
                self.yres += self.speed
            else:
                self.yres = yDest
                self.state = const.STATE_IDLE
                
        if self.state == const.STATE_MOVING_LEFT:
            if self.xres > xDest:
                self.xres -= self.speed
            else:
                self.xres = xDest
                self.state = const.STATE_IDLE
                
        if self.state == const.STATE_MOVING_RIGHT:
            if self.xres < xDest:
                self.xres += self.speed
            else:
                self.xres = xDest
                self.state = const.STATE_IDLE
                
        self.rect.x = self.xres
        self.rect.y = self.yres
        
        #temporary means to handle the image size difference (from tilesize) for the bman image
        if self.kind == const.PC:
            #self.changeDirection(self.facing)
            self.hitbox.x = self.rect.x + const.HIT_BOX_OFFSET_X - 2
            self.hitbox.y = self.rect.y + 4
            self.rect.x += 0#8
            self.rect.y -= 16
        else:
            self.hitbox.x = self.rect.x + const.HIT_BOX_OFFSET_X / 2
            self.hitbox.y = self.rect.y + const.HIT_BOX_OFFSET_Y / 2


    def advancedMovement(self, level, player):
        pathsBlocked = 0
        if self.x > player.x:
            self.direction = const.LEFT
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        elif self.x < player.x:
            self.direction = const.RIGHT
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        elif self.y > player.y:
            self.direction = const.UP
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        elif self.y < player.y:
            self.direction = const.DOWN
            pathBlocked = self.move(self.direction, level)
            if pathBlocked:
                pathsBlocked += 1
        if pathsBlocked > 0 or self.direction == None:
            self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
            self.move(self.direction, level)


class PlayerCharacter(Character):
    
    '''
    This object is for the player's character. Only one
    should be instantiated.
    '''
    
    def __init__(self, level, x, y):
        '''Constructor'''
        facing = const.DOWN
        super().__init__(x, y, facing, const.PLAYER_SPEED, const.PC)
        self.bombCount = 1
        self.bombRange = 1
        #self.speed = 40 #placeholder
        self.activeBombs = 0
        self.boot = False
        
        
        #imageFile = str(Path.cwd() / "graphics" / "player_bman.png")
        #self.image = pygame.image.load(imageFile).convert_alpha()

        imageFile = str(Path.cwd() / "graphics" / "Left.png")
        self.left = pygame.image.load(imageFile).convert_alpha()

        imageFile = str(Path.cwd() / "graphics" / "Right.png")
        self.right = pygame.image.load(imageFile).convert_alpha()

        imageFile = str(Path.cwd() / "graphics" / "Front.png")
        self.front = pygame.image.load(imageFile).convert_alpha()

        imageFile = str(Path.cwd() / "graphics" / "Back.png")
        self.back = pygame.image.load(imageFile).convert_alpha()

        self.image = self.front


        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-const.HIT_BOX_OFFSET_X, -const.HIT_BOX_OFFSET_Y)
        self.deathSound = pygame.mixer.Sound(str(Path.cwd() / "sounds" / "yell.wav"))

    def dropBomb(self):
        '''Creates an instance of the bomb class at the PC's position'''
        xDiff = abs(self.xres - (const.SCREEN_OFFSET_X_LEFT + self.x * const.TILE_SIZE))
        yDiff = abs(self.yres - (const.SCREEN_OFFSET_Y_TOP + self.y * const.TILE_SIZE))
        if xDiff < 10 and yDiff < 10:# and self.activeBombs < self.bombCount:
            newBomb = Bomb.Bomb(self.x, self.y, self.bombRange)
            self.changeBombCount(1)
            return newBomb
        else:
            return None

    def changeBombCount(self,change):
        '''This method is how to change the value of self.activeBombs
        will be called by dropBomb method of the PlayerCharacter, and
        the explode method of the Bomb
        '''
        self.activeBombs = self.activeBombs + change

    def getPowerup(self,powerup):
        '''This method is called when the PC occupies the same space as a 
        powerup. 
        '''
        if powerup == const.RANGE and self.bombRange < 5:
            self.bombRange += 1
        elif powerup == const.COUNT and self.bombCount < 5:
            self.bombCount += 1
        elif powerup == const.BOOT:
            self.boot = True
    
    def changeDirection(self,direction):
        if direction == const.RIGHT and self.image != self.right: #and self.state == const.STATE_IDLE:
            self.image = self.right
        if direction == const.LEFT and self.image != self.left: #and self.state == const.STATE_IDLE:
            self.image = self.left
        if direction == const.UP and self.image != self.back: #and self.state == const.STATE_IDLE:
            self.image = self.back
        if direction == const.DOWN and self.image != self.front:# and self.state == const.STATE_IDLE:
            self.image = self.front

        
    


class Enemy(Character):

    '''
    This is the object for enemies. Many of them will be 
    instantiated at once. Version  allows the
    constructor to choose one of several attribute values
    '''

    def __init__(self, level, x, y):#version):
        '''Constructor'''
        facing = const.DOWN
        version = const.BASIC       #placeholder, maybe load enemy types from a list based on level #
        super().__init__(x, y, facing, 0, const.ENEMY)
        self.direction = random.choice([const.UP, const.DOWN, const.LEFT, const.RIGHT])
        version = random.choice([const.BASIC, const.RANDOM, const.ADVANCED]) 
        self.pursuePlayer = False

        self.image = level.enemyImage
        self.rect = self.image.get_rect()
        self.hitbox = self.rect.inflate(-const.HIT_BOX_OFFSET_X, -const.HIT_BOX_OFFSET_Y)
        
        if version == const.RANDOM: #BASIC is some value that we have not mapped yet
            self.speed = const.SPEED_LOW
            self.logic = const.RANDOM
        elif version == const.BASIC: 
            self.speed = const.SPEED_MED
            self.logic = const.BASIC
        elif version == const.ADVANCED:
            self.speed = const.SPEED_LOW    #advanced enemies start slow but speed up when in pursuit
            self.logic = const.ADVANCED
        

    def destroy(self):
        #gets called if something destroys an enemy
        pass