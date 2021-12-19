from abc import ABC
import copy

class AI(ABC):

    def recommendMove(self, field: list, player: int) -> tuple:
        pass

    def translate_player_symbols(self, field, symbol_one, symbol_two):
        field = copy.deepcopy(field)
        for i in range(len(field)):
            for j in range(len(field[0])):
                if field[i][j] == symbol_one:
                    field[i][j] = 0
                elif field[i][j] == symbol_two:
                    field[i][j] = 1
        return field
