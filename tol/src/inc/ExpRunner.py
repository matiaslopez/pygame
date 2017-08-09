# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties
import json

INIT_OP, OP, INIT_FEED, FEED, INIT_SUBJ, SUBJ, END = [ p for p in range(7) ]

class ExpRunner():

    def __init__(self, exp_struct, trial):
        self.exp_struct = exp_struct
        self.trial = trial
        self.set()
        self.instruction = None

    def set(self):
        self.current_trial = 0
        self.num_consecutive_lost = 0
        self.waiting = True

    def next_trial(self, correct, feedback=False):
        if not feedback:
            if correct:
                self.num_consecutive_lost = 0
            else:
                self.num_consecutive_lost += 1

        # print "NEXT - Num consecutive_lost", self.num_consecutive_lost

        if self.waiting == True:
            if self.num_consecutive_lost < 3:
                self.next()
            else:
                self.end_test()


    def to_waiting(self):
        self.waiting = True

    def next(self):
        self.current_trial = self.current_trial + 1

        t = str(self.current_trial)
        if self.exp_struct["trials"].has_key(t):
            # print "STARTING WITH trial " + t

            src = self.exp_struct["trials"][t][0]
            target = self.exp_struct["trials"][t][1]
            feedback = self.exp_struct["trials"][t][2]
            self.trial.set(src,target, feedback)
            self.instruction.set_num(len(sequence), (lambda: self.trial.start(t, sequence, feedback)))
        else:
            self.end_test()
