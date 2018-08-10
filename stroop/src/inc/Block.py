# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties

INIT_OP, OP, INIT_FEED, ACTIVE_STOP_2, FEED, INIT_SUBJ, ACTIVE_STOP_3, SUBJ, END, ACTIVE_STOP_1 = [ p for p in range(10) ]

current_milli_time_block = lambda: int(round(time.time() * 1000))

class Block():

    def __init__(self, trial, msgs):
        self.trial = trial
        self.msgs = msgs
        self.waiting = False
        self.activeEndTrial = False

    def set(self, block_props, block_id, handle_end = None):
        self.n1 = block_props['n1']
        self.n2 = block_props['n2']
        self.n3 = block_props['n3']
        self.block_id = block_id
        self.idx = 0
        self.properties = block_props['properties']
        self.state = INIT_OP
        self.waiting = True
        self.activeEndTrial = False
        self.next_by_usr()
        self.handle_end = handle_end

    def next_by_usr(self):
        if self.waiting == True:
            self.next()
        else:
            self.trial.next_by_usr()

    def to_waiting(self):
        self.msgs["wait"].draw_bar(self.idx, len(self.n3))
        self.msgs["wait"].show()

        self.waiting = True

    def to_activeEndTrial(self):
        # self.msgs["background"].show()
        self.activeEndTrial = True
        self.init_time = current_milli_time_block()

    def next(self):
        self.hide()

        if self.state == INIT_OP:
            # print ("Estamos en la condicion: INIT_OP")
            self.waiting = True
            self.msgs["op"].show()
            self.state = self.state + 1
            # print "Show INIT_OP msj"
        # elif self.state == ACTIVE_STOP_1:
            # print ("Estamos en la condicion: ACTIVE_STOP_1")
            # self.to_activeEndTrial()
            # self.state = self.state + 1
        elif self.state == OP:
            # print ("Estamos en la condicion: OP")
            # if len(self.n1) > self.idx:
            if len(self.n1) > self.idx:
                self.trial.set(self.n1[self.idx], # TS
                        self.properties["tmax"], # TP
                        self.properties["tfeed"],
                        "OPERATOR-" + str(self.block_id),
                        "TRIAL-" + str(self.idx),
                        self.to_activeEndTrial
                        )
                self.idx = self.idx + 1
            else: # INIT_FEED
                self.state = self.state + 2
                self.waiting = True
                self.msgs["feed"].show()
                self.idx = 0
                # print "Show INIT_FEED msj"
        elif self.state == ACTIVE_STOP_2:
            # print ("Estamos en la condicion: ACTIVE_STOP_2")
            self.to_activeEndTrial()
            self.state = self.state + 1
        elif self.state == FEED:
            # print ("Estamos en la condicion: FEED")
            if len(self.n2) > self.idx:
                self.trial.set(self.n2[self.idx], # TS
                        self.properties["tmax"], # TP
                        self.properties["tfeed"],
                        "FEEDBACK-" + str(self.block_id),
                        "TRIAL-" + str(self.idx),
                        self.to_activeEndTrial)
                self.idx = self.idx + 1
            else: # INIT_SUBJ
                self.state = self.state + 2
                self.waiting = True
                self.msgs["subj"].show()
                self.idx = 0
                # print "Show INIT_SUBJ msj"
        elif self.state == ACTIVE_STOP_3:
            # print ("Estamos en la condicion: ACTIVE_STOP_3")
            self.to_activeEndTrial()
            self.state = self.state + 1
        elif self.state == SUBJ:
            # print ("Estamos en la condicion: SUBJ")
            if len(self.n3) > self.idx:
                self.trial.set(self.n3[self.idx], # TS
                        self.properties["tmax"], # TP
                        0, # TFEED
                        "SUBJECT-" + str(self.block_id),
                        "TRIAL-" + str(self.idx),
                        self.to_activeEndTrial)
                        # self.to_waiting)
                self.idx = self.idx + 1
            else:
                self.state = self.state + 1
                # self.waiting = True
                self.msgs["end_block"].show()
                if self.handle_end is not None:
                    self.handle_end()


    def hide(self):
        self.waiting = False
        self.trial.hide()
        for v in self.msgs.itervalues():
            # print "block -> Hiding"
            v.hide()

    def tic(self):
        if self.activeEndTrial:
            # if 0 + self.init_time < current_milli_time_block():
            if 1000 + self.init_time < current_milli_time_block():
                # print "END state in t= ", current_milli_time_block() - self.init_time
                self.next()
                self.activeEndTrial = False
                return True
        return False

