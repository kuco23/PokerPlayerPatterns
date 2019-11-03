from collections import namedtuple
from pathlib import Path
import csv

from lib import patterns, parser

DATA_DIR = Path.cwd() / 'datasets'
DATASET = DATA_DIR / 'poker_games.txt'
ROUND_DATA = DATA_DIR / 'round_data.csv'

ROUND_ROW = (
    'turn',
    'pot',
    'small_blind_value',
    'big_blind_value',
    'small_blind_player',
    'big_blind_player'
)

def roundCsvWriter():
    with open(ROUND_DATA, 'w', newline='') as file:
        writer = csv.writer(
            file, delimiter=',',
            quoting=csv.QUOTE_MINIMAL
        )
        while True:
            _round = (yield)
            writer.writerow(
                [_round.__dict__[row] for row in ROUND_ROW]
            )
            file.flush()

round_counter = 0
round_writer = roundCsvWriter()
round_parser = parser.roundSeriesParser()
next(round_writer) # prime generator
next(round_parser) # prime generator
with open(DATASET, 'r') as file:
    for line in file:
        print(line)
        if not line.strip(): continue
        round_obj = round_parser.send(line)
        if round_obj is not None:
            round_writer.send(round_obj)
            round_counter += 1
            
            if round_counter >= 1:
                break
        
    
    
    
    
