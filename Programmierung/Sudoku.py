import json

class Sudoku:
    def __init__(self):
        self.load_grid()
        print(self.grid)

    def load_grid(self):
        with open('editable_Sudokus.json','r') as the_json:
            raw_grid = json.load(the_json)
            self.grid = raw_grid['board']
