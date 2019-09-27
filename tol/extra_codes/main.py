# -*- coding: utf-8 -*-
import csv
from props import *
from utils_pygame import *
from TowerOfLondon import *

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

    if dist not in list(range(1,9)):
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


def distance_groups():
    d = [ ([ -1  for _ in range(36) ]) for _ in range(36) ]
    get_distances(d)

    res = [ ([ []  for _ in range(8+1) ]) for _ in range(6) ]

    for idx in range(len(res)):
        for j in range(len(res[idx])):
            a = sorted([i//6 for i,k in enumerate(d[idx*6]) if k==j])
            res[idx][j]=dict((i,a.count(i)) for i in a)
            # print dict((i,a.count(i)) for i in a)

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
    for k in list(src.board.keys()):
        if len(src.board[k]):
            for h in range(len(src.board[k])):
                if len(dst.board[k])>h:
                   if dst.board[k][h]==src.board[k][h]:
                        res=res+1
    return res


def all_data(dist):
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

    for src in range(36):
        for dst in range(36):
            if src==dst:
                continue

            t_src.set_board_number(src)
            t_dst.set_board_number(dst)
            p = get_all_minimum_paths(dist, src, dst)

            src_family = get_papercode(src)//10
            dst_family = get_papercode(dst)//10
            paper_i = str(get_papercode(src))
            paper_f = str(get_papercode(dst))


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

    with open('generated_files/full_cases.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(header + res)
    return res


def equivalence_trials(dist):
    res = []
    header = [( "src",
                "goal",
                "equiv_src",
                "equiv_goal",
                "distance",
                "num_paths"),]

    base_boards = [i*6 for i in range(6)]
    t_src = TowerOfLondon()
    t_dst = TowerOfLondon()
    t_src_equiv = TowerOfLondon()
    t_dst_equiv = TowerOfLondon()
    for src in range(36):
        for dst in range(36):
            t_src.set_board_number(src)
            t_dst.set_board_number(dst)
            if src==dst:
                continue

            p = get_all_minimum_paths(dist, src, dst)
            a_path = p[0]

            if src in base_boards:
                src_equiv = src
                dst_equiv = dst
            else:
                src_kind_board = t_src.get_board_arrangement_number()
                src_equiv = 6 * src_kind_board
                t_src_equiv.set_board_number(src_equiv)
                current_equive = a_path[0]
                for next_b in a_path[1:]:
                    (f,t) = t_src.which_move(next_b)
                    t_src.move(f,t)
                    t_src_equiv.move(f,t)
                dst_equiv = t_src_equiv.get_board_number()

            line = ( src, #"Tablero inicial",
                    dst, #"Tablero final",
                    src_equiv, #"Tablero inicial",
                    dst_equiv, #"Tablero final",
                    len(a_path)-1, #"Long",
                    len(p), #"Cantidad Caminos min",
            )
            res.append(line)

    with open('generated_files/equiv_paths.csv', 'w') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerows(header + res)
    return res

def generate_distances():
    dist = [ ([ -1  for _ in range(36) ]) for _ in range(36) ]
    count_min_paths = [ ([ 0  for _ in range(36) ]) for _ in range(36) ]

    _ = get_distances(dist, count_min_paths)
    nd = [ y for x in count_min_paths for y in x ]

    import json
    with open('generated_files/dist.json', 'w') as outfile:
        json.dump(dist, outfile)

    # dict_min_path = {}
    # for i in nd:
        # dict_min_path[i] = dict_min_path.setdefault(i,0) + 1
    return dist

import os
if not os.path.exists('generated_files'):
    os.makedirs('generated_files')

dist = generate_distances()
all_data(dist)
equivalence_trials(dist)


