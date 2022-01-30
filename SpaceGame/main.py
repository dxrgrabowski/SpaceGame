import pygame, sys
import os
from button import Button
pygame.init()

width,height=800,1000
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Space by @Dexor")
mainFont = pygame.font.SysFont("cambria", 50)
BG=pygame.image.load(
    os.path.join('SpaceGame\Assets', 'background_blue_1.png'))
FPS=120

#Objects
class Bullet:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
    def draw(self,window):
        window.blit(self.img,(self.x,self.y))
    def move(self, vel):
        self.y+=vel
        
class Ship:
    cooldown=60
    def __init__(self,x,y,health):
        self.x=x
        self.y=y
        self.health=health
        self.shipIMG=None
        self.bulletIMG=None
        self.bullets=[]
        self.cooldownC=0
    def draw(self,window):
        pygame.draw.rect(window,(255,0,0),(self.x,self.y,48,48))
    def cooldown(self):
        if self.cooldownC>=self.cooldown:
            self.cooldownC=1
        elif self.cooldownC>0:
            self.cooldownC+=1
    def shoot(self):
        if self.cooldownC==0:
            bullet=Bullet(x,y,self.bulletIMG)
            self.bullets.append(bullet)
            self.cooldownC=1
    
    def get_width(self):
        return self.shipIMG.get_width()
    def get_height(self):
        return self.shipIMG.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.shipIMG=purpleSmallPlayer
        self.mask=pygame.mask.from_surface(self.shipIMG)
        self.max_health=health

purpleSmallPlayerIMG=pygame.image.load(
    os.path.join('SpaceGame\Assets', 'purple_small_player.png'))
purpleSmallPlayer=pygame.transform.scale(purpleSmallPlayerIMG,(48,48))


#Window draw
def windowDraw():
    player=Player(400,500,100)
    while True:
        pygame.mouse.set_visible(0)
        win.fill("#1c1e1f")
        player.draw(win)
        win.blit(purpleSmallPlayer,(pygame.mouse.get_pos()))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainMenu()
        pygame.display.update() 
    
#Menu
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("SpaceGame/assets/font.ttf", size)
def mainMenu():
    clock=pygame.time.Clock()
    run=True
    while run:
        clock.tick(FPS)
        win.blit(BG,(0,0))
        pygame.mouse.set_visible(1)
        menuPos=pygame.mouse.get_pos()
        mainMenuIMG=pygame.image.load(
        os.path.join('SpaceGame\Assets', 'Skyspace_logo_white.png'))
        menuTXT=get_font(100).render("MAIN MENU", True, "#b68f40")
        menuRect=menuTXT.get_rect(center=(640,100))
        playButton = Button(image=pygame.image.load("SpaceGame/assets/Play Rect.png"), pos=(640, 320), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quitButton = Button(image=pygame.image.load("SpaceGame/assets/Quit Rect.png"), pos=(640, 480), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        win.blit(menuTXT,menuRect)

        for button in [playButton,quitButton]:
            button.changeColor(menuPos)
            button.update(win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(menuPos):
                    windowDraw()
                if quitButton.checkForInput(menuPos):
                    run=False
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
mainMenu()

