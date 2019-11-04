PokerPlayerPatterns (PPP)
-------------------------

### General

This is a project which focuses on analysing 
the poker game dataset, which should give us 
some insight into patterns created by users.

We aim to represent every round, which includes 
gathering the following information:
- featured players' user name
- round pot
- round blinds
- featured players' actions
	 - calls
	 - raises
	 - folds
	 - allins

Using this information hopefully we can execute
the following actions:
- analyse specific player's behaviour
- classify player into a certain subgroup
- determine the best player

### To Do

Player data
- [ ] player id
- [ ] player name

Poker round csv data including columns
- [x] round id
- [x] turns played
- [x] pot size
- [x] small blind
- [x] big blind
- [x] small blind player
- [x] big blind player

Player round csv data including columns
- [x] round id
- [x] player id
- [x] player assets
- [x] winnings
- [x] folded to bet
- [x] turn folded
- [x] turn first raised
- [x] times raised
- [x] raise sum
- [x] times called
- [x] call sum
- [x] times allined
- [ ] hand

### Data 

The datasets used are sourced from [here](https://www.kaggle.com/smeilz/poker-holdem-games#File198.txt).