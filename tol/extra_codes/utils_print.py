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


def print_dist(table):
    res = ""
    for i in range(len(table)):
        #res +=  "%d  " % (i, )
        for j in range(len(table[i])):
            res += " %d " % (table[i][j], )
        res +=  "\n"

    print(res)