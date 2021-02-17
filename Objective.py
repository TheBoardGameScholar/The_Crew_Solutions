# Objective class for - The Crew: The Quest for Planet Nine
# The Board Game Scholar Post 4
# Freddy Reiber
import random
from Hand import Hand


class Objective:
    listOfAllColors = ['B', 'P', 'G', 'Y']

    # Objectives represent cards that must be won by who ever has the Objective.
    # Rocket Cards are not able to be objectives
    def __init__(self, token=0, player=None, suit=None, value=None, ):

        if suit == 'R':
            raise ValueError('Rocket cards cannot be objective cards')
        # Generates a random Objective if nothing is passed to the constructor
        if suit is None and value is None:
            self._suit = self.listOfAllColors[random.randint(0, 3)]
            self._value = random.randint(1, 9)
        else:
            self._suit = suit
            self._value = value
        self.taskToken = token
        self.player = player
        self.criticalCards = [ self._suit + str(self._value)]
        self._completed = False

    def __eq__(self, other):
        if isinstance(other, Objective):
            if other._suit == self._suit and other._value == self._value:
                return True
        return False

    def __repr__(self):
        return self._suit + str(self._value)
        # + ", " + str(self.player) + ", " + str(self.taskToken)

    # Task Tokens are the modifiers to tasks. They can be an int 1-5, which means that task must in that position.
    # Tasks can also be a -1, which means they must be completed last
    # Tasks can also be a 11, 12, 13, 14. Tasks with this code must be completed in order, but other tasks can go in between.
    def setTaskToken(self, newToken):
        self.taskToken = newToken

    # Sets which player has this objective
    def setPlayer(self, player):
        self.player = player

    def addCriticalCards(self, newCriticalCard):
        self.criticalCards.append(newCriticalCard)

    def clearCriticalCards(self):
        self.criticalCards = []

    # Returns the suit char
    def suit(self):
        return self._suit

    # Returns the value int
    def value(self):
        return self._value

    def getCard(self):
        return self._suit + str(self._value)

    # Checks for completion when a hand is taken
    def setComplete(self, Status):
        self._completed = Status

    def isComplete(self):
        return self._completed
