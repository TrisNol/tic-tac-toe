import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from pprint import pprint
import pandas as pd

from utils.db import DB

class Scoreboard(QTableWidget):
    def __init__(self):
        super().__init__() 

        n = 5
        self.setWindowTitle("Scoreboard")
        self.setGeometry(100, 100,
                         n*100, (n+1)*2*100) 

        self.highscore_list = self.get_highscore_list()
        self.createTable(self.highscore_list)
        self.show()

    def get_highscore_list(self):
        """Calculates and returns the Scores based on the games stored on the database"""
        self.db = DB()
        results = list(self.db.get_player_stats())
        highscore_list = {}
        for game in results:
            player1 = False
            player2 = False
            is_draw = False
            if game["turns"][-1]["latest_turn"]:
                id = game["turns"][-1]["player_id"]
                if id == 0:
                    player1 = True
                else:
                    player2 = True
            else:
                is_draw = True

            if game["name_player1"] in highscore_list:
                highscore_list[game["name_player1"]]["Wins"] += int(player1)
                highscore_list[game["name_player1"]]["Draws"] += int(is_draw)
                highscore_list[game["name_player1"]]["Looses"] += int(player2)
            else:    
                highscore_list[game["name_player1"]] =  {"Wins": int(player1), "Draws": int(is_draw), "Looses": int(player2)}

            if game["name_player2"] in highscore_list:
                highscore_list[game["name_player2"]]["Wins"] += int(player2)
                highscore_list[game["name_player2"]]["Draws"] += int(is_draw)
                highscore_list[game["name_player2"]]["Looses"] += int(player1)
            else:    
                highscore_list[game["name_player2"]] =  {"Wins": int(player2), "Draws": int(is_draw), "Looses": int(player1)}
        return highscore_list

    def createTable(self, highscore_list):
        """Creates the UI elements (Table) and adds the data from the database"""
        self.setRowCount(len(highscore_list))
        self.setColumnCount(4)
        names = list(highscore_list)
        self.setItem(0,0, QTableWidgetItem("Name"))
        for i in range(len(names)):
            name = names[i]
            self.setItem(i,0, QTableWidgetItem(name))
            self.setItem(i,1, QTableWidgetItem(str(highscore_list[name]["Wins"])))
            self.setItem(i,2, QTableWidgetItem(str(highscore_list[name]["Draws"])))
            self.setItem(i,3, QTableWidgetItem(str(highscore_list[name]["Looses"])))
        self.setHorizontalHeaderLabels(['Name', 'Wins', 'Draws', 'Looses'])