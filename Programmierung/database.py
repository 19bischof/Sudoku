import sqlite3
import prettytable
import json
import random

def open_con():
    try:
        con = sqlite3.connect('welcomeUser.db')
        return con
    except :
        print("Can't connect to welcomeUser.db !")
        quit()
def alter_table(con):
    con = open_con()
    cur = con.cursor() 
    query = '''
    CREATE TABLE IF NOT EXISTS Sud1 (hash text,
    Sudoku_raw json, Sudoku_solved json, difficulty text);
    '''
    cur.execute(query)
    res = cur.fetchone()
    print("Create new table: ",res)
    #now select all the rows from the old table and copy them to the new table and then delete old
    #and rename new to old

    if Sudoku_table_exists(con):
        query = '''
        DROP TABLE Sudokus;
        '''
        cur.execute(query)
        res = cur.fetchone()
        print("Drop old table: ",res)
    
    query = '''
    ALTER Table Sud1 RENAME TO Sudokus;
    '''
    cur.execute(query)
    res = cur.fetchone()
    print("Rename new table: ",res)
    
    con.commit()
    con.close()

def create_table(con):
    con = open_con()
    cur = con.cursor() 
    query = '''
    CREATE TABLE IF NOT EXISTS Sudokus (hash text,
    Sudoku_raw blob, Sudoku_solved blob, difficulty text);
    '''
    cur.execute(query)
    res = cur.fetchone()
    print("Database-Response: ",res)

    con.commit()
    con.close()

def load_json_Sudoku_to_db(the_hash,_dict,difficulty,con = None):
    if con == None:
        con = open_con()
    if Sudoku_table_exists(con):
        cur = con.cursor()
        query = '''
        INSERT INTO Sudokus (hash,Sudoku_raw,difficulty) values (?,?,?);
        '''
        cur.execute(query,(the_hash,_dict,difficulty))
        res = cur.fetchone()
        print("Database-Response: ",res)

        con.commit()
    con.close()

def show_tables(con = None):
    if con == None:
        con = open_con()
    cur = con.cursor()
    query = '''
    SELECT * FROM sqlite_master
    WHERE NAME NOT LIKE 'sqlite_%';
    '''    
    cur.execute(query)
    print(prettytable.from_db_cursor(cur))
    if Sudoku_table_exists(con):
        query = '''
        SELECT hash,difficulty FROM Sudokus;
        '''
        cur.execute(query)
        print(prettytable.from_db_cursor(cur))
    con.close()

def template_json_file(con):
    with open('editable_Sudokus.json','r') as the_json:
        raw_grid = json.load(the_json)
        the_hash = list(raw_grid.keys())[0]    # 0 because only one Sudoku in file
        print(the_hash,type(the_hash))
        print("check: ",type(raw_grid[the_hash]),raw_grid[the_hash])
        load_json_Sudoku_to_db(con,the_hash,json.dumps(raw_grid[the_hash]),"easy")    #easy because uneditable json is pulled solely from easy category


def Sudoku_table_exists(con):
    cur = con.cursor()
    query = '''
    Select * FROM Sudokus;
    '''
    try:
        cur.execute(query)
        return True
    except:
        print("Table \"Sudokus\" doesn't exist!")
        return False

def get_hashes(con):
    cur = con.cursor()
    query = '''
    SELECT hash FROM Sudokus;
    '''
    cur.execute(query)
    res = cur.fetchall()    #res is of type list
    index = random.randint(0,len(res)-1)
    return res[index]


def get_raw_Sudoku(con = None,hash = None):
    if con == None:
        con = open_con()
    if not Sudoku_table_exists(con):
        return None
    if not hash:
        hash = get_hashes(con)
    cur = con.cursor()
    query = '''
    SELECT Sudoku_raw FROM Sudokus WHERE hash = ?;
    '''
    cur.execute(query,hash)
    res = cur.fetchone()    #res is tuple of one dictionary where the key is 'board' => we just need the dict
    # print("type is: ",type(res),res)
    con.close()
    return res[0],hash


# create_table(con)
# alter_table(con)
# show_tables(con)
# template_json_file(con)
# test_if_table_has_data(con)

# get_raw_Sudoku(con)
# show_tables(con)












