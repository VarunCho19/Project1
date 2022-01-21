#Handles user input and the main driver for the chess game and display cuurent state
from curses import KEY_DOWN
import pygame as p
import chessEngine

WIDTH = HEIGHT =  512
DIMENSION = 8
sq_size = HEIGHT//DIMENSION
max_fps = 15
images = {}

#Intialize a glob dict of images
#images['wp'] gives the image of white pawn
def load_Images():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))



#main function
def main():   
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock() #creates timer/clock
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #only should when move is made
    load_Images()
    running = True
    sqSelected = ()# a tuple
    playerClicks = []# tracks player clicks
    while running:
        for x in p.event.get():
            if x.type == p.QUIT:
                running = False
            elif x.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()# gives in array of x and y
                col = location[0]//sq_size
                row = location[1]//sq_size
                if sqSelected == (row,col):#if same then need to restare
                    sqSelected = ()
                    playerClicks = []
                else: 
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2: #if there are two valid locations then will tell engine to move
                    move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)#passed through start and ending square and board
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = ()
                    playerClicks = []
            elif x.type == p.KEYDOWN:
                if x.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs)
        clock.tick(max_fps)
        p.display.flip()# updates screen

#Graphics for gamestate
def drawGameState(screen, gs):
    drawBoard(screen)#put squares on the board
    # put pieces on top of board
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("dark orange")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))

if __name__  == '__main__':
    main()
