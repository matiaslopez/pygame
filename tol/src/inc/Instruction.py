# -*- coding: utf-8 -*-

import pygame
import Properties

class Instruction(pygame.sprite.DirtySprite):

    def __init__(self, moves=2, trial=2):
        super(Instruction, self).__init__()

        w, h = Properties.SCREEN_RES
        self.image = pygame.Surface((4*w/8,3*h/8), pygame.SRCALPHA)
        self.font = pygame.font.Font('fonts/Oswald-Bold.ttf', 34)
        self.font2 = pygame.font.Font('fonts/Oswald-Bold.ttf', 18)

        self.set_num(moves, trial)
        self.callback = None

    def set_num(self, moves, trial, callback=None):
        self.callback = callback
        self.image.fill((30,170,70,250))

        self.rect = self.image.get_rect()

        x = self.rect.centerx
        y = self.rect.height / 3

        t = self.font.render("SALE EN {} MOVIDA{}".format(moves, "S" if moves>1 else ""), True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y-(t.get_height()/2)))

        t = self.font2.render(u"TRIAL {} - HACÉ CLICK PARA COMENZAR".format(trial), True, (0,0,0))
        y = 4* self.rect.height / 5
        self.image.blit(t, (x-(t.get_width()/2), y))

        self.rect.center = pygame.display.get_surface().get_rect().center
        self.show()

    def hide(self):
        self.visible =  False
        self.dirty = True
        if self.callback:
            self.callback()
            self.callback = None

    def show(self):
        self.visible =  True
        self.dirty = True