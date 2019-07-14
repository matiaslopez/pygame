# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties



class ImageMessage(pygame.sprite.DirtySprite):

    def __init__(self, name, profile=""):
        pygame.sprite.DirtySprite.__init__(self)
        self.name = name
        self.profile = profile + ("-" if profile != "" else "")

        self.set()

    def set(self):
        self.image = pygame.transform.smoothscale(
            pygame.image.load("./images/{}".format(self.profile + self.name)).convert_alpha(),
                         Properties.SCREEN_RES)
        self.rect = self.image.get_rect()

        self.hide()

    def scale(self, x, y):
        self.image = pygame.transform.smoothscale(self.image, (x, y))
        self.rect = self.image.get_rect()
        self.dirty = True

    def hide(self):
        # print "Hiding ", self.name
        self.visible =  False
        self.dirty = True

    def show(self):
        # print "Showing ", self.name
        self.visible =  True
        self.dirty = True

class ImageButton(ImageMessage):
    def __init__(self, side):
        self.side = side
        if side:
            ImageMessage.__init__(self, "right_idle.png")
        else:
            ImageMessage.__init__(self, "left_idle.png")

        self.image_unpressed = self.image
        self.image_pressed = pygame.image.load("./images/" + ("right"  if side else "left")
                            + "_pressed.png" ).convert_alpha()

        x = pygame.display.get_surface().get_rect().width
        y = pygame.display.get_surface().get_rect().height
        img_done_side = min(int(x*1.0/7), int(y*1.0/5))
        button_position = {0: (int(x*1.0/8), int(y*5.0/6)),
                         1: (int(x*7.0/8), int(y*5.0/6))}

        self.image_unpressed = pygame.transform.smoothscale(
                                self.image_unpressed,
                                (img_done_side, img_done_side))
        self.image_pressed = pygame.transform.smoothscale(
                                self.image_pressed,
                                (img_done_side, img_done_side))

        self.image = self.image_unpressed

        self.rect = self.image.get_rect()
        self.rect.center = button_position[self.side]
        # self.rect.center = (7.5 * (self.image.get_width() * 1.25), 6 * (self.image.get_height()* 1.25))

    def set_callback(self, callback):
        self.callback = callback

    def click(self):
        print "ImageDone clicked"
        self.image = self.image_pressed
        self.dirty = True

    def un_click(self):
        self.image = self.image_unpressed
        self.dirty = True
        # self.callback()

    def release_click(self):
        self.un_click()
        print "Result press " + ("right" if self.side else "left")
        self.callback(self.side)


class Feedback(ImageMessage):

    def __init__(self, is_ok=True):
        src = "feed-ok.png" if is_ok else "feed-no.png"
        ImageMessage.__init__(self, src)

        (x,y) = pygame.display.get_surface().get_rect().size
        # (x,y) = Properties.SCREEN_RES
        self.image = pygame.surface.Surface((x*1., y*1.)).convert_alpha()
        # self.background["pasive"].image = pygame.surface.Surface(self.screen.get_size())
        self.image.fill([255,250,104,100] if is_ok else [40,40,40,100])

        emoji = pygame.image.load("./images/" + src).convert_alpha()

        self.rect = self.image.get_rect()
        self.image.blit(emoji, (self.rect.centerx-(emoji.get_width()/2), self.rect.centery-(emoji.get_height()/2)))

        self.rect.center = pygame.display.get_surface().get_rect().center

        self.dirty = True
        self.visible = False

    def set_callback(self, callback):
        self.callback = callback

    def click(self):
        # print "ImageDone clicked"
        self.image = self.image_pressed
        self.dirty = True

    def release_click(self):
        self.image = self.image_unpressed
        self.dirty = True
        # print "ImageDone clicked"
        self.callback()