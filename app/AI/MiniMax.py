from AI.AI import AI
from utils.DB import DB
from Logic import GameMaster
import time


class MiniMax(AI):  #create class 'MiniMax'

	def __init__(self) -> None: #receive Board-list and current player
		super().__init__()
		print('constructor MiniMax')

	def recommendMove(self, field: list, player: int, sign1, sign2) -> tuple: #receive Board-list and current player
		self.size=len(field)
		self.sign1=sign1
		self.sign2=sign2
		self.boardlist=[]
		start=time.perf_counter()
		best=findBestMove(self,field)
		stop=time.perf_counter()
		calctime=stop-start
		print('Calc_Time : ', calctime)
		print('Debug Minimax best move: ', best)
		print(len(self.boardlist))
		print(self.boardlist)
		#initialize returning values
		row = -1    
		column = -1

		return best

# This is the evaluation function as discussed
# in the previous article ( http://goo.gl/sJgv68 )
def evaluate(self, b, size,sign1,sign2) :
	self.size=size
	self.board=b
	#sign2 is maximizer --> get positive values
	#sign1 is minimizer --> get negative values

	for i in range(self.size):
		if all(x == self.board[i][0] for x in [self.board[i][j] for j in range(self.size)]) and self.board[i][0] != "":
			if (b[i][0] == self.player) :
				return 10
			elif (b[i][0] == self.opponent) :
				return -10
	# Checking for Columns for X or O victory.
	for i in range(self.size):
		if all(x == self.board[0][i] for x in [self.board[j][i] for j in range(self.size)]) and self.board[0][i] != "":
		
			if (b[0][i] == self.player) :
				return 10
			elif (b[0][i] == self.opponent) :
				return -10

	# checking if dioagonal from top-left to bottom-right crossed
	if all(x == self.board[0][0] for x in [self.board[i][i] for i in range(self.size)]) and self.board[0][0] != "":
		if (b[0][0] == self.player) :
			return 10
		elif (b[0][0] == self.opponent) :
			return -10

		# checking if dioagonal from top-right to bottom-left crossed
	if all(x == self.board[0][self.size-1] for x in [self.board[self.size-1-i][i] for i in range(self.size-1, -1, -1)]) and self.board[0][self.size-1] != "":	
		if (b[0][2] == self.player) :
			return 10
		elif (b[0][2] == self.opponent) :
			return -10
	# Else if none of them have won then return 0
	return 0

def isMovesLeft(self, board) :

	for i in range(self.size) :
		for j in range(self.size) :
			if (board[i][j] == '') :
				return True
	return False

def minimax(self, board, depth, isMax, alpha = float('-inf'), beta = float('inf')) :

	interrupt=10
	cnt=0
	score = evaluate(self, board,self.size,self.sign1,self.sign2)
	#print('Debug score: ',score)
	# If Maximizer has won the game return his/her
	# evaluated score
	if (score == 10) :
		return score

	# If Minimizer has won the game return his/her
	# evaluated score
	if (score == -10) :
		return score

	# If there are no more moves and no winner then
	# it is a tie
	if (isMovesLeft(self,board) == False) :
		return 0

	# If this maximizer's move
	if (isMax) :	
		best = -1000

		# Traverse all cells
		for i in range(self.size) :			
			for j in range(self.size) :		

				#Check if cell is empty
				if (board[i][j]==''):	
					#print('Debug Minimax Board: ', board)
					# Make the move
					board[i][j]=self.sign2
					# Call minimax recursively and choose
					# the maximum value
					best = max(best, minimax(self,board,depth + 1, isMax))
					self.cnt+=1
					
					# Undo the move
					board[i][j] = ''
					
					#break recursive loop to save processing time --> depends on board size
					if depth > self.tiefe:
						#print('Debug break recursion maxi')
						return best

		return best

	# If this minimizer's move
	else :
		best = 1000

		# Traverse all cells
		for i in range(self.size) :		
			for j in range(self.size) :
			
				# Check if cell is empty
				if (board[i][j] == '') :
				
					# Make the move
					board[i][j] = self.sign1
					# Call minimax recursively and choose
					# the minimum value
					best = min(best, minimax(self,board, depth + 1,  not isMax)) #not isMax
					self.cnt+=1
					# Undo the move
					board[i][j] = ''

					#break recursive loop to save processing time --> depends on board size
					if depth > self.tiefe:
						#print('Debug break recursion mini')
						return best


		return best


# This will return the best possible move for the player
def findBestMove(self, board) :
	bestVal = -1000
	bestMove = (-1, -1)
	self.player=self.sign2
	self.opponent=self.sign1
	self.cnt=0
	# Traverse all cells, evaluate minimax function for
	# all empty cells. And return the cell with optimal
	# value.

	#--------------------------------------------
	#pre-processing to get free elements of board
	#to decide the depth of MiniMax
	#--------------------------------------------
	free=0
	self.tiefe=0
	for i in range(self.size) :	
		for j in range(self.size) :
			if board[i][j]=='':
				free+=1

	if free>15:
		self.tiefe=1
	elif free>10 and free<=15:
		self.tiefe=2
	elif free>7 and free<=10:
		self.tiefe=4
	elif free>4 and free<=7:
		self.tiefe=8		
	elif free<=4:
		self.tiefe=20
	
	#--------------------------------

	#self.tiefe=((self.size*self.size)-free)*1
	print('freie Felder: ', free)
	print('empfohlene Tiefe: ', self.tiefe)

	for i in range(self.size) :	
		for j in range(self.size) :
		
			# Check if cell is empty
			if (board[i][j] == '') :
			
				# Make the move
				board[i][j] = self.player
				#print(board)

				# compute evaluation function for this
				# move.
				moveVal = minimax(self, board, 0, False) #True: Maximizer; False: Minimizer turn

				# Undo the move
				board[i][j] = ''

				# If the value of the current move is
				# more than the best value, then update
				# best/
				if (moveVal > bestVal) :			
					bestMove = (i, j)
					bestVal = moveVal

	print("The value of the best Move is :", bestVal)
	print()
	print('Counter: ',self.cnt)
	return bestMove