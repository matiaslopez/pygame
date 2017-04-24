# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import math
import numpy
import time

import Properties

current_milli_time = lambda: int(round(time.time() * 1000))

SLOW, OK, QUICK, REFERENCE = [ p for p in range(0,4) ]

class Feedback():

    def __init__(self, block_num):
        self.reference = FeedbackTarget(block_num, REFERENCE)
        self.slow = FeedbackTarget(block_num, SLOW)
        self.ok = FeedbackTarget(block_num, OK)
        self.quick = FeedbackTarget(block_num, QUICK)

    def hide(self):
        self.reference.hide()
        self.slow.hide()
        self.ok.hide()
        self.quick.hide()

    def set(self, percent): #percent between 0 and 2
        self.reference.show()
        if percent is None:
            percent = 2;
        if percent < (1 - Properties.DELTA_OK):
            self.quick.show(percent)
        elif percent > (1 + Properties.DELTA_OK):
            self.slow.show(percent)
        else:
            self.ok.show(percent)


class FeedbackTarget(pygame.sprite.DirtySprite):

    def __init__(self, block_num, is_stimulus=OK):
        pygame.sprite.DirtySprite.__init__(self)
        if is_stimulus == OK:
            self.image = pygame.image.load("./imgs/" + block_num + "-feedback_ok.png").convert_alpha()
        elif is_stimulus == SLOW:
            self.image = pygame.image.load("./imgs/" + block_num + "-feedback_slow.png").convert_alpha()
        elif is_stimulus == QUICK:
            self.image = pygame.image.load("./imgs/" + block_num + "-feedback_quick.png").convert_alpha()
        else:
            self.image = pygame.image.load("./imgs/" + block_num + "-feedback_reference.png").convert_alpha()

        if is_stimulus != REFERENCE:
            w,h = self.image.get_size()
            scale = 0.4
            self.image = pygame.transform.scale(self.image, (int(w*scale), int(h*scale)))

        self.rect = self.image.get_rect()
        self.rect.center = (Properties.SCREEN_RES[0]/2, Properties.SCREEN_RES[1]*3/4)
        self.hide()

    def setX(self, x_percent):
        a = 0.15 * Properties.SCREEN_RES[0]
        b = 0.7 * Properties.SCREEN_RES[0]
        final_x = a + b * x_percent / 2
        self.rect.center = (final_x, Properties.SCREEN_RES[1]/2)

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self, x_percent=None):
        if x_percent is not None:
            x = min(2, x_percent)
            self.setX(x)
        self.visible =  True
        self.dirty = True