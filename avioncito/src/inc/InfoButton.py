# -*- coding: utf-8 -*-
import pygame
import ActionButton
 

class InfoButton(ActionButton.ActionButton):
    
    def __init__(self, action, topleft=(1100, 85)):
        super(InfoButton, self).__init__(action)
        self.image = pygame.image.load("./images/info.png").convert_alpha()
        self.action = action
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft


    
