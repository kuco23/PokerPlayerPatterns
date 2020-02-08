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

class Suit(IntEnum):
    HEARTS = 0
    DIAMONDS = 1
    CLUBS = 2
    SPADES = 3

class Value(IntEnum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12

class Hand(IntEnum):
    HIGHCARD = 0
    ONEPAIR = 1
    TWOPAIR = 2
    THREEOFAKIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULLHOUSE = 6
    FOUROFAKIND = 7
    STRAIGHTFLUSH = 8
