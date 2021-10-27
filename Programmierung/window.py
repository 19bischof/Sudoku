import numpy
import pygame
import random
from settings import settings as st
import json
from Sudoku import Sudoku
class window:
    color_highlights = [(255,255,255),(227, 68, 68)]
    def __init__(self):
        self.running = True
        self.Sudoku_cur = Sudoku()
        self.x_calibration = 14
        self.y_calibration = -3
        self.font_height = 45
        self.rects = []
        self.highlighted = [[0 for x in range(9)] for x in range(9)]
        print(self.highlighted)
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption('Sudoku')
        
        self.myfont = pygame.font.SysFont('Arial',self.font_height)
        self.window = pygame.display.set_mode((st.width,st.height))
        self.show_background()
        self.show_grid()

    def event_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.x_calibration += 1
                        self.show_grid()
                        print(self.x_calibration)
                        self.render_number2()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.y_calibration += 1
                        self.show_grid()
                        print(self.y_calibration)
                        self.render_number2()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for index,row in enumerate(self.rects):
                        for iindex,rect in enumerate(row):
                            if rect.collidepoint(pos):
                                # rect.left += self.x_calibration
                                # rect.top += self.y_calibration
                                new_h = []
                                for h in self.highlighted:
                                    new_h.append([0 if x==1 else x for x in iter(h)])
                                new_h[index][iindex] = 1
                                self.highlighted = new_h
                                self.show_background()
                                self.show_grid()

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

    def render_number2(self):
        # new_rect = cur_rect.move((rect_size),(rect_size))     #this was only used to see the rectangle and adjust the x and y calibration with the font
        new_rect = self.cur_rect
        new_rect.left += self.x_calibration
        new_rect.top -= self.y_calibration
        sud_value = self.myfont.render("2",True,(0,0,0))
        
        self.window.blit(sud_value,new_rect)
        pygame.display.flip()

    def show_background(self):
        self.window.fill((79, 179, 105))
        
    def show_grid(self):
        #this method renders in columns so its slightly disharminous because all 2dim list are rows first
        
        rect_size = 50
        self.rect_size = rect_size # delete later
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
                pygame.draw.rect(winx,window.color_highlights[self.highlighted[iindex][index]],inflated_rect)
                parse_column.append(cur_rect)
                self.render_number(cur_rect,iindex,index)
            parse_rects.append(parse_column)
        self.rects = list(map(list,zip(*parse_rects)))      #this transpose the array so first dimension are now rows
        # print(parse_rects,'\n',self.rects,type(self.rects),type(self.rects[0][0]))
        # pygame.draw.rect(winx,(0,255,255),self.rects[0][5]) 
        self.cur_rect = cur_rect # delete later       

        for x in range(2):
            pygame.draw.line(winx,(0,0,0),(x_offset+3*rect_size*(x+1),y_offset),(x_offset+3*rect_size*(x+1),y_offset+9*rect_size),4)
        for y in range(2):
            pygame.draw.line(winx,(0,0,0),(x_offset,y_offset+3*rect_size*(y+1)),(x_offset+9*rect_size,y_offset+3*rect_size*(y+1)),4)
        pygame.display.flip()
    
 