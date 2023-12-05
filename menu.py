import pygame
from parameters import Parameters

# les paramètres du jeu
parameters = Parameters()

# dimension de l'écran
#SCREEN_WIDTH  = parameters.SCREEN_WIDTH
#SCREEN_HEIGHT = parameters.SCREEN_HEIGHT

class Menu(object):
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        
        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        self.state        = parameters.MENUITEMS.PLAY.value
        self.font         = pygame.font.Font(parameters.MENU_TT_FONT, 
                                             parameters.MENU_FONT_SIZE)
    
    def item(self):
        return parameters.MENUITEMS(self.state)
    
    def display_frame(self, screen):
        # on efface l'écran
        screen.fill(parameters.MENU_BACKGROUND_COLOR)
        
        # on affiche le titre du jeu
        label = self.font.render(parameters.TITLE, True, parameters.MENU_TITLE_COLOR)
        # on calcule la position du texte
        width  = label.get_width()
        height = label.get_height()
        posX = (self.SCREEN_WIDTH / 2) - (width / 2)
        posY = 0.25 * ( (self.SCREEN_HEIGHT / 2) - (height / 2) )
        screen.blit(label, (posX, posY))
        
        for index, item in enumerate(parameters.MENU_ITEMS):
            if self.state == index:
                # si l'item est sélectionné, on affiche le texte avec la couleur de sélection
                label = self.font.render(parameters.MENU_ITEMS_NAMES[item], 
                                         True, parameters.MENU_SELECT_COLOR)
            else:
                # sinon on affiche le texte avec la couleur par défaut
                label = self.font.render(parameters.MENU_ITEMS_NAMES[item], 
                                         True, parameters.MENU_FONT_COLOR)
            
            # on calcule la position du texte
            width  = label.get_width()
            height = label.get_height()
            posX = (self.SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(parameters.MENU_ITEMS) * height # t_h: total height of text block
            posY = (self.SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)
            screen.blit(label, (posX, posY))
            
    # pour se balader dans le menu
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(parameters.MENU_ITEMS) - 1:
                    self.state += 1
