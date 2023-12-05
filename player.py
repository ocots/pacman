import pygame
from animation import Animation
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

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction, filename, level):
            
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # score
        self.score = 0
        
        # définit vitesse de déplacement du joueur
        self.change_x = 0
        self.change_y = 0
        
        # charge l'image du joueur
        self.image_save = pygame.image.load(filename).convert_alpha()
        self.image_save = pygame.transform.scale(self.image_save, (parameters.PLAYER_WIDTH, parameters.PLAYER_HEIGHT))
        self.image = self.image_save
        
        # définit une couleur comme transparente
        #self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x + level.field_x, y + level.field_y)
        
        # create a mask from the image for collision detection
        self.mask = pygame.mask.from_surface(self.image)
        
        # on oriente l'image du joueur en fonction de la direction
        if direction == "right":
            self.image = self.image_save
        elif direction == "left":
            self.image = pygame.transform.flip(self.image_save, True, False)
        elif direction == "up":
            self.image = pygame.transform.rotate(self.image_save, 90)
        elif direction == "down":
            self.image = pygame.transform.rotate(self.image_save, 270)
        
        # charge l'image de l'animation
        #img = pygame.image.load(filename).convert()
        
        # crée les objets pour les animations
        # self.move_right_animation   = Animation(img, 32, 32)
        # self.move_left_animation    = Animation(pygame.transform.flip(img, True, False), 32, 32)
        # self.move_up_animation      = Animation(pygame.transform.rotate(img, 90), 32, 32)
        # self.move_down_animation    = Animation(pygame.transform.rotate(img, 270), 32, 32)
        
        # charge l'image de l'explosion
        #img = pygame.image.load("resources/explosion.png").convert()
        #self.explosion_animation    = Animation(img, 30, 30)
        
        # Save the player image: useful when the player stops moving
        #self.player_image = pygame.image.load(filename).convert()
        #self.player_image.set_colorkey(BLACK)
        
        # nombre de vies du joueur
        self.lives = parameters.PLAYER_LIVES
        
        # indicateur a été touché par un ennemi
        self.touched = False
        
        # compteur pour le délai entre la perte d'une vie et la reprise du jeu
        self.counter_touched = 0
        
        # on stocke les touches appuyées par le joueur dans une liste ordonnées
        self.keys = list()
        
        #
        self.level = level
    
    def update_image_from_direction(self):
        if self.change_x > 0:
            self.image = self.image_save
        elif self.change_x < 0:
            self.image = pygame.transform.flip(self.image_save, True, False)
        elif self.change_y > 0:
            self.image = pygame.transform.rotate(self.image_save, 270)
        elif self.change_y < 0:
            self.image = pygame.transform.rotate(self.image_save, 90)        
    
    def update(self): #, horizontal_blocks, vertical_blocks):
        
        # on vérifie si le joueur est sorti du terrain de jeu
        # sachant que le terrain de jeu est centré à l'écran
        # et qu'il se déplace sur un tore
        FX = self.level.field_x
        FY = self.level.field_y
        FW = self.level.field_width
        FH = self.level.field_height
        dx = parameters.PLAYER_WIDTH / 2
        dy = parameters.PLAYER_HEIGHT / 2
        if self.rect.right < (FX + dx) :
            self.rect.left = FX + FW - dx
        elif self.rect.left > (FX + FW - dx):
            self.rect.right = FX + dx
        if self.rect.bottom < (FY + dy):
            self.rect.top = FY + FH - dy
        elif self.rect.top > (FY + FH - dy):
            self.rect.bottom = FY + dy
            
        # déplace le joueur
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        # on évite les collisions avec les murs en utilisant les ShadowWall
        for block in pygame.sprite.spritecollide(self, self.level.shadow_walls, False):
            # coordinates of the center of the player in the (x,y) plane centered in the block
            x = self.rect.centerx - block.rect.centerx
            y = block.rect.centery - self.rect.centery
            # 
            # get the angle of the vector (x,y) in the (x,y) plane
            angle = math.atan2(y, x) # between -pi and pi
            angle = angle % (2*math.pi) # between 0 and 2*pi
            # get the angle of reference for the block: 
            # that is tha angle of the vector joining the center and the top right corner of the block
            a = math.atan2(block.rect.height/2, block.rect.width/2)
            a = a % (2*math.pi) # between 0 and 2*pi
            e = parameters.PLAYER_EPSILON_WALL
            d = parameters.WALL_DISTANCE_TO_CORNER
            # 
            if not (a >= 0 and a < math.pi/2):
                raise ValueError("a = %f" % a)
            # [2pi-a+e, a-e]: right
            if angle > (2.0*math.pi-a+e) or angle < (a-e):
                self.change_x = 0
                self.rect.left = block.rect.right
            # [a+e, pi-a-e]: top
            elif angle > (a+e) and angle < (math.pi-a-e):
                self.change_y = 0
                self.rect.bottom = block.rect.top
            # [pi-a+e, pi+a-e]: left
            elif angle > (math.pi-a+e) and angle < (math.pi+a-e):
                self.change_x = 0
                self.rect.right = block.rect.left
            # [pi+a+e, 2pi-a-e]: bottom
            elif angle > (math.pi+a+e) and angle < (2*math.pi-a-e):
                self.change_y = 0
                self.rect.top = block.rect.bottom
            # in the last 4 following cases, we have to check the distance to the block
            # top-right: [a-e, a+e]
            elif angle >= (a-e) and angle < (a+e):
                # get the vector joining the top right corner of the block and the center of the player
                dx = self.rect.centerx - block.rect.right
                dy = block.rect.top - self.rect.centery
                # move the player at the distance d from the corner of the block in the direction (dx, dy)
                self.rect.centerx = block.rect.right + d * dx / math.sqrt(dx*dx + dy*dy)
                self.rect.centery = block.rect.top - d * dy / math.sqrt(dx*dx + dy*dy)
            # top-left: [pi-a-e, pi-a+e]
            elif angle >= (math.pi-a-e) and angle < (math.pi-a+e):
                # get the vector joining the top left corner of the block and the center of the player
                dx = self.rect.centerx - block.rect.left
                dy = block.rect.top - self.rect.centery
                # move the player at the distance d from the corner of the block in the direction (dx, dy)
                self.rect.centerx = block.rect.left + d * dx / math.sqrt(dx*dx + dy*dy)
                self.rect.centery = block.rect.top - d * dy / math.sqrt(dx*dx + dy*dy)
            # bottom-left: [pi+a-e, pi+a+e]
            elif angle >= (math.pi+a-e) and angle < (math.pi+a+e):
                # get the vector joining the bottom left corner of the block and the center of the player
                dx = self.rect.centerx - block.rect.left
                dy = block.rect.bottom - self.rect.centery
                # move the player at the distance d from the corner of the block in the direction (dx, dy)
                self.rect.centerx = block.rect.left + d * dx / math.sqrt(dx*dx + dy*dy)
                self.rect.centery = block.rect.bottom - d * dy / math.sqrt(dx*dx + dy*dy)
            # bottom-right: [2pi-a-e, 2pi-a+e]
            elif angle >= (2*math.pi-a-e) and angle < (2*math.pi-a+e):
                # get the vector joining the bottom right corner of the block and the center of the player
                dx = self.rect.centerx - block.rect.right
                dy = block.rect.bottom - self.rect.centery
                # move the player at the distance d from the corner of the block in the direction (dx, dy)
                self.rect.centerx = block.rect.right + d * dx / math.sqrt(dx*dx + dy*dy)
                self.rect.centery = block.rect.bottom - d * dy / math.sqrt(dx*dx + dy*dy)
        
        # on change l'orientation de l'image en fonction de l'orientation du joueur
        self.update_image_from_direction()
            
        # ceci entrainera le démarrage de l'animation
        # if self.change_x > 0:
        #     self.move_right_animation.update(10)
        #     self.image = self.move_right_animation.get_current_image()
        # elif self.change_x < 0:
        #     self.move_left_animation.update(10)
        #     self.image = self.move_left_animation.get_current_image()
        # if self.change_y > 0:
        #     self.move_down_animation.update(10)
        #     self.image = self.move_down_animation.get_current_image()
        # elif self.change_y < 0:
        #     self.move_up_animation.update(10)
        #     self.image = self.move_up_animation.get_current_image()
                
    def move_right(self):
        self.change_x = parameters.PLAYER_SPEED
        
    def move_left(self):
        self.change_x = -parameters.PLAYER_SPEED
        
    def move_up(self):
        self.change_y = -parameters.PLAYER_SPEED
        
    def move_down(self):
        self.change_y = parameters.PLAYER_SPEED
        
    def stop_move_x(self):
        self.change_x = 0
        
    def stop_move_y(self):
        self.change_y = 0
        
    def event_handler(self, event):
        
        # si l'utilisateur appuie sur une touche du clavier
        # on stocke la touche dans la liste keys
        # seulement si cette touche correspond à une action du joueur
        # et si elle n'est pas déjà dans la liste
        if event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN]:
                if not event.key in self.keys:
                    self.keys.append(event.key)
        
        # si l'utilisateur relâche une touche du clavier
        # on supprime la touche de la liste keys
        elif event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.keys.remove(event.key)
        
        # on met à jour le déplacement du joueur en fonction des touches appuyées
        # on ne considère que la dernière touche appuyée
        if len(self.keys) > 0:
            if self.keys[-1] == pygame.K_RIGHT:
                self.move_right()
            elif self.keys[-1] == pygame.K_LEFT:
                self.move_left()
            elif self.keys[-1] == pygame.K_UP:
                self.move_up()
            elif self.keys[-1] == pygame.K_DOWN:
                self.move_down()
        
        # si pas de touches gauche ou droite appuyées
        # on arrête le déplacement horizontal du joueur
        if not pygame.K_RIGHT in self.keys and not pygame.K_LEFT in self.keys:
            self.stop_move_x()
        # si pas de touches haut ou bas appuyées
        # on arrête le déplacement vertical du joueur
        if not pygame.K_UP in self.keys and not pygame.K_DOWN in self.keys:
            self.stop_move_y()
