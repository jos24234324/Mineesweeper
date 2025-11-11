#functioning part below
import pygame
import random
from features import *
# types
# unknown -> U
# numbered ->N
# mine -> M
class Tiles:
    def __init__(self,x,y,image,type,flagged=False,known=False):
        self.x,self.y=x *Tile,y*Tile
        self.image=image
        self.flagged=flagged
        self.type=type
        self.known=known
    def __repr__(self):
        return self.type
    def draw(self,surface):
        if not self.flagged and self.known:
            surface.blit(self.image,(self.x , self.y))
        elif self.flagged and not self.known:
            surface.blit(image_Flag,(self.x,self.y))
        elif not self.known:
            surface.blit(image_Unknown,(self.x,self.y))
class Board:
    def __init__(self):
        self.surface=pygame.Surface((Width,Height))
        self.board_list=[[Tiles(row,col,image_empty,"U") for col in range(cols)]for row in range(rows)]
        self.place_mines()
        self.clues()
        self.dug=[]
    def draw(self,screen):
        for row in self.board_list:
            for tile in row:
                tile.draw(self.surface)
        screen.blit(self.surface,(0,0))
    def clues(self):
        for row in range(rows):
            for col in range(cols):
                if self.board_list[row][col].type != "M":
                    total_mine=self.mines_count(row,col)
                    if total_mine>0:
                        self.board_list[row][col].type="N"
                        self.board_list[row][col].image=image_numbers[total_mine-1]
    @staticmethod
    def is_inside(x,y):
        return 0<=x<rows and 0<=y<cols
    def mines_count(self,x,y):
        total_mines=0
        for row in range(-1,2):
            for col in range(-1,2):
                x_negh=x+row
                y_negh=y+col
                if self.is_inside(x_negh,y_negh) and self.board_list[x_negh][y_negh].type=="M":
                    total_mines+=1
        return total_mines
    def place_mines(self):
        for _ in range(MinesCount):
            while True :
                x=random.randint(0,rows-1)
                y=random.randint(0,cols-1)
                if self.board_list[x][y].type == "U":
                    self.board_list[x][y].type="M"
                    self.board_list[x][y].image=image_Mine
                    break
    def display(self):
        for row in self.board_list:
            print(row)
    def dig(self,x,y):
        self.dug.append((x,y))
        if self.board_list[x][y].type=="M":
            self.board_list[x][y].known=True
            self.board_list[x][y].image=image_Exploded
            return False
        elif self.board_list[x][y].type=="N":
            self.board_list[x][y].known=True
            return True
        self.board_list[x][y].known=True
        for row in range(max(0,x-1),min(rows-1,x+1)+1):
            for col in range(max(0,y-1),min(cols-1,y+1)+1):
                if (row,col) not in self.dug:
                    self.dig(row,col)
        return True


