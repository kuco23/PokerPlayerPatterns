from operator import add
from types import SimpleNamespace
from collections import namedtuple

from ._enums import OutId as OId
from . import _stream_patterns as pt
from ._stream_patterns import out_types, data_info


data_gather = {
    OId.RoundId : (
        ['small_blind', 'big_blind'], 
        ['id']
    ),
    OId.RoundEnd : (
        [],
        ['id', 'turn']
    ),
    OId.SeatJoined : (
        ['seat', 'user', 'buyin'], 
        ['id']
    ),
    OId.SeatButton : (
        ['seat'], 
        ['id']
    ),
    OId.PlayerBlind : (
        ['user', 'blind_type'], 
        ['id']
    ),
    OId.PlayerShowCards : (
        ['user', 'collects', 'state', 'amount'],
        ['id']
    ),
    OId.PlayerAction : (
        ['user', 'action', 'amount'],
        ['id', 'turn', 'turn_stake']
    ),
    OId.PotSize : (
        ['pot_size'],
        ['id']
    )
}

state_change = [
    OId.RoundStart,
    OId.RoundEnd,
    OId.SeatJoined,
    OId.NewTurn,
    OId.PlayerAction
]

namedtuples = dict(zip(
    data_gather.keys(),
    map(
        lambda oid, data: namedtuple(
            oid.name, add(*data)
        ),
        data_gather.keys(),
        data_gather.values()
    )
))

class _Round:
                   
    def __init__(self, _id):
        self.id = _id
        self.__turn = 0
        self.turn_stake = 0

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, value):
        self.turn_stake = 0
        self.__turn = value


def parseLine(line):
    out_type = pt.out_type.search(line)
    out_type = out_type.group('out_type')
    if out_type in pt.out_types:
        for pat, pid in pt.out_types[out_type]:
            mch = pat.search(line)
            if mch: return pid, mch
    return None, None

def extractData(pid, match, ns):
    dct = match.groupdict()
    for key in dct:
        if dct[key] is None: continue
        dct[key] = data_info[pid][key](dct[key])

    return namedtuples[pid](*add(
        list(map(
            dct.get, 
            data_gather[pid][0]
        )),
        list(map(
            lambda x: getattr(ns.round, x),
            data_gather[pid][1]
        ))
    ))

def updateState(pid, match, ns):
    dct = match.groupdict()
    if pid == OId.RoundStart:
        ns.id += 1
        ns.round = _Round(ns.id)
    elif ns.round is None: return
    elif pid == OId.RoundEnd:
        ns.round = None
    elif pid == OId.SeatJoined:
        'generate new player'
    elif pid == OId.NewTurn:
        ns.round.turn += 1
    elif pid == OId.PlayerAction:
        if dct.get('amount'):
            amount = float(dct.get('amount'))
            ns.round.turn_stake += amount
    elif pid == OId.PlayerBlind:
        ns.round.turn_stake += dct.get('amount')

def parseCoro():
    ns = SimpleNamespace(round=None, id=0)
    while True:
        line = (yield)
        pid, mch = parseLine(line)
        if pid is None: continue
        if pid in data_gather and ns.round: 
            yield extractData(pid, mch, ns)
        if pid in state_change:
            updateState(pid, mch, ns)
                   
