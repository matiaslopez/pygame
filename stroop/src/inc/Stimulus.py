# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

import Properties

current_milli_time = lambda: int(round(time.time() * 1000))



class Stimulus(pygame.sprite.DirtySprite):
    def __init__(self, profile="", is_conguent=True):
        pygame.sprite.DirtySprite.__init__(self)

        root_dir = "./images/" + profile + ("-" if profile!= "" else "")
        x = pygame.display.get_surface().get_rect().width
        y = pygame.display.get_surface().get_rect().height
        stim_side = int(min(x*1.0/6, y*1.0/5))
        self.stim_position = {0: (int(x*2.0/8), y/2),
                          1: (int(x*6.0/8), y/2)}

        self.image_cong = pygame.transform.smoothscale(
                        pygame.image.load(root_dir + "congruent.png").convert_alpha(),
                        (stim_side, stim_side))
        self.image_incong = pygame.transform.smoothscale(
                        pygame.image.load(root_dir + "incongruent.png").convert_alpha(),
                        (stim_side, stim_side))

        self.image = self.image_incong
        self.rect = self.image.get_rect()

        # self.rect.center = (Properties.SCREEN_RES[0]/2, Properties.SCREEN_RES[1]/2)
        self.hide()


    def set_stimulus(self,is_incongruent, side):
        self.image = self.image_cong if not is_incongruent else self.image_incong
        self.rect.center = self.stim_position[side]

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True
