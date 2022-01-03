from abc import ABC
import copy

class AI(ABC):
    """The abstract class AI mimics the behaviour of an interface in OOP. 
    This class is employed to unify the structure of the different AI implementations for Tic-Tac-Toe 
    in order to enable dependency injection."""

    def recommend_move(self, field: list, player: int) -> tuple:
        """Central method of this interface which will output the recommended row and column index for the given field and player

        Parameters:
            field (list): Nested list of integers representing the Tic-Tac-Toe field
            player (int): Number of the current player (0=Player 1, 1=Player 2)

        Returns:
            int, int: Row and column index recommended by the AI 
        """
        pass

    def translate_player_symbols(self, field, symbol_one, symbol_two) -> list:
        """Helper-Method to convert a field of symbols (e.g.: X and O) to the int representation expected by recommendMove()

        Parameters:
            field (list): Nested list of integers representing the Tic-Tac-Toe field
            symbol_one (str): Symbol used to identify Player 1
            symbol_two (str): Symbol used to identify Player 1

        Returns:
            list: Tic-Tac-Toe field with player symbols replaces by 0 and 1
        """
        field = copy.deepcopy(field)
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] == symbol_one:
                    field[i][j] = 0
                elif field[i][j] == symbol_two:
                    field[i][j] = 1
        return field
