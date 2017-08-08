import pygame
import inc.Properties as Properties
import inc.Event as Event
import inc.EventHandler as EventHandler
import inc.State as State
import inc.pytweener as TW

from random import randrange, choice

from inc.StickSprite import StickSprite
from inc.DiskSprite import DiskSprite
from inc.Text import Text, TextLevel

import inc.distance

BACKGR_lyr, STICK_lyr, GOAL_lyr, LEVEL_SEL_lyr, LEVEL_BAR_lyr, LEVEL_BAR_CHK_lyr, MSG_lyr, CTRL_BTN_lyr, DISKS_lyr = [ p for p in range(0,9) ]


class TowerOfLondon():

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()

        self.event_handler = EventHandler.EventHandler()
        self.keyboard_handler = Event.Event()

        self.sprites_group = pygame.sprite.LayeredDirty()

        self.background = pygame.sprite.DirtySprite()
        # self.background.image = pygame.image.load("images/fondo"  + str(Properties.SCREEN_RES[0]) + "x"
                                                            # + str(Properties.SCREEN_RES[1]) + ".png")
        self.background.image = pygame.image.load("images/fondo1200x900.png")
        self.background.rect = self.background.image.get_rect()
        self.sprites_group.add(self.background, layer=BACKGR_lyr)


        self.state = State.State()
        st = self.state

        self.state.show()

        self.sprites_group.add(StickSprite(st.sticks[1]), layer=STICK_lyr)
        self.sprites_group.add(StickSprite(st.sticks[2]), layer=STICK_lyr)
        self.sprites_group.add(StickSprite(st.sticks[3]), layer=STICK_lyr)


        print "R: ", st.get_disk_position(State.R)
        print "G: ", st.get_disk_position(State.G)
        print "B: ", st.get_disk_position(State.B)

        self.sprites_group.add(DiskSprite(st.get_disk(State.B),st.get_disk_position(State.B)), layer=DISKS_lyr)
        self.sprites_group.add(DiskSprite(st.get_disk(State.G),st.get_disk_position(State.G)), layer=DISKS_lyr)
        self.sprites_group.add(DiskSprite(st.get_disk(State.R),st.get_disk_position(State.R)), layer=DISKS_lyr)

        self.goal = pygame.sprite.DirtySprite()
        self.goalText = Text("Prueba")
        self.stepsText = Text("Prueba")
        self.statusText = Text("Prueba")
        self.sprites_group.add(self.goal, layer=GOAL_lyr)
        self.sprites_group.add(self.goalText, layer=GOAL_lyr)
        self.sprites_group.add(self.stepsText, layer=GOAL_lyr)
        self.sprites_group.add(self.statusText, layer=GOAL_lyr)

        self.set_goal(randrange(36))

        self.clicked_sprite = None

        for i in range(1,8+1):
            self.sprites_group.add(TextLevel(i,self.set_board_distance), layer=LEVEL_SEL_lyr)


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

    def set_board(self, board_num):
        self.state.set_board_number(board_num)
        self.state.show()

    def set_goal(self, board_num):
        self.goal_num = board_num
        self.moves_num = 0

        d = inc.distance.dist[board_num][self.state.get_board_number()]

        self.goalText.set_message("Sale en %d movidas" %(d,))

        self.goal.image = pygame.image.load("images/boards/%02d.png" %(board_num, ))
        self.goal.rect = self.goal.image.get_rect()
        self.goal.rect.topright = (Properties.SCREEN_RES[0]-30,30)
        self.goal.dirty = 1
        (x,y) = self.goal.rect.bottomright
        self.goalText.rect.topright = (x,y)
        self.refresh_indicators()
        self.refresh_all_sprites()


    def refresh_indicators(self):
        self.stepsText.set_message("Movidas: %d" %(self.moves_num,))
        (x,y) = self.goalText.rect.bottomright
        self.stepsText.rect.topright = (x,y)
        (x,y) = self.stepsText.rect.bottomright

        if self.state.get_board_number() == self.goal_num:
            self.statusText.set_message("GANASTE")
        else:
            self.statusText.set_message("")
        self.statusText.rect.topright = (x,y)

    def refresh_all_sprites(self):
        for i in self.sprites_group.get_sprites_from_layer(DISKS_lyr):
            i.set_stick_pos(self.state.get_disk_position(i.disk.num))
            i.dirty = 1

    def new_trial(self):
        self.set_board_distance()

    def clicked(self, res):
        (x, y) = pygame.mouse.get_pos()
        for i in self.sprites_group.get_sprites_from_layer(DISKS_lyr):
            if (i.rect.collidepoint(x, y)):
                r = i.click()

                if r:
                    self.clicked_sprite = i
        for i in self.sprites_group.get_sprites_from_layer(GOAL_lyr):
            if (i.rect.collidepoint(x, y)):
                self.new_trial()

        for i in self.sprites_group.get_sprites_from_layer(LEVEL_SEL_lyr):
            if (i.rect.collidepoint(x, y)):
                i.click()

    def move_mouse(self, res):
        if self.clicked_sprite is not None:
            self.clicked_sprite.set_position(pygame.mouse.get_pos())

    def unclicked(self, res):
        if self.clicked_sprite is not None:
            for i in self.sprites_group.get_sprites_from_layer(STICK_lyr):
                if (i.rect.colliderect(self.clicked_sprite)):
                    print "Left on Stick ", i.stick.num
                    if i.stick.not_full() and i.stick.num!=self.state.get_stick_of_disk(self.clicked_sprite.disk.num).num:
                        print "There is room enough. Number of moves: ", self.moves_num
                        self.state.moveSP(self.clicked_sprite, i)
                        self.clicked_sprite = None
                        self.moves_num += 1
                        self.refresh_indicators()
                        if self.state.get_board_number() == self.goal_num:
                            print "GANASTE"
                        return


            self.clicked_sprite.set_stick_pos()
            self.clicked_sprite = None

    def run(self):
        #~ import pdb; pdb.set_trace()
        self.running = True
        self.set_events()

        self.mainLoop()

    def end_game(self, ev=None):
        self.running = False

    def mainLoop(self):
        print "MainLoop"
        pygame.display.flip()

        while self.running:
            self.event_handler.handle()

#             dt = self.clock.tick(30)
            dt = self.clock.tick(100)
            #self.tweener.update(dt / 1000.0)

            self.sprites_group.draw(self.screen)
            pygame.display.flip()

def main():
    global LOG
    if pygame.display.get_init():
        from includes.fw_api import Fw_API  # @UnresolvedImport
        LOG = True
    else:
        pygame.init()
        pygame.display.set_mode(Properties.SCREEN_RES)
        LOG = False
    game = TowerOfLondon()
    game.run()

    print "Saliendo"
    pygame.quit()

if __name__ == '__main__':
    main()
