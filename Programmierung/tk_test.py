from tkinter import *
from pprint import pprint
import tkinter
import database
# from controller import s_id

def choose_sud(s_id):
    choice_i = None
    wind = tkinter.Tk()
    username,codename = database.get_user_and_sud_name_from_session_id(s_id)
    lot = database.get_codenames_and_hashes_and_userdata(s_id)
    lon = [x[0] for x in lot]                   #list of names
    loh = [x[1] for x in lot]                   #list of hash
    los = ["0 s" if x[2] is None else str(x[2]) + " s" for x in lot]                   #list of seconds
    left = Listbox(wind,font="Calibri 20",listvariable=StringVar(value = lon))
    right = Listbox(wind,font="Calibri 20",listvariable=StringVar(value = los))
    scroll = Scrollbar(wind)
    left_head = Label(wind,text="Names")
    right_head = Label(wind,text="Time")

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
    
    def you_chose(*args):
        nonlocal choice_i
        ind = left.curselection()
        if ind == ():
            return
        choice_i = ind[0]
        wind.destroy()


    right.bind("<<ListboxSelect>>",right_select)
    right.bind("<FocusIn>",lambda e: left.focus_set())
    left.bind("<Double-Button-1>",you_chose)

    wind.resizable(False,False)
    left.configure(width=12,yscrollcommand=right_scroll,highlightthickness=0,borderwidth=2,foreground="white",background="#2E294E",selectforeground="black",selectbackground="#F1E9DA")
    right.configure(width=12,yscrollcommand=left_scroll,highlightthickness=0,borderwidth=2,foreground="white",background="#29374f",selectforeground="black")
    scroll.configure(command=left_right)


        

    left_head.grid(column=1,row=0)
    right_head.grid(column=2,row=0)
    left.grid(column=1,row=1)
    right.grid(column=2,row=1)
    scroll.grid(column=3,row=1,sticky="ns")




    wind.winfo_toplevel().title("progress - "+username)
    wind.eval("tk::PlaceWindow . center")
    wind.mainloop()
    if choice_i is not None:
        return loh[choice_i]

# print(choose_sud(s_id))
