from tkinter import *
import tkinter
import database
import time

s_id = ""
general_bg = '#3495eb'

def close():
    label_entry_1.grid_remove()
    label_entry_2.grid_remove()
    label_entry_3.grid_remove()
    entry1.grid_remove()
    entry2.grid_remove()
    entry3.grid_remove()
    login_button.grid_remove()
    winx.update()
    time.sleep(2)
    winx.quit()
def try_login():
    global s_id
    s_id = database.login_user(entry_1_var.get().strip(),entry_2_var.get().strip())
    if s_id == "Username doesn't exist":
        result_label.configure(text="User and Password do not exist")
        result_label.grid(row=7)
        register_button.grid(row=6)
    else:
        result_label.configure(text="You are logged in as "+entry_1_var.get())
        close()
def register_user():
    global s_id
    if label_entry_3.grid_info() == {}:
        label_entry_1.configure(text="Username:")
        label_entry_2.configure(text="Password:")
        # entry_1_var.set("")
        # entry_2_var.set("")
        result_label.configure(text="")
        label_entry_3.grid(row=4)
        entry3.grid(row=5)
    else:
        u_name = entry_1_var.get().strip()
        if u_name == "":
            result_label.configure(text="Invalid Username")
            return
        pass1 = entry_2_var.get().strip()
        pass2 = entry_3_var.get().strip()
        if pass1 != pass2:
            result_label.configure(text="The Passwords are different")
            return
        database.register_new_user(u_name,pass1)
        s_id = database.login_user(u_name,pass1)
        result_label.configure(text="You are logged in as "+entry_1_var.get())
        close()

winx = tkinter.Tk()
winx.winfo_toplevel().title("login")
winx.eval('tk::PlaceWindow . center')
winx.geometry("200x200")
winx.configure(background=general_bg,)
winx.bind("<Return>",lambda t: try_login())


label_entry_1 = tkinter.Label(winx,text="Username:",background=general_bg)
label_entry_2 = tkinter.Label(winx,text="Password:",background=general_bg)
label_entry_3 = tkinter.Label(winx,text="Repeat the Password",background=general_bg)
entry_1_var = StringVar()
entry_2_var = StringVar()
entry_3_var = StringVar()
entry1 = tkinter.Entry(winx,textvariable=entry_1_var)
entry2 = tkinter.Entry(winx,textvariable=entry_2_var,show="*")
entry3 = tkinter.Entry(winx,textvariable=entry_3_var,show="*")

login_button = tkinter.Button(winx,text="Login",command=try_login,background='lightblue')
register_button = tkinter.Button(winx,text="Register new User",command=register_user,background='lightblue')

result_label = tkinter.Label(winx,text="",background=general_bg)



winx.grid_columnconfigure(0,weight=1)


label_entry_1.grid(row=0)
entry1.grid(row=1)
label_entry_2.grid(row=2)
entry2.grid(row=3)
login_button.grid(row=6)

winx.mainloop()