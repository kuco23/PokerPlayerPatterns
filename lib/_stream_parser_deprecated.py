from types import SimpleNamespace

from ._enums import OutId as OId
from . import _stream_patterns as pt

class RoundPlayer:
    def __init__(self, player_name, seat, assets):
        self.name = player_name
        self.seat = seat
        self.assets = assets

        self.winnings = 0
        self.stakes = [0] * 5

        self.folded_to = -1
        self.folded_turn = -1
        self.raised_turn = -1
        self.times_raised = 0
        self.raise_sum = 0
        self.times_called = 0
        self.call_sum = 0
        self.times_allined = 0
    
    def addWinnings(self, winnings):
        self.winnings += winnings
    
    def addLosings(self, losings):
        self.winnings -= losings
    
    def folds(self, stake, turn):
        self.folded_to = stake - self.stakes[turn]
        self.folded_turn = turn

    def raises(self, amount, turn):
        self.stakes[turn] += amount
        self.times_raised += 1
        self.raise_sum += amount
        if not self.raised_turn: 
            self.raised_turn = turn

    def calls(self, amount, turn):
        self.stakes[turn] += amount
        self.times_called += 1
        self.call_sum += amount

    def allins(self, amount, turn):
        self.stakes[turn] += amount
        self.times_allined += 1

class RoundParser:
    _turns = ['PREFLOP', 'FLOP', 'TURN', 'RIVER']

    def __init__(self, round_id):
        self.id = round_id       

        self.players = dict()
        self.turn = 0
        self.pot = 0
        self.small_blind = -1
        self.big_blind = -1

        # data used only for export
        self.small_blind_player = None
        self.big_blind_player = None

    @property
    def turn_max_stake(self):
        return max(map(
            lambda p: p.stakes[self.turn],
            self.players.values()
        ))

    def __iter__(self):
        yield from self.players.values()
            
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
        self.big_blind_value = big_blind
        self.small_blind_value = small_blind

    def playerBuyin(self, seat, player_name, buyin):
        player = RoundPlayer(player_name, seat, buyin)
        self += player
    
    def smallBlind(self, player):
        self.small_blind_player = player.name
    
    def bigBlind(self, player):
        self.big_blind_player = player.name
    
    def newTurn(self, turn):
        self.turn += 1


def parseLine(line):
    out_type = pt.out_type.search(line)
    out_type = out_type.group('out_type')
    if out_type in pt.out_types:
        for pat, pid in pt.out_types[out_type]:
            mch = pat.search(line)
            if mch: return pid, mch
    return None, None

def parseMatch(pid, mch, rns):
    dic = mch.groupdict()

    if pid == OId.RoundStart: pass
        
    elif pid == OId.RoundId:
        rns.obj = RoundParser(rns.id)
        rns.obj.blinds(*map(
            float, dic.get('blinds').split('/')
        ))
    
    elif pid == OId.RoundEnd:
        rns.finished = True
        
    elif pid == OId.SeatJoined:
        user, seat, buyin = map(
            dic.get, ['user', 'seat', 'buyin']
        )
        rns.obj.playerBuyin(
            int(seat), user, float(buyin)
        )
        
    elif pid == OId.SeatButton: pass
        
    elif pid == OId.PlayerBlind:
        blind_type = dic.get('blind_type')
        player = rns.obj[dic.get('user')]
        if blind_type == "small":
            rns.obj.smallBlind(player)
        elif blind_type == "big":
            rns.obj.bigBlind(player)

    elif pid == OId.PlayerReceivedCard: pass
        
    elif pid == OId.PlayerShowCards:
        player = rns.obj[dic.get('user')]
        state = dic.get('state')
        amount = float(dic.get('amount'))
        if state == 'Wins': 
            player.addWinnings(amount)
        elif state == 'Loses': 
            player.addLosings(amount)
    
    elif pid == OId.PlayerAction:
        player = rns.obj[dic.get('user')]
        action = dic.get('action')
        amount = dic.get('amount')
        if action == 'folds':
            stake = rns.obj.turn_max_stake
            player.folds(stake, rns.obj.turn)
        elif action == 'calls': 
            player.calls(float(amount), rns.obj.turn)
        elif action == 'raises':
            player.raises(float(amount), rns.obj.turn)
        elif action == 'allin': 
            player.allins(float(amount), rns.obj.turn)
    
    elif pid == OId.NewTurn:
        rns.obj.newTurn(dic.get('turn_name'))

    elif pid == OId.PotSize:
        rns.obj.pot = float(dic['pot_size'])

def roundSeriesParser():
    round_ns = SimpleNamespace(
        obj=None, id=0, finished=False
    )
    while True:
        line = (yield)
        pid, mch = parseLine(line)
        if pid is None: continue
        parseMatch(pid, mch, round_ns)
        if round_ns.obj is not None and round_ns.finished:
            yield round_ns.obj
            round_ns.id += 1
            round_ns.obj = None
            round_ns.finished = False
