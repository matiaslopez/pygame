# -*- coding: utf-8 -*-
import pygame

#~ SCREEN_RES = (1200, 900)

if pygame.display.get_init():
    SCREEN_RES = pygame.display.get_surface().get_size()
    print "TRRUEE"
else:
    print "FOLLsss"
    SCREEN_RES = (1200, 900)
SCREEN_RES = (800, 600)

(disk_width, disk_heigth)   = (120,60)
(stick_width, stick_heigth) = (30, disk_heigth)


disk_colors = [(255,0,0),
               (0,255,0),
               (0,0,255)]


disk_rect = pygame.Rect(0, 0, disk_width, disk_heigth)

stick_color = (255,127,0)

stick_rect = [
              pygame.Rect(0, 0, stick_width, (stick_heigth+05)*1),
              pygame.Rect(0, 0, stick_width, (stick_heigth+05)*2),
              pygame.Rect(0, 0, stick_width, (stick_heigth+05)*3),
         ]

stick_pos = [(200,500), (400,500), (600,500)]