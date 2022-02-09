from urllib.parse import MAX_CACHE_SIZE
import pygame,random
import constants as c

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
        
class Level:
    lvl_desc={
    #lvlN (enemiesN,asteroidsN) 
        1:(5,2),
        2:(7,3),
        3:(10,3),
        4:(13,4),
        5:(17,4),
        6:(20,5),
        7:(23,5),
        8:(27,6),
        9:(30,7),
        10:(33,7)
    }

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
        if self.x>c.WIDTH/2:
            self.velx=self.velx*(-0.0005*self.x)+0.3*random.randrange(-self.velx,self.velx)
        else:
            self.velx=self.velx*(0.001*self.x)+0.3*random.randrange(-self.velx,self.velx)
    
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self,):
        self.y+=self.vely
        self.x+=self.velx
    def get_height(self):
        return self.img.get_height()
    def collision(self, obj):
        return collide(self, obj)
    def off_screen(self, height):
        return not(self.y <= height)

class Ship:
    COOLDOWN = 14

    def __init__(self, x, y, health):
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
            if laser.off_screen(c.HEIGHT+100):
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

class Boss:
    COOLDOWN=15
    def __init__(self,img,x, y,health,vx):
        self.x=x
        self.y=y
        self.img=img
        self.health=health
        self.max_health=health
        self.vx=vx
        self.lasers = []
        self.mask=pygame.mask.from_surface(self.img)
   
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        self.healthbar(window)
    def move(self,vy):
        self.y += vy
        if self.x==100 or self.x==800:
            self.vx=-self.vx
        self.x+=self.vx
    def death(self, enemies,enemy):
        if self.health<=0:
            enemies.remove(enemy)
    def healthbar(self, window):
        if self.max_health!=self.health:
            pygame.draw.rect(window, (255,0,0), (self.x, self.y -20, self.img.get_width(), 10))
            pygame.draw.rect(window, (0,255,0), (self.x, self.y -20, self.img.get_width() * (self.health/self.max_health), 10))
    def collision(self, obj):
        return collide(self, obj)
    
    def move_lasers(self, vel, obj):
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(c.HEIGHT+120):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 30
                self.lasers.remove(laser)
    
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

class Bosslvl5(Boss):
    BULLET = {
                "left": (c.bbullet_left1),
                "staright": (c.bbullet_straight1),
                "right": (c.bbullet_right1),
                "loaded": (c.bbullet_loaded1)
                }
    def __init__(self, img, x, y, health, vx):
        super().__init__(img, x, y, health, vx)
        self.last = pygame.time.get_ticks()
    #choice(["1","2"])
    
    def leftRightshoot(self):
        fireCD=1
        now=pygame.time.get_ticks()
        if fireCD==1:
            for x in range(5):
                fireCD=0
                if now-self.last>=350:
                    self.last=now
                    laser = Laser(self.x+12, self.y+64, c.bbullet_left1)
                    self.lasers.append(laser)
                    if now-self.last>=350:
                        self.last=now
                        laser = Laser(self.x+76, self.y+64, c.bbullet_right1)
                        self.lasers.append(laser)
                        if now-self.last>=1000:
                            fireCD=1
                

    def shoot(self):
        laser = Laser(self.x+12, self.y+64, x)
        self.lasers.append(laser)
        laser = Laser(self.x+76, self.y+64, x)
        self.lasers.append(laser)
        laser = Laser(self.x+30, self.y+62, x)
        self.lasers.append(laser)
        laser = Laser(self.x+50, self.y+62, x)
        self.lasers.append(laser)

class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = c.SHIP1
        self.laser_img = c.bullet5
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(c.HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        obj.health-=100
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
                "1": (c.enemy1, c.bullet5),
                "2": (c.enemy2, c.bullet5),
                "3": (c.enemy3, c.bullet5),
                "4": (c.enemy4, c.bullet5),
                "5": (c.enemy5, c.bullet5),
                "6": (c.enemy6, c.bullet5),
                "7": (c.enemy7, c.bullet5),
                "8": (c.enemy8, c.bullet5)
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.ENEMY_SHIP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def death(self, enemies,enemy):
        if self.health<=0:
            enemies.remove(enemy)

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x+17, self.y+40, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 2

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None