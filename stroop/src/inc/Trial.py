# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties

INIT, STIM, TP1, ANSW, TP2, FEED, END = [ p for p in range(7) ]

current_milli_time = lambda: int(round(time.time() * 1000))

LEFT, RIGHT = [0,1]
CONGUENT, INCONGRUENT = [0,1]

stimulus_reference = {
    0: (CONGUENT, LEFT),
    1: (CONGUENT, RIGHT),
    2: (INCONGRUENT, LEFT),
    3: (INCONGRUENT, RIGHT),
}

class Trial():

    def __init__(self, logger, change_to_active_mode):
        self.state = None
        self.running = False
        self.handle_end = None
        self.logger = logger
        self.change_to_active_mode = change_to_active_mode


    def set_images(self, stim, target, feed):
        self.stim = stim
        self.target_img = target
        self.feed = feed

    def set(self, stim_kind, tmax, tfeed, block_id, handle_end = None):
        print (tmax, tfeed, block_id, handle_end)
        self.state = INIT
        self.stim_kind = stim_kind
        self.tmax = tmax
        self.tfeed = tfeed
        self.timed_state = False
        self.block_id = block_id
        self.next()
        if handle_end is not None:
            self.handle_end = handle_end

    def usr_answer(self):
        if self.state == ANSW:
            delta = current_milli_time() - self.init_time
            # print "ANSWER in: ", delta
            self.logger.log_answer(self.block_id, self.ts, delta)
            self.percent_answer = float(delta) / float(self.ts)
            self.next()
            return True
        else:
            return False

    def next_by_usr(self):
        if self.state == FEED:
            self.next()


    def next(self):
        self.hide()
        self.state = self.state + 1
        self.running = False
        self.init_time = current_milli_time()

        if self.state == TP2 and self.tfeed == 0:
            self.state = self.state + 2

        if self.state == STIM:
            self.running = True
            self.state_duration = self.tmax
            self.stim.set_stimulus(stimulus_reference[self.stim_kind][0],
                                   stimulus_reference[self.stim_kind][1])
            self.stim.show()
            self.change_to_active_mode(True)
            # print "Show STIM"
            self.percent_answer = None
        elif self.state == ANSW:
            self.running = True
            self.state_duration = self.ts * self.tam
            self.target_img.show()
            # print "Waiting ANSW"
        elif self.state == FEED:
            # self.running = True
            # self.state_duration = self.tfeed
            if self.percent_answer is None: # Loggin No Answer
                self.logger.log_answer(self.block_id, self.ts, "NA")
            self.feed.set(self.percent_answer)
            # print "Show FEED"
        elif self.state == TP1 or self.state == TP2:
            self.running = True
            self.state_duration = self.tp
            # print "PAUSE time"
        if self.state == END and self.handle_end is not None:
            self.handle_end()

    def hide(self):
        self.stim.hide()
        self.target_img.hide()
        self.feed.hide()

    def tic(self):
        if self.running:
            if self.state_duration + self.init_time < current_milli_time():
                # print "END state in t= ", current_milli_time() - self.init_time
                self.next()
                return True
        return False
