from tkinter import *


##############################################################
class SaperCell(Button):
    def __init__(self, parent=None):
        Button.__init__(self, parent)
        self.pack()
        self.index = 0
        self.isBomb = 0
        self.checked = 0
        self.isFlag = 0
        self.end = 0
        self.deep = 0

    def set_index(self, index):
        self.index = index

    def select_it(self, event):
        if self.end == 0 and self.isFlag == 0 and self.checked == 0:
            self.config(bg='lightgray')

    def deselect_it(self, event):
        if self.end == 0 and self.isFlag == 0 and self.checked == 0:
            self.config(bg='gray')

    def openb(self, event):
        if self.end == 0 and self.isFlag == 0 and self.checked == 0:
            self.checked = 1
            if self.isBomb:
                self.config(bg='red')
                self.mummy.loser()
            else:
                res = self.mummy.on_count_Bobms(self.index)
                if res == 0:
                    self.config(bg='green')
                    self.deep = 1
                    self.mummy.openall(self.index)
                else:
                    self.config(bg='green')
                    self.config(text=res)
                self.mummy.check_field()

    def flagb(self, event):
        if self.end == 0 and self.checked == 0:
            if self.isFlag == 1:
                self.isFlag = 0
                self.mummy.bomb_set(1)
                self.config(bg='gray')
            else:
                self.isFlag = 1
                self.config(bg='blue')
                self.mummy.bomb_set(-1)
                self.mummy.check_field()

    def iflose(self):
        self.end = 1
        if self.isBomb:
            self.config(bg='red')
        else:
            res = self.mummy.on_count_Bobms(self.index)
            if res == 0:
                self.config(bg='green')
            else:
                self.config(bg='green')
                self.config(text = res)

    def depper_opener(self):
        k = 1
        if self.end == 0:
            self.checked = 1
            res = self.mummy.on_count_Bobms(self.index)
            if res == 0:
                self.deep = 1
                self.config(bg='green')
            else:
                self.config(bg='green')
                self.config(text = res)
            self.mummy.check_field()
        return k
##############################################################

    def set_BIG_MUM(self, mummy):
        self.mummy = mummy

