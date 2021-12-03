from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from random import randint

from Logic import GameMaster

#-----------------    
#Spielfenster
#-----------------

class GameWindow(QWidget):
    """
    This "window" is a QWidget. If it has no parent, it
    will appear as a free-floating window as we want.
    """
    def __init__(self):
        n=windowMain.Modus
        self.master = GameMaster(n)
        super().__init__()
        layout = QVBoxLayout()
        #layout.addWidget(self.label)
        self.setLayout(layout)
        self.setWindowTitle('Game Window')
        self.setStyleSheet("background-color: grey;")
         # setting geometry
        self.setGeometry(700, 100, n*100, (n+1)*120)  #(X,Y,Breite,Höhe)

        #Methode für UI Komponenten von GameWindow
        self.UiComponents()

    def __del__(self):
        print('Game Windows destructed!')

    def UiComponents(self):

    # creating a push button list
        self.push_list = []

        # creating 2d list; Befülle die Reihe mit drei Button
        for _ in range(self.master.size):
            temp = []
            for _ in range(self.master.size):
                temp.append((QPushButton(self)))
            # adding 3 push button in single row
            self.push_list.append(temp) #befülle die 'push_list' mit 3x3 Elementen

        # x and y co-ordinate
        x = 90
        y = 90

        # traversing through push button list
        for i in range(self.master.size):
            for j in range(self.master.size):

                # setting geometry to the button
                self.push_list[i][j].setGeometry(x*i + 30,   #Startkoordinate für Auswahlfelder in X
                                                  y*j + 20,    #Startkoordinate für Auswahlfelder in Y
                                                   80, 80)    #Groeße der Felder

                # setting font to the button X or O define font and size
                self.push_list[i][j].setFont(QFont(QFont('Times', 30)))
                self.push_list[i][j].setStyleSheet("background-color: lightgrey")

                # adding action
                self.push_list[i][j].clicked.connect(lambda state, i=i, j=j: self.action_called(i,j))
                

        # creating label to tel the score
        self.label = QLabel(self)

        # setting geometry to the label
        self.label.setGeometry(30, self.master.size*100, 260, 60)

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

                #-------------------------------------------------------
        # Neuer Button zum Beenden des Spiels
        end_game = QPushButton("Beenden", self)
        # setting geometry
        end_game.setGeometry(50, self.master.size*100+70, 200, 50) #(X, Y, Breite, Höhe)
        end_game.setStyleSheet('background-color: lightgrey')

        # adding action action to the reset push button
        end_game.clicked.connect(self.end_game_action)
        #------------------------------------------------------

    def end_game_action(self):              #Drücke Beenden Button im GameWindow / Reset bzw. Freigabe im Hauptfenster
        print('Debug Beende GameWindow')    #Debug Ausgabe
        windowMain.gameWindow=None          #Reset der Variable gameWindow, damit neues Fenster bei Spielstart erzeugt wird
        # resetting values
        windowMain.selectsign1.setEnabled(True)
        windowMain.playername1.setEnabled(True)
        windowMain.selectsign2.setEnabled(True)
        windowMain.playername2.setEnabled(True) 
        windowMain.labelPlayer1.setStyleSheet('background: grey')
        windowMain.labelPlayer2.setStyleSheet('background: grey')       
        windowMain.start=False
        # making label text empty:
        windowMain.label.setText("")
        self.close()                        #schließe das Fenster

    # action called by the push buttons
    def action_called(self, row, column):
        print('Debug: Button betätigt')
        #--------------
        #Verriegelung der Buttons weil Spiel nicht gestartet ist
        #--------------
        if windowMain.start==False: 
            windowMain.label.setText('Spiel nicht gestartet!')
            return
        #-----------------
     
        # getting button which called the action
        button = self.sender()

        # making button disabled
        button.setEnabled(False)     

        # checking the turn
        if self.master.current_player == 0:
            #button.setText("X")
            windowMain.labelPlayer1.setStyleSheet('background: lightgrey')
            windowMain.labelPlayer2.setStyleSheet('background: lightgreen')
            button.setStyleSheet('background: lightblue')
            button.setText(windowMain.sign1) #setze Spielzeichen Spieler 1
            self.master.set_field(row, column, windowMain.sign1)
        else:
            windowMain.labelPlayer1.setStyleSheet('background: lightgreen')
            windowMain.labelPlayer2.setStyleSheet('background: lightgrey')
            button.setStyleSheet('background: yellow')
            button.setText(windowMain.sign2) #setze Spielzeichen Spieler 2
            self.master.set_field(row, column, windowMain.sign2)

        # call the winner checker method
        # win = self.who_wins()
        win = self.master.is_won()

        # text
        text = ""

        # if winner is decided
        if win == True:
            # if current chance is 0
            if self.master.current_player == 1:
                # Spieler 2 hat gewonnen
                #text = "{} \n {} hat gewonnen".format(self.player2,self.sign2)
                text = "{} \n hat gewonnen".format(windowMain.player2)
            # Spieler 1 hat gewonnen
            else:
                text = "{} \n hat gewonnen".format(windowMain.player1)

            # disabling all the buttons
            for buttons in self.push_list:
                for push in buttons:
                    push.setEnabled(False)

        # if winner is not decided
        # and total times is 9
        elif self.master.is_draw():
            text = "Unentschieden"

        # setting text to the label
        self.label.setText(text)
        self.master.next_player()

        #---------------------------------------------------
        #Überprüfe ob KI angewählt ist, um Zug durchzuführen
        #---------------------------------------------------
        if windowMain.KIenabled == True :
            print('Debug KI enabled')
            if self.master.current_player == 1: 
                print('Debug KI am Zug')
                r,c= self.master.KI_set()
                self.push_list[r][c].click()
            self.master.current_player=0
            print('Spieler: ',self.master.current_player)
        #---------------------------------------------------
        #print('Debug Nextplayer:' ,self.master.next_player())

#-----------------    
#Hauptfenster
#-----------------

# create a Window class
class Window(QMainWindow):
    master = None
    # constructor
    def __init__(self):
        super().__init__()

        self.master = GameMaster()
        self.start=False
        self.sign1=''
        self.sign2=''
        self.Modus=0
        self.gameWindow=None #Var zum Überprüfen, dass kein 'GameWindow' geöffnet ist
        self.KIenabled=False #Computer KI ausgeschaltet


        #Set background color
        self.setStyleSheet("background-color: grey;")

        # setting title
        self.setWindowTitle("TicTacToe")

        # setting geometry
        self.setGeometry(100, 100,
                        300, 700)  #(X,Y,Breite,Höhe)

        # calling method
        self.UiComponents()

        # showing all the widgets
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

        #-------------------------------------------------------
        # Neuer Button zum Beenden des Spiels
        exit_game = QPushButton("Exit", self)
        # setting geometry
        exit_game.setGeometry(50, 600, 200, 50) #(X, Y, Breite, Höhe)
        exit_game.setStyleSheet('background-color: red')

        # adding action action to the reset push button
        exit_game.clicked.connect(self.exit_game_action)
        #------------------------------------------------------
        
        #-------------------------------------------------------
        # Neuer Button zum Start des Spiels --> Verriegelung der Zeichenauswahl, Spielername, Freigabe des Spielfelds
        start_game = QPushButton("Start", self)
        # setting geometry
        start_game.setGeometry(50, 550, 200, 50) #(X, Y, Breite, Höhe)
        start_game.setStyleSheet('background-color: green')

        # adding action action to the reset push button
        start_game.clicked.connect(self.start_game_action)
        #start_game.clicked.connect(self.show_game_window)

        #--------------------------------------
        #ComboBox Item für Auswahl des Zeichens
        #--------------------------------------
        self.labelPlayer1=QLabel(self)
        self.labelPlayer1.setText('Spieler 1')
        self.labelPlayer1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.labelPlayer1.setFont(QFont('Arial',16))
        
        self.labelPlayer2=QLabel(self)
        self.labelPlayer2.setText('Spieler 2')
        self.labelPlayer2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.labelPlayer2.setFont(QFont('Arial',16))
        
        self.playername1=QLineEdit(self) #erstelle Texteingabe Spieler 1
        self.playername1.setText('Spieler 1') #Defaultwert 'Spieler 1' für Name
        self.playername1.setFont(QFont('Arial',12))
        self.playername1.setStyleSheet('background: lightblue')


        self.player1='Spieler 1'
        self.selectsign1=QComboBox(self) #erstelle DropDown Objekt Zeichen Spieler 1
        self.selectsign1.setFont(QFont('Arial',20))
        self.selectsign1.setStyleSheet('background: lightgrey')
        #self.selectcolour1=QComboBox(self) #erstelle DropDown Objekt Farbe Spieler 1

        #------------------------------------------------
        #Dropdown für Modus 3x3 - 4x4 - 5x5
        #------------------------------------------------
        self.labelGameMode=QLabel(self)
        self.labelGameMode.setText('Modus')
        self.labelGameMode.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.labelGameMode.setFont(QFont('Arial',16))

        self.GameMode=QComboBox(self) #erstelle DropDown Objekt Zeichen Spieler 1
        self.GameMode.setFont(QFont('Arial',16))
        self.GameMode.setStyleSheet('background: lightgrey')
        self.GameMode.addItem('')
        self.GameMode.addItem('3x3')
        self.GameMode.addItem('4x4')
        self.GameMode.addItem('5x5')

        #-------------------------------------------------

        #------------------------------------------------
        #Toggle-Button für Spielmodus 1vs1 - 1vsKI
        #------------------------------------------------
        self.KIButton=QPushButton("", self)
        # setting checkable to true
        self.KIButton.setCheckable(True)
        # setting default color of button to light-grey
        self.KIButton.setFont(QFont('Arial',18))
        self.KIButton.setText('1 vs 1')
        self.KIButton.setStyleSheet("background-color : lightgrey")
        #-------------------------------------------------

        self.playername2=QLineEdit(self) #erstelle Texteingabe Spieler 2
        self.playername2.setText('Spieler 2') #Defaultwert 'Spieler 2' für Name
        self.playername2.setFont(QFont('Arial',12))
        self.playername2.setStyleSheet('background: yellow')

        self.player2='Spieler 2'
        self.selectsign2=QComboBox(self) #erstelle DropDown Objekt Zeichen Spieler 2
        self.selectsign2.setFont(QFont('Arial',20))
        self.selectsign2.setStyleSheet('background: lightgrey')
        #self.selectcolour2=QComboBox(self) #erstelle DropDown Objekt Farbe Spieler 2

        #--------------------------------------------------------------------
        #Zeichensatz: hier wird festgelegt, welche Zeichen zur Auswahl stehen
        #und die Dropdownliste befüllt
        #------------------------------
        self.zeichensatz=['','X','O','Ø','@','!','?']
        
        for x in range(len(self.zeichensatz)):
            self.selectsign1.addItem(self.zeichensatz[x])
            self.selectsign2.addItem(self.zeichensatz[x])         
        #------------
        #Farbauswahl nicht fertig!!!
        #-----------
        self.farbensatz=['red','green','blue','yellow','grey','white']    
               
        #-----------------------
        #GUI Elemente platzieren
        #-----------------------
        self.labelPlayer1.setGeometry(30,10,100,35)
        self.playername1.setGeometry(30,45,100,35)
        self.selectsign1.setGeometry(30,80,100,35) # Koordinate, Abmaße des Dropdowns
        #self.selectcolour1.setGeometry(30,115,100,30)
        
        self.labelPlayer2.setGeometry(180,10,100,35)
        self.selectsign2.setGeometry(180,80,100,35)
        self.playername2.setGeometry(180,45,100,35)
        #self.selectcolour2.setGeometry(180,115,100,30)
        self.labelGameMode.setGeometry(100,130,100,35)
        self.GameMode.setGeometry(100,170,100,35)
        self.KIButton.setGeometry(100, 210, 100, 35)
        #------------------------------------------
        
        #---------------------------------
        #Aufruf Methode bei Zeichenwechsel
        #---------------------------------
        self.selectsign1.activated[str].connect(self.sign_changed1)
        self.selectsign2.activated[str].connect(self.sign_changed2)
        self.playername1.textChanged.connect(self.textchangedPlayer1)
        self.playername2.textChanged.connect(self.textchangedPlayer2)
        self.GameMode.activated[str].connect(self.GameMode_changed)
        self.KIButton.clicked.connect(self.changeKI)
        #--------------------------------


#----------------
#Methoden für GUI
#----------------
    def changeKI(self):
        if self.KIButton.isChecked():
            self.KIButton.setStyleSheet('background-color: lightblue')
            self.KIButton.setText('1 vs KI')
            self.playername2.setText('KI')
            self.playername2.setEnabled(False)
            self.selectsign2.setEnabled(False)
            self.selectsign2.addItem('©') #Sonderzeichen für KI Gegner
            self.selectsign2.setCurrentText('©')
            self.sign2='©'
            self.KIenabled=True
            print('Debug 1vsKI', self.KIenabled)
        else:
            self.KIButton.setStyleSheet('background-color: lightgrey')
            self.KIButton.setText('1 vs 1')
            self.selectsign2.removeItem(7)
            self.selectsign2.setEnabled(True)
            self.selectsign2.setCurrentIndex(0)
            self.playername2.setText('Player 2')
            self.playername2.setEnabled(True)
            self.sign2=""
            self.KIenabled=False


            print('Debug 1vs1', self.KIenabled)

    def GameMode_changed(self,s):
        print('GameMode changed to: ',s )
        if s =='3x3':
            self.Modus=3
        elif s == '4x4':
            self.Modus=4
        elif s == '5x5':
            self.Modus=5
        else:
            self.Modus=0       
        
    def show_game_window(self, checked):
        print('Debug Game Window')
        if self.gameWindow is None:
            self.gameWindow = GameWindow()
        self.gameWindow.show()
    
    def textchangedPlayer1(self,s):
        self.player1=s
        
    def textchangedPlayer2(self,s):
        self.player2=s  
    
    def sign_changed1(self,s):
        self.sign1=s
        zeichenTemp=self.zeichensatz            
        print('Auswahl geaendert Spieler 1!',s)
        
    def sign_changed2(self,s):
        self.sign2=s
        zeichenTemp=self.zeichensatz            
        print('Auswahl geaendert Spieler 2!',s)    
                 
    def start_game_action(self):
        print('Debug Button Start')
        #---------------------------------
        #Plausibiltät-Check vor Spielstart --> sind alle erforderlichen Einstellungen gewählt
        #--------------------------------
        if self.sign1 =='':
            self.label.setFont(QFont('Arial',10))
            self.label.setStyleSheet('background: red')
            self.label.setText('Fehler Spieler 1: kein Zeichen ausgewählt')
            return
        elif self.sign2 =='':
            self.label.setStyleSheet('background: red')
            self.label.setFont(QFont('Arial',10))
            self.label.setText('Fehler Spieler 2: kein Zeichen ausgewählt')
            return
        elif self.Modus==0:
            self.label.setStyleSheet('background: red')
            self.label.setFont(QFont('Arial',10))
            self.label.setText('Fehler Modus: kein Spielmodus ausgewählt')
            return
        #------------------------------------------------------------------------------------------
        self.selectsign1.setEnabled(False)
        self.playername1.setEnabled(False)
        self.selectsign2.setEnabled(False)
        self.playername2.setEnabled(False)
        self.start=True
        self.labelPlayer1.setStyleSheet('background: lightgreen') #Highlighte Spieler 1 bei Spielstart
        self.label.setStyleSheet('background: white')
        self.label.setFont(QFont('Arial',16))
        self.label.setText('Spiel gestartet')
        self.show_game_window(None)
        
               
    def exit_game_action(self):
        print('Test')
        sys.exit() #Beende Applikation
        

    # action called by the push buttons
    def action_called(self, row, column):
        
        #--------------
        #Verriegelung der Buttons weil Spiel nicht gestartet ist
        #--------------
        if self.start==False: 
            self.label.setText('Spiel nicht gestartet!')
            return
        #-----------------

        # getting button which called the action
        button = self.sender()

        # making button disabled
        button.setEnabled(False)
       
        # checking the turn
        if self.master.current_player == 0:
            #button.setText("X")
            self.labelPlayer1.setStyleSheet('background: lightgrey')
            self.labelPlayer2.setStyleSheet('background: lightgreen')
            button.setText(self.sign1) #setze Spielzeichen Spieler 1
            self.master.set_field(row, column, self.sign1)
        else:
            self.labelPlayer1.setStyleSheet('background: lightgreen')
            self.labelPlayer2.setStyleSheet('background: lightgrey')
            button.setText(self.sign2) #setze Spielzeichen Spieler 2
            self.master.set_field(row, column, self.sign2)

        # text
        text = ""

        # if winner is decided
        if win == True:
            # if current chance is 0
            if self.master.current_player == 1:
                # Spieler 2 hat gewonnen
                #text = "{} \n {} hat gewonnen".format(self.player2,self.sign2)
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
        elif self.master.is_draw():
            text = "Unentschieden"

        # setting text to the label
        self.label.setText(text)
        self.master.next_player()


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
windowMain = Window()

# start the app
sys.exit(App.exec())
