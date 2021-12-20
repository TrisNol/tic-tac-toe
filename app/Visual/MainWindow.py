from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from random import randint

from Logic import GameMaster
from Visual import Gamewindow, Leaderboard
from Analysis.AnalysisWindow import AnalysisWindow
from Model.Game import Game
from utils.DB import DB
from datetime import datetime

# ----------------------
# create a Window class
# ----------------------


class Window(QMainWindow):
    master = None
    # constructor

    def __init__(self):
        super().__init__()
        #self.DB=DB()
        self.game=Game() #erstelle Objekt game aus Klasse Game: Spielername, Feldgröße, Zeichen
        self.start=False
        self.gameWindow=None #Var zum Überprüfen, dass kein 'GameWindow' geöffnet ist
        self.KIenabled=False #Computer KI ausgeschaltet
       #self.initialize_game_class()
        self.leaderboard = None
        #Set background color
        self.setStyleSheet("background-color: grey;")
        # Enable help
        self.helper = None
        # setting title
        self.setWindowTitle("TicTacToe")

        # setting geometry
        self.setGeometry(100, 100,
                         300, 800)  # (X,Y,Breite,Höhe)

        # calling method
        self.UiComponents()

        self.show()

    # method for components
    def UiComponents(self):

        # creating label to tel the score
        self.label = QLabel(self)

        # setting geometry to the label
        self.label.setGeometry(20, 450, 260, 60)

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

        # ------------------------------------
        # Neuer Button zum Beenden des Spiels
        # ------------------------------------
        exit_game = QPushButton("Exit", self)
        # setting geometry
        exit_game.setGeometry(50, 600, 200, 50)  # (X, Y, Breite, Höhe)
        exit_game.setStyleSheet('background-color: red')
        # adding action action to the reset push button
        exit_game.clicked.connect(self.exit_game_action)

        # -------------------------------------------------------
        # Neuer Button zum Start des Spiels --> Verriegelung der Zeichenauswahl, Spielername, Freigabe des Spielfelds
        # ------------------------------------
        self.start_game = QPushButton("Start", self)
        # setting geometry
        self.start_game.setGeometry(50, 550, 200, 50)  # (X, Y, Breite, Höhe)
        self.start_game.setStyleSheet('background-color: green')
        # adding action action to the reset push button
        self.start_game.clicked.connect(self.start_game_action)

        self.open_leaderboard = QPushButton("Leaderboard", self)
        self.open_leaderboard.setGeometry(50, 650, 200, 50) #(X, Y, Breite, Höhe)
        self.open_leaderboard.setStyleSheet('background-color: yellow')
        self.open_leaderboard.clicked.connect(self.show_leaderboard)

        #--------------------------------------
        #ComboBox Item für Auswahl des Zeichens
        #--------------------------------------
        self.labelPlayer1=QLabel(self)
        # Button to open the Analysis/Repoting Window
        self.show_analysis = QPushButton("Analysis", self)
        self.show_analysis.setGeometry(
            50, 700, 200, 50)  # (X, Y, Breite, Höhe)
        self.show_analysis.setStyleSheet('background-color: blue')
        # adding action action to the reset push button
        self.show_analysis.clicked.connect(self.show_analysis_action)

        # --------------------------------------
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
        self.playername1.setFont(QFont('Arial', 12))
        self.playername1.setStyleSheet('background: lightblue')

        self.game.name_player1 = 'Spieler 1'
        # erstelle DropDown Objekt Zeichen Spieler 1
        self.selectsign1 = QComboBox(self)
        self.selectsign1.setFont(QFont('Arial', 20))
        self.selectsign1.setStyleSheet('background: lightgrey')
        # ------------------------------------------------
        # Dropdown für Modus 3x3 - 4x4 - 5x5
        # ------------------------------------------------
        self.labelGameMode = QLabel(self)
        self.labelGameMode.setText('Modus')
        self.labelGameMode.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.labelGameMode.setFont(QFont('Arial', 16))

        # erstelle DropDown Objekt Zeichen Spieler 1
        self.GameMode = QComboBox(self)
        self.GameMode.setFont(QFont('Arial', 16))
        self.GameMode.setStyleSheet('background: lightgrey')
        self.GameMode.addItem('')
        self.GameMode.addItem('3x3')
        self.GameMode.addItem('4x4')
        self.GameMode.addItem('5x5')
        self.GameMode.currentTextChanged.connect(self.conditional_render_player_help)
        # ------------------------------------------------
        # Toggle-Button für Spielmodus 1vs1 - 1vsKI
        # ------------------------------------------------
        self.KIButton = QPushButton("", self)
        # setting checkable to true
        self.KIButton.setCheckable(True)
        # setting default color of button to light-grey
        self.KIButton.setFont(QFont('Arial', 18))
        self.KIButton.setText('1 vs 1')
        self.KIButton.setStyleSheet("background-color : lightgrey")
        # ------------------------------------------------
        # Checkbox to enable player advice
        # ------------------------------------------------
        self.helperCheckBox = QCheckBox(self)
        self.helperCheckBox.setText("Player 1 helper")
        self.helperCheckBox.setToolTip("If this checkbox is checked, Player 1 will get hints to play succesful.\n Only available in the 3x3 game mode")



        # -------------------------------------------------
        self.playername2 = QLineEdit(self)  # erstelle Texteingabe Spieler 2
        # Defaultwert 'Spieler 2' für Name
        self.playername2.setText('Spieler 2')
        self.playername2.setFont(QFont('Arial', 12))
        self.playername2.setStyleSheet('background: yellow')

        self.game.name_player2 = 'Spieler 2'
        # erstelle DropDown Objekt Zeichen Spieler 2
        self.selectsign2 = QComboBox(self)
        self.selectsign2.setFont(QFont('Arial', 20))
        self.selectsign2.setStyleSheet('background: lightgrey')

        # --------------------------------------------------------------------
        # Zeichensatz: hier wird festgelegt, welche Zeichen zur Auswahl stehen
        # und die Dropdownliste befüllt
        # ------------------------------
        self.zeichensatz = ['', 'X', 'O', 'Ø', '@', '!', '?']

        for x in range(len(self.zeichensatz)):
            self.selectsign1.addItem(self.zeichensatz[x])
            self.selectsign2.addItem(self.zeichensatz[x])
        # -----------------------
        # GUI Elemente platzieren
        # -----------------------
        self.labelPlayer1.setGeometry(30, 10, 100, 35)
        self.playername1.setGeometry(30, 45, 100, 35)
        # Koordinate, Abmaße des Dropdowns
        self.selectsign1.setGeometry(30, 80, 100, 35)

        self.labelPlayer2.setGeometry(180, 10, 100, 35)
        self.selectsign2.setGeometry(180, 80, 100, 35)
        self.playername2.setGeometry(180, 45, 100, 35)

        self.labelGameMode.setGeometry(100, 130, 100, 35)
        self.GameMode.setGeometry(100, 170, 100, 35)
        self.KIButton.setGeometry(100, 210, 100, 35)
        self.helperCheckBox.setGeometry(70, 260, 200,35)

        # ---------------------------------
        # Aufruf Methode bei Zeichenwechsel
        # ---------------------------------
        self.selectsign1.activated[str].connect(self.sign_changed1)
        # self.selectsign1.activated[str].connect(self.game.sign_player1=)
        self.selectsign2.activated[str].connect(self.sign_changed2)
        self.playername1.textChanged.connect(self.textchangedPlayer1)
        self.playername2.textChanged.connect(self.textchangedPlayer2)
        self.GameMode.activated[str].connect(self.GameMode_changed)
        self.KIButton.clicked.connect(self.changeKI)
        # --------------------------------
# ----------------
# Methoden für GUI
# ----------------

    def changeKI(self):
        if self.KIButton.isChecked():
            self.KIButton.setStyleSheet('background-color: lightblue')
            self.KIButton.setText('1 vs KI')
            self.playername2.setText('KI')
            self.playername2.setEnabled(False)
            self.selectsign2.setEnabled(False)
            self.selectsign2.addItem('©')  # Sonderzeichen für KI Gegner
            self.selectsign2.setCurrentText('©')
            self.game.sign_player2 = '©'
            self.KIenabled = True
            print('Debug 1vsKI', self.KIenabled)
        else:
            self.KIButton.setStyleSheet('background-color: lightgrey')
            self.KIButton.setText('1 vs 1')
            self.selectsign2.removeItem(7)
            self.selectsign2.setEnabled(True)
            self.selectsign2.setCurrentIndex(0)
            self.playername2.setText('Player 2')
            self.playername2.setEnabled(True)
            self.game.sign_player2 = ""
            self.KIenabled = False

            print('Debug 1vs1', self.KIenabled)

    def GameMode_changed(self, s):  # Auswahl der Spielfeldgröße 3x3, 4x4, 5x5
        print('GameMode changed to: ', s)
        if s == '3x3':
            self.game.size = 3
        elif s == '4x4':
            self.game.size = 4
        elif s == '5x5':
            self.game.size = 5
        else:
            self.game.size = 0

    def close_game(self):                   #Methode welche das Gamewindow bei Verlassen ausführt, um die Eingabefelder freizugeben
        self.gameWindow=None #lösche Objekt gameWindow, um es bei erneutem Start neu zu erstellen
         # resetting values
        sign1Temp=self.game.sign_player1
        sign2Temp=self.game.sign_player2
        name1Temp=self.game.name_player1
        name2Temp=self.game.name_player2
        sizeTemp=self.game.size
        #---------------------
        self.game = Game()
        #---------------------
        self.game.sign_player1=sign1Temp
        self.game.sign_player2=sign2Temp
        self.game.name_player1=name1Temp
        self.game.name_player2=name2Temp
        self.game.size=sizeTemp
        #-------------------        
        self.selectsign1.setEnabled(True)
        self.selectsign2.setEnabled(True)
        self.playername1.setEnabled(True)
        self.selectsign2.setEnabled(True)
        self.playername2.setEnabled(True)
        self.GameMode.setEnabled(True)
        self.KIButton.setEnabled(True)
        self.start_game.setEnabled(True)
        self.labelPlayer1.setStyleSheet('background: grey')
        self.labelPlayer2.setStyleSheet('background: grey')
        self.label.setText('Spiel beendet')

    # Erstellung des Child-Objekts 'GameWindow' in welchem gespielt wird
    def show_game_window(self):
        print('Debug Game Window')
        self.initialize_game_class()
        if self.gameWindow is None:
            print(self.game)
            # erstelle das Objekt GameWindow mit Übergabe der Spielbrettgröße und einer Instanz der Klasse Window
            self.gameWindow = Gamewindow.GameWindow(
                self.game, self, self.KIenabled, self.helperCheckBox.isChecked())
            # self.gameWindow = Gamewindow.GameWindow(self.game.size,self.game.sign_player1,self.game.sign_player2,self.game.name_player1,self.game.name_player2,self,self.KIenabled) #erstelle das Objekt GameWindow mit Übergabe der Spielbrettgröße und einer Instanz der Klasse Window
        self.gameWindow.show()

    def show_leaderboard(self):    #Erstellung des Child-Objekts 'GameWindow' in welchem gespielt wird
        print('Debug Leaderboard Window')
        # self.initialize_game_class()
        if self.leaderboard is None:
            # print(self.game)
            self.leaderboard = Leaderboard.Leaderboard() #erstelle das Objekt GameWindow mit Übergabe der Spielbrettgröße und einer Instanz der Klasse Window
            #self.gameWindow = Gamewindow.GameWindow(self.game.size,self.game.sign_player1,self.game.sign_player2,self.game.name_player1,self.game.name_player2,self,self.KIenabled) #erstelle das Objekt GameWindow mit Übergabe der Spielbrettgröße und einer Instanz der Klasse Window
        self.leaderboard.show()

    def show_analysis_action(self):
        print('Debug Game Window')
        self.analysis_window = AnalysisWindow(self)
        self.analysis_window.show()
    
    def textchangedPlayer1(self,s):         #setze Spielernamen 1 bei Änderung
        self.game.name_player1=s
        
    def textchangedPlayer2(self,s):         #setze Spielernamen 2 bei Änderung
        self.game.name_player2=s  
    
    def sign_changed1(self,s):              #setze Spielerzeichen 1 bei Änderung
        self.game.sign_player1=s
        zeichenTemp=self.zeichensatz            
        print('Auswahl geaendert Spieler 1!',s)
        
    def sign_changed2(self,s):              #setze Spielerzeichen 2 bei Änderung
        self.game.sign_player2=s
        zeichenTemp=self.zeichensatz            
        print('Auswahl geaendert Spieler 2!',s)    
                 
    def start_game_action(self):            #Betätigung des grünen 'Start'-Buttons
        print('Debug Button Start')
        # ---------------------------------
        # Plausibiltät-Check vor Spielstart --> sind alle erforderlichen Einstellungen gewählt
        # --------------------------------
        if self.game.sign_player1 == '':
            self.label.setFont(QFont('Arial', 10))
            self.label.setStyleSheet('background: red')
            self.label.setText('Fehler Spieler 1: kein Zeichen ausgewählt')
            return
        elif self.game.sign_player2 == '':
            self.label.setStyleSheet('background: red')
            self.label.setFont(QFont('Arial', 10))
            self.label.setText('Fehler Spieler 2: kein Zeichen ausgewählt')
            return
        elif self.game.size == 0:
            self.label.setStyleSheet('background: red')
            self.label.setFont(QFont('Arial', 10))
            self.label.setText('Fehler Modus: kein Spielmodus ausgewählt')
            return
        # ------------------------------------------------------------------------------------------
        self.selectsign1.setEnabled(False)
        self.playername1.setEnabled(False)
        self.selectsign2.setEnabled(False)
        self.playername2.setEnabled(False)
        self.GameMode.setEnabled(False)
        self.KIButton.setEnabled(False)
        self.start_game.setEnabled(False)
        self.start = True
        self.label.setStyleSheet('background: white')
        self.label.setFont(QFont('Arial', 16))
        self.label.setText('Spiel gestartet')
        self.show_game_window()

    def exit_game_action(self):  # Betätigung des roten 'Exit'-Buttons
        print('Test')
        sys.exit()  # Beende Applikation

    def initialize_game_class(self):
        self.DB = DB()
        self.game.id = self.DB.get_amount_off_documents()
        now = datetime.now()
        self.game.start_time = now.strftime("%d.%m.%Y %H:%M:%S")

    def conditional_render_player_help(self, selectedMode):
        print("CHECKBOX", selectedMode)
        if selectedMode == '3x3':
            self.helperCheckBox.show()
        else:
            self.helperCheckBox.setChecked(False)
            self.helperCheckBox.hide()

