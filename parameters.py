from enum import Enum
import math

class MenuItems(Enum):
    PLAY  = 0
    ABOUT = 1
    QUIT  = 2
    LEVEL = 3
    OPTION = 4
    
class Frames(Enum):
    MENU  = 0
    GAME  = 1
    ABOUT = 2
    QUIT  = 3
    GAMEOVER = 4
    
class Actions(Enum):
    RETURN   = 0
    BACK     = 1
    QUIT     = 2
    GAMEOVER = 3
    EMPTY    = 4
    ESCAPE   = 5
    DOWN     = 6
    UP       = 7
    LEFT     = 8
    RIGHT    = 9

class Parameters():
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        
        #
        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
        # couleurs
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE  = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        self.RED   = (205, 0, 0)
        self.BLUE_MATE = (0, 127, 162)
        self.BROWN = (60, 30, 0)
        self.GRAY = (155, 155, 155)
        self.LIGHT_GRAY = (200, 200, 200)
        self.ROUGE_BRIQUE = (181, 50, 11)
        
        # Enum
        self.MENUITEMS = MenuItems
        self.FRAMES = Frames
        self.ACTIONS = Actions
        
        # FPS
        self.FPS = 30
        
        #
        self.TITLE = "Pacman Reloaded"
        
        # MENU
        self.MENU_BACKGROUND_COLOR  = self.WHITE
        self.MENU_TITLE_COLOR       = self.BLUE_MATE
        self.MENU_FONT_COLOR        = self.BLACK
        self.MENU_ITEM_COLOR        = self.BLACK
        self.MENU_SELECT_COLOR      = self.RED
        self.MENU_FONT_SIZE         = 40
        self.MENU_TT_FONT           = None
        self.MENU_ITEMS_NAMES       = { self.MENUITEMS.PLAY: 'Jouer',
                                        self.MENUITEMS.LEVEL: 'Niveau',
                                        self.MENUITEMS.OPTION: 'Options',
                                        self.MENUITEMS.ABOUT: 'A propos',
                                        self.MENUITEMS.QUIT: 'Quitter'}
        
        # DEFAULT FONT COLOR
        self.FONT_COLOR = self.WHITE
        
        # PANEL
        self.PANEL_BACKGROUND_COLOR = self.BLUE_MATE
        
        # SCORE
        self.SCORE_FONT_COLOR   = self.WHITE
        self.SCORE_TT_FONT      = None
        self.SCORE_FONT_SIZE    = 35
        
        #
        if self.SCREEN_WIDTH <= 1200 or self.SCREEN_HEIGHT <= 800:
            self.UNIT_LENGTH = 52
        else:
            self.UNIT_LENGTH = 80
        
        # GAME
        self.MUSIC              = ( "resources/music/soprano-coach.mp3",
                                    "resources/music/soprano-marseille.mp3",
                                    "resources/music/alonzo-normal.mp3",
                                    "resources/music/bigflo-oli-coup-vieux.mp3",
                                    "resources/music/biglo-oli-ca-va-beaucoup-trop-vite.mp3",
                                    "resources/music/soprano-chasseur-d-etoiles.mp3")
        self.SOUND_GAME_OVER    = "resources/game_over.wav"
        
        # JOUEUR
        self.PLAYER_IMAGE       = "resources/perso-rond.png"
        self.PLAYER_SPEED       = 9
        self.PLAYER_WIDTH       = 0.7*self.UNIT_LENGTH
        self.PLAYER_HEIGHT      = 0.7*self.UNIT_LENGTH
        self.PLAYER_LIVES       = 3
        #self.PLAYER_DISTANCE_TO_CROSSROAD = self.UNIT_LENGTH/2.2
        self.PLAYER_DURATION_FREEZE = 50
        self.PLAYER_EPSILON_WALL = math.pi/10
        
        # ENNEMIS
        self.ENNEMY_IMAGE       = "resources/fantome-perso.png"
        self.ENNEMY_SPEED       = 7
        self.ENNEMY_WIDTH       = 0.7*self.UNIT_LENGTH
        self.ENNEMY_HEIGHT      = 0.7*self.UNIT_LENGTH
        self.ENNEMY_DELAY_DIRECTION_CHANGE = 10
        #self.ENNEMY_DISTANCE_TO_CROSSROAD = 4
        self.ENNEMY_EPSILON_WALL = math.pi/6
        
        # DIMENSIONS DU DECOR
        self.BLOCK_WIDTH        = self.UNIT_LENGTH #32
        self.BLOCK_HEIGHT       = self.UNIT_LENGTH #32
        #
        self.WALL_BIG_LENGTH    = self.UNIT_LENGTH #32
        self.WALL_SMALL_LENGTH  = 2*self.UNIT_LENGTH//26  #3
        self.WALL_DISTANCE_TO_CORNER = self.UNIT_LENGTH//2.5
        #
        self.ELLIPSE_WIDTH      = self.UNIT_LENGTH//4
        self.ELLIPSE_HEIGHT     = self.UNIT_LENGTH//4
        #self.ELLIPSE_COLOR      = self.GREEN
        
        # COULEURS DU DECOR
        self.GAME_BACKGROUND_COLOR = self.GRAY
        self.FIELD_WALL_COLOR = self.BLACK
        self.FIELD_PATH_COLOR = self.ROUGE_BRIQUE
        self.FIELD_EMPTY_BLOCK_COLOR = self.BLACK
        
        # LEVEL
        self.LEVEL_BACKGROUND_IMAGE = "resources/level-background.jpg"