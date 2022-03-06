import pygame, sys, random, ptext, os
from button import Button
from volume import Volume
from objects import *
import constants as c
from coin import Coin
pygame.init()
pygame.font.init()
#TO DO
'''
-Więcej dźwięków
-winietowanie
-Level design
-Plik konfiguracyjny opcji
-Boostery,HP
-Healthbar z boku ekranu
'''

WIN = pygame.display.set_mode((c.WIDTH, c.HEIGHT))
pygame.display.set_caption("SkySpace by @Dexor")

asteroidSpawn=pygame.USEREVENT
pygame.time.set_timer(asteroidSpawn,c.FPS*30)
xChange=pygame.USEREVENT
pygame.time.set_timer(xChange,1500)

if os.path.exists("SpaceGame/save.txt")==False:
    makeSaveFile()
loadFromFile()

def main():
    pygame.mouse.set_visible(0)
    run = True
    lives = 5
    main_font = get_font(45)
    lost_font = get_font(60)
    asteroids=[]
    enemies = []
    bosses=[]
    enemy_number=Level.lvl_desc[1]
    enemy_vel = 1

    laser_vel = 5

    lost = False
    lost_count = 0
    x,y=pygame.mouse.get_pos()
    player=Player(x,y)
    match c.shiplvl:
        case 1:
            player.health=100
        case 2:
            player.health=200
        case 3:
            player.health=400
        case 4:
            player.health=800
    
    def redraw_window():
        WIN.blit(c.BG, (0,0))
        # draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {c.level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (c.WIDTH - level_label.get_width() - 10, 10))
        for boss in bosses:
            boss.draw(WIN)
        for enemy in enemies:
            enemy.draw(WIN)
        for asteroid in asteroids:
            asteroid.draw(WIN)
        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (c.WIDTH/2 - lost_label.get_width()/2, 350))
            pygame.time.delay(3000)

        pygame.display.update()

    while run:
        c.clock.tick(c.FPS)
        redraw_window()
        
        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
        if lost:
            c.money+=c.killedEnemy
            run=False
            summary(c.killedEnemy)
#resp enemy
        
        if len(enemies) == 0 and len(bosses)==0:
            c.level += 1
            if c.level==2 and len(bosses)==0:
                boss=Bosslvl5(c.boss1IMG,c.WIDTH/2-c.boss1IMG.get_width()/2,-75,1800,2)
                bosses.append(boss)
            enemy_number=Level.lvl_desc[c.level]
            if len(bosses)==0:
                for i in range(enemy_number):
                    enemy = Enemy(random.randrange(50, c.WIDTH-100), random.randrange(-100, -10), random.choice(["1", "2", "3", "4", "5", "6", "7", "8"]))
                    enemies.append(enemy)    
#Events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused()
                if event.key == pygame.K_UP:
                    boss.topleft()
                              
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==asteroidSpawn:
                asteroid=Asteroid(random.randrange(-20,c.WIDTH+50),-30,c.asteroid1)
                asteroids.append(asteroid)
            if event.type==xChange:
                if len(bosses)!=0:
                    if random.randint(0,1)==1:
                        boss.vx = -boss.vx
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                player.shoot()
            
#Collision and move       
        for boss in bosses[:]:
            boss.death(bosses,boss)
            boss.move(0.2)
            boss.move_lasers(laser_vel,player)
            if boss.collision(player):
                player.health -= 100
        for asteroid in asteroids[:]:
            asteroid.move()
            if asteroid.collision(player):
                player.health -= 40
                asteroids.remove(asteroid)
            if asteroid.y + asteroid.get_height() > c.HEIGHT:
                asteroids.remove(asteroid)
        for enemy in enemies[:]:
            enemy.death(enemies,enemy)
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
        player.move_lasers(-laser_vel, bosses)

def paused():
    c.pause=True
    
    for opacity in range(0, 15, 1):
     work_img = c.BLACK.copy()
     pygame.draw.rect(work_img, (0,0, 0, opacity),  (0,0, c.WIDTH,c.HEIGHT))
     WIN.blit(work_img, (0,0))
     ptext.draw('GAME PAUSED\nPRESS ESC TO RESUME', centery=c.HEIGHT/3,centerx=c.WIDTH/2, color="#bfbfbf",gcolor="#292a40", fontsize=75, alpha=0.8)
     pygame.display.update()

    while c.pause:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    c.pause=False
            if event.type == pygame.QUIT:
                pygame.quit()
                quit() 
        c.clock.tick(15)  
    pygame.display.update()

############################################## MAIN MENU/UI FUNCTIONS #################################################


def options_menu():
    run = True
    volume_var=1
    pygame.mouse.set_visible(1)
    pygame.mixer.music.load('SpaceGame\Assets\music\menu.wav')
    pygame.mixer.music.play(-1)
    
    while run:
        WIN.blit(c.BG, (0,0))
        menuPos=pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False

        pygame.display.update()  
    pygame.quit() 

def levelchoose():
    run=True

    while run:
        WIN.blit(c.MMBG, (0,0))
        menuPos=pygame.mouse.get_pos()
        ptext.draw('Select the level you want to jump to\n (The higher the level, the more enemies):', (130,60), color=(255,255,255),gcolor="purple", fontsize=60, alpha=1)

        easyShowcase=pygame.transform.scale2x(c.boss1IMG)
        mediumShowcase=pygame.transform.scale2x(c.boss3IMG)
        hardShowcase=pygame.transform.scale2x(c.boss4IMG) 

        easyButton=Button(None, pos=(c.WIDTH-860, 720), 
                            text_input="EASY", font=get_font(55), base_color="White", hovering_color="green")
        mediumButton=Button(None, pos=(c.WIDTH/2, 720), 
                            text_input="MEDIUM", font=get_font(55), base_color="White", hovering_color="blue")
        hardButton=Button(None, pos=(c.WIDTH-140, 720), 
                            text_input="HARD", font=get_font(55), base_color="White", hovering_color="Red")
        ptext.draw('You start at level 1', (c.WIDTH-985, 780), color=(255,255,255),gcolor="purple", fontsize=45, alpha=0.8)
        ptext.draw('You start at level 10', (c.WIDTH/2-150, 780), color=(255,255,255),gcolor="purple", fontsize=45, alpha=0.8)
        ptext.draw('You start at level 20', (c.WIDTH-140-150, 780), color=(255,255,255),gcolor="purple", fontsize=45, alpha=0.8)
        #Boss ships
        WIN.blit(easyShowcase, (c.WIDTH-860-c.boss1IMG.get_width(), 410))
        WIN.blit(mediumShowcase, (c.WIDTH/2-c.boss3IMG.get_width(), 380)) 
        WIN.blit(hardShowcase, (c.WIDTH-140-c.boss4IMG.get_width()-10, 380)) 

        for button in [easyButton,mediumButton,hardButton]:
            button.changeColor(menuPos)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easyButton.checkForInput(menuPos):
                    c.level=0
                    pygame.mixer.music.fadeout(240)
                    main()
                if mediumButton.checkForInput(menuPos):
                    c.level=9
                    pygame.mixer.music.fadeout(240)
                    main()
                if hardButton.checkForInput(menuPos):
                    c.level=19
                    pygame.mixer.music.fadeout(240)
                    main()

        pygame.display.update()  
    pygame.quit() 

def summary(level):
    run=True
    c.killedEnemy=0
    saveToFile()    
    
    #Music/sounds
    pygame.mouse.set_visible(1)
    pygame.mixer.music.load('SpaceGame\Assets\music\menu.wav')
    pygame.mixer.music.play(-1)
    
    #Graphics declaration
    plus=get_font(50).render("+", 1, (255,255,255))
    equal=get_font(50).render("=", 1, (255,255,255))
    bbalancev = get_font(60).render(str(c.money-level), 1, "#383733")
    earningsv = get_font(60).render(str(level), 1, "#2f8022")
    currentbalancev= get_font(60).render(str(c.money), 1, "#bfb152")
    bbalance = get_font(22).render("balance before: ", 1, "#383733")
    earnings = get_font(22).render("earnings: ", 1, "#2f8022")
    currentbalance= get_font(22).render("current balance: ", 1, "#bfb152")
    playButton=Button(None, pos=(c.WIDTH/2-200,650), 
                        text_input="PLAY AGAIN", font=get_font(50), base_color="White", hovering_color="Blue")
    returnButton=Button(None, pos=(c.WIDTH/2+300,650), 
                        text_input="RETURN", font=get_font(50), base_color="White", hovering_color="Blue")
    
    #vignetting
    for opacity in range(255, 30, -2):
     menuPos=pygame.mouse.get_pos()
     WIN.blit(c.BG,(0,0))
     work_img = c.BLACK.copy()
     pygame.draw.rect(work_img, (0,0, 0, opacity),  (0,0, c.WIDTH,c.HEIGHT))
     ptext.draw('YOU\'RE DEAD', centery=c.HEIGHT/8,centerx=c.WIDTH/2, color="#c40000",gcolor="#0a0000", fontsize=80, alpha=0.8)
     for button in [returnButton,playButton]:
            button.update(WIN)
     WIN.blit(work_img, (0,0))
     WIN.blit(bbalancev, (c.WIDTH/2 - bbalancev.get_width()/2-300, 320))
     WIN.blit(earningsv, (c.WIDTH/2 - earningsv.get_width()/2, 320))
     WIN.blit(currentbalancev, (c.WIDTH/2 - currentbalancev.get_width()/2+300, 320))
     WIN.blit(plus, (c.WIDTH/2 - plus.get_width()/2-150, 320))
     WIN.blit(equal, (c.WIDTH/2 - equal.get_width()/2+150, 320))
     WIN.blit(bbalance, (c.WIDTH/2 - bbalance.get_width()/2-300, 250))
     WIN.blit(earnings, (c.WIDTH/2 - earnings.get_width()/2, 250))
     WIN.blit(currentbalance, (c.WIDTH/2 - currentbalance.get_width()/2+300, 250))
     pygame.display.update()



    while run:
        menuPos=pygame.mouse.get_pos()
        for button in [returnButton,playButton]:
            button.changeColor(menuPos)
            button.update(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.Sound('SpaceGame\Assets\music\click_sound_2.mp3').play().set_volume(0.1)
                if returnButton.checkForInput(menuPos):
                    main_menu()
                if playButton.checkForInput(menuPos):
                    pygame.mixer.music.fadeout(240)
                    levelchoose()
        pygame.display.update()

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("SpaceGame/assets/font.ttf", size)
def main_menu():
    run = True
    volume_var=1
    pygame.mouse.set_visible(1)
    pygame.mixer.music.load('SpaceGame\Assets\music\menu.wav')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    
    moving_sprites = pygame.sprite.Group()
    balancecoin = Coin(c.WIDTH/2+295, 275)
    upgradecoin=Coin(c.WIDTH/2+395, 745)
    moving_sprites.add(balancecoin,upgradecoin)
    
    while run:
        WIN.blit(c.MMBG, (0,0))
        menuPos=pygame.mouse.get_pos()
        WIN.blit(c.LOGO, (c.WIDTH/2 - c.LOGO.get_width()/2, 25))
        
        moving_sprites.draw(WIN)
        moving_sprites.update()

        match volume_var:
            case 1:
                pygame.mixer.music.set_volume(0.5)
                WIN.blit(c.VOLUMEHIGH,(c.WIDTH-150,c.HEIGHT-150))
            case 2:
                pygame.mixer.music.set_volume(0.15)
                WIN.blit(c.VOLUMELOW,(c.WIDTH-150,c.HEIGHT-150))
            case 0:
                pygame.mixer.music.set_volume(0.0)
                WIN.blit(c.VOLUMEMUTE,(c.WIDTH-150,c.HEIGHT-150))
          
        playButton=Button(None, pos=(190, 320), 
                            text_input="PLAY", font=get_font(75), base_color="White", hovering_color="Blue")
        optionsButton=Button(None, pos=(190, 420), 
                            text_input="OPTI", font=get_font(75), base_color="White", hovering_color="Blue")     
        quitButton=Button(None, pos=(190, 520), 
                            text_input="QUIT", font=get_font(75), base_color="White", hovering_color="Blue")     
        upgrade=Button(None, pos=(c.WIDTH/2+200, 700), 
                            text_input="UPGRADE", font=get_font(60), base_color="White", hovering_color="Red")
        shiplvl= get_font(25).render("ship level:"+ str(c.shiplvl), 1, "#edda5a")
        currentbalance= get_font(25).render("balance:"+str(c.money), 1, "#edda5a")

        WIN.blit(currentbalance, (c.WIDTH/2+20, 280))
        WIN.blit(shiplvl, (c.WIDTH/2+20, 320))
        volumeButton=Volume(c.VOLUMEHIGH,pos=(c.WIDTH-100,c.HEIGHT-100))
        
        match c.shiplvl:
            case 1:
              shipShowcase=pygame.transform.scale(c.SHIP1,(240,240)) #SKALA DO POPRAWY
              upgradecost= get_font(25).render("money needed:"+str(100), 1, "#edda5a") 
            case 2:
              shipShowcase=pygame.transform.scale(c.SHIP2,(240,240)) 
              upgradecost= get_font(25).render("money needed:"+str(150), 1, "#edda5a")             
            case 3:
              shipShowcase=pygame.transform.scale(c.SHIP3,(240,240)) 
              upgradecost= get_font(25).render("money needed:"+str(250), 1, "#edda5a")
            case 4:
              shipShowcase=pygame.transform.scale(c.SHIP4,(240,240)) 
              upgradecost= get_font(25).render("money needed:"+str(400), 1, "#edda5a")
        
        WIN.blit(upgradecost, (c.WIDTH/2-10, 750))      
        WIN.blit(shipShowcase, (c.WIDTH/2+80, 400)) 
        #for volume in [optionsButton]:
        #    volume.hooverChange(menuPos,c.HbuttonOptionsimg)
        #    volume.draw(WIN)
        for button in [playButton,quitButton,optionsButton,upgrade]:
            button.changeColor(menuPos)
            button.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if playButton.checkForInput(menuPos):
                    pygame.mixer.Sound('SpaceGame\Assets\music\click_sound_2.mp3').play().set_volume(0.1)
                    levelchoose()
                if quitButton.checkForInput(menuPos):
                    pygame.mixer.Sound('SpaceGame\Assets\music\click_sound_2.mp3').play().set_volume(0.1)
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
                    pygame.mixer.Sound('SpaceGame\Assets\music\click_sound_2.mp3').play().set_volume(0.1)
                    options_menu()  
                if upgrade.checkForInput(menuPos):
                    if int(c.money)>=100 and c.shiplvl==1:
                        pygame.mixer.Sound('SpaceGame\Assets\music\click_sound_2.mp3').play().set_volume(0.1)
                        c.shiplvl=2
                        c.money-=100
                        saveToFile()
                    elif c.money>=150 and c.shiplvl==2:
                        c.shiplvl=3
                        c.money-=150
                        saveToFile()
                    elif c.money>=250 and c.shiplvl==3:
                        c.shiplvl=4
                        c.money-=250
                        saveToFile()
                    else:
                        if int(c.money)<100 and c.shiplvl==1:
                            c.ifunds=True
                        elif c.money<150 and c.shiplvl==2:
                            c.ifunds=True
                        elif c.money<250 and c.shiplvl==3:
                            c.ifunds=True
                        else:
                            c.maxlvlreached=True     

        if c.maxlvlreached:
            c.alfa=c.alfa-0.01
            ptext.draw('You reached the maximum level!', (c.WIDTH/2-12,788), color=(255,255,255), fontsize=40, alpha=c.alfa)            
            if c.alfa<=0:
                c.maxlvlreached=False
                c.alfa=1
        if c.ifunds:
            c.alfa=c.alfa-0.01
            ptext.draw('Inufficient funds!', (c.WIDTH/2-12,788), color=(255,255,255), fontsize=50, alpha=c.alfa)             
            if c.alfa<=0:
                c.ifunds=False
                c.alfa=1
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
X-pauza
X-Plik z zapisem
X-Dodanie Bossow
X-Statek gracza z postepem
X-Mozliwosc wyboru statku gracza
X-Zmiana Play, Quit, dodanie Resume
X-uporządkowanie constants.py
'''