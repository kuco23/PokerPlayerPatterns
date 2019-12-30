from enum import IntEnum

class OutId(IntEnum):
    RoundStart = 0
    RoundEnd = 1
    RoundId = 2
    SeatJoined = 3
    SeatButton = 4
    PlayerBlind = 5
    PlayerReceivedCard = 6
    PlayerShowCards = 7
    PlayerAction = 8
    NewTurn = 9
    PotSize = 10
    BoardShow = 11

class ActionId(IntEnum):
    FOLD = 0
    CALL = 1
    RAISE = 2
    CHECK = 3
    BET = 4
    ALLIN = 5

class TurnId(IntEnum):
    PREFLOP = 0
    FLOP = 1
    TURN = 2
    RIVER = 3
