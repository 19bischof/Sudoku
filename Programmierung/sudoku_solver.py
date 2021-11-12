from pprint import pprint


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


def reset_quads():
    global quadrants
    quadrants = [[] for x in range(9)]


def print_quads():
    for q in quadrants:
        pprint(q)


def check_if_quadrants_valid():
    for q_no, q in enumerate(quadrants):
        have = []
        for e in q:
            if e in have:
                print("double number in quadrant:", q_no)
                print_quads()
                quit()
            have.append(e)


def reset_rows():
    global rows
    rows = [[] for x in range(9)]


def print_rows():
    global rows
    for r in rows:
        # left off here in implementing what i did for quadrants for rows and columns as well
        pprint(r)


check_if_rows_valid():
    for q_no, q in enumerate(rows):
        have = []
        for e in q:
            if e in have:
                print("double number in quadrant:", q_no)
                print_quads()
                quit()
            have.append(e)


def update_quadrants():
    global quadrants
    reset_quads()
    for q_no in range(9):
        for r in range(3*int(q_no/3), 3*(int(q_no/3)+1)):
            for c in range(3*(q_no % 3), (3*(q_no % 3+1))):
                # print("row:",r,"\tcolumn:",c)
                if grid[r][c] != 0:
                    quadrants[q_no].append(grid[r][c])


update_quadrants()
print_quads()
check_if_quadrants_valid()
