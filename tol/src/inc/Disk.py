# -*- coding: utf-8 -*-
import pygame
import Properties as Properties


class Disk():

    def __init__(self, num):
        self.num = num
        self.moveable = True
        
    def on_top(self):
        self.moveable = True
        
    def under_disk(self):
        self.moveable = False
        
    
     
        