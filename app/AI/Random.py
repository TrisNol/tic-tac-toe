from ai.ai import AI
from random import randint

class Random(AI):
    """Implementation of the AI-Class based a Random procedure."""

    def recommend_move(self, field: list, player: int) -> tuple:        
        # Generate random row and column indexes and check if the cell is free, Main discription see in parent class ai.
        row = -1
        column = -1
        for x in range(100): 
            row = randint(0,len(field)-1)
            column = randint(0,len(field)-1)
            # empty cell found
            if field[row][column] =='':
                print('Free field at: ', row, column )
                print('taken iterations: ', x)
                break

        return (row, column)