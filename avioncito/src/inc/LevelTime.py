# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

import Level
import Properties



class LevelTime(pygame.sprite.DirtySprite):    
    def __init__(self, l):
        pygame.sprite.DirtySprite.__init__(self)
        self.level = l
        self.screen_rect =  pygame.display.get_surface().get_rect()
                 
        self.image = pygame.Surface((self.screen_rect.width, Properties.TIME_BAR_HEIGHT), pygame.SRCALPHA)
        self.image_empty = self.image.copy()
        
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (0, self.screen_rect.height)

        self.refresh()
    
    def refresh(self):
        self.image = self.image_empty.copy()
        self.dirty = 1
        
        mh = float(Properties.MAX_PLANE_GAME)
        width = int(self.screen_rect.width * (1.0-(1.0-(float(self.level.get_num_trials())/mh))))

        r = pygame.Rect((0, 0), (width, Properties.TIME_BAR_HEIGHT))
        self.image.fill(Properties.TIME_BAR_COLOR, r)