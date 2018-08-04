# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties
from ImageMessage import *

class ImageMessageBar(ImageMessage):


    def __init__(self, block_num, name, feedback):
        self.feedback = feedback
        ImageMessage.__init__(self, block_num, name)

    def reset(self):
        self.set()

    def draw_bar(self, num, length):
        self.reset()
        (x,y) = Properties.SCREEN_RES
        box = (x/10, 6*y/10, 8*x/10, y/10)

        percent = int(float(num)/float(length) * 10)
        margin = 10
        box2 = (x/10 + margin, 6*y/10 + margin, percent * 8*x/100 - 2*margin, y/10 - 2*margin)

        rect = pygame.draw.rect(self.image, (60,60,100), box)
        rect2 = pygame.draw.rect(self.image, (220, 60,60), box2)

        if num==length:
            (x2, y2, w, h) = self.feedback.ok.image.get_rect()
            self.image.blit(self.feedback.ok.image, (x/2 - w/2,y/2-h/2))

    def hide(self):
        self.visible =  False
        self.dirty = True
        self.feedback.hide()

    def show(self):
        self.visible =  True
        self.dirty = True
