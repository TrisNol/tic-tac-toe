from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

from Logic import GameMaster
from Logic.IController import IController

# Quelle:
# https://www.geeksforgeeks.org/tic-tac-toe-game-using-pyqt5-in-python/


# create a Window class
class Window(QMainWindow):
    master: IController = None
    # constructor
    def __init__(self):
        super().__init__()
        self.master = GameMaster(3)
        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100,
                         300, 500)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):

        # creating a push button list
        self.push_list = []

        # creating 2d list
        for _ in range(self.master.size):
            temp = []
            for _ in range(self.master.size):
                temp.append((QPushButton(self)))
            # adding 3 push button in single row
            self.push_list.append(temp)

        # x and y co-ordinate
        x = 90
        y = 90

        # traversing through push button list
        for i in range(self.master.size):
            for j in range(self.master.size):

                # setting geometry to the button
                self.push_list[i][j].setGeometry(x*i + 20,
                                                 y*j + 20,
                                                 80, 80)

                # setting font to the button
                self.push_list[i][j].setFont(QFont(QFont('Times', 17)))

                # adding action
                # https://stackoverflow.com/questions/6784084/how-to-pass-arguments-to-functions-by-the-click-of-button-in-pyqt/42945033
                self.push_list[i][j].clicked.connect(lambda state, i=i, j=j: self.action_called(i,j))

        # creating label to tel the score
        self.label = QLabel(self)

        # setting geometry to the label
        self.label.setGeometry(20, 300, 260, 60)

        # setting style sheet to the label
        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black;"
                                 "background : white;"
                                 "}")

        # setting label alignment
        self.label.setAlignment(Qt.AlignCenter)

        # setting font to the label
        self.label.setFont(QFont('Times', 15))

        # creating push button to restart the score
        reset_game = QPushButton("Reset-Game", self)

        # setting geometry
        reset_game.setGeometry(50, 380, 200, 50)

        # adding action action to the reset push button
        reset_game.clicked.connect(self.reset_game_action)

    # method called by reset button

    def reset_game_action(self):

        # resetting values
        self.master = GameMaster(self.master.size)

        # making label text empty:
        self.label.setText("")

        # traversing push list
        for buttons in self.push_list:
            for button in buttons:
                # making all the button enabled
                button.setEnabled(True)
                # removing text of all the buttons
                button.setText("")

    # action called by the push buttons
    def action_called(self, row, column):
        self.master.set_field(row, column, self.master.current_player)

        # getting button which called the action
        button = self.sender()

        # making button disabled
        button.setEnabled(False)

        # checking the turn
        if self.master.current_player == 0:
            button.setText("X")
        else:
            button.setText("O")

        # call the winner checker method
        win = self.master.is_won()

        # text
        text = ""

        # if winner is decided
        if win == True:
            # if current chance is 0
            if self.master.current_player == 0:
                # O has won
                text = "X Won"
            # X has won
            else:
                text = "O Won"

            # disabling all the buttons
            for buttons in self.push_list:
                for push in buttons:
                    push.setEnabled(False)

        # if winner is not decided
        # and total times is 9
        elif self.master.is_draw():
            text = "Match is Draw"

        # setting text to the label
        self.label.setText(text)
        self.master.next_player()

if __name__ == '__main__':
    # create pyqt5 app
    App = QApplication(sys.argv)

    # create the instance of our Window
    window = Window()

    # start the app
    sys.exit(App.exec())
