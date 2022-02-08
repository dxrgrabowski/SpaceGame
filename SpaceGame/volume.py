import pygame,os

class Volume ():
    def __init__(self,volumeIMG,pos):
        self.volumeIMG=volumeIMG
        self.x=pos[0]
        self.y=pos[1]
        self.rect = self.volumeIMG.get_rect(center=(self.x, self.y))
        
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def draw(self,screen):
        screen.blit(self.volumeIMG, self.rect)
    
    def hooverChange(self, position,hooverIMG):
	    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
		    self.volumeIMG = hooverIMG