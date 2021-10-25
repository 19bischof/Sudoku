import pygame
from settings import settings as st
import json
import Sudoku
class window:
    
    def __init__(self):
        self.running = True
        self.Sudoku_cur = Sudoku()
        pygame.init()
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Georgia',16)
        self.window = pygame.display.set_mode((st.width,st.height))
        pygame.display.set_caption('Sudoku')
        self.show_grid()
    def event_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def render_number(self,posit):
        self.myfont.render(0)
        self.window.blit(sud_value,posit)

    def show_grid(self):
        rect_size = 50
        x_offset = int(0.5*(st.width - 9*rect_size))
        y_offset = int(0.5*(st.height - 9*rect_size))
        winx = self.window
        winx.fill((79, 179, 105))
        for x in range (0,9*rect_size,rect_size):
            for y in range (0,9*rect_size,rect_size):
                rect = pygame.Rect(x+x_offset,y+y_offset,rect_size,rect_size)
                pygame.draw.rect(winx,(0,0,0),rect,1)
                self.render_number(rect)
                

        for x in range(2):
            pygame.draw.line(winx,(0,0,0),(x_offset+3*rect_size*(x+1),y_offset),(x_offset+3*rect_size*(x+1),y_offset+9*rect_size),4)
        for y in range(2):
            pygame.draw.line(winx,(0,0,0),(x_offset,y_offset+3*rect_size*(y+1)),(x_offset+9*rect_size,y_offset+3*rect_size*(y+1)),4)
        pygame.display.flip()
    
 