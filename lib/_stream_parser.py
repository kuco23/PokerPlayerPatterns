from types import SimpleNamespace

from ._enums import OutId as OId
from . import _stream_patterns as pt

class RoundPlayer:
    def __init__(self, player_name, seat, assets):
        self.seat = seat
        self.name = player_name
        self.assets = assets

        self.has_folded = False
        self.has_folded_preflop = False
        self.has_raised_preflop = False
        self.number_of_raises = 0
        self.sum_of_raises = 0
        self.number_of_calls = 0
        self.number_of_allins = 0

        self.winnings = 0
    
    def addWinnings(self, winnings):
        self.winnings += winnings
    
    def addLosings(self, losings):
        self.winnings -= losings
    
    def folds(self, turn):
        self.has_folded = True
        if turn == 0: 
            self.has_folded_preflop = True

    def raises(self, amount, turn):
        self.number_of_raises += 1
        self.sum_of_raises += amount
        if turn == 0: 
            self.has_raised_preflop = True

    def calls(self, amount):
        pass

    def allins(self, amount):
        self.number_of_allins += 1

class RoundParser:
    _turns = ['PREFLOP', 'FLOP', 'TURN', 'RIVER']

    def __init__(self, round_id, time=-1):
        self.id = round_id
        self.time_started = time

        self.small_blind_value = -1
        self.big_blind_value = -1
        self.button = None
        self.small_blind_player = None
        self.big_blind_player = None

        self.players = dict()
        self.turn = 0
        self.is_finished = False
    
    def __iadd__(self, player : RoundPlayer):
        self.players[player.name] = player
        return self
    
    def __getitem__(self, player_name):
        return self.players.get(player_name)
    
    def getPlayerBySeat(self, player_seat):
        for player in self.players.values():
            if player.seat == player_seat:
                return player

    def blinds(self, big_blind, small_blind):
        self.big_blind = big_blind
        self.small_blind = small_blind

    def playerBuyin(self, seat, player_name, buyin):
        player = RoundPlayer(player_name, seat, buyin)
        self.players[player_name] = player
    
    def seatButton(self, seat):
        self.button = self.getPlayerBySeat(seat)
    
    def smallBlind(self, player_name):
        self.small_blind_player = self[player_name]
    
    def bigBlind(self, player_name):
        self.big_blind_player = self[player_name]
    
    def newTurn(self, turn):
        self.turn += 1


def parseLine(line):
    out_type = pt.out_type.search(line)
    out_type = out_type.group('out_type')
    if out_type in pt.out_types:
        for pat, pid in pt.out_types[out_type]:
            mch = pat.search(line)
            if mch: return pid, mch

def parseMatch(pid, mch, rns):
    dic = mch.groupdict()
    round_ = rns.obj

    if pid == OId.RoundStart:
        rns.obj = RoundParser(
            round_.id, dic.get('time')
        )
    
    elif pid == OId.RoundEnd:
        round_.is_finished = True

    elif pid == OId.RoundId:
        round_.blinds(*map(
            float, dic.get('blinds').split('/')
        ))
        
    elif pid == OId.SeatJoined:
        user, seat, buyin = map(
            dic.get, ['user', 'seat', 'buyin']
        )
        round_.playerBuyin(
            user, seat, float(buyin)
        )
        
    elif pid == OId.SeatButton:
        round_.seatbutton(int(dic.get('button')))
        
    elif pid == OId.PlayerBlind:
        blind_type = dic.get('blind_type')
        player = round_[dic.get('user')]
        if blind_type == "small": 
            round_.smallBlind(player)
        elif blind_type == "big":
            round_.bigBlind(player)
        
    elif pid == OId.PlayerShowCards:
        player = round_[dic.get('user')]
        state = dic.get('state')
        amount = float(dic.get('amount'))
        if state == 'Wins': 
            player.addWinnings(amount)
        elif state == 'Loses': 
            player.addLosings(amount)
    
    elif pid == OId.PlayerAction:
        player = round_[dic.get('user')]
        action = dic.get('action')
        amount = float(dic.get('amount'))
        if action == 'folds': 
            player.folds(round_.turn)
        elif action == 'calls': player.calls()
        elif action == 'raises': player.raises(amount)
        elif action == 'allin': player.allins(amount)
    
    elif pid == OId.NewTurn:
        round_.newTurn(dic.get('turn_name'))
    
    return False

def roundSeriesParser():
    yield None # priming the generator
    round_ns = SimpleNamespace(obj=None, id=0)
    while True:
        line = (yield)
        pid, mch = parseLine(line)
        round_finished = parseMatch(pid, mch, round_ns)
        if round_finished: yield round_ns.obj

round_row = ('round_id', 'time', 'button', 'small_blind', 'big_blind')