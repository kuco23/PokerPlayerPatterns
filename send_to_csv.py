from collections import namedtuple
from functools import partial
from pathlib import Path
import csv

from lib import *

DATA_DIR = Path.cwd() / 'datasets'
DATASET_PATH = DATA_DIR / 'poker_games.txt'

stream_parser = parser.parseCoro()
next(stream_parser) # prime generator
with open(DATASET_PATH, 'r') as file:
    for line in file:
        if not line.strip(): continue
        tup = stream_parser.send(line)
        if tup: print(tup)
        
