from pathlib import Path
import csv

from lib import parser

DATA_DIR = Path.cwd() / 'datasets'
DATASET_PATH = DATA_DIR / 'poker_games.txt'

csv_paths = list(map(
    lambda nm: DATA_DIR /  f'{nm.name.lower()}.csv',
    parser.data_gather.keys()
))

def csvWriterCoro(filepath):
    filepath.touch()
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        while True:
            row = yield
            writer.writerow(row)

csv_writers = dict(zip(
    parser.data_gather.keys(),
    map(csvWriterCoro, csv_paths)
))

for writer in csv_writers.values():
    next(writer) # priming generators

stream_parser = parser.parseCoro()
next(stream_parser)
with open(DATASET_PATH, 'r') as file:
    for line in file:
        if not line.strip(): continue
        pid, data = stream_parser.send(line)
        next(stream_parser)
        if data is not None: 
            csv_writers[pid].send(data)

for writer in csv_writers.values():
    writer.close()
        
