# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties
import State


class Goal(pygame.sprite.DirtySprite):

    def __init__(self, mode=3):
        pygame.sprite.DirtySprite.__init__(self)
        self.mode = mode
        self.set(0)

    def set(self, board_num):
        board = State.State()
        board.set_board_number(board_num)

        self.image = pygame.surface.Surface((
                                            int(Properties.SCREEN_RES[0] * Properties.goal_scale),
                                            int(Properties.SCREEN_RES[1] * Properties.goal_scale)))

        print "size: ", (int(Properties.SCREEN_RES[0] * Properties.goal_scale),
                         int(Properties.SCREEN_RES[1] * Properties.goal_scale))

        self.image.fill([255,255,255])

        floor = pygame.surface.Surface((
                                            int(Properties.SCREEN_RES[0] * Properties.goal_scale),
                                            int(Properties.floor_height * Properties.goal_scale)))
        floor.fill([0,200,0])
        self.image.blit(floor, (0, self.image.get_height()-floor.get_height()))


        self.rect = self.image.get_rect()
        self.rect.topleft = Properties.goal_pos #(Properties.SCREEN_RES[0]-30,30)

        # self.image = pygame.Surface(Properties.stick_rect[num].size)
        # self.image.fill(Properties.stick_color)
        # self.rect = pygame.Rect(Properties.stick_rect[num])

        # self.rect.midbottom = Properties.stick_pos[num]
        for num in xrange(0,3):
            stick = pygame.Surface(Properties.goal_stick_rect[num].size)
            stick.fill(Properties.stick_color)
            self.image.blit(stick, Properties.goal_stick_pos[num])

        (x,y) = self.rect.size
        for num in xrange(1,3+1):
            stim = pygame.transform.scale(pygame.image.load("images/mode_%d_disk_%d.png" %(self.mode, num, )),
                Properties.goal_disk_rect)
            (stick,pos) = board.get_disk_position(num)
            # qq = Properties.goal_stick_pos[stick-1]
            (stick,pos) = Properties.goal_disk_pos["x"][stick-1],Properties.goal_disk_pos["y"][pos-1],
            # self.image.blit(stim, (10*num,10*num))
            print num, (stick,pos)
            self.image.blit(stim, (stick,pos))



        self.dirty = 1


    def hide(self):
        self.visible =  False
        self.dirty = True

    def show(self):
        self.visible =  True
        self.dirty = True
