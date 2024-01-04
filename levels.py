import pygame
from player import Player
from ennemies import Ennemy
from assets import Ellipse, Block, Wall, ShadowWall

def environment(level_number):
    if level_number == 0:
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

def split_row_env(row):
    return row

def get_size_horizontal_wall(parameters):
    return parameters.WALL_BIG_LENGTH, parameters.WALL_SMALL_LENGTH

def get_size_vertical_wall(parameters):
    return parameters.WALL_SMALL_LENGTH, parameters.WALL_BIG_LENGTH

def get_size_square_wall(parameters):
    return parameters.WALL_SMALL_LENGTH, parameters.WALL_SMALL_LENGTH

def get_size_path(parameters):
    return parameters.BLOCK_WIDTH, parameters.BLOCK_HEIGHT

def get_size_empty_block(parameters):
    return parameters.BLOCK_WIDTH, parameters.BLOCK_HEIGHT

def isemptyblock(item):
    return 'x' in item

def isverticalwall(item):
    # it is a vertical wall if it contains `|` but can contain other characters
    return '|' in item

def ishorizontalwall(item):
    # it is a horizontal wall if it contains `-` but can contain other characters
    return '-' in item

def issquarewall(item):
    # it is a square wall if it contains `▪` but can contain other characters
    return '▪' in item

def isdot(item):
    # it is a dot if it contains `•` but can contain other characters
    return '•' in item

def ispath(item):
    return 'o' in item or ' ' in item or '•' in item

def isplayer(item):
    # it is a player if it contains `p` but can contain other characters
    return 'p' in item

def isennemy(item):
    # it is an ennemy if it contains `e` but can contain other characters
    return 'e' in item

def direction(item):
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

def dimensions(environment, parameters):
    # on parcours l'environnement et crée les structures au fur et à mesure
    # pour cela, nous allons avoir besoin des différentes tailles
    horizontal_wall_width, horizontal_wall_height   = get_size_horizontal_wall(parameters)
    vertical_wall_width, vertical_wall_height       = get_size_vertical_wall(parameters)
    square_wall_width, square_wall_height           = get_size_square_wall(parameters)
    path_width, path_height                         = get_size_path(parameters)
    empty_block_width, empty_block_height           = get_size_empty_block(parameters)
    # on parcours l'environnement, pour connaitre la position courante, 
    # on utilise deux variables que l'on incrémente
    x = 0
    y = 0
    dy = 0
    for i, row in enumerate(environment):
        x = 0
        dy = 0
        for j, item in enumerate(split_row_env(row)):
            if isverticalwall(item):
                dx = vertical_wall_width
                dy = max(dy, vertical_wall_height)
            elif ishorizontalwall(item):
                dx = horizontal_wall_width
                dy = max(dy, horizontal_wall_height)
            elif issquarewall(item):
                dx = square_wall_width
                dy = max(dy, square_wall_height)
            elif ispath(item):
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
            elif isemptyblock(item):
                dx = empty_block_width
                dy = max(dy, empty_block_height)
            x += dx
        y += dy
    return x, y

# Les positions sont relatives au terrain de jeu
class Levels():
    
    def __init__(self, level_number, parameters):
        
        # paramètres du jeu
        self.parameters = parameters
        
        # level number
        self.level_number = level_number
        
        # environnement
        self.environment = environment(self.level_number)
        
        # on calcule les dimensions du terrain de jeu
        self.field_width, self.field_height = dimensions(self.environment, self.parameters)
        self.field_x = (self.parameters.SCREEN_WIDTH  - self.field_width ) / 2
        self.field_y = (self.parameters.SCREEN_HEIGHT - self.field_height) / 2
        origin = (self.field_x, self.field_y)
        
        # 
        self.paths, self.walls, self.dots, self.ennemies, \
            self.players, self.empty_blocks, self.shadow_walls = self.intialize(origin)
        
    def intialize(self, origin):
        
        #
        environment  = self.environment
        level_number = self.level_number
        parameters   = self.parameters
        
        # on parcours l'environnement et crée les structures au fur et à mesure
        # pour cela, nous allons avoir besoin des différentes tailles
        horizontal_wall_width, horizontal_wall_height = get_size_horizontal_wall(parameters)
        vertical_wall_width, vertical_wall_height     = get_size_vertical_wall(parameters)
        square_wall_width, square_wall_height         = get_size_square_wall(parameters)
        path_width, path_height                       = get_size_path(parameters)
        empty_block_width, empty_block_height         = get_size_empty_block(parameters)
        
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
            for j, item in enumerate(split_row_env(row)):
                
                if isverticalwall(item):
                    dx = vertical_wall_width
                    walls.add(Wall( x, y, parameters.FIELD_WALL_COLOR, dx, vertical_wall_height, origin))
                    shadow_walls.add(ShadowWall( x, y, parameters.WHITE, dx, vertical_wall_height, origin))
                    # for dy we take the max between dy and vertical_wall_height
                    # indeed, if we have a vertical wall followed by a horizontal wall, we want to take the max
                    # otherwise, we would have a gap between the two walls
                    dy = max(dy, vertical_wall_height)
                elif ishorizontalwall(item):
                    dx = horizontal_wall_width
                    walls.add(Wall( x, y, parameters.FIELD_WALL_COLOR, dx, horizontal_wall_height, origin))
                    shadow_walls.add(ShadowWall( x, y, parameters.WHITE, dx, horizontal_wall_height, origin))
                    dy = max(dy, horizontal_wall_height)
                elif issquarewall(item):
                    dx = square_wall_width
                    walls.add(Wall( x, y, parameters.FIELD_WALL_COLOR, dx, square_wall_height, origin))
                    shadow_walls.add(ShadowWall( x, y, parameters.WHITE, dx, square_wall_height, origin))
                    dy = max(dy, square_wall_height)
                elif ispath(item):
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
                    paths.add(Block(x, y, parameters.FIELD_PATH_COLOR, w, h, origin))
                    dx = w
                    dy = max(dy, h)
                elif isemptyblock(item):
                    dx = empty_block_width
                    empty_blocks.add(Block(x, y, parameters.FIELD_EMPTY_BLOCK_COLOR, dx, empty_block_height, origin, alpha=55))
                    dy = max(dy, empty_block_height)
                if isdot(item):
                    dots.add(Ellipse(x+path_width/2-parameters.ELLIPSE_WIDTH/2, # on positionne le coin supérieur gauche de l'ellipse vu comme un rectangle 
                                            y+path_height/2-parameters.ELLIPSE_HEIGHT/2, # en son centre
                                            parameters.WHITE, 
                                            parameters.ELLIPSE_WIDTH, 
                                            parameters.ELLIPSE_HEIGHT, 
                                            origin))
                    #dx = 0
                # if isplayer(item):
                #     direction = direction(item)
                #     players.add(Player(x, y, direction, parameters.PLAYER_IMAGE, self))
                #     dx = 0
                # if isennemy(item):
                #     direction = direction(item)
                #     ennemies.add(Ennemy(x, y, direction, self))
                #     dx = 0
                x += dx
            y += dy
            
        players.add(Player(100*parameters.UNIT_LENGTH/80, 104*parameters.UNIT_LENGTH/80, \
            'right', parameters.PLAYER_IMAGE, origin, self)) # à supprimer plus tard
        
        if level_number == 1:
            ennemies.add(Ennemy(1000*parameters.UNIT_LENGTH/80, 104*parameters.UNIT_LENGTH/80, 'up', origin, self))
            ennemies.add(Ennemy(300*parameters.UNIT_LENGTH/80, 500*parameters.UNIT_LENGTH/80, 'up', origin, self))
            ennemies.add(Ennemy(600*parameters.UNIT_LENGTH/80, 800*parameters.UNIT_LENGTH/80, 'up', origin, self))
            
        return paths, walls, dots, ennemies, players, empty_blocks, shadow_walls