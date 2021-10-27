import json

class Sudoku:
    def __init__(self):
        self.load_grid()

    def load_grid(self):
        with open('editable_Sudokus.json','r') as the_json:
            raw_grid = json.load(the_json)
            self.grid = raw_grid['board']
    def set_value(self,i,ii,value):
        self.grid[i][ii] = value
