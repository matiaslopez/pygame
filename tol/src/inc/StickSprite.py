# -*- coding: utf-8 -*-
import pygame
import Properties as Properties

class StickSprite(pygame.sprite.DirtySprite):

    def __init__(self, stick, prop=None):
        super(StickSprite, self).__init__()

        self.stick = stick
        num = self.stick.num -1

        self.image = pygame.Surface(prop.stick_rect[num].size)
        self.image.fill(prop.stick_color)
        self.rect = pygame.Rect(prop.stick_rect[num])

        self.rect.midbottom = prop.stick_pos[num]

