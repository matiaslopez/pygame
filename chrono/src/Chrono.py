# -*- coding: utf-8 -*-
import pygame
from pygame import time
#import pygame._view
#from pygame.locals import *
from random import choice
import time

import json
import datetime

import inc.Properties as Properties

from inc.EventHandler import EventHandler
from inc.Event import Event
from inc.ExpRunner import *
from inc.Stimulus import *
from inc.Block import *
from inc.Feedback import *
#from inc.Message import *
from inc.ImageMessage import *
from inc.ImageMessageBar import *
from inc.Trial import *

SUBJECT_NAME = raw_input('Nombre: ')

pygame.init()
# pygame.display.set_mode(Properties.SCREEN_RES, pygame.FULLSCREEN)
pygame.display.set_mode(Properties.SCREEN_RES)

#~ BACKGR_lyr: Background
#~ STIM_lyr: Stimulus

(BACKGR_lyr,
    STIM_lyr,
    FEED_lyr,
    MSG_lyr,
    ) = [ p for p in range(0,4) ]


class FileLogger():

    def __init__(self):
        import os
        directory = os.path.join(os.getcwd(), 'logs')
        if not os.path.exists(directory):
            os.makedirs(directory)

        d = datetime.datetime.today().strftime("%Y-%m-%d_%H.%M.%S")
        file_name = SUBJECT_NAME + "_" + d + ".csv"
        file_path = os.path.join(directory, file_name)

        self.f = open(file_path, 'w')

        str_store = []
        str_store.append("Kind of Data")
        str_store.append("Date")
        str_store.append("Block")
        str_store.append("Stimulus Length")
        str_store.append("Subject Answer Time")

        self.write_down(str_store)

    def log_answer(self, block, stim_time, subj_ans):
        str_store = []
        str_store.append("ANSWER")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
        str_store.append(str(block))
        str_store.append(str(stim_time))
        str_store.append(str(subj_ans))

        self.write_down(str_store)

    def log_invalid_press(self):
        str_store = []
        str_store.append("INVALID PRESS")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))

        self.write_down(str_store)

    def write_down(self, arr):
        str_store = ";".join(arr)
        str_store = str_store + ";\n"

        self.f.write(str_store)

    def close(self):
        self.f.close()

class Chrono():
    def __init__(self, experiment):
        self.logger = FileLogger()

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.experiment = experiment
        # self.level = Level()

        self.event_handler = EventHandler()
        self.keyboard_handler = Event()

        self.sprites_group = pygame.sprite.LayeredDirty()

        self.msgs = {}

        self.msgs["welcome"] =  ImageMessage(str(0), "welcome.jpg")
        self.msgs["the_end"] =  ImageMessage(str(0), "theEnd.jpg")

        for v in self.msgs.itervalues():
            self.sprites_group.add(v, layer=MSG_lyr)

        self.trial = Trial(self.logger)
        self.block = Block(self.trial, self.msgs)
        self.exp_runner = ExpRunner(self.experiment, self.block, self.msgs, self.set_images)

        # self.log("INIT ", "INICIANDO JUEGO")

        # self.state = State()

    def set_images(self, block_num):
        # print "Set images"
        self.sprites_group.empty()

        self.background = ImageMessage(block_num, "background.jpg")
        self.background.show()

        self.stimulus = Stimulus(block_num)
        self.target_img = Stimulus(block_num, False)
        self.feed = Feedback(block_num)


        self.msgs["background"] =  ImageMessage(block_num, "background.jpg")
        self.msgs["op"] =  ImageMessage(block_num, "operator.jpg")
        self.msgs["feed"] =  ImageMessage(block_num, "feedback.jpg")
        self.msgs["subj"] =  ImageMessage(block_num, "subject.jpg")
        self.msgs["wait"] =  ImageMessageBar(block_num, "endTrial.jpg", self.feed)
        self.msgs["end_block"] =  ImageMessage(block_num, "endBlock.jpg")

        for v in self.msgs.itervalues():
            self.sprites_group.add(v, layer=MSG_lyr)

        self.sprites_group.add(self.background, layer=BACKGR_lyr)
        self.sprites_group.add(self.stimulus, layer=STIM_lyr)
        self.sprites_group.add(self.target_img, layer=STIM_lyr)
        self.sprites_group.add(self.feed.reference, layer=FEED_lyr)
        self.sprites_group.add(self.feed.slow, layer=FEED_lyr)
        self.sprites_group.add(self.feed.ok, layer=FEED_lyr)
        self.sprites_group.add(self.feed.quick, layer=FEED_lyr)

        self.trial.set_images(self.stimulus, self.target_img, self.feed)

    def set_events(self):
        key_suscribe = self.keyboard_handler.suscribe

        # self.event_handler.suscribe(pygame.QUIT, self.terminar_juego)
        # self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, self.sprites_clicked)
        self.event_handler.suscribe(pygame.KEYDOWN, lambda ev: self.keyboard_handler.dispatch(ev.key, ev))

        key_suscribe(pygame.K_ESCAPE, self.terminar_juego)
        # key_suscribe(pygame.K_SPACE, lambda ev: self.restart_game())
        # key_suscribe(pygame.K_q, self.start_stimulus)
        key_suscribe(pygame.K_SPACE, self.report_answ)

        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, lambda ev: self.block.next_by_usr())
        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, lambda ev: self.exp_runner.next_block())
        # key_suscribe(pygame.K_a, lambda ev: self.block.next_by_usr())
        # key_suscribe(pygame.K_a, lambda ev: self.exp_runner.next_block())

    def terminar_juego(self, ev=None):
        self.logger.close()
        self.running = False

    def report_answ(self, ev=None):
        if not self.trial.usr_answer():
            self.logger.log_invalid_press()


    def run(self):
        #~ import pdb; pdb.set_trace()
        self.running = True
        self.set_events()
        self.mainLoop()
        self.current_block = 0

    def trial_handle_next(self):
        pass

    def mainLoop(self):
        # print "MainLoop"

        pygame.display.flip()
        self.playing = None

        while self.running:
            self.clock.tick(10)

            self.event_handler.handle()
            self.trial.tic()
            self.block.tic()
            self.sprites_group.draw(self.screen)

            pygame.display.flip()

def main():
    json_data=open("input.json").read()
    experiment = json.loads(json_data)
    # print experiment
    game = Chrono(experiment)
    game.run()

if __name__ == '__main__':
    main()
