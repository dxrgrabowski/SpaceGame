import pygame,os

class Volume ():
    def __init__(self,volumeIMG,volumeBG,pos,hovering_color):
        self.volumeIMG=volumeIMG
        self.x=pos[0]
        self.y=pos[1]
        self.volumeBG=volumeBG
        self.hovering_color=hovering_color
    
    def change_color (self,imgcolor):
        self.w,self.h=self.volumeIMG.get_size()
        for x in range(self.w):
            for y in range(self.h):
                 a = self.volumeIMG.get_at((x, y))[3]
                 self.volumeIMG.set_at((x, y), pygame.Color(imgcolor))
  
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
		    self.text = self.font.render(self.text_input, True, self.hovering_color)
	    else:
		    self.text = self.font.render(self.text_input, True, self.base_color)
