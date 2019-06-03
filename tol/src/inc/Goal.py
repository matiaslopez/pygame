# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import State


class Goal(pygame.sprite.DirtySprite):

    def __init__(self, mode=3, prop=None):
        pygame.sprite.DirtySprite.__init__(self)
        self.mode = mode
        self.prop = prop
        self.set(0)

    def set(self, board_num):
        board = State.State()
        board.set_board_number(board_num)

        self.image = pygame.surface.Surface((
                                            int(self.prop.SCREEN_RES[0] * self.prop.goal_scale),
                                            int(self.prop.SCREEN_RES[1] * self.prop.goal_scale)))

        self.image.fill([255,255,255])

        floor = pygame.surface.Surface((
                                            int(self.prop.SCREEN_RES[0] * self.prop.goal_scale),
                                            int(self.prop.floor_height * self.prop.goal_scale)))
        floor.fill([0,200,0])
        self.image.blit(floor, (0, self.image.get_height()-floor.get_height()))


        self.rect = self.image.get_rect()
        self.rect.topleft = self.prop.goal_pos #(self.prop.SCREEN_RES[0]-30,30)


        for num in xrange(0,3):
            stick = pygame.Surface(self.prop.goal_stick_rect[num].size)
            stick.fill(self.prop.stick_color)
            self.image.blit(stick, self.prop.goal_stick_pos[num])

        (x,y) = self.rect.size
        for num in xrange(1,3+1):
            stim = pygame.transform.scale(pygame.image.load("images/mode_%s_disk_%s.png" %(self.mode, num, )),
                self.prop.goal_disk_rect)
            (stick,pos) = board.get_disk_position(num)
            (stick,pos) = self.prop.goal_disk_pos["x"][stick-1],self.prop.goal_disk_pos["y"][pos-1],
            self.image.blit(stim, (stick,pos))



        self.dirty = 1


    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True
