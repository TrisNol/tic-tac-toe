from abc import ABC

class IController(ABC):

    
    def build_board(self, n: int)->list:
        pass

    def is_won(self)->bool:
        pass

