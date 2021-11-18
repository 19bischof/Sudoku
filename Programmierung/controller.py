from window import window
import login
import choose_name
import os

os.system('cls' if os.name.startswith('nt') else 'clear')


s_id = login.tk_login()
if s_id is None:
    s_id = login.cli_login()
print(s_id)
chosen_hash = choose_name.choose_sud(s_id)
winx = window(s_id,chosen_hash)
def Game_loop():
    while winx.running:
        winx.event_loop()
Game_loop()