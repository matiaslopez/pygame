# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties

INIT, PLAY, ANSWERED, END = [ p for p in range(4) ] # STIM, TP1, TP2

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
        self.feedback = {}
        self.change_to_active_mode = change_to_active_mode


    def set_images(self, stim, feed):
        self.stim = stim
        # self.target_img = target
        self.feed = feed

    def set(self, stim_kind, tmax, tfeed, block_id, idx_trial, handle_end = None):
        # print (tmax, tfeed, block_id, handle_end)
        self.state = INIT
        self.stim_kind = stim_kind
        self.tmax = tmax
        self.tfeed = tfeed
        self.timed_state = False
        self.block_id = block_id
        self.idx_trial =  idx_trial
        self.next()
        if handle_end is not None:
            self.handle_end = handle_end

    def usr_answer(self, ans_value):

        if stimulus_reference[self.stim_kind][0] == 0:
            is_correct = ans_value == stimulus_reference[self.stim_kind][1]
        else:
            is_correct = ans_value != stimulus_reference[self.stim_kind][1]

        # print "Receiving answer", ans_value, " - Is correct? ", is_correct

        delta = current_milli_time() - self.init_time
        # print delta
        self.logger.log_trial_result(self.block_id,
                                     self.stim_kind,
                                     self.idx_trial,
                                     is_correct,
                                     delta)
        self.result =  is_correct
        self.next()


    def next_by_usr(self):
        if self.state == ANSWERED:
            self.next()


    def next(self):
        self.hide()
        self.state = self.state + 1
        self.running = False
        self.init_time = current_milli_time()
        self.state_duration = 0

        # if self.state == TP2 and self.tfeed == 0:
            # self.state = self.state + 2

        if self.state == PLAY: #STIM:
            self.running = True
            self.state_duration = self.tmax
            self.stim.set_stimulus(stimulus_reference[self.stim_kind][0],
                                   stimulus_reference[self.stim_kind][1])
            self.stim.show()
            self.change_to_active_mode(True)
            # print "Show STIM", self.state_duration
            self.percent_answer = None
        elif self.state == ANSWERED:
            self.running = True
            if self.tfeed:
                self.state_duration = self.tfeed
                self.feedback[self.result].show()
            # if self.percent_answer is None: # Loggin No Answer
                # self.logger.log_answer(self.block_id, self.ts, "NA")
            # self.feed.set(self.percent_answer)
            # print "Show ANSWERED", self.result
        # elif self.state == TP2:
        #     self.running = True
        #     self.state_duration = self.tfeed
        #     # print "PAUSE time"
        if self.state == END and self.handle_end is not None:
            for i in self.feedback.values():
                i.hide()
            self.handle_end()

    def hide(self):
        # print "Trial -> hide"
        self.stim.hide()
        # self.target_img.hide()
        self.feed.hide()
        self.change_to_active_mode(False)

    def tic(self):
        if self.running:
            # print ".",
            if self.state_duration + self.init_time < current_milli_time():
                # print "END state in t= ", current_milli_time() - self.init_time
                self.result = False
                self.next()
                return True
        return False
