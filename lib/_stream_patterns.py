import re
from ._enums import OutId

_actions = '|'.join([
    'folds',
    'calls',
    'checks',
    'raises',
    'allin',
    'bets'
])

out_type = re.compile(
    r'\*?(?P<out_type>[^\s]+)'
)
game_start = re.compile(
    r'Game started at: '
    r'(?P<date>[\d/]+) '
    r'(?P<time>[\d:]+)'
)
game_id = re.compile(
    r'Game ID: '
    r'(?P<game_id>\d+) '
    r'(?P<blinds>[\d\./]+) '
)
game_end = re.compile(
    r'Game ended at: '
    r'(?P<date>[\d/]+) '
    r'(?P<time>[\d:]+)'
)
seat_joined = re.compile(
    r'Seat '
    r'(?P<seat>\d): '
    r'(?P<username>.+?) '
    r'\((?P<buyin>[\d\.]+)\)\.'
)
seat_button = re.compile(
    r'Seat (?P<seat>\d) is the button'
)
player_blind = re.compile(
    r'Player (?P<username>.+?) '
    r'has (?P<blind_type>\w+) blind '
    r'\((?P<blind_amount>[\d\.]+)\)'
)
player_received_card = re.compile(
    r'Player (?P<username>.+?) '
    r'received(?: a)? card'
)
player_action = re.compile(
    r'Player (?P<username>.+?) '
    rf'(?P<action>{_actions})'
    r'(?: \((?P<amount>[\d\.]+)\))?'
)
player_show_cards = re.compile(
    r'\*?Player '
    r'(?P<username>.+?) '
    r'(?:mucks )?'
    r'(?:\(?does not show cards\)?\.)|'
    r'(?:shows: (?P<hand>.+?)\. )'
    r'Bets: (?P<bets>[\d\.]+)\. '
    r'Collects: (?P<collects>[\d\.]+)\. '
    r'(?P<state>Wins|Loses): '
    r'(?P<amount>[\d\.]+)\.'
)
new_turn = re.compile(
    r'\*{3} '
    r'(?P<turn_name>\w+) '
    r'\*{3}: '
    r'(?P<board>\[.+?\])'
    r'(?: (?P<new_card>\[\w{2}\]))?'
)
pot_size = re.compile(
    r'Pot: '
    r'(?P<pot_size>[\d\.]+)'
)
board_show = re.compile(
    r'(?P<board>\[.+?\])'
)

out_types = {
    'Game': [
        (game_start, OutId.GameStart),
        (game_end, OutId.GameEnd),
        (game_id, OutId.GameId)
    ],
    'Seat': [
        (seat_joined, OutId.SeatJoined),
        (seat_button, OutId.SeatButton)
    ],
    'Player': [
        (player_blind, OutId.PlayerBlind),
        (player_received_card, OutId.PlayerReceivedCard),
        (player_show_cards, OutId.PlayerShowCards),
        (player_action, OutId.PlayerAction)
    ],
    '**': [
        (new_turn, OutId.NewTurn)
    ],
    'Pot': [
        (pot_size, OutId.PotSize)
    ],
    'Board': [
        (board_show, OutId.BoardShow)
    ]
}
