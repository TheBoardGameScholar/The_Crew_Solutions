# Hand class for The Crew: The Quest for Planet Nine project
# This class represents a played hand, not the hand of cards each player has.
# The Board Game Scholar Project 4
# Freddy Reiber

class Hand:

    # First Card Played needs to be in the init as it sets the suit for the hand
    def __init__(self, firstCardPlayed, player):
        # The list of all cards played in the hand
        self.cardsPlayed = [None] * 4
        self.cardsPlayed[player] = firstCardPlayed
        # The suit for the hand
        self.handSuit = firstCardPlayed.suit()
        # To lower the complexity of finding the winner,
        # We do the overhead during each addition of a card to the hand
        self.currentWinningCard = firstCardPlayed
        self.winningPlayer = 0

    def __repr__(self):
        return str(self.cardsPlayed) + " Winner - " + str(self.currentWinningCard)

    def playCard(self, newCard, player):
        self.cardsPlayed[player] = (newCard)
        if newCard.suit() == self.handSuit and newCard.value() > self.currentWinningCard.value():
            self.winningPlayer = len(self.cardsPlayed) - 1
            self.currentWinningCard = newCard
        if newCard.suit() == 'R':
            if self.currentWinningCard.suit() != 'R' or self.currentWinningCard.value() < newCard.value():
                self.winningPlayer = len(self.cardsPlayed) - 1
                self.currentWinningCard = newCard

    # Getters for important values
    def getSuit(self):
        return self.handSuit

    def getCardsPlayedInOrder(self):
        return self.cardsPlayed

    def getWinningCard(self):
        return self.currentWinningCard

    def getWinningPlayer(self):
        for i in range(4):
            if self.cardsPlayed[i] == self.currentWinningCard:
                return i
        return -1
