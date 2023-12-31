import pygame

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class MenuNode(object):
    
    def __init__(self, *, itemid=None, name="Menu", children=None, values=None, root=False):
        self.itemid        = itemid
        self.name          = name
        self.children      = children
        self.values        = values
        self.index         = 0
        self.parent        = None
        self.brother_left  = None
        self.brother_right = None
        if children is not None:
            for child in children:
                child.parent = self
            for i in range(len(children)):
                if i > 0:
                    children[i].brother_left = children[i-1]
                if i < len(children) - 1:
                    children[i].brother_right = children[i+1]
        self.root = root

class MenuLeafSimple(MenuNode):

    def __init__(self, itemid, name):
        super().__init__(itemid=itemid, name=name)

class MenuLeafValues(MenuNode):

    def __init__(self,itemid, name, values):
        super().__init__(itemid=itemid, name=name, values=values)

class MenuNoLeaf(MenuNode):
    
    def __init__(self, itemid, name, children):
        super().__init__(itemid=itemid, name=name, children=children)

class MenuTree(MenuNode):
    
    def __init__(self, children):
        
        #
        super().__init__(children=children, root=True) 
        
        # raise an error if children is not a list and if it is an empty list
        if not isinstance(children, list):
            raise ValueError("children must be a list")
        if len(children) == 0:
            raise ValueError("children must not be an empty list")
        self.current = self.children[0]
    
#
class Menu(object):
    
    def __init__(self, parameters):
        
        self.parameters = parameters
        self.font       = pygame.font.Font(self.parameters.MENU_TT_FONT, 
                                           self.parameters.MENU_FONT_SIZE)
        
        # make the menu tree
        MENUITEMS = self.parameters.MENUITEMS
        MENU_ITEMS_NAMES = self.parameters.MENU_ITEMS_NAMES
        
        # 
        item_play  = self.make_item(itemid=MENUITEMS.PLAY,  name=MENU_ITEMS_NAMES[MENUITEMS.PLAY])
        item_level = self.make_item(itemid=MENUITEMS.LEVEL, name=MENU_ITEMS_NAMES[MENUITEMS.LEVEL],
                                    values=[1, 2])
        item_about = self.make_item(itemid=MENUITEMS.ABOUT, name=MENU_ITEMS_NAMES[MENUITEMS.ABOUT])
        item_quit  = self.make_item(itemid=MENUITEMS.QUIT,  name=MENU_ITEMS_NAMES[MENUITEMS.QUIT])
        
        # 
        item_opt_fullscreen = self.make_item(itemid=MENUITEMS.OPTION, name='Plein écran',
                                             values=[False, True])
        item_opt_sound      = self.make_item(itemid=MENUITEMS.OPTION, name='Son        ',
                                             values=[False, True])
        item_option = self.make_submenu(itemid=MENUITEMS.OPTION, 
                                        name=MENU_ITEMS_NAMES[MENUITEMS.OPTION],
                                        subitems=[item_opt_fullscreen, item_opt_sound])
        
        #
        self.state = self.make_menu(items=[item_play, 
                                           item_level, 
                                           item_option,
                                           item_about, 
                                           item_quit])
    
    def item(self):
        return self.parameters.MENUITEMS(self.state.current.itemid)
   
    # affiche le menu
    def print_menu_tree(self, node, level=0):
        if node is not None:
            if node == self.state.current:
                DEB = color.BOLD
                FIN = color.END
            else:
                DEB = ""
                FIN = ""
            if node.values is not None:
                FIN = FIN + " < " + str(node.values[node.index]) + " >"
            print("  " * level + DEB + node.name + FIN)
            if node.children is not None:
                for child in node.children:
                    self.print_menu_tree(child, level+1)
   
    # mise à jour de l'état du menu
    def update_state(self, action):
        
        current = self.state.current
        if action == self.parameters.ACTIONS.UP:
            if current.brother_left is not None:
                self.state.current = current.brother_left
        elif action == self.parameters.ACTIONS.DOWN:
            if current.brother_right is not None:
                self.state.current = current.brother_right
        elif action == self.parameters.ACTIONS.LEFT:
            # update self.current.index if possible
            if current.values is not None:
                if current.index > 0:
                    current.index -= 1
                else:
                    current.index = len(current.values) - 1
        elif action == self.parameters.ACTIONS.RIGHT:
            # update self.current.index if possible
            if current.values is not None:
                if current.index < len(current.values) - 1:
                    current.index += 1
                else:
                    current.index = 0
        elif action == self.parameters.ACTIONS.RETURN:
            if current.children is not None:
                self.state.current = current.children[0]
        elif action == self.parameters.ACTIONS.BACK or action == self.parameters.ACTIONS.ESCAPE:
            if current.parent is not None and current.parent.root is False:
                self.state.current = current.parent
        
        #
        # self.print_menu_tree(self.state)
   
    # gère les événements clavier dans le menu
    def process_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.update_state(self.parameters.ACTIONS.UP)
            elif event.key == pygame.K_DOWN:
                self.update_state(self.parameters.ACTIONS.DOWN)
            elif event.key == pygame.K_LEFT:
                self.update_state(self.parameters.ACTIONS.LEFT)
            elif event.key == pygame.K_RIGHT:
                self.update_state(self.parameters.ACTIONS.RIGHT)
            elif event.key == pygame.K_RETURN:
                self.update_state(self.parameters.ACTIONS.RETURN)
            elif event.key == pygame.K_ESCAPE:
                self.update_state(self.parameters.ACTIONS.ESCAPE)
            elif event.key == pygame.K_BACKSPACE:
                self.update_state(self.parameters.ACTIONS.BACK)

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
        
        posX     = (self.parameters.SCREEN_WIDTH / 4)  # - (width / 2)
        posYs    = []
        maxwidth = 0
        items = self.state.current.parent.children
        for index, item in enumerate(items):
            
            if item == self.state.current:
                color = self.parameters.MENU_SELECT_COLOR
            else:
                color = self.parameters.MENU_ITEM_COLOR
            
            label  = self.font.render(item.name, True, color)
            width  = label.get_width()
            maxwidth = max(maxwidth, width)
            height = 1.5*label.get_height()
            t_h    = len(items) * height
            posY   = (self.parameters.SCREEN_HEIGHT / 2) - (t_h / 2) + (index * height)
            posYs.append(posY)
            screen.blit(label, (posX, posY))
            
        for index, item in enumerate(items):
                    
            if item == self.state.current:
                color = self.parameters.MENU_SELECT_COLOR
            else:
                color = self.parameters.MENU_ITEM_COLOR
                
            if item.values is not None:
                value = " < " + str(item.values[item.index]) + " >"
            else:
                value = ""
            
            label = self.font.render(value, True, color)
            posY  = posYs[index]
            screen.blit(label, (posX + 1.1*maxwidth, posY))
             
    # make a MenuLeaf or a MenuNoLeaf
    def make_item(self, *, itemid, name, values=None, children=None):
        if children is None:
            if values is None:
                return MenuLeafSimple(itemid, name)
            else:
                # if values is empty raise an error
                if len(values) == 0:
                    raise ValueError("values must not be an empty list")
                return MenuLeafValues(itemid, name, values)
        else:
            return MenuNoLeaf(itemid, name, children)
        
    # make a submenu from a list of items, an itemid and a name
    def make_submenu(self, *, itemid, name, subitems):
        # if subitems is empty raise an error
        if len(subitems) == 0:
            raise ValueError("subitems must not be an empty list")
        return self.make_item(itemid=itemid, name=name, children=subitems)
    
    # make a menu from a list of items
    def make_menu(self, *, items):
        # if items is empty raise an error
        if len(items) == 0:
            raise ValueError("items must not be an empty list")
        return MenuTree(items)