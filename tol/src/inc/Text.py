# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties as Properties

class Text(pygame.sprite.DirtySprite):

    def __init__(self, msg):
        pygame.sprite.DirtySprite.__init__(self)

        self.font = pygame.font.Font('fonts/Oswald-Bold.ttf', 30)
        self.set_message(msg)

    def set_message(self, msg):
        t = self.font.render(msg, True, (0,0,0))

        self.image = pygame.Surface((t.get_width()+20,t.get_height()+20), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        self.rect = self.image.get_rect()

        self.rect = self.image.get_rect()
        x = self.rect.centerx
        y = self.rect.centery

        self.image.blit(t, (x-(t.get_width()/2), y-(t.get_height()/2)))

        self.dirty = 1

class TextLevel(Text):

    def __init__(self, num, method):
        super(TextLevel, self).__init__(str(num))
        self.num = num
        self.method = method

        self.rect.center = ((Properties.SCREEN_RES[0]-30)*num/9 + 10, Properties.SCREEN_RES[1]-30)

    def click(self):
        self.method(self.num)


