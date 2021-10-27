from window import window

winx = window()
def Game_loop():
    while winx.running:
        winx.event_loop()
Game_loop()