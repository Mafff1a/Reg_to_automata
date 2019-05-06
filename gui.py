# -*- coding: utf-8 -*-
import automatatheory
from automatatheory import *
import Tkinter
import os
from Tkinter import *

tk = Tkinter.Tk()
text = Tkinter.Entry(tk)
text.pack()
relabel = Tkinter.Label(tk, text="RE:")
string = Tkinter.Label(tk, text="String to test:")
acceptlabel = Tkinter.Label(tk, text="")
cmptext = Tkinter.Entry(tk)
cmptext.pack()


def init1():
    input = text.get()
    global NFA
    NFA = NFAfromRegex(input)
    min = NFA.getNFA()
    global DFA
    DFA = DFAfromNFA(min)


def ShowNFA():
    NFA.displayNFA()


def ShowDFA():
    DFA.displayDFA()


def ShowMinDFA():
    DFA.displayMinimisedDFA()


def ButtonClick(btn):
    if btn == "i":
        init1()
    elif btn == 'N':
        ShowNFA()
    elif btn == 'D':
        ShowDFA()
    elif btn == 'M':
        ShowMinDFA()
    elif btn == "C":
        txt = cmptext.get()
        b = DFA.acceptsString(txt)
        if (b):
            show = "True"
        else:
            show = "False"
        acceptlabel.config(text=show)


tk.geometry("600x550")
NFABTN = Tkinter.Button(tk, text='NFA', command=lambda: ButtonClick('N'))
INITBTN = Tkinter.Button(tk, text='INIT', command=lambda: ButtonClick('i'))
DFABTN = Tkinter.Button(tk, text='DFA', command=lambda: ButtonClick('D'))
MDFABTN = Tkinter.Button(tk, text='MINDFA', command=lambda: ButtonClick('M'))
CMPBTN = Tkinter.Button(tk, text='TEST', command=lambda: ButtonClick('C'))

tk.title("RE to AUTOMATA")
text.place(x=150, y=50, width=300, height=45)
acceptlabel.place(x=150, y=250, width=70, height=25)
cmptext.place(x=150, y=390, width=300, height=45)
INITBTN.place(x=40, y=150, width=75, height=25)
string.place(x=40, y=400, width=90, height=25)
relabel.place(x=120, y=60, width=20, height=25)
NFABTN.place(x=40, y=200, width=75, height=25)
CMPBTN.place(x=40, y=350, width=75, height=25)
DFABTN.place(x=40, y=250, width=75, height=25)
MDFABTN.place(x=40, y=300, width=75, height=25)
tk.mainloop()
