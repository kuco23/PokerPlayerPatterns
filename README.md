PokerPlayerPatterns (PPP)
=====================
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kuco23/PokerPlayerPatterns/master)

In this project we analyse the data, which describes over 40 000 rounds of poker.
This data is taken from [KAGGLE.com](https://www.kaggle.com/smeilz/poker-holdem-games#File198.txt), though is also zipped in the repository under the name `poker_games.7z`

The main themes of the analysis contain:
- [x] correlation between the number of wins and the money-winning average,
- [x] the effect of specific card combinations on the winnings,
- [x] characterisation of bluffing.

In the repository there are two main scripts for converting the source file into more managable csv files. The first, `send_to_csv.py` takes the raw data inside `poker_games.txt` and sorts them into tables. The second, `tidy_csv.py` tidies the data into something more analysis-friendly.