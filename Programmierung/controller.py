from window import window
import login
from login import s_id
import os
os.system('cls')


winx = window(s_id)
def Game_loop():
    while winx.running:
        winx.event_loop()
Game_loop()