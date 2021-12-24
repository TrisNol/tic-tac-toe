from ai.ai import AI
from utils.db import DB
from logic import GameMaster
import time


class MiniMax(AI): 
	"""Implementation of AI"""

	def __init__(self) -> None: 
		super().__init__()

	def recommend_move(self, field: list, player: int, sign1=0, sign2=1) -> tuple: 
		self.size = len(field)
		self.sign1 = sign1
		self.sign2 = sign2
		self.board_list = []
		start = time.perf_counter()
		best = find_best_move(self,field)
		stop = time.perf_counter()
		calctime = stop-start
		print('Calc_Time : ', calctime)
		print('Debug Minimax best move: ', best)
		print(len(self.board_list))
		print(self.board_list)
		#initialize returning values
		row = -1    
		column = -1

		return best

# This is the evaluation function as discussed
# in the previous article ( http://goo.gl/sJgv68 )
def evaluate(self, board, size, sign1, sign2):
	"""Helper-Method to convert a field of symbols (e.g.: X and O) to the int representation expected by recommend_move()

        Parameters:
            board (): Nested list of integers representing the Tic-Tac-Toe field
            size (str): Size of the board
            sign1 (str): Symbol used to identify Player 1
			sign2 (str): Symbol used to identify Player 1

        Returns:
            list: Tic-Tac-Toe field with player symbols replaces by 0 and 1
        """
	self.size = size
	self.board = board
	#sign2 is maximizer --> get positive values
	#sign1 is minimizer --> get negative values

	for i in range(self.size):
		if all(x == self.board[i][0] for x in [self.board[i][j] for j in range(self.size)]) and self.board[i][0] != "":
			if (board[i][0] == self.player):
				return 10
			elif (board[i][0] == self.opponent):
				return -10
	# Checking for Columns for X or O victory.
	for i in range(self.size):
		if all(x == self.board[0][i] for x in [self.board[j][i] for j in range(self.size)]) and self.board[0][i] != "":
		
			if (board[0][i] == self.player):
				return 10
			elif (board[0][i] == self.opponent):
				return -10

	# checking if dioagonal from top-left to bottom-right crossed
	if all(x == self.board[0][0] for x in [self.board[i][i] for i in range(self.size)]) and self.board[0][0] != "":
		if (board[0][0] == self.player):
			return 10
		elif (board[0][0] == self.opponent):
			return -10

		# checking if dioagonal from top-right to bottom-left crossed
	if all(x == self.board[0][self.size-1] for x in [self.board[self.size-1-i][i] for i in range(self.size-1, -1, -1)]) and self.board[0][self.size-1] != "":	
		if (board[0][2] == self.player):
			return 10
		elif (board[0][2] == self.opponent):
			return -10
	# Else if none of them have won then return 0
	return 0

def is_moves_left(self, board):

	for i in range(self.size):
		for j in range(self.size):
			if (board[i][j] == ''):
				return True
	return False

def minimax(self, board, depth, is_max, alpha = float('-inf'), beta = float('inf')):

	interrupt = 10
	cnt = 0
	score = evaluate(self, board, self.size, self.sign1, self.sign2)
	
	# If Maximizer has won the game return his/her
	# evaluated score
	if (score == 10):
		return score

	# If Minimizer has won the game return his/her
	# evaluated score
	if (score == -10):
		return score

	# If there are no more moves and no winner then
	# it is a tie
	if (is_moves_left(self,board) == False):
		return 0

	# If this maximizer's move
	if (is_max):	
		best = -1000

		# Traverse all cells
		for i in range(self.size):			
			for j in range(self.size):		

				#Check if cell is empty
				if (board[i][j] ==''):	
					#print('Debug Minimax Board: ', board)
					# Make the move
					board[i][j] = self.sign2
					# Call minimax recursively and choose
					# the maximum value
					best = max(best, minimax(self, board, depth + 1, is_max))
					self.cnt += 1
					
					# Undo the move
					board[i][j] = ''
					
					#break recursive loop to save processing time --> depends on board size
					if depth > self.depth:
						#print('Debug break recursion maxi')
						return best

		return best

	# If this minimizer's move
	else:
		best = 1000

		# Traverse all cells
		for i in range(self.size):		
			for j in range(self.size):
			
				# Check if cell is empty
				if (board[i][j] == ''):
				
					# Make the move
					board[i][j] = self.sign1
					# Call minimax recursively and choose
					# the minimum value
					best = min(best, minimax(self,board, depth + 1,  not is_max)) #not is_max
					self.cnt+=1
					# Undo the move
					board[i][j] = ''

					#break recursive loop to save processing time --> depends on board size
					if depth > self.depth:
						#print('Debug break recursion mini')
						return best


		return best


# This will return the best possible move for the player
def find_best_move(self, board) :
	best_val = -1000
	best_move = (-1, -1)
	self.player = self.sign2
	self.opponent = self.sign1
	self.cnt = 0
	# Traverse all cells, evaluate minimax function for
	# all empty cells. And return the cell with optimal
	# value.

	#--------------------------------------------
	#pre-processing to get free elements of board
	#to decide the depth of MiniMax
	#--------------------------------------------
	free = 0
	self.depth = 0
	for i in range(self.size):	
		for j in range(self.size):
			if board[i][j] =='':
				free+=1

	if free > 15:
		self.depth = 1
	elif free > 10 and free <= 15:
		self.depth = 2
	elif free > 7 and free <= 10:
		self.depth=4
	elif free > 4 and free <= 7:
		self.depth = 8		
	elif free <= 4:
		self.depth = 20
	


	for i in range(self.size):	
		for j in range(self.size):
			if (board[i][j] == ''):
				board[i][j] = self.player
				move_val = minimax(self, board, 0, False) 
				board[i][j] = ''

				if (move_val > best_val):			
					best_move = (i, j)
					best_val = move_val
	return best_move