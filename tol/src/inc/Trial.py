# -*- coding: utf-8 -*-
#!/usr/bin/python

import pygame
import time

import Properties

INIT, PLAY, FEEDBACK, END = [ p for p in range(4) ]

current_milli_time = lambda: int(round(time.time() * 1000))


class Trial():

    def __init__(self, logger, show_messages,
            handle_end,feedback_handler, tol):
        self.state = None
        self.handle_end = None
        self.logger = logger
        self.show_messages = show_messages
        self.handle_end = handle_end
        self.feedback_handler = None #feedback_handler
        self.tol = tol
        self.current_trial = None

    def start(self, trial_name):
        # print "Trial.start -- "
        self.state = INIT
        self.trial_name  = trial_name
        self.init_time = current_milli_time()
        self.logger.log_trial_start(self.trial_name,
                self.current_trial["source"],
                self.current_trial["target"],
                self.current_trial["feedback"],
                self.current_trial["expected_moves"],
                )
        # self.logger.

    def set_trial(self, source_num, target_num, feedback, expected_moves):
        self.current_trial = {"source": source_num,
                                "target": target_num,
                                "feedback": feedback,
                                "expected_moves": expected_moves}
        # print self.current_trial

        self.tol.set_board(source_num)
        self.tol.set_goal(target_num)

    def check_answer(self):
        # print "--- usr answer - boxclicked: ", self.box_clicked_num, " - current box: ", box_name
        # print " - expected: ", self.sequence[self.box_clicked_num]
        # print self.tol.state.get_board_number(), self.current_trial
        # print self.state
        delta = current_milli_time() - self.init_time
        if (self.tol.state.get_board_number()==self.current_trial["target"] and
            self.tol.moves_num==self.current_trial["expected_moves"]):
            correct = True
        else:
            correct = False

        self.logger.log_trial_result(self.trial_name,
                correct,
                self.tol.moves_num,
                self.current_trial["expected_moves"],
                self.tol.sequence_boards)

        self.tol.show_messages(False, int(correct) if self.current_trial["feedback"] else 2)

        self.tol.exp_runner.next_trial(correct, self.current_trial["feedback"])
        return correct

    # def next_by_usr(self):
    #     if self.state == END:
    #         self.next()

    # def next(self):
    #     self.init_time = current_milli_time()
    #     # print "leaving ", self.state,
    #     if self.state == INIT:
    #         self.state = STIM
    #         self.stim_index = 0
    #     elif self.state == STIM:
    #         # self.state = WAIT
    #     # elif self.state == WAIT:
    #         self.box_clicked_num = 0
    #         self.click_num = 0
    #         self.state = ANSW
    #         self.show_messages(True)
    #     elif self.state == ANSW:
    #         self.show_messages(False)
    #         if self.feedback:
    #             # print "Showing feedback"
    #             self.state = FEEDBACK
    #             correct = self.correct_answer & (self.box_clicked_num == len(self.sequence))
    #             if correct:
    #                 self.feedback_handler["ok"]()
    #             else:
    #                 self.feedback_handler["no"]()
    #         else:
    #             self.state = END
    #     elif self.state == FEEDBACK:
    #         self.feedback_handler["off"]()
    #         self.state = END

    #     if self.state == END and self.handle_end is not None:
    #         # print "Summary, self.correct_answer", self.correct_answer
    #         # print "All clicked: ", self.box_clicked_num == len(self.sequence)
    #         correct = self.correct_answer & (self.box_clicked_num == len(self.sequence))
    #         self.logger.log_trial_result(self.trial_name, "CORRECT" if correct else "INCORRECT", self.box_clicked_num,
    #             self.click_num, "".join(self.sequence), self.current_answer)
    #         self.handle_end(correct, self.feedback)
    #     # print " - new state: ", self.state


    # def hide(self):
    #     self.stim.hide()
    #     self.target_img.hide()
    #     self.feed.hide()

    # def tic(self):
    #     if self.running:
    #         if self.state == INIT:
    #             if self.init_time + self.properties["tprev"]  < current_milli_time():
    #                 self.next()
    #         elif self.state == STIM:
    #             appear_time = self.stim_index * (self.properties["tstim"] + self.properties["tinterstim"])
    #             if self.init_time + appear_time < current_milli_time():
    #                 if self.stim_index >= len(self.sequence):
    #                     self.next()
    #                     # print "END of STIM"
    #                 else:
    #                     current_box_id = self.sequence[self.stim_index]
    #                     self.boxes[current_box_id].click(self.properties["tstim"], self.unsuscribe_box)
    #                     self.suscribe_box(self.boxes[current_box_id])
    #                     self.stim_index += 1
    #         elif self.state == WAIT:
    #             if self.init_time + self.properties["tprev"]  < current_milli_time():
    #                 self.next()
    #         elif self.state == FEEDBACK:
    #             if self.init_time + self.properties["tfeedback"]  < current_milli_time():
    #                 self.next()
    #         # elif self.state == ANSW:
    #             # if (self.init_time + self.properties["timeoutextra"] +
    #                 # self.properties["timeoutperanswer"] * len(self.sequence)) < current_milli_time():
    #                 # self.next()
    #         # elif self.state == END:
    #             # if self.init_time + self.properties["tprev"]  < current_milli_time():
    #                 # self.next()

