# -*- coding: utf-8 -*-
import Stick
import Disk

R = 1
G = 2
B = 3

class State():
    
    def __init__(self):
        self.sticks={1: Stick.Stick(1), 2: Stick.Stick(2), 3: Stick.Stick(3)}
        
        self.sticks[2].add_disk(Disk.Disk(G))
        self.sticks[2].add_disk(Disk.Disk(B))
        self.sticks[1].add_disk(Disk.Disk(R))

        #self.sticks = {1: [], 2:[], 3: [B,R,G]}
        
    def available_move(self, src, dst):
        if len(self.sticks[src])==0:
            return False
        if len(self.sticks[dst])== dst:
            return False
            
        return True

    def get_disk(self, disk_num):
        for (k,v) in self.sticks.items():
            dd= [ x for x in v.disks]
            for x in dd:
                if x.num == disk_num:
                    return x
        
        print "ERROR, no such disk_num"

    def get_stick_of_disk(self, disk_num):
        for (k,v) in self.sticks.items():
            dd= [ x for x in v.disks]
            for x in dd:
                if x.num == disk_num:
                    return v
        
        print "ERROR, no such disk_num", disk_num, "...\n"
                
    def get_disk_position(self, disk_num):
        for (k,v) in self.sticks.items():
            dd= [ x.num for x in v.disks]
            if dd.count(disk_num):
                return (k, dd.index(disk_num)+1)
        
        print "ERROR, no such to disk_num", disk_num, "...\n"

    def move(self, disknum, sticknum):
        src_stick = self.get_stick_of_disk(disknum)
        
        d = src_stick.remove_disk()
        self.sticks[sticknum].add_disk(d)

    def moveSP(self, diskSP, stickSP):
        
        self.move(diskSP.disk.num, stickSP.stick.num)
         
        
        diskSP.set_stick_pos(self.get_disk_position(diskSP.disk.num))
        print self.get_disk_position(diskSP.disk.num)
        print diskSP.rect.midbottom
        self.show()

    def get_board_number(self):
        order = self.sticks[1].disks + self.sticks[2].disks + self.sticks[3].disks
        order = [ x.num for x in order]
        order_sum = sum([ 1*(len(order)-x-1)  for x in range(len(order)) for i in range(x, len(order)) if order[x]>order[i]])

        kind_board = [ len(self.sticks[i].disks) for i in self.sticks.keys()]
        
        if kind_board[2]==0:
            kind_board_num = 0
        elif kind_board[2]==1:            
            kind_board_num = kind_board[2] + kind_board[1]-1
        elif kind_board[2]==2:            
            kind_board_num = kind_board[2] + kind_board[1]+1
        elif kind_board[2]==3:            
            kind_board_num = kind_board[2] + 2
        
        return kind_board_num * 6 + order_sum

    def set_board_number(self, n):
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
        
        #self.sticks={1: Stick.Stick(1), 2: Stick.Stick(2), 3: Stick.Stick(3)}
        disks = []
        print self.sticks
        for s in self.sticks.values():
            for _ in range(3):
                d = s.remove_disk()
                if d is not None:
                    disks.append(d)
        
        for i in range(len(layout)):
            for _ in range(layout[i]):
                print disks
                v = relative_blocks_order.pop()
                idx = [x.num for x in disks].index(v)
                cur_disk = disks[idx]
                self.sticks[i+1].add_disk(cur_disk)
                disks.pop(idx)
        
    def show(self):
        p1_1 = to_text(self.sticks[1].disks[0].num) if len(self.sticks[1].disks) else "|"
        p2_1 = to_text(self.sticks[2].disks[0].num) if len(self.sticks[2].disks) else "|"
        p2_2 = to_text(self.sticks[2].disks[1].num) if len(self.sticks[2].disks) == 2 else "|"
        p3_1 = to_text(self.sticks[3].disks[0].num) if len(self.sticks[3].disks) else "|"
        p3_2 = to_text(self.sticks[3].disks[1].num) if len(self.sticks[3].disks) >= 2 else "|"
        p3_3 = to_text(self.sticks[3].disks[2].num) if len(self.sticks[3].disks) == 3 else "|"

        print "              %c" % (p3_3,)
        print "        %c     %c" % (p2_2, p3_2)
        print "  %c     %c     %c" % (p1_1, p2_1, p3_1)
        #~ print "-----------------" 
        print "--1-----2-----3--   El tablero es el número %d" % self.get_board_number()
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
        
def to_text(l):
    if l==R:
        return "R"
    if l==B:
        return "B"
    if l==G:
        return "G"