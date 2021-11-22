
# TODO since now we got the row_quads and the column_quads correctly working we now have to use this information:
# meaning if the space in a *-quad available is the same as the number of all possible number options for this *-quad then remove this set of numbers from the rest of the
# *-quad! Also then look at the (column if row-quad,row if column-quad) !*-quad and see if there is an easy solution to be had (with crude checking if number not duplicate in
# !*-quad(row,column))
from pprint import pprint
import window
import database
import json
import time


class Solve:

    nos = (1, 2, 3, 4, 5, 6, 7, 8, 9)

    def __init__(self, g):
        self.grid = g
        self.finished = False
        self.stop = False
        self.solve_loop()

    def close(self):
        print("Error: Stopping execution")
        self.print_stack()
        self.stop = True
        # quit()

        # problem = True

    def update_stack(self):
        self.update_rows()
        self.update_columns()
        self.update_quadrants()
        self.update_row_quads()
        self.update_column_quads()
        self.update_cells()  # important that cells is last
        # this has to be after the cells are updated
        self.reduce_cells_options_via_quad_in_row_or_column()

    def valid_stack(self):
        self.check_if_rows_valid()
        self.check_if_columns_valid()
        self.check_if_quadrants_valid()
        self.check_if_row_quads_valid()
        self.check_if_column_quads_valid()
        self.check_if_cells_valid()

    def reset_stack(self):
        self.reset_rows()
        self.reset_columns()
        self.reset_quads()
        self.reset_row_quads()
        self.reset_column_quads()
        self.reset_cells()
        self.reset_guessed()

    def print_stack(self):
        self.print_rows()
        self.print_columns()
        self.print_quads()
        self.print_row_quads()
        self.print_column_quads()
        self.print_cells()
        pprint(self.grid)
        print(self.guessed)

    def reset_quads(self):
        self.quadrants = [[] for x in range(9)]

    def print_quads(self):
        print("quadrants:")
        x_quadrants = self.quadrants.copy()
        for q_no in range(9):
            print("[{}]:".format(q_no), end="")
            for n in Solve.nos:
                while n in x_quadrants[q_no]:
                    if n in x_quadrants[q_no]:
                        print(n, end=",", flush=True)
                        x_quadrants[q_no].remove(n)
            print()

    def check_if_quadrants_valid(self):
        for q_no, q in enumerate(self.quadrants):
            have = []
            for e in q:
                if e in have:
                    print("duplicate number in quadrant:", q_no)
                    self.print_quads()
                    self.guess_was_wrong()
                    self.check_if_quadrants_valid()
                    return
                have.append(e)

    def get_quadrant(self, r, c):
        quadrant = int(r/3)*3 + int(c/3)

        return quadrant

    # quadrant 0-8: top left to top right and then one row down
    def update_quadrants(self):
        global quadrants
        self.reset_quads()
        for q_no in range(9):
            for r in range(3*int(q_no/3), 3*(int(q_no/3)+1)):
                for c in range(3*(q_no % 3), (3*(q_no % 3+1))):
                    if self.grid[r][c] != 0:
                        self.quadrants[q_no].append(self.grid[r][c])
        self.check_if_quadrants_valid()

    def reset_rows(self):
        self.rows = [[] for x in range(9)]

    def print_rows(self):
        print("rows:")
        x_rows = self.rows.copy()
        for r_no in range(9):
            print("[{}]:".format(r_no), end="")
            for n in Solve.nos:
                while n in x_rows[r_no]:
                    if n in x_rows[r_no]:
                        print(n, end=",", flush=True)
                        x_rows[r_no].remove(n)
            print()

    def check_if_rows_valid(self):
        for r_no, r in enumerate(self.rows):
            have = []
            for e in r:
                if e in have:
                    print("duplicate number in row:", r_no)
                    self.print_rows()
                    self.guess_was_wrong()
                    self.check_if_rows_valid()
                    return
                have.append(e)

    def update_rows(self):
        self.reset_rows()
        for r_no in range(9):
            for c in range(9):
                if self.grid[r_no][c] != 0:
                    self.rows[r_no].append(self.grid[r_no][c])
        self.check_if_rows_valid()

    def reset_columns(self):
        self.columns = [[] for x in range(9)]

    def print_columns(self):
        print("columns:")
        x_columns = self.columns.copy()
        for c_no in range(9):
            print("[{}]:".format(c_no), end="")
            for n in Solve.nos:
                while n in x_columns[c_no]:
                    if n in x_columns[c_no]:
                        print(n, end=",", flush=True)
                        x_columns[c_no].remove(n)
            print()

    def check_if_columns_valid(self):
        for c_no, c in enumerate(self.columns):
            have = []
            for e in c:
                if e in have:
                    print("duplicate number in column:", c_no)
                    self.print_columns()
                    pprint(self.columns)
                    self.guess_was_wrong()
                    self.check_if_columns_valid()
                    return
                have.append(e)

    def update_columns(self):
        self.reset_columns()
        for c in range(9):
            for r in range(9):
                if self.grid[r][c] != 0:
                    self.columns[c].append(self.grid[r][c])
        self.check_if_columns_valid()

    def reset_cells(self):  # cells stores options for each cell (which number could be here)
        self.cells = [[[]for y in range(9)] for x in range(9)]

    def print_cells(self):
        print("cells:")
        pprint(self.cells)

    def check_if_cells_valid(self):
        for r in range(9):
            for c in range(9):
                have = []
                for e in self.cells[r][c]:
                    if e in have:
                        print("duplicate number in cells(r,c):", (r, c))
                        self.print_cells()
                        self.guess_was_wrong()
                        self.check_if_cells_valid()
                        return
                    have.append(e)

    def update_cells(self):  # 3 dim array of possible numbers per cell
        self.reset_cells()
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    for n in Solve.nos:
                        if n not in self.rows[r]:
                            if n not in self.columns[c]:
                                if n not in self.quadrants[self.get_quadrant(r, c)]:
                                    self.cells[r][c].append(n)
        self.check_if_cells_valid()

    def check_if_finished(self):
        nozero = True
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    nozero = False
        self.valid_stack()
        if nozero == True:
            print("DONE:)")
            self.finished = True

    def reset_row_quads(self):
        self.row_quads = [[[] for y in range(3)] for x in range(9)]

    def print_row_quads(self):
        print("row_quads:")
        for r_no in range(9):
            print("[{}]:".format(r_no), end="")
            for i in range(3):
                for x in self.row_quads[r_no][i]:
                    print(x, end="", flush=True)
                print(" ; ", end="", flush=True)
            print()

    def check_if_row_quads_valid(self):
        for r_no in range(9):
            for i in range(3):
                have = []
                for e in self.row_quads[r_no][i]:
                    if e in have:
                        print("duplicate number in row_quads(r_no,i):", (r_no, i))
                        self.print_cells()
                        self.guess_was_wrong()
                        self.check_if_row_quads_valid()
                        return
                    have.append(e)

    # row quads: 2 dim array: for each row there are 3 sections in it (for each quad)
    def update_row_quads(self):
        # usefule if you are not certain in which cell exactly a pair of numbers go but know
        self.reset_row_quads()  # they have to be in a specific quad
        for r_no in range(9):
            first_quad_no = int(r_no/3)*3
            for ind, q_no in enumerate(range(first_quad_no, first_quad_no+3)):
                space_available = False
                for i in range(3):
                    if self.grid[r_no][ind*3+i] == 0:
                        space_available = True
                if space_available is False:
                    # print("no space in row:{} ind:{}".format(r_no, ind))
                    continue
                for n in Solve.nos:
                    if n not in self.rows[r_no]:
                        if n not in self.quadrants[q_no]:
                            self.row_quads[r_no][ind].append(n)
        self.check_if_row_quads_valid()

    def reset_column_quads(self):
        self.column_quads = [[[] for y in range(3)] for x in range(9)]

    def print_column_quads(self):
        print("column_quads:")
        for c_no in range(9):
            print("[{}]:".format(c_no), end="")
            for i in range(3):
                for x in self.column_quads[c_no][i]:
                    print(x, end="", flush=True)
                print(" ; ", end="", flush=True)
            print()

    def check_if_column_quads_valid(self):
        for c_no in range(9):
            for i in range(3):
                have = []
                for e in self.column_quads[c_no][i]:
                    if e in have:
                        print("duplicate number in column_quads(r_no,i):", (c_no, i))
                        self.print_cells()
                        self.guess_was_wrong()
                        self.check_if_column_quads_valid()
                        return
                    have.append(e)

    # column quads: 2 dim array: for each column there are 3 sections in it (for each quad)
    def update_column_quads(self):
        # usefule if you are not certain in which cell exactly a pair of numbers go but know
        self.reset_column_quads()  # they have to be in a specific quad
        for c_no in range(9):
            first_quad_no = int(c_no/3)
            for ind, q_no in enumerate(range(first_quad_no, first_quad_no+9, 3)):
                space_available = False
                for i in range(3):
                    if self.grid[ind*3+i][c_no] == 0:
                        space_available = True
                if space_available is False:
                    # print("no space in column:{} ind:{}".format(c_no, ind))
                    continue
                for n in Solve.nos:
                    if n not in self.columns[c_no]:
                        if n not in self.quadrants[q_no]:
                            self.column_quads[c_no][ind].append(n)
        self.check_if_column_quads_valid()

    # list of dict:(row,column,set_of_options=[],cur_guess,already_guessed=[])
    def reset_guessed(self):
        # ->history of the guesses
        self.guessed = []

    def solve_for_one_solution(self):
        progress = None
        for r in range(9):
            for c in range(9):
                if len(self.cells[r][c]) == 1:
                    self.grid[r][c] = self.cells[r][c][0]
                    print("solved: row={} column={} number={}".format(
                        r, c, self.grid[r][c]))
                    # input()
                    progress = True
                    self.update_stack()

        return progress

    def reduce_cells_options_via_quad_in_row_or_column(self):
        for r_no in range(9):
            r_q = self.row_quads[r_no]
            for i in range(3):
                space = 0
                for k in range(3):
                    if self.grid[r_no][i*3+k] == 0:
                        space += 1
                if space > len(r_q[i]):
                    self.print_stack()
                    print("Error: cant be more space than options in row_quad:",
                          r_q[i], "(r_no,i,space,len)", (r_no, i, space, len(r_q[i])))
                    # print_stack()
                    self.guess_was_wrong()
                if space == len(r_q[i]):

                    for n in r_q[i]:
                        # print("reducing row options: len == options:", "(r_no,i,space,len,n)",
                            #   (r_no, i, space, len(r_q[i]), n))
                        if n in r_q[(i+1) % 3]:
                            if n in self.cells[r_no][((i+1) % 3)*3]:
                                self.cells[r_no][((i+1) % 3)*3].remove(n)
                            if n in self.cells[r_no][((i+1) % 3)*3+1]:
                                self.cells[r_no][((i+1) % 3)*3+1].remove(n)
                            if n in self.cells[r_no][((i+1) % 3)*3+2]:
                                self.cells[r_no][((i+1) % 3)*3+2].remove(n)

                        if n in r_q[(i+2) % 3]:
                            if n in self.cells[r_no][((i+2) % 3)*3]:
                                self.cells[r_no][((i+2) % 3)*3].remove(n)
                            if n in self.cells[r_no][((i+2) % 3)*3+1]:
                                self.cells[r_no][((i+2) % 3)*3+1].remove(n)
                            if n in self.cells[r_no][((i+2) % 3)*3+2]:
                                self.cells[r_no][((i+2) % 3)*3+2].remove(n)

        for c_no in range(9):
            c_q = self.column_quads[c_no]
            for i in range(3):
                space = 0
                for k in range(3):
                    if self.grid[i*3+k][c_no] == 0:
                        space += 1
                if space > len(c_q[i]):
                    self.print_stack()
                    print("Error: cant be more space than options in column_quad:",
                          c_q[i], "(c_no,i,space,len)", (c_no, i, space, len(c_q[i])))
                    self.guess_was_wrong()
                if space == len(c_q[i]):

                    for n in c_q[i]:
                        # print("reducing column options: len == options:", "(c_no,i,space,len,n)",
                        #       (c_no, i, space, len(c_q[i]), n))
                        if n in c_q[(i+1) % 3]:
                            if n in self.cells[((i+1) % 3)*3][c_no]:
                                self.cells[((i+1) % 3)*3][c_no].remove(n)
                            if n in self.cells[((i+1) % 3)*3+1][c_no]:
                                self.cells[((i+1) % 3)*3+1][c_no].remove(n)
                            if n in self.cells[((i+1) % 3)*3+2][c_no]:
                                self.cells[((i+1) % 3)*3+2][c_no].remove(n)

                        if n in c_q[(i+2) % 3]:
                            if n in self.cells[((i+2) % 3)*3][c_no]:
                                self.cells[((i+2) % 3)*3][c_no].remove(n)
                            if n in self.cells[((i+2) % 3)*3+1][c_no]:
                                self.cells[((i+2) % 3)*3+1][c_no].remove(n)
                            if n in self.cells[((i+2) % 3)*3+2][c_no]:
                                self.cells[((i+2) % 3)*3+2][c_no].remove(n)

    def guess_was_wrong(self):
        if len(self.guessed) == 0:
            self.close()
            return

        print("guess_was_wrong!!!", self.guessed[0])
        self.guessed[0]['already_guessed'].append(
            self.guessed[0]['cur_guess'])
        self.grid[self.guessed[0]['row']][self.guessed[0]['column']] = 0
        if len(self.guessed[0]['set_of_options']) == len(self.guessed[0]['already_guessed']):
            self.guessed.pop(0)
            if len(self.guessed) == 0:
                print(
                    "Error unable to go back further-> there is mistake somewhere before the guess")
                self.close()
            else:
                self.guess_was_wrong()
        else:
            for opt in self.guessed[0]['set_of_options']:
                if opt in self.guessed[0]['already_guessed']:
                    continue
                self.guessed[0]['cur_guess'] = opt
                self.grid[self.guessed[0]['row']
                          ][self.guessed[0]['column']] = opt
        self.update_stack()

    def check_if_impossible(self):
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    if len(self.cells[r][c]) == 0:
                        print("impossible: (r,c)", (r, c))
                        return True
        return False

    def make_a_new_guess(self):
        smallest_set_len = 2
        for r in range(9):
            for c in range(9):
                next = False
                if 0 < len(self.cells[r][c]) <= smallest_set_len and self.grid[r][c] == 0:
                    for x in self.guessed:
                        if x['row'] == r and x['column'] == c:
                            next = True
                    if next:
                        continue
                    the_guess = self.cells[r][c][0]
                    self.grid[r][c] = the_guess
                    self.guessed.append(
                        {"row": r, "column": c, "set_of_options": self.cells[r][c], "cur_guess": the_guess, "already_guessed": []})
                    print("new guess {} at {}".format(the_guess, (r, c)))
        self.update_stack()

    def solve_loop(self):
        self.reset_stack()
        # input("ready:")
        for i in range(60):
            self.update_stack()
            # self.print_stack()
            if self.stop :
                break
            if self.check_if_impossible():  # this has to be after every cell has been evaluated
                self.guess_was_wrong()
            self.check_if_finished()
            if self.finished:
                print("solved in iteration {}".format(i))
                break
            if not self.solve_for_one_solution():
                print("no progress")
                print("making a guess")
                self.make_a_new_guess()
                # input()
                # Game_loop(self)
        if not self.finished:
            print("not solved :(")
            


def main():
    s_id = database.login_user("solution", "cillitbang")
    lot = database.get_codenames_and_hashes_and_userdata(s_id)
    loh = [x[1] for x in lot]  # list of hash
    loh.sort()   #[6, 11, 13, 30, 31, 40, 42, 43, 47, 50, 59, 65, 70, 71, 99]
    # loh = [loh[6],loh[ 11],loh[ 13],loh[ 30],loh[ 31],loh[ 40],loh[ 42],loh[ 43],loh[ 47],loh[ 50],loh[ 59],loh[ 65],loh[ 70],loh[ 71],loh[ 99]]
    loh = [loh[0]]
    s_old = time.time()
    global current_hash
    current_hash = loh[0]
    not_working_sud = [i for i in range(len(loh))]
    for index,h in enumerate(loh):
        g, raw, s, seconds ,completed,best_time = database.get_edited_raw_solved_Sudoku_and_seconds_and_completed(s_id, h)
        json_grid = json.loads(raw)
        board = json_grid['board']
        pprint(board)
        # board = [[8, 0, 0, 0, 0, 7, 0, 0, 2],
        #          [0, 0, 4, 0, 0, 6, 7, 0, 9],
        #          [0, 0, 0, 0, 0, 8, 0, 0, 6],
        #          [1, 0, 0, 0, 6, 5, 0, 9, 7],
        #          [0, 0, 0, 0, 0, 0, 0, 1, 0],
        #          [0, 9, 8, 0, 1, 0, 0, 0, 0],
        #          [0, 1, 0, 5, 0, 0, 0, 7, 8],
        #          [0, 0, 5, 8, 7, 3, 0, 0, 0],
        #          [9, 8, 7, 6, 2, 1, 5, 3, 4]]

        solved = Solve(board)
        if solved.finished:
            not_working_sud.remove(index)
            the_taken_time = int(seconds + time.time() - s_old)
            # the_taken_time = 9999999
            database.update_edited_Sudoku(s_id,{'board':solved.grid},the_taken_time,0)
            print("solved :)")
    print("Not solvable:")
    print(not_working_sud)

def Game_loop(inst_of_solve):
    s_id = "e21cf13722224387af2d80b97714d5d6"
    print(current_hash)
    input()
    wind = window.window(s_id,current_hash)
    wind.Sudoku_cur.grid = inst_of_solve.grid
    while wind.running:
        wind.event_loop()
    quit()
# update_quadrants()
# print_quads()
# update_rows()
# print_rows()
# update_columns()
# print_columns()
# update_cells()
# print_cells()
main()
