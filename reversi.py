import pygame
from pygame.locals import *
import pprint
import sys
import time


pygame.init()
WIDTH = HEIGHT = 800
# Set up the window.
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Reversi!')

# Set up the colors.
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (125,125,125)
# Set up fonts.
basicFont = pygame.font.SysFont(None, 48)

#set up constants
GRID_WIDTH = WIDTH - 100
BLOCK_SIZE = GRID_WIDTH // 8
BOARD =[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
TILE = WHITE
OTHER_TILE = BLACK
def drawTitle():
	# Set up the text.
	text = basicFont.render('Reversi', True, BLACK, GREY)
	textRect = text.get_rect()
	textRect.topleft = ((WIDTH//2)-(textRect.width//2),10)
	windowSurface.blit(text, textRect)
	

def drawGrid():
	for y in range(50,GRID_WIDTH,BLOCK_SIZE):
		for x in range(50,GRID_WIDTH,BLOCK_SIZE):
			xb,yb = (y-50)//BLOCK_SIZE,(x-50)//BLOCK_SIZE
			BOARD[xb][yb] = {'content':' ','coors':(x,y),'index':(xb,yb)}
			pygame.draw.rect(windowSurface, BLACK, (x,y, BLOCK_SIZE, BLOCK_SIZE),4)

def whereToDrawCircle(x,y):
	for row in BOARD:
		for b in row:
			if x >= b['coors'][0] and x <= b['coors'][0] + BLOCK_SIZE and y >= b['coors'][1] and y <= b['coors'][1] + BLOCK_SIZE:
				return b
	return False
def drawCircle(b,color):
	b['content'] = color
	centerx = b['coors'][0]+(BLOCK_SIZE//2)
	centery = b['coors'][1]+(BLOCK_SIZE//2)
	pygame.draw.circle(windowSurface, color, (centerx, centery), BLOCK_SIZE-50, 0)

def onBoard(x,y):
	return x>=0 and x<=7 and y>=0 and y<=7

def isValidMove(board,move,tile):
	x,y = move
	possibles = []
	if onBoard(x,y) and board[x][y]['content'] == ' ':
		for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1],[0, -1], [-1, -1], [-1, 0], [-1, 1]]:
			possibles += checkBorders(x+xdirection,y+ydirection,xdirection,ydirection,board,tile)
	return possibles

def checkBorders(x,y,xdirection,ydirection,board,tile):
	other_tile = OTHER_TILE if TILE == tile else TILE
	possibles = []
	if onBoard(x,y):
		if board[x][y]['content'] == other_tile:
			while True:
				possibles.append([x,y])
				x += xdirection
				y += ydirection
				if onBoard(x,y):
					if board[x][y]['content'] == tile:
						return possibles
					if board[x][y]['content']==' ':
						return []
				else:
					return []
		if board[x][y]['content'] == tile or board[x][y]['content'] ==' ':
			return []
	return []

def makeMove(x,y,spots,tile):
	if spots:
		drawCircle(BOARD[x][y],tile)
		for x,y in spots:
			drawCircle(BOARD[x][y],tile)
def pc_move(board):
	copy = board.copy()
	if isValidMove(board,[0,0],OTHER_TILE) != []:
		makeMove(0,0,isValidMove(board,[0,0],OTHER_TILE),OTHER_TILE)

	if isValidMove(board,[0,7],OTHER_TILE) != []:
		makeMove(0,7,isValidMove(board,[0,7],OTHER_TILE),OTHER_TILE)

	if isValidMove(board,[7,0],OTHER_TILE) != []:
		makeMove(7,0,isValidMove(board,[7,0],OTHER_TILE),OTHER_TILE)

	if isValidMove(board,[7,7],OTHER_TILE) != []:
		makeMove(7,7,isValidMove(board,[7,7],OTHER_TILE),OTHER_TILE)
	else:
		best = []
		xc,yc = None,None
		for x in range(8):
			for y in range(8):
				if len(isValidMove(board,[x,y],OTHER_TILE)) > len(best):
					xc,yc = x,y
					best = isValidMove(board,[x,y],OTHER_TILE)
		if best != []:
			makeMove(xc,yc,best,OTHER_TILE)
def filledBoard(board):
	for row in board:
		for b in row:
			if b['content'] == ' ':
				return False
	return True


def getScore(board):
	tile_score = 0
	other_tile_score = 0
	for row in board:
		for b in row:
			if b['content'] == TILE:
				tile_score +=1
			if b['content'] == OTHER_TILE:
				other_tile_score +=1
	winner = 'computer' if other_tile_score > tile_score else 'you'
	return {'computer':other_tile_score,'you':tile_score,'winner':winner}


def drawText(text, surface,center):
	text = basicFont.render(text, True, BLACK, WHITE)
	textRect = text.get_rect()
	textRect.centerx = center[0]
	textRect.centery = center[1]
	surface.blit(text, textRect)
    
def gameOver():
	windowSurface.fill(WHITE)
	xc,yc = windowSurface.get_rect().centerx,windowSurface.get_rect().centery
	data = getScore(BOARD)
	drawText('GAME OVER!',windowSurface,[xc,yc-40])
	drawText(f"the score is : computer {data['computer']} you {data['you']}, {data['winner']} won!",windowSurface,[xc,yc])
	pygame.display.update()
	

def moreMoves(board,tile):
	for x in range(8):
		for y in range(8):
			if isValidMove(board,(x,y),tile) != []:
				return True
	return False

def setUpCanvs():
	windowSurface.fill(GREY)
	drawTitle()
	drawGrid()
	drawCircle(BOARD[3][3],OTHER_TILE)
	drawCircle(BOARD[3][4],TILE)
	drawCircle(BOARD[4][3],TILE)
	drawCircle(BOARD[4][4],OTHER_TILE)
	pygame.display.update()

setUpCanvs()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if not moreMoves(BOARD,TILE) and not moreMoves(BOARD,OTHER_TILE):
        	print(True)
        	gameOver()
        if event.type == MOUSEBUTTONUP:
        	b = whereToDrawCircle(event.pos[0],event.pos[1])
        	if b != False:
        		if isValidMove(BOARD,b['index'],TILE) != []:
        			makeMove(b['index'][0],b['index'][1],isValidMove(BOARD,b['index'],TILE),TILE)
	        		pygame.display.update()
	        		if filledBoard(BOARD):
	        			gameOver()
	        		time.sleep(0.3)
	        		pc_move(BOARD)
	        		pygame.display.update()
	        		if filledBoard(BOARD):
	        			gameOver()



























board =[[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', 'X', 'O', ' ', ' ', ' '],
		[' ', ' ', ' ', 'O', 'X', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
		[' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
TILE = 'X'
OTHER_TILE = 'O'

def make_move(board,move,tile):
	x,y = move
	possibles = []
	if onBoard(x,y) and board[x][y] == ' ':
		for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1],[0, -1], [-1, -1], [-1, 0], [-1, 1]]:
			possibles += function(x+xdirection,y+ydirection,xdirection,ydirection,board,tile)
	return possibles
def affect_move(x,y,spots,tile):
	if spots:
		board[x][y] = tile
		for x,y in spots:
			board[x][y] = tile


def function(x,y,xdirection,ydirection,board,tile):
	other_tile = OTHER_TILE if TILE == tile else TILE
	possibles = []
	if onBoard(x,y):
		if board[x][y] == other_tile:
			while True:
				possibles.append([x,y])
				x += xdirection
				y += ydirection
				if onBoard(x,y):
					if board[x][y] == tile:
						return possibles
					if board[x][y]==' ':
						return []
				else:
					return []
		if board[x][y] == tile or board==' ':
			return []
	return []
def onBoard(x,y):
	return x>=0 and x<=7 and y>=0 and y<=7
def pc_move(board):
	copy = board.copy()
	if make_move(board,[0,0],OTHER_TILE) != []:
		affect_move(0,0,make_move(board,[0,0],OTHER_TILE),OTHER_TILE)
		drawBoard(board)

	if make_move(board,[0,7],OTHER_TILE) != []:
		affect_move(0,7,make_move(board,[0,7],OTHER_TILE),OTHER_TILE)
		drawBoard(board)

	if make_move(board,[7,0],OTHER_TILE) != []:
		affect_move(7,0,make_move(board,[7,0],OTHER_TILE),OTHER_TILE)
		drawBoard(board)

	if make_move(board,[7,7],OTHER_TILE) != []:
		affect_move(7,7,make_move(board,[7,7],OTHER_TILE),OTHER_TILE)
		drawBoard(board)
	else:
		best = []
		xc,yc = None,None
		for x in range(8):
			for y in range(8):
				if len(make_move(board,[x,y],OTHER_TILE)) > len(best):
					xc,yc = x,y
					best = make_move(board,[x,y],OTHER_TILE)
		if best != []:
			affect_move(xc,yc,best,OTHER_TILE)
			drawBoard(board)
				
def drawBoard(board):
	# Print the board passed to this function. Return None.
	print('  01234567')
	print(' +--------+')
	for x in range(8):
		print('%s|' % x, end='')
		for y in range(8):
			print(board[x][y], end='')
		print('|%s' % x)
	print(' +--------+')
	print('  01234567')
# drawBoard(board)
# while True:
# 	inp = input()
# 	if inp == 'q':
# 		break
# 	x,y = inp[0],inp[1]	
# 	spots = make_move(board,[int(x),int(y)],TILE)
# 	affect_move(int(x),int(y),spots,TILE)
# 	drawBoard(board)
# 	pc_move(board)
