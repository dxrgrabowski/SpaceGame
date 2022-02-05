import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.sprites=[]
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0000'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0001'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0002'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0003'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0004'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0005'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0006'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0007'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0008'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0009'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0010'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0011'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0012'))
        self.sprites.append(pygame.image.load('C:\Users\Dexor\source\PyProjects\'SpaceGame\Assets\objectsSample\outline_light\coin_large/frame0013'))
        self.current_sprite=0
        self.image=self.sprites[self.current_sprite]
        self.rect=self.image.get_rect()
        self.rect.topleft=[x,y]

    def update(self):
        self.current_sprite+=0.2