from logic.icontroller import IController

class GameMaster(IController):
    """Implementation of the IController for dynamic field sizes as provided in the constructor"""

    def __init__(self, board_size: int = 3):
        self.build_board(board_size)
        self.current_player = 0
        self.times = 0
        self.labels = []

    def build_board(self, n: int) -> list:
        if n < 3:
            raise TypeError('Board cannot have less than 3 fields per row')
        self.size = n
        self.board = [["" for i in range(self.size)]
                      for j in range(self.size)]

    def set_field(self, row: int, column: int, label: str) -> None:
        if row >= self.size and column >= self.size:
            raise IndexError('Row or column Index out of range')
        self.board[row][column] = label
        self.times += 1

    def next_player(self) -> None:
        self.current_player = int(not(self.current_player))

    def is_draw(self) -> bool:
        return self.times == (self.size*self.size)

    def is_won(self) -> bool:
        # checking if any row crossed

        for i in range(self.size):
            if all(x == self.board[i][0] for x in [self.board[i][j] for j in range(self.size)]) and self.board[i][0] != "":
                return True

        # checking if any column crossed
        for i in range(self.size):
            if all(x == self.board[0][i] for x in [self.board[j][i] for j in range(self.size)]) and self.board[0][i] != "":
                return True

        # checking if dioagonal from top-left to bottom-right crossed
        if all(x == self.board[0][0] for x in [self.board[i][i] for i in range(self.size)]) and self.board[0][0] != "":
            return True

        # checking if dioagonal from top-right to bottom-left crossed
        if all(x == self.board[0][self.size-1] for x in [self.board[self.size-1-i][i] for i in range(self.size-1, -1, -1)]) and self.board[0][self.size-1] != "":
            return True

        # if nothing is crossed
        return False
