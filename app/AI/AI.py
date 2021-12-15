from abc import ABC


class AI(ABC):

    def recommendMove(self, field: list, player: int) -> tuple:
        pass
