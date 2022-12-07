import pygame
import os
import pyperclip

running = True

startx = 150
starty = 180
blocksx = 10
blocksy = 7
blocksize = 32
blockwidth = 2

pygame.init()
s = pygame.display.set_mode((blocksx * blocksize + 10 * blocksize, blocksy * blocksize + 18 * blocksize))
s.fill((20, 20, 20))

def grid(startx, starty, blocksx, blocksy, blocksize, blockwidth):
    for i in range(startx, startx + (blocksx * blocksize), blocksize):
        for j in range(starty, starty + (blocksy * blocksize), blocksize):
            rect = pygame.Rect(i, j, blocksize, blocksize)
            pygame.draw.rect(s, (255, 255, 255), rect, blockwidth)

cpx = 0
cpy = 0

def blockrenderer(x, y, color, smaller = False):
    global startx, starty, blocksize, blockwidth
    if(smaller):
        block = pygame.Rect(startx + (x * blocksize) + blocksize // 4, starty + (y * blocksize) + blocksize // 4, blocksize // 2, blocksize // 2)
    else:
        block = pygame.Rect(startx + (x * blocksize), starty + (y * blocksize), blocksize, blocksize)
    pygame.draw.rect(s, color, block, blocksize - 1)

piecesindex = {
    "I": (0, 255, 255),
    "Z": (255, 0, 0),
    "S": (0, 255, 0),
    "J": (0, 0, 255),
    "L": (255, 100, 0),
    "T": (255, 0, 255),
    "O": (255, 255, 0),
    "G": (156, 156 , 156),
    " ": (20, 20, 20)
}

rotation = 0

currentx = 0

piece = 0

smaller = False

filledpieces = []

def drawallpieces():
    for i in filledpieces:
        blockrenderer(i[0], i[1], piecesindex[i[2]], i[3])

def createcolorsquares():
    for v, i in enumerate(piecesindex):
        blockrenderer(blocksx + 2, v, piecesindex[i])

    blockrenderer(blocksx + 2, len(pieces) + 2, (255, 255, 255), smaller)

    blockrenderer(blocksx + 2, len(pieces) + 4, (0, 0, 255))

    blockrenderer(blocksx + 2, len(pieces) + 6, (255, 0, 255))

board = [["  " for i in range(blocksx)] for i in range(blocksy)]

def makeboard():
    for i in filledpieces:
        board[i[1]][i[0]] = str(i[2]) + "1" if (i[3]) else str(i[2]) + "0"

seperateframe = False

pieces = "IZSJLTOG "
pieceemojis = [":blue_square:", ":red_square:", ":green_square:", ":ballot_box_with_check:", ":orange_square:", ":purple_square:", ":yellow_square:", ":grey_exclamation:", ":black_large_square:"]

def outputcode():
    global board
    tempboard = []

    for i in board:
        for j in i:
            tempboard.append(pieceemojis[pieces.index(j[0])])
        tempboard.append("\n")

    tempboard = ''.join(tempboard)
    pyperclip.copy(tempboard)


while running:
    s.fill((30, 30, 30))
    makeboard()
    grid(startx, starty, blocksx, blocksy, blocksize, blockwidth)
    createcolorsquares()

    drawallpieces()

    for event in pygame.event.get():
        if pygame.mouse.get_pressed()[0]:
            pos = list(pygame.mouse.get_pos())
            pos[0] = (pos[0] - startx) // blocksize
            pos[1] = (pos[1] - starty) // blocksize

            if(pos[0] >= 0 and pos[0] < blocksx and pos[1] >= 0 and pos[1] < blocksy):
                filledpieces.append([pos[0], pos[1], pieces[piece], smaller])

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] < len(pieces)):
                piece = pos[1]

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] == len(pieces) + 2):
                smaller = not smaller

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] == len(pieces) + 4):
                outputcode()

            if(pos[0] == blocksx + 2 and pos[1] >= 0 and pos[1] == len(pieces) + 6):
                filledpieces = []
                board = [["  " for i in range(blocksx)] for i in range(blocksy)]

        if event.type == pygame.QUIT:
            running = False

    grid(startx, starty, blocksx, blocksy, blocksize, blockwidth)

    #rendering the screen; keep last
    pygame.display.update()
