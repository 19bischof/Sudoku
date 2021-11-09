import json
from settings import settings as st
import database
import msvcrt
class Sudoku:
    
    def __init__(self,s_id,hash = None):
        self.error = ""
        self.seconds = ""
        if s_id == "":
            if input("Login?").lower().strip() in ("y","yes"):
                self.login()
            else:
                print("Logging in as Guest")
                self.session_id = "5033c8b3f8372ddd0937fea202d1be28"
        else:
            self.session_id = s_id
        self.load_grid_from_db()        #switch these for db or json
        self.hash = hash

    
    def load_grid_from_db(self,hash = None):
        res,seconds = database.get_edited_Sudoku(self.session_id,hash)
        self.seconds = seconds
        if res == "not valid session_id":
            self.error += res
            return
        str_grid = res
        raw_grid = json.loads(str_grid)
        self.grid = raw_grid['board']

    def update_db_with_data(self):

    def set_value(self,i,ii,value):
        if value == 0:
            self.grid[i][ii]= 0
            return "reset"
        self.grid[i][ii] = value
        if st.crude_checking:
            resp = self.check_if_obviously_wrong((i,ii))
            if resp:
                print("Help: This number already exists in its",resp)
                return "bad"
        return None

    def login(self):
        print("----Login----")
        user = input("Username: ")
        print("Password: ",end="",flush=True)
        passw = ""
        while 1:
            char = msvcrt.getch()
            if char == b'\r':
                break
            if char == b'\x03':
                print("Logging in as Guest")
                self.session_id = "5033c8b3f8372ddd0937fea202d1be28"
            if char == b'\x08':
                print("\rPassword: ",end="",flush=True)
                for l in range(len(passw)):
                    print(" ",end="",flush="True")
                print("\rPassword: ",end="",flush=True)
                for l in range(len(passw)-1):
                    print("*",end="",flush="True")
                passw = passw[0:len(passw)-1]
            else:
                passw += char.decode('utf-8')
                print('*',end="",flush=True)
        print()
        user = user.strip()
        passw = passw.strip()
        self.session_id = database.login_user(user,passw)
        if self.session_id == "Username doesn't exist":
            print(self.session_id)
            self.session_id = None
            if input("Do you want to register this User?").lower().strip() in ("yes","y"):
                database.register_new_user(user,passw)
                self.session_id = database.login_user(user,passw)
            else:
                self.login()


    def check_if_obviously_wrong(self,pos):
        the_value = self.grid[pos[0]][pos[1]]
        for i in range(9):  #check row
            if i != pos[1]:
                if self.grid[pos[0]][i] == the_value:
                    return "row"

        for i in range(9):  #check column
            if i != pos[0]:
                if self.grid[i][pos[1]] == the_value:
                    return "column"
        #get quadrant
        x = int(pos[1]/3)
        y = int(pos[0]/3)
        for c in range(x*3,3+x*3):
            for r in range(y*3,3+y*3):
                if (r,c) != pos:
                    if self.grid[r][c] == the_value:
                        return "area"
        return False