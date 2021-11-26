from tkinter import *
from tkinter import ttk
from pprint import pprint
import tkinter
import database
# from controller import s_id

def choose_sud(s_id):
    choice_i = None
    wind = tkinter.Tk()
    
    def restart_sud(*args):
        print(*args)

    def sortby(col_index):
        tree.selection_remove(tree.get_children())


        rows = [[] for x in lon]
        for index,n in enumerate(lon):
            rows[index].append(n)
        for index,s in enumerate(los):
            rows[index].append(s)
        for index,c in enumerate(loc):
            rows[index].append(c)
        for index,b in enumerate(lob):
            rows[index].append(b)                
        if col_index %2 == 0:
            rows.sort(key=lambda x:x[col_index])
        elif col_index %2 == 1:
            rows.sort(key=lambda x:int(x[col_index][:len(x[col_index])-2]),reverse = True)
        for i,r in enumerate(rows):
            tree.insert('',i,values = r)

    username = database.get_user_from_session_id(s_id)
    global lot,lon,loh,los,loc,lob
    lot = database.get_codenames_and_hashes_and_userdata(s_id)
    lon = [x[0] for x in lot]                   #list of names
    loh = [x[1] for x in lot]                   #list of hash
    los = ["0 s" if x[2] is None else str(x[2]) + " s" for x in lot]                   #list of seconds
    loc = ["Done" if x[3]==1 else "Not Done" for x in lot]          #list of completed
    lob = ["0 s" if x[4] == None or x[4] == 0 else str(x[4]) + " s" for x in lot]                    #list of best_time
    # los = [x[2] if x[2] != None else 0 for x in lot] 

    # lob = [x[4] if x[4] != None else 0 for x in lot] 
    

    scroll = Scrollbar(wind)

    columns = ['Names','seconds','completed','best_time']
    tree = ttk.Treeview(wind,columns=columns,show='headings',selectmode='browse')
    pcorn = Menu(tree,tearoff=0)
    pcorn.add_command(label="Restart",command=restart_sud)
    tree.heading(column=0,text='Names',command=lambda :sortby(0))
    tree.heading(column=1,text='Seconds Played',command=lambda :sortby(1))
    tree.heading(column=2,text='Completed',command=lambda :sortby(2))
    tree.heading(column=3,text='Fastest Time',command=lambda :sortby(3))
    rows = [[] for x in lon]
    for index,n in enumerate(lon):
        rows[index].append(n)
    for index,s in enumerate(los):
        rows[index].append(s)
    for index,c in enumerate(loc):
        rows[index].append(c)
    for index,b in enumerate(lob):
        rows[index].append(b)                
    
    for i,r in enumerate(rows):
        tree.insert('',i,values = r)
    
    tree.column(0,width=90)
    tree.column(1,width=132)
    tree.column(2,width=112)
    tree.column(3,width=90)

    tree.selection_set('I001')

    def selected(*args):
        nonlocal choice_i
        s = tree.selection()
        if len(s) != 1:
            #nothing selected again after clicking on heading
            return
        s = s[0][1:]    #from tuple to string with I in front to number in string
        s = int(s)      #to int
        s -= 1          #because first element has value 1
        choice_i = s
        
    def chosen(*args):
        if tree.selection():
            wind.destroy()

    def popup(event):
        print("x:",event.x,"y:",event.y,dir(event),"delta:",event.delta,"num:",event.num)
        # tree.selection(event)
        tree.event_generate('<Button-1>',x=event.x,y=event.y)
        pcorn.tk_popup(event.x_root,event.y_root,0)


    tree.configure(yscrollcommand=scroll.set)
    scroll.configure(command=tree.yview)

    tree.bind('<Button-3>',popup)
    tree.bind('<Double-Button-1>',chosen)
    tree.bind('<<TreeviewSelect>>', selected)

    tree.grid(row=0,column=0,sticky="nswe")
    scroll.grid(row=0,column=1,sticky="ns")




        






    wind.resizable(False,False)
    wind.winfo_toplevel().title("progress - "+username)
    wind.eval("tk::PlaceWindow . center")

    wind.mainloop()

    if choice_i is not None:
        return loh[choice_i]








if __name__ == "__main__":
    s_id = database.login_user('solution',"cillitbang")
    choose_sud(s_id)












def choose_sud_old_meaning_with_listboxes_and_deprecated_because_unhandy(s_id):
    choice_i = None
    wind = tkinter.Tk()
    
    username = database.get_user_from_session_id(s_id)
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
