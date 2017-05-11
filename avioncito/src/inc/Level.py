# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame

import Properties
from Plane import *
from random import choice


class Level():
    def __init__(self, initial=0):
        self.trial_builder = [  ForwardPlaneLeft, ForwardPlaneRight, 
                                InversePlaneLeft, InversePlaneRight,
                                ReverseForwardPlaneLeft, ReverseForwardPlaneRight,
                                ReverseInversePlaneLeft, ReverseInversePlaneRight]
                             
        self.yellow = [ForwardPlaneLeft, ForwardPlaneRight] 
        self.red = [InversePlaneLeft, InversePlaneRight]
        self.yellow_inv = [ReverseForwardPlaneLeft, ReverseForwardPlaneRight]
        self.red_inv = [ReverseInversePlaneLeft, ReverseInversePlaneRight]
        
        self.initial_values(initial)
                                
    def initial_values(self, initial=0):
        self.checkpoint = initial
        self.correct = 0
        self.continuous_correct = 0
        self.wrong = 0
        self.trial_count = 0

    def wrong_answer(self):
        self.wrong += 1
        self.continuous_correct = 0
        self.trial_count += 1 

    def correct_answer(self):
        self.correct += 1
        self.continuous_correct += 1
        self.trial_count += 1
        self.condition_next()
                
    def condition_next(self):
        if (self.checkpoint == 0 and self.continuous_correct == 10) or (self.checkpoint != 0 and self.continuous_correct == 30):
            self.continuous_correct = 0
            self.wrong = 0
            self.checkpoint += 1
        
    def next_trial(self):
        if self.checkpoint==0:
            return choice(self.yellow)
        elif self.checkpoint in range(1,3+1):
            return choice(sum((self.yellow for i in range(3)),sum((self.red for i in range(2)), [])))
        elif self.checkpoint in range(4,5+1):
            return choice(sum((self.yellow_inv for i in range(3)),sum((self.red_inv for i in range(2)), [])))
        elif self.checkpoint in range(6,10+1):
            return choice(sum((self.yellow for i in range(3)),
                              sum((self.red for i in range(2)),
                                  sum((self.yellow_inv for i in range(3)),
                                      sum((self.red_inv for i in range(2)),[])))))
        else:
            print "Bad case.....***********"

        
    def is_won(self):
        return False #self.checkpoint == (len(self.trial_builder)+1)

    def is_lost(self):
        return self.lost_by_miss() or self.lost_by_time()

    def lost_by_miss(self):
        return self.wrong >= 3
    
    def lost_by_time(self):
        return self.get_num_trials() == Properties.MAX_PLANE_GAME
        
    def get_num_trials(self):
        return self.trial_count