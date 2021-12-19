from AI.AI import AI
from random import randint

class Random(AI):

    def recommendMove(self, field: list, player: int) -> tuple:
        # boardlist=[]
        # Generate random row and column indexes and check if the cell is free
        row = -1
        column = -1
        # TODO optimize loop?
        for x in range(100): 
            row=randint(0,len(field)-1)
            column=randint(0,len(field)-1)
            # empty cell found
            if field[row][column]=='':
                print('Freies Feld bei: ', row, column )
                print('benoetigte Iterationen: ', x)
                break

        # TODO check what this is for
        # #Erstelle eine eindimensionale Liste aus der Boardliste
        # for element in field:
        #     if type(element) is list:
        #         for item in element:
        #             boardlist.append(item)
        #     else:
        #         boardlist.append(element)
        #-------------------------------------                
        #print('boardlist: ', boardlist)
        #print(row, column)

        return (row, column)