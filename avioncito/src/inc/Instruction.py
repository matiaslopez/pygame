# -*- coding: utf-8 -*-

import pygame
import Properties as prop
import textrect  
    
class Instruction(pygame.sprite.DirtySprite):
    
    def __init__(self):
        super(Instruction, self).__init__()
        
        self.image = pygame.Surface((800,800), pygame.SRCALPHA)  
        self.image.fill((30,170,70,250))      
        self.rect = self.image.get_rect()

        self.font = pygame.font.Font('fonts/Mandingo.ttf', 48)
        self.font2 = pygame.font.Font('fonts/Mandingo.ttf', 34)        
        self.font3 = pygame.font.Font('fonts/Mandingo.ttf', 24)        
        
        self.rect = self.image.get_rect()
        
        x = self.rect.centerx
        y = 50
       
        t = self.font.render(prop.TITLE, True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y-(t.get_height()/2)))

        y += 10 + t.get_height()
        
        text_r = textrect.render_textrect(unicode(prop.MM_INST.upper()), self.font3, pygame.Rect(0,0,700,300), (0,0,0), (100,100,200,0))
        self.image.blit(text_r, (x-(text_r.get_width()/2), y))
        y += 10 + text_r.get_height()

#        for i in [prop.OBJECTIVE, prop.INSTRUCTIONS, prop.COMMANDS]:
#            t = self.font2.render(i[0], True, (0,0,0))
#            self.image.blit(t, (x-(t.get_width()/2), y))
#            y += 5 + t.get_height()
#
#            text_r = textrect.render_textrect(unicode(i[1]), self.font3, pygame.Rect(0,0,700,100), (0,0,0), (100,100,200,0))
#            self.image.blit(text_r, (x-(text_r.get_width()/2), y))
#            y += 10 + text_r.get_height()

        t = self.font2.render(u"PRESIONÁ ESPACIO PARA COMENZAR", True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y))
        y += 5 + t.get_height()


        self.rect.center = pygame.display.get_surface().get_rect().center