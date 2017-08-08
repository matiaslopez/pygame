# -*- coding: utf-8 -*-
import pygame
import Properties as Properties

class StickSprite(pygame.sprite.DirtySprite):    
    
    def __init__(self, stick):
        super(StickSprite, self).__init__()
        
        self.stick = stick
        num = self.stick.num -1
        
        self.image = pygame.Surface(Properties.stick_rect[num].size)
        self.image.fill(Properties.stick_color)      
        self.rect = pygame.Rect(Properties.stick_rect[num])
          
        self.rect.midbottom = Properties.stick_pos[num]

