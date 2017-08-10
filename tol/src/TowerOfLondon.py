import pygame
import inc.Properties as Properties
import inc.Event as Event
import inc.EventHandler as EventHandler
import inc.State as State
# import inc.pytweener as TW

import datetime
import json
from random import randrange, choice

from inc.StickSprite import StickSprite
from inc.DiskSprite import DiskSprite
from inc.Text import Text, TextLevel
from inc.ImageMessage import *
from inc.Instruction import *
from inc.ExpRunner import *
from inc.Trial import *


import inc.distance

(BACKGR_lyr, STICK_lyr, FLOOR_lyr, GOAL_lyr,
    LEVEL_SEL_lyr, LEVEL_BAR_lyr, LEVEL_BAR_CHK_lyr,
    MSG_lyr, DISKS_lyr, CTRL_BTN_lyr,  INST_lyr, FEED_lyr
    ) = [ p for p in range(0,12) ]

EXPERIMENT_MODE, FREE_MODE = [ p for p in range(0,2) ]
INTERACTIVE, PASSIVE = [ p for p in range(0,2) ]

# SUBJECT_NAME = raw_input('Nombre: ')
SUBJECT_NAME = 'Nombre: '

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

        self.log_headers()

    def log_headers(self):

        str_store = ["KIND_OF_LOG","Date","trial_id","col1", "col2","col3","col4","col5","col6","col7","col8"]
        self.write_down(str_store)

        str_store = ["CLICK","Date","trial_id","box_clicked_num",
            "click_num","box_name","expected_box_name","time","correct","x","y"]
        self.write_down(str_store)

        str_store = ["RESULT","Date","trial_id","was_correct","number_of_box_clicked",
            "number_of_clicks", "expected_sequence", "result_sequence"]
        self.write_down(str_store)

        str_store = ["TRIAL START","Date","trial_id","sequence", "Feedback"]
        self.write_down(str_store)


    def log_click(self, trial_id, box_clicked_num, click_num, box_name, expected_box_name, time, correct, x, y):
        str_store = []
        str_store.append("CLICK")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
        str_store.append(str(trial_id))
        str_store.append(str(box_clicked_num))
        str_store.append(str(click_num))
        str_store.append(str(box_name))
        str_store.append(str(expected_box_name))
        str_store.append(str(time))
        str_store.append(str(correct))
        str_store.append(str(x))
        str_store.append(str(y))

        self.write_down(str_store)

    def log_trial_result(self, trial_id, correct, box_clicked_num,
                number_of_clicks, expected_sequence, result_sequence):
        str_store = []
        str_store.append("RESULT")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
        str_store.append(str(trial_id))
        str_store.append(str(correct))
        str_store.append(str(box_clicked_num))
        str_store.append(str(number_of_clicks))
        str_store.append(str(expected_sequence))
        str_store.append(str(result_sequence))

        self.write_down(str_store)

    def log_trial_start(self, trial_id, sequence, feedback):
        str_store = []
        str_store.append("TRIAL START")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))
        str_store.append(str(trial_id))
        str_store.append(str(sequence))
        str_store.append(str(feedback))

        self.write_down(str_store)

    def log_invalid_press(self):
        str_store = []
        str_store.append("INVALID PRESS")
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))

        self.write_down(str_store)

    def log_message(self, message):
        str_store = []
        str_store.append(message.upper())
        str_store.append(str(datetime.datetime.today().strftime("[%Y-%m-%d %H.%M.%S] ")))

        self.write_down(str_store)

    def write_down(self, arr):
        str_store = ";".join(arr)
        str_store = str_store + ";\n"

        self.f.write(str_store)

    def close(self):
        self.f.close()


class TowerOfLondon():

    def __init__(self, experiment):
        self.logger = FileLogger()
        self.experiment = experiment
        self.mode = EXPERIMENT_MODE

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.event_handler = EventHandler.EventHandler()
        self.keyboard_handler = Event.Event()

        self.sprites_group = pygame.sprite.LayeredDirty()

        self.background = pygame.sprite.DirtySprite()
        self.background.image = pygame.surface.Surface(Properties.SCREEN_RES)
        self.background.image.fill([240,240,240])
        self.background.rect = self.background.image.get_rect()
        self.sprites_group.add(self.background, layer=BACKGR_lyr)

        self.floor = pygame.sprite.DirtySprite()
        self.floor.image = pygame.surface.Surface((800, 100))
        self.floor.image.fill([0,200,0])
        self.floor.rect = self.floor.image.get_rect()
        self.floor.rect.bottom = Properties.SCREEN_RES[1]
        self.sprites_group.add(self.floor, layer=FLOOR_lyr)


        self.feedback_ok = Feedback()
        self.feedback_no = Feedback(False)
        self.sprites_group.add(self.feedback_ok, layer=FEED_lyr)
        self.sprites_group.add(self.feedback_no, layer=FEED_lyr)

        self.state = State.State()
        st = self.state

        self.trial = Trial(self.logger, self.change_to_active_mode,
                None,
                {"ok": self.feedback_ok.show, "no": self.feedback_no.show,
                "off": (lambda: [self.feedback_ok.hide(), self.feedback_no.hide()])})

        # self.state.show()

        self.sprites_group.add(StickSprite(st.sticks[1]), layer=STICK_lyr)
        self.sprites_group.add(StickSprite(st.sticks[2]), layer=STICK_lyr)
        self.sprites_group.add(StickSprite(st.sticks[3]), layer=STICK_lyr)


        # print "R: ", st.get_disk_position(State.R)
        # print "G: ", st.get_disk_position(State.G)
        # print "B: ", st.get_disk_position(State.B)

        self.sprites_group.add(DiskSprite(st.get_disk(State.B),st.get_disk_position(State.B)), layer=DISKS_lyr)
        self.sprites_group.add(DiskSprite(st.get_disk(State.G),st.get_disk_position(State.G)), layer=DISKS_lyr)
        self.sprites_group.add(DiskSprite(st.get_disk(State.R),st.get_disk_position(State.R)), layer=DISKS_lyr)

        self.goal = pygame.sprite.DirtySprite()
        # self.goalText = Text("Prueba")
        # self.stepsText = Text("Prueba")
        # self.statusText = Text("Prueba")
        self.sprites_group.add(self.goal, layer=GOAL_lyr)
        # self.sprites_group.add(self.goalText, layer=GOAL_lyr)
        # self.sprites_group.add(self.stepsText , layer=GOAL_lyr)
        # self.sprites_group.add(self.statusText, layer=GOAL_lyr)


        self.instruction =  Instruction()
        self.instruction.hide()
        self.sprites_group.add(self.instruction, layer=INST_lyr)

        self.msgs = {}
        self.msgs["done"] =  ImageDone()
        self.msgs["done"].set_callback((lambda: 1))
        for v in self.msgs.itervalues():
            self.sprites_group.add(v, layer=CTRL_BTN_lyr)

        self.exp_runner = ExpRunner(self.experiment,
            self.set_trial)
        self.exp_runner.end_test = self.end_game
        self.exp_runner.instruction = self.instruction
        self.exp_runner.next()

        # self.set_goal(randrange(36))

        self.clicked_sprite = None

        if self.mode == FREE_MODE:
            for i in range(1,8+1):
                self.sprites_group.add(TextLevel(i,self.set_board_distance), layer=LEVEL_SEL_lyr)

        self.change_to_active_mode(False)

    def change_to_active_mode(self, toActive=True):
        # self.change_background(toActive)
        if toActive:
            # print "To INTERACTIVE MODE"
            self.msgs["done"].show()
            self.moving_state = INTERACTIVE
            self.instruction.hide()
            self.goal.visible = True
        else:
            # print "To PASSIVE MODE"
            self.moving_state = PASSIVE
            self.msgs["done"].hide()
            self.instruction.show()
            self.goal.visible = False


    def set_events(self):
        suscribir_tecla = self.keyboard_handler.suscribe

        self.event_handler.suscribe(pygame.QUIT, self.end_game)

        self.event_handler.suscribe(pygame.MOUSEBUTTONDOWN, self.clicked)
        self.event_handler.suscribe(pygame.MOUSEMOTION, self.move_mouse)
        self.event_handler.suscribe(pygame.MOUSEBUTTONUP, self.unclicked)
        self.event_handler.suscribe(pygame.KEYDOWN, lambda ev: self.keyboard_handler.dispatch(ev.key, ev))

        suscribir_tecla(pygame.K_ESCAPE, self.end_game)

    def set_board_distance(self, distance=None):
        if distance is None:
            distance = randrange(8)+1

        l1 = randrange(len(inc.distance.dist))

        indexes = [i for i, x in enumerate(inc.distance.dist[l1]) if x == distance]

        l2 = choice(indexes)
        self.set_board(l1)
        self.set_goal(l2)

    def set_trial(self, source_num, target_num):
        self.set_board(source_num)
        self.set_goal(target_num)

    def set_board(self, board_num):
        self.state.set_board_number(board_num)
        # self.state.show()

    def set_goal(self, board_num):
        self.goal_num = board_num
        self.moves_num = 0

        d = inc.distance.dist[board_num][self.state.get_board_number()]

        # self.goalText.set_message("Sale en %d movidas" %(d,))

        self.goal.image = pygame.image.load("images/boards/%02d.png" %(board_num, ))
        self.goal.rect = self.goal.image.get_rect()
        self.goal.rect.topleft = Properties.goal_pos #(Properties.SCREEN_RES[0]-30,30)
        self.goal.dirty = 1
        (x,y) = self.goal.rect.bottomright
        # self.goalText.rect.center = Properties.goal_pos
        self.refresh_indicators()
        self.refresh_all_sprites()


    def refresh_indicators(self):
        # self.stepsText.set_message("Movidas: %d" %(self.moves_num,))
        # (x,y) = self.goalText.rect.bottomright
        # self.stepsText.rect.topright = (x,y)
        # (x,y) = self.stepsText.rect.bottomright

        # if self.state.get_board_number() == self.goal_num:
            # self.statusText.set_message("GANASTE")
        # else:
            # self.statusText.set_message("")
        # self.statusText.rect.topright = (x,y)
        pass

    def refresh_all_sprites(self):
        for i in self.sprites_group.get_sprites_from_layer(DISKS_lyr):
            i.set_stick_pos(self.state.get_disk_position(i.disk.num))
            i.dirty = 1

    def new_trial(self):
        self.set_board_distance()

    def clicked(self, res):
        (x, y) = pygame.mouse.get_pos()
        if self.moving_state == INTERACTIVE:
            for i in self.sprites_group.get_sprites_from_layer(DISKS_lyr):
                if (i.rect.collidepoint(x, y)):
                    r = i.click()

                    if r:
                        self.clicked_sprite = i

            for i in self.sprites_group.get_sprites_from_layer(CTRL_BTN_lyr):
                if (i.rect.collidepoint(x, y)):
                    i.click()

            if self.mode==FREE_MODE:
                for i in self.sprites_group.get_sprites_from_layer(LEVEL_SEL_lyr):
                    if (i.rect.collidepoint(x, y)):
                        i.click()
        elif self.moving_state == PASSIVE:
            self.change_to_active_mode()

    def move_mouse(self, res):
        if self.clicked_sprite is not None:
            self.clicked_sprite.set_position(pygame.mouse.get_pos())

    def unclicked(self, res):
        already_placed = False
        # import pdb; pdb.set_trace()
        if self.clicked_sprite is not None:
            for i in self.sprites_group.get_sprites_from_layer(STICK_lyr):
                if (i.rect.colliderect(self.clicked_sprite)):
                    # print "Left on Stick ", i.stick.num
                    if i.stick.not_full() and i.stick.num!=self.state.get_stick_of_disk(self.clicked_sprite.disk.num).num:
                        # print "There is room enough. Number of moves: ", self.moves_num
                        self.state.moveSP(self.clicked_sprite, i)
                        self.clicked_sprite = None
                        self.moves_num += 1
                        self.refresh_indicators()
                        if self.state.get_board_number() == self.goal_num:
                            print "GANASTE"
                        already_placed = True
                        return

            # if not already_placed:
            self.clicked_sprite.set_stick_pos()
            self.clicked_sprite = None


        (x, y) = pygame.mouse.get_pos()
        for i in self.sprites_group.get_sprites_from_layer(CTRL_BTN_lyr):
            if (i.rect.collidepoint(x, y)):
                i.release_click()




    def run(self):
        #~ import pdb; pdb.set_trace()
        self.running = True
        self.set_events()

        self.mainLoop()

    def end_game(self, ev=None):
        self.logger.log_message("end game")
        self.logger.close()
        self.running = False

    def mainLoop(self):
        # print "MainLoop"
        pygame.display.flip()

        while self.running:
            self.event_handler.handle()

#             dt = self.clock.tick(30)
            dt = self.clock.tick(60)
            self.trial.tic()
            #self.tweener.update(dt / 1000.0)

            self.sprites_group.draw(self.screen)
            pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_mode(Properties.SCREEN_RES)
    json_data=open("input.json").read()
    experiment = json.loads(json_data)


    game = TowerOfLondon(experiment)
    game.run()

    print "Saliendo"
    pygame.quit()

if __name__ == '__main__':
    main()
