import pygame
from parameters import Parameters
parameters = Parameters()

# définit les couleurs du jeu
BLACK = parameters.BLACK

class Ellipse(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, level):
        
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la couleur de l'arrère-plan comme transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        # on positionne le point à l'écran en fonction de sa position dans le terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        self.rect.center = (x + level.field_x + width/2.0, y + level.field_y + height/2.0)

class Block(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, level):
        
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la couleur de l'arrère-plan comme transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # on positionne le bloc à l'écran en fonction de sa position dans le terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        self.rect.center = (x + level.field_x + width/2.0, y + level.field_y + height/2.0)

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, level):
        
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la couleur de l'arrère-plan comme transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # on positionne le bloc à l'écran en fonction de sa position dans le terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        self.rect.center = (x + level.field_x + width/2.0, y + level.field_y + height/2.0)

class ShadowWall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, level):
        
        ratio = 4.0
        if width < height:
            width__  = ratio * width
            height__ = height
        elif width > height:
            width__  = width
            height__ = ratio * height
        else:
            width__  = ratio * width
            height__ = ratio * height
            
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la couleur de l'arrère-plan comme transparente
        self.image = pygame.Surface([width__, height__])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # on positionne le bloc à l'écran en fonction de sa position dans le terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        self.rect.center = (x + level.field_x + width/2.0, y + level.field_y + height/2.0)
    