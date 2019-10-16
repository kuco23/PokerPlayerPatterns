import re

path = 'datasets/poker_games.txt'

actions = [
    'folds',
    'calls',
    'checks',
    'raises'
]
actionstr = '|'.join(actions)

rx_out_type = re.compile(
    r'\*?(?P<typeo>[^\s]+)'
)

rx_game_start = re.compile(
    r'Game started at: '
    r'(?P<date>[\d/]+) '
    r'(?P<time>[\d:]+)'
)
rx_game_id = re.compile(
    r'Game ID: '
    r'(?P<id>\d+) '
    r'(?P<blinds>[\d\./]+) '
)
rx_game_end = re.compile(
    r'Game ended at: '
    r'(?P<date>[\d/]+) '
    r'(?P<time>[\d:]+)'
)
rx_seat_joined = re.compile(
    r'Seat '
    r'(?P<seat>\d): '
    r'(?P<username>.+?) '
    r'\((?P<buyin>[\d\.]+)\)\.'
)
rx_seat_button = re.compile(
    r'Seat (?P<seat>\d) is the button'
)
rx_player_blind = re.compile(
    r'Player (?P<username>[^\s]+) '
    r'has (?P<blind_type>\w+) blind '
    r'\((?P<blind_amount>[\d\.]+)\)'
)
rx_player_received_card = re.compile(
    r'Player (?P<username>.+?) '
    r'received a card\.'
)
rx_player_action = re.compile(
    r'Player (?P<username>.+?) '
    rf'(?P<action>{actionstr})'
    r'(?: \((?P<amount>[\d\.]+)\))?'
)
rx_player_show_cards = re.compile(
    r'\*?Player '
    r'(?P<username>[^\s]+) '
    r'(\)?(?:does not show cards\.)\)?|'
    r'(?:shows: (?P<hand>.+?\.)))'
    r'Bets: (?P<bets>[\d\.]+) '
    r'Collects: (?P<collects>[\d\.]+) '
    r'Loses: (?P<loses>[\d\.]+)'
)
rx_new_turn = re.compile(
    r'\*{3} '
    r'(?P<turn_name>\w+) '
    r'\*{3}: '
    r'(?P<board>\[.+?\])'
    r'(?: (?P<new_card>\[\w{2}\]))?'
)
rx_pot = re.compile(
    r'Pot: '
    r'(?P<pot_size>[\d\.]+)'
)
rx_board = re.compile(
    r'(?P<board>\[.+?\])'
)

out_types = {
    'Game': [
        rx_game_start,
        rx_game_end,
        rx_game_id
    ],
    'Seat': [
        rx_seat_joined,
        rx_seat_button
    ],
    'Player': [
        rx_player_blind,
        rx_player_received_card,
        rx_player_show_cards,
        rx_player_action
    ],
    '**': [
        rx_new_turn
    ],
    'Pot': [
        rx_pot
    ],
    'Board': [
        rx_board
    ]
}

with open(path, 'r') as file:
    h = [next(file) for _ in range(50)]

for line in h:
    out_type = rx_out_type.search(line)
    out_type = out_type.group('typeo')
    if out_type in out_types:
        for rx in out_types[out_type]:
            mach = rx.search(line)
            if mach:
                print('')
                print(line.strip())
                print(mach.groupdict())
                break
        else:
            print('WARNING', line)
