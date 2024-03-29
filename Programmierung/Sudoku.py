from pprint import pprint
import json
from settings import settings as st
import database
import msvcrt
import time
class Sudoku:
    
    def __init__(self,s_id,hash = None):
        self.error = ""
        print(hash)
        self.old_seconds = 0
        self.session_id = s_id
        self.load_grid_from_db(hash)    
        self.completed = False
        self.username,self.codename = database.get_user_and_sud_name_from_session_id(self.session_id)
        self.hash = hash

    def determine_changes(self):
        changed = [[0 for x in range(9)] for x in range(9)]
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] != self.raw_grid[r][c]:
                    if self.check_if_obviously_wrong((r,c)):
                        changed[r][c] = 4
                    else:
                        changed[r][c] = 3
        self.changes = changed
    def load_grid_from_db(self,hash = None):
        res = database.get_edited_raw_solved_Sudoku_and_seconds_and_completed(self.session_id,hash)   #grid_current,grid_raw,grid_solved
        print(res)
        g_c,g_r,g_s,seconds,completed,best_time = res
        if completed:
            print("resetting...")
            g_c = g_r
            time.sleep(1)
            seconds = 0
        if seconds != None:
            self.old_seconds = seconds
        self.time_sud = time.time()
        if g_c == "not valid session_id":
            self.error += g_c
            print("not valid session id")
            quit()
        self.grid = json.loads(g_c)['board']
        self.raw_grid = json.loads(g_r)['board']
        self.best_time = best_time
        pprint(self.grid)
        pprint(self.raw_grid)
        self.determine_changes()
        
        # self.solved_grid = json.loads(g_s)['board']

    def update_db_with_data(self):
        seconds_on_sud = self.old_seconds + int(time.time() - self.time_sud)
        print(seconds_on_sud,"seconds!")
        database.update_edited_Sudoku(self.session_id,{'board':self.grid},seconds_on_sud,self.completed)

    def set_value(self,i,ii,value):
        if value == 0:
            self.grid[i][ii]= 0
            return "reset"
        self.grid[i][ii] = value
        if st.crude_checking:
            resp = self.check_if_obviously_wrong((i,ii))
            if resp:
                print("Help: This number already exists in its",resp)
                return "bad"
            else:
                nozero = True
                print("checking")
                for r in range(9):
                    for c in range(9):
                        if self.grid[r][c] == 0:
                            nozero = False
                if nozero == True:
                    print("well_lets end it here!")
                    self.completed = True
                    self.update_db_with_data()
                    return "completed"
    


    def check_if_obviously_wrong(self,pos):
        the_value = self.grid[pos[0]][pos[1]]
        for i in range(9):  #check row
            if i != pos[1]:
                if self.grid[pos[0]][i] == the_value:
                    return "row"

        for i in range(9):  #check column
            if i != pos[0]:
                if self.grid[i][pos[1]] == the_value:
                    return "column"
        #get quadrant
        x = int(pos[1]/3)
        y = int(pos[0]/3)
        for c in range(x*3,3+x*3):
            for r in range(y*3,3+y*3):
                if (r,c) != pos:
                    if self.grid[r][c] == the_value:
                        return "area"
        return False
