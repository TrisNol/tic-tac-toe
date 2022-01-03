from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from random import randint

from logic import GameMaster
from model.gameturn import GameTurn
from datetime import datetime
from ai.strategy import Strategy
from ai.ai import AI
from utils.db import DB
from ai.minimax import MiniMax

import copy

class GameWindow(QWidget):
    """This "window" is a QWidget. If it has no parent, it will appear as a free-floating window as we want"""

    ai: AI = None
    def __init__(self,game, parent, ai_enabled, ai, helper):
        super().__init__()
        self.DB = DB()
        self.parent = parent
        self.game = game        
        self.ai_enabled = ai_enabled
        self.ai = ai

        print('passed down AI: '+ str(self.ai))
        print(self.game.name_player2)

        self.master = GameMaster(self.game.size)
        self.turn_number = 0

        self.with_help = helper
        self.strategy = None

        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setWindowTitle('Game Window')
        self.setStyleSheet("background-color: grey;")
        # setting geometry
        self.setGeometry(700, 100, self.game.size*100,
                         (self.game.size+1)*120)  

        self.ui_components()

    def ui_components(self):
        """Creates the UI components for the game on the window object"""
        self.push_list = []

        for _ in range(self.master.size):
            temp = []
            for _ in range(self.master.size):
                temp.append((QPushButton(self)))
            self.push_list.append(temp)

        x = 90
        y = 90

        for i in range(self.master.size):
            for j in range(self.master.size):
                self.push_list[i][j].setGeometry(x*i + self.master.size*6,
                                                 y*j + 20,  
                                                 80, 80) 

                self.push_list[i][j].setFont(QFont(QFont('Times', 30)))
                self.push_list[i][j].setStyleSheet(
                    "background-color: lightgrey")

                
                self.push_list[i][j].clicked.connect(
                    lambda state, i=i, j=j: self.action_called(i, j))

        if self.with_help:
            self.strategy = Strategy(
                self.push_list, self.master.board, self.game)

        self.label = QLabel(self)

        self.label.setGeometry(int((self.master.size*100)/2-130),
                               (self.master.size*80)+self.master.size*20, 260, 60)

        self.label.setStyleSheet("QLabel"
                                 "{"
                                 "border : 3px solid black;"
                                 "background : white;"
                                 "}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(QFont('Times', 15))

        end_game = QPushButton("Finish", self)
        end_game.setGeometry(int((self.master.size*100)/2-100), (self.master.size*80) +
                             self.master.size*20+80, 200, 50) 
        end_game.setStyleSheet('background-color: lightgrey')
        end_game.clicked.connect(self.end_game_action)

        if self.strategy:
            self.strategy.handler()

    def write_game_stats(self, row, column, won=False):
        """Writes games stats to the corresponding variables"""
        player_id = self.master.current_player
        state = copy.deepcopy(self.master.board)
        game_turn = GameTurn(player_id, row, column,
                             state, self.turn_number, won)
        self.game.turns.append(game_turn.__dict__)
        self.turn_number += 1

    def end_game_action(self):
        """Closes the game object"""
        self.parent.close_game()  
        self.close()  

    def action_called(self, row, column):
        """Checks if somebody has one"""
        button = self.sender()
        button.setEnabled(False)

        if self.master.current_player == 0:
            if self.strategy:
                self.strategy.reset()
            button.setStyleSheet('background: lightblue')
            button.setText(self.game.sign_player1)
            self.master.set_field(row, column, self.game.sign_player1)
        else:
            button.setStyleSheet('background: yellow')
            button.setText(self.game.sign_player2)
            self.master.set_field(row, column, self.game.sign_player2)
            if self.strategy:
                self.strategy.handler()

        win = self.master.is_won()
        text = ""
        self.write_game_stats(row, column, win)

        # if winner is decided
        if win == True:
            self.save_game()
            # if current chance is 0
            if self.master.current_player == 1:
                text = "{} \n has won".format(self.game.name_player2)
           
            else:
                text = "{} \n has won".format(self.game.name_player1)

            # disabling all the buttons
            for buttons in self.push_list:
                for push in buttons:
                    push.setEnabled(False)

        # if winner is not decided
        # and total times is 9
        elif self.master.is_draw():
            self.save_game()
            text = "draw"

        self.master.next_player()
        # setting text to the label
        self.label.setText(text)
        if self.ai_enabled == True and not self.master.is_won():
            if self.master.current_player == 1: 
                board = self.ai.translate_player_symbols(self.master.board, self.game.sign_player1, self.game.sign_player2)
                row, column = self.ai.recommend_move(board, 1)
                self.push_list[row][column].click()
            self.master.current_player=0

    def save_game(self):
        """Stores the data of the game in the database"""
        print(self.game.id)
        now = datetime.now()
        self.game.end_time = now.strftime("%d.%m.%Y %H:%M:%S")
        self.DB.write_record(self.game)
        self.DB.close()

    def indicate_preffered_turns(self):
        """Highlights visualy the recommended turn"""
        for i in range(self.master.size):
            for j in range(self.master.size):
                if self.helper.suggestions[i][j] == 1:
                    self.push_list[i][j].setStyleSheet(
                        "background-color: red")
