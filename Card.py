# Card class for - The Crew: The Quest for Planet Nine
# Board Game Scholar Project #4
# Freddy Reiber

class Card:

    # Suit is one of four colors - blue, pink, yellow, or green, or a rocket card and represented as a char
    # Value is a value from 1-9 for color cards and 1-4 for rocket cards. Represented as an int
    def __init__(self, suit: str, value: int):
        self._suit = suit
        if self.suit == 'R' and value > 4:
            raise ValueError("Rockets can only be of value 4 or less")
        self._value = value
        self._critical = False

    def __eq__(self, other):
        if isinstance(other, str):
            if other[0] == self._suit and int(other[1]) == self._value:
                return True
        if isinstance(other, Card):
            if self._suit == other.suit() and self._value == other.value():
                return True
        return False

    def __repr__(self):
        return self._suit + str(self._value)

    # Returns the suit char
    def suit(self):
        return self._suit

    # Checks if card is critical
    def isCritical(self):
        return self._critical

    # Returns the value int
    def value(self):
        return self._value

    # Sets the critical status of the card
    def setCritical(self, status):
        self._critical = status
