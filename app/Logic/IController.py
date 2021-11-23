from abc import ABC


class IController(ABC):
    current_player = 0
    times = 0
    size = 0

    labels = []
    board = []

    
    def build_board(self, n: int)->list:
        pass

    def is_won(self)->bool:
        pass

    def set_field(self, row, column, label):
        pass

    def next_player(self):
        pass

    def is_draw(self)->bool:
        pass

