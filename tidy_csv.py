import os
from pathlib import Path

import pandas as pd
import numpy as np
from lib import parser

if not os.path.isdir('tidy_data'):
    os.makedir('tidy_data')

nrow = 10**10
import_from = Path.cwd() / 'parsed_data'
export = Path.cwd() / 'tidy_data'

actions = pd.read_csv(import_from / 'playeraction.csv', nrows=nrow)
buyins = pd.read_csv(import_from / 'seatjoined.csv', nrows=nrow)
blinds = pd.read_csv(import_from / 'playerblind.csv', nrows=nrow)
rounds = pd.read_csv(import_from / 'roundid.csv', nrows=nrow)
cardshow = pd.read_csv(import_from / 'playershowcards.csv', nrows=nrow)
potsize = pd.read_csv(import_from / 'potsize.csv', nrows=nrow)


pd.DataFrame(
    data = {
        'turn_name': ['preflop', 'flop', 'turn', 'river'],
        'turn_id': [0, 1, 2, 3]
    }
).to_csv(f'{export}/turn_ids.csv', index=False)


pd.DataFrame(
    data = {
        'blind_type': ['small_blind', 'big_blind'],
        'blind_type_id': [0, 1]
    }
).to_csv(f'{export}/blind_type_ids.csv', index=False)


pd.DataFrame(
    data = {
        'state_name': ['Loses', 'Wins'],
        'state_id': [0, 1]
    }
).to_csv(f'{export}/state_name_ids.csv', index=False)


action_ids = pd.DataFrame(
    data = {
        'action_name': [
            'folds', 'calls', 'raises',
            'checks', 'bets', 'allin'
        ],
        'action_id': [
            0, 1, 2, 3, 4, 5
        ]
    }
)
action_ids.to_csv(f'{export}/action_ids.csv', index=False)


unique_players = buyins['user'].unique()
player_df = pd.DataFrame(
    data = {
        'user': unique_players,
        'user_id': range(len(unique_players))
    }
)
player_df.to_csv(f'{export}/user_ids.csv', index=False)


pd.merge(
    buyins, player_df,
    how='outer', on='user'
).dropna().drop(
    columns=['user']
).to_csv(f'{export}/buyins.csv', index=False)


rounds.melt(
    id_vars='round_id', var_name='blind_type_id'
).replace(
    ['small_blind', 'big_blind'], [0, 1]
).to_csv(f'{export}/round_blinds.csv', index=False)


pd.merge(
    player_df, blinds,
    how='outer', on='user'
).dropna().drop(
    columns=['user']
).replace(
    ['small', 'big'], [0, 1]
).to_csv(f'{export}/user_blinds.csv', index=False)
    

pd.merge(
    cardshow, player_df,
    how='outer', on='user'
).dropna().drop(
    columns=['user']
).replace(
    ['Loses', 'Wins'], [0, 1]
).rename(
    columns={'state': 'state_id'}
).to_csv(f'{export}/cardshow.csv', index=False)


actions.amount = actions.amount.replace(pd.NaT, 0)
pd.merge(
    actions, player_df,
    how='outer', on='user',
).dropna().drop(
    columns=['user']
).merge(
    action_ids,
    how='outer', left_on='action', right_on='action_name'
).dropna().drop(
    columns=['action', 'action_name']
).to_csv(f'{export}/actions.csv', index=False)


potsize.to_csv(f'{export}/potsize.csv', index=False)
