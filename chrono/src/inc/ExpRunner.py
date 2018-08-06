# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties
import json

INIT_OP, OP, INIT_FEED, FEED, INIT_SUBJ, SUBJ, END = [ p for p in range(7) ]

class ExpRunner():

    def __init__(self, exp_struct, block, msgs, handle_set_images):
        self.handle_set_images = handle_set_images
        self.set(exp_struct, block, msgs)

    def set(self, exp_struct, block, msgs):
        self.current_block = 0
        self.struct = exp_struct
        self.block = block
        self.msgs = msgs
        self.waiting = True
        self.msgs["welcome"].show()

    def next_block(self):
        if self.waiting == True:
            self.next()

    def to_waiting(self):
        # self.msgs["wait"].show()
        self.waiting = True

    def next(self):
        self.current_block = self.current_block + 1

        if self.struct.has_key(str(self.current_block)):
            # print "STARTING WITH BLOCK " + str(self.current_block)
            self.handle_set_images(str(self.current_block))
            self.hide()
            self.block.set(self.struct[str(self.current_block)], self.current_block, self.to_waiting)
        else:
            self.hide()
            self.msgs["the_end"].show()

    def hide(self):
        self.waiting = False
        self.block.hide()
        for v in self.msgs.itervalues():
            v.hide()
