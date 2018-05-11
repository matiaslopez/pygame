# -*- coding: utf-8 -*-
import pygame

#~ SCREEN_RES = (1200, 900)

# if pygame.display.get_init():
    # SCREEN_RES = pygame.display.get_surface().get_size()
    # print "TRRUEE"
# else:
    # print "FOLLsss"
    # SCREEN_RES = (1200, 900)
SCREEN_RES = (800, 600)

(x,y) = SCREEN_RES

# DRAWS
floor_height = 50


# DISKS
(disk_width, disk_height)   = (120,60)
disk_colors = [(210,0,30),
               (0,210,30),
               (30,0,210)]
disk_rect = pygame.Rect(0, 0, disk_width, disk_height)


# STICKS
(stick_width, stick_height) = (30, disk_height)
stick_color = (255,127,0)
sticks_y_pos = [200, 400, 600]

stick_rect = [ pygame.Rect(0, 0, stick_width, (disk_height+5)*qq+15) for qq in [1,2,3]]
stick_pos = [ (qq, y - floor_height) for qq in sticks_y_pos]

# GOAL
goal_pos = (0.05* x, 0.05* y)
goal_scale = 0.2
goal_disk_rect = (int(disk_width*goal_scale), int(disk_height*goal_scale))
goal_stick_rect = [ pygame.Rect(0, 0, int(stick_width*goal_scale), int(((disk_height+5)*qq+15)*goal_scale)) for qq in [1,2,3]]
goal_stick_pos = [ (int((qq- stick_width/2) * goal_scale),
                    int((y - (floor_height + (disk_height+5)* (num+1) + 15))*goal_scale))
                  for num,qq in enumerate(sticks_y_pos)]
goal_disk_pos = {
      "x": [ int((qq - disk_width/2) * goal_scale) for qq in sticks_y_pos],
      "y": [ int((y - (floor_height + (disk_height+5)* (num+1) + 15))*goal_scale) for num in range(3)]
      }

# BUTTONS
img_done_pos = (1.05* x, 0.32 * y)
