# -*- coding: utf-8 -*-
import pygame
import ActionButton


class CloseButton(ActionButton.ActionButton):
    
    def __init__(self, action, topleft=(1150, 85)):
        super(CloseButton, self).__init__(action)
        self.image = pygame.image.load("./images/close.png").convert_alpha()
        self.action = action
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft


    
