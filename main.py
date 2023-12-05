import tkinter
import pygame
from game import Game
from parameters import Parameters

# les paramètres du jeu
parameters = Parameters()

# dimension de l'écran
#SCREEN_WIDTH  = parameters.SCREEN_WIDTH
#SCREEN_HEIGHT = parameters.SCREEN_HEIGHT

# FPS
FPS = parameters.FPS

def main():
 
    root = tkinter.Tk()
    root.withdraw()
    SCREEN_WIDTH, SCREEN_HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
    
    # pygame setup
    pygame.init()
    pygame.display.set_caption("Pacman")
    screen  = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    running = True
    clock   = pygame.time.Clock()
    
    # crée le jeu
    game = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # boucle du jeu principale
    while running:
        
        # gère les évènements du jeu: fermeture de la fenêtre, touches du clavier, etc.
        running = not game.process_events()
        
        # met à jour les objets du jeu
        game.run_logic()
        
        # affiche les objets du jeu à l'écran
        game.display_frame(screen)
        
        # limite le jeu à FPS images par seconde
        clock.tick(FPS)

    # ferme le jeu
    pygame.quit()
    
if __name__ == "__main__":
    main()