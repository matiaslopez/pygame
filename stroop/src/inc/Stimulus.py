# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

import Properties

current_milli_time = lambda: int(round(time.time() * 1000))


class Stimulus(pygame.sprite.DirtySprite):
    def __init__(self, profile="", is_conguent=True):
        pygame.sprite.DirtySprite.__init__(self)

        root_dir = "./images/" + profile + ("-" if profile!= "" else "")
        self.image_cong = pygame.transform.smoothscale(
                        pygame.image.load(root_dir + "congruent.png").convert_alpha(),
                        (Properties.stim_side, Properties.stim_side))
        self.image_incong = pygame.transform.smoothscale(
                        pygame.image.load(root_dir + "incongruent.png").convert_alpha(),
                        (Properties.stim_side, Properties.stim_side))

        self.image = self.image_incong
        self.rect = self.image.get_rect()

        self.rect.center = (Properties.SCREEN_RES[0]/2, Properties.SCREEN_RES[1]/2)
        self.hide()


    def set_stimulus(self,is_incongruent, side):
        self.image = self.image_cong if not is_incongruent else self.image_incong
        self.rect.center = Properties.stim_position[side]

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True
