import sys
sys.path.append("..")  #

from AI.AI import AI
from utils.DB import DB
from Analysis.Analysis import Analysis
import pandas as pd


class Statistic(AI):
    """Implementation of the AI-Class based on the previously played games recorded on the DB.
    """

    def __init__(self):
        self.analysis = Analysis()

    def encode_field_to_string(self, field: list) -> str:
        """Helper-Method to convert the field to a string to utizilize the panda group-by function.

        Parameters:
            field (list): Nested list representing the Tic-Tac-Toe field

        Returns:
            str: Field represented in a string(columns: space-separated, rows: \\n separated)
        
        """
        return '\n'.join([' '.join([str(z) if z != "" else "-1" for z in y]) for y in field])

    def decode_field_to_list(self, field: str) -> list:
        """Helper-Method to convert the string representing the field back to a nested list.
        
        Parameters:
            field (str): String-representation of the Tic-Tac-Toe field

        Returns:
            list: Nested-list representation of the Tic-Tac-Toe field

        """
        return [[z for z in y.split(" ")] for y in field.split('\n')]

    def transform_turns(self, df):
        """Helper-Method to convert the field-states in the provided dataframe into the 0 and 1 representation.
        
        Parameters:
            df (DataFrame): DataFrame containing the DB entries of the games played so far

        Returns:
            DataFrame: Converted frame

        """
        for index, row in df.iterrows():
            symbol_one = row['sign_player1']
            symbol_two = row['sign_player2']

            for i in range(len(row.turns)):
                row.turns[i]['state'] = self.translate_player_symbols(
                    row.turns[i]['state'], symbol_one, symbol_two)
            df[index] = row
            # print(df[index])
        return df

    def recommendMove(self, field: list, player: int) -> tuple:
        frame = self.analysis.get_frame()
        frame = self.transform_turns(frame)

        moves = []  # {'current': [[]], 'next':[[]], 'won': True || False}
        for index, row in frame.iterrows():
            for i in range(len(row.turns)):
                # current field state found
                if row.turns[i]['state'] == field:
                    # increment index to fetch the next move executed by the current player
                    i = i+1
                    # fetch if this game has been won by the current player
                    last = row.turns[-1]
                    moves.append(
                        {'current': field, 'next': row.turns[i]['state'], 'won': last['player_id'] == player and last['latest_turn'] == True})

        df_recom = pd.DataFrame(moves)

        # Pandas cannot group by (nested) lists so it is transformed into a string-represenatation before the groups are built
        # 0 --> player 1, 1 --> player 2, -1 --> empty cell
        df_recom['current'] = df_recom['current'].apply(
            self.encode_field_to_string)
        df_recom['next'] = df_recom['next'].apply(self.encode_field_to_string)

        # Output: Possible next moves by descending count of won games following this move
        groups = df_recom.groupby("next").agg(
            {'current': 'first', 'next': 'first', 'won': 'sum'}).sort_values('won', ascending=False)
        # reset the string to the nested list
        groups['current'] = groups['current'].apply(self.decode_field_to_list)
        groups['next'] = groups['next'].apply(self.decode_field_to_list)

        currentState = groups.current[0]
        nextState = groups.next[0]

        # find difference in current and next state to calculate row and column
        row = -1
        column = -1
        for i in range(len(currentState)):
            for j in range(len(currentState[i])):
                if currentState[i][j] != nextState[i][j]:
                    row = i
                    column = j
        if row == -1 or column == -1:
            raise Exception('No result')

        print(f"Recommendation --> row: {row}, column: {column}")
        return (row, column)


if __name__ == '__main__':
    temp = [[0, 1, '', '', ''], [0, 1, '', '', ''], [0, 1, '', '', ''], [0, '', '', '', ''], ['', '', '', '', '']]
    stat = Statistic()
    (row, column) = stat.recommendMove(temp, 0)
    print(row, column)
