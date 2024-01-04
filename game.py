import pygame
import datetime
import random
from levels import Levels
from menu import Menu
import utils

class Game(object):
    
    def __init__(self, parameters):
        
        # paramètres du jeu
        self.parameters = parameters
        
        # états du jeu
        self.state = dict()
        self.state["frame"]  = self.parameters.FRAMES.MENU
        self.state["action"] = self.parameters.ACTIONS.EMPTY
        
        # police pout l'affichage du score à l'écran 
        self.font = pygame.font.Font(self.parameters.SCORE_TT_FONT, 
                                     self.parameters.SCORE_FONT_SIZE)
        
        # menu du jeu
        self.menu = Menu(self.parameters)
        
        # mise en place du niveau du jeu
        self.level = Levels(self.menu.get_level(), self.parameters)

        # on démarre la musique
        try:
            self.game_music = pygame.mixer.Sound(random.choice(self.parameters.MUSIC))
        except FileNotFoundError:
            self.game_music = None
            print("Fichier audio non trouvé")
        
        # charge les effets sonores
        #self.pacman_sound    = pygame.mixer.Sound("resources/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound(self.parameters.SOUND_GAME_OVER)
    
        # chronomètre pour le jeu
        self.clock = pygame.time.Clock()
        self.temps = 0
        
        # load the background image
        self.level_background_image = pygame.image.load(self.parameters.LEVEL_BACKGROUND_IMAGE).convert()
        self.level_background_image = pygame.transform.scale(self.level_background_image,
                                                                (self.parameters.SCREEN_WIDTH, 
                                                                self.parameters.SCREEN_HEIGHT))
    
    def reset_level(self):
        
        # mise en place du niveau 1 du jeu
        self.level = Levels(self.menu.get_level(), self.parameters)
        
        # on démarre la musique
        try:
            self.game_music = pygame.mixer.Sound(random.choice(self.parameters.MUSIC))
            self.game_music.play(-1)
        except FileNotFoundError:
            self.game_music = None
            print("Fichier audio non trouvé")
        
        # on remet le chronomètre à zéro
        self.clock = pygame.time.Clock()
        self.temps = 0

    # mise à jour de l'état du jeu
    def update_state(self, action):
        
        # si l'action est de quitter le jeu depuis n'importe quel état
        # c'est l'appuie sur la croix de fermeture de la fenêtre
        if action == self.parameters.ACTIONS.QUIT:
            self.state["frame"]  = self.parameters.FRAMES.QUIT
            self.state["action"] = self.parameters.ACTIONS.EMPTY
            
        # si on est dans le menu
        elif self.state["frame"] == self.parameters.FRAMES.MENU:
            
            # si on appuie sur la touche Entrée
            if action == self.parameters.ACTIONS.RETURN:
                
                if self.menu.item() == self.parameters.MENUITEMS.PLAY:
                    self.reset_level()
                    self.state["frame"]  = self.parameters.FRAMES.GAME
                    self.state["action"] = self.parameters.ACTIONS.EMPTY
                    
                elif self.menu.item() == self.parameters.MENUITEMS.ABOUT:
                    self.state["frame"]  = self.parameters.FRAMES.ABOUT
                    self.state["action"] = self.parameters.ACTIONS.EMPTY
                    
                elif self.menu.item() == self.parameters.MENUITEMS.QUIT:
                    self.state["frame"]  = self.parameters.FRAMES.QUIT
                    self.state["action"] = self.parameters.ACTIONS.EMPTY
                    
            #elif action == self.parameters.ACTIONS.ESCAPE:
            #    self.state["action"] = self.parameters.ACTIONS.QUIT
                
        # si on est dans le about
        elif self.state["frame"] == self.parameters.FRAMES.ABOUT:
                
                if action == self.parameters.ACTIONS.BACK or \
                action == self.parameters.ACTIONS.ESCAPE:
                    self.state["frame"]  = self.parameters.FRAMES.MENU
                    self.state["action"] = self.parameters.ACTIONS.EMPTY
                
        # si on est dans le jeu
        elif self.state["frame"] == self.parameters.FRAMES.GAME:
            
            if action == self.parameters.ACTIONS.ESCAPE or \
            action == self.parameters.ACTIONS.BACK:
                self.state["frame"]  = self.parameters.FRAMES.MENU
                self.state["action"] = self.parameters.ACTIONS.EMPTY

            elif action == self.parameters.ACTIONS.GAMEOVER:
                self.state["frame"]  = self.parameters.FRAMES.GAMEOVER
                self.state["action"] = self.parameters.ACTIONS.EMPTY
                
        elif self.state["frame"] == self.parameters.FRAMES.GAMEOVER:
            
            if action == self.parameters.ACTIONS.ESCAPE or \
            action == self.parameters.ACTIONS.BACK:
                self.state["frame"]  = self.parameters.FRAMES.MENU
                self.state["action"] = self.parameters.ACTIONS.EMPTY
        
    # gère les évènements du jeu
    def process_events(self):
        
        # boucle des évènements
        for event in pygame.event.get():
                
            # si l'utilisateur clique sur la croix de fermeture de la fenêtre
            if event.type == pygame.QUIT:
                self.update_state(self.parameters.ACTIONS.QUIT)
            
            # si l'utilisateur appuie sur une touche du clavier
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.update_state(self.parameters.ACTIONS.RETURN)
                elif event.key == pygame.K_ESCAPE:
                    self.update_state(self.parameters.ACTIONS.ESCAPE)
                elif event.key == pygame.K_BACKSPACE:
                    self.update_state(self.parameters.ACTIONS.BACK)
                    
            # mise à jour de l'état du menu si on est dans le menu
            if self.state["frame"] == self.parameters.FRAMES.MENU:
                self.menu.process_event(event)
            
            # si l'on est dans le jeu est pas game over
            if self.state["frame"] == self.parameters.FRAMES.GAME and not \
            self.state["action"] == self.parameters.ACTIONS.GAMEOVER:
                # mise à jour de l'état du joueur pour tous les joueurs
                for player in self.level.players:
                    player.event_handler(event)
                    
            # si on quitte le jeu, on arrête la musique
            if self.state["frame"] == self.parameters.FRAMES.MENU and \
            self.state["action"] == self.parameters.ACTIONS.EMPTY:
                if self.game_music is not None:
                    self.game_music.stop()
                
            if self.state["frame"] == self.parameters.FRAMES.GAME and \
            self.state["action"] == self.parameters.ACTIONS.GAMEOVER:
                if self.game_music is not None:
                    self.game_music.stop()
                self.game_over_sound.play()
                
        return self.state["frame"] == self.parameters.FRAMES.QUIT
    
    # met à jour les objets du jeu
    def run_logic(self):
        
        # si on est dans le jeu et pas game over
        if self.state["frame"] == self.parameters.FRAMES.GAME and not \
        self.state["action"] == self.parameters.ACTIONS.GAMEOVER:
            
            # on met à jour le chronomètre
            self.clock.tick()
            self.temps += self.clock.get_rawtime()
            
            for player in self.level.players:
            
                if player.lives == 0:
                    break
            
                # si le joueut a été touché par un fantome, on incrémente le compteur
                if player.touched:
                    player.counter_touched += 1
                    if player.counter_touched == self.parameters.PLAYER_DURATION_FREEZE:
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
                self.update_state(self.parameters.ACTIONS.GAMEOVER)
            
            # on déplace les ennemis
            self.level.ennemies.update()
    
    # affiche les objets du jeu à l'écran
    def display_frame(self, screen):
        
        # tout d'abord effacer l'écran
        screen.fill(self.parameters.WHITE)
        
        # si on est dans le menu
        if self.state["frame"] == self.parameters.FRAMES.MENU:
            self.menu.display_frame(screen)
            
        # sinon si on est dans le about
        elif self.state["frame"] == self.parameters.FRAMES.ABOUT:
            utils.display_message(screen, "Jeu à la Pacman. Développé par Olivier et Léon Cots",
                self.parameters, 
                font = self.font,
                color_font=self.parameters.BLACK, 
                color_background=self.parameters.WHITE)
            
        # sinon si on est dans le jeu et pas game over
        elif self.state["frame"] == self.parameters.FRAMES.GAME or \
            self.state["frame"] == self.parameters.FRAMES.GAMEOVER:

            # dessin du cadre du terrain de jeu, centré à l'écran, de dimension FIELD_WIDTH x FIELD_HEIGHT
            #pygame.draw.rect(screen, BLUE,
            #                    [(SCREEN_WIDTH - FIELD_WIDTH) / 2,
            #                    (SCREEN_HEIGHT - FIELD_HEIGHT) / 2,
            #                    FIELD_WIDTH, FIELD_HEIGHT], 2)
            
            # arrière-plan du jeu
            screen.fill(self.parameters.GAME_BACKGROUND_COLOR)
            
            # dessin des chemins
            #self.level.paths.draw(screen)
            
            # dessin de l'arrière plan du niveau
            screen.blit(self.level_background_image, [0, 0])
            
            # dessin de l'environnement : les murs
            if self.level.level_number == 0:
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
            SW = self.parameters.SCREEN_WIDTH
            SH = self.parameters.SCREEN_HEIGHT
            DW = (SW - self.level.field_width) / 2
            DH = (SH - self.level.field_height) / 2
            pygame.draw.rect(screen, self.parameters.GAME_BACKGROUND_COLOR, [0, 0, DW, SH])
            pygame.draw.rect(screen, self.parameters.GAME_BACKGROUND_COLOR, [0, 0, SW, DH])
            pygame.draw.rect(screen, self.parameters.GAME_BACKGROUND_COLOR, [0, SH - DH, SW, DH])
            pygame.draw.rect(screen, self.parameters.GAME_BACKGROUND_COLOR, [SW - DW, 0, DW, SH])
            
            # on fait un panneau pour mettre le score et les vies
            pygame.draw.rect(screen, self.parameters.PANEL_BACKGROUND_COLOR, [0, 0, SW, 60])
            
            img_live = pygame.image.load("resources/coeur.png").convert_alpha()
            for player in self.level.players:
                
                # affiche le score à l'écran
                text = self.font.render("Score : " + str(player.score), True, self.parameters.SCORE_FONT_COLOR)
                screen.blit(text, [200, 20])
                
                # affiche les vies du joueur à l'écran
                screen.blit(pygame.transform.scale(player.image_save, (30, 30)), [50, 20])
                for i in range(player.lives):
                    screen.blit(img_live, [68 + (i+1) * 22, 24])
                    
                # affiche le temps de jeu à l'écran
                # on convertit le temps en minutes et secondes
                temps = datetime.timedelta(milliseconds=self.temps)
                # n'affiche que les minutes et secondes
                text = self.font.render("Temps : " + str(temps)[2:-7], True, self.parameters.SCORE_FONT_COLOR)
                screen.blit(text, [SW - 300, 20])
            
        # # sinon si dans le jeu est game over
        if self.state["frame"] == self.parameters.FRAMES.GAMEOVER:
            utils.display_message(screen, "Game Over", self.parameters,
                font = self.font,
                color_font=self.parameters.RED, 
                color_background=self.parameters.WHITE)
            
        # rafraichissement de l'écran
        pygame.display.flip()

