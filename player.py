import pygame
#from animation import Animation
import utils

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y, direction, filename, level):
        
        #
        self.parameters = level.parameters
            
        # appelle le constructeur de la classe parent (Sprite)
        pygame.sprite.Sprite.__init__(self)
        
        # score
        self.score = 0
        
        # définit vitesse de déplacement du joueur
        self.change_x = 0
        self.change_y = 0
        
        # charge l'image du joueur
        self.image_save = pygame.image.load(filename).convert_alpha()
        self.image_save = pygame.transform.scale(self.image_save, (self.parameters.PLAYER_WIDTH, self.parameters.PLAYER_HEIGHT))
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
        self.lives = self.parameters.PLAYER_LIVES
        
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
    
    def update(self):
        
        # sorti du terrain de jeu
        utils.update_state_tore(self)
            
        # déplace le joueur
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        
        # on vérifie les collisions avec les murs
        e = self.parameters.PLAYER_EPSILON_WALL
        d = self.parameters.WALL_DISTANCE_TO_CORNER
        authorized_directions = utils.update_state_collision_walls(self, e, d)
        
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
        self.change_x = self.parameters.PLAYER_SPEED
        
    def move_left(self):
        self.change_x = -self.parameters.PLAYER_SPEED
        
    def move_up(self):
        self.change_y = -self.parameters.PLAYER_SPEED
        
    def move_down(self):
        self.change_y = self.parameters.PLAYER_SPEED
        
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
