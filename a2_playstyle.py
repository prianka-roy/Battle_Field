"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
from typing import Any
import random
from stack_for_a2 import Stack


class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError


class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)


class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    """
    bq = battle_queue.copy()
    if bq.is_over():
        if bq.get_winner() == bq.peek():
            return bq.peek().get_hp()
        elif bq.get_winner() == bq.peek().enemy:
            return bq.peek().enemy.get_hp() * -1

        return 0

    else:
        bq_a = bq.copy()
        bq_s = bq.copy()
        bq_a_current = bq_a.peek()
        bq_s_current = bq_s.peek()

        a_score = []
        s_score = []

            # There's a player at this state (our current player)
            # next_p!
        if bq_a_current.is_valid_action('A'):
            bq_a_current.attack()
            if bq_a_current.get_available_actions() != []:
                bq_a.remove()

            if bq_a_current != bq_a.peek():
                a_score.append(get_state_score(bq_a) * -1)
            elif bq_a_current == bq_a.peek():
                a_score.append(get_state_score(bq_a))

        if bq_s_current.is_valid_action('S'):
            bq_s_current.special_attack()
            if bq_s_current.get_available_actions() != []:
                bq_s.remove()

            if bq_s_current != bq_s.peek():
                s_score.append(get_state_score(bq_s) * -1)
            elif bq_s_current == bq_s.peek():
                s_score.append(get_state_score(bq_s))

        return max(a_score + s_score)


class RecursiveMinimax(Playstyle):
    """ RecursiveMinimax"""

    def __init__(self, battle_queue) -> None:
        """ Initializes"""
        self.battle_queue = battle_queue
        self.is_manual = False

    def select_attack(self, parameter: Any = None):
        """ Selects Attacks"""

        bq_a = self.battle_queue.copy()
        bq_s = self.battle_queue.copy()
        bq_a_player = bq_a.peek()
        bq_s_player = bq_s.peek()

        if bq_a_player.get_available_actions() == ['A']:
            return 'A'

        else:

            bq_a.peek().attack()
            if bq_a_player.get_available_actions() != []:
                bq_a.remove()

            bq_s.peek().special_attack()
            if bq_s_player.get_available_actions() != []:
                bq_s.remove()


            if bq_a_player == bq_a.peek():
                a_score = get_state_score(bq_a)
            else:
                a_score = get_state_score(bq_a) * -1

            if bq_s_player == bq_s.peek():
                s_score = get_state_score(bq_s)
            else:
                s_score = get_state_score(bq_s) * -1

            max_score = max(a_score, s_score)

            if max_score == a_score:
                return 'A'
            elif max_score == s_score:
                return 'S'


    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        return RecursiveMinimax(new_battle_queue)


class IterativeMinimax(Playstyle):
    """ IterativeMinimax Playstyle

    """

    def __init__(self, battle_queue) -> None:
        """ Initializes the IterativeMinimax"""

        self.battle_queue = battle_queue
        self.is_manual = False

    def select_attack(self, parameter: Any = None):
        """ Selects Attacks"""

        st = Stack()
        states = []
        char = self.battle_queue.peek()
        first_state = State(self.battle_queue)
        st.add(first_state)

        if char.get_available_actions() == ['A']:
            return 'A'
        else:

            while not st.is_empty():
                s = st.remove()
                states += [s]
                if s.bq.is_over():
                    if s.bq.get_winner() is None:
                        s.score = 0
                    elif s.bq.get_winner() != s.bq.peek():
                        s.score = s.bq.get_winner().get_hp() * -1
                    else:
                        s.score = s.bq.get_winner().get_hp()

                elif s.children != []:
                    c_score_l = []
                    for c in s.children:
                        if c.flip_score is True:
                            c_score_l += [(c.score * -1)]
                        else:
                            c_score_l += [c.score]

                    s.score = max(c_score_l)

                elif s.children == []:
                    bq_c = s.bq.copy()
                    state_c = bq_c.peek()
                    st.add(s)

                    bq_p = s.bq.copy()
                    state_p = bq_p.peek()

                    if state_c.is_valid_action("A"):

                        state_c.attack()
                        if state_c.get_available_actions() != []:
                            bq_c.remove()

                        new_c = State(bq_c)
                        states += [new_c]
                        s.children += [new_c]
                        st.add(new_c)

                        if state_c != bq_c.peek():
                            new_c.flip_score = True
                        else:
                            new_c.flip_score = False

                    if state_p.is_valid_action("S"):
                        state_p.special_attack()
                        if state_p.get_available_actions() != []:
                            bq_p.remove()

                        new_c2 = State(bq_p)
                        states += [new_c2]
                        s.children += [new_c2]
                        st.add(new_c2)

                        if state_c != bq_c.peek():
                            new_c2.flip_score = True
                        else:
                            new_c2.flip_score = False

            init_score = states[0].score

            for i in range(len(states[0].children)):

                if states[0].children[i].flip_score is True:
                    if init_score == (states[0].children[i].score * -1):
                        if i == 0:
                            return 'A'

                        return 'S'

                else:
                    if init_score == states[0].children[i].score:
                        if i == 0:
                            return 'A'

                        return 'S'


    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        return RecursiveMinimax(new_battle_queue)

class State:
    """ State class"""
    def __init__(self, bq: 'BattleQueue', children=None, score=0)-> None:
        """ Initializes a state"""

        self.bq = bq
        self.children = children[:] if children else []
        self.score = score
        self.flip_score = False


if __name__ == '__main__':

    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
