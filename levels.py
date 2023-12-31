import pygame
from player import Player
from ennemies import Ennemy
from assets import Ellipse, Block, Wall, ShadowWall
from errors import InternalException

# Les positions sont relatives au terrain de jeu
class Levels():
    
    def __init__(self, level_number, parameters):
        
        # paramètres du jeu
        self.parameters = parameters
        
        # niveau du jeu
        # self.level = level
        if level_number > 2:
            raise(InternalException("Level not found"))
        
        # environnement
        self.environment = self.environment(level_number)
        
        # on calcule les dimensions du terrain de jeu
        self.field_width, self.field_height = self.dimensions(self.environment)
        print("field_width: ", self.field_width)
        print("field_height: ", self.field_height)
        self.field_x = (self.parameters.SCREEN_WIDTH  - self.field_width ) / 2
        self.field_y = (self.parameters.SCREEN_HEIGHT - self.field_height) / 2
        
        # 
        paths, walls, dots, ennemies, players, empty_blocks, shadow_walls = self.intialize(self.environment, level_number)
        self.paths        = paths
        self.walls        = walls
        self.dots         = dots
        self.ennemies     = ennemies
        self.players      = players
        self.empty_blocks = empty_blocks
        self.shadow_walls  = shadow_walls
    
    def environment(self, level_number):
        if level_number == 2:
            grid = (('▪-▪-▪-▪-▪-▪-▪-▪ ▪-▪-▪-▪-▪-▪-▪-▪'),
                    ('                               '),
                    ('    ▪-▪-▪-▪       ▪            '),
                    ('          |                    '),
                    ('▪-▪-▪-▪-▪ ▪        -           '),
                    ('        | |                    '),
                    ('        ▪ ▪                    '),
                    ('        | |                    '),
                    ('        ▪ ▪-▪-▪                '),
                    ('        |               |      '),
                    ('        ▪-▪-▪-▪                '),
                    ('                               '),
                    ('                               '),
                    ('                               '))
        elif level_number == 1:
            # legend: 
            # vertical wall: '|'
            # horizontal wall: '-'
            # square wall: '▪'
            # path: 'o'
            grid = (('▪-▪-▪-▪-▪-▪-▪-▪ ▪-▪-▪-▪-▪-▪-▪-▪'),
                    ('|•|• • • • • •|• • •|• •|• • •|'),
                    ('▪ ▪ ▪ ▪-▪-▪ ▪ ▪-▪-▪ ▪ ▪ ▪ ▪-▪ ▪'),
                    ('|• •|• • • •|• • • •|•|•|•|• •|'),
                    ('▪ ▪-▪-▪-▪-▪ ▪-▪-▪ ▪ ▪ ▪ ▪ ▪ ▪-▪'),
                    ('|•|• •|• • •|• • •|• •|• •|• •|'),
                    ('▪ ▪ ▪ ▪ ▪-▪-▪ ▪ ▪-▪-▪ ▪ ▪-▪-▪ ▪'),
                    ('|•|•|• • •|• •|•|• • •|•|• • •|'),
                    ('▪ ▪ ▪-▪-▪ ▪ ▪-▪ ▪ ▪ ▪-▪ ▪ ▪ ▪-▪'),
                    ('|• • •|• •|• •|• •|•|• •|•|• •|'),
                    ('▪ ▪-▪ ▪ ▪ ▪ ▪ ▪-▪ ▪ ▪ ▪-▪ ▪-▪ ▪'),
                    ('|• • •|•|• •|• •|•|• • • • •|•|'),
                    ('▪-▪ ▪-▪ ▪-▪ ▪-▪ ▪ ▪-▪-▪-▪-▪ ▪ ▪'),
                    ('|• • •|• •|• •|• • • • •|• •|•|'),
                    ('▪ ▪-▪ ▪ ▪ ▪-▪ ▪ ▪-▪-▪ ▪ ▪ ▪ ▪ ▪'),
                    ('|• •|•|•|• •|• •|• • •|• •|•|•|'),
                    ('▪-▪ ▪ ▪ ▪-▪ ▪-▪-▪ ▪ ▪-▪ ▪-▪ ▪ ▪'),
                    (' •|•|• • • •|x|• •|• • • • • • '),
                    ('▪ ▪ ▪-▪-▪ ▪-▪-▪ ▪-▪-▪ ▪-▪ ▪-▪ ▪'),
                    ('|•|• •|• •|• • •|• •|•|x|• • •|'),
                    ('▪ ▪ ▪ ▪ ▪ ▪ ▪-▪-▪ ▪ ▪ ▪-▪-▪-▪-▪'),
                    ('|• •|• •|• • • • •|• • • • • •|'),
                    ('▪-▪-▪-▪-▪-▪-▪-▪ ▪-▪-▪-▪-▪-▪-▪-▪'))
        return grid
    
    def split_row_env(self, row):
        return row
    
    def dimensions(self, environment):
        # on parcours l'environnement et crée les structures au fur et à mesure
        # pour cela, nous allons avoir besoin des différentes tailles
        horizontal_wall_width, horizontal_wall_height = self.get_size_horizontal_wall()
        vertical_wall_width, vertical_wall_height = self.get_size_vertical_wall()
        square_wall_width, square_wall_height = self.get_size_square_wall()
        path_width, path_height = self.get_size_path()
        empty_block_width, empty_block_height = self.get_size_empty_block()
        # on parcours l'environnement, pour connaitre la position courante, on utilise deux variables que l'on incrémente
        x = 0
        y = 0
        dy = 0
        for i, row in enumerate(environment):
            x = 0
            dy = 0
            for j, item in enumerate(self.split_row_env(row)):
                if self.isverticalwall(item):
                    dx = vertical_wall_width
                    dy = max(dy, vertical_wall_height)
                elif self.ishorizontalwall(item):
                    dx = horizontal_wall_width
                    dy = max(dy, horizontal_wall_height)
                elif self.issquarewall(item):
                    dx = square_wall_width
                    dy = max(dy, square_wall_height)
                elif self.ispath(item):
                    # si j est pair, on a un chemin de largeur square_wall_width, sinon on a un chemin de largeur path_width
                    # si i est pair, on a un chemin de hauteur square_wall_height, sinon on a un chemin de hauteur path_height
                    if j % 2 == 0:
                        w = square_wall_width
                    else:
                        w = path_width
                    if i % 2 == 0:
                        h = square_wall_height
                    else:
                        h = path_height
                    dx = w
                    dy = max(dy, h)
                elif self.isemptyblock(item):
                    dx = empty_block_width
                    dy = max(dy, empty_block_height)
                x += dx
            y += dy
        return x, y
    
    def intialize(self, environment, level_number):
        # on parcours l'environnement et crée les structures au fur et à mesure
        # pour cela, nous allons avoir besoin des différentes tailles
        horizontal_wall_width, horizontal_wall_height = self.get_size_horizontal_wall()
        vertical_wall_width, vertical_wall_height     = self.get_size_vertical_wall()
        square_wall_width, square_wall_height         = self.get_size_square_wall()
        path_width, path_height                       = self.get_size_path()
        empty_block_width, empty_block_height         = self.get_size_empty_block()
        # on crée les groupes de sprites
        paths        = pygame.sprite.Group()
        walls        = pygame.sprite.Group()
        shadow_walls = pygame.sprite.Group()
        dots         = pygame.sprite.Group()
        ennemies     = pygame.sprite.Group()
        players      = pygame.sprite.Group()
        empty_blocks = pygame.sprite.Group()
        # on parcours l'environnement, pour connaitre la position courante, on utilise deux variables que l'on incrémente
        x = 0
        y = 0
        dy = 0
        for i, row in enumerate(environment):
            x = 0
            dy = 0
            for j, item in enumerate(self.split_row_env(row)):
                if self.isverticalwall(item):
                    dx = vertical_wall_width
                    walls.add(Wall( x, y, self.parameters.FIELD_WALL_COLOR, dx, vertical_wall_height, self))
                    shadow_walls.add(ShadowWall( x, y, self.parameters.WHITE, dx, vertical_wall_height, self))
                    # for dy we take the max between dy and vertical_wall_height
                    # indeed, if we have a vertical wall followed by a horizontal wall, we want to take the max
                    # otherwise, we would have a gap between the two walls
                    dy = max(dy, vertical_wall_height)
                elif self.ishorizontalwall(item):
                    dx = horizontal_wall_width
                    walls.add(Wall( x, y, self.parameters.FIELD_WALL_COLOR, dx, horizontal_wall_height, self))
                    shadow_walls.add(ShadowWall( x, y, self.parameters.WHITE, dx, horizontal_wall_height, self))
                    dy = max(dy, horizontal_wall_height)
                elif self.issquarewall(item):
                    dx = square_wall_width
                    walls.add(Wall( x, y, self.parameters.FIELD_WALL_COLOR, dx, square_wall_height, self))
                    shadow_walls.add(ShadowWall( x, y, self.parameters.WHITE, dx, square_wall_height, self))
                    dy = max(dy, square_wall_height)
                elif self.ispath(item):
                    # si j est pair, on a un chemin de largeur square_wall_width, sinon on a un chemin de largeur path_width
                    # si i est pair, on a un chemin de hauteur square_wall_height, sinon on a un chemin de hauteur path_height
                    if j % 2 == 0:
                        w = square_wall_width
                    else:
                        w = path_width
                    if i % 2 == 0:
                        h = square_wall_height
                    else:
                        h = path_height
                    paths.add(Block(x, y, self.parameters.FIELD_PATH_COLOR, w, h, self))
                    dx = w
                    dy = max(dy, h)
                elif self.isemptyblock(item):
                    dx = empty_block_width
                    empty_blocks.add(Block(x, y, self.parameters.FIELD_EMPTY_BLOCK_COLOR, dx, empty_block_height, self, alpha=55))
                    dy = max(dy, empty_block_height)
                if self.isdot(item):
                    dots.add(Ellipse(x+path_width/2-self.parameters.ELLIPSE_WIDTH/2, # on positionne le coin supérieur gauche de l'ellipse vu comme un rectangle 
                                          y+path_height/2-self.parameters.ELLIPSE_HEIGHT/2, # en son centre
                                          self.parameters.WHITE, 
                                          self.parameters.ELLIPSE_WIDTH, 
                                          self.parameters.ELLIPSE_HEIGHT, 
                                          self))
                    #dx = 0
                # if self.isplayer(item):
                #     direction = self.direction(item)
                #     players.add(Player(x, y, direction, self.parameters.PLAYER_IMAGE, self))
                #     dx = 0
                # if self.isennemy(item):
                #     direction = self.direction(item)
                #     ennemies.add(Ennemy(x, y, direction, self))
                #     dx = 0
                x += dx
            y += dy
        players.add(Player(100*self.parameters.UNIT_LENGTH/80, 104*self.parameters.UNIT_LENGTH/80, \
            'right', self.parameters.PLAYER_IMAGE, self)) # à supprimer plus tard
        if level_number == 1:
            ennemies.add(Ennemy(1000*self.parameters.UNIT_LENGTH/80, 104*self.parameters.UNIT_LENGTH/80, 'up', self))
            ennemies.add(Ennemy(300*self.parameters.UNIT_LENGTH/80, 500*self.parameters.UNIT_LENGTH/80, 'up', self))
            ennemies.add(Ennemy(600*self.parameters.UNIT_LENGTH/80, 800*self.parameters.UNIT_LENGTH/80, 'up', self))
        return paths, walls, dots, ennemies, players, empty_blocks, shadow_walls
    
    def get_size_horizontal_wall(self):
        return self.parameters.WALL_BIG_LENGTH, self.parameters.WALL_SMALL_LENGTH
    
    def get_size_vertical_wall(self):
        return self.parameters.WALL_SMALL_LENGTH, self.parameters.WALL_BIG_LENGTH
    
    def get_size_square_wall(self):
        return self.parameters.WALL_SMALL_LENGTH, self.parameters.WALL_SMALL_LENGTH
    
    def get_size_path(self):
        return self.parameters.BLOCK_WIDTH, self.parameters.BLOCK_HEIGHT
    
    def get_size_empty_block(self):
        return self.parameters.BLOCK_WIDTH, self.parameters.BLOCK_HEIGHT
    
    def isemptyblock(self, item):
        return 'x' in item
    
    def isverticalwall(self, item):
        # it is a vertical wall if it contains `|` but can contain other characters
        return '|' in item
    
    def ishorizontalwall(self, item):
        # it is a horizontal wall if it contains `-` but can contain other characters
        return '-' in item
    
    def issquarewall(self, item):
        # it is a square wall if it contains `▪` but can contain other characters
        return '▪' in item
    
    def isdot(self, item):
        # it is a dot if it contains `•` but can contain other characters
        return '•' in item
    
    def ispath(self, item):
        return 'o' in item or ' ' in item or '•' in item
    
    def isplayer(self, item):
        # it is a player if it contains `p` but can contain other characters
        return 'p' in item
    
    def isennemy(self, item):
        # it is an ennemy if it contains `e` but can contain other characters
        return 'e' in item
    
    def direction(self, item):
        if '<' in item:
            return 'left'
        elif '>' in item:
            return 'right'
        elif '^' in item:
            return 'up'
        elif 'v' in item:
            return 'down'
        else: # no moving
            return 'static'
    