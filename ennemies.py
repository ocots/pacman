import pygame
import random
from parameters import Parameters
import math 

# les paramètres du jeu
parameters = Parameters()

# définit les couleurs du jeu
BLACK = parameters.BLACK
WHITE = parameters.WHITE
BLUE  = parameters.BLUE
GREEN = parameters.GREEN
RED   = parameters.RED
        
class Ennemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction, level):
        
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la direction du fantome
        if direction == "right":
            self.change_x = parameters.ENNEMY_SPEED
            self.change_y = 0
        elif direction == "left":
            self.change_x = -parameters.ENNEMY_SPEED
            self.change_y = 0
        elif direction == "up":
            self.change_x = 0
            self.change_y = -parameters.ENNEMY_SPEED
        elif direction == "down":
            self.change_x = 0
            self.change_y = parameters.ENNEMY_SPEED
        else:
            self.change_x = 0
            self.change_y = 0
        
        # charge l'image du fantome
        self.image = pygame.image.load(parameters.ENNEMY_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (parameters.ENNEMY_WIDTH, parameters.ENNEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x + level.field_x, y + level.field_y)
        
        # create a mask from the image for collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # on sauvegarde l'environnement du niveau courant
        self.level = level
        
        # compteur depuis le dernier changement de direction
        self.counter_direction_change = 0
        
    def update(self): #, horizontal_blocks, vertical_blocks):
        
        # on vérifie si le joueur est sorti du terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        # et qu'il se déplace sur un tore
        FX = self.level.field_x
        FY = self.level.field_y
        FW = self.level.field_width
        FH = self.level.field_height
        dx = parameters.ENNEMY_WIDTH / 2
        dy = parameters.ENNEMY_HEIGHT / 2
        if self.rect.right < (FX + dx) :
            self.rect.left = FX + FW - dx
        elif self.rect.left > (FX + FW - dx):
            self.rect.right = FX + dx
        if self.rect.bottom < (FY + dy):
            self.rect.top = FY + FH - dy
        elif self.rect.top > (FY + FH - dy):
            self.rect.bottom = FY + dy
            
        # déplace le fantome
        self.rect.x += self.change_x
        self.rect.y += self.change_y
                        
        # # on change la direction du fantome s'il se trouve à une intersection
        # self.counter_direction_change += 1
        # d = self.level.distance_to_crossroad(x, y)
        # if d <= parameters.ENNEMY_DISTANCE_TO_CROSSROAD:
        #     direction = random.choice( ("left", "right", "up", "down") )
        #     if self.counter_direction_change > parameters.ENNEMY_DELAY_DIRECTION_CHANGE:
        #         if direction == "left" and self.change_x == 0:
        #             self.change_x = -parameters.ENNEMY_SPEED
        #             self.change_y = 0
        #             self.counter_direction_change = 0
        #         elif direction == "right" and self.change_x == 0:
        #             self.change_x = parameters.ENNEMY_SPEED
        #             self.change_y = 0
        #             self.counter_direction_change = 0
        #         elif direction == "up" and self.change_y == 0:
        #             self.change_x = 0
        #             self.change_y = -parameters.ENNEMY_SPEED
        #             self.counter_direction_change = 0
        #         elif direction == "down" and self.change_y == 0:
        #             self.change_x = 0
        #             self.change_y = parameters.ENNEMY_SPEED
        #             self.counter_direction_change = 0
        
        #
        self.counter_direction_change += 1
        
        # on évite les collisions avec les murs en utilisant les ShadowWall
        x_blocked = False
        y_blocked = False
        for block in pygame.sprite.spritecollide(self, self.level.shadow_walls, False):
            #
            x = self.rect.centerx - block.rect.centerx
            y = block.rect.centery - self.rect.centery
            # 
            angle = math.atan2(y, x)    # between -pi and pi
            angle = angle % (2*math.pi) # between 0 and 2*pi
            angle_ref = math.atan2(block.rect.height/2, block.rect.width/2)
            angle_ref = angle_ref % (2*math.pi) # between 0 and 2*pi
            if not (angle_ref >= 0 and angle_ref < math.pi/2):
                raise ValueError("angle_ref = %f" % angle_ref)
            epsilon =  parameters.ENNEMY_EPSILON_WALL
            if angle > (2.0*math.pi-angle_ref+epsilon) or angle < (angle_ref-epsilon):
                self.change_x = 0
                self.rect.left = block.rect.right
                x_blocked = True
            if angle > (angle_ref+epsilon) and angle < (math.pi-angle_ref-epsilon):
                self.change_y = 0
                self.rect.bottom = block.rect.top
                y_blocked = True
            if angle > (math.pi-angle_ref+epsilon) and angle < (math.pi+angle_ref-epsilon):
                self.change_x = 0
                self.rect.right = block.rect.left
                x_blocked = True
            if angle > (math.pi+angle_ref+epsilon) and angle < (2*math.pi-angle_ref-epsilon):
                self.change_y = 0
                self.rect.top = block.rect.bottom
                y_blocked = True

        if self.counter_direction_change > parameters.ENNEMY_DELAY_DIRECTION_CHANGE:
            
            direction = None
            
            if x_blocked:
                if self.change_y == 0:
                    direction = random.choice( ("up", "down") )
                elif self.change_y < 0:
                    direction = random.choice( ("down", "up", "up", "up") )
                else:
                    direction = random.choice( ("up", "down", "down", "down") )
                    
            if y_blocked:
                if self.change_x == 0:
                    direction = random.choice( ("left", "right") )
                elif self.change_x < 0:
                    direction = random.choice( ("right", "left", "left", "left") )
                else:
                    direction = random.choice( ("left", "right", "right", "right") )
                    
            if self.change_x == 0 and self.change_y == 0:
                direction = random.choice( ("left", "right", "up", "down") )
            
            if not direction is None:
                if direction == "left":
                    self.change_x = -parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0
                elif direction == "right":
                    self.change_x = parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0
                elif direction == "up":
                    self.change_y = -parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0
                elif direction == "down":
                    self.change_y = parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0