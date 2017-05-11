# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import Properties
from Plane import *
from random import choice, shuffle


class Level():
    def __init__(self, initial=0):
        self.trial_builder = [  ForwardPlaneLeft, ForwardPlaneRight, #@IgnorePep8
                             InversePlaneLeft, InversePlaneRight,
                             ReverseForwardPlaneLeft, ReverseForwardPlaneRight,
                             ReverseInversePlaneLeft, ReverseInversePlaneRight]
        self.level_structure = {}
        l = self.level_structure
        l["yellow_test"] = [ForwardPlaneLeft for _ in range(3)] + [ForwardPlaneRight for _ in range(3)]   # 6 #@IgnorePep8
        l["yellow"]      = [ForwardPlaneLeft for _ in range(12)] + [ForwardPlaneRight for _ in range(12)]   # 24#@IgnorePep8
        l["red_test"]    = [InversePlaneLeft for _ in range(3)] + [  InversePlaneRight for _ in range(3)]  # 6#@IgnorePep8
        l["red"]         = [InversePlaneLeft for _ in range(12) ] + [  InversePlaneRight for _ in range(12)]  # 24#@IgnorePep8
        l["mix_test"]    = ([ForwardPlaneLeft for _ in range(2) ] + [ ForwardPlaneRight for _ in range(2)] + #@IgnorePep8
                                 [InversePlaneLeft for _ in range(2) ] + [  InversePlaneRight for _ in range(2)]) # 8 #@IgnorePep8
        l["mix"]         = ([ForwardPlaneLeft for _ in range(12) ] + [ ForwardPlaneRight for _ in range(12)] + #@IgnorePep8
                                 [InversePlaneLeft for _ in range(12) ] + [  InversePlaneRight for _ in range(12)]) # 48 #@IgnorePep8

        self.level_order = ["yellow_test", "yellow", "red_test", "red", "mix_test", "mix"] #@IgnorePep8
        self.timed_levels = ["yellow", "red", "mix"]
        for k in l.keys():
            shuffle(l[k])

        self.initial_values(initial)

    def initial_values(self, initial=0):
        self.checkpoint = initial
        #self.correct = 0
        #self.continuous_correct = 0
        #self.wrong = 0
        self.trial_count = 0

    def wrong_answer(self):
        #self.wrong += 1
        #self.continuous_correct = 0
        self.trial_count += 1
        self.condition_next()

    def correct_answer(self):
        #self.correct += 1
        #self.continuous_correct += 1
        self.trial_count += 1
        self.condition_next()

    def condition_next(self):
        if (self.trial_count ==
                len(self.level_structure[self.level_order[self.checkpoint]])):
            self.trial_count = 0
            self.checkpoint += 1

    def next_trial(self):
        if self.checkpoint < len(self.level_order):
            planelist = self.level_structure[self.level_order[self.checkpoint]]
            return planelist[self.trial_count]
        else:
            print "Bad case.....***********"

    def is_timed_level(self):
        return self.level_order[self.checkpoint] in self.timed_levels

    def is_won(self):
        return self.checkpoint >= len(self.level_order)

    def is_lost(self):
        return False  # self.lost_by_miss() or self.lost_by_time()

    def lost_by_miss(self):
        return False  # self.wrong >= 3

    def lost_by_time(self):
        return False  # self.get_num_trials() == Properties.MAX_PLANE_GAME

    def get_num_trials(self):
        return self.trial_count
