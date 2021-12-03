from Logic.IController import IController
from random import randint


class GameMaster(IController):

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

    def set_field(self, row, column, label):
        if row >= self.size and column >= self.size:
            raise IndexError('Row or column Index out of range')
        self.board[row][column] = label
        self.times += 1

    def next_player(self):
        self.current_player = int(not(self.current_player))

    def is_draw(self):
        return self.times == (self.size*self.size)

    def is_won(self) -> bool:
        # checking if any row crossed
        #print('Debug Board Liste')
        #print(self.board)
        for i in range(self.size):
            if all(x == self.board[i][0] for x in [self.board[i][j] for j in range(self.size)]) and self.board[i][0] != "":
                return True

        # checking if any column crossed
        for i in range(self.size):
            if all(x == self.board[0][i] for x in [self.board[j][i] for j in range(self.size)]) and self.board[0][i] != "":
                return True

        if all(x == self.board[0][0] for x in [self.board[i][i] for i in range(self.size)]) and self.board[0][0] != "":
            return True

        if all(x == self.board[0][self.size-1] for x in [self.board[self.size-1-i][i] for i in range(self.size-1, -1, -1)]) and self.board[0][self.size-1] != "":
            return True

        # if nothing is crossed
        return False

    #--------------------------------------
    #KI Methode für das Setzen eines Feldes
    #--------------------------------------
    def KI_set(self):
        print('Debug KI_set')
        boardlist=[]
        #Generiere einen row/column Eintrag und überprüfe ob frei
        for x in range(len(self.board)):
            row=randint(0,len(self.board)-1)
            column=randint(0,len(self.board)-1)
            fieldstatus=self.board[row][column]
            if fieldstatus=='': #leeres Feld gefunden
                print('Freies Feld bei: ', row, column )
                break

        #Erstelle eine eindimensionale Liste aus der Boardliste
        for element in self.board:
            if type(element) is list:
                for item in element:
                    boardlist.append(item)
            else:
                boardlist.append(element)
        #-------------------------------------
        
                
        #print('boardlist: ', boardlist)
        print(row, column)
        return row, column


if __name__ == "__main__":
    temp = GameMaster()
    temp.build_board(4)

    # temp.board= [['X','X','X'], [], []]
    temp.set_field(0, 0, 'X')
    print(temp.current_player)
    temp.set_field(1, 0, 'X')
    print(temp.current_player)
    temp.set_field(2, 0, 'X')
    print(temp.current_player)
    temp.set_field(3, 0, 'X')
    print(temp.current_player)
    print(temp.board)
    print(f"hat gewonnen? {temp.is_won()}")

    temp.times = 16
    print(temp.is_draw())
