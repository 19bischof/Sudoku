import numpy
import pygame
import random

from settings import settings as st
import json
from Sudoku import Sudoku
class window:

    colors = [(255,255,255),(244, 40, 40),(145, 42, 42),(145, 156, 154),(233,239,59)]

    def __init__(self):
        self.running = True
        self.Sudoku_cur = Sudoku()
        self.x_calibration = 14
        self.y_calibration = -3
        self.font_height = 45
        self.pressed = False
        self.rects = []
        self.highlighted = [[0 for x in range(9)] for x in range(9)]
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sudoku')
        
        self.myfont = pygame.font.SysFont('Arial',self.font_height)
        self.window = pygame.display.set_mode((st.width,st.height))
        self.show_background()
        self.show_grid()

    

    def event_loop(self):

        while self.running:
            pygame.time.Clock().tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.KEYDOWN:
                    if hasattr(self,'in_focus'):
                        if self.Sudoku_cur.grid[self.in_focus[0]][self.in_focus[1]] == 0 or self.highlighted[self.in_focus[0]][self.in_focus[1]] != 0:
                            event.key = self.filter_numpad(event.key)
                            if 47 < event.key < 58:
                                self.highlighted[self.in_focus[0]][self.in_focus[1]] = 3
                                res = self.Sudoku_cur.set_value(self.in_focus[0],self.in_focus[1],int(chr(event.key)))
                                if res  == "bad":
                                    self.highlighted[self.in_focus[0]][self.in_focus[1]] = 4
                                if res == "reset":
                                    self.highlighted[self.in_focus[0]][self.in_focus[1]] = 0
                                self.render_again()

                if event.type == pygame.MOUSEMOTION:
                    if self.pressed:
                        pos = pygame.mouse.get_pos()
                        if pos != None:
                            index,iindex = self.get_index_from_rect_or_pos(pos)
                            self.in_focus = (index,iindex)
                            self.render_again()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos != None:
                        index,iindex = self.get_index_from_rect_or_pos(pos)
                        self.in_focus = (index,iindex)
                        self.pressed = True
                        self.render_again()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.pressed = False
                    pos = pygame.mouse.get_pos()
                    if pos != None:
                        index,iindex = self.get_index_from_rect_or_pos(pos)
                        self.in_focus = (index,iindex)
                        self.render_again() 

    def filter_numpad(self,key):#filter and return ascii value of 0-9 if numpad was used
        if 1073741912 < key < 1073741922:
            key -= 1073741912
            key += 48
        return key
    def render_again(self):
        self.show_background()
        self.show_grid()

    def get_index_from_rect_or_pos(self,pos):
        for index,row in enumerate(self.rects):
            for iindex,rect in enumerate(row):
                if rect.collidepoint(pos):
                    return index,iindex
        return -1,-1

    def render_number(self,cur_rect,row,column):
        # new_rect = cur_rect.move((rect_size),(rect_size))
        new_rect = cur_rect.copy()              #dangerous with just an assignment because 
        new_rect.left += self.x_calibration     # in python assignments  just gives the reference
        new_rect.top += self.y_calibration
        # sud_value = self.myfont.render(str(random.randint(1,9)),True,(0,0,0))         #random number each rendering
        number = self.Sudoku_cur.grid[row][column]
        if number == 0 : number = ""
        sud_value = self.myfont.render(str(number),True,(0,0,0))
        
        self.window.blit(sud_value,new_rect)
        # pygame.display.flip()


    def get_color(self,row,column):
        if hasattr(self,'in_focus'):
            if self.pressed:
                pass
            if (row,column) == self.in_focus:
                if self.pressed:
                    return window.colors[2]
                return window.colors[1]
        return window.colors[self.highlighted[row][column]]

    def show_background(self):
        self.window.fill((79, 179, 105))
        
    def show_grid(self):
        #this method renders in columns so its slightly disharminous because all 2dim list are rows first
        
        rect_size = 50
        x_offset = int(0.5*(st.width - 9*rect_size))
        y_offset = int(0.5*(st.height - 9*rect_size))
        winx = self.window
        parse_rects = []
        for index,x in enumerate((range (0,9*rect_size,rect_size))):        #index is the column; iindex is the row
            parse_column = []
            for iindex,y in enumerate(range (0,9*rect_size,rect_size)):
                cur_rect = pygame.Rect(x+x_offset,y+y_offset,rect_size,rect_size)
                pygame.draw.rect(winx,(0,0,0),cur_rect,1)
                inflated_rect = cur_rect.inflate(-2,-2)
                color = self.get_color(iindex,index)
                pygame.draw.rect(winx,color,inflated_rect)
                parse_column.append(cur_rect)
                self.render_number(cur_rect,iindex,index)
            parse_rects.append(parse_column)
        self.rects = list(map(list,zip(*parse_rects)))      #this transpose the array so first dimension are now rows

        for x in range(2):
            pygame.draw.line(winx,(0,0,0),(x_offset+3*rect_size*(x+1),y_offset),(x_offset+3*rect_size*(x+1),y_offset+9*rect_size),4)
        for y in range(2):
            pygame.draw.line(winx,(0,0,0),(x_offset,y_offset+3*rect_size*(y+1)),(x_offset+9*rect_size,y_offset+3*rect_size*(y+1)),4)
        pygame.display.flip()
    
 