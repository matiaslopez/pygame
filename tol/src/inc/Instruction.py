# -*- coding: utf-8 -*-

import pygame
import Properties

class Instruction(pygame.sprite.DirtySprite):

    def __init__(self, moves=2, trial=2):
        super(Instruction, self).__init__()

        w, h = Properties.SCREEN_RES
        self.image = pygame.Surface((4*w/8,3*h/8), pygame.SRCALPHA)
        self.font = pygame.font.Font('fonts/Oswald-Bold.ttf', 34)
        self.font2 = pygame.font.Font('fonts/Oswald-Bold.ttf', 18)

        self.set_num(moves, trial)
        self.callback = None

    def set_num(self, moves, trial, callback=None):
        self.callback = callback
        self.image.fill((30,170,70,250))

        self.rect = self.image.get_rect()

        x = self.rect.centerx
        y = self.rect.height / 3

        t = self.font.render("SALE EN {} MOVIDA{}".format(moves, "S" if moves>1 else ""), True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y-(t.get_height()/2)))

        t = self.font2.render(u"ENSAYO {} - HACÉ CLICK PARA COMENZAR".format(trial), True, (0,0,0))
        y = 4* self.rect.height / 5
        self.image.blit(t, (x-(t.get_width()/2), y))

        self.rect.center = pygame.display.get_surface().get_rect().center
        # self.show()

    def hide(self):
        self.visible =  False
        self.dirty = True
        if self.callback:
            self.callback()
            self.callback = None

    def show(self):
        self.visible =  True
        self.dirty = True

class Statistics(pygame.sprite.DirtySprite):

    def __init__(self, stats):
        super(Statistics, self).__init__()

        w, h = Properties.SCREEN_RES
        self.image = pygame.Surface((7*w/8,7*h/8), pygame.SRCALPHA)
        self.font = pygame.font.Font('fonts/Oswald-Bold.ttf', 24)
        self.font2 = pygame.font.Font('fonts/Oswald-Bold.ttf', 18)
        self.font3 = pygame.font.Font('fonts/Oswald-Bold.ttf', 14)
        self.rect = self.image.get_rect()

        self.stats = stats

        self.callback = None

    def set_stats(self):
        self.image.fill((30,170,70,250))


        x = self.rect.centerx
        y = self.rect.y + 20

        played = sum([k for k in self.stats["played"].itervalues()])
        stats_by_num = {k: (v, self.stats["won"][k], None if v==0 else self.stats["won"][k]*100/v) for k,v in self.stats["played"].iteritems()}

        # print played, stats_by_num

        t = self.font2.render("JUGASTE {} ENSAYOS SELECCIONADOS AL AZAR".format(played), True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y))
        # self.image.blit(t, (x, y))
        y += t.get_height() * 1.8

        t = self.font2.render(u"NUESTRA HIPÓTESIS ES QUE:", True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y))
        y += t.get_height() * 1.2
        t = self.font.render(u"CUANTOS MÁS MOVIMIENTOS REQUIERE UN ENSAYO,", True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y))
        y += t.get_height() * 1.2
        t = self.font.render(u"MÁS DIFÍCIL ES PLANIFICAR CORRECTAMENTE", True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y))
        y += t.get_height() * 2


        t = self.font2.render(u"VOS LOGRASTE UN PLAN ÓPTIMO EN LA SIGUIENTE CANTIDAD DE ENSAYOS:", True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y))
        y += t.get_height() * 1.5

        for k in range(3,6+1):
            if stats_by_num[k][2] is not None:
                t = self.font2.render(u"{} MOVIMIENTOS: {}%".format(k, stats_by_num[k][2]), True, (0,0,0))
                self.image.blit(t, (x-(t.get_width()/2), y))
                y += t.get_height() * 1.1

        y += t.get_height() * 1.1

        if (stats_by_num[3][2] >= stats_by_num[4][2] and
            stats_by_num[4][2] >= stats_by_num[5][2] and
            stats_by_num[5][2] >= stats_by_num[6][2]):
            t = self.font.render(u"ACABAS DE APORTAR EVIDENCIA PARA SOSTENER ESTA HIPÓTESIS", True, (0,0,0))
        else:
            t = self.font.render(u"ACABAS DE APORTAR EVIDENCIA PARA RECHAZAR ESTA HIPÓTESIS", True, (0,0,0))

        self.image.blit(t, (x-(t.get_width()/2), y))
        y += t.get_height() * 1.2

        t = self.font3.render(u"(NO COMENTES LA HIPÓTESIS CON FUTUROS PARTICIPANTES PARA NO INFLUENCIARLOS)", True, (0,0,0))
        self.image.blit(t, (x-(t.get_width()/2), y))
        y += t.get_height() * 1.2

        self.rect.center = pygame.display.get_surface().get_rect().center
        self.show()

        '''Jugaste N ensayos que te dimos seleccionados al azar. Nuestra hipótesis es cuantos más movimientos requiere un ensayo, más difícil es planificar correctamente.

            Vos lograste un plan óptimo en la siguiente cantidad de ensayos:
            - Distancia 3: 80%
            - Distancia 4: 60%
            - Distancia 5: 30%
            - Distancia 6: 20%

            Acabas de aportar evidencia para sostener esta hipótesis
            (no comentes la hipótesis con futuros participantes para no influenciarlos)

            El mensaje alternativo sería el mismo pero cambia la anteúltima línea:

            Acabas de aportar evidencia para refutar esta hipótesis
        '''



    def hide(self):
        self.visible =  False
        self.dirty = True
        if self.callback:
            self.callback()
            self.callback = None

    def show(self):
        self.visible =  True
        self.dirty = True