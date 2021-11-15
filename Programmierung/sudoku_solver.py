from pprint import pprint
import window

grid = [[8, 0, 0, 0, 0, 7, 0, 0, 2],
        [0, 0, 4, 0, 0, 6, 7, 0, 9],
        [0, 0, 0, 0, 0, 8, 0, 0, 6],
        [1, 0, 0, 0, 6, 5, 0, 9, 7],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 9, 8, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 5, 0, 0, 0, 7, 8],
        [0, 0, 5, 8, 7, 3, 0, 0, 0],
        [9, 8, 7, 6, 2, 1, 5, 3, 4]]

nos = (1, 2, 3, 4, 5, 6, 7, 8, 9)

def close():
    print("Error: Stopping execution\ngrid:")
    pprint(grid)
    quit()
def update_stack():
    update_rows()
    update_columns()
    update_quadrants()
    update_cells()  #important that cells is last
def valid_stack():
    check_if_rows_valid()
    check_if_columns_valid()
    check_if_quadrants_valid()
    check_if_cells_valid()
def reset_stack():
    reset_rows()
    reset_columns()
    reset_quads()
    reset_cells()
def print_stack():
    print_rows()
    print_columns()
    print_quads()
    print_cells()
def reset_quads():
    global quadrants
    quadrants = [[] for x in range(9)]

def print_quads():
    print("quadrants:")
    for q_no in range(9):
        print("[{}]:".format(q_no),end="")
        for n in nos:
            if n in quadrants[q_no]:
                print(n,end=",",flush=True)
        print()

def check_if_quadrants_valid():
    for q_no, q in enumerate(quadrants):
        have = []
        for e in q:
            if e in have:
                print("duplicate number in quadrant:", q_no)
                print_quads()
                close()
            have.append(e)

def get_quadrant(r,c):
    quadrant = int(r/3)*3 + int(c/3)

    return quadrant

def update_quadrants():         #quadrant 0-8: top left to top right and then one row down
    global quadrants
    reset_quads()
    for q_no in range(9):
        for r in range(3*int(q_no/3), 3*(int(q_no/3)+1)):
            for c in range(3*(q_no % 3), (3*(q_no % 3+1))):
                if grid[r][c] != 0:
                    quadrants[q_no].append(grid[r][c])
    check_if_quadrants_valid()

def reset_rows():
    global rows
    rows = [[] for x in range(9)]

def print_rows():
    print("rows:")
    global rows
    for r_no in range(9):
        print("[{}]:".format(r_no),end="")
        for n in nos:
            if n in rows[r_no]:
                print(n,end=",",flush=True)
        print()

def check_if_rows_valid():
    for r_no, r in enumerate(rows):
        have = []
        for e in r:
            if e in have:
                print("duplicate number in row:", r_no)
                print_rows()
                close()
            have.append(e)

def update_rows():
    global rows
    reset_rows()
    for r_no in range(9):
        for c in range(9):
            if grid[r_no][c] != 0:
                rows[r_no].append(grid[r_no][c])
    check_if_rows_valid()

def reset_columns():
    global columns
    columns = [[] for x in range(9)]

def print_columns():
    print("columns:")
    global columns
    for c_no in range(9):
        print("[{}]:".format(c_no),end="")
        for n in nos:   
            if n in columns[c_no]:
                print(n,end=",",flush=True)
        print()
def check_if_columns_valid():
    for c_no, c in enumerate(columns):
        have = []
        for e in c:
            if e in have:
                print("duplicate number in column:", c_no)
                print_columns()
                close()
            have.append(e)

def update_columns():
    global columns
    reset_columns()
    for c in range(9):
        for r in range(9):
            if grid[r][c] != 0:
                columns[c].append(grid[r][c])
    check_if_columns_valid()

def reset_cells():
    global cells
    cells = [[[]for y in range(9)] for x in range(9)]

def print_cells():
    global cells
    print("cells:")
    pprint(cells)

def check_if_cells_valid():
    for r in range(9):
        for c in range(9):
            have = []
            for e in cells[r][c]:
                if e in have:
                    print("duplicate number in cells(r,c):", (r,c))
                    print_cells()
                    close()
                have.append(e)
def update_cells(): #3 dim array of possible numbers per cell
    global cells
    reset_cells()
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                for n in nos:
                    if n not in rows[r]:
                        if n not in columns[c]:
                            if n not in quadrants[get_quadrant(r,c)]:
                                cells[r][c].append(n)
    check_if_cells_valid()

def solve_for_one_solution():
    print("new attempt")
    progress = None
    global grid
    for r in range(9):
        for c in range(9):
            if len(cells[r][c]) == 1:
                grid[r][c] = cells[r][c][0]
                print("solved: row={} column={} number={}".format(r,c,grid[r][c]))
                # input()
                progress = True
                update_stack()
    
    return progress

def check_if_finished():
    nozero = True
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                nozero = False
    valid_stack()
    return nozero
    
def loop():
    reset_stack()
    input("ready:")
    for i in range(100):
        pprint(grid)
        update_stack()
        print_stack()
        check_if_finished()
        if not solve_for_one_solution():
            pprint(grid)
            break
    Game_loop()
#TODO: each row and each column has 3 guarantees (interaction with the quadruples)
#meaning that even if you don't know to which cell you can know this row has those two
#numbers in this quad and therefor this row cant have the two numbers as an option
#anywhere else!
s_id = "5033c8b3f8372ddd0937fea202d1be28"
def Game_loop():
    winx = window.window(s_id,"c850c5be22fa6169")
    winx.Sudoku_cur.grid = grid
    winx.show_background()
    while winx.running:
        winx.event_loop()
# update_quadrants()
# print_quads()
# update_rows()
# print_rows()
# update_columns()
# print_columns()
# update_cells()
# print_cells()
loop()