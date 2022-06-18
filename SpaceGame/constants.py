import pygame,os

#Constants
WIDTH, HEIGHT = 1000, 1000
FPS=100
money=None #type: int
shiplvl=None    #type: int
alfa=1
level=None
pause=False
clock = pygame.time.Clock()
killedEnemy=0

#Communicates
ifunds=0
maxlvlreached=0
#Player
SHIP1=pygame.transform.scale(pygame.image.load(os.path.join("Assets\playerShips/Ship_1.png")),(48,48))
SHIP2=pygame.transform.scale(pygame.image.load(os.path.join('Assets/playerShips/Ship_2.png')),(48,48))
SHIP3=pygame.transform.scale(pygame.image.load(os.path.join('Assets/playerShips/Ship_3.png')),(48,48))
SHIP4=pygame.transform.scale(pygame.image.load(os.path.join('Assets/playerShips/Ship_4.png')),(48,48))

#Enemy
enemy1=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_1.png')),(48,48))
enemy2=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_2.png')),(48,48))
enemy3=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_3.png')),(48,48))
enemy4=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_4.png')),(48,48))
enemy5=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_5.png')),(48,48))
enemy6=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_6.png')),(48,48))
enemy7=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_7.png')),(48,48))
enemy8=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/enemy_8.png')),(48,48))
boss1IMG=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/boss_1.png')),(88,70))
boss3IMG=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/boss_3.png')),(100,104))
boss4IMG=pygame.transform.scale(pygame.image.load(os.path.join('Assets/enemies/boss_4.png')),(104,98))
#Bullet bbullet==boss bullet int==boss level
bbullet_left1=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/boss_left_1.png')),(21,30))
bbullet_right1=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/boss_right_1.png')),(21,30))
bbullet_straight1=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/boss_straight_1.png')),(15,36))
bbullet_loaded1=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/boss_loaded_1.png')),(40,32))

bullet1=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/bullet_small_1.png')),(22,22))
bullet2=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/bullet_small_2.png')),(22,22))
bullet3=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/bullet_small_3.png')),(12,12))
bullet4=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/bullet_small_4.png')),(12,12))
bullet5=pygame.transform.scale(pygame.image.load(os.path.join('Assets/bullets/bullet_small_5.png')),(12,12))
asteroid1=pygame.transform.scale(pygame.image.load(os.path.join('Assets/asteroids/asteroid_1.png')),(28,28))

#Lasers
#RED_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_red.png"))
#GREEN_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_green.png"))
#BLUE_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_blue.png"))
#YELLOW_LASER = pygame.image.load(os.path.join("test/assets", "pixel_laser_yellow.png"))

#Background
BG = pygame.transform.scale(pygame.image.load(os.path.join("Assets/bg_1.jpg")), (WIDTH, HEIGHT))
MMBG = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "bg_2.jpg")), (WIDTH, HEIGHT))
BLACK=pygame.transform.scale(pygame.image.load(os.path.join("Assets", "black.png")), (WIDTH, HEIGHT))
LOGO=pygame.image.load(os.path.join("Assets", "Skyspace_logo_white.png"))
VOLUMELOW=pygame.transform.scale(pygame.image.load(os.path.join("Assets/menu", "volume_low.png")), (100, 100))
VOLUMEHIGH=pygame.transform.scale(pygame.image.load(os.path.join("Assets/menu", "volume_high.png")), (100, 100))
VOLUMEMUTE=pygame.transform.scale(pygame.image.load(os.path.join("Assets/menu", "volume_mute.png")), (100, 100))
buttonOptionsimg=pygame.transform.scale(pygame.image.load(os.path.join('Assets/menu/options_button.png')),(300,100))
HbuttonOptionsimg=pygame.transform.scale(pygame.image.load(os.path.join('Assets/menu/options_button_h.png')),(300,100))