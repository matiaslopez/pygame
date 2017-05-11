# -*- coding: utf-8 -*-

import pygame

#~ SCREEN_RES = (1200, 900)
#~ SCREEN_RES = (800, 600)

if pygame.display.get_init():
    SCREEN_RES = pygame.display.get_surface().get_size()
else:
    SCREEN_RES = (1200, 900)

MAX_PLANE_GAME = 279

x_max = SCREEN_RES[0]
y_pos = SCREEN_RES[1]/2
positions = [(x_max*1/13, y_pos), (x_max*2/13, y_pos), (x_max*3/13, y_pos), (x_max*4/13, y_pos), (x_max*5/13, y_pos), 
             (x_max*7/13, y_pos), (x_max*8/13, y_pos), (x_max*9/13, y_pos), (x_max*10/13, y_pos), (x_max*11/13, y_pos)
             ]

TITLE = 'AVIONCITO'
MM_INST = u' Este es un juego de velocidad, debes responder lo más rápido que puedas pero sin equivocarte. La letra L indica derecha y la letra A, izquierda. Si el avión es amarillo, tienes que indicar a qué lado apunta; si el avión es naranja, debes indicar el lado opuesto al cual apunta. Si los aviones están dados vuelta, debes indicar la dirección opuesta a la que seleccionarías si estuvieran derechos. ¡Es muy difícil!'
#OBJECTIVE = (u'OBJETIVO', u'APRETAR SEGÚN PARA QUE LADO VA EL AVIÓN.')
#INSTRUCTIONS = (u'INSTRUCCIONES', u'SI EL AVIÓN ES AMARILLO APRETAR PARA DONDE SE DIRIGE EL AVIÓN, SI ES ROJO, AL REVES.')
#COMMANDS = (u'COMANDOS', u'LA TECLA A PARA INDICAR LA IZQUIERDA, LA TECLA L PARA LA DERECHA.')


TIME_BAR_COLOR = (150,100,12, 150)
TIME_BAR_HEIGHT = 30