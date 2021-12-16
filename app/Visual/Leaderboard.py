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

 
class Leaderboard(QWidget):
    def __init__(self):
        super().__init__() 

        n = 5

        self.setWindowTitle("Leaderboard")
        # setting geometry
        self.setGeometry(100, 100,
                         n*100, (n+1)*2*100)  # (X,Y,Breite,Höhe)

        self.highscoreList = self.getHighscoreList()

        self.createTable(self.highscoreList)

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        # showing all the widgets
        self.show()


    def getHighscoreList(self):
        # DB instance
        self.db = DB()
        results = list(self.db.get_player_stats())
        highscoreList = [] #{'Player': "o", "Won": 1}
        for game in results:
            # print(game["name_player1"])
            player1 = True
            player2 = True
            for entry in highscoreList:
                if entry["Name"] == game["name_player1"]:
                    player1 = False
                if entry["Name"] == game["name_player2"]:
                    player2 = False
            if player1:
                highscoreList.append({"Name": game["name_player1"],"Wins": 1, "Drafts": 2, "Looses": 0})
            if player2:
                highscoreList.append({"Name": game["name_player2"],"Wins": 1, "Drafts": 2, "Looses": 0})
            
        return highscoreList

    def createTable(self, highscoreList):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['Name', 'Wins', 'Drafts', 'Looses'])
        
       # Create table
        self.tableWidget = QTableWidget()
        # self.tableWidget.setModel(model)
        self.tableWidget.setRowCount(len(highscoreList))
        self.tableWidget.setColumnCount(4)
        for i in range(len(highscoreList)):
            self.tableWidget.setItem(i,0, QTableWidgetItem(highscoreList[i]["Name"]))
            self.tableWidget.setItem(i,1, QTableWidgetItem(highscoreList[i]["Wins"]))
            self.tableWidget.setItem(i,2, QTableWidgetItem(highscoreList[i]["Drafts"]))
            self.tableWidget.setItem(i,3, QTableWidgetItem(highscoreList[i]["Looses"]))
        # self.tableWidget.move(0,0)
