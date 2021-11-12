from window import window
import login
import tk_test
import os

os.system('cls' if os.name.startswith('nt') else 'clear')


s_id = login.tk_login()
if s_id is None:
    s_id = login.cli_login()
    
choose_hash = tk_test.choose_sud(s_id)
winx = window(s_id,choose_hash)
def Game_loop():
    while winx.running:
        winx.event_loop()
Game_loop()