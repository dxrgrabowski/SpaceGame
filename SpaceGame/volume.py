import pygame,os

class Volume ():
    def __init__(self,volumeIMG,pos):
        self.volumeIMG=volumeIMG
        self.x=pos[0]
        self.y=pos[1]
    
    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    '''def changeIMG(self, position):
	    if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
		    self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)'''