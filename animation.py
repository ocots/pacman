import pygame

class Animation(object):
    
    def __init__(self, img, width, height):
        self.sprite_sheet = img
        self.images_list = []
        self.load_images(width, height)
        self.index = 0
        self.clock = 1
        
    def load_images(self, width, height):
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                img = self.get_image(x, y, width, height)
                self.images_list.append(img)
                
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        BLACK = (0, 0, 0)
        image.set_colorkey(BLACK)
        return image
    
    def get_current_image(self):
        return self.images_list[self.index]
    
    def get_length(self):
        return len(self.images_list)
    
    def update(self, fps=30):
        step = 30 // fps
        l = range(1, 30, step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1
        if self.clock in l:
            self.index += 1
            if self.index == len(self.images_list):
                self.index = 0
                