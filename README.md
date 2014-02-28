                                                               X
  O-----------O             O-----------O--+-->.field  {(x,y):" "}
  |           |             |           |  |             ^     Y
  |  partita  |             |   field   |  |             |
  |           |     +-----> |           |  +-->.coord    |
  O-----------O     |       O-----------O          |     |
    |               |                            sorted(x,y)
    +-.field  ------+
    +-.player1 --------------+----------+-------+  O-----+-----O
    |                        |          |       +->|           |
    +-.player2 --------------+    O-----+-----O    |    A.I.   |
    |                        |    |           |    |           |
    +-.p --->{1: .player2    |    |   human   |    O-----------O
    |         2: .player1}---+    |           |
    |                             O-+---------O
    |                         +-----+
    |  0->8 turni ---+        +-.player :numero giocatore
    |                |        +-.symbol :simbolo che usa
    |  giocatore --+ |        +-.move   :ultima mossa
    |     1 o 2    | |        +-.history:memoria personale
    +-.turno ---->[1,0]                  [(x,y),(..),..]
    |
    |        O--------O
    +-.End   |  End   |--+-.why: 0:patta
    |        O--------O          1,2:vittoria per chi
    |
    +-.History
        storia globale:[ ( (End),
                           (alternate history .p[1] e .p[2]) ) ]










