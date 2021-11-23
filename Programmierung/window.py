import pygame

from settings import settings as st
from Sudoku import Sudoku


class window:
    colors = {"white":(255,255,255),"bright_red":(244,40,40),"dark_red":(145,42,42),"grey":(145,156,154),
    "yellow":(233,239,59),"bright_green":(79,179,105),"dark_blue":(0,0,102),"bright_blue":(0, 208, 255),"black":(0,0,0)}
    # colors = [(255, 255, 255), (244, 40, 40), (145, 42, 42), (145, 156, 154),
    #           (233, 239, 59),(79, 179, 105),(0,0,102)]  # white, bright_red, dark_red, grey, yellow,bright_green,dark_blue

    def __init__(self, s_id,hash):
        self.running = True
        self.Sudoku_cur = Sudoku(s_id,hash=hash)
        self.completed_sud = False
        if len(self.Sudoku_cur.error) != 0:
            print(self.Sudoku_cur.error)
            quit()
        self.x_calibration = 14
        self.y_calibration = -3
        self.font_height = 45
        self.pressed = False
        self.rects = []
        self.highlighted = self.Sudoku_cur.changes        #0=normal,1=selected,2=mousedown,3=changed_value,4=changed_and_bad_value
        self.number_cur = 0                             #stores the number currently highlighted so all other are as well
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sudoku - '+self.Sudoku_cur.username)
        self.myfont = pygame.font.SysFont('Arial', self.font_height)
        self.text_font = pygame.font.SysFont('Arial', 20)
        self.window = pygame.display.set_mode(
            (st.width, st.height), flags=pygame.SHOWN)
        pygame.display.flip()
        self.show_background()
        self.show_grid()

    def event_loop(self):

        while self.running:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Sudoku_cur.update_db_with_data()
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if hasattr(self, 'in_focus'):
                        if self.Sudoku_cur.grid[self.in_focus[0]][self.in_focus[1]] == 0 or self.highlighted[self.in_focus[0]][self.in_focus[1]] != 0:
                            event.key = self.filter_numpad(event.key)
                            if 47 < event.key < 58:
                                self.highlighted[self.in_focus[0]
                                                 ][self.in_focus[1]] = 3
                                res = self.Sudoku_cur.set_value(
                                    self.in_focus[0], self.in_focus[1], int(chr(event.key)))
                                if res == "bad":
                                    self.highlighted[self.in_focus[0]
                                                     ][self.in_focus[1]] = 4
                                elif res == "reset":
                                    self.highlighted[self.in_focus[0]
                                                     ][self.in_focus[1]] = 0
                                elif res == "completed":
                                    self.completed_sud = True
                                    self.running = False
                                self.number_cur = self.Sudoku_cur.grid[index][iindex]
                                self.render_again()

                if event.type == pygame.MOUSEMOTION:
                    if self.pressed:
                        pos = pygame.mouse.get_pos()
                        if pos != None:
                            index, iindex = self.get_index_from_rect_or_pos(pos)
                            self.number_cur = self.Sudoku_cur.grid[index][iindex]
                            self.in_focus = (index, iindex)
                            self.render_again()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos != None:
                        index, iindex = self.get_index_from_rect_or_pos(pos)
                        self.in_focus = (index, iindex)
                        self.number_cur = self.Sudoku_cur.grid[index][iindex]
                        self.pressed = True
                        self.render_again()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.pressed = False
                    pos = pygame.mouse.get_pos()
                    if pos != None:
                        index, iindex = self.get_index_from_rect_or_pos(pos)
                        self.in_focus = (index, iindex)
                        self.render_again()
        if self.running is False:
            pygame.quit()
    def filter_numpad(self, key):  # filter and return ascii value of 0-9 if numpad was used
        if 1073741912 < key < 1073741923:
            key -= 1073741912
            if key == 10:           #on numpad 0 is 10
                key = 0
            key += 48
        return key

    def render_again(self):
        self.show_background()
        self.show_grid()

    def get_index_from_rect_or_pos(self, pos):
        for index, row in enumerate(self.rects):
            for iindex, rect in enumerate(row):
                if rect.collidepoint(pos):
                    return index, iindex
        return -1, -1

    def render_number(self, cur_rect, row, column):
        # new_rect = cur_rect.move((rect_size),(rect_size))
        new_rect = cur_rect.copy()  # dangerous with just an assignment because
        # in python assignments  just gives the reference
        new_rect.left += self.x_calibration
        new_rect.top += self.y_calibration
        # sud_value = self.myfont.render(str(random.randint(1,9)),True,(0,0,0))         #random number each rendering
        number = self.Sudoku_cur.grid[row][column]
        if number == 0:
            number = ""
        sud_value = self.myfont.render(str(number), True, (0, 0, 0))

        self.window.blit(sud_value, new_rect)
        # pygame.display.flip()

    def get_color(self, row, column):
        c_map = ['white','bright_red','dark_red','grey','yellow']
        if hasattr(self, 'in_focus'):
            if self.pressed:
                pass
            if (row, column) == self.in_focus:
                if self.pressed:
                    return window.colors['dark_red']
                return window.colors['bright_red']
            if self.Sudoku_cur.grid[row][column] == self.number_cur and self.number_cur != 0:
                return window.colors['bright_blue']
        return window.colors[c_map[self.highlighted[row][column]]]

    def show_background(self):
        self.window.fill(window.colors['bright_green'])
        self.window.blit(self.text_font.render(self.Sudoku_cur.username+" - "+self.Sudoku_cur.codename,True,window.colors['dark_blue']),(0,0))

    def show_grid(self):
        # this method renders in columns so its slightly disharminous because all 2dim list are rows first

        rect_size = 50
        x_offset = int(0.5*(st.width - 9*rect_size))
        y_offset = int(0.5*(st.height - 9*rect_size))
        winx = self.window
        parse_rects = []
        # index is the column; iindex is the row
        for index, x in enumerate((range(0, 9*rect_size, rect_size))):
            parse_column = []
            for iindex, y in enumerate(range(0, 9*rect_size, rect_size)):
                cur_rect = pygame.Rect(
                    x+x_offset, y+y_offset, rect_size, rect_size)
                pygame.draw.rect(winx, (0, 0, 0), cur_rect, 1)
                inflated_rect = cur_rect.inflate(-2, -2)
                color = self.get_color(iindex, index)
                pygame.draw.rect(winx, color, inflated_rect)
                parse_column.append(cur_rect)
                self.render_number(cur_rect, iindex, index)
            parse_rects.append(parse_column)
        # this transpose the array so first dimension are now rows
        self.rects = list(map(list, zip(*parse_rects)))

        for x in range(2):
            pygame.draw.line(winx, (0, 0, 0), (x_offset+3*rect_size*(x+1), y_offset),
                             (x_offset+3*rect_size*(x+1), y_offset+9*rect_size), 4)
        for y in range(2):
            pygame.draw.line(winx, (0, 0, 0), (x_offset, y_offset+3*rect_size*(y+1)),
                             (x_offset+9*rect_size, y_offset+3*rect_size*(y+1)), 4)
        pygame.display.flip()