from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from datetime import datetime
from copy import deepcopy

from Logic import GameMaster
from Model.Game import Game
from Model.GameTurn import GameTurn
from utils.DB import DB
from windows import Leaderboard

# create a Window class


class Window(QMainWindow):
    master = None
    # constructor

    def __init__(self):
        super().__init__()

        n = 5
        self.master = GameMaster(n)
        self.start = False

        self.initialize_record_parameter()

        # DB instance
        self.db = DB()

        # setting title
        self.setWindowTitle("Python ")

        # setting geometry
        self.setGeometry(100, 100,
                         n*100, (n+1)*2*100)  # (X,Y,Breite,Höhe)

        # calling method
        self.UiComponents()

        # showing all the widgets
        self.show()

    # method for components
    def UiComponents(self):

        # creating a push button list
        self.push_list = []

        # creating 2d list; Befülle die Reihe mit drei Button
        for _ in range(self.master.size):
            temp = []
            for _ in range(self.master.size):
                temp.append((QPushButton(self)))
            # adding 3 push button in single row
            # befülle die 'push_list' mit 3x3 Elementen
            self.push_list.append(temp)

        # x and y co-ordinate
        x = 90
        y = 90

        # traversing through push button list
        for i in range(self.master.size):
            for j in range(self.master.size):

                # setting geometry to the button
                self.push_list[i][j].setGeometry(x*i + 20,  # Startkoordinate für Auswahlfelder in X
                                                 y*j + 170,  # Startkoordinate für Auswahlfelder in Y
                                                 80, 80)  # Groeße der Felder

                # setting font to the button X or O define font and size
                self.push_list[i][j].setFont(QFont(QFont('Times', 30)))

                # adding action
                self.push_list[i][j].clicked.connect(
                    lambda state, i=i, j=j: self.action_called(i, j))

        # creating label to tel the score
        self.label = QLabel(self)

        # setting geometry to the label
        self.label.setGeometry(20, self.master.size*100+150, 260, 60)

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
        # -------------------------------------------------------
        # Neuer Button zum Beenden des Spiels
        exit_game = QPushButton("Exit", self)
        # setting geometry
        exit_game.setGeometry(50, self.master.size*100 +
                              325, 200, 50)  # (X, Y, Breite, Höhe)
        exit_game.setStyleSheet('background-color: red')

        # adding action action to the reset push button
        exit_game.clicked.connect(self.exit_game_action)
        # ------------------------------------------------------

        # -------------------------------------------------------
        # Neuer Button zum Start des Spiels --> Verriegelung der Zeichenauswahl, Spielername, Freigabe des Spielfelds
        start_game = QPushButton("Start", self)
        # setting geometry
        # (X, Y, Breite, Höhe)
        start_game.setGeometry(50, self.master.size*100+225, 200, 50)
        start_game.setStyleSheet('background-color: green')

        # adding action action to the reset push button
        start_game.clicked.connect(self.start_game_action)
        # ------------------------------------------------------

        # setting geometry
        reset_game.setGeometry(50, self.master.size*100 + 275, 200, 50)

        # adding action action to the reset push button
        reset_game.clicked.connect(self.reset_game_action)

        # --------------------------------------
        # Leaderboard
        leaderboard = QPushButton("Leaderboard", self)
        leaderboard.setGeometry(50, self.master.size*100+350, 200, 50)
        leaderboard.setStyleSheet('background-color: yellow')

        # adding action action to the 
        leaderboard.clicked.connect(self.show_leaderboard)
        # ComboBox Item für Auswahl des Zeichens
        # --------------------------------------
        self.labelPlayer1 = QLabel(self)
        self.labelPlayer1.setText('Spieler 1')
        self.labelPlayer1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.labelPlayer1.setFont(QFont('Arial', 16))

        self.labelPlayer2 = QLabel(self)
        self.labelPlayer2.setText('Spieler 2')
        self.labelPlayer2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.labelPlayer2.setFont(QFont('Arial', 16))

        self.playername1 = QLineEdit(self)  # erstelle Texteingabe Spieler 1
        # Defaultwert 'Spieler 1' für Name
        self.playername1.setText('Spieler 1')
        self.player1 = 'Spieler 1'
        # erstelle DropDown Objekt Zeichen Spieler 1
        self.selectsign1 = QComboBox(self)
        self.selectsign1.setFont(QFont('Arial', 20))
        # self.selectcolour1=QComboBox(self) #erstelle DropDown Objekt Farbe Spieler 1

        self.playername2 = QLineEdit(self)  # erstelle Texteingabe Spieler 2
        # Defaultwert 'Spieler 2' für Name
        self.playername2.setText('Spieler 2')
        self.player2 = 'Spieler 2'
        # erstelle DropDown Objekt Zeichen Spieler 2
        self.selectsign2 = QComboBox(self)
        self.selectsign2.setFont(QFont('Arial', 20))
        # self.selectcolour2=QComboBox(self) #erstelle DropDown Objekt Farbe Spieler 2

        # --------------------------------------------------------------------
        # Zeichensatz: hier wird festgelegt, welche Zeichen zur Auswahl stehen
        # und die Dropdownliste befüllt
        # ------------------------------
        self.zeichensatz = ['', 'X', 'O', 'Ø', '@', '!', '?']

        for x in range(len(self.zeichensatz)):
            self.selectsign1.addItem(self.zeichensatz[x])
            self.selectsign2.addItem(self.zeichensatz[x])

        # ------------
        # Farbauswahl nicht fertig!!!
        # -----------
        self.farbensatz = ['red', 'green', 'blue', 'yellow', 'grey', 'white']

        # -----------------------
        # GUI Elemente platzieren
        # -----------------------
        self.labelPlayer1.setGeometry(30, 10, 100, 30)
        self.playername1.setGeometry(30, 45, 100, 30)
        # Koordinate, Abmaße des Dropdowns
        self.selectsign1.setGeometry(30, 80, 100, 30)
        # self.selectcolour1.setGeometry(30,115,100,30)

        self.labelPlayer2.setGeometry(180, 10, 100, 30)
        self.selectsign2.setGeometry(180, 80, 100, 30)
        self.playername2.setGeometry(180, 45, 100, 30)
        # self.selectcolour2.setGeometry(180,115,100,30)

        # ------------------------------------------

        # ---------------------------------
        # Aufruf Methode bei Zeichenwechsel
        # ---------------------------------
        self.selectsign1.activated[str].connect(self.sign_changed1)
        self.selectsign2.activated[str].connect(self.sign_changed2)
        self.playername1.textChanged.connect(self.textchangedPlayer1)
        self.playername2.textChanged.connect(self.textchangedPlayer2)
        # --------------------------------


# ----------------
# Methoden für GUI
# ----------------

    def textchangedPlayer1(self, s):
        self.player1 = s

    def textchangedPlayer2(self, s):
        self.player2 = s

    def sign_changed1(self, s):
        self.sign1 = s
        zeichenTemp = self.zeichensatz
        print('Auswahl geaendert Spieler 1!', s)

    def sign_changed2(self, s):
        self.sign2 = s
        zeichenTemp = self.zeichensatz
        print('Auswahl geaendert Spieler 2!', s)

    def start_game_action(self):
        print('Test Start')
        self.selectsign1.setEnabled(False)
        self.playername1.setEnabled(False)
        self.selectsign2.setEnabled(False)
        self.playername2.setEnabled(False)
        self.start = True
        # Highlighte Spieler 1 bei Spielstart
        self.labelPlayer1.setStyleSheet('background: lightgreen')
        self.initialize_game_class()

    def show_leaderboard(self):
        print('Start showing Leaderboard')
        self.w = Leaderboard()
        self.w.show()
        self.hide()

    def initialize_game_class(self):
        self.game.id = self.db.get_amount_off_documents()
        self.game.name_player1 = self.playername1.text()
        self.game.sign_player1 = self.selectsign1.currentText()
        self.game.name_player2 = self.playername2.text()
        self.game.sign_player2 = self.selectsign2.currentText()
        now = datetime.now()
        self.game.start_time = now.strftime("%d.%m.%Y %H:%M:%S")

    def write_game_stats(self, row, column, won=False):
        # temp = self.master
        player_id = self.master.current_player
        game_turn = GameTurn(player_id, row, column, deepcopy(self.master.board), self.turn_number, won)
        self.game.turns.append(game_turn.__dict__)
        self.turn_number += 1

    def initialize_record_parameter(self) -> None:
        self.game = Game()
        self.turn_number = 0

    def exit_game_action(self):
        print('Test')
        sys.exit()  # Beende Applikation

    # method called by reset button
    def reset_game_action(self):

        # resetting values
        self.selectsign1.setEnabled(True)
        self.playername1.setEnabled(True)
        self.selectsign2.setEnabled(True)
        self.playername2.setEnabled(True)
        self.start = False
        # making label text empty:
        self.label.setText("")

        # traversing push list
        for buttons in self.push_list:
            for button in buttons:
                # making all the button enabled
                button.setEnabled(True)
                # removing text of all the buttons
                button.setText("")
        self.master = GameMaster(self.master.size)

        self.initialize_record_parameter()

    # action called by the push buttons
    def action_called(self, row, column):

        # --------------
        # Verriegelung der Buttons weil Spiel nicht gestartet ist
        # --------------
        if self.start == False:
            self.label.setText('Spiel nicht gestartet!')
            return
        # -----------------
        # self.times += 1

        # getting button which called the action
        button = self.sender()

        # making button disabled
        button.setEnabled(False)

        # checking the turn
        if self.master.current_player == 0:
            # button.setText("X")
            self.labelPlayer1.setStyleSheet('background: lightgrey')
            self.labelPlayer2.setStyleSheet('background: lightgreen')
            button.setText(self.sign1)  # setze Spielzeichen Spieler 1
            self.master.set_field(row, column, self.sign1)
        else:
            self.labelPlayer1.setStyleSheet('background: lightgreen')
            self.labelPlayer2.setStyleSheet('background: lightgrey')
            button.setText(self.sign2)  # setze Spielzeichen Spieler 2
            self.master.set_field(row, column, self.sign2)

        # call the winner checker method
        # win = self.who_wins()
        win = self.master.is_won()
        draw = self.master.is_draw()

        # text
        text = ""

        # if winner is decided
        if win == True:
            # if current chance is 0
            if self.master.current_player == 1:
                # Spieler 2 hat gewonnen
                # text = "{} \n {} hat gewonnen".format(self.player2,self.sign2)
                text = "{} \n hat gewonnen".format(self.player2)
            # Spieler 1 hat gewonnen
            else:
                text = "{} \n hat gewonnen".format(self.player1)

            # disabling all the buttons
            for buttons in self.push_list:
                for push in buttons:
                    push.setEnabled(False)

        # if winner is not decided
        # and total times is 9
        elif draw:
            text = "Unentschieden"

        self.write_game_stats(row, column, win)

        if win or draw:
            now = datetime.now()
            self.game.end_time = now.strftime("%d.%m.%Y %H:%M:%S")
            self.game.winner = self.master.current_player
            self.db.write_record(self.game)

        # setting text to the label
        self.label.setText(text)
        self.master.next_player()


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window11 = Window()

# start the app
sys.exit(App.exec())
