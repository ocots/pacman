import pygame
import random
import math 
import utils
        
class Ennemy(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction, origin, level):
        
        # 
        self.parameters = level.parameters
        
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la direction du fantome
        if direction == "right":
            self.change_x = self.parameters.ENNEMY_SPEED
            self.change_y = 0
        elif direction == "left":
            self.change_x = -self.parameters.ENNEMY_SPEED
            self.change_y = 0
        elif direction == "up":
            self.change_x = 0
            self.change_y = -self.parameters.ENNEMY_SPEED
        elif direction == "down":
            self.change_x = 0
            self.change_y = self.parameters.ENNEMY_SPEED
        else:
            self.change_x = 0
            self.change_y = 0
        
        # charge l'image du fantome
        self.image = pygame.image.load(self.parameters.ENNEMY_IMAGE).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.parameters.ENNEMY_WIDTH, self.parameters.ENNEMY_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x + origin[0], y + origin[1])
        
        # create a mask from the image for collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # on sauvegarde le niveau
        self.level = level
        
        # compteur depuis le dernier changement de direction
        self.counter_direction_change = 0
    
    def get_direction(self):
        if self.change_x > 0:
            return "right"
        elif self.change_x < 0:
            return "left"
        elif self.change_y > 0:
            return "down"
        elif self.change_y < 0:
            return "up"
        else:
            return ""
    
    def update(self): 
        
        # sorti du terrain de jeu
        utils.update_state_tore(self)
            
        # déplace le fantome
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        #
        self.counter_direction_change += 1
        
        # on vérifie les collisions avec les murs
        e = self.parameters.ENNEMY_EPSILON_WALL
        d = self.parameters.WALL_DISTANCE_TO_CORNER
        authorized_directions = utils.update_state_collision_walls(self, e, d)
        ennemy_direction = self.get_direction()

        if self.counter_direction_change > self.parameters.ENNEMY_DELAY_DIRECTION_CHANGE:
            
            for player in self.level.players: # there is one player for now
                pass
            
            x_player = player.rect.x
            y_player = player.rect.y
            
            direction = None
            
            # le fantome se déplace horizontalement
            # il se trouve au dessus du joueur : self.rect.y < player.rect.y. Il essaie de descendre
            # s'il ne peut pas descendre et s'il ne peut plus continuer dans sa direction alors il monte
            if self.change_x != 0:
                if self.rect.y < y_player: # le joueur est en dessous du fantome
                    if "down" in authorized_directions:
                        direction = "down"
                    elif not ennemy_direction in authorized_directions:
                        direction = "up"
                elif self.rect.y > y_player:
                    if "up" in authorized_directions:
                        direction = "up"
                    elif not ennemy_direction in authorized_directions:
                        direction = "down"
                else:
                    if not ennemy_direction in authorized_directions and "up" in authorized_directions:
                        direction = "up"
                    elif not ennemy_direction in authorized_directions and "down" in authorized_directions:
                        direction = "down"
            else:
                if self.rect.x < x_player:
                    if "right" in authorized_directions:
                        direction = "right"
                    elif not ennemy_direction in authorized_directions:
                        direction = "left"
                elif self.rect.x > x_player:
                    if "left" in authorized_directions:
                        direction = "left"
                    elif not ennemy_direction in authorized_directions:
                        direction = "right"
                else:
                    if not ennemy_direction in authorized_directions and "left" in authorized_directions:
                        direction = "left"
                    elif not ennemy_direction in authorized_directions and "right" in authorized_directions:
                        direction = "right"
            
            # if y_player > self.rect.y:
            #     direction = "down"
            # else:
            #     direction = "up"
            
            # if x_player > self.rect.x:
            #     direction = "right"
            # else:
            #     direction = "left"
                
            #if x_blocked:
                # if self.change_y == 0:
                #     direction = random.choice( ("up", "down") )
                # elif self.change_y < 0:
                #     direction = random.choice( ("down", "up", "up", "up") )
                # else:
                #     direction = random.choice( ("up", "down", "down", "down") )
                    
            #if y_blocked:
                # if self.change_x == 0:
                #     direction = random.choice( ("left", "right") )
                # elif self.change_x < 0:
                #     direction = random.choice( ("right", "left", "left", "left") )
                # else:
                #     direction = random.choice( ("left", "right", "right", "right") )
                    
            if self.change_x == 0 and self.change_y == 0:
                direction = random.choice( ("left", "right", "up", "down") )
            
            if not direction is None:
                if direction == "left":
                    self.change_x = -self.parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0
                elif direction == "right":
                    self.change_x = self.parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0
                elif direction == "up":
                    self.change_y = -self.parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0
                elif direction == "down":
                    self.change_y = self.parameters.ENNEMY_SPEED
                    self.counter_direction_change = 0