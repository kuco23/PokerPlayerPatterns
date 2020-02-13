PokerPlayerPatterns (PPP)
=====================
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/kuco23/PokerPlayerPatterns/master)

V projektu bom analiziral podatke, ki opisujejo 40 000 odigranih partij pokra.
Podatki so vzeti od [tukaj](https://www.kaggle.com/smeilz/poker-holdem-games#File198.txt).

Med zajete podatke spadajo:
- [x] karte dobljene na začetku partije,
- [x] igralčeve akcije,
- [x] igralčev končni relativni dobiček.

Analiza vključuje naslednje teme:
- [x] korelacija med številom zmag in povprečjem dobičkov,
- [x] vpliv kombinacij vrednosti kart na dobiček,
- [x] karakterizacija in analiza blefiranja.

V repozitoriju sta dve glavni skripti za predelavo podatkov v csv.
Skripta `send_to_csv.py` podatke v `poker_games.txt` spravi
v tabele sprejemljive oblike, `tidy_csv.py` pa jih popravi
v podatke prijazne za analizo. Končne čiste tabele so predstavljene
v datoteki `notebook_tabele.ipynb`.