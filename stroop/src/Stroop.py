import pygame
import inc.Properties as Properties
import inc.Event as Event
import inc.EventHandler as EventHandler
# import inc.State as State
from inc.Logger import FileLogger
# import inc.pytweener as TW

import datetime
import json
from random import randrange, choice

from inc.ImageMessage import *
from inc.Diagram import *
from inc.ExpRunner import *
from inc.Trial import *
from inc.Block import *
from inc.Stimulus import *

(BACKGR_lyr, SCREENSHOTS_lyr, DIAGRAM_lyr,
    STIM_lyr,
    MSG_lyr, CTRL_BTN_lyr,  INST_lyr, FEED_lyr, ANSW_BTN_lyr
    ) = [ p for p in range(0,9) ]

INTERACTIVE, PASSIVE, FEEDBACK = [ p for p in range(0,3) ]

SUBJECT_NAME = raw_input('Nombre: ')
BACKGROUND_PROFILE = raw_input('Perfil de fondo (1, 2): ')
STIM_PROFILE = raw_input('Perfil de piezas (1, 2): ')


# SUBJECT_NAME = "Q"
# BACKGROUND_PROFILE = "1"
# STIM_PROFILE = "2"


class Stroop():

    def __init__(self, experiment_data):
        self.logger = FileLogger(SUBJECT_NAME)
        self.experiment_data = experiment_data
        SCREEN_RES = (int(experiment_data["screen_res"]["x"]), int(experiment_data["screen_res"]["y"]))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.event_handler = EventHandler.EventHandler()
        self.keyboard_handler = Event.Event()

        self.sprites_group = pygame.sprite.LayeredDirty()

        # self.background = pygame.sprite.DirtySprite()
        self.background =  ImageMessage("background.png", BACKGROUND_PROFILE)
        self.background.scale(SCREEN_RES[0], SCREEN_RES[1])
        self.background.show()
        self.sprites_group.add(self.background, layer=BACKGR_lyr)

        self.msgs = {}

        self.msgs["welcome"] =  ImageMessage("welcome.png", BACKGROUND_PROFILE)
        self.msgs["the_end"] =  ImageMessage("theEnd.png", BACKGROUND_PROFILE)
        # self.msgs["background"] =  ImageMessage("background.png")
        self.msgs["op"] =  ImageMessage("operator.png", BACKGROUND_PROFILE)
        self.msgs["feed"] =  ImageMessage("feedback.png", BACKGROUND_PROFILE)
        self.msgs["subj"] =  ImageMessage("subject.png", BACKGROUND_PROFILE)
        self.msgs["end_block"] =  ImageMessage("endBlock.png", BACKGROUND_PROFILE)

        for v in self.msgs.itervalues():
            v.scale(SCREEN_RES[0], SCREEN_RES[1])
            self.sprites_group.add(v, layer=MSG_lyr)

        self.feedback_ok = Feedback()
        self.feedback_no = Feedback(False)
        self.sprites_group.add(self.feedback_ok, layer=FEED_lyr)
        self.sprites_group.add(self.feedback_no, layer=FEED_lyr)


        # self.state = State.State()
        # st = self.state

        # self.trial = Trial(self.logger, self.show_messages,
        #         None,
        #         {"ok": self.feedback_ok.show, "no": self.feedback_no.show,
        #         "off": (lambda: [self.feedback_ok.hide(), self.feedback_no.hide()])},
        #         self)


        # self.add_elements(experiment_data["trials"]["2"][1], 0)
        # self.add_elements(experiment_data["trials"]["2"][2], 2)
        self.btns = {}
        self.btns["left"] =  ImageButton(0)
        self.btns["right"] =  ImageButton(1)
        for v in self.btns.itervalues():
            self.sprites_group.add(v, layer=ANSW_BTN_lyr)

        # self.btns["left"].set_callback(lambda: self.exp_runner.check_answer([
                    # c for i in xrange(len(self.palettes)) for c in self.palettes[i].get_selected() ]))


        self.trial = Trial(self.logger, self.change_to_active_mode)
        self.trial.feedback[1] = self.feedback_ok
        self.trial.feedback[0] = self.feedback_no
        self.block = Block(self.trial, self.msgs)

        # self.exp_runner = ExpRunner(self.experiment_data, self.add_elements, self.add_screenshot)
        self.exp_runner = ExpRunner(self.experiment_data, self.block,
                    self.msgs, self.set_images)

        self.exp_runner.end_test = self.end_game

        self.btns["left"].set_callback(self.trial.usr_answer)
        self.btns["right"].set_callback(self.trial.usr_answer)


        # self.exp_runner.instruction = self.instruction
        # self.exp_runner.next()
        self.change_to_active_mode(False)
        # self.msgs["welcome"].show()
        self.clicked_sprite = None



    def change_to_active_mode(self, toActive=True):
        # self.change_background(toActive)
        if toActive:
            self.state = INTERACTIVE
            self.btns["left"].show()
            self.btns["right"].show()
        else:
            self.state = PASSIVE
            self.btns["left"].hide()
            self.btns["right"].hide()



    def set_images(self, block_num):
        # print "Set images"
        self.sprites_group.empty()

        self.stimulus = Stimulus(STIM_PROFILE)
        self.feed = Feedback()

        self.sprites_group.add(self.feedback_ok, layer=FEED_lyr)
        self.sprites_group.add(self.feedback_no, layer=FEED_lyr)


        # self.msgs["wait"] =  ImageMessageBar("endTrial.png", self.feed)


        for v in self.msgs.itervalues():
            self.sprites_group.add(v, layer=MSG_lyr)

        for v in self.btns.itervalues():
            self.sprites_group.add(v, layer=ANSW_BTN_lyr)

        self.sprites_group.add(self.background, layer=BACKGR_lyr)
        self.sprites_group.add(self.stimulus, layer=STIM_lyr)
        # self.sprites_group.add(self.target_img, layer=STIM_lyr)
        # self.sprites_group.add(self.feed.slow, layer=FEED_lyr)
        # self.sprites_group.add(self.feed.ok, layer=FEED_lyr)
        # self.sprites_group.add(self.feed.quick, layer=FEED_lyr)

        self.trial.set_images(self.stimulus, self.feed)



    def remove_elements(self):
        self.sprites_group.remove_sprites_of_layer(DIAGRAM_lyr)
        self.sprites_group.remove_sprites_of_layer(SCREENSHOTS_lyr)
        self.background.dirty = 1
        self.msgs["done"].hide()

    def add_elements(self, diags):
        self.remove_elements()
        self.msgs["done"].show()
        self.diagrams = []
        self.palettes = []
        num_whites = 0
        for row, diags in diags.iteritems():
            for (n,i) in enumerate(diags):
                d = Diagram(layout=i[0], colors=i[1:], position=(n,row, len(diags)))
                num_whites += d.get_whites()
                self.diagrams.append(d)
                self.sprites_group.add(d, layer=DIAGRAM_lyr)

        for i in xrange(num_whites):
            p = ColorPalette(num=i+1, num_palettes=num_whites)
            self.palettes.append(p)
            self.sprites_group.add(p , layer=DIAGRAM_lyr)


    def add_screenshot(self, filename):
        self.remove_elements()
        self.sprites_group.add(Screenshot(filename), layer=DIAGRAM_lyr)
        # self.show_messages(False)

    def show_messages(self, toActive=True, info_or_feedback=2):
        # self.change_background(toActive)
        # print "To PASSIVE MODE"
        for i in [GOAL_lyr, DISKS_lyr, CTRL_BTN_lyr,FEED_lyr, INST_lyr]:
            for sp in self.sprites_group.get_sprites_from_layer(i):
                sp.hide()
        if toActive:
            # print "To INTERACTIVE MODE"
            # self.msgs["done"].show()
            self.moving_state = INTERACTIVE
            # self.instruction.hide()
            # self.goal.visible = True
            for i in [GOAL_lyr, DISKS_lyr, CTRL_BTN_lyr]:
                for sp in self.sprites_group.get_sprites_from_layer(i):
                    sp.show()
        else:
            if info_or_feedback==2:
                self.moving_state = PASSIVE
                self.instruction.show()
            else:
                self.moving_state = FEEDBACK
                if info_or_feedback==1:
                    self.feedback_ok.show()
                elif info_or_feedback==0:
                    self.feedback_no.show()


    def set_events(self):
        suscribir_tecla = self.keyboard_handler.suscribe

        self.event_handler.suscribe(pygame.QUIT, self.end_game)

        # self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, self.clicked)
        self.event_handler.suscribe(pygame.MOUSEMOTION, self.move_mouse)
        # self.event_handler.suscribe(pygame.MOUSEBUTTONUP, self.unclicked)
        self.event_handler.suscribe(pygame.KEYDOWN, lambda ev: self.keyboard_handler.dispatch(ev.key, ev))

        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, lambda ev: self.block.next_by_usr())
        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, lambda ev: self.exp_runner.next_block())

        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, self.click)
        self.event_handler.suscribe(pygame.MOUSEBUTTONUP, self.release_click)


        suscribir_tecla(pygame.K_ESCAPE, self.end_game)
        suscribir_tecla(pygame.K_LEFT, self.prev)


    def click(self, res):
        (x, y) = pygame.mouse.get_pos()

        if self.state == INTERACTIVE:
            # print (x,y, len(self.sprites_group.get_sprites_from_layer(ANSW_BTN_lyr)))
            for i in self.sprites_group.get_sprites_from_layer(ANSW_BTN_lyr):
                if (i.rect.collidepoint(x, y)):
                    self.clicked_sprite = i
                    # print "Click box ", i.box_name
                    i.click()

    def release_click(self, res):
        (x, y) = pygame.mouse.get_pos()

        if self.state == INTERACTIVE and self.clicked_sprite is not None:
            for i in self.sprites_group.get_sprites_from_layer(ANSW_BTN_lyr):
                if (i.rect.collidepoint(x, y)):
                    # print "Click button "
                    i.release_click()
            self.clicked_sprite = None


    # def clicked(self, res):
    #     (x, y) = pygame.mouse.get_pos()
    #     if self.exp_runner.clicked():
    #         for i in self.sprites_group.get_sprites_from_layer(DIAGRAM_lyr) + self.sprites_group.get_sprites_from_layer(CTRL_BTN_lyr):
    #             if (i.rect.collidepoint(x, y)):
    #                 # print "Clicked", (x, y)
    #                 i.click()
    #     # else:
    #     #     self.exp_runner.next()



    def move_mouse(self, res):
        (x, y) = pygame.mouse.get_pos()
        if self.clicked_sprite is not None:
            if not self.clicked_sprite.rect.collidepoint(x, y):
                self.clicked_sprite.un_click()
                self.clicked_sprite = None


    # def unclicked(self, res):
    #     (x, y) = pygame.mouse.get_pos()
    #     if self.exp_runner.clicked():
    #         for i in self.sprites_group.get_sprites_from_layer(CTRL_BTN_lyr):
    #             if (i.rect.collidepoint(x, y)):
    #                 i.release_click()
    #     else:
    #         self.exp_runner.next()

        # if self.clicked_sprite is not None:
        #     qq = self.clicked_sprite
        #     for i in self.sprites_group.get_sprites_from_layer(STICK_lyr):
        #         if (i.rect.colliderect(self.clicked_sprite)):
        #             # print "Left on Stick ", i.stick.num
        #             if i.stick.not_full() and i.stick.num!=self.state.get_stick_of_disk(self.clicked_sprite.disk.num).num:
        #                 # print "There is room enough. Number of moves: ", self.moves_num
        #                 self.state.moveSP(self.clicked_sprite, i)
        #                 self.clicked_sprite = None
        #                 self.moves_num += 1
        #                 self.sequence_boards.append(self.state.get_board_number())
        #                 self.refresh_indicators()
        #                 # if self.state.get_board_number() == self.goal_num:
        #                     # print "GANASTE"
        #                 already_placed = True
        #                 self.logger.log_release_disk(self.exp_runner.trial.trial_name,
        #                                         self.trial.current_trial["source"],
        #                                         self.trial.current_trial["target"],
        #                                         self.state.get_board_number(),
        #                                         self.trial.tol.moves_num,
        #                                         qq.disk.num,
        #                                         True
        #                                         )
        #                 return

        #     # if not already_placed:
        #     self.clicked_sprite.set_stick_pos()
        #     self.clicked_sprite = None
        #     self.logger.log_release_disk(self.exp_runner.trial.trial_name,
        #                             self.trial.current_trial["source"],
        #                             self.trial.current_trial["target"],
        #                             self.state.get_board_number(),
        #                             self.trial.tol.moves_num,
        #                             qq.disk.num,
        #                             False
        #                             )

        # if self.moving_state == INTERACTIVE:
        #     (x, y) = pygame.mouse.get_pos()
        #     for i in self.sprites_group.get_sprites_from_layer(CTRL_BTN_lyr):
        #         if (i.rect.collidepoint(x, y)):
        #             i.release_click()
        # elif self.moving_state == PASSIVE:
        #     self.show_messages()
        # elif self.moving_state == FEEDBACK:
        #     self.show_messages(False)

    def run(self):
        #~ import pdb; pdb.set_trace()
        self.running = True
        self.set_events()

        self.mainLoop()

    def prev(self, ev=None):
        self.exp_runner.prev()
        # self.logger.close()
        # self.running = False

    def end_game(self, ev=None):
        self.logger.log_message("end game")
        self.logger.close()
        self.running = False

    def mainLoop(self):
        # print "MainLoop"
        pygame.display.flip()
        # pygame.image.save(out,fname+".tga")

        while self.running:
            self.event_handler.handle()

            dt = self.clock.tick(10)
            self.trial.tic()
            self.block.tic()

            self.sprites_group.draw(self.screen)
            pygame.display.flip()

        # pygame.image.save(pygame.display.get_surface(), "screenshot.png")

def main():
    json_data=open("input.json").read()
    experiment_data = json.loads(json_data)
    SCREEN_RES = (int(experiment_data["screen_res"]["x"]), int(experiment_data["screen_res"]["y"]))

    pygame.init()
    pygame.display.set_mode(SCREEN_RES)


    game = Stroop(experiment_data)
    game.run()

    print "Saliendo"
    pygame.quit()

if __name__ == '__main__':
    main()
