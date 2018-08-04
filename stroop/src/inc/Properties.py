# -*- coding: utf-8 -*-
import pygame

SCREEN_RES = (1200, 900)
# SCREEN_RES = (800, 600)

(x,y) = SCREEN_RES

BLACK, BLUE, RED, YELLOW, WHITE = [ p for p in range(0,5) ]

colors_dict = {
  "BLACK": BLACK, "BLUE": BLUE, "RED": RED, "YELLOW": YELLOW, "WHITE": WHITE,
}

# (BACKGR_lyr, DIAGRAM_lyr,
#     MSG_lyr, CTRL_BTN_lyr,  INST_lyr, FEED_lyr
#     ) = [ p for p in range(0,6) ]

EXPERIMENT_MODE, FREE_MODE = [ p for p in range(0,2) ]
INTERACTIVE, PASSIVE, FEEDBACK = [ p for p in range(0,3) ]

class Profile():
  def __init__(self, props = {"BACKGROUND": 1, "PIECES": 1}):
    self.BACKGROUND = props["BACKGROUND"]
    self.PIECES = props["PIECES"]


PROFILE = Profile()

img_done_pos = (int(x*11.0/12), int(y * 7.0/10))
img_done_side = int(x*1.0/10)

stim_side = int(min(x*1.0/6, y*1.0/5))
stim_position = {0: (int(x*2.0/8), y/2),
                 1: (int(x*6.0/8), y/2)}

button_position = {0: (int(x*1.0/8), int(y*5.0/6)),
                 1: (int(x*7.0/8), int(y*5.0/6))}

# positions_diagrams_x = {1: [int(x * (2+0.5) / 5 + 1) for i in xrange(1,2)],
#                       2: [int(x * (i+0.5) / 4 +1) for i in xrange(1,3)],
#                       3: [int(x * (i+0.5) / 5 +1) for i in xrange(1,4)],
#                       5: [int(x * (i+0.5) / 5) for i in xrange(5)]}
# positions_diagrams_y = [y * (i+1) / 5 for i in xrange(3)]

# diagram_scale = 0.3
# diagram_size_x, diagram_size_y = (x/5, x/5) # 200
# diagram_back = [100,100,100]

# diagram_box_side = x/20 # 40
# # off_set = (diagram_size_x - diagram_box_side * 4)/8
# off_set = (diagram_size_x)/32
# print "diagram_size_x - diagram_box_side  ", diagram_size_x, diagram_box_side
# print "off_set ", off_set
# # arrows_pos = (diagram_size_x/2 - diagram_box_side/2, diagram_size_y*1/4 + diagram_box_side/2)
# arrows_pos = (diagram_size_x/2, diagram_size_y*1/4 + diagram_box_side/2 + 1*off_set)

# positions_palette_y = int(y * 9/10)
# positions_palette_x = [x/2 + diagram_box_side * 1.4 * i + 0.7*diagram_box_side for i in xrange(-2,2)]




# print "img_done_side ", img_done_side


# palette_place = {1: [0], 2: [-x/4, x/4], 3: [-x/3, 0, x/3]}