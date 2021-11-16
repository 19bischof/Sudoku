#TODO since now we got the row_quads and the column_quads correctly working we now have to use this information:
#meaning if the space in a *-quad available is the same as the number of all possible number options for this *-quad then remove this set of numbers from the rest of the 
#*-quad! Also then look at the (column if row-quad,row if column-quad) !*-quad and see if there is an easy solution to be had (with crude checking if number not duplicate in 
# !*-quad(row,column))
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
    update_row_quads()
    update_column_quads()
    update_cells()  #important that cells is last
def valid_stack():
    check_if_rows_valid()
    check_if_columns_valid()
    check_if_quadrants_valid()
    check_if_row_quads_valid()
    check_if_column_quads_valid()
    check_if_cells_valid()
def reset_stack():
    reset_rows()
    reset_columns()
    reset_quads()
    reset_row_quads()
    reset_column_quads()
    reset_cells()
def print_stack():
    print_rows()
    print_columns()
    print_quads()
    print_row_quads()
    print_column_quads()
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

def reset_cells():  #cells stores options for each cell (which number could be here)
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

def reset_row_quads():
    global row_quads
    row_quads = [[ [] for y in range(3)] for x in range(9)]

def print_row_quads():
    print("row_quads:")
    for r_no in range(9):
        print("[{}]:".format(r_no),end="")
        for i in range(3):
            for x in row_quads[r_no][i]:
                print(x,end="",flush=True)
            print(" ; ",end="",flush=True)
        print()

def check_if_row_quads_valid():
    for r_no in range(9):
        for i in range(3):
            have = []
            for e in row_quads[r_no][i]:
                if e in have:
                    print("duplicate number in row_quads(r_no,i):", (r_no,i))
                    print_cells()
                    close()
                have.append(e)

def update_row_quads(): #row quads: 2 dim array: for each row there are 3 sections in it (for each quad)
    global row_quads        #usefule if you are not certain in which cell exactly a pair of numbers go but know
    reset_row_quads()       #they have to be in a specific quad
    for r_no in range(9):
        first_quad_no = int(r_no/3)*3
        for ind,q_no in enumerate(range(first_quad_no,first_quad_no+3)):
            space_available = False
            for i in range(3):
                if grid[r_no][ind*3+i] == 0:
                    space_available = True
            if space_available is False:
                print("no space in row:{} ind:{}".format(r_no,ind))
                continue
            print("before q_no",q_no)
            for n in nos:
                if n not in rows[r_no]:
                    print("before n",n)
                    if n not in quadrants[q_no]:
                        print("q_no,n",q_no,n)
                        row_quads[r_no][ind].append(n)
                        print("here")
    check_if_row_quads_valid()
            
def reset_column_quads():
    global column_quads
    column_quads = [[ [] for y in range(3)] for x in range(9)]

def print_column_quads():
    print("column_quads:")
    for c_no in range(9):
        print("[{}]:".format(c_no),end="")
        for i in range(3):
            for x in column_quads[c_no][i]:
                print(x,end="",flush=True)
            print(" ; ",end="",flush=True)
        print()

def check_if_column_quads_valid():
    for c_no in range(9):
        for i in range(3):
            have = []
            for e in column_quads[c_no][i]:
                if e in have:
                    print("duplicate number in column_quads(r_no,i):", (c_no,i))
                    print_cells()
                    close()
                have.append(e)
                
def update_column_quads(): #column quads: 2 dim array: for each column there are 3 sections in it (for each quad)
    global column_quads        #usefule if you are not certain in which cell exactly a pair of numbers go but know
    reset_column_quads()       #they have to be in a specific quad
    for c_no in range(9):
        first_quad_no = int(c_no/3) 
        for ind,q_no in enumerate(range(first_quad_no,first_quad_no+9,3)):
            space_available = False
            for i in range(3):
                if grid[ind*3+i][c_no] == 0:
                    space_available = True
            if space_available is False:
                print("no space in column:{} ind:{}".format(c_no,ind))
                continue
            print("in update_column: q_no:",q_no)
            for n in nos:
                if n not in columns[c_no]:
                    if n not in quadrants[q_no]:
                        column_quads[c_no][ind].append(n)
    check_if_column_quads_valid()

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