import pygame, sys, random, time
import os
from button import Button
pygame.font.init()

#TO DO
'''
-Dodanie muzyki w menu
-Efekty po kliknieciu przycisku w menu
-Healthbar z boku ekranu
-Boostery,HP
-Wysrodkowanie strzalu 
-Asteroidy ktore nadlatuja z bokow,moga niszczyc enemy
-Dodanie Bossow
-Przycisk wylaczania muzyki
-Mozliwosc wyboru statku gracza

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
bullet1=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_1.png'))
bullet2=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_2.png'))
bullet3=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_3.png'))
bullet4=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_4.png'))
bullet5=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_5.png'))
bullet6=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_1.png'))
bullet7=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_2.png'))
bullet8=pygame.image.load(os.path.join('SpaceGame\Assets/bullets', 'bullet_small_3.png'))


#Lasers
RED_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_yellow.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("test/assets", "background-black.png")), (WIDTH, HEIGHT))
MMBG = pygame.transform.scale(pygame.image.load(os.path.join("SpaceGame\Assets", "background_blue_1.png")), (WIDTH, HEIGHT))
LOGO=pygame.image.load(os.path.join("SpaceGame\Assets", "Skyspace_logo_white.png"))
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
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
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
                "1": (enemy1, bullet1),
                "2": (enemy2, bullet2),
                "3": (enemy3, bullet3),
                "4": (enemy4, bullet4),
                "5": (enemy5, bullet5),
                "6": (enemy6, bullet6),
                "7": (enemy7, bullet7),
                "8": (enemy8, bullet8)
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.ENEMY_SHIP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def main():
    run = True
    FPS = 120
    level = 0
    lives = 5
    main_font = get_font(45)
    lost_font = get_font(60)

    enemies = []
    wave_length = 5
    enemy_vel = 1

    player_vel = 5
    laser_vel = 5

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0
    x,y=pygame.mouse.get_pos()
    player=Player(x,y)

    def redraw_window():
        WIN.blit(BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

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
            else:
                continue
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -50), random.choice(["1", "2", "3", "4", "5", "6", "7", "8"]))
                enemies.append(enemy)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

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
    while run:
        WIN.blit(MMBG, (0,0))
        menuPos=pygame.mouse.get_pos()
        WIN.blit(LOGO, (WIDTH/2 - LOGO.get_width()/2, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
        playButton = Button(image=pygame.image.load("SpaceGame/assets/Play Rect.png"), pos=(WIDTH/2, 320), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Blue")
        quitButton = Button(image=pygame.image.load("SpaceGame/assets/Quit Rect.png"), pos=(WIDTH/2, 480), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Blue")
        for button in [playButton,quitButton]:
            button.changeColor(menuPos)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(menuPos):
                    main()
                if quitButton.checkForInput(menuPos): 
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
    pygame.quit()
main_menu()