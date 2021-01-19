'''Author: Jennifer Zhu
   Date: May 28, 2019
   Desc: Sprites used in a remake of Atari Centipede.
'''
import pygame, random

class Counter(pygame.sprite.Sprite):
    '''This class defines a label sprite to display a count, i.e. the player's
    current score or number of lives left.'''
    def __init__(self, label, initialCount, xPos):
        '''This initializer takes a label (string), initial count (int) and
        x-coordinate (int) as parameters.  It loads the custom font "Eater" and
        defines the object's instance variables.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Font and instance variables
        self.font = pygame.font.Font("Eater.ttf", 25)
        self.label = label
        self.count = initialCount
        self.xPos = xPos
         
    def setCount(self, points):
        '''This mutator method takes an integer and adds it to the count.'''
        self.count += points
    
    def getCount(self):
        '''This accessor method returns the current count.'''
        return self.count
    
    def update(self):
        '''This method will be called automatically to display the current
        count at the specified position on the game window.'''
        message = self.label+": "+str(self.count)
        self.image = self.font.render(message, True, (255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.centery = self.xPos, 20

class Text(pygame.sprite.Sprite):
    '''This class defines a label sprite to display a static message, e.g. on
    the menu screen. It enables text to be shown on top of other sprites.'''
    def __init__(self, msg, position, size, colour=(255,255,255)):
        '''This initializer takes a message (string), position (tuple), size
        (int) and colour (tuple) as parameters. If no colour is given, it
        defaults to white. It loads the custom font "Eater" at the given size
        and centers the message at the given position.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
 
        # Font and instance variables
        self.font = pygame.font.Font("Eater.ttf", size)
        
        # Set the image and rect attributes
        self.image = self.font.render(msg, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = position

class Player(pygame.sprite.Sprite):
    '''This class defines the sprite for the player.'''
    def __init__(self):
        '''This initializer has no parameters. It
        initializes the image and rect attributes of the player.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Set the image and rect attributes
        self.image = pygame.image.load("images/head.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        
        self.rect = self.image.get_rect()
        self.rect.center = (240, 625)
        
        # Instance variables
        self.dx, self.dy = 0, 0
    
    def setDirection(self, direction):
        '''This mutator accepts a tuple representing a direction and uses it to
        change the values of dx and dy.'''
        self.dx = direction[0]*4
        self.dy = -direction[1]*4
    
    def getPosition(self):
        '''This accessor returns the center position of the player.'''
        return self.rect.center
    
    def update(self):
        '''This method ensures that the player does not leave the screen.'''
        if not( ((self.rect.centerx < 10) and (self.dx < 0)) or ((self.rect.centerx > 470) and (self.dx > 0)) ):
            self.rect.centerx += self.dx
        if not( ((self.rect.centery < 550) and (self.dy < 0)) or ((self.rect.centery > 630) and (self.dy > 0)) ):
            self.rect.centery += self.dy

class Laser(pygame.sprite.Sprite):
    '''This class represents a laser (similar to a bullet) shot by the player.
    It moves straight up the screen until it either hits something or leaves
    the screen.'''
    def __init__(self, xPos, yPos):
        '''This initalizer takes an x-coordinate (int) and a y-coordinate (int) as parameters. It
        initializes the image and rect attributes of the laser.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Set the image and rect attributes
        self.image = pygame.Surface((2, 15))
        self.image.convert()
        self.image.fill((255, 0, 0))
        
        self.rect = self.image.get_rect()
        self.rect.center = (xPos, yPos)
    
    def update(self):
        '''This method is called automatically to move the laser straight up the screen.'''
        self.rect.centery -= 20
        if self.rect.bottom <= 0:
            self.kill()

class Mushroom(pygame.sprite.Sprite):
    '''This class represents a static mushroom.'''
    def __init__(self, position):
        '''This initializer accepts a tuple representing a position. It
        initializes the image and rect attributes of the mushroom.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Set the image and rect attributes
        self.cremini = pygame.image.load("images/cremini.png")
        self.cremini = pygame.transform.scale(self.cremini, (20, 20))
        self.agaric = pygame.image.load("images/fly-agaric.png")
        self.agaric = pygame.transform.scale(self.agaric, (20, 20))
        
        self.image = self.cremini
        self.rect = self.image.get_rect()
        
        self.rect = self.image.get_rect()
        self.rect.center = position
        
        # Instance variables
        self.health = 4
        self.isPoisonous = False
    
    def setHealth(self, health):
        '''This mutator accepts an int and uses it to change the value of health.'''
        self.health = health
    
    def getHealth(self):
        '''This accessor returns the value of health.'''
        return self.health
    
    def setIsPoisonous(self, poisonous):
        '''This mutator accepts a boolean and changes the value of isPoisonous.
        It also changes the mushroom's image to match the value of isPoisonous.'''
        self.isPoisonous = poisonous
        if poisonous:
            self.image = self.agaric
        else:
            self.image = self.cremini
    
    def getIsPoisonous(self):
        '''This accessor returns the value of isPoisonous.'''
        return self.isPoisonous
    
    def update(self):
        '''This method automatically kills the mushroom if it has run out of health.'''
        # If all health is lost, kill the mushroom
        if self.health <= 0:
            self.kill()

class Centipede(pygame.sprite.Sprite):
    '''This class represents one segment of the centipede, the player's main
    enemy. It starts at the top of the screen and moves down gradually towards
    the player, alternating between turning left and turning right.'''
    def __init__(self, yPos, speed):
        '''This initializer takes a y-coordinate (int) and a speed (int) as
        parameters. It initializes the image and rect attributes of the
        centipede and defines its many instance variables.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        # Set the image and rect attributes
        self.down = pygame.image.load("images/UD-centipede.png")
        self.down = pygame.transform.scale(self.down, (20, 20))        
        self.LR = pygame.image.load("images/LR-centipede.png")
        self.LR = pygame.transform.scale(self.LR, (20, 20))
        
        self.image = self.down     
        self.rect = self.image.get_rect()        
        
        self.rect = self.image.get_rect()
        self.rect.center = (200, yPos)        
        
        # Instance variables
        self.dx = 0
        self.dy = speed
        self.speed = speed
        self.lastDx = speed
        
        self.isPoisoned = False
        self.reachedBottom = False
        self.hitMushroom = False
    
    def goDown(self):
        '''This method sets hitMushroom to True, which tells the update method
        to make the Centipede go downwards (or upwards).'''
        self.hitMushroom = True
    
    def setIsPoisoned(self, poisoned):
        '''This mutator accepts a boolean and changes the value of isPoisoned.'''
        self.isPoisoned = poisoned
    
    def update(self):
        '''This method automatically changes the direction of the centipede
        according to its position and its instance variables. It then moves the
        centipede in that direction.'''
        rows = tuple(range(10, 640, 20))
        
        if self.rect.centery >= 630:
            # If the centipede has reached the bottom of the screen, set reachedBottom to True and turn the speed negative to make it go up.
            # Also remove poisoning if necessary.
            self.reachedBottom = True
            self.isPoisoned = False
            self.speed = -abs(self.speed)
        
        if self.reachedBottom and self.rect.centery <= 550:
            # If the centipede had already reached the bottom and is now about to leave the player area, make it go back down again.
            self.isPoisoned = False
            self.speed = abs(self.speed)

        if (self.rect.centery in rows and self.dy != 0):
            # If the centipede is currently going down/up and has reached the next row, go left/right
            self.dy = 0
            self.dx = -self.lastDx
            self.lastDx = self.dx
            self.image = self.LR
        
        elif (self.rect.centerx <= 10 or self.rect.centerx >= 470) and self.dx != 0:
            # If the centipede is currently going left/right and has hit the edge of the screen, go down/up
            self.dx = 0
            self.dy = self.speed
            self.image = self.down
            
        elif self.hitMushroom:
            # If the centipede has hit a mushroom, go down/up
            self.dx = 0
            self.dy = self.speed
            self.image = self.down            
        
        elif self.isPoisoned:
            # If the centipede is poisoned, go down/up
            # (the poisoned centipede will have a wriggling effect)
            self.dx = 0
            self.dy = self.speed            
            self.image = self.down
            
        self.hitMushroom = False
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        
        # In case the centipede glitches for whatever reason and does leave the screen,
        # kill it so that it will not interfere with the game
        if self.rect.right < 0 or self.rect.left > 480 or self.rect.top > 640:
            self.kill()            

class Spider(pygame.sprite.Sprite):
    '''This class represents a spider, the second enemy the player encounters.
        It zig-zags up and down across the player area.'''
    def __init__(self, screen, speed):
        '''This initializer takes a screen surface and a speed (int) as
        parameters. It chooses a random side of the screen to place the spider.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Set the image attributes
        self.image = pygame.image.load("images/spider.png")
        self.image = pygame.transform.scale(self.image, (20, 20))
        self.rect = self.image.get_rect()
        
        # Set the position and direction
        # Randomly choose either left side or right side of screen
        if random.randrange(2) == 0:
            self.rect.left = 0
            self.dx = 2
        else:
            self.rect.right = screen.get_width()
            self.dx = -2
        self.rect.top = 480
        self.dy = speed
        
        # Instance variable to keep track of the screen
        self.window = screen 
    
    def update(self):
        '''This method is called automatically to move the spider in a zig-zag
        pattern across the player area.'''
        # if it reaches top of last 8 rows or bottom of screen, reverse dy
        if self.rect.top < 480 or self.rect.bottom > self.window.get_height():
            self.dy = -self.dy
        
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

class Flea(pygame.sprite.Sprite):
    '''This class represents a flea, another enemy the player encounters. It
    simply moves vertically down the screen before disappearing.'''
    def __init__(self, speed):
        '''This initializer takes a speed (int) as a parameter. It initializes
        the image and rect attributes of the flea.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
         
        # Set the image attributes
        self.image = pygame.image.load("images/flea.png")
        self.image = pygame.transform.scale(self.image, (20, 20)) 
        self.rect = self.image.get_rect()
        
        # Set the position and direction
        self.rect.centerx = random.randrange(10, 480, 20) # random col
        self.rect.top = 0
        self.dy = speed
    
    def update(self):
        '''This method is called automatically to move the flea straight down
        the screen.'''
        self.rect.centery += self.dy

class Scorpion(pygame.sprite.Sprite):
    '''This class represents a scorpion, the third enemy the player encounters.
    It simply moves horizontally across the screen before disappearing.'''
    def __init__(self, screen):
        '''This initializer takes a screen surface as a parameter. It randomly
        chooses a row and one side of the screen to place the scorpion.'''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)    

        # Set the position and direction, and set the image and rect attributes accordingly
        # Randomly choose either left side or right side of screen
        if random.randrange(2) == 0:
            self.image = pygame.image.load("images/scorpion_right.png")
            self.image = pygame.transform.scale(self.image, (25, 20))  
            self.rect = self.image.get_rect() 
            self.rect.left = 0
            self.dx = 3
        else:
            self.image = pygame.image.load("images/scorpion_left.png")
            self.image = pygame.transform.scale(self.image, (25, 20))  
            self.rect = self.image.get_rect()
            self.rect.right = screen.get_width()
            self.dx = -3
        # Choose a random row excl. player area
        self.rect.centery = random.randrange(10, 540, 20)        
    
    def update(self):
        '''This method is called automatically to move the scorpion horizantally
        across the screen in a straight line.'''      
        self.rect.centerx += self.dx