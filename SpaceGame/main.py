import pygame, sys, random, time
import os
from button import Button
from volume import Volume
from objects import Level,Booster,Laser,Asteroid,Player,Enemy,collide
import constants as c
pygame.init()
pygame.font.init()

#TO DO
'''
-Level design
-Plik konfiguracyjny opcji
-Plik z zapisem
-Dodanie Bossow
-Statek gracza z postepem
-Boostery,HP
-Mozliwosc wyboru statku gracza
-Zmiana Play, Quit, dodanie Resume
-Healthbar z boku ekranu
'''

WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("SkySpace by @Dexor")

#Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("test/assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("test/assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("test/assets", "pixel_ship_blue_small.png"))

#Player
YELLOW_SPACE_SHIP=pygame.transform.scale(pygame.image.load(os.path.join('SpaceGame\Assets\playerShips', 'player_3.png')),(48,48))

asteroidSpawn=pygame.USEREVENT+1
pygame.time.set_timer(asteroidSpawn,5)
enemySpawn=pygame.USEREVENT+1
pygame.time.set_timer(enemySpawn,5)

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
        WIN.blit(c.BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (c.WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)
        for asteroid in asteroids:
            asteroid.draw(WIN)
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (c.WIDTH/2 - lost_label.get_width()/2, 350))

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
#resp enemy
        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, c.WIDTH-100), random.randrange(-1000, -10), random.choice(["1", "2", "3", "4", "5", "6", "7", "8"]))
                enemies.append(enemy)
        
        if asteroidClock==0:
            asteroid=Asteroid(random.randrange(-20,c.WIDTH+50),-30,c.asteroid1)
            asteroids.append(asteroid)
            asteroidClock=1

#Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

#Key binding
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_ESCAPE]:
            main_menu()
        if keys[pygame.K_UP]:
            asteroidClock-=1
#Collision        
        for asteroid in asteroids:
            asteroid.move()
            if asteroid.collision(player):
                player.health -= 40
                asteroids.remove(asteroid)
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > c.HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

######################################################################################################################

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("SpaceGame/assets/font.ttf", size)
def main_menu():
    run = True
    volume_var=1
    pygame.mouse.set_visible(1)
    pygame.mixer.music.load('SpaceGame\Assets\music\menu.wav')
    pygame.mixer.music.play(-1)
    

    while run:
        WIN.blit(c.MMBG, (0,0))
        menuPos=pygame.mouse.get_pos()
        WIN.blit(c.LOGO, (c.WIDTH/2 - c.LOGO.get_width()/2, 50))
        
        match volume_var:
            case 1:
                pygame.mixer.music.set_volume(1.0)
                WIN.blit(c.VOLUMEHIGH,(c.WIDTH-150,c.HEIGHT-150))
            case 2:
                pygame.mixer.music.set_volume(0.5)
                WIN.blit(c.VOLUMELOW,(c.WIDTH-150,c.HEIGHT-150))
            case 0:
                pygame.mixer.music.set_volume(0.0)
                WIN.blit(c.VOLUMEMUTE,(c.WIDTH-150,c.HEIGHT-150))
          
        playButton=Button(None, pos=(c.WIDTH/2, 320), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="Blue")
        quitButton=Button(None, pos=(c.WIDTH/2, 420), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="Blue")     
        optionsButton=Volume(pygame.transform.scale(pygame.image.load('SpaceGame\Assets\menu\options_button.png'),(300,100)),pos=(c.WIDTH/2,520))
        volumeButton=Volume(c.VOLUMEHIGH,pos=(c.WIDTH-100,c.HEIGHT-100))

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

#DONE
'''
X-Dodanie muzyki w menu 
X-Efekty po kliknieciu przycisku w menu
X-Przycisk wylaczania muzyki
X-Wysrodkowanie strzalu 
X-Asteroidy ktore nadlatuja z bokow
'''