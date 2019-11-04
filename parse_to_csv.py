from collections import namedtuple
from functools import partial
from pathlib import Path
import csv

from lib import patterns, parser

DATA_DIR = Path.cwd() / 'datasets'
DATASET = DATA_DIR / 'poker_games.txt'
ROUND_DATA = DATA_DIR / 'round_data.csv'
PLAYER_DATA = DATA_DIR / 'player_data.csv'

ROUND_ROW = (
    'id',
    'turn',
    'pot',
    'small_blind_value',
    'big_blind_value',
    'small_blind_player',
    'big_blind_player'
)

PLAYER_ROW = (
    # round_id,
    'name',
    'assets',
    'winnings',
    'folded_to',
    'folded_turn',
    'raised_turn',
    'times_raised',
    'raise_sum',
    'times_called',
    'call_sum',
    'times_allined'
)

CsvWriter = partial(
    csv.writer, delimiter=',',
    quoting=csv.QUOTE_MINIMAL
)

def roundCsvWriter():
    with open(ROUND_DATA, 'w', newline='') as file:
        writer = CsvWriter(file)
        while True:
            _round = (yield)
            writer.writerow(
                [getattr(_round, row) for row in ROUND_ROW]
            )
            file.flush()

def playerCsvWriter():
    with open(PLAYER_DATA, 'w', newline='') as file:
        writer = CsvWriter(file)
        while True:
            _round = (yield)
            for player in _round:
                writer.writerow(
                    [_round.id] +
                    [getattr(player, row) for row in PLAYER_ROW]
                )
            file.flush()

player_writer = playerCsvWriter()
round_writer = roundCsvWriter()
round_parser = parser.roundSeriesParser()
next(player_writer) # prime generator
next(round_writer) # prime generator
next(round_parser) # prime generator
with open(DATASET, 'r') as file:
    for line in file:
        if not line.strip(): continue
        round_obj = round_parser.send(line)
        if round_obj is not None:
            round_writer.send(round_obj)
            player_writer.send(round_obj)
            
round_writer.close()
player_writer.close()
