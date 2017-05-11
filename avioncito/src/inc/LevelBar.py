# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

import Level

BAR_COLOR = (100,125,12)
BAR_CHK_POINT_COLOR = (250,250,250)
W = 75
CANT_CHK_POINT = 10

class LevelBar():    
    def __init__(self, l):
        self.level = l
        
        self.bar = pygame.sprite.DirtySprite()
        self.check = pygame.sprite.DirtySprite()

        self.make_bar()
        self.make_checkpoint()
    
    def make_bar(self):
        self.screen =  pygame.display.get_surface() 
        sc_width = self.screen.get_rect().width

        self.bar.image = pygame.Surface((sc_width, W))
        self.bar.image.fill(BAR_COLOR)      
        self.bar.rect = self.bar.image.get_rect()
        
        for i in range(0,CANT_CHK_POINT+1):
            pygame.draw.rect(self.bar.image, BAR_CHK_POINT_COLOR, 
                    pygame.rect.Rect(i*(sc_width-W)/(CANT_CHK_POINT),0, W,W))
        
        self.bar.rect.topleft = (0,0)

    def make_checkpoint(self):
        self.screen =  pygame.display.get_surface() 
        sc_width = self.screen.get_rect().width
        
        i = pygame.image.load("images/checkpoints/" +  str(self.level.checkpoint) + ".png")
        i.set_colorkey((153, 203, 238, 255), pygame.RLEACCEL)
        
        self.check.image = i.convert()
        self.check.rect = self.check.image.get_rect()
        
        self.check.rect.midleft = (((self.level.checkpoint)*(sc_width-W)/CANT_CHK_POINT) , W/2)
        
        self.check.dirty = 1
