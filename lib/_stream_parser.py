from operator import add
from types import SimpleNamespace
from collections import namedtuple

from ._enums import OutId as OId
from . import _stream_patterns as pt
from ._stream_patterns import out_types, data_info


data_gather = {
    OId.RoundId : (
        ['small_blind', 'big_blind'], 
        ['round_id']
    ),
    OId.RoundEnd : (
        [],
        ['round_id', 'turn']
    ),
    OId.SeatJoined : (
        ['seat', 'user', 'buyin'], 
        ['round_id']
    ),
    OId.PlayerBlind : (
        ['user', 'blind_type'], 
        ['round_id']
    ),
    OId.PlayerShowCards : (
        ['user', 'collects', 'state', 'amount'],
        ['round_id']
    ),
    OId.PlayerAction : (
        ['user', 'action', 'amount'],
        ['round_id', 'turn']
    ),
    OId.PotSize : (
        ['pot_size'],
        ['round_id']
    )
}

state_change = [
    OId.RoundStart,
    OId.RoundEnd,
    OId.SeatJoined,
    OId.PlayerBlind,
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
            lambda x: getattr(ns, x),
            data_gather[pid][1]
        ))
    ))

def updateState(pid, ns):
    if pid == OId.RoundStart:
        ns.round_id += 1
        ns.round = True
        ns.turn = 0
    elif not ns.round: return
    elif pid == OId.RoundEnd: ns.round = False
    elif pid == OId.NewTurn: ns.turn += 1

def parseCoro():
    ns = SimpleNamespace(
        round=False, turn=0, round_id=0, data=None
    )
    while True:
        line = yield
        pid, mch = parseLine(line)
        if pid is not None:
            if pid in data_gather and ns.round: 
                ns.data = extractData(pid, mch, ns)
            if pid in state_change:
                updateState(pid, ns)
        yield ns.data
        ns.data = None
                   
