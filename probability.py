## probability used in Sudoku solving ##
## by A.C.B. ##

from config import *

class Probability:
    def __init__(self, p):
        assert p >= 0 and p <= 1
        self.value = p

    # comparison #

    def __lt__(self, other) -> bool:
        if instanceof(other, Probability):
            return self.value < other.value
        return self.value < other
    
    def __gt__(self, other) -> bool: 
        if instanceof(other, Probability):
            return self.value > other.value
        return self.value > other

    def __eq__(self, other) -> bool: 
        if instanceof(other, Probability):
            return self.value == other.value
        return self.value == other

    # unary #
    def __invert__(self) -> 'Probability':
        return Probability(1 - self.value)

    # arithmetic #

    def __div__(self, other) -> 'Probability':
        assert not instanceof(other, Probability)
        return Probability(self.value / other)

    def __idiv__(self, other) -> 'Probability':
        self.value = self.value / other
        return self

    def __add__(self, other) -> 'Probability':
        if instanceof(other, Probability):
            return Probability(self.value + other.value)
        return Probability(self.value + other)
    
    def __iadd__(self, other) -> 'Probability':
        value = self.value + other
        return Probability(value)

    # string formatting
    def __str__(self) -> str:
        return "{0:.2f}".format(self.value)

# common values #
UNIFORM = Probability(1/D)
NEVER = Probability(0)
ALWAYS = Probability(1)

# TODO tests/main