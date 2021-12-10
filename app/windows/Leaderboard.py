import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QToolTip, QMessageBox, QLabel,QTableWidget,QTableWidgetItem, QVBoxLayout
from utils.DB import DB
from pprint import pprint

 
class Leaderboard(QMainWindow):
    def __init__(self):
        super().__init__() 

        n = 5

        self.setWindowTitle("Leaderboard")
        # setting geometry
        self.setGeometry(100, 100,
                         n*100, (n+1)*2*100)  # (X,Y,Breite,Höhe)

        # DB instance
        self.db = DB()
        results = list(self.db.get_player_stats())
        # pprint(list(results))
        print(results[4]["winner"])

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        # showing all the widgets
        self.show()


    def createTable(self):
       # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(4)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0,0, QTableWidgetItem("Cell (1,1)"))
        self.tableWidget.setItem(0,1, QTableWidgetItem("Cell (1,2)"))
        self.tableWidget.setItem(1,0, QTableWidgetItem("Cell (2,1)"))
        self.tableWidget.setItem(1,1, QTableWidgetItem("Cell (2,2)"))
        self.tableWidget.setItem(2,0, QTableWidgetItem("Cell (3,1)"))
        self.tableWidget.setItem(2,1, QTableWidgetItem("Cell (3,2)"))
        self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
        self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0,0)
