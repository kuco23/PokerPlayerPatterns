from collections import namedtuple

from lib import patterns, parser

path = 'datasets/poker_games.txt'

with open(path, 'r') as file:
    h = [next(file) for _ in range(100)]

for line in h:
    if not line.strip(): continue
    data = parser.parseLine(line)
    if data:
        pid, mch = data
        print(line)
        print(pid, mch.groupdict())

    

('round_id', 'big_blind', 'small_blind')
('player_id', 'player_name')
(
    'round_id',
    'player_id',
    'gave_big_blind',
    'gave_small_blind',
    'fold_before_turn',
    'raise_before_turn',
    'number_of_calls'
)
    
 
