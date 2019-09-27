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

def to_text(l):
    if l==R:
        return "R"
    if l==B:
        return "B"
    if l==G:
        return "G"

def get_papercode(nro):
    # print "nro", nro
    return [y for (y,x) in translation_mycode_to_paper_code if x==nro][0]

def get_mycode(nro):
    return [x for (y,x) in translation_mycode_to_paper_code if y==nro][0]
