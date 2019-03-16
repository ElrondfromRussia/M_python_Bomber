from tkinter import *


class Asker(Toplevel):
    def __init__(self, parent=None):
        Toplevel.__init__(self, parent)
        #self.pack()
        self.mummy = None
        self.ent1 = None
        self.ent2 = None
        self.str1 = StringVar()
        self.str2 = StringVar()
        self.buf1 = 0
        self.buf2 = 0
        self.make_form()

    def set_default(self, n, b):
        self.str1.set(n)
        self.str2.set(b)
        self.buf1 = eval(n)
        self.buf2 = eval(b)

    def sem_mummy(self, mummy):
        self.mummy = mummy

    def make_form(self):
        row1 = Frame(self)
        lab1 = Label(row1, width=5, text='Size')
        self.ent1 = Entry(row1)
        self.ent1.config(textvariable=self.str1)
        row1.pack(side=TOP, fill=X)
        lab1.pack(side=LEFT)
        self.ent1.pack(side=RIGHT, expand=YES, fill=X)

        row2 = Frame(self)
        lab2 = Label(row2, width=5, text='Bombs')
        self.ent2 = Entry(row2)
        self.ent2.config(textvariable=self.str2)
        row2.pack(side=TOP, fill=X)
        lab2.pack(side=LEFT)
        self.ent2.pack(side=RIGHT, expand=YES, fill=X)

        btn = Button(self, text='Apply')
        btn.pack(side=TOP, fill=X)
        btn.config(command=self.send_apply)

    def send_apply(self):
        if (self.ent1.get() is "") or (self.ent2.get() is ""):
            self.mummy.apply_all(self.buf1, self.buf2)
        else:
            self.mummy.apply_all(eval(self.ent1.get()), eval(self.ent2.get()))


if __name__ == '__main__':
    MyAsker = Asker()
    MyAsker.mainloop()
