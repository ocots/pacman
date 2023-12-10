import pygame

class Menu(object):
    
    def __init__(self, parameters):
        
        self.parameters    = parameters
        self.state         = self.parameters.MENUITEMS.PLAY.value
        self.font          = pygame.font.Font(self.parameters.MENU_TT_FONT, 
                                              self.parameters.MENU_FONT_SIZE)
    
    def item(self):
        return self.parameters.MENUITEMS(self.state)
    
    def display_frame(self, screen):
        # on efface l'écran
        screen.fill(self.parameters.MENU_BACKGROUND_COLOR)
        
        # on affiche le titre du jeu
        label = self.font.render(self.parameters.TITLE, True, self.parameters.MENU_TITLE_COLOR)
        # on calcule la position du texte
        width  = label.get_width()
        height = label.get_height()
        posX = (self.parameters.SCREEN_WIDTH / 2) - (width / 2)
        posY = 0.25 * ( (self.parameters.SCREEN_HEIGHT / 2) - (height / 2) )
        screen.blit(label, (posX, posY))
        
        for index, item in enumerate(self.parameters.MENU_ITEMS):
            if self.state == index:
                # si l'item est sélectionné, on affiche le texte avec la couleur de sélection
                label = self.font.render(self.parameters.MENU_ITEMS_NAMES[item], 
                                         True, self.parameters.MENU_SELECT_COLOR)
            else:
                # sinon on affiche le texte avec la couleur par défaut
                label = self.font.render(self.parameters.MENU_ITEMS_NAMES[item], 
                                         True, self.parameters.MENU_FONT_COLOR)
            
            # on calcule la position du texte
            width  = label.get_width()
            height = label.get_height()
            posX = (self.parameters.SCREEN_WIDTH / 2) - (width / 2)
            t_h = len(self.parameters.MENU_ITEMS) * height # t_h: total height of text block
            posY = (self.parameters.SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)
            screen.blit(label, (posX, posY))
            
    # pour se balader dans le menu
    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.parameters.MENU_ITEMS) - 1:
                    self.state += 1
