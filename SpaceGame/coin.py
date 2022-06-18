import pygame,os,sys

class Coin(pygame.sprite.Sprite):
    def __init__(self, x,y):
        super().__init__()
        self.sprites=[]
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0000.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0001.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0002.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0003.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0004.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0005.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0006.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0007.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0008.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0009.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0010.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0011.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0012.png'))
        self.sprites.append(pygame.image.load('Assets/objectsSample/outline_light/coin_large/frame0013.png'))
        self.current_sprite=0
        self.image=self.sprites[self.current_sprite]
        self.rect=self.image.get_rect()
        self.rect.topleft=[x,y]

    def update(self):
        self.current_sprite+=0.2
        if self.current_sprite>=len(self.sprites):
            self.current_sprite=0
        self.image=self.sprites[int(self.current_sprite)]