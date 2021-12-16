import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel,QTableWidget,QTableWidgetItem, QVBoxLayout
from utils.DB import DB
from pprint import pprint
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import pandas as pd

 
class Leaderboard(QTableWidget):
    def __init__(self):
        super().__init__() 

        n = 5

        self.setWindowTitle("Leaderboard")
        # setting geometry
        self.setGeometry(100, 100,
                         n*100, (n+1)*2*100)  # (X,Y,Breite,Höhe)

        self.highscoreList = self.getHighscoreList()
        print(self.highscoreList)
        self.createTable(self.highscoreList)

        # Add box layout, add table to box layout and add box layout to widget
        # self.layout = QVBoxLayout()
        # self.layout.addWidget(self.tableWidget)
        # self.setLayout(self.layout)
        # showing all the widgets
        self.show()


    def getHighscoreList(self):
        # DB instance
        self.db = DB()
        results = list(self.db.get_player_stats())
        highscoreList = {}
        for game in results:
            player1 = False
            player2 = False
            isDraw = False
            if game["turns"][-1]["latest_turn"]:
                id = game["turns"][-1]["player_id"]
                if id == 0:
                    player1 = True
                else:
                    player2 = True
            else:
                isDraw = True

            if game["name_player1"] in highscoreList:
                highscoreList[game["name_player1"]]["Wins"] += int(player1)
                highscoreList[game["name_player1"]]["Draws"] += int(isDraw)
                highscoreList[game["name_player1"]]["Looses"] += int(player2)
            else:    
                highscoreList[game["name_player1"]] =  {"Wins": int(player1), "Draws": int(isDraw), "Looses": int(player2)}

            if game["name_player2"] in highscoreList:
                highscoreList[game["name_player2"]]["Wins"] += int(player2)
                highscoreList[game["name_player2"]]["Draws"] += int(isDraw)
                highscoreList[game["name_player2"]]["Looses"] += int(player1)
            else:    
                highscoreList[game["name_player2"]] =  {"Wins": int(player2), "Draws": int(isDraw), "Looses": int(player1)}

            
            
        return highscoreList

     

    def createTable(self, highscoreList):
        # model = QStandardItemModel()
        
        
       # Create table
        # self.tableWidget = QTableWidget()
        # self.tableWidget.setModel(model)
        self.setRowCount(len(highscoreList))
        self.setColumnCount(4)
        names = list(highscoreList)
        self.setItem(0,0, QTableWidgetItem("Name"))
        for i in range(len(names)):
            name = names[i]
            self.setItem(i,0, QTableWidgetItem(name))
            self.setItem(i,1, QTableWidgetItem(str(highscoreList[name]["Wins"])))
            # print(highscoreList[name]["Wins"])
            self.setItem(i,2, QTableWidgetItem(str(highscoreList[name]["Draws"])))
            self.setItem(i,3, QTableWidgetItem(str(highscoreList[name]["Looses"])))
        self.setHorizontalHeaderLabels(['Name', 'Wins', 'Draws', 'Looses'])
        # self.tableWidget.move(0,0)
