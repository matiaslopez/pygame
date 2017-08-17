# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties



class Goal(pygame.sprite.DirtySprite):

    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)

        self.set(0)

    def set(self, board_num):
        self.image = pygame.image.load("images/boards/%02d.png" %(board_num, ))
        self.rect = self.image.get_rect()
        self.rect.topleft = Properties.goal_pos #(Properties.SCREEN_RES[0]-30,30)
        self.dirty = 1


    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True
