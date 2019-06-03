# -*- coding: utf-8 -*-
import pygame

#~ SCREEN_RES = (1200, 900)

# if pygame.display.get_init():
    # SCREEN_RES = pygame.display.get_surface().get_size()
    # print "TRRUEE"
# else:
    # print "FOLLsss"
    # SCREEN_RES = (1200, 900)
# SCREEN_RES = (1200, 700)
class Properties():

  def __init__(self, SCREEN_RES):
    self.SCREEN_RES = SCREEN_RES
    (x,y) = SCREEN_RES

    # DRAWS
    self.floor_height = 50


    # DISKS
    (self.disk_width, self.disk_height)   = (120,60)
    self.disk_colors = [(210,0,30),
                   (0,210,30),
                   (30,0,210)]
    self.disk_rect = pygame.Rect(0, 0, self.disk_width, self.disk_height)


    # STICKS
    (self.stick_width, self.stick_height) = (30, self.disk_height)
    self.stick_color = (255,127,0)
    self.sticks_y_pos = [200, 400, 600]

    self.stick_rect = [ pygame.Rect(0, 0, self.stick_width, (self.disk_height+5)*qq+15) for qq in [1,2,3]]
    self.stick_pos = [ (qq, y - self.floor_height) for qq in self.sticks_y_pos]

    # GOAL
    self.goal_pos = (0.05* x, 0.05* y)
    self.goal_scale = 0.2
    self.goal_disk_rect = (int(self.disk_width*self.goal_scale),
                           int(self.disk_height*self.goal_scale))
    self.goal_stick_rect = [ pygame.Rect(0, 0, int(self.stick_width*self.goal_scale),
                  int(((self.disk_height+5)*qq+15)*self.goal_scale)) for qq in [1,2,3]]
    self.goal_stick_pos = [ (int((qq- self.stick_width/2) * self.goal_scale),
                        int((y - (self.floor_height + (self.disk_height+5)* (num+1) + 15))*self.goal_scale))
                      for num,qq in enumerate(self.sticks_y_pos)]
    self.goal_disk_pos = {
          "x": [ int((qq - self.disk_width/2) * self.goal_scale) for qq in self.sticks_y_pos],
          "y": [ int((y - (self.floor_height + (self.disk_height+5)* (num+1) + 15))*self.goal_scale) for num in range(3)]
          }

    # BUTTONS
    self.img_done_pos = (1.05* x, 0.32 * y)
