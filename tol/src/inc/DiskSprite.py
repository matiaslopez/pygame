# -*- coding: utf-8 -*-
import pygame
import Properties as Properties


class DiskSprite(pygame.sprite.DirtySprite):

    def __init__(self, disk, (x,y)):
        super(DiskSprite, self).__init__()

        self.disk = disk
        num = self.disk.num

        self.image = pygame.Surface(Properties.disk_rect.size)
        self.image.fill(Properties.disk_colors[num-1])
        self.rect = pygame.Rect(Properties.disk_rect)

        self.set_stick_pos((x,y))

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
        (x_b,y_b) = Properties.stick_pos[x-1]
        self.rect.midbottom = (x_b,y_b-(Properties.disk_heigth+5)*(y-1)-10)
        self.current_pos = p
        self.dirty = 1


    def set_position(self, pos):
        self.rect.center = pos
        self.dirty = 1