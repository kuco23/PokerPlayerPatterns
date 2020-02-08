from operator import add
from types import SimpleNamespace
from collections import namedtuple

from ._enums import OutId as OId
from . import _stream_patterns as pt
from ._stream_patterns import out_types, data_info


# data to gather from regex parser / context,
# namedtuples are created to represent rows
# in tables, each for every schema key
gather = {
    OId.RoundId : (
        ['small_blind', 'big_blind'], 
        ['round_id']
    ),
    OId.SeatJoined : (
        ['user', 'buyin'], 
        ['round_id']
    ),
    OId.PlayerReceivedCard: (
        ['user', 'card'],
        ['round_id']
    ),
    OId.PlayerBlind : (
        ['user', 'blind_type'], 
        ['round_id']
    ),
    OId.PlayerShowCards : (
        ['user', 'collects', 'state', 'amount', 'bets'],
        ['round_id']
    ),
    OId.PlayerAction : (
        ['user', 'action', 'amount'],
        ['round_id', 'turn', 'action_order']
    ),
    OId.NewTurn : (
        ['board', 'new_card'],
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
    OId.NewTurn,
    OId.PlayerAction
]

namedtuples = dict(zip(
    gather.keys(),
    map(
        lambda oid, data: namedtuple(
            oid.name, add(*data)
        ),
        gather.keys(),
        gather.values()
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

def extractData(pid, match, context):
    dct = match.groupdict()
    for key in dct:
        if dct[key] is None: continue
        dct[key] = data_info[pid][key](dct[key])
    return namedtuples[pid](*add(
        list(map(
            dct.get, 
            gather[pid][0]
        )),
        list(map(
            lambda x: getattr(context, x),
            gather[pid][1]
        ))
    ))

def updateContext(pid, context):
    if pid == OId.RoundStart:
        context.round_id += 1
        context.round = True
        context.turn = 0
        context.action_order = 0
    elif not context.round: return
    elif pid == OId.RoundEnd: context.round = False
    elif pid == OId.NewTurn: context.turn += 1
    elif pid == OId.PlayerAction: context.action_order += 1

def parseCoro():
    context = SimpleNamespace(
        round=False, turn=0,
        round_id=0, action_order=0,
        data=None
    )
    pid = None
    while True:
        line = yield (pid, context.data)
        context.data = None
        pid, mch = parseLine(line)
        if pid in state_change:
            updateContext(pid, context)
        if pid in gather and context.round:
            context.data = extractData(pid, mch, context)
