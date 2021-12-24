from ai.ai import AI

class Strategy(AI):
    """
    Will indicate preferred fields
    """

    def __init__(self, buttons, board, game, starter=True) -> None:
        self.buttons = buttons
        self.board = board
        self.game = game
        self.starter = starter
        self.opponent_sign = self.game.sign_player2
        self.own_sign = self.game.sign_player1
        self.recommendation = []

    def handler(self):
        self.reset()
        if self.starter:
            self.starter = False
            self.first()
        else:
            # Check If I can win
            res = self.can_win(self.own_sign, self.opponent_sign)
            if res:
                self.highlight_button(res[0], res[1])
                return

            # Check If opponent can win
            res = self.can_win(self.opponent_sign, self.own_sign)
            if res:
                self.highlight_button(res[0], res[1])
                return
                
            self.analyze()

    def first(self):
        for i in range(0, len(self.buttons), 2):
            for j in range(0, len(self.buttons), 2):
                self.highlight_button(i, j)
        self.highlight_button(1, 1)

    def highlight_button(self, i, j):
        self.buttons[i][j].setStyleSheet("border :5px solid ;"
                                         "border-top-color : red; "
                                         "border-left-color :pink;"
                                         "border-right-color :yellow;"
                                         "border-bottom-color : green")

    def analyze(self):
        # Select corner
        for i in range(0, len(self.board), 2):
            for j in range(0, len(self.board), 2):
                if self.buttons[i][j].isEnabled():
                    if [i, j] not in self.recommendation:
                        self.recommendation.append([i, j])

        # Select Center if available
        if self.buttons[1][1].isEnabled():
            self.recommendation.append([1, 1])

        if len(self.recommendation) < 2:
            self.recommendation = []
            res = self.can_win(self.opponent_sign, self.own_sign, 0)
            if res:
                self.recommendation.append([res[0], res[1]])

        # Highlight preferred buttons
        for entry in self.recommendation:
            self.highlight_button(entry[0], entry[1])

        self.recommendation = []

    def enemy_check_column(self, column):
        for i in range(0, len(self.board)):
            if self.board[column][i] == self.opponent_sign:
                return True

    def enemy_check_row(self, row):
        for i in range(0, len(self.board)):
            if self.board[i][row] == self.opponent_sign:
                return True

    def enemy_check_left_right_diagonal(self):
        for i in range(0, 3):
            if self.board[i][i] == self.opponent_sign:
                return True

    def enemy_check_right_left_diagonal(self):
        temp = 0
        for i in reversed(range(2, -1, -1)):
            if self.board[i][temp] == self.opponent_sign:
                return True
            temp += 1

    def win_check_column(self, caller_sign, opponent_sign, threshold=2):
        counter = 0
        value = None
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if self.board[i][j] == opponent_sign:
                    break
                elif self.board[i][j] == caller_sign:
                    counter += 1
                else:
                    value = (i, j)
            if counter == threshold:
                return value
            counter = 0

    def win_check_row(self, caller_sign, opponent_sign, threshold=2):
        counter = 0
        value = None
        for i in range(0, len(self.board)):
            for j in range(0, len(self.board)):
                if self.board[j][i] == opponent_sign:
                    break
                elif self.board[j][i] == caller_sign:
                    counter += 1
                else:
                    value = (j, i)
            if counter == threshold:
                return value
            counter = 0
        return False

    def win_check_left_right_diagonal(self, caller_sign, opponent_sign, threshold=2):
        counter = 0
        value = None
        for i in range(0, 3):
            if self.board[i][i] == opponent_sign:
                break
            elif self.board[i][i] == caller_sign:
                counter += 1
            else:
                value = (i, i)
        if counter == threshold:
            return value

    def win_check_right_left_diagonal(self, caller_sign, opponent_sign, threshold=2):
        counter = 0
        temp = 0
        value = None
        for i in range(2, -1, -1):
            if self.board[i][temp] == opponent_sign:
                break
            elif self.board[i][temp] == caller_sign:
                counter += 1
            else:
                value = (i, temp)
            temp += 1

        if counter == threshold:
            return value

    def can_win(self, caller_sign, opponent_sign, threshold=2):
        res = self.win_check_column(caller_sign, opponent_sign, threshold)
        if res:
            return res

        res = self.win_check_row(caller_sign, opponent_sign, threshold)
        if res:
            return res

        res = self.win_check_left_right_diagonal(
            caller_sign, opponent_sign, threshold)
        if res:
            return res

        res = self.win_check_right_left_diagonal(
            caller_sign, opponent_sign, threshold)
        if res:
            return res

    def reset(self):
        for i in range(0, len(self.buttons), 1):
            for j in range(0, len(self.buttons), 1):
                if self.buttons[i][j].isEnabled():
                    self.buttons[i][j].setStyleSheet('background: lightgrey')
