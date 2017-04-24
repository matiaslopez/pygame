# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties

class ImageMessage(pygame.sprite.DirtySprite):


    def __init__(self, block_num, name):
        pygame.sprite.DirtySprite.__init__(self)
        self.block_num = block_num
        self.name = name

        self.set()

    def set(self):
        self.image = pygame.image.load("./imgs/" + self.block_num + "-" + self.name).convert_alpha()
        self.image = pygame.transform.scale(self.image,(Properties.SCREEN_RES[0],Properties.SCREEN_RES[1]))
        self.rect = self.image.get_rect()

        self.hide()

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True
