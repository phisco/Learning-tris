#!/usr/bin/env python
from __future__ import print_function
import itertools
import pickle
import random
class End(Exception):
    """
An Event thet gets raised when the game comes to an end.
why =      0  if tie. (default value)
      1 or 2  if player 1 or player 2 won.
    """
    def __init__(self, why=0):
        self.why = why

    def __getitem__(self, *obj):
            return self.why

    def clear(self):
        self.why = 0


class Error(UserWarning):
    """
    Generical kind of Warning,
    """
    def __init__(self, espressione, messaggio):
        self.expr = espressione
        self.str = messaggio

    def __str__(self):
        return repr(self.messaggio)


class partita(object):
    """
    Init class of the game, the two player's symbol can be costumized by
    passing them to the __init__(p1="X",p2="O")
    """
    def __init__(self, p1="X", p2="O"):
        self.field = field()
        player1 = human(player=1, symbol=p1, field=self.field)
        player2 = human(player=2, symbol=p2, field=self.field)
        self.p = {1: player1, 2: player2}
        self.turno = [1, 0]
        self.End = End()
        self.History = []

    def __main__(self):
        while self.__turno() is True:
            pass
        else:
            self.__save_history()
            return

    def __cambia_turno(self):
        self.turno[0] = self.turno[0] % 2 + 1
        self.turno[1] += 1
        if self.turno[1] is 8:
            raise End("end_of_game", "partita finita")

    def __gioca(self, coord):
        self.field[coord] = self.p[self.turno[0]].symbol

    def __check(self, player=0):
        if player is 0:
            player = self.turno[0]
        move_to_control = self.p[player].symbol
        counter = {"diag": [0, 0], "col": [0, 0, 0], "row": [0, 0, 0]}
        for key, val in self.field:
            if val is move_to_control:
                x, y = key
                counter["col"][y] += 1
                counter["row"][x] += 1
                if x == y:
                    counter["diag"][0] += 1
                if x == -1 * y + 2:
                    counter["diag"][1] += 1
        print(counter)
        for val in itertools.chain.from_iterable(counter.values()):
            if val is 3 and self.End.why is 0:
                    self.End.why = player
                    print("""
 __   __  _______  __   __    _     _  _______  __    _  __   __
|  | |  ||       ||  | |  |  | | _ | ||       ||  |  | ||  | |  |
|  |_|  ||   _   ||  | |  |  | || || ||   _   ||   |_| ||  | |  |
|       ||  | |  ||  |_|  |  |       ||  | |  ||       ||  | |  |
|_     _||  |_|  ||       |  |       ||  |_|  ||  _    ||__| |__|
  |   |  |       ||       |  |   _   ||       || | |   | __   __
  |___|  |_______||_______|  |__| |__||_______||_|  |__||__| |__|
                    """)
                    raise End

    def __turno(self):
        self.field.visualizza()
        player = self.p[self.turno[0]]
        player.ask_move()
        self.__gioca(player.move)
        try:
            self.__check()
            self.__cambia_turno()
        except End:
            self.field.visualizza()
            self.__store_history()
            if self.p[self.turno[0]].ask_to_play():
                self.__reset_game()
            else:
                return False
        return True

    def __store_history(self):
        """
It stores the whole history of the game in self.History,
a list of tuples of (why the game ended, (the sequence of the moves
that brought to the end) )
[((End.why), (alternated moves of the two players))]
        """
        def zip_alternated(it1, it2):
            for el1, el2 in itertools.izip_longest(it1, it2):
                yield el1
                yield el2
        self.History.append((self.End.why,
                            [move for move in
                             zip_alternated(self.p[1].history,
                                            self.p[2].history)]))
        for x in range(1, 3):
            self.p[x].history = []
    def __save_history(self):
        """
    At the moment it just print the whole self.History stored.
    So it prints the sum of every game that has been played.
    
    FILE will be the list "history" pickled to a file
    History is appended (the aim is to have "historical" memory)
        """
        savefile = open("savefile.p", "ab")
        pickle.dump(self.History, savefile)
        savefile.close()
        print (self.History)

    def __reset_game(self):
        self.field.reinit()
        self.End.clear()
        self.turno = [1, 0]


class AI(object,human):
    """
    inherit the __init__ and store personal history from human
    only ask_to_play and ask_move must be overloaded
    _choose_move must be implemented
To be implemented
    """
    def play (self):
        pass

    """
    STUB
    """
    def __init__(self, player = 2, symbol = 'O', field = None):
        self.field = field
        self.player = player
        self.symbol = symbol
        self.move = ()
        self.history = []
    
    def make_move (self):
        while True:
            x, y = random.sample([0,1,2], 2)
            if self.field[(x, y)] is " ":
                self.move = (x, y)
                self.history.append(self.move)
                break   

    def _choose_move(self):
        """
choose the move to play, must be implemented
        """

    def ask_to_play(self):
        """
Or true or based on a counter ???
        """
        return True

    def ask_move(self):
        """
To be implemented
        """
        pass

class human(object):
    """
The class of the human player, so it has the methods to ask for a move,
that gets stored in self.move as a tuple and appended to the personal history
of the player and the method to ask the player if he wants to play again.
To check if the move has not already been used, the field should be passed as
with the number of the player and the symbol he'll use,
like that: (player="1",symbol="X",field="self.field")
//self.field is setted to None as default !!
    """
    def __init__(self, player=1, symbol="X", field=None):
        self.field = field
        self.player = player
        self.symbol = symbol
        self.move = ()
        self.history = []

    def ask_to_play(self):
        return raw_input("Do you want to play again? "
                         "Yes/No\n").lower().startswith("y")

    def ask_move(self):
        try:
            x, y = (int(x)-1 for x in raw_input("Where do you want play? "
                                                "(x,y) \n").split(","))
            if max(x, y) > 2 or min(x, y) < 0:
                raise Error("Out_of_field", "coordinate non esistenti")
            elif self.field[(x, y)] is not " ":
                raise Error("Coord_used", "coordinate gia' usate")
            else:
                self.move = (x, y)
                self.store_p_history(self.move)
        except ValueError:
            print("Remember to write only the two coordinates, "
                  "separated by a comma.\nLike that: x,y")
            self.ask_move()
        except Error:
            print("The coordinates you have passed are wrong")
            self.ask_move()

    def store_p_history(self, coord):
        self.history.append(self.coord)


class field(object):
    """
Classe del campo da gioco
    """
    def __init__(self):
        self.field = {}
        self.coord = list(itertools.product(xrange(3), repeat=2))
        self.field.update(dict.fromkeys(self.coord, " "))

    def reinit(self):
        self.field.update(dict.fromkeys(self.coord, " "))

    def __iter__(self):
        for coord in self.coord:
            yield (coord, self.field[coord])

    def __getitem__(self, key):
            return self.field[key]

    def __setitem__(self, key, val):
        self.field[key] = val

    def visualizza(self):
        print('      1    2    3     ')
        for x in range(len(self.coord)/3):
            print("   ----------------- ")
            print(x+1, " |", end="")
            for y in range(len(self.coord)/3):
                print("| ", end="")
                print(self.field[(x, y)], end="")
                print(" |", end="")
            else:
                print("|")
        else:
            print("   ----------------- ")


if __name__ == "__main__":
    game = partita()
    game.__main__()
