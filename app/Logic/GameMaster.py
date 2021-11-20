
from IController import IController


class GameMaster(IController):
    turn = 0
    times = 0
    size = 0

    board = []

    def build_board(self, n: int = 3) -> list:
        if n < 3:
            raise TypeError('Board cannot have less than 3 fields per row')
        self.size = n
        self.board = [["" for i in range(self.size)]
                      for j in range(self.size)]

    def is_won(self) -> bool:
        # checking if any row crossed
        for i in range(self.size):
           if all(x.upper() == self.board[i][0].upper() for x in [self.board[i][j] for j in range(self.size)]) and self.board[i][0].upper() != "":
                return True

        # checking if any column crossed
        for i in range(self.size):
            if all(x.upper() == self.board[0][i].upper() for x in [self.board[j][i] for j in range(self.size)]) and self.board[0][i].upper() != "":
                return True

        if all(x.upper() == self.board[0][0].upper() for x in [self.board[i][i] for i in range(self.size)]) and self.board[0][0].upper() != "":
            return True

        if all(x.upper() == self.board[0][self.size-1].upper() for x in [self.board[self.size-1-i][i] for i in range(self.size-1, -1, -1)]) and self.board[0][self.size-1].upper() != "":
            return True

        # if nothing is crossed
        return False


if __name__ == "__main__":
    temp = GameMaster()
    temp.build_board(4)

    # temp.board= [['X','X','X'], [], []]
    temp.board[0][0] = 'X'
    temp.board[1][0] = 'X'
    temp.board[2][0] = 'X'
    temp.board[3][0] = 'X'
    print(temp.board)
    print(f"hat gewonnen? {temp.is_won()}")
