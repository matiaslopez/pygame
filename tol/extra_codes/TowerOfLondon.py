from props import *


class TowerOfLondon:
    def __init__(self):
        self.board = {1: [], 2:[], 3: [B,G,R]}

    def available_move(self, src, dst):
        if len(self.board[src])==0:
            return False
        if len(self.board[dst])== dst:
            return False

        return True

    def sticks_state(self):
        ret = {}
        for (k,v) in self.board.items():
            ret[k] = v
        return ret

    def where_is(self, ball):
        for (k,v) in self.board.items():
            if ball in v:
                return k
    def position_in_stick(self, ball, stick):
        return self.board[stick].index(ball)

    def move(self, src, dst):
        if src==dst:
            print("moviste al mismo lugar")
        else:
            try:
                if len(self.board[dst])== dst:
                    raise KeyError
                card = self.board[src].pop()
                self.board[dst].append(card)
            except IndexError:
                print("En la pila %d no hay ninguna ficha" % (src, ))
            except KeyError:
                print("En la pila %d no hay lugar" % (dst, ))

    def get_board_number(self):
        order = self.board[1] + self.board[2] + self.board[3]
        order_sum = sum([ 1*(len(order)-x-1)  for x in range(len(order)) for i in range(x, len(order)) if order[x]>order[i]])

        kind_board = [ len(self.board[i]) for i in list(self.board.keys())]

        if kind_board[2]==0:
            kind_board_num = 0
        elif kind_board[2]==1:
            kind_board_num = kind_board[2] + kind_board[1]-1
        elif kind_board[2]==2:
            kind_board_num = kind_board[2] + kind_board[1]+1
        elif kind_board[2]==3:
            kind_board_num = kind_board[2] + 2

        return kind_board_num * 6 + order_sum

    def get_board_arrangement_number(self):
        return self.get_board_number()//6

    def translate_arrangement_number(self):
        equiv = {0: 6, 1: 5, 2: 4,
                 3: 2, 4: 3, 5: 1,
                }
        return equiv[self.get_board_arrangement_number()]

    def set_board_number(self, n):
        if n not in list(range(36)):
            raise ValueError("Board number must be in range [0:35]")
        kind_board_num = n // 6
        order_sum = n%6

        if kind_board_num == 5:
            layout = [0,0,3]
        elif kind_board_num == 4:
            layout = [0,1,2]
        elif kind_board_num == 3:
            layout = [1,0,2]
        elif kind_board_num == 2:
            layout = [0,2,1]
        elif kind_board_num == 1:
            layout = [1,1,1]
        elif kind_board_num == 0:
            layout = [1,2,0]

        #~ import pdb; pdb.set_trace()

        available_values = [R,G,B]
        relative_blocks_order = []

        v = available_values[order_sum//2]
        relative_blocks_order += [v]
        available_values.remove(v)
        order_sum = order_sum%2

        v = available_values[order_sum//1]
        relative_blocks_order += [v]
        available_values.remove(v)

        relative_blocks_order += [available_values[0]]

        relative_blocks_order.reverse()

        self.board = {1: [], 2:[], 3: []}
        for i in range(len(layout)):
            for _ in range(layout[i]):
                v = relative_blocks_order.pop()
                self.board[i+1] = self.board[i+1] + [v]

    def show(self):
        p1_1 = to_text(self.board[1][0]) if len(self.board[1]) else "|"
        p2_1 = to_text(self.board[2][0]) if len(self.board[2]) else "|"
        p2_2 = to_text(self.board[2][1]) if len(self.board[2]) == 2 else "|"
        p3_1 = to_text(self.board[3][0]) if len(self.board[3]) else "|"
        p3_2 = to_text(self.board[3][1]) if len(self.board[3]) >= 2 else "|"
        p3_3 = to_text(self.board[3][2]) if len(self.board[3]) == 3 else "|"

        print("  %c              " % (p3_3,))
        print("  %c     %c       " % (p3_2, p2_2))
        print("  %c     %c     %c" % (p3_1, p2_1, p1_1))
        #~ print "-----------------"
        print("--3-----2-----1--   El tablero es el número %d  -- kind board: %s " % (
                self.get_board_number(), self.get_board_arrangement_number()))
        print("")

    def neighbours(self):
        res = []
        for s in [1,2,3]:
            for d in [1,2,3]:
                if s==d:
                    continue
                if self.available_move(s,d):
                    self.move(s,d)
                    res += [((s,d), self.get_board_number())]
                    self.move(d,s)
        return res

    def which_move(self, dst):
        try:
            src = self.get_board_number()
            for s in [1,2,3]:
                for d in [1,2,3]:
                    if s==d:
                        continue
                    if self.available_move(s,d):
                        self.move(s,d)
                        temp = self.get_board_number()
                        self.move(d,s)
                        if temp == dst:
                            return (s, d)
            raise KeyError
        except KeyError:
            print("Not available (one) move from {} to {}".format(src, dst))

    def save_pygame(self):
        import pygame
        # from pygame.locals import *
        pygame.display.init()
        (W, H) = (200, 100)
        surf = pygame.display.set_mode((W, H),32)

        surf = surf.convert_alpha()
        surf.fill((0,0,0,255))
        #~ surf.fill((255,255,255,255))
        surf.fill((255,255,255,255), pygame.Rect((1,1),(198,98)))

        # sticks
        BROWN = (210,105,30)
        BLACK = (0,200,0)
        CARD_COLORS = [(210,0,30), (0,210,30), (30,0,210)]
        CARD_LINE_POINTS = [ ((0,0), (1,1)), ((0,0.5), (1,0.5)), ((0.5,0), (0.5,1))]
        CARD_W = 54
        CARD_H = 20
        FLOORH = 20
        WS = 10
        DH = CARD_H
        surf.fill(BROWN, rect=pygame.Rect(( 40-WS//2, H-(DH*1+10)-FLOORH), (WS, DH*1+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect((100-WS//2, H-(DH*2+10)-FLOORH), (WS, DH*2+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect((160-WS//2, H-(DH*3+10)-FLOORH), (WS, DH*3+10+FLOORH-1)))

        surf.fill(BLACK, rect=pygame.Rect((1, H-FLOORH), (W-2, FLOORH-1)))




        for k in list(self.board.keys()):
            i = 0
            for j in self.board[k]:
                (card_x0, card_y0) = (40+60*(k-1)-CARD_W//2, H-FLOORH-((CARD_H+2)*(i+1)))
                surf.fill(CARD_COLORS[j-1], rect=pygame.Rect(
                    (card_x0, card_y0), (CARD_W, CARD_H)))
                (start_x, start_y) = (card_x0 + CARD_LINE_POINTS[j-1][0][0]*CARD_W,
                                      card_y0 + CARD_LINE_POINTS[j-1][0][1]*CARD_H)
                (end_x, end_y) = (card_x0 + CARD_LINE_POINTS[j-1][1][0]*CARD_W,
                       card_y0 + CARD_LINE_POINTS[j-1][1][1]*CARD_H)
                pygame.draw.line(surf, (255,255,255),(start_x, start_y), (end_x, end_y), 2)
                i+=1

        pygame.font.init()
        f = pygame.font.get_default_font()
        font = pygame.font.Font(f, 20)
        text = font.render(str(self.get_board_number()), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = surf.get_rect().centerx
        surf.blit(text, textpos)

        pygame.display.flip()
        pygame.image.save(surf, "imgs/%02d.png" % (self.get_board_number(),))
        pygame.quit()


    def mm_syntax(self):
        d_col = { 0:2, 1:3, 2: 1}
        d_col_reverse = dict([(x_y[1],x_y[0]) for x_y in iter(d_col.items())])
        res = []
        for k in [3,2,1]:
            res.append([d_col_reverse[v] for v in self.board[k]])

        return res



    def save_pygame_letters(self):
        import pygame
        # from pygame.locals import *
        pygame.display.init()
        (W, H) = (200, 100)
        surf = pygame.display.set_mode((W, H),32)

        surf = surf.convert_alpha()
        surf.fill((0,0,0,255))
        #~ surf.fill((255,255,255,255))
        surf.fill((255,255,255,255), pygame.Rect((1,1),(198,98)))

        # sticks
        # BROWN = (210,105,30)
        BROWN = pygame.Color("#63151B")
        BLACK = (0,200,0)
        CARD_COLORS = [(150,0,30), (30,0,150), (150,150,30)]
                                                    # RED,   GREEN, BLUE
        CARD_COLORS = [pygame.Color(x) for x in ["#A3232D", "#CFCA13", "#2680B0"]]
        CARD_COLORS = [pygame.Color(x) for x in ["#B2502A", "#90BD75", "#3040CC"]]
        CARD_LINE_POINTS = [ ((0,0), (1,1)), ((0,0.5), (1,0.5)), ((0.5,0), (0.5,1))]
        CARD_W = 54
        CARD_H = 27
        FLOORH = 5
        WS = 10
        DH = CARD_H
        # surf.fill(BROWN, rect=pygame.Rect(( 40-WS/2, H-(DH*1+10)-FLOORH), (WS, DH*1+10+FLOORH-1)))
        # surf.fill(BROWN, rect=pygame.Rect((100-WS/2, H-(DH*2+10)-FLOORH), (WS, DH*2+10+FLOORH-1)))
        # surf.fill(BROWN, rect=pygame.Rect((160-WS/2, H-(DH*3+10)-FLOORH), (WS, DH*3+10+FLOORH-1)))

        surf.fill(BROWN, rect=pygame.Rect((160-WS//2, H-(DH*1+10)-FLOORH), (WS, DH*1+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect((100-WS//2, H-(DH*2+10)-FLOORH), (WS, DH*2+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect(( 40-WS//2, H-(DH*3+10)-FLOORH), (WS, DH*3+10+FLOORH-1)))


        surf.fill(BLACK, rect=pygame.Rect((1, H-FLOORH), (W-2, FLOORH-1)))



        pygame.font.init()
        f = pygame.font.get_default_font()
        font = pygame.font.Font(f, 20)

        for k in list(self.board.keys()):
            i = 0
            for j in self.board[k]:
                (card_x0, card_y0) = (40+60*(-1*k+3)-CARD_W//2, H-FLOORH-((CARD_H+2)*(i+1)))
                surf.fill((0,0,0), rect=pygame.Rect(
                    (card_x0, card_y0), (CARD_W, CARD_H)))
                surf.fill(CARD_COLORS[j-1], rect=pygame.Rect(
                    (card_x0+1, card_y0+1), (CARD_W-2, CARD_H-2)))

                text = font.render(to_text(j), 1, (255, 255, 255))
                textpos = (card_x0 + (CARD_W - text.get_width())//2, card_y0 + (CARD_H-text.get_height())//2 )
                surf.blit(text, textpos)
                i+=1

        text = font.render(str(self.get_board_number()), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = surf.get_rect().centerx
        surf.blit(text, textpos)

        pygame.display.flip()
        pygame.image.save(surf, "imgs/l-%02d.png" % (self.get_board_number(),))
        pygame.quit()