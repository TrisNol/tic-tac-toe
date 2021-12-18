from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from random import randint

from Logic import GameMaster
from Model.GameTurn import GameTurn
from datetime import datetime
from Analysis.Strategy import Strategy
from utils.DB import DB

import copy


class GameWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """

    def __init__(self, game, parent, KI):
        super().__init__()
        self.DB = DB()

        # print('Debug Uebergabe:',x,game.sign_player1,game.sign_player2,game.name_player1,game.name_player2)
        self.parent = parent
        self.game = game
        self.KIenabled = KI
        print(self.game.name_player2)
        # --------------------------------------------

        # Erstelle Spielfeld
        self.master = GameMaster(self.game.size)
        self.turn_number = 0

        self.withHelp = True
        self.strategy = None

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle('Game Window')
        self.setStyleSheet("background-color: grey;")
        # setting geometry
        self.setGeometry(700, 100, self.game.size*100,
                         (self.game.size+1)*120)  # (X,Y,Breite,Höhe)

        # Methode für UI Komponenten von GameWindow
        self.UiComponents()

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
                self.push_list[i][j].setGeometry(x*i + self.master.size*6,  # Startkoordinate für Auswahlfelder in X
                                                 y*j + 20,  # Startkoordinate für Auswahlfelder in Y
                                                 80, 80)  # Groeße der Felder

                # setting font to the button X or O define font and size
                self.push_list[i][j].setFont(QFont(QFont('Times', 30)))
                self.push_list[i][j].setStyleSheet(
                    "background-color: lightgrey")

                # adding action
                self.push_list[i][j].clicked.connect(
                    lambda state, i=i, j=j: self.action_called(i, j))

        if self.withHelp:
            self.strategy = Strategy(
                self.push_list, self.master.board, self.game)

        # creating label to tel the score
        self.label = QLabel(self)

        # setting geometry to the label
        self.label.setGeometry(int((self.master.size*100)/2-130),
                               (self.master.size*80)+self.master.size*20, 260, 60)

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

        # -------------------------------------------------------
        # Neuer Button zum Beenden des Spiels
        end_game = QPushButton("Beenden", self)
        # setting geometry
        end_game.setGeometry(int((self.master.size*100)/2-100), (self.master.size*80) +
                             self.master.size*20+80, 200, 50)  # (X, Y, Breite, Höhe)
        end_game.setStyleSheet('background-color: lightgrey')

        # adding action action to the reset push button
        end_game.clicked.connect(self.end_game_action)

        if self.strategy:
            self.strategy.handler()
        # ------------------------------------------------------

    def write_game_stats(self, row, column, won=False):
        player_id = self.master.current_player
        state = copy.deepcopy(self.master.board)
        game_turn = GameTurn(player_id, row, column,
                             state, self.turn_number, won)
        self.game.turns.append(game_turn.__dict__)
        self.turn_number += 1

    # Drücke Beenden Button im GameWindow / Reset bzw. Freigabe im Hauptfenster
    def end_game_action(self):
        print('Debug Beende GameWindow')  # Debug Ausgabe
        self.parent.close_game()  # rufe Methode close_game von der Elternklasse MainWindow auf
        self.close()  # schließe das Fenster

    # action called by the push buttons

    def action_called(self, row, column):
        print('Debug: Button betätigt')

        # getting button which called the action
        button = self.sender()

        # making button disabled
        button.setEnabled(False)

        # checking the turn
        if self.master.current_player == 0:
            if self.strategy:
                self.strategy.reset()
            # hellblaues Feld für Spieler 1
            button.setStyleSheet('background: lightblue')
            # setze Spielzeichen Spieler 1
            button.setText(self.game.sign_player1)
            self.master.set_field(row, column, self.game.sign_player1)

        else:

            # gelbes Feld für Spieler 2
            button.setStyleSheet('background: yellow')
            # setze Spielzeichen Spieler 2
            button.setText(self.game.sign_player2)
            self.master.set_field(row, column, self.game.sign_player2)
            if self.strategy:
                self.strategy.handler()


        # call the winner checker method
        win = self.master.is_won()

        # text
        text = ""

        self.write_game_stats(row, column, win)

        # if winner is decided
        if win == True:
            self.save_game()
            # if current chance is 0
            if self.master.current_player == 1:
                # Spieler 2 hat gewonnen
                text = "{} \n hat gewonnen".format(self.game.name_player2)
            # Spieler 1 hat gewonnen
            else:
                text = "{} \n hat gewonnen".format(self.game.name_player1)

            # disabling all the buttons
            for buttons in self.push_list:
                for push in buttons:
                    push.setEnabled(False)

        # if winner is not decided
        # and total times is 9
        elif self.master.is_draw():
            self.save_game()
            text = "Unentschieden"



        self.master.next_player()
        # setting text to the label
        self.label.setText(text)

        # ---------------------------------------------------
        # Überprüfe ob KI angewählt ist, um Zug durchzuführen
        # ---------------------------------------------------
        if self.KIenabled == True:
            print('Debug KI enabled')
            if self.master.current_player == 1:
                print('Debug KI am Zug')
                r, c = self.master.KI_set()
                self.push_list[r][c].click()
            self.master.current_player = 0
            print('Spieler: ', self.master.current_player)
        # ---------------------------------------------------

    def save_game(self):
        print(self.game.id)
        now = datetime.now()
        self.game.end_time = now.strftime("%d.%m.%Y %H:%M:%S")
        self.DB.write_record(self.game)
        self.DB.close()

    def indicatePrefferedTurns(self):
        for i in range(self.master.size):
            for j in range(self.master.size):
                if self.strategy.suggestions[i][j] == 1:
                    self.push_list[i][j].setStyleSheet(
                        "background-color: red")
