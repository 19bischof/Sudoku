from window import window
import login
import choose_name
import os

os.system('cls' if os.name.startswith('nt') else 'clear')


s_id = login.tk_login()
if s_id is None:
    s_id = login.cli_login()
print("Session Id:",s_id)
new_loop = True

def Game_loop(chosen_hash):
    global new_loop
    winx = window(s_id,chosen_hash)
    while winx.running:
        winx.event_loop()
    if winx.completed_sud:
        new_loop = True
    else:
        new_loop = False

def new_loop():
    while new_loop:
        chosen_hash = choose_name.choose_sud(s_id)
        print("Hash:",chosen_hash)
        if chosen_hash == None:
            break
        Game_loop(chosen_hash)

new_loop()
print("Thanks for playing :)")
