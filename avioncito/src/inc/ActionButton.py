# -*- coding: utf-8 -*-

import pygame
import Properties as prop
  
class ActionButton(pygame.sprite.DirtySprite):
    
    def __init__(self, action):
        super(ActionButton, self).__init__()
        self.rect = pygame.Rect(-5, -5, 1, 1) 
        self.visible = True
        self.action = action
        
    def hide(self):
        self.visible = False
    
    def show(self):
        self.visible = True
        
    def clicked(self, pos_mouse):
        if self.visible and self.rect.collidepoint(pos_mouse):
            self.do_click()

    def do_click(self):
        self.action()
