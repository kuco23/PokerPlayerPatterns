import os
from pathlib import Path

import pandas as pd
import numpy as np

from lib import parser
from lib import TurnId

if not os.path.isdir('tidy_data'):
    os.mkdir('tidy_data')

import_from = Path.cwd() / 'parsed_data'
export = Path.cwd() / 'tidy_data'

actions = pd.read_csv(import_from / 'playeraction.csv')
buyins = pd.read_csv(import_from / 'seatjoined.csv')
blinds = pd.read_csv(import_from / 'playerblind.csv')
rounds = pd.read_csv(import_from / 'roundid.csv')
cardshow = pd.read_csv(import_from / 'playershowcards.csv')
potsize = pd.read_csv(import_from / 'potsize.csv')


pd.DataFrame(
    data = {
        'turn_name': [turn.name.lower() for turn in TurnId],
        'turn_id': list(map(int, TurnId))
    }
).to_csv(f'{export}/turn_ids.csv', index=False)


action_ids = pd.DataFrame(
    data = {
        'action_name': [
            'folds', 'calls', 'raises',
            'checks', 'bets', 'allin'
        ],
        'action_id': [0, 1, 2, 3, 4, 5]
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


round_blinds = rounds.melt(
    id_vars='round_id', var_name='blind_type_id'
).replace(
    ['small_blind', 'big_blind'], [0, 1]
)
pd.merge(
    player_df, blinds,
    how='outer', on='user'
).dropna().drop(
    columns=['user']
).replace(
    ['small', 'big'], [0, 1]
).rename(
    columns={'blind_type': 'blind_type_id'}
).merge(
    round_blinds,
    how='outer', on=['blind_type_id', 'round_id']
).to_csv(f'{export}/blinds.csv', index=False)


cardshow.amount = (
    cardshow.amount * 
    cardshow.state.replace(
        ['Loses', 'Wins'], [-1, 1]
    )
)
cardshow.drop(
    columns=['state']
).merge(
    player_df,
    how='outer', on='user'
).dropna().drop(
    columns=['user']
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
