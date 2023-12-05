import pygame
import datetime
import random
from levels import Levels
from menu import Menu
from parameters import Parameters

# les paramètres du jeu
parameters = Parameters()

# couleurs du jeu
BLACK = parameters.BLACK
WHITE = parameters.WHITE
BLUE  = parameters.BLUE
GREEN = parameters.GREEN
RED   = parameters.RED

class Game(object):
    
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        
        self.SCREEN_WIDTH  = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT
        
        # états du jeu
        self.state = dict()
        self.state["frame"]  = parameters.FRAMES.MENU
        self.state["action"] = parameters.ACTIONS.EMPTY
        
        # police pout l'affichage du score à l'écran 
        self.font = pygame.font.Font(parameters.SCORE_TT_FONT, 
                                     parameters.SCORE_FONT_SIZE)
        
        # menu du jeu
        self.menu = Menu(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # mise en place du niveau 1 du jeu
        self.level = Levels(1, SCREEN_WIDTH, SCREEN_HEIGHT)

        # on démarre la musique
        self.game_music = pygame.mixer.Sound(random.choice(parameters.MUSIC))
        
        # charge les effets sonores
        #self.pacman_sound    = pygame.mixer.Sound("resources/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound(parameters.SOUND_GAME_OVER)
    
        # chronomètre pour le jeu
        self.clock = pygame.time.Clock()
        self.temps = 0
    
    def reset_level(self):
        
        # mise en place du niveau 1 du jeu
        self.level = Levels(1, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        
        # on démarre la musique
        self.game_music = pygame.mixer.Sound(random.choice(parameters.MUSIC))
        self.game_music.play(-1)
        
        # on remet le chronomètre à zéro
        self.clock = pygame.time.Clock()
        self.temps = 0

    def update_state(self, action):
        
        # si l'action est de quitter le jeu depuis n'importe quel état
        # c'est l'appuie sur la croix de fermeture de la fenêtre
        if action == parameters.ACTIONS.QUIT:
            self.state["action"] = parameters.ACTIONS.QUIT
            
        # si on est dans le menu
        elif self.state["frame"] == parameters.FRAMES.MENU:
            
            # si on appuie sur la touche Entrée
            if action == parameters.ACTIONS.RETURN:
                
                if self.menu.item() == parameters.MENUITEMS.PLAY:
                    self.reset_level()
                    self.state["frame"]  = parameters.FRAMES.GAME
                    self.state["action"] = parameters.ACTIONS.EMPTY
                    
                elif self.menu.item() == parameters.MENUITEMS.ABOUT:
                    self.state["frame"]  = parameters.FRAMES.ABOUT
                    self.state["action"] = parameters.ACTIONS.EMPTY
                    
                elif self.menu.item() == parameters.MENUITEMS.QUIT:
                    self.state["action"] = parameters.ACTIONS.QUIT
                    
            elif action == parameters.ACTIONS.ESCAPE:
                self.state["action"] = parameters.ACTIONS.QUIT
                
        # si on est dans le about
        elif self.state["frame"] == parameters.FRAMES.ABOUT:
                
                if action == parameters.ACTIONS.BACK or \
                action == parameters.ACTIONS.ESCAPE:
                    self.state["frame"]  = parameters.FRAMES.MENU
                    self.state["action"] = parameters.ACTIONS.EMPTY
                
        # si on est dans le jeu
        elif self.state["frame"] == parameters.FRAMES.GAME:
            
            if action == parameters.ACTIONS.ESCAPE or \
            action == parameters.ACTIONS.BACK:
                self.state["frame"]  = parameters.FRAMES.MENU
                self.state["action"] = parameters.ACTIONS.EMPTY
        
    def process_events(self):
        
        # boucle des évènements
        for event in pygame.event.get():
                
            # si l'utilisateur clique sur la croix de fermeture de la fenêtre
            if event.type == pygame.QUIT:
                self.update_state(parameters.ACTIONS.QUIT)
            
            # si l'utilisateur appuie sur une touche du clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.update_state(parameters.ACTIONS.RETURN)
                elif event.key == pygame.K_ESCAPE:
                    self.update_state(parameters.ACTIONS.ESCAPE)
                elif event.key == pygame.K_BACKSPACE:
                    self.update_state(parameters.ACTIONS.BACK)
                    
            # mise à jour de l'état du menu si on est dans le menu
            if self.state["frame"] == parameters.FRAMES.MENU:
                self.menu.event_handler(event)
            
            # si l'on est dans le jeu est pas game over
            if self.state["frame"] == parameters.FRAMES.GAME and not \
            self.state["action"] == parameters.ACTIONS.GAMEOVER:
                # mise à jour de l'état du joueur pour tous les joueurs
                for player in self.level.players:
                    player.event_handler(event)
                    
            # si on quitte le jeu, on arrête la musique
            if self.state["frame"] == parameters.FRAMES.MENU and \
            self.state["action"] == parameters.ACTIONS.EMPTY:
                self.game_music.stop()
                
            if self.state["frame"] == parameters.FRAMES.GAME and \
            self.state["action"] == parameters.ACTIONS.GAMEOVER:
                self.game_music.stop()
                self.game_over_sound.play()
                
        return self.state["action"] == parameters.ACTIONS.QUIT
    
    # met à jour les objets du jeu
    def run_logic(self):
        
        # si on est dans le jeu et pas game over
        if self.state["frame"] == parameters.FRAMES.GAME and not \
        self.state["action"] == parameters.ACTIONS.GAMEOVER:
            
            # on met à jour le chronomètre
            self.clock.tick()
            self.temps += self.clock.get_rawtime()
            
            for player in self.level.players:
            
                if player.lives == 0:
                    break
            
                # si le joueut a été touché par un fantome, on incrémente le compteur
                if player.touched:
                    player.counter_touched += 1
                    if player.counter_touched == parameters.PLAYER_DURATION_FREEZE:
                        player.touched = False
                        player.counter_touched = 0
                else:
                    # on met à jour le joueur
                    player.update()
                    
                    # détection de collision entre le joueur et les points
                    block_hit_list = pygame.sprite.Group()
                    block_hit_list.add(pygame.sprite.spritecollide(player, 
                                                                    self.level.dots, 
                                                                    True,
                                                                    pygame.sprite.collide_rect_ratio(0.3)))
                    if len(block_hit_list) > 0:
                        player.score += 1
                        
                    # détection de collision entre le joueur et les fantomes
                    block_hit_list = pygame.sprite.Group()
                    block_hit_list.add(pygame.sprite.spritecollide(player, 
                                                                    self.level.ennemies, 
                                                                    False,
                                                                    pygame.sprite.collide_rect_ratio(0.6)))
                    if len(block_hit_list) > 0:
                        #self.game_over_sound.play()
                        player.lives -= 1
                        player.touched = True
                
            # on met à jour l'état du jeu pour la fin de partie
            is_game_over = True
            for player in self.level.players:
                if player.lives > 0:
                    is_game_over = False
            if is_game_over:
                self.state["action"] = parameters.ACTIONS.GAMEOVER
            
            # on déplace les ennemis
            self.level.ennemies.update() #self.level.horizontal_paths, 
                                       #self.level.vertical_paths)
    
    # affiche les objets du jeu à l'écran
    def display_frame(self, screen):
        
        # tout d'abord effacer l'écran
        screen.fill(WHITE)
        
        # si on est dans le menu
        if self.state["frame"] == parameters.FRAMES.MENU:
            self.menu.display_frame(screen)
            
        # sinon si on est dans le about
        elif self.state["frame"] == parameters.FRAMES.ABOUT:
            self.display_message(screen, "Jeu à la Pacman. Développé par Olivier et Léon Cots", color_font=BLACK, \
                color_background=WHITE)
            
        # sinon si on est dans le jeu et pas game over
        elif self.state["frame"] == parameters.FRAMES.GAME:

            # dessin du cadre du terrain de jeu, centré à l'écran, de dimension FIELD_WIDTH x FIELD_HEIGHT
            #pygame.draw.rect(screen, BLUE,
            #                    [(SCREEN_WIDTH - FIELD_WIDTH) / 2,
            #                    (SCREEN_HEIGHT - FIELD_HEIGHT) / 2,
            #                    FIELD_WIDTH, FIELD_HEIGHT], 2)
            
            # arrière-plan du jeu
            screen.fill(parameters.GAME_BACKGROUND_COLOR)
            
            # dessin des chemins
            self.level.paths.draw(screen)
            
            # dessin de l'environnement : les murs
            self.level.shadow_walls.draw(screen)
            self.level.walls.draw(screen)
            
            # dessins des blocs vides
            self.level.empty_blocks.draw(screen)
            
            # dessin des points
            self.level.dots.draw(screen)
            
            # dessin des ennemis
            self.level.ennemies.draw(screen)
            
            # dessin du joueur
            for player in self.level.players:
                if player.lives > 0:
                    screen.blit(player.image, player.rect)
                    
            # pour ne rien avoir qui dépasse du terrain de jeu on remet la couleur de fond
            # autour du terrain de jeu
            # il faut donc dessiner 4 rectangles
            pygame.draw.rect(screen, parameters.GAME_BACKGROUND_COLOR,
                                [0, 0, (self.SCREEN_WIDTH - self.level.field_width) / 2, self.SCREEN_HEIGHT])
            pygame.draw.rect(screen, parameters.GAME_BACKGROUND_COLOR,
                                [0, 0, self.SCREEN_WIDTH, (self.SCREEN_HEIGHT - self.level.field_height) / 2])
            pygame.draw.rect(screen, parameters.GAME_BACKGROUND_COLOR,
                                [0, self.SCREEN_HEIGHT - (self.SCREEN_HEIGHT - self.level.field_height) / 2, 
                                 self.SCREEN_WIDTH, (self.SCREEN_HEIGHT - self.level.field_height) / 2])
            pygame.draw.rect(screen, parameters.GAME_BACKGROUND_COLOR,
                                [self.SCREEN_WIDTH - (self.SCREEN_WIDTH - self.level.field_width) / 2, 0, 
                                 (self.SCREEN_WIDTH - self.level.field_width) / 2, self.SCREEN_HEIGHT])
            
            # on fait un panneau pour mettre le score et les vies
            pygame.draw.rect(screen, parameters.PANEL_BACKGROUND_COLOR,
                                [0, 0, self.SCREEN_WIDTH, 60])
            
            img_live = pygame.image.load("resources/coeur.png").convert_alpha()
            for player in self.level.players:
                
                # affiche le score à l'écran
                text = self.font.render("Score : " + str(player.score), True, parameters.SCORE_FONT_COLOR)
                screen.blit(text, [200, 20])
                
                # affiche les vies du joueur à l'écran
                screen.blit(pygame.transform.scale(player.image_save, (30, 30)), [50, 20])
                for i in range(player.lives):
                    screen.blit(img_live, [68 + (i+1) * 22, 24])
                    
                # affiche le temps de jeu à l'écran
                # on convertit le temps en minutes et secondes
                temps = datetime.timedelta(milliseconds=self.temps)
                # n'affiche que les minutes et secondes
                text = self.font.render("Temps : " + str(temps)[2:-7], True, parameters.SCORE_FONT_COLOR)
                screen.blit(text, [self.SCREEN_WIDTH - 300, 20])
            
        # # sinon si dans le jeu est game over
        # if self.state["frame"] == parameters.FRAMES.GAME and \
        # self.state["action"] == parameters.ACTIONS.GAMEOVER:
        #     self.display_message(screen, "Game Over")
            
        # rafraichissement de l'écran
        pygame.display.flip()
        
    # affiche un message à l'écran
    def display_message(self, screen, message, *, color_font=parameters.FONT_COLOR, \
        color_background=parameters.PANEL_BACKGROUND_COLOR):
        label = self.font.render(message, True, color_font)
        width = label.get_width()
        height = label.get_height()
        posX = (self.SCREEN_WIDTH / 2) - (width / 2)
        posY = (self.SCREEN_HEIGHT / 2) - (height / 2)
        # on ajoute un panneau autour du message
        d = 50
        pygame.draw.rect(screen, color_background, [posX - d, posY - d, width + 2*d, height + 2*d])
        # on affiche le message
        screen.blit(label, (posX, posY))
