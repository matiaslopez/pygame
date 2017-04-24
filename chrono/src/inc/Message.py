# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

class Message(pygame.sprite.DirtySprite):


    def __init__(self, msg, snd_msg = None):
        pygame.sprite.DirtySprite.__init__(self)

        self.image = pygame.Surface((800,200), pygame.SRCALPHA)
        self.image.fill((30,170,70,120))
        self.rect = self.image.get_rect()

        self.font = pygame.font.Font('fonts/Mandingo.ttf', 48)
        self.font2 = pygame.font.Font('fonts/Mandingo.ttf', 30)

        self.rect = self.image.get_rect()
        x = self.rect.centerx
        y = self.rect.centery

        if snd_msg is not None:
            y -=30

        t = self.font.render(msg, True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y-(t.get_height()/2)))

        if snd_msg is not None:
            y +=60

            t = self.font2.render(snd_msg, True, (0,0,0))
            self.image.blit(t, (x-(t.get_width()/2), y-(t.get_height()/2)))

        self.rect.center = pygame.display.get_surface().get_rect().center
        self.hide()

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self, x_percent=None):
        self.visible =  True
        self.dirty = True
