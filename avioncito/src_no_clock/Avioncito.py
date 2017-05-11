#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from pygame import time, mouse
#import gtk
from pygame.locals import *
#~ from random import choice
import time

import json
import datetime

SUBJECT_NAME = raw_input('Nombre: ')

import inc.Properties as Properties

if pygame.display.get_init():
    from includes.fw_api import Fw_API #@UnresolvedImport
    LOG = True
else:
    pygame.init()
    pygame.display.set_mode(Properties.SCREEN_RES, pygame.FULLSCREEN)
    LOG = False

from inc.EventHandler import EventHandler
from inc.Event import Event
from inc.Plane import *
from inc.LevelBar import *
from inc.Clock import *
from inc.LevelTime import *
from inc.Message import *
from inc.Instruction import *
from inc.CloseButton import *
from inc.InfoButton import *
from inc.Level import *
from inc.Text import *
from inc.State import *

#~ BACKGR_lyr: Background
#~ CLOCK_lyr: Clock
#~ CLOCK_HAND_lyr: clock hand
#~ PLANE_lyr: Plane
#~ DEBUG_TXT_lyr: 
#~ LEVEL_BAR_lyr barra de niveles
#~ LEVEL_BAR_CHK_lyr checkpoint
#~ MSG_lyr : wrong and correct shadow
#~ CTRL_BTN_lyr : Info Button and Close Button
#~ INST_lyr : instruction layer
(BACKGR_lyr,
    CLOCK_lyr,
    CLOCK_HAND_lyr,
    PLANE_lyr,
    DEBUG_TXT_lyr,
    LEVEL_TIME_lyr,
    LEVEL_BAR_lyr,
    LEVEL_BAR_CHK_lyr,
    MSG_lyr,
    CTRL_BTN_lyr,
    INST_lyr
    ) = [p for p in range(0, 11)]


class DebugGame():
    def __init__(self):
        import os
        directory = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(directory):
            os.makedirs(directory)

        d = datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
        file_name = SUBJECT_NAME + "_" + d
        file_path = os.path.join(directory, file_name)

        self.f = open(file_path, 'w')

    def log(self, t1, t2):
        print t1, " -- ", t2
        self.f.write(t2)

    def close(self):
        self.f.close()

class Avioncito():
    # Este juego es equivalente al test de Coraz'on-Flor de Adelle Diamond.


    def __init__(self):
        if LOG:
            self.api = Fw_API()
        else:
            self.api = DebugGame()

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.level = Level()

        self.background = pygame.sprite.DirtySprite()
        self.background.image = pygame.image.load(
                            "images/fondo" + str(Properties.SCREEN_RES[0])
                            + "x" + str(Properties.SCREEN_RES[1]) + ".png")
        self.background.rect = self.background.image.get_rect()

        self.event_handler = EventHandler()
        self.keyboard_handler = Event()

        self.sprites_group = pygame.sprite.LayeredDirty()
        self.clickeableGroup = pygame.sprite.Group()

        self.sprites_group.add(self.background, layer=BACKGR_lyr)

        self.clock_hand = ClockHand()
        self.sprites_group.add(self.clock_hand, layer=CLOCK_HAND_lyr)

        c = Clock()
        c.rect.x = self.screen.get_rect().centerx - c.rect.width / 2
        c.rect.y = self.screen.get_rect().centery - c.rect.height / 2

        self.sprites_group.add(c, layer=CLOCK_lyr)

        self.log("INIT ", "INICIANDO JUEGO")

        self.shadow = pygame.sprite.DirtySprite()
        self.shadow.image = pygame.Surface(self.screen.get_size(),
                                           pygame.SRCALPHA)  # per-pixel alpha
        self.shadow.image.fill((0, 50, 150, 180))
        self.shadow.rect = self.screen.get_rect()
        self.shadow.visible = 0

        self.levelbar = LevelBar(self.level)
        self.sprites_group.add(self.levelbar.bar, layer=LEVEL_BAR_lyr)

        self.leveltime = LevelTime(self.level)
        self.sprites_group.add(self.leveltime, layer=LEVEL_TIME_lyr)

        self.sprites_group.add(self.levelbar.check, layer=LEVEL_BAR_CHK_lyr)

        self.sprites_group.add(self.shadow, layer=MSG_lyr)

        self.info_button = InfoButton(self.show_instructions)
        self.sprites_group.add(self.info_button, layer=CTRL_BTN_lyr)
        self.clickeableGroup.add(self.info_button)

        self.close_button = CloseButton(self.terminar_juego)
        self.sprites_group.add(self.close_button, layer=CTRL_BTN_lyr)
        self.clickeableGroup.add(self.close_button)

        self.instructions_window = Instruction()
        self.sprites_group.add(self.instructions_window, layer=INST_lyr)

        self.state = State()

    def sprites_clicked(self, _):
        for i in self.clickeableGroup:
            i.clicked(mouse.get_pos())

    def show_instructions(self):
        if self.state.show_instructions():
            self.instructions_window.visible = 1

    def log(self, prop, value):
        self.api.log("AVIONCITO",
                     datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")
                     + prop + value + "\n")

    def log_new_game(self):
        self.log("NEW ", "*****************")

    def log_plane(self, kind):
        self.log("PLANE_KIND ", json.dumps(kind))

    def log_plane_pos(self, pos):
        self.log("PLANE_POS ", json.dumps(pos))

    def log_res(self, res, time):
        self.log("RES ", json.dumps(res) + " " + json.dumps(time))

    def terminar_juego(self, ev=None):
        self.running = False

    def set_events(self):
        suscribir_tecla = self.keyboard_handler.suscribe

        self.event_handler.suscribe(pygame.QUIT, self.terminar_juego)
        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN,
                                    self.sprites_clicked)
        self.event_handler.suscribe(pygame.KEYDOWN,
                        lambda ev: self.keyboard_handler.dispatch(ev.key, ev))

        suscribir_tecla(pygame.K_ESCAPE, self.terminar_juego)
        suscribir_tecla(pygame.K_SPACE, lambda ev: self.restart_game())
        suscribir_tecla(pygame.K_a, lambda ev: self.plane_left())
        suscribir_tecla(pygame.K_l, lambda ev: self.plane_right())

    def plane_left(self):
        if self.plane is not None:
            res = self.plane.plane_left()
            self.eval_result(res)

    def plane_right(self):
        if self.plane is not None:
            res = self.plane.plane_right()
            self.eval_result(res)

    def set_info_status(self):
        self.log("Status ",
                        " - Checkpoint: " + str(self.level.checkpoint))

    def refresh_game_indicators(self):
        self.set_info_status()
        self.levelbar.make_checkpoint()
        self.leveltime.refresh()

    def restart_game(self):
        if self.state.is_initial():
            self.instructions_window.visible = 0
            self.level.initial_values()
            self.refresh_game_indicators()
            self.clock_hand.start()

            self.ticks = 0
            self.plane_ticks = 50
            self.answered = False
            self.state.go_next()

        elif self.state.is_pause():
            self.instructions_window.visible = 0
            self.state.go_next()

        elif self.state.is_inst_lost():
            self.instructions_window.visible = 0
            self.state.go_next()
        elif self.state.is_lost() and False:
            self.level.initial_values()
            self.refresh_game_indicators()
            self.clock_hand.start()

            self.ticks = 0
            self.plane_ticks = 50
            self.answered = False
            self.state.go_next()
            self.hide_messages()

    def hide_messages(self):
        for s in self.sprites_group.get_sprites_from_layer(MSG_lyr):
            s.visible = 0
            s.dirty = 0

    def eval_result(self, res):
        self.clock_hand.stop()
        current_checkpoint = self.level.checkpoint
        if not self.state.is_playing():
            return

        if not self.answered:
            if res is None:
                self.level.wrong_answer()
                self.log_res("NO ANSW ", time.time()
                             - self.clock_hand.init_time)
            elif res:
                self.level.correct_answer()
                self.log_res("CORRECT ", time.time()
                             - self.clock_hand.init_time)

            else:
                self.level.wrong_answer()
                self.log_res("WRONG ", time.time() - self.clock_hand.init_time)
            self.shadow.visible = 1
            self.shadow.dirty = 1

            self.answered = True
            self.plane_ticks = 0

            self.refresh_game_indicators()

            if (current_checkpoint != self.level.checkpoint and
                        self.level.checkpoint < len(self.level.level_order)):
                self.show_instructions()

        if self.level.is_won():
            print "ganaste"
            self.sprites_group.add(Message("GANASTE", "ESC PARA SALIR"),
                                   layer=MSG_lyr)
            self.state.lost()

    def delete_current_plane(self):
        self.sprites_group.remove(self.plane)
        self.plane = None
        self.answered = False

    def plane_builder(self):
        p = self.level.next_trial()

        self.plane = p()
        self.plane.rect.center = choice(Properties.positions)
        self.log_plane(self.plane.kind)
        self.log_plane_pos(self.plane.rect.center)
        
        print self.plane.rect.center

        self.sprites_group.add(self.plane, layer=PLANE_lyr)

        self.clock_hand.start()

    def run(self):
        #~ import pdb; pdb.set_trace()
        self.running = True
        self.set_events()
        self.mainLoop()

    def mainLoop(self):
        print "MainLoop"

        pygame.display.flip()
        self.plane = None

        while self.running:
            self.clock.tick(10)
            #while gtk.events_pending():
            #    gtk.main_iteration()

            #1) Procesar acciones del jugador
            self.event_handler.handle()

            if self.state.is_playing():
                if self.level.is_timed_level():
                    res = self.clock_hand.tic()
                else:
                    res = True
                self.plane_ticks += 1

                if not res:
                    self.eval_result(None)

                if self.answered and self.plane_ticks > 5:  # ANDRE
                    self.delete_current_plane()

                #if self.plane_ticks > 10 and self.plane is None:
                if self.plane is None:
                    self.plane_builder()
                    self.plane_ticks = 0

                    self.hide_messages()

            self.sprites_group.draw(self.screen)

            pygame.display.flip()

        self.api.close()


def main():
    game = Avioncito()
    game.run()
    pygame.quit()

if __name__ == '__main__':
    main()
