import sqlite3
import prettytable
import json

try:
    con = sqlite3.connect('welcomeUser.db')
except :
    print("Can't connect !")
    quit()

def create_table(con):
    cur = con.cursor() 
    query = '''
    CREATE TABLE IF NOT EXISTS Sudokus (id INTEGER primary key autoincrement,
    Sudoku_raw blob, Sudoku_solved blob, difficulty text);
    '''
    cur.execute(query)
    res = cur.fetchone()
    print("Database-Response: ",res)
    con.commit()
    con.close()

def load_json_Sudoku_to_db(con,dicky,diffy):
    cur = con.cursor()
    query = '''
    INSERT INTO Sudokus (Sudoku_raw,difficulty) values (?,?);
    '''
    print("what is the type: ",type(dicky))
    cur.execute(query,(sqlite3.Binary(dicky),diffy))
    res = cur.fetchone()
    print("Database-Response: ",res)
    cur.commit()
    show_tables(con)

def show_tables(con):
    cur = con.cursor()
    query = '''
    SELECT * FROM Sudokus
    '''
    cur.execute(query)
    print(prettytable.from_db_cursor(cur))




# create_table(con)
with open('editable_Sudokus.json','r') as the_json:
    raw_grid = json.load(the_json)
    load_json_Sudoku_to_db(con,raw_grid['board'],"easy")    #easy because uneditable json is pulled solely from easy category






# show_tables(con)








con.close()
