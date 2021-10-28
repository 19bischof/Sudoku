import json
from settings import settings as st

class Sudoku:
    def __init__(self):
        self.load_grid()

    def load_grid(self):
        with open('editable_Sudokus.json','r') as the_json:
            raw_grid = json.load(the_json)
            self.grid = raw_grid['board']

    def set_value(self,i,ii,value):
        if value == 0:
            self.grid[i][ii]= ""
            return "reset"
        self.grid[i][ii] = value
        if st.crude_checking:
            if self.check_if_obviously_wrong((i,ii)):
                return "bad"
        return None

    def check_if_obviously_wrong(self,pos):
        the_value = self.grid[pos[0]][pos[1]]
        for i in range(9):  #check row
            if i != pos[1]:
                if self.grid[pos[0]][i] == the_value:
                    return True

        for i in range(9):  #check column
            if i != pos[0]:
                if self.grid[i][pos[1]] == the_value:
                    return True
        #get quadrant
        x = int(pos[1]/3)
        y = int(pos[0]/3)
        for c in range(x*3,3+x*3):
            for r in range(y*3,3+y*3):
                if (r,c) != pos:
                    if self.grid[r][c] == the_value:
                        return True
        return False