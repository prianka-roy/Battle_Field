""" Stack Class"""
from typing import Any


class Stack:
    """ Stack is a kind of container to store objects"""

    def __init__(self) -> None:
        """ Initializes the stack class

        >>> s = Stack()
        >>> s.is_empty()
        True
        """
        self._contain = []

    def add(self, other: Any) -> None:
        """ Add an object to the Stack

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add('A')
        >>> s.is_empty()
        False
        """

        self._contain.append(other)

    def remove(self) -> Any:
        """
        Remove an object from Stack

        >>> q = Stack()
        >>> q.add("A")
        >>> q.add("B")
        >>> q.remove()
        'B'
        """

        if not self.is_empty():
            return self._contain.pop(-1)
        else:
            raise Exception('EmptyContainer')

    def __str__(self) -> str:
        """
        String rep of the Stack

        >>> s = Stack()
        >>> s.add('A')
        >>> s.add('B')
        >>> str(s)
        'A, B'
        """
        res = ''
        for i in self._contain:
            res += str(i)
        return ', '.join(res)

    def __repr__(self) -> str:
        """ Repr method for Stack

        >>> s = Stack()
        >>> s.add('A')
        >>> s.add('B')
        >>> repr(s)
        'A, B'
        """
        res = ''
        for i in self._contain:
            res += str(i)
        return ', '.join(res)

    def is_empty(self) -> bool:
        """ Checks if a Container is empty or not

        >>> s = Stack()
        >>> s.is_empty()
        True
        >>> s.add('A')
        >>> s.is_empty()
        False
        """

        return self._contain == []


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config='a2_pyta.txt')
