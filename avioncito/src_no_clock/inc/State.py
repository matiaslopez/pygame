# -*- coding: utf-8 -*-


INIT, PAUSE, LOST, PLAYING, INST_LOST = [p for p in range(5)]


class State():

    def __init__(self):
        self.state = INIT

    def show_instructions(self):
        if self.state == LOST:
            self.state = INST_LOST
            return True

        if self.state == PLAYING:
            self.state = PAUSE
            return True

        return False

    def is_initial(self):
        return self.state == INIT

    def is_pause(self):
        return self.state == PAUSE

    def is_inst_lost(self):
        return self.state == INST_LOST

    def is_lost(self):
        return self.state == LOST

    def is_playing(self):
        return self.state == PLAYING

    def go_next(self):
        if self.state == INIT or self.state == PAUSE: # or self.state == LOST:
            self.state = PLAYING

        if self.state == INST_LOST:
            self.state = LOST

    def lost(self):
        self.state = LOST
