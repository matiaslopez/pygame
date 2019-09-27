# -*- coding: utf-8 -*-
import csv


R = 1
G = 2
B = 3

translation_mycode_to_paper_code = [ # (paper, mycode)
    (11, 30), (12, 22), (13, 28), (14, 17), (15,  9), (16,  3),
    (21, 31), (22, 20), (23, 26), (24, 15), (25, 11), (26,  5),
    (31, 34), (32, 21), (33, 27), (34, 14), (35,  6), (36,  0),
    (41, 35), (42, 19), (43, 25), (44, 12), (45,  8), (46,  2),
    (51, 33), (52, 18), (53, 24), (54, 13), (55, 10), (56,  4),
    (61, 32), (62, 23), (63, 29), (64, 16), (65,  7), (66,  1),
]

# deprecated name
degrees_per_family = { #(number of balls can take, number of posible board destiny)
    0: (2, 2),
    1: (3, 4),
    2: (2, 3),
    3: (2, 3),
    4: (2, 4),
    5: (1, 2),
}

degrees_per_arrangement = { #(number of balls can take, number of posible board destiny)
    0: (2, 2),
    1: (3, 4),
    2: (2, 3),
    3: (2, 3),
    4: (2, 4),
    5: (1, 2),
}

def get_papercode(nro):
    # print "nro", nro
    return [y for (y,x) in translation_mycode_to_paper_code if x==nro][0]

def get_mycode(nro):
    return [x for (y,x) in translation_mycode_to_paper_code if y==nro][0]


def get_distances(table, count_paths=None):
    # print "a"
    for i in range(len(table)):
        for j in range(len(table[i])):
            if i==j:
                table[i][j] = 0

    current_expand = 0
    t = TowerOfLondon()

    for _ in range(len(table)):
        for i in range(len(table)):
            #t.show()
            for j in range(len(table[i])):
                if table[i][j] == current_expand:
                    t.set_board_number(j)
                    ngs = t.neighbours()
                    # print i, j,ngs
                    for ng in ngs:
                        if table[i][ng[1]] == -1:
                            table[i][ng[1]] = current_expand + 1

        current_expand += 1

    if (count_paths is not None):
        for n in range(1, max(max(table))+1):
            for i in range(len(table)):
                for j in range(len(table)):
                    if n==1 and table[i][j]==n:
                        count_paths[i][j]=n
                    else:
                        if table[i][j]==n:
                            t.set_board_number(i)
                            ngs = t.neighbours()
                            for ng in ngs:
                                if (table[ng[1]][j] == n-1):
                                    count_paths[i][j]=count_paths[i][j]+count_paths[ng[1]][j]

    return table

def get_all_minimum_paths(table_of_dist, src, dest):

    dist = table_of_dist[src][dest]

    if dist not in range(1,9):
        return []

    paths = [[src]]
    t = TowerOfLondon()

    for i in range(dist,0,-1): #to go along all the distances
        old_paths = paths
        paths = []
        for p in old_paths:
            current_board = p[-1]
            t.set_board_number(current_board)

            ngs = t.neighbours()
            for ng in ngs:
                if table_of_dist[ng[1]][dest] == i-1:
                    paths = paths + [p + [ng[1]]]

    return paths

def print_dist(table):
    res = ""
    for i in range(len(table)):
        #res +=  "%d  " % (i, )
        for j in range(len(table[i])):
            res += " %d " % (table[i][j], )
        res +=  "\n"

    print res

def distance_groups():
    d = [ ([ -1  for _ in range(36) ]) for _ in range(36) ]
    get_distances(d)

    res = [ ([ []  for _ in range(8+1) ]) for _ in range(6) ]

    for idx in range(len(res)):
        for j in range(len(res[idx])):
            a = sorted([i/6 for i,k in enumerate(d[idx*6]) if k==j])
            res[idx][j]=dict((i,a.count(i)) for i in a)
            # print dict((i,a.count(i)) for i in a)

    return res

def translate_path_to_paper_code(p):
    res = []
    # print "Translating ", p
    for t in p:
        res.append(get_papercode(t))

    return res

def path_value(path):
    src = path[0]
    dst = path[-1]

    res = {"step": 0, "subgoal": 0, "anti0": 0, "anti1": 0, "anti2": 0, "semi-anti1": 0, "semi-anti2": 0}
    # step: none of the next categories
    # subgoal: move ball to a definitive position
    # anti0: remove from final position, and it has 0 balls under it
    # anti1: remove from final position, and it has 1 balls under it
    # anti2: remove from final position, and it has 2 balls under it
    # semi-anti1: removes form final stick but its final position is under the current
    # semi-anti2: removes form final stick but its final position is over the current
    # values: [ S , G , A0 , A1 , A2 , SA1 , SA2 ]

    final = TowerOfLondon()
    final.set_board_number(path[-1])
    res_arr = []
    for i in range(len(path)-1):
        n_cur = in_position_balls(path[i],dst)
        n_next = in_position_balls(path[i+1],dst)
        move_data = moving_data(path[i],path[i+1])


        if n_cur > n_next:
            st = move_data["src_sticks"]
            pos = len(st[move_data["src_ball"]]) - 1

            res["anti%d" % pos] = res["anti%d" % pos] + 1
            res_arr.append("A%d" % pos)
        elif n_cur < n_next:
            res["subgoal"] = res["subgoal"] + 1
            res_arr.append("G")
        else: # n_cur == n_next:
            fs = final.where_is(move_data["moved_ball"])
            if fs == move_data["src_ball"]:
                # import pdb; pdb.set_trace()
                # take ball out of final stick, but not in position
                idx = final.position_in_stick(move_data["moved_ball"], fs) # possible values [0, 1, 2]
                current_idx = len(move_data["src_sticks"][move_data["src_ball"]]) - 1
                if idx < current_idx: # semi1
                    res["semi-anti1"] = res["semi-anti1"] + 1
                    res_arr.append("SA1")
                else:
                    res["semi-anti2"] = res["semi-anti2"] + 1
                    res_arr.append("SA2")
            else:
                res["step"] = res["step"] + 1
                res_arr.append("S")

    return (res, res_arr)

def moving_data(src_num, dst_num):
    src = TowerOfLondon()
    dst = TowerOfLondon()

    src.set_board_number(src_num)
    dst.set_board_number(dst_num)

    src_sticks = src.sticks_state()
    dst_sticks = dst.sticks_state()

    for i in range(1,3+1):
        if len(src_sticks[i]) > len(dst_sticks[i]):
            moved_ball = src_sticks[i][-1]
            src_ball = i
        elif len(src_sticks[i]) < len(dst_sticks[i]):
            dst_ball = i

    ret = {}
    ret["moved_ball"] = moved_ball
    ret["src_ball"] = src_ball
    ret["dst_ball"] = dst_ball
    ret["src_sticks"] = src_sticks
    ret["dst_sticks"] = dst_sticks

    return ret

def in_position_balls(n,m):
    src = TowerOfLondon()
    dst = TowerOfLondon()

    src.set_board_number(n)
    dst.set_board_number(m)

    res = 0
    for k in src.board.keys():
        if len(src.board[k]):
            for h in range(len(src.board[k])):
                if len(dst.board[k])>h:
                   if dst.board[k][h]==src.board[k][h]:
                        res=res+1
    return res



def show_dist(table):
    res = ""
    for i in range(len(table)):
        res +=  "%d & " % (i, )
        for j in range(len(table[i])):
            res += "%d " % (table[i][j], )
            if j+1!=len(table[i]):
                res += "& "
        res +=  "\\\\\n"

    f = open("tabla.tex", "w")
    f.write(res)
    f.close()


def save_pygame_path(path):
    import pygame
    import os
    # from pygame.locals import *
    pygame.display.init()
    n = len(path)
    (W, H) = (200*n+50*(n-1), 100)
    surf = pygame.display.set_mode((W, H),32)

    surf = surf.convert_alpha()
    surf.fill((255,255,255,255))
    surf.fill((0,0,0,255), pygame.Rect((0,49),(200*n+50*(n-1),2)))

    for (i,v) in enumerate(path):
        filename = "l-%02d.png" % v
        img = pygame.image.load(os.path.join('imgs', filename))

        surf.blit(img, (200*i+50*(i),0))

    (_, letters) = path_value(path)

    pygame.font.init()
    f = pygame.font.get_default_font()
    font = pygame.font.Font(f, 20)

    for (i,v) in enumerate(letters):
        text = font.render(v, 1, (10, 10, 10))
        textrec = text.get_width()
        #textpos.centerx = surf.get_rect().centerx
        surf.blit(text, (200*(i+1)+50*i+(50-textrec)/2,25))

    str_file = ("from_%02d-to_%02d-long_%d-" % (path[0],path[-1],(len(path)-1))) + "-".join(["%02d" % i for i in path ])
    pygame.display.flip()
    pygame.image.save(surf, "paths/%s-.png" % (str_file,))
    pygame.quit()


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
        for (k,v) in self.board.iteritems():
            ret[k] = v
        return ret

    def where_is(self, ball):
        for (k,v) in self.board.iteritems():
            if ball in v:
                return k
    def position_in_stick(self, ball, stick):
        return self.board[stick].index(ball)

    def move(self, src, dst):

        if src==dst:
            print "moviste al mismo lugar"
        else:
            try:
                if len(self.board[dst])== dst:
                    raise KeyError
                card = self.board[src].pop()
                self.board[dst].append(card)
            except IndexError:
                print "En la pila %d no hay ninguna ficha" % (src, )
            except KeyError:
                print "En la pila %d no hay lugar" % (dst, )

    def get_board_number(self):
        order = self.board[1] + self.board[2] + self.board[3]
        order_sum = sum([ 1*(len(order)-x-1)  for x in range(len(order)) for i in range(x, len(order)) if order[x]>order[i]])

        kind_board = [ len(self.board[i]) for i in self.board.keys()]

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
        return self.get_board_number()/6

    def translate_arrangement_number(self):
        equiv = {0: 6, 1: 5, 2: 4,
                 3: 2, 4: 3, 5: 1,
                }
        return equiv[self.get_board_arrangement_number()]

    def set_board_number(self, n):
        if n not in range(36):
            raise ValueError("Board number must be in range [0:35]")
        kind_board_num = n / 6
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

        v = available_values[order_sum/2]
        relative_blocks_order += [v]
        available_values.remove(v)
        order_sum = order_sum%2

        v = available_values[order_sum/1]
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

        print "  %c              " % (p3_3,)
        print "  %c     %c       " % (p3_2, p2_2)
        print "  %c     %c     %c" % (p3_1, p2_1, p1_1)
        #~ print "-----------------"
        print "--3-----2-----1--   El tablero es el número %d  -- en CEMIC syntax: %s  -- en MM syntax: %s " % (
                self.get_board_number(), self.cemic_syntax(), self.mm_syntax())
        print ""

    def neighbours(self):
        s = self.get_board_number()
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
        surf.fill(BROWN, rect=pygame.Rect(( 40-WS/2, H-(DH*1+10)-FLOORH), (WS, DH*1+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect((100-WS/2, H-(DH*2+10)-FLOORH), (WS, DH*2+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect((160-WS/2, H-(DH*3+10)-FLOORH), (WS, DH*3+10+FLOORH-1)))

        surf.fill(BLACK, rect=pygame.Rect((1, H-FLOORH), (W-2, FLOORH-1)))




        for k in self.board.keys():
            i = 0
            for j in self.board[k]:
                (card_x0, card_y0) = (40+60*(k-1)-CARD_W/2, H-FLOORH-((CARD_H+2)*(i+1)))
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

    def cemic_syntax(self):
        keys = self.board.keys()
        keys.reverse()
        res = ""
        for k in keys:
            i = 0
            for j in self.board[k]:
                nro = "1" if (k==3) else ("2" if (k==2) else "3")
                res  = res + " " + to_text_CEMIC(j) + nro

        return res

    def mm_syntax(self):
        d_col = { 0:2, 1:3, 2: 1}
        d_col_reverse = dict(map(lambda (x,y): (y,x), d_col.iteritems()))
        res = []
        for k in [3,2,1]:
            res.append([d_col_reverse[v] for v in self.board[k]])

        return res


    def set_board_from_cemic_syntax(self, str_in):
        q = str_in.split()

        self.board = {1:[], 2:[], 3:[]}
        for d in q:
            nro = int("1" if (int(d[1])==3) else ("2" if (int(d[1])==2) else "3"))
            #print "ubicando %s en %d con numero %d " % (d, nro, cemic_nro(d[0]))
            self.board[nro] = self.board[nro] + [cemic_nro(d[0])]


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

        surf.fill(BROWN, rect=pygame.Rect((160-WS/2, H-(DH*1+10)-FLOORH), (WS, DH*1+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect((100-WS/2, H-(DH*2+10)-FLOORH), (WS, DH*2+10+FLOORH-1)))
        surf.fill(BROWN, rect=pygame.Rect(( 40-WS/2, H-(DH*3+10)-FLOORH), (WS, DH*3+10+FLOORH-1)))


        surf.fill(BLACK, rect=pygame.Rect((1, H-FLOORH), (W-2, FLOORH-1)))



        pygame.font.init()
        f = pygame.font.get_default_font()
        font = pygame.font.Font(f, 20)

        for k in self.board.keys():
            i = 0
            for j in self.board[k]:
                (card_x0, card_y0) = (40+60*(-1*k+3)-CARD_W/2, H-FLOORH-((CARD_H+2)*(i+1)))
                surf.fill((0,0,0), rect=pygame.Rect(
                    (card_x0, card_y0), (CARD_W, CARD_H)))
                surf.fill(CARD_COLORS[j-1], rect=pygame.Rect(
                    (card_x0+1, card_y0+1), (CARD_W-2, CARD_H-2)))

                text = font.render(to_text_color(j), 1, (255, 255, 255))
                textpos = (card_x0 + (CARD_W - text.get_width())/2, card_y0 + (CARD_H-text.get_height())/2 )
                surf.blit(text, textpos)
                i+=1

        text = font.render(str(self.get_board_number()), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = surf.get_rect().centerx
        # text = font.render(self.cemic_syntax()[1:]+ " - " + str(self.get_board_number()), 1, (10, 10, 10))
        # textpos = text.get_rect()
        # textpos.centerx = surf.get_rect().centerx - 35
        surf.blit(text, textpos)

        pygame.display.flip()
        pygame.image.save(surf, "imgs/l-%02d.png" % (self.get_board_number(),))
        pygame.quit()

def to_text_color(l):
    if l==R:
        return "R"
    if l==B:
        return "B"
    if l==G:
        return "G"


def to_text_CEMIC(l):
    if l==R:
        return "B"
    if l==B:
        return "A"
    if l==G:
        return "C"

def cemic_nro(n):
    if n=="B":
        return R
    if n=="A":
        return B
    if n=="C":
        return G

def to_text(l):
    if l==R:
        return "R"
    if l==B:
        return "B"
    if l==G:
        return "G"


# run toweroflondon.py
# copy_str = cemic_draft(cemic2_red)
# print copy_str

def all_data():
    t_src = TowerOfLondon()
    t_dst = TowerOfLondon()
    res = []
    header = [(  "Tablero inicial",
                "Configutrcion inicial", # forma en la que están acomodadas las bolitas asumiendolas de color único
                "Familia inicial", # familia definida según el paper
                "Opciones_salida",
                "Opciones_llegada",
                "Tablero final",
                "Configuracion final",
                "Familia final",
                "Long",
                "Cantidad Caminos min",
                "Caminos"),]

    for src in xrange(36):
        for dst in xrange(36):
            if src==dst:
                continue

            t_src.set_board_number(src)
            t_dst.set_board_number(dst)
            p = get_all_minimum_paths(dist, src, dst)

            src_family = get_papercode(src)/10
            dst_family = get_papercode(dst)/10
            paper_i = str(get_papercode(src))
            paper_f = str(get_papercode(dst))


            print src, dst
            line = ( src, #"Tablero inicial",
                    t_src.translate_arrangement_number(), #"Configutrcion inicial",
                    src_family, #"Familia inicial", # digito más signigicativo
                    degrees_per_arrangement[t_src.get_board_arrangement_number()][0], #"Opciones_salida",
                    degrees_per_arrangement[t_src.get_board_arrangement_number()][1], #"Opciones_llegada",
                    dst, #"Tablero final",
                    t_dst.translate_arrangement_number(), #"Configuracion final",
                    dst_family, #"Familia final",
                    len(p[0])-1, #"Long",
                    len(p), #"Cantidad Caminos min",
                    p, #"Caminos")
                )
            res.append(line)

    with open('full_cases.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(header + res)
    return res


def all_regular_path():
    t_src = TowerOfLondon()
    t_dst = TowerOfLondon()
    res = []
    header = [(  "Tablero inicial",
                "Configutrcion inicial", # forma en la que están acomodadas las bolitas asumiendolas de color único
                "Familia inicial", # familia definida según el paper
                "Opciones_salida",
                "Opciones_llegada",
                "Tablero final",
                "Configuracion final",
                "Familia final",
                "Long",
                "Cantidad Caminos min",
                "Caminos"),]

    for src in xrange(36):
        for dst in xrange(36):
            if src==dst:
                continue

            t_src.set_board_number(src)
            t_dst.set_board_number(dst)
            p = get_all_minimum_paths(dist, src, dst)

            src_family = get_papercode(src)/10
            dst_family = get_papercode(dst)/10
            paper_i = str(get_papercode(src))
            paper_f = str(get_papercode(dst))


            print src, dst
            line = ( src, #"Tablero inicial",
                    t_src.translate_arrangement_number(), #"Configutrcion inicial",
                    src_family, #"Familia inicial", # digito más signigicativo
                    degrees_per_arrangement[t_src.get_board_arrangement_number()][0], #"Opciones_salida",
                    degrees_per_arrangement[t_src.get_board_arrangement_number()][1], #"Opciones_llegada",
                    dst, #"Tablero final",
                    t_dst.translate_arrangement_number(), #"Configuracion final",
                    dst_family, #"Familia final",
                    len(p[0])-1, #"Long",
                    len(p), #"Cantidad Caminos min",
                    p, #"Caminos")
                )
            res.append(line)

    with open('full_cases.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(header + res)
    return res


def cemic_draft(input_str):
    t_src = TowerOfLondon()
    t_dst = TowerOfLondon()
    res = "Nivel\tEnsayo\t"
    res = res + "Inicial\tPaper_i\tPermutacion_i\tFamilia_i\tOpciones_salida\tOpciones_llegada\t"
    res = res + "Final\tPaper_f\tPermutacion_f\tFamilia_f\t"
    res = res + "Misma Permutacion\tMisma Familia\tLong\tCantidad Caminos min\tCaminos\n"
    for (k,trial) in enumerate(input_str):
        t_src.set_board_from_cemic_syntax(trial[2])
        t_dst.set_board_from_cemic_syntax(trial[3])

        src = t_src.get_board_number()
        dst = t_dst.get_board_number()

        p = get_all_minimum_paths(dist, src, dst)
        print "%d - Para nivel %d ensayo %d hay distancia %d y se puede lograr por %d caminos \t(de tablero %d a %d)" % (k,
             trial[0], trial[1],dist[src][dst], len(p), src, dst)

        src_family = t_src.get_board_arrangement_number()
        paper_i = str(get_papercode(src))
        paper_f = str(get_papercode(dst))
        res = res + "%d\t%d\t" % (trial[0], trial[1],)
        res = res + "%s\t%s\t%s\t%s\t%d\t%d\t" % (trial[2], paper_i, paper_i[0], paper_i[1],
                degrees_per_family[src_family][0],degrees_per_family[src_family][1]) # inicial
        res = res + "%s\t%s\t%s\t%s\t" % (trial[3], paper_f, paper_f[0], paper_f[1],) # final
        res = res + "%d\t%d\t%d\t %d \t%s\n" % (paper_i[0]==paper_f[0],
                paper_i[1]==paper_f[1],
                dist[src][dst],
                len(p),
                ("\t".join([str(translate_path_to_paper_code(x)) + " {" + " ".join(path_value(x)[1]) + "}" for x in p]))) # caminos

        #for unP in p:
        #    save_pygame_path(unP)

    return res


#cemic_translate_tomas(cemic_tomas)
def cemic_translate_tomas(list_trials):
    header = [("Ensayo", "Source", "Goal", "Nivel")]
    body = []

    t_src = TowerOfLondon()
    t_dst = TowerOfLondon()
    for (set_trial, level, trial_num, src, dst) in list_trials:
        t_src.set_board_from_cemic_syntax(src)
        t_dst.set_board_from_cemic_syntax(dst)

        src = t_src.get_board_number()
        dst = t_dst.get_board_number()
        body.append((set_trial, trial_num, src, dst, level))

    with open('toma01.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(header + [ (trial_num, src, dst, level)
            for (set_trial, trial_num, src, dst, level) in body if set_trial == 1])

    with open('toma02.csv', 'wb') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerows(header + [ (trial_num, src, dst, level)
            for (set_trial, trial_num, src, dst, level) in body if set_trial == 2])


cemic_test = [(1,1,'C1 B1 A1' , 'C1 B1 A3'),
(1,2,'C1 B1 A2' , 'C1 A2 B2'),
(1,3,'A1 C2 B2' , 'A1 C2 B3'),
(1,4,'A1 C1 B3' , 'A1 C2 B3'),
(1,5,'B1 C1 A2' , 'B1 C1 A3'),
(2,1,'A1 C2 B2' , 'A1 B1 C3'),
(2,2,'B1 C1 A1' , 'B1 A2 C3'),
(2,3,'B1 A2 C2' , 'C1 A2 B3'),
(2,4,'C1 A1 B2' , 'C1 B1 A3'),
(2,5,'B1 C1 A3' , 'B1 A2 C3'),
(3,1,'C1 A1 B2' , 'A1 B2 C3'),
(3,2,'B1 C1 A1' , 'A2 B2 C3'),
(3,3,'C1 B1 A3' , 'A2 B2 C3'),
(3,4,'B1 C1 A3' , 'B1 A1 C1'),
(3,5,'B1 C1 A2 ', 'B1 C2 A2'),
(4,1,'C1 A1 B1' , 'A1 B2 C3'),
(4,2,'B1 C1 A1' , 'C1 A2 B2'),
(4,3,'B1 C1 A3' , 'A1 B1 C2'),
(4,4,'A2 C2 B3' , 'C1 B2 A2'),
(4,5,'A1 C2 B2' , 'B2 A2 C3'),
(5,1,'A1 B2 C1' , 'B1 A1 C2'),
(5,2,'B1 C1 A1' , 'C1 A1 B3'),
(5,3,'A2 C2 B3' , 'C2 B2 A3'), #(5,3,'A2 C2 B2' , 'C2 B2 A3'),
(5,4,'C1 B2 A3' , 'A1 C2 B3'),
(5,5,'A2 C2 B3' , 'C2 B2 A3'),
(6,1,'A2 C2 B3' , 'A1 B2 C3'),
(6,2,'C1 B2 A2' , 'B1 C1 A2'),#(6,2,'C1 B2 A2' , 'B1 C1 B2'),
(6,3,'B1 C1 A3' , 'A1 B2 C3'),
(6,4,'B1 C1 A2' , 'A1 B1 C3'),
(6,5,'A1 C2 B3' , 'A2 B2 C3'),
(7,1,'C1 A1 B2' , 'B1 A1 C1'),
(7,2,'C1 B2 A3' , 'C2 B2 A3'),
(7,3,'B1 C1 A3' , 'C1 B2 A2'),
(7,4,'B2 C2 A3' , 'B1 A1 C3'),
(7,5,'A1 C1 B2' , 'A2 C2 B3'),
(8,1,'C1 B1 A1' , 'A1 C2 B2'),
(8,2,'A2 B2 C3' , 'A1 B1 C1'),
(8,3,'C2 A2 B3' , 'C1 B1 A2'),
(8,4,'B1 A2 C2' , 'A1 C1 B1'),
(8,5,'B1 C1 A1' , 'B2 A2 C3'),
]


cemic_test_2 =[("1","1","1","C1 B1 A1","C1 B1 A3"),
("1","1","2","B1 A2 C2","B1 C1 A2"),
("1","1","3","B1 C1 A2","B1 C1 A1"),
("1","1","4","C1 B1 A2","C1 A2 B3"),
("1","1","5","C1 B2 A3","C1 B2 A2"),
("1","2","1","A2 B2 C3","C1 B1 A2"),
("1","2","2","B1 A2 C3","C1 A2 B2"),
("1","2","3","A1 B2 C2","A1 C1 B3"),
("1","2","4","B1 C1 A2","A2 B2 C3"),
("1","2","5","B1 C2 A3","B1 A1 C1"),
("1","3","1","C1 A1 B2","A1 B2 C3"),
("1","3","2","B1 C1 A1","A2 B2 C3"),
("1","3","3","C1 B1 A3","A2 B2 C3"),
("1","3","4","B1 C1 A3","B1 A1 C1"),
("1","3","5","B1 C1 A2","B1 C2 A2"),
("1","4","1","C1 A1 B1","A1 B2 C3"),
("1","4","2","B1 C1 A1","C1 A2 B2"),
("1","4","3","B1 C1 A3","A1 B1 C2"),
("1","4","4","A2 C2 B3","C1 B2 A2"),
("1","4","5","A1 C2 B2","B2 A2 C3"),
("1","5","1","A1 B1 C1","B1 A1 C2"),
("1","5","2","B1 C1 A1","C1 A1 B3"),
("1","5","3","A2 C2 B3","C2 B2 A3"),
("1","5","4","C1 B2 A3","A1 C2 B3"),
("1","5","5","A1 B1 C3","B1 C1 A3"),
("1","6","1","A2 C2 B3","A1 B2 C3"),
("1","6","2","C1 B2 A2","B1 C1 A2"),
("1","6","3","B1 C1 A3","A1 B2 C3"),
("1","6","4","B1 C1 A2","A1 B1 C3"),
("1","6","5","A1 C2 B3","A2 B2 C3"),
("1","7","1","C1 A1 B2","B1 A1 C1"),
("1","7","2","C1 B2 A3","C2 B2 A3"),
("1","7","3","B1 C1 A3","C1 B2 A2"),
("1","7","4","B2 C2 A3","B1 A1 C3"),
("1","7","5","A1 C1 B2","A2 C2 B3"),
("1","8","1","C1 B1 A1","A1 C2 B2"),
("1","8","2","A2 B2 C3","A1 B1 C1"),
("1","8","3","C2 A2 B3","C1 B1 A3"),
("1","8","4","B1 A2 C2","A1 C1 B1"),
("1","8","5","B1 C1 A1","A1 B2 C3"),
("2","1","1","A2 C2 B3","B1 A2 C2"),
("2","1","2","B1 C1 A3","B1 C2 A3"),
("2","1","3","B1 A2 C3","B1 C1 A2"),
("2","1","4","A1 C2 B3","C2 A2 B3"),
("2","1","5","B1 C1 A2","B1 A2 C2"),
("2","2","1","B1 A2 C2","C1 A2 B3"),
("2","2","2","B2 A2 C3","A1 B1 C3"),
("2","2","3","C1 A2 B3","A2 B2 C3"),
("2","2","4","C1 A1 B2","C1 B1 A3"),
("2","2","5","B1 C2 A3","B1 A1 C3"),
("2","3","1","A1 C2 B2","B1 C1 A3"),
("2","3","2","B1 C1 A1","B1 A1 C3"),
("2","3","3","B1 A2 C2","B1 C2 A3"),
("2","3","4","C1 A1 B2","A2 C2 B3"),
("2","3","5","B1 C1 A3","A2 B2 C3"),
("2","4","1","B1 C1 A1","C1 A2 B3"),
("2","4","2","C1 B1 A1","B1 A2 C2"),
("2","4","3","A2 C2 B3","B1 A1 C2"),
("2","4","4","B1 A2 C3","C1 B1 A3"),
("2","4","5","B1 A2 C2","C2 B2 A3"),
("2","5","1","C1 B1 A1","A1 C1 B2"),
("2","5","2","C1 A1 B1","A1 B1 C3"),
("2","5","3","B1 A2 C2","C1 B2 A2"),
("2","5","4","C1 A1 B3","B1 C1 A1"),
("2","5","5","B1 C1 A2","A1 B1 C2"),
("2","6","1","A1 C1 B1","B1 A1 C1"),
("2","6","2","C1 B2 A2","C2 B2 A3"),
("2","6","3","A1 B1 C3","B1 C1 A1"), # old: ("2","6","3","A1 C1 B3","B1 C1 A1"),
("2","6","4","B1 C1 A2","C1 B2 A2"),
("2","6","5","C1 B2 A3","B1 A1 C3"),
("2","7","1","B2 A2 C3","B1 C1 A2"),
("2","7","2","B1 C1 A1","A1 B2 C3"),
("2","7","3","B1 A2 C3","A1 B1 C1"),
("2","7","4","A1 B1 C2","A2 B2 C3"),
("2","7","5","B1 C1 A1","C1 B2 A3"),
("2","8","1","B1 C1 A1","C1 B2 A2"),
("2","8","2","C1 A2 B2","A1 B1 C1"),
("2","8","3","B1 C2 A3","C1 B2 A3"),
("2","8","4","C1 B1 A1","C2 A2 B3"),
("2","8","5","C1 A2 B2","A1 C1 B3"),
]



cemic2_red = [ (int(x[1]), int(x[2]), x[3], x[4]) for x in cemic_test_2]

cemic_tomas = [ (int(x[0]), int(x[1]), int(x[2]), x[3], x[4]) for x in cemic_test_2]

dist = [ ([ -1  for _ in range(36) ]) for _ in range(36) ]
count_min_paths = [ ([ 0  for _ in range(36) ]) for _ in range(36) ]

_ = get_distances(dist, count_min_paths)
nd = [ y for x in count_min_paths for y in x ]

import json
with open('dist.json', 'w') as outfile:
    json.dump(dist, outfile)

dict_min_path = {}
for i in nd:
    dict_min_path[i] = dict_min_path.setdefault(i,0) + 1

# subg = [ ([ -1  for _ in range(36) ]) for _ in range(36) ]
# for i in range(36):
#     for j in range(36):
#         if has_subgoal(i,j):
#             subg[i][j] = 1
#         else:
#             subg[i][j] = 0


def generate_plots():
    t = TowerOfLondon()
    t.show()

    for i in range(36):
        t.set_board_number(i)
        t.save_pygame_letters()
        t.save_pygame()

if __name__ == "__main__":
    t = TowerOfLondon()
    # t.show()

    #~ t.save_pygame()

    neighborhoud = {}
    for i in range(36):
        t.set_board_number(i)
        # t.save_pygame_letters()
        neighborhoud[i] = t.neighbours()

    # print neighborhoud

    clusters = []
    for k in neighborhoud.keys():
        for v in neighborhoud[k]:
            #~ print "%d -> %d;" %(k,v[1])

            if (k<v[1]):
                c1 = k/6
                c2 = v[1]/6
                if clusters.count((c1,c2))==0:
                    clusters.append((c1,c2))
                # print "%d -- %d;" %(k,v[1])

    # print "--------------"
    # for (s,d) in clusters:
        # print "cluster_%d -- cluster_%d;" %(s,d)
    #~
    #~ t.set_board_number(0)
    #~ t.move(3,3); t.show()
    #~ t.move(3,2); t.show()
    #~ t.move(2,3); t.show()
    #~ t.move(3,2); t.show()




        #~ res = 0;
        #~ if len(self.board[1]):
            #~ res = res+ self.board[1][0]; # Card in stack 1
        #~ if len(self.board[2])>=1:
            #~ res = res+ (self.board[2][0]) *3; # Card in stack 2
        #~ if len(self.board[2])==2:
            #~ res = res+ (self.board[2][1]) *6; # Card in stack 2
        #~ if len(self.board[3])>=1:
            #~ res = res+ (self.board[3][0]) *18; # Card in stack 2
        #~ if len(self.board[3])>=2:
            #~ res = res+ (self.board[3][1]) *18; # Card in stack 2
        #~ if len(self.board[3])==3:
            #~ res = res+ (self.board[3][2]) *18; # Card in stack 2

