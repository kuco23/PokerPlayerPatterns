from operator import add
from pathlib import Path
import os
import csv

from lib import parser

FOLDER_NAME = 'parsed_data'
DATA_LOAD = Path.cwd() / 'poker_games.txt'
DATA_SAVE = Path.cwd() / FOLDER_NAME

if not os.path.isdir(FOLDER_NAME):
    os.mkdir(FOLDER_NAME)

gather_enums = parser.gather.keys()
gather_fields = [add(*t) for t in parser.gather.values()]
csv_names = [nm.name.lower() + '.csv' for nm in gather_enums]
csv_paths = [DATA_SAVE / csv_name for csv_name in csv_names]

def csvWriterCoro(filepath):
    filepath.touch()
    with open(filepath, 'w', newline='') as file:
        writer = csv.writer(file)
        while True:
            row = yield
            writer.writerow(row)

csv_writers = dict(zip(
    gather_enums,
    map(csvWriterCoro, csv_paths)
))

for writer, fields in zip(csv_writers.values(), gather_fields):
    next(writer) # priming generator
    writer.send(fields) # write column names

stream_parser = parser.parseCoro()
next(stream_parser) # priming generator
with open(DATA_LOAD, 'r') as file:
    for line in file:
        if not line.strip(): continue
        pid, data = stream_parser.send(line)
        if data is not None:
            csv_writers[pid].send(data)

for writer in csv_writers.values():
    writer.close()
        
