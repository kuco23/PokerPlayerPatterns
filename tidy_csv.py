import os
from pathlib import Path
import pandas as pd
import numpy as np
from lib import parser
from lib import TurnId, ActionId

if not os.path.isdir('tidy_data'):
    os.mkdir('tidy_data')

import_from = Path.cwd() / 'parsed_data'
export = Path.cwd() / 'tidy_data'

varnames = {
    'actions': 'playeraction',
    'buyins': 'seatjoined',
    'received': 'playerreceivedcard',
    'blinds': 'playerblind',
    'rounds': 'roundid',
    'cardshow': 'playershowcards',
    'potsize': 'potsize',
    'newturn': 'newturn'
}
for varname, filename in varnames.items():
    path = import_from / (filename + '.csv')
    globals()[varname] = pd.read_csv(path)

convert_suit = dict(zip(
    ['h', 'd', 'c', 's'],
    ['♠', '♣', '♦', '♥']
))
convert_value = dict(zip(
    list(map(str, range(2, 11))) + ['J', 'Q', 'K', 'A'],
    list(map(str, range(2, 11))) + ['J', 'Q', 'K', 'A']
))
encodeCard = lambda card: (
    convert_value[card[:-1]] + convert_suit[card[-1]]
)


pd.DataFrame(
    data = {
        'turn_name': [turn.name.lower() for turn in TurnId],
        'turn_id': list(map(int, TurnId))
    }
).to_csv(f'{export}/turn_ids.csv', index=False)


action_ids = pd.DataFrame(
    data = {
        'action_name': [action.name.lower() for action in ActionId],
        'action_id': list(map(int, ActionId))
    }
)
action_ids.to_csv(f'{export}/action_ids.csv', index=False)


unique_users = buyins['user'].unique()
user_df = pd.DataFrame(
    data = {
        'user': unique_users,
        'user_id': range(len(unique_users))
    }
)
user_df.to_csv(f'{export}/user_ids.csv', index=False)


buyins_df = pd.merge(
    buyins, user_df,
    how='inner', on='user'
).drop(
    columns=['user']
)
buyins_df.to_csv(f'{export}/buyins.csv', index=False)


round_blinds = rounds.melt(
    id_vars='round_id', var_name='blind_type_id'
).replace(
    ['small_blind', 'big_blind'], [0, 1]
)
pd.merge(
    user_df, blinds, 'inner', 'user'
).drop(
    columns=['user']
).replace(
    ['small', 'big'], [0, 1]
).rename(
    columns = {
        'blind_type': 'blind_type_id',
        'value': 'blind_value'
    }
).merge(
    round_blinds,
    'inner', ['blind_type_id', 'round_id']
).to_csv(f'{export}/blinds.csv', index=False)


pd.merge(
    user_df, received, 'inner', 'user'
).drop(
    columns=['user']
).groupby(
    ['round_id', 'user_id']
).apply(
    lambda df: pd.DataFrame(
        data = dict(zip(
            ['card1', 'card2'],
            sorted([
                [encodeCard(list(df.card)[0])],
                [encodeCard(list(df.card)[1])]
            ])
        ))
    )
).reset_index().drop(
    columns=['level_2']
).to_csv(f'{export}/received_cards.csv', index=False)


cardshow.assign(
    winnings = (
        cardshow.amount * 
        cardshow.state.replace(
            ['Loses', 'Wins'], [-1, 1]
        )
    )
).drop(
    columns=['state', 'amount']
).merge(
    user_df, 'inner', 'user'
).drop(
    columns=['user']
).to_csv(f'{export}/cardshow.csv', index=False)


actions.amount = actions.amount.replace(pd.NaT, 0)
action_df = actions.replace([
    'folds', 'calls', 'raises', 
    'checks', 'bets', 'allin'
    ],[0, 1, 2, 3, 4, 5]
).rename(
    columns = {
        'action': 'action_id',
        'turn': 'turn_id'
    }
).merge(
    user_df, 'inner', 'user'
).drop(
    columns=['user']
).to_csv(f'{export}/actions.csv', index=False)


newturn.new_card = newturn.new_card.replace(pd.NaT, '')
newturn.assign(
    board = [
        ' '.join(encodeCard(c) for c in cards.split())
        for cards in (newturn.board + ' ' + newturn.new_card)
    ]
).drop(
    columns=['new_card']
).rename(
    columns = dict(turn='turn_id')
).to_csv(f'{export}/board.csv', index=False)


potsize.to_csv(f'{export}/potsize.csv', index=False)
