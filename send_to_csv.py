from operator import add
from pathlib import Path
import csv

from lib import parser

DATA_LOAD = Path.cwd() / 'datasets'
DATA_SAVE = Path.cwd() / 'sample'
DATA_PATH = DATA_LOAD / 'poker_games.txt'

gather_enums = parser.gather.keys()
gather_fields = [add(*t) for t in parser.gather.values()]
csv_paths = [
    DATA_SAVE / f'{nm.name.lower()}.csv'
    for nm in gather_enums
]

def csvWriterCoro(filepath, fields):
    filepath.touch()
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(fields)
        while True:
            row = yield
            writer.writerow(row)

csv_writers = dict(zip(
    gather_enums,
    map(csvWriterCoro, csv_paths, gather_fields)
))
for writer in csv_writers.values():
    next(writer) # priming generators

stream_parser = parser.parseCoro()
next(stream_parser)
with open(DATA_PATH, 'r') as file:
    for line in file:
        if not line.strip(): continue
        pid, data = stream_parser.send(line)
        if data is not None:
            csv_writers[pid].send(data)

for writer in csv_writers.values():
    writer.close()
        
