# -*- coding: utf-8 -*-
import pygame
import Properties as Properties

class Stick():    
    
    def __init__(self, num):        
        self.num = num
        self.disks = []

    def add_disk(self, disk):
        if len(self.disks) < self.num:
            if len(self.disks):
                self.disks[len(self.disks)-1].under_disk()
            self.disks.append(disk)
            return True
        return False
        
    def remove_disk(self):
        if len(self.disks) > 0: 
            d = self.disks.pop()
            if len(self.disks):
                self.disks[len(self.disks)-1].on_top()
            return d
        return None
    
    def not_full(self):
        return len(self.disks) < self.num
    