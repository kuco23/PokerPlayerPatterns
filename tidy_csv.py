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

actions = pd.read_csv(import_from / 'playeraction.csv')
buyins = pd.read_csv(import_from / 'seatjoined.csv')
received = pd.read_csv(import_from / 'playerreceivedcard.csv')
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
    how='outer', on='user'
).dropna().drop(
    columns=['user']
)
buyins_df.to_csv(f'{export}/buyins.csv', index=False)


round_blinds = rounds.melt(
    id_vars='round_id', var_name='blind_type_id'
).replace(
    ['small_blind', 'big_blind'], [0, 1]
)
pd.merge(
    user_df, blinds, 'outer', 'user'
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


convert_suit = dict(zip(
    ['h', 'd', 'c', 's'],
    ['♠', '♣', '♦', '♥']
))
convert_value = dict(zip(
    list(map(str, range(2, 11))) + ['J', 'Q', 'K', 'A'],
    list(map(str, range(2, 11))) + ['J', 'Q', 'K', 'A']
))
def encodeCard(card):
    v = convert_value[card[:-1]]
    s = convert_suit[card[-1]]
    return v + s

pd.merge(
    user_df, received, 'outer', 'user'
).dropna().drop(
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


cardshow.amount = (
    cardshow.amount * 
    cardshow.state.replace(
        ['Loses', 'Wins'], [-1, 1]
    )
)
cardshow.drop(
    columns=['state']
).merge(
    user_df,
    how='outer', on='user'
).dropna().drop(
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
    user_df, 'outer', 'user'
).dropna().drop(
    columns=['user']
)
# Some players bought in without taking any actions.
# This will be treated as a fold.
active_users = set(action_df.user_id.unique())
inactive_users = [
    user for user in user_df.user_id
    if user not in active_users
]
inactive_rounds = [
    buyins_df[
        buyins_df.user_id == user_id
    ].round_id.values[0]
    for user_id in inactive_users
]
default_rows = [
    [0, 0, round_id, 0, -1, user_id]
    for user_id, round_id in zip(
        inactive_users, inactive_rounds
    )
]
action_df.append(pd.DataFrame(
    default_rows, columns = list(action_df.columns)
)).to_csv(f'{export}/actions.csv', index=False)


potsize.to_csv(f'{export}/potsize.csv', index=False)
