import pygame, sys, random, time
import os
from button import Button
pygame.init()

width,height=800,1000
win=pygame.display.set_mode((width,height))
pygame.display.set_caption("Space by @Dexor")
mainFont = pygame.font.SysFont("cambria", 50)

#IMG load and transform
BG=pygame.image.load(
    os.path.join('SpaceGame\Assets', 'background_blue_1.png'))
purpleSmallPlayerIMG=pygame.image.load(
    os.path.join('SpaceGame\Assets', 'purple_small_player.png'))
purpleSmallPlayer=pygame.transform.scale(purpleSmallPlayerIMG,(48,48))
mainMenuIMG=pygame.image.load(
    os.path.join('SpaceGame\Assets', 'Skyspace_logo_white.png'))
bulletSmall_1IMG=pygame.image.load(
    os.path.join('SpaceGame\Assets', 'bullet_small_1.png'))
bulletSmall_1=pygame.transform.scale(bulletSmall_1IMG,(12,12))
yellowSmallEnemyIMG=purpleSmallPlayerIMG=pygame.image.load(
    os.path.join('SpaceGame\Assets', 'yellow_small_player.png'))
yellowSmallEnemy=pygame.transform.scale(yellowSmallEnemyIMG,(48,48))
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
    def off_screen(self, height):
        return not(self.y<=height and self.y>=0)
    def collision(self,obj):
        return collide(self,obj)    

class Ship:
    setcooldown=30
    
    def __init__(self,x,y,health=100):
        self.x=x
        self.y=y
        self.health=health
        self.shipIMG=None
        self.bulletIMG=None
        self.bullets=[]
        self.cooldownC=0
    
    def draw(self,window):
        window.blit(self.shipIMG, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(window)

    def cooldown(self):
        if self.cooldownC>=self.setcooldown:
            self.cooldownC=0
        elif self.cooldownC>0:
            self.cooldownC+=1
    
    def move_bullets(self, vel, obj):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(height):
                self.bullets.remove(bullet)
            elif bullet.collision(obj):
                obj.health -= 10
                self.bullets.remove(bullet)
    
    def shoot(self):
        if self.cooldownC==0:
            bullet=Bullet(self.x,self.y,self.bulletIMG)
            self.bullets.append(bullet)
            self.cooldownC=1
    
    def get_width(self):
        return self.shipIMG.get_width()
    def get_height(self):
        return self.shipIMG.get_height()

class Player(Ship):
    def __init__(self,x,y, health=100):
        super().__init__(x, y, health)
        self.shipIMG=purpleSmallPlayer
        self.bulletIMG=bulletSmall_1
        self.mask=pygame.mask.from_surface(self.shipIMG)
        self.max_health=health
    
    def move_bullets(self, vel, objs):
        self.cooldown()
        for bullet in self.bullets:
            bullet.move(vel)
            if bullet.off_screen(height):
                self.bullets.remove(bullet)
            else:
                for obj in objs:
                    if bullet.collision(obj):
                        objs.remove(obj)
                        if bullet in self.bullets:
                            self.bullets.remove(bullet)
    def draw(self, window):
        super().draw(window)

class Enemy(Ship):
    COLOR_MAP = {
                "red": (yellowSmallEnemy, bulletSmall_1)
                }

    def __init__(self,x,y,color,health=100):
        super().__init__(x,y,health)
        self.shipIMG,self.bulletIMG=self.COLOR_MAP[color]
        self.mask=pygame.mask.from_surface(self.shipIMG)

    def move(self,vel):
        self.y+=vel

    def shoot(self):
        if self.cooldownC == 0:
            bullet=Bullet(self.x-20, self.y, self.bulletIMG)
            self.bullets.append(bullet)
            self.cooldownC = 1


def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x, offset_y)) != None

#Game Body
def main():
    run=True
    FPS=120
    clock=pygame.time.Clock()
    pygame.mouse.set_visible(0)
    enemies=[]
    wave_length=5
    enemy_vel=1
    player_vel=5
    bullet_vel=5
    level=0
    lives=5
    lost=False
    lost_count=0
    
    def windowDraw():
        win.blit(BG,(0,0))
        player.draw(win)
        for enemy in enemies:
            enemy.draw(win)
        pygame.display.update()     
    
    while run:
        x,y=pygame.mouse.get_pos()
        player=Player(x,y)
        clock.tick(FPS)
        windowDraw()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, width-100), random.randrange(-1500, -50), random.choice(["red"]))
                enemies.append(enemy)
        
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_bullets(bullet_vel, player)     
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > height:
                enemies.remove(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        event = pygame.event.wait()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            mainMenu()
        if keys[pygame.K_SPACE]:
            player.shoot()
        
        player.move_bullets(-bullet_vel, enemies)
    
#Menu font
def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("SpaceGame/assets/font.ttf", size)

#Main Menu
def mainMenu():
    run=True
    pygame.mouse.set_visible(1)
    while run:
        win.blit(BG,(0,0))
        menuPos=pygame.mouse.get_pos()
        menuTXT=get_font(100).render("MAIN MENU", True, "#b68f40")
        menuRect=menuTXT.get_rect(center=(450,100))
        playButton = Button(image=pygame.image.load("SpaceGame/assets/Play Rect.png"), pos=(400, 320), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quitButton = Button(image=pygame.image.load("SpaceGame/assets/Quit Rect.png"), pos=(400, 480), 
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
                    main()
                if quitButton.checkForInput(menuPos):
                    run=False
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
mainMenu()

