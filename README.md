PokerPlayerPatterns (PPP)
-------------------------
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kuco23/PokerPlayerPatterns/master)

### General

This is a project which focuses on analysing 
the poker game dataset, which should give us 
some insight into patterns created by users.

We aim to represent every round, which includes 
gathering the following information:
- round's big and small blinds
- the turn round ended
- pot size

We also wish to capture the following information
about the round's featured players:
- user name
- buyin
- actions made
- money put in the pot
- money lost / won

Using this information hopefully we can execute
the following actions:
- analyse specific player's behaviour
- classify player into a certain subgroup
- determine the best player

### To do

Player data
- [ ] id
- [ ] name
- [ ] action
- [ ] money won / lost
- [ ] pot additions
- [ ] had small blind
- [ ] had big blind

Poker round csv data including columns
- [x] round id
- [x] turns played
- [x] pot size
- [x] small blind
- [x] big blind

### Data 

The datasets used are sourced from [here](https://www.kaggle.com/smeilz/poker-holdem-games#File198.txt).