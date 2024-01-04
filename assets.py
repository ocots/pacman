import pygame

class Ellipse(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, origin):
        
        #
        BLACK = (0, 0, 0)
        
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
        self.rect.center = (x + origin[0] + width/2.0, y + origin[1] + height/2.0)

class Block(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, origin, alpha=255):
        
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la couleur de l'arrère-plan comme transparente
        self.image = pygame.Surface([width, height])
        self.image.set_alpha(alpha)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # on positionne le bloc à l'écran en fonction de sa position dans le terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        self.rect.center = (x + origin[0] + width/2.0, y + origin[1] + height/2.0)

class Wall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, origin):
        
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # définit la couleur de l'arrère-plan comme transparente
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # on positionne le bloc à l'écran en fonction de sa position dans le terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        self.rect.center = (x + origin[0] + width/2.0, y + origin[1] + height/2.0)

class ShadowWall(pygame.sprite.Sprite):
    
    def __init__(self, x, y, color, width, height, origin):
        
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
        self.rect.center = (x + origin[0] + width/2.0, y + origin[1] + height/2.0)
    