# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import math

try:
    import numpy
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
import time

import Properties


def rot(point, ang, center):
# ang es un porcentaje, va entre 0 y 1 (se podría pasar)
    #a = numpy.matrix(point)
    #c = numpy.matrix(center)
    #~ R = numpy.matrix([[math.cos(2 * math.pi * ang), -math.sin(2 * math.pi * ang)],
                      # [2 * math.pi * math.sin(ang), math.cos(2 * math.pi * ang)]])
    #R = numpy.matrix([[math.cos(2 * math.pi * ang), math.sin(2 * math.pi * ang)],
         #             [math.sin(-2 * math.pi * ang), math.cos(2 * math.pi * ang)]])
    res = 0 #tuple((((a-c)*R)+c).tolist()[0])
    return res

class ClockHand(pygame.sprite.DirtySprite):
    running = False
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.screen = pygame.display.get_surface()
        #~ self.image_orig = pygame.image.load("./images/hand.png").convert_alpha()
        self.image = pygame.Surface((400,400), pygame.SRCALPHA)   # per-pixel alpha
        self.rect = self.image.get_rect()
        self.rect.center = self.screen.get_rect().center
        (self.x_c,self.y_c) = (self.rect.width/2, self.rect.height/2)

        self.base_points    = { "a0": (self.x_c-6, self.y_c-180),
                        "a1": (self.x_c+6, self.y_c-180),
                        "a2": (self.x_c+6, self.y_c+10),
                        "a3": (self.x_c-6, self.y_c+10)
                        }

        self.next_points = []

#        self.start()
#        self.rotate_image()

    def start(self):
        #~ import pdb; pdb.set_trace()
        self.rotate = 0.0;
        self.init_time = time.time()
        self.already_init = False

        self.tic()
        self.draw()
        self.running = True

    def stop(self):
        self.running = False

    def tic(self):
        if self.running:
            self.rotate_image()

            return (self.rotate < 1)

    def rotate_f(self):
        pts = self.base_points.values()
        self.next_points = self.base_points.values()
        #for i in range(0, len(pts)):
        #    self.next_points.append(rot(pts[i], self.rotate, (self.x_c,self.y_c)))

        #~ print self.next_points

    def draw(self):
        self.image.fill((255,255,255,0))
        self.rotate_f()
        pygame.draw.polygon(self.image, (0,50,250), self.next_points)
        pygame.draw.aalines(self.image, (0,50,250), True, self.next_points, 1)

    def rotate_image(self):
        if not self.already_init:
            self.init_time = time.time()
            self.already_init = True

        delta = time.time() - self.init_time

        delta = min(1.0,delta/2.0)
        self.rotate = delta
        self.draw()


        #~ pass
        #~ self.image = pygame.transform.rotozoom(self.image_orig, self.rotate, 1.0)
        #~ self.rect = self.image.get_rect()
        #~ self.rect.center = (Properties.SCREEN_RES[0]/2, Properties.SCREEN_RES[1]/2)
            #~
        #~ self.rotate += -5


class Clock(pygame.sprite.DirtySprite):
    def __init__(self):
        pygame.sprite.DirtySprite.__init__(self)
        self.image = pygame.image.load("./images/circle.png").convert_alpha()
        self.rect = self.image.get_rect()

        #~ self.rect.center = (400,300)
        self.rect.center = (Properties.SCREEN_RES[0]/2, Properties.SCREEN_RES[1]/2)



