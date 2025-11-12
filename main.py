import pygame 
import os
import random

# game setting 

pygame.init()

home = pygame.transform.scale(
    pygame.image.load(os.path.join("HOME1.png")), (900,600))

Tile = 35

scini = pygame.display.set_mode((900,600))
pygame.display.set_caption("Minesweeper: Home")


rows = 16
cols = 16
MinesCount = 30

one = True
while one:
    scini.blit(home, (0, 0))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

        
        if event.type == pygame.MOUSEBUTTONDOWN:
            px, py = pygame.mouse.get_pos()

            # --- EASY ---
            if 0< px < 300 and 0 < py < 600:
                rows = 9
                cols = 9
                MinesCount = 10
                one = False
                Width = Tile * cols
                Height = Tile * rows+70
                break

            #MEDIUM
            if 300 < px < 600 and 0 < py < 600:
                rows = 16
                cols = 16
                MinesCount = 40
                one = False
                Width = Tile * cols
                Height = Tile * rows+70
                break
            #HARD

            
            if 600 < px < 900 and 0< py < 600:
                rows = 20
                cols = 20
                MinesCount = 70
                one = False
                Width = Tile * cols
                Height = Tile * rows+70
                break


Title="Minesweeper"
FPS=100
BGcolour="#5C5E59"


image_numbers=[]

for i in range(1,9):
    image_numbers.append(pygame.transform.scale(pygame.image.load(os.path.join(f"N-{i}.jpeg")),(Tile,Tile)))
image_empty=pygame.transform.scale(pygame.image.load(os.path.join("Empty.jpeg")),(Tile,Tile))
image_Flag=pygame.transform.scale(pygame.image.load(os.path.join("Flag.jpeg")),(Tile,Tile))
image_Mine=pygame.transform.scale(pygame.image.load(os.path.join("Mine.jpeg")),(Tile,Tile))
image_Unknown=pygame.transform.scale(pygame.image.load(os.path.join("Unknown.jpeg")),(Tile,Tile))
image_Exploded=pygame.transform.scale(pygame.image.load(os.path.join("Exploded.jpeg")),(Tile,Tile))
image_notABomb=pygame.transform.scale(pygame.image.load(os.path.join("!(Bomb).jpeg")),(Tile,Tile))




class Game :
    def __init__(self):
        

                    
            

        

        self.screen=pygame.display.set_mode((Width,Height))
        pygame.display.set_caption(Title)
        self.clock=pygame.time.Clock()
    def run(self):
        self.play=True
        while self.play:
            self.clock.tick(FPS)
            self.events()
            self.draw()
        else :
            self.endgame()
    def new(self): 
        self.board=Board()
        self.board.display()
    def draw(self):
        self.screen.fill(BGcolour)
        self.board.draw(self.screen)
        pygame.display.flip()
    def restart_menu(self):
    
    
        restart = pygame.transform.scale(pygame.image.load(os.path.join("restart.png")), (310,70))
        one = True
        while one:
            self.screen.blit(restart, ((Width//2)-155,Height-70))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)

                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    px, py = pygame.mouse.get_pos()

                    
                    if 0< px < Width//2:
                        
                        game=Game()
                        game.new()
                        game.run()
                        
                        break
                    else:
                        pygame.quit()
                        quit(0)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)
            if event.type==pygame.MOUSEBUTTONDOWN:
                px,py=pygame.mouse.get_pos()
                px//=Tile
                py//=Tile
                if event.button==1:
                    if not self.board.board_list[px][py].flagged:
                        if not self.board.dig(px,py):
                            for row in self.board.board_list:
                                for tile in row:
                                    if tile.flagged and tile.type !="M":
                                        tile.flagged=False
                                        tile.known=True
                                        tile.image=image_notABomb
                                    elif tile.type=="M":
                                        tile.known=True
                            self.play=False    
                if event.button==3:
                    if not self.board.board_list[px][py].known:
                        self.board.board_list[px][py].flagged = not self.board.board_list[px][py].flagged 
                if self.won():
                    self.play=False
                    for row in self.board.board_list:
                        for tile in row:
                            if not tile.known:
                                tile.flagged=True
    def won(self):
        for row in self.board.board_list:
            for tile in row:
                if tile.type != "M" and not tile.known:
                    return False
        return True
    def endgame(self):
        while True:
            self.restart_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit(0)
                if event.type==pygame.MOUSEBUTTONDOWN:
                    return

#functioning part below
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
        for row in [list(row) for row in zip(*self.board_list)]:
            print(row)
    def dig(self,x,y):
        if not self.dug:
            if not self.board_list[x][y].type=="U" :
                return True
            








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


                
                #HARD
    




game=Game()
game.new()
game.run()
