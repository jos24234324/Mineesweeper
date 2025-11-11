import pygame
import os
# game setting 
Tile = 35
def start():
    pygame.init()

    home = pygame.transform.scale(
        pygame.image.load(os.path.join("HOME1.png")), (900,600)
    )
    
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
                    Height = Tile * rows
                    break

                
                if 300 < px < 600 and 0 < py < 600:
                    rows = 16
                    cols = 16
                    MinesCount = 40
                    one = False
                    Width = Tile * cols
                    Height = Tile * rows
                    break

                
                if 600 < px < 900 and 0< py < 600:
                    rows = 20
                    cols = 20
                    MinesCount = 70
                    one = False
                    Width = Tile * cols
                    Height = Tile * rows
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
