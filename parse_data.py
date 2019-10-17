from lib import patterns, parser

path = 'datasets/poker_games.txt'

with open(path, 'r') as file:
    h = [next(file) for _ in range(30)]

for line in h:
    if not line.strip(): continue
    pid, mch = parser.parseLine(line)
    print(pid, mch.groupdict())

    
