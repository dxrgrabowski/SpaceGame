import pygame, sys, random, time
import os
from button import Button
from volume import Volume
pygame.init()
pygame.font.init()

#TO DO
'''
X-Dodanie muzyki w menu 
X-Efekty po kliknieciu przycisku w menu
X-Przycisk wylaczania muzyki
X-Wysrodkowanie strzalu 
X-Asteroidy ktore nadlatuja z bokow
-Level design
-Plik konfiguracyjny opcji
-Plik z zapisem
-Dodanie Bossow
-Boostery,HP
-Mozliwosc wyboru statku gracza
-Zmiana Play, Quit, dodanie Resume
-Healthbar z boku ekranu
'''

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SkySpace by @Dexor")

#Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("test/assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("test/assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("test/assets", "pixel_ship_blue_small.png"))

#Player
YELLOW_SPACE_SHIP=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\playerShips', 'player_3.png')),(48,48))

#Enemy
enemy1=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_1.png')),(48,48))
enemy2=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_2.png')),(48,48))
enemy3=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_3.png')),(48,48))
enemy4=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_4.png')),(48,48))
enemy5=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_5.png')),(48,48))
enemy6=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_6.png')),(48,48))
enemy7=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_7.png')),(48,48))
enemy8=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\enemies', 'enemy_8.png')),(48,48))
#Bullet
bullet1=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_1.png')),(22,22))
bullet2=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_2.png')),(22,22))
bullet3=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_3.png')),(12,12))
bullet4=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_4.png')),(12,12))
bullet5=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_5.png')),(12,12))
asteroid1=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets/asteroids/asteroid_1.png')),(28,28))

#Lasers
RED_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_yellow.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("SpaceGame\Assets/bg_2.jpg")), (WIDTH, HEIGHT))
MMBG = pygame.transform.scale(pygame.image.load(os.path.join("SpaceGame\Assets", "bg_2.jpg")), (WIDTH, HEIGHT))
LOGO=pygame.image.load(os.path.join("SpaceGame\Assets", "Skyspace_logo_white.png"))
VOLUMELOW=pygame.transform.scale(pygame.image.load(os.path.join("SpaceGame\Assets/menu", "volume_low.png")), (100, 100))
VOLUMEHIGH=pygame.transform.scale(pygame.image.load(os.path.join("SpaceGame\Assets/menu", "volume_high.png")), (100, 100))
VOLUMEMUTE=pygame.transform.scale(pygame.image.load(os.path.join("SpaceGame\Assets/menu", "volume_mute.png")), (100, 100))

class Booster:
    def __init__(self,x,y,img,vel):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel
        
class Laser: 
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)

class Asteroid:
    def __init__(self,x,y,img):
        self.x=x
        self.y=y
        self.velx=5
        self.vely=5
        self.img=img
        self.mask=pygame.mask.from_surface(self.img)
        if self.x>WIDTH/2:
            self.velx=self.velx*(-0.0005*self.x)+0.3*random.randrange(-self.velx,self.velx)
        else:
            self.velx=self.velx*(0.001*self.x)+0.3*random.randrange(-self.velx,self.velx)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self,):
        self.y+=self.vely
        self.x+=self.velx
    
    def collision(self, obj):
        return collide(self, obj)
    def off_screen(self, height):
        return not(self.y <= height)

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT+100):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = bullet5
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+18, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        x,y=pygame.mouse.get_pos()
        self.x=x
        self.y=y
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    ENEMY_SHIP = {
                "1": (enemy1, bullet5),
                "2": (enemy2, bullet5),
                "3": (enemy3, bullet5),
                "4": (enemy4, bullet5),
                "5": (enemy5, bullet5),
                "6": (enemy6, bullet5),
                "7": (enemy7, bullet5),
                "8": (enemy8, bullet5)
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.ENEMY_SHIP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+17, self.y+40, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 2


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5
    main_font = get_font(45)
    lost_font = get_font(60)

    asteroidClock=0
    asteroids=[]
    enemies = []
    wave_length = 5
    enemy_vel = 1

    laser_vel = 5

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    x,y=pygame.mouse.get_pos()
    player=Player(x,y)
    pygame.mouse.set_visible(0)
    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        for asteroid in asteroids:
            asteroid.draw(WIN)
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            if lost_count > FPS * 3:
                run = False
                #Tutaj bedzie plansza z podsumowaniem
            else:
                continue
    
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-100, -10), random.choice(["1", "2", "3", "4", "5", "6", "7", "8"]))
                enemies.append(enemy)
        
        
        
        if asteroidClock==0:
            asteroid=Asteroid(random.randrange(-20,WIDTH+50),-30,asteroid1)
            asteroids.append(asteroid)
            asteroidClock=1

            

        for asteroid in asteroids:
            
            asteroid.move()
            
            if asteroid.collision(player):
                player.health -= 40
                asteroids.remove(asteroid)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            main_menu()
        if keys[pygame.K_UP]:
            asteroidClock-=1
        
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)




def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("SpaceGame/assets/font.ttf", size)

def main_menu():
    run = True
    volume_var=1
    pygame.mouse.set_visible(1)
    pygame.mixer.music.load('SpaceGame\Assets\music\menu.wav')
    pygame.mixer.music.play(-1)
    

    while run:
        WIN.blit(MMBG, (0,0))
        menuPos=pygame.mouse.get_pos()
        WIN.blit(LOGO, (WIDTH/2 - LOGO.get_width()/2, 50))
        
        match volume_var:
            case 1:
                pygame.mixer.music.set_volume(1.0)
                WIN.blit(VOLUMEHIGH,(WIDTH-150,HEIGHT-150))
            case 2:
                pygame.mixer.music.set_volume(0.5)
                WIN.blit(VOLUMELOW,(WIDTH-150,HEIGHT-150))
            case 0:
                pygame.mixer.music.set_volume(0.0)
                WIN.blit(VOLUMEMUTE,(WIDTH-150,HEIGHT-150))
          
        playButton=Button(None, pos=(WIDTH/2, 320), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Blue")
        quitButton=Button(None, pos=(WIDTH/2, 420), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Blue")     
        optionsButton=Volume(pygame.transform.scale(pygame.image.load('SpaceGame\Assets\menu\options_button.png'),(300,100)),pos=(WIDTH/2,520))
        volumeButton=Volume(VOLUMEHIGH,pos=(WIDTH-100,HEIGHT-100))

        for volume in [optionsButton]:
            volume.draw(WIN)
        for button in [playButton,quitButton]:
            button.changeColor(menuPos)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound('SpaceGame\Assets\music\click_sound_2.mp3').play().set_volume(0.2)
                if playButton.checkForInput(menuPos):
                    pygame.mixer.music.fadeout(240)
                    main()
                if quitButton.checkForInput(menuPos):
                    pygame.quit()
                    sys.exit()
                if volumeButton.checkForInput(menuPos):
                    if volume_var==1:
                        volume_var=2
                    elif volume_var==2:
                        volume_var=0  
                    elif volume_var==0:
                        volume_var=1
                if optionsButton.checkForInput(menuPos):
                    options_menu()            
        pygame.display.update()
    pygame.quit()
main_menu()
