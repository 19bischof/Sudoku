from tkinter import *
from pprint import pprint
from lorem.text import TextLorem
import names
import tkinter
import database

wind = tkinter.Tk()
# database.get_codenames_and_userdata()
left = Listbox(wind,font="Calibri 20",listvariable=StringVar(value = names.j_names))
right = Listbox(wind,font="Calibri 20",listvariable=StringVar(value = [TextLorem(srange=(5,9))._word() for x in range(100)]))
scroll = Scrollbar(wind)


def right_scroll(*args):
    right.yview_moveto(args[0])
    scroll.set(*args)

def left_scroll(*args):
    left.yview_moveto(args[0])
    scroll.set(*args)

def left_right(*args):
    left.yview(*args)
    right.yview(*args)

def right_select(*args):
    i = right.curselection()
    if i == ():
        return
    i = i[0]
    print(i)
    right.selection_clear(0,tkinter.END)
    left.activate(i)
    left.selection_set(i,i)
    


right.bind("<<ListboxSelect>>",right_select)
right.bind("<FocusIn>",lambda e: left.focus_set())

wind.resizable(False,False)
left.configure(width=12,yscrollcommand=right_scroll,highlightthickness=0,borderwidth=0,foreground="white",background="crimson",selectforeground="black",selectbackground='yellow')
right.configure(width=12,yscrollcommand=left_scroll,highlightthickness=0,borderwidth=0,foreground="white",background="crimson",selectforeground="black",selectbackground='yellow')
scroll.configure(command=left_right)


    


left.grid(column=1,row=1)
right.grid(column=2,row=1)
scroll.grid(column=3,row=1,sticky="ns")




wind.winfo_toplevel().title("serious")
wind.mainloop()