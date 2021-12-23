from abc import ABC


class IController(ABC):
    """Abstract class to provide the functionality to manage the Tic-Tac-Toe board and host the primary game-logic.
    """
    current_player = 0
    times = 0
    size = 0

    labels = []
    board = []

    def build_board(self, n: int) -> list:
        """Builds a nxn-sized list to hold the Tic-Tac-Toe fields.

        Parameters:
            n (int): Size of the field.

        Returns:
            list: 2-dimensional list to be used as the Tic-Tac-Toe field
        """
        pass

    def is_won(self) -> bool:
        """Determines if the game is won.

        Returns:
            bool: Status if game is won.
        """
        pass

    def set_field(self, row: int, column: int, label: str) -> None:
        """Sets a field of the board with a label

        Parameters:
            row (int): Index of the row where the labed shall be placed.
            column (int): Index of the column where the labed shall be placed.
            label (str): Label to be placed.
        """
        pass

    def next_player(self):
        """Switch to the next player."""
        pass

    def is_draw(self) -> bool:
        """Calculates if a draw has been reached.
        
        Returns:
            bool: Is it a draw?
        """
        pass
