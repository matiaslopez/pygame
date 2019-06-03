# -*- coding: utf-8 -*-
import pygame

class DiskSprite(pygame.sprite.DirtySprite):

    def __init__(self, disk, coord, mode=3, is_img = False, prop = None):
        super(DiskSprite, self).__init__()

        self.disk = disk
        self.prop = prop
        num = self.disk.num

        # self.image = pygame.Surface(Properties.disk_rect.size)
        # self.image.fill(Properties.disk_colors[num-1])
        # self.rect = pygame.Rect(Properties.disk_rect)

        self.image = pygame.transform.scale(pygame.image.load("images/mode_%s_disk_%s.png" %(mode,num, )), self.prop.disk_rect.size)
        self.rect = self.image.get_rect()
        # self.rect.topleft = Properties.goal_pos #(Properties.SCREEN_RES[0]-30,30)
        self.dirty = 1

        self.set_stick_pos(coord)

    def newpos(self):
        self.rect.center = (self.x, self.y)
        self.dirty = 1

    def click(self):
        # print "Clicked on Disk ", self.disk.num

        return self.disk.moveable

    def set_stick_pos(self, p=None):
        if p is None:
            p = self.current_pos
        (x,y) = p
        (x_b,y_b) = self.prop.stick_pos[x-1]
        self.rect.midbottom = (x_b,y_b-(self.prop.disk_height+5)*(y-1)-10)
        self.current_pos = p
        self.dirty = 1


    def set_position(self, pos):
        self.rect.center = pos
        self.dirty = 1

    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True