import pandas as pd
import numpy as np
from lib import parser

nrow = 100

export = 'tidy_data'

actions = pd.read_csv('./sample/playeraction.csv', nrows=nrow)
players = pd.read_csv('./sample/seatjoined.csv', nrows=nrow)
blinds = pd.read_csv('./sample/playerblind.csv', nrows=nrow)
rounds = pd.read_csv('./sample/roundid.csv', nrows=nrow)


pd.DataFrame(
    data = {
        'blind_name': ['small_blind', 'big_blind'],
        'blind_id': [0, 1]
    }
).to_csv(f'{export}/blind_ids.csv')


rounds_df = rounds_reshaped = rounds.melt(
    id_vars='round_id', var_name='blind_id'
)
rounds_df['blind_id'] = rounds_df['blind_id'].apply(
    lambda x: {'small_blind': 0, 'big_blind': 1}[x]
)
rounds_df.to_csv(f'{export}/round_blinds.csv')


unique_players = players['user'].unique()
player_df = pd.DataFrame(
    data = {
        'user': unique_players,
        'id': range(len(unique_players))
    }
)
player_df.to_csv(f'{export}/user_ids.csv', index=False)


blinds_df = pd.merge(
    player_df, blinds,
    how='outer', on='user'
).dropna().drop(
    columns=['user']
).rename(
    columns={'id': 'user_id'}
)
blinds_df.to_csv(f'{export}/user_blinds.csv', index=False)
