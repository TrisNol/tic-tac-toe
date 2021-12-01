from dataclasses import dataclass

@dataclass()
class GameTurn(object):
    """ Class to store data related to a turn. """
    player_id: int
    row: int
    column: int
    turn_number: int
    latest_turn: bool
