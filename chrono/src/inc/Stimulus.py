# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

import Properties

current_milli_time = lambda: int(round(time.time() * 1000))

class Stimulus(pygame.sprite.DirtySprite):
    def __init__(self, block_num, is_stimulus=True):
        pygame.sprite.DirtySprite.__init__(self)
        if is_stimulus:
            self.image = pygame.image.load("./imgs/" + block_num + "-stimulus.png").convert_alpha()
        else:
            self.image = pygame.image.load("./imgs/" + block_num + "-target.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.rect.center = (Properties.SCREEN_RES[0]/2, Properties.SCREEN_RES[1]/2)
        self.hide()

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True
