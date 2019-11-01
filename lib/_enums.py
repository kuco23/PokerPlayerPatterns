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
