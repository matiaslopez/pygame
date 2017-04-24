# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties

INIT, STIM, TP1, ANSW, TP2, FEED, END = [ p for p in range(7) ]

current_milli_time = lambda: int(round(time.time() * 1000))


class Trial():

    def __init__(self, logger):
        self.state = None
        self.running = False
        self.handle_end = None
        self.fake_answer = 0
        self.logger = logger

    def set_images(self, stim, target, feed):
        self.stim = stim
        self.target_img = target
        self.feed = feed

    def set(self, ts, tp, tam, tfeed, block_id, handle_end = None, fake_answer=0):
        self.state = INIT
        self.ts = ts
        self.tp = tp
        self.tam = tam
        self.tfeed = tfeed
        self.timed_state = False
        self.block_id = block_id
        self.next()
        if handle_end is not None:
            self.handle_end = handle_end
        self.fake_answer = fake_answer

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
            self.state_duration = self.ts
            self.stim.show()
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
            if self.fake_answer==0:
                self.feed.set(self.percent_answer)
            else:
                self.feed.set(self.fake_answer)
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
