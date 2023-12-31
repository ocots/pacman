import pygame
import math

# affiche un message à l'écran
def display_message(screen, message, parameters, *, font, color_font, color_background):
    #
    label  = font.render(message, True, color_font)
    width  = label.get_width()
    height = label.get_height()
    posX   = (parameters.SCREEN_WIDTH / 2) - (width / 2)
    posY   = (parameters.SCREEN_HEIGHT / 2) - (height / 2)
    # on ajoute un panneau autour du message
    d = 50
    pygame.draw.rect(screen, color_background, [posX - d, posY - d, width + 2*d, height + 2*d])
    # on affiche le message
    screen.blit(label, (posX, posY))

def update_state_tore(sprite):
    # on vérifie si le sprite est sorti du terrain de jeu
    # sachant que le terrain de jeu est centré à l'écran
    # et qu'il se déplace sur un tore
    FX = sprite.level.field_x
    FY = sprite.level.field_y
    FW = sprite.level.field_width
    FH = sprite.level.field_height
    dx = sprite.rect.width / 2
    dy = sprite.rect.height / 2
    if sprite.rect.right < (FX + dx) :
        sprite.rect.left = FX + FW - dx
    elif sprite.rect.left > (FX + FW - dx):
        sprite.rect.right = FX + dx
    if sprite.rect.bottom < (FY + dy):
        sprite.rect.top = FY + FH - dy
    elif sprite.rect.top > (FY + FH - dy):
        sprite.rect.bottom = FY + dy
        
def update_state_collision_walls(sprite, e, d):
    
    #
    left_blocked   = False
    right_blocked  = False
    top_blocked    = False
    bottom_blocked = False
        
    # on évite les collisions avec les murs en utilisant les ShadowWall
    for block in pygame.sprite.spritecollide(sprite, sprite.level.shadow_walls, False):
                       
        # coordinates of the center of the player in the (x,y) plane centered in the block
        x = sprite.rect.centerx - block.rect.centerx
        y = block.rect.centery - sprite.rect.centery
        
        # 
        # get the angle of the vector (x,y) in the (x,y) plane
        angle = math.atan2(y, x) # between -pi and pi
        angle = angle % (2*math.pi) # between 0 and 2*pi
        # get the angle of reference for the block: 
        # that is tha angle of the vector joining the center and the top right corner of the block
        a = math.atan2(block.rect.height/2, block.rect.width/2)
        a = a % (2*math.pi) # between 0 and 2*pi
        # 
        if not (a >= 0 and a < math.pi/2):
            raise ValueError("a = %f" % a)
        
        # [2pi-a+e, a-e]: right
        if angle > (2.0*math.pi-a+e) or angle < (a-e):
            sprite.change_x = 0
            sprite.rect.left = block.rect.right
            left_blocked = True
            
        # [a+e, pi-a-e]: top
        elif angle > (a+e) and angle < (math.pi-a-e):
            sprite.change_y = 0
            sprite.rect.bottom = block.rect.top
            bottom_blocked = True
        
        # [pi-a+e, pi+a-e]: left
        elif angle > (math.pi-a+e) and angle < (math.pi+a-e):
            sprite.change_x = 0
            sprite.rect.right = block.rect.left
            right_blocked = True
            
        # [pi+a+e, 2pi-a-e]: bottom
        elif angle > (math.pi+a+e) and angle < (2*math.pi-a-e):
            sprite.change_y = 0
            sprite.rect.top = block.rect.bottom
            top_blocked = True
            
        # in the last 4 following cases, we have to check the distance to the block
        # top-right: [a-e, a+e]
        elif angle >= (a-e) and angle < (a+e):
            # get the vector joining the top right corner of the block and the center of the player
            dx = sprite.rect.centerx - block.rect.right
            dy = block.rect.top - sprite.rect.centery
            # move the player at the distance d from the corner of the block in the direction (dx, dy)
            sprite.rect.centerx = block.rect.right + d * dx / math.sqrt(dx*dx + dy*dy)
            sprite.rect.centery = block.rect.top - d * dy / math.sqrt(dx*dx + dy*dy) 
            
        # top-left: [pi-a-e, pi-a+e]
        elif angle >= (math.pi-a-e) and angle < (math.pi-a+e):
            # get the vector joining the top left corner of the block and the center of the player
            dx = sprite.rect.centerx - block.rect.left
            dy = block.rect.top - sprite.rect.centery
            # move the player at the distance d from the corner of the block in the direction (dx, dy)
            sprite.rect.centerx = block.rect.left + d * dx / math.sqrt(dx*dx + dy*dy)
            sprite.rect.centery = block.rect.top - d * dy / math.sqrt(dx*dx + dy*dy)
            
        # bottom-left: [pi+a-e, pi+a+e]
        elif angle >= (math.pi+a-e) and angle < (math.pi+a+e):
            # get the vector joining the bottom left corner of the block and the center of the player
            dx = sprite.rect.centerx - block.rect.left
            dy = block.rect.bottom - sprite.rect.centery
            # move the player at the distance d from the corner of the block in the direction (dx, dy)
            sprite.rect.centerx = block.rect.left + d * dx / math.sqrt(dx*dx + dy*dy)
            sprite.rect.centery = block.rect.bottom - d * dy / math.sqrt(dx*dx + dy*dy)
            
        # bottom-right: [2pi-a-e, 2pi-a+e]
        elif angle >= (2*math.pi-a-e) and angle < (2*math.pi-a+e):
            # get the vector joining the bottom right corner of the block and the center of the player
            dx = sprite.rect.centerx - block.rect.right
            dy = block.rect.bottom - sprite.rect.centery
            # move the player at the distance d from the corner of the block in the direction (dx, dy)
            sprite.rect.centerx = block.rect.right + d * dx / math.sqrt(dx*dx + dy*dy)
            sprite.rect.centery = block.rect.bottom - d * dy / math.sqrt(dx*dx + dy*dy)
            
    
    # return authorized directions
    directions = []
    if not left_blocked:
        directions.append("left")
    if not right_blocked:
        directions.append("right")
    if not top_blocked:
        directions.append("up")
    if not bottom_blocked:
        directions.append("down")
    
    return directions