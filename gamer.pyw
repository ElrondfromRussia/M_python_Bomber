#from tkinter import *
from tkinter import font
from sapcell import *
from asker import *
import random


##############################################################
class Gamer(Tk):
    def __init__(self, parent=None):
        Tk.__init__(self, parent)
        self.parent = parent
        self.cells = []
        self.size = 9
        self.bombs = 10
        self.b_temp = 10
        self.max_size = 30
        self.min_size = 9
        self.max_bombs = 200
        self.min_bombs = 10
        self.lb = None
        self.bombMatrix = []
        self.make_grid()
        self.make_bomb_matrix()

##############################################################
    def loser(self):
        for btn in self.cells:
            btn.iflose()

    def win(self):
        for btn in self.cells:
            btn.end = 1
            btn.config(bg='green', text="!")

    def bomb_set(self, bb):
        if bb == 1:
            self.b_temp += 1
        else:
            if bb == -1:
                self.b_temp -= 1
        self.set_labl(self.b_temp)

    def apply_all(self, size, bombs):
        if (size >= self.min_size) and (size <= self.max_size):
            self.size = size
        if (bombs >= self.min_bombs) and (bombs <= self.max_bombs):
            self.bombs = bombs
        self.clearField()

    def clearField(self):
        self.new_game()

##############################################################
    def get_matrix(self):
        return self.matrix

    def on_count_Bobms(self, index):
        res = 0
        res += self.bombMatrix.__contains__(index + self.size - 1) \
               * (index % self.size != 0 and index < (self.size * (self.size - 1)))
        res += self.bombMatrix.__contains__(index + self.size + 1) \
               *((index+1) % self.size != 0 and index < (self.size * (self.size - 1)))
        res += self.bombMatrix.__contains__(index + self.size) * (index < (self.size * (self.size - 1)))
        res += self.bombMatrix.__contains__(index - self.size - 1) * (index % self.size != 0 and index >= self.size)
        res += self.bombMatrix.__contains__(index - self.size + 1) * ((index + 1) % self.size != 0 and index >= self.size)
        res += self.bombMatrix.__contains__(index - self.size) * (index >= self.size)
        res += self.bombMatrix.__contains__(index - 1) * (index % self.size != 0)
        res += self.bombMatrix.__contains__(index + 1) * ((index + 1) % self.size != 0)
        return res

    def check_field(self):
        field_full = 1
        for btn in self.cells:
            if btn.checked == 0 and btn.isFlag == 0:
                field_full = 0
                break
        field_full = field_full * (self.b_temp == 0)
        if field_full:
            self.win()

##############################################################
    def new_game(self):
        self.make_grid()
        self.make_bomb_matrix()

    def make_bomb_matrix(self):
        self.bombMatrix = []
        self.b_temp = self.bombs
        bom = self.b_temp
        if self.b_temp <= (self.size * self.size):
            while bom > 0:
                resa = random.randrange(self.size*self.size)
                if self.bombMatrix.__contains__(resa):
                    a = 1
                else:
                    self.bombMatrix.append(resa)
                    self.cells.__getitem__(resa).isBomb = 1
                    bom -= 1

    def set_labl(self, n):
        self.lb.config(text="Bombs = " + n.__str__())

    def destroy_all(self):
        for child in self.winfo_children(): child.destroy()

    def make_grid(self):
        ind = 0
        self.cells.clear()
        self.destroy_all()
        self.lb = Label(self, text="Bombs = " + self.bombs.__str__())
        self.lb.pack(side=TOP, fill=BOTH)
        for i in range(self.size):
            frm = Frame(self)
            frm.pack(side=TOP, expand=YES, fill=BOTH)
            for i in range(self.size):
                cell = SaperCell(frm)
                self.cells.append(cell)
                cell.set_index(ind)
                cell.set_BIG_MUM(self)
                cell.config(text=' ', bg='gray', width=2, height=1,
                            font=font.Font(weight='bold'))
                cell.pack(side=LEFT, pady=1, expand=YES, fill=BOTH)
                ind += 1
                cell.bind('<Button-1>', cell.openb)
                cell.bind('<Button-3>', cell.flagb)
                cell.bind('<Enter>', cell.select_it)
                cell.bind('<Leave>', cell.deselect_it)
        top = Menu(self)
        self.config(menu=top)
        top.add_command(label='New game', command=self.clearField)
        top.add_command(label='Settings', command=self.open_settings)

##############################################################
    def check_right(self, index):
        if (index+1) % self.size > 0:
            k = self.cells.__getitem__(index + 1).depper_opener()
            if self.cells.__getitem__(index + 1).deep == 1:
                self.check_right(index + 1)
                self.check_right_up_dia(index + 1)
                self.check_right_down_dia(index + 1)

    def check_left(self, index):
        if index % self.size > 0:
            k = self.cells.__getitem__(index - 1).depper_opener()
            if self.cells.__getitem__(index - 1).deep == 1:
                self.check_left(index - 1)
                self.check_left_down_dia(index - 1)
                self.check_left_up_dia(index - 1)

    def check_up(self, index):
        if index >= self.size:
            k = self.cells.__getitem__(index - self.size).depper_opener()
            if self.cells.__getitem__(index - self.size).deep == 1:
                self.check_up(index - self.size)
                self.check_left_up_dia(index - self.size)
                self.check_right_up_dia(index - self.size)

    def check_down(self, index):
        if index < (self.size * (self.size - 1)):
            k = self.cells.__getitem__(index + self.size).depper_opener()
            if self.cells.__getitem__(index + self.size).deep == 1:
                self.check_down(index + self.size)
                self.check_right_down_dia(index + self.size)
                self.check_left_down_dia(index + self.size)

    def check_right_up_dia(self, index):
        if ((index+1) % self.size > 0) and (index >= self.size):
            k = self.cells.__getitem__(index - self.size + 1).depper_opener()
            if self.cells.__getitem__(index - self.size + 1).deep == 1:
                self.check_right_up_dia(index - self.size + 1)
                if (index - self.size + 1 + 1 >= 0) and (index - self.size + 1 + 1 < self.size * self.size):
                    if self.cells.__getitem__(index - self.size + 1 + 1).checked == 0:
                        self.check_right(index - self.size + 1)
                if (index - self.size + 1 - self.size >= 0) and (index - self.size + 1 - self.size < self.size * self.size):
                    if self.cells.__getitem__(index - self.size + 1 - self.size).checked == 0:
                        self.check_up(index - self.size + 1)
                if (index - self.size + 1 + self.size >= 0) and (index - self.size + 1 + self.size < self.size * self.size):
                    if self.cells.__getitem__(index - self.size + 1 + self.size).checked == 0:
                        self.check_down(index - self.size + 1)
                if (index - self.size + 1 + self.size + 1 >= 0) and (index - self.size + 1 + self.size + 1 < self.size * self.size):
                    if self.cells.__getitem__(index - self.size + 1 + self.size + 1).checked == 0:
                        self.check_right_down_dia(index - self.size + 1)
                if (index - self.size + 1 - self.size - 1 >= 0) and (index - self.size + 1 - self.size - 1 < self.size * self.size):
                    if self.cells.__getitem__(index - self.size + 1 - self.size - 1).checked == 0:
                        self.check_left_up_dia(index - self.size + 1)

    def check_right_down_dia(self, index):
        if ((index+1) % self.size > 0) and (index < self.size*(self.size - 1)):
            k = self.cells.__getitem__(index + self.size + 1).depper_opener()
            if self.cells.__getitem__(index + self.size + 1).deep == 1:
                self.check_right_down_dia(index + self.size + 1)
                if (index + self.size + 1 + 1 >= 0) and (index + self.size + 1 + 1 < self.size * self.size):
                    if self.cells.__getitem__(index + self.size + 1 + 1).checked == 0:
                        self.check_right(index + self.size + 1)
                if (index + self.size + 1 - self.size >= 0) and (index + self.size + 1 - self.size < self.size * self.size):
                    if self.cells.__getitem__(index + self.size + 1 - self.size).checked == 0:
                        self.check_up(index + self.size + 1)
                if (index + self.size + 1 + self.size >= 0) and (index + self.size + 1 + self.size < self.size * self.size):
                    if self.cells.__getitem__(index + self.size + 1 + self.size).checked == 0:
                        self.check_down(index + self.size + 1)
                if (index + self.size + 1 - self.size + 1 >= 0) and (index + self.size + 1 - self.size + 1 < self.size * self.size):
                    if self.cells.__getitem__(index + self.size + 1 - self.size + 1).checked == 0:
                        self.check_right_up_dia(index + self.size + 1)
                if (index + self.size + 1 + self.size - 1 >= 0) and (index + self.size + 1 + self.size - 1 < self.size * self.size):
                    if self.cells.__getitem__(index + self.size + 1 + self.size - 1).checked == 0:
                        self.check_left_down_dia(index + self.size + 1)

    def check_left_up_dia(self, index):
        if (index % self.size > 0) and (index >= self.size):
            k = self.cells.__getitem__(index - self.size - 1).depper_opener()
            if self.cells.__getitem__(index - self.size - 1).deep == 1:
                self.check_left_up_dia(index - self.size - 1)
                if (index - self.size - 1 - 1 >= 0) and (index - self.size - 1 - 1 < self.size * self.size):
                    if self.cells.__getitem__(index - self.size - 1 - 1).checked == 0:
                        self.check_left(index - self.size - 1)
                if (index - self.size - 1 - self.size >= 0) and (index - self.size - 1 - self.size < self.size * self.size):
                    if self.cells.__getitem__(index - self.size - 1 - self.size).checked == 0:
                        self.check_up(index - self.size - 1)
                if (index - self.size - 1 + self.size >= 0) and (index - self.size - 1 + self.size < self.size * self.size):
                    if self.cells.__getitem__(index - self.size - 1 + self.size).checked == 0:
                        self.check_down(index - self.size - 1)
                if (index - self.size - 1 + self.size - 1 >= 0) and (index - self.size - 1 + self.size - 1 < self.size * self.size):
                    if self.cells.__getitem__(index - self.size - 1 + self.size - 1).checked == 0:
                        self.check_left_down_dia(index - self.size - 1)
                if (index - self.size - 1 - self.size + 1 >= 0) and (index - self.size - 1 - self.size + 1 < self.size * self.size):
                    if self.cells.__getitem__(index - self.size - 1 - self.size + 1).checked == 0:
                        self.check_right_up_dia(index - self.size - 1)

    def check_left_down_dia(self, index):
        if (index % self.size > 0) and (index  < self.size*(self.size - 1)):
            k = self.cells.__getitem__(index + self.size - 1).depper_opener()
            if self.cells.__getitem__(index + self.size - 1).deep == 1:
                self.check_left_down_dia(index + self.size - 1)
                if (index + self.size - 1 - 1 >= 0) and (index + self.size - 1 - 1 < self.size * self.size):
                    if self.cells.__getitem__(index + self.size - 1 - 1).checked == 0:
                        self.check_left(index + self.size - 1)
                if (index + self.size - 1 - self.size >= 0) and (index + self.size - 1 - self.size < self.size * self.size):
                    if self.cells.__getitem__(index + self.size - 1 - self.size).checked == 0:
                        self.check_up(index + self.size - 1)
                if (index + self.size - 1 + self.size >= 0) and (index + self.size - 1 + self.size < self.size * self.size):
                    if self.cells.__getitem__(index + self.size - 1 + self.size).checked == 0:
                        self.check_down(index + self.size - 1)
                if (index + self.size - 1 - self.size - 1 >= 0) and (index + self.size - 1 - self.size - 1 < self.size * self.size):
                    if self.cells.__getitem__(index + self.size - 1 - self.size - 1).checked == 0:
                        self.check_left_up_dia(index + self.size - 1)
                if (index + self.size - 1 + self.size + 1 >= 0) and (index + self.size - 1 + self.size + 1 < self.size * self.size):
                    if self.cells.__getitem__(index + self.size - 1 + self.size + 1).checked == 0:
                        self.check_right_down_dia(index + self.size - 1)

    def openall(self, ind):
        self.check_right(ind)
        self.check_right_up_dia(ind)
        self.check_up(ind)
        self.check_left_up_dia(ind)
        self.check_left(ind)
        self.check_left_down_dia(ind)
        self.check_down(ind)
        self.check_right_down_dia(ind)

##############################################################
    def open_settings(self):
        asker = Asker(self)
        asker.sem_mummy(self)
        asker.set_default(self.size.__str__(), self.bombs.__str__())
        asker.mainloop()

##############################################################


if __name__ == '__main__':
    MyGame = Gamer()
    MyGame.mainloop()
