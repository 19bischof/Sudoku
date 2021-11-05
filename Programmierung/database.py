import sqlite3
import prettytable
import json
import random
import pbkdf2_impl
import os
import names
from pprint import pprint

def open_con():
    try:
        con = sqlite3.connect('welcomeUser.db')
        return con
    except :
        print("Can't connect to welcomeUser.db !")
        quit()



def random_queries():
    con = open_con()
    cur = con.cursor()
    query = '''
    ALTER TABLE Sudokus ADD COLUMN IF NOT EXISTS codename text;'''
    cur.execute(query)
    # print(prettytable.from_db_cursor(cur))
    print(cur.fetchone())
    con.commit()
    con.close()

def _username_exists(username,con):
    cur = con.cursor()
    query = '''Select username from users where username = ?'''
    cur.execute(query,(username,))
    res = cur.fetchone()
    if res != None:
        return True
    return False

def _Cross_table_exists(con):
    cur = con.cursor()
    query = '''
    Select * FROM Cross_Sudokus_Users;
    '''
    try:
        cur.execute(query)
        return True
    except:
        print("Table \"Cross\" doesn't exist!")
        return False

def _Users_table_exists(con):
    cur = con.cursor()
    query = '''
    Select * FROM Users;
    '''
    try:
        cur.execute(query)
        return True
    except:
        print("Table \"Users\" doesn't exist!")
        return False

def _Sudoku_table_exists(con):
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


def drop_users():
    con = open_con()
    cur = con.cursor()
    if _Users_table_exists(con):
        query ='''Drop Table Users;'''
        cur.execute(query)
        res = cur.fetchone()
        print("Database-Response: ",res)
        con.commit()
    con.close()

def drop_cross():
    con = open_con()
    cur = con.cursor()
    if _Cross_table_exists(con):
        query ='''Drop Table Cross_Sudokus_Users;'''
        cur.execute(query)
        res = cur.fetchone()
        print("Database-Response: ",res)
        con.commit()
    con.close()


def create_table_Sudokus():
    con = open_con()
    cur = con.cursor() 
    query = '''
    CREATE TABLE IF NOT EXISTS Sudokus (hash text,
    Sudoku_raw json, Sudoku_solved json, difficulty text);
    '''
    cur.execute(query)
    res = cur.fetchone()
    print("Database-Response: ",res)

    con.commit()
    con.close()

def create_table_cross():
    con = open_con()
    cur = con.cursor() 
    query = '''
    CREATE TABLE IF NOT EXISTS Cross_Sudokus_Users(
    u_rowid int,s_rowid int,Sudoku_edited json);
    '''
    cur.execute(query)
    res = cur.fetchone()
    print("Database-Response: ",res)

    con.commit()
    con.close()

def create_table_user():
    con = open_con()
    cur = con.cursor()
    query = '''
    CREATE TABLE IF NOT EXISTS Users (username text, password text,salt text,cur_s_rowid int,session text);
    '''
    cur.execute(query)
    res = cur.fetchone()
    print("Database-Response: ",res)
    con.commit()
    con.close()

def register_new_user(username,password):
    con = open_con()
    if _username_exists(username,con):
        con.close()
        print("username exists already")
        return "exists already"
    cur = con.cursor()
    query = '''
    INSERT INTO Users (username,password,salt)
    VALUES (?,?,?);'''
    result = pbkdf2_impl.hash_of_passw(password)
    cur.execute(query,(username,result['hash'],result['salt']))
    res = cur.fetchone()
    print("Database-Response: ",res)
    con.commit()
    con.close()

def login_user(username,password):
    con = open_con()
    if _username_exists(username,con):
        cur = con.cursor()
        query = '''Select password,salt from Users where username = ?'''
        cur.execute(query,(username,))
        response = cur.fetchone()
        if response != None:
            db_hash,the_salt = response
            result = pbkdf2_impl.hash_of_passw(password,bytes.fromhex(the_salt))
            gen_hash = result['hash']
            if gen_hash == db_hash:
                session_id = os.urandom(16).hex()
                if _set_session_id(session_id,username,con):
                    con.close()
                    return session_id
            else:
                print("Wrong Password!")
                con.close()
                return None    
    else:
        print("Username doesn't exist")
        con.close()
        return "Username doesn't exist"
    print("Couldn't login")
    con.close()

def _set_session_id(session_id,username,con):
    cur = con.cursor()
    query = '''UPDATE Users Set session = ? where username = ?'''
    cur.execute(query,(session_id,username))
    res = cur.fetchone()
    print("Database-Response: ",res)
    con.commit()
    return True

def _valid_session_id(session_id,con):
    cur = con.cursor()
    query = '''Select username from Users WHERE session = ? '''
    cur.execute(query,(session_id,))
    res = cur.fetchone()
    if res == None:
        return False
    return True
    
def _get_rowids_from_session_id(session_id,con):
    cur = con.cursor()
    query = '''SELECT rowid,cur_s_rowid from Users WHERE session = ?;'''
    cur.execute(query,(session_id,))
    res = cur.fetchone()
    return res

def load_json_Sudoku_to_db(the_hash,_dict,difficulty):
    con = open_con()
    if _Sudoku_table_exists(con):
        cur = con.cursor()
        query = '''Select hash from Sudokus where hash = ?'''
        cur.execute(query,(the_hash,))
        res = cur.fetchone()
        if res == None:
            query = '''
            INSERT INTO Sudokus (hash,Sudoku_raw,difficulty) values (?,?,?);
            '''
            cur.execute(query,(the_hash,_dict,difficulty))
            res = cur.fetchone()
            print("Database-Response: ",res)
            con.commit()
    con.close()


def template_json_file():
    with open('editable_Sudokus.json','r') as the_json:
        raw_grid = json.load(the_json)
        keys = list(raw_grid.keys())  
        for index,the_hash in enumerate(keys):
            print("Loading",str(index)+".")
            load_json_Sudoku_to_db(the_hash,json.dumps(raw_grid[the_hash]),"easy")    #easy because uneditable json is pulled solely from easy category

def load_codenames_to_Sudokus():
    con = open_con()
    cur = con.cursor()
    lot = []            #generate list of tuples with each tuple: (name,rowid)
    for index,n in enumerate(names.j_names):
        lot.append((n,index+1))
    # pprint(lot)
    query = '''UPDATE Sudokus SET codename = ? WHERE rowid = ?;'''
    cur.executemany(query,lot)
    print(cur.fetchone())

    con.commit()
    con.close()
    
def show_tables():
    con = open_con()
    cur = con.cursor()
    query = '''
    SELECT * FROM sqlite_master WHERE NAME NOT LIKE 'sqlite_%';
    '''    
    cur.execute(query)
    print(prettytable.from_db_cursor(cur))
    if _Sudoku_table_exists(con):
        query = '''
        SELECT rowid,hash,difficulty,codename FROM Sudokus;
        '''
        cur.execute(query)
        print("Table Sudokus:")
        print(prettytable.from_db_cursor(cur))

    if _Users_table_exists(con):
        query = '''
        SELECT rowid,username,password,salt,cur_s_rowid,session FROM Users;
        '''
        cur.execute(query)
        print("Table Users:")
        print(prettytable.from_db_cursor(cur))
    if _Cross_table_exists(con):
        query = '''
        SELECT rowid,u_rowid,s_rowid FROM Cross_Sudokus_Users;
        '''
        cur.execute(query)
        print("Table Cross:")
        print(prettytable.from_db_cursor(cur))
    
    con.close()


def _get_hashes(con):
    cur = con.cursor()
    query = '''
    SELECT hash FROM Sudokus;
    '''
    cur.execute(query)
    res = cur.fetchall()            #fetchall fetches the rows as tuples in an array of rows
    index = random.randint(0,len(res)-1)
    return res[index][0]            #only the string not the tuple (res[index] is of type tuple!)
    



def _set_cur_s_rowid_with_hash(hash,session_id,con):
    cur = con.cursor()
    query = '''Select rowid from Sudokus where hash = ?'''
    cur.execute(query,(hash,))
    res = cur.fetchone()
    the_rowid = res[0]
    query = '''UPDATE Users SET cur_s_rowid = ? WHERE session = ?;'''
    cur.execute(query,(the_rowid,session_id))
    res = cur.fetchone()
    print("Database-Response:",res)
    con.commit()

def _cur_s_rowid_in_cross(session_id,con):
    cur = con.cursor()
    query = '''Select rowid,cur_s_rowid from Users WHERE session = ?'''
    cur.execute(query,(session_id,))
    u_rowid,s_rowid = cur.fetchone()
    query = '''SELECT rowid from Cross_Sudokus_Users where u_rowid = ? and s_rowid = ?'''
    cur.execute(query,(u_rowid,s_rowid))
    res = cur.fetchone()
    if res == None:
        return False
    return True

def get_edited_Sudoku(session_id,hash = None):          #the method which is called to get a Sudoku from a User (new or already edited)
    con = open_con()    
    if not _valid_session_id(session_id,con):
        return "not valid session_id"
    cur = con.cursor()
    if hash == None:
        hash = _get_hashes(con)
    _set_cur_s_rowid_with_hash(hash,session_id,con)
    if not _cur_s_rowid_in_cross(session_id,con):
        _update_edited_Sudoku_with_raw(session_id,con)
    query = '''
    SELECT Sudoku_edited FROM Cross_Sudokus_Users,Users WHERE 
    Users.cur_s_rowid = Cross_Sudokus_Users.s_rowid
    and Users.rowid = Cross_Sudokus_Users.u_rowid
    and Users.session = ?;
    '''    
    cur.execute(query,(session_id,))
    
    res = cur.fetchone()
    new_s = res[0]
    con.close()
    return new_s

def _update_edited_Sudoku_with_raw(session_id,con):
    cur = con.cursor()
    u_rowid,s_rowid = _get_rowids_from_session_id(session_id,con)
    query = '''Select Sudoku_raw from Sudokus,Users where Users.cur_s_rowid = Sudokus.rowid and Users.session = ?'''
    cur.execute(query,(session_id,))
    res = cur.fetchone()
    grid = res[0]

    query = '''Insert into Cross_Sudokus_Users (u_rowid,s_rowid,Sudoku_edited)
    VALUES (?,?,?);'''
    cur.execute(query,(u_rowid,s_rowid,grid))
    res = cur.fetchone()
    print("Database-Response:",res)
    con.commit()

def update_edited_Sudoku(session_id,grid):
    con = open_con()
    cur = con.cursor()
    u_rowid,s_rowid = _get_rowids_from_session_id(session_id,con)
    if not _cur_s_rowid_in_cross(session_id,con):
        _update_edited_Sudoku_with_raw(session_id,con)
    
    query = '''Update Cross_Sudokus_Users set Sudoku_edited = ? where u_rowid = ? and s_rowid = ?;'''
    cur.execute(query,(json.dumps(grid),u_rowid,s_rowid))
    res = cur.fetchone()
    print("Database-Response:",res)
    con.commit()
    con.close()

# create_table(con)
# alter_table(con)
# show_tables(con)
# template_json_file(con)
# test_if_table_has_data(con)

# get_raw_Sudoku(con)
# show_tables(con)

# create_table_user()
# create_table_cross()
# test_rowid()
# register_new_user("gerald","welcome to hogwarts")
# drop_users()
# drop_cross()

# s_id = login_user("gerald","welcome to hogwarts")
# con = open_con()
# hash = _get_hashes(con)
# con.close()
# the_grid = json.loads(get_edited_Sudoku(s_id,hash))
# update_edited_Sudoku(s_id,the_grid)

show_tables()


# load_codenames_to_Sudokus()
# template_json_file()


# random_queries()