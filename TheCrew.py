# This is the main class for The Crew: The Quest for Planet Nine project
# This project focuses on generating a valid series of plays that will complete all of the objectives
# Board Game Scholar Post 4
# Freddy Reiber


# Notes
# Avg High Card = 6.7

# TODO - Main focus is on finding solutions that require a deeper search, and heuristics for the objective draft.

from Card import Card
from Objective import Objective
from Hand import Hand
from ObjectiveNetwork import TaskNetwork

import random

# B = Blue, P = Pink, G = Green, Y = Yellow, 'R' = Rocket
listOfALlColors = ['B', 'P', 'G', 'Y']
listOfAllValues = [1, 2, 3, 4, 5, 6, 7, 8, 9]


# This generates a list of a cards
def generateAllCards():
    listOfAllCards = []
    for color in listOfALlColors:
        for value in listOfAllValues:
            listOfAllCards.append(Card(color, value))
    for value in range(1, 5):
        listOfAllCards.append(Card('R', value))
    return listOfAllCards


# This will just generate objectives equal to numberOfObjectives without any special conditions
def generateObjective(numberOfObjectives):
    objectiveList = []
    counter = 0
    while len(objectiveList) < numberOfObjectives:
        newObjective = Objective()
        possible = True
        for objective in objectiveList:
            if objective == newObjective:
                possible = False
        if possible:
            objectiveList.append(newObjective)
    return objectiveList


# B, P, G, Y
def dealCards():
    allCards = generateAllCards()
    random.shuffle(allCards)
    playerHands = {0: [], 1: [], 2: [], 3: []}
    counter = 0
    for card in allCards:
        playerHands[counter % 4].append(card)
        counter += 1
    return playerHands


def setCardCritical(playerHands, criticalCard):
    for player in playerHands:
        for card in playerHands[player]:
            if card.__repr__() == criticalCard:
                card.setCritical(True)


def handCompletesObjective(hand, objective):
    if objective.player == hand.getWinningPlayer():
        for card in hand.getCardsPlayedInOrder():
            if card.suit() == objective.suit() and card.value() == objective.value():
                return True
    return False


def checkIfAllSameSuit(possiblePlays):
    checkSuit = None
    for card in possiblePlays:
        if checkSuit is None:
            checkSuit = card.suit()
        if checkSuit != card.suit():
            return False
    return True


def getPossiblePlays(playerHand, objective):
    possiblePlays = []
    for card in playerHand:
        if card.suit() == objective.suit():
            possiblePlays.append(card)
    if not possiblePlays:
        for card in playerHand:
            possiblePlays.append(card)
    # Not ideal, but due to such a small calculation size, it doesn't really matter
    for play in possiblePlays:
        if play.isCritical():
            canPlay = False
            for card in objective.criticalCards:
                if play == card:
                    canPlay = True
            if not canPlay:
                possiblePlays.remove(play)
    return possiblePlays


# The players need to be ordered in play order
def generateAllPossibleHands(possiblePlays, currentLeader):
    possibleHands = []
    for play in possiblePlays[currentLeader]:
        for play1 in possiblePlays[(currentLeader + 1) % 4]:
            for play2 in possiblePlays[(currentLeader + 2) % 4]:
                for play3 in possiblePlays[(currentLeader + 3) % 4]:
                    newHand = Hand(play, currentLeader)
                    newHand.playCard(play1, (currentLeader + 1) % 4)
                    newHand.playCard(play2, (currentLeader + 2) % 4)
                    newHand.playCard(play3, (currentLeader + 3) % 4)
                    possibleHands.append(newHand)
    return possibleHands


def findHighestCardOfSuit(playerHand, suit):
    currentBestCard = None
    for card in playerHand:
        if card.suit() == suit:
            if currentBestCard is None:
                currentBestCard = card
            else:
                if card.value() > currentBestCard.value():
                    currentBestCard = card
    return currentBestCard


def generateHandsForObjective(playerHands, objective, currentLeader):
    possiblePlays = []
    for i in range(4):
        possiblePlays.append(getPossiblePlays(playerHands[i], objective))
    possibleHands = generateAllPossibleHands(possiblePlays, currentLeader)
    return possibleHands


def findCardsOwner(cardToFind, playerHands):
    for player in playerHands:
        for card in playerHands[player]:
            if card == cardToFind:
                return player
    return -1


def playerCanWinObjective(player: int, objective, playerHands):
    cardOwner = findCardsOwner(objective.getCard(), playerHands)
    possibleHands = generateHandsForObjective(playerHands, objective, cardOwner)
    objective.setPlayer(player)
    for hand in possibleHands:
        if handCompletesObjective(hand, objective):
            objective.setPlayer(None)
            return True, hand.getWinningCard()
    objective.setPlayer(None)
    return False, None


def handleObjectiveDraft(playerHands, objectives, objectivePairing):
    criticalCards = []
    for i in range(len(objectivePairing)):
        objectives[i].setPlayer(objectivePairing[i][0])
        objectives[i].addCriticalCards(objectivePairing[i][1])
        criticalCards.append(objectivePairing[i][1].__repr__())
        criticalCards.append(objectives[i].getCard())

    for card in criticalCards:
        setCardCritical(playerHands, card)


def undoObjectiveDraft(playerHands, objectives):
    for player in playerHands:
        for card in playerHands[player]:
            card.setCritical(False)
    for objective in objectives:
        objective.setPlayer(None)
        objective.clearCriticalCards()


# Generates all valid pairing.
def validValueParing(pairingDictionary, objectiveList):
    pairs = []
    validParing = []
    objectiveCardList = []
    for objective in objectiveList:
        objectiveCardList.append(objective.getCard())

    def buildPairs(pairingDict, key, currentPair):
        if key >= len(pairingDict):
            pairs.append(currentPair[:])
            return
        for value in pairingDict[key]:
            currentPair.append(value)
            buildPairs(pairingDict, key + 1, currentPair)
            currentPair.pop()

    buildPairs(pairingDictionary, 0, list())

    def checkPairs(pair):
        criticalCards = []
        playerObjectives = {0: 0, 1: 0, 2: 0, 3: 0}
        counter1 = 0
        for item in pair:
            if item[1] in criticalCards:
                return False
            counter2 = 0
            for card in objectiveCardList:
                if card == item[1] and counter1 != counter2:
                    return False
                counter2 += 1
            else:
                criticalCards.append(item[1])
                playerObjectives[item[0]] += 1
            counter1 += 1
        for i in range(len(pair)):
            playerObjectives[i % 4] -= 1
        for i in playerObjectives:
            if playerObjectives[i] != 0:
                return False
        return True

    for pair in pairs:
        if checkPairs(pair):
            validParing.append(pair)
    if len(validParing) == 0:
        return False
    return validParing


def objectiveDraft(playerHands, objectives):
    # Setting initial values for objective draft
    playersNeedingObjectives = []
    objectiveDict = {}
    for i in range(len(objectives)):
        objectiveDict[i] = []

    # Main Draft loop. Finds if players can win a hand in a single line of play
    for playerInt in range(4):
        assigned = False
        for i in range(len(objectives)):
            if objectives[i].player is not None:
                continue
            canWin, criticalCard = playerCanWinObjective(playerInt % 4, objectives[i], playerHands)
            if canWin:
                objectiveDict[i].append((playerInt, criticalCard))

    objectivePairing = validValueParing(objectiveDict, objectives)
    # TODO - add a system for pairing objectives that don't have a way to win in a single hand.
    if not objectivePairing:
        print("No Valid Objective Pairing")
        quit()

    return objectivePairing


def playHand(playerHands, objective, currentLeader):
    handsToCheck = []
    # print(playerHands)
    # print(objective)
    # This generates all possible starts to hand:
    possiblePlays = {currentLeader: getPossiblePlays(playerHands[currentLeader], objective)}
    # If we can match a suit on the objective, we will try and find a solution to it with the playing on one hand.:
    if checkIfAllSameSuit(possiblePlays[currentLeader]):
        for i in range(1, 4):
            possiblePlays[(currentLeader + i) % 4] = getPossiblePlays(playerHands[(currentLeader + i) % 4], objective)
        # Generates all possible hands and looks to find if one of them completes the objective
        possibleHands = generateAllPossibleHands(possiblePlays, currentLeader)
        for hand in possibleHands:
            if handCompletesObjective(hand, objective):
                handsToCheck.append(hand)
    # TODO implement a system for finding solutions for objectives that may take more than one play.
    if len(handsToCheck) == 0:
        return False
    return handsToCheck


# Add and remove cards from hands
def removePlayedCards(playerHands, playedHand):
    playedCards = playedHand.getCardsPlayedInOrder()
    playerI = 0
    for card in playedCards:
        playerHands[playerI].remove(card)
        playerI += 1


def addPlayedCards(playerHands, playedHand):
    playedCards = playedHand.getCardsPlayedInOrder()
    playerI = 0
    for card in playedCards:
        playerHands[playerI].append(card)
        playerI += 1


# Main Game Loop
def findSolution(playerHands=None, objectives=None):
    # Setting up initial values
    if not playerHands:
        playerHands = dealCards()
    if isinstance(objectives, int):
        objectives = generateObjective(objectives)
    elif not objectives:
        objectives = generateObjective(3)
    # Setting up the objectives for play
    print("Player Hands - " + str(playerHands))
    print("Objectives - " + str(objectives))
    possiblePairings = objectiveDraft(playerHands, objectives)
    for pairing in possiblePairings:
        handleObjectiveDraft(playerHands, objectives, pairing)
        objectiveNetwork = TaskNetwork()
        for objective in objectives:
            if not objective.isComplete():
                objectiveNetwork.addTask(objective)

        solution = []

        def findValidPlays(playerHands, currentLeader):
            if objectiveNetwork.isComplete():
                return True
            for objective in objectiveNetwork.getPossibleTasks():
                checkHand = playHand(playerHands, objective, currentLeader)
                if not checkHand:
                    continue
                for hand in checkHand:
                    objective.setComplete(True)
                    removePlayedCards(playerHands, hand)
                    handLeader = hand.getWinningPlayer()
                    if findValidPlays(playerHands, handLeader):
                        solution.append(hand)
                        return True
                    else:
                        objective.setComplete(False)
                        addPlayedCards(playerHands, hand)
            return False

        check = findValidPlays(playerHands, 0)
        if not check:
            undoObjectiveDraft(playerHands, objectives)
            continue
        else:
            return solution
    return "No Solution Found"


# This is the main handler
if __name__ == "__main__":
    objectiveValue = int(input("How many objectives do you want to generate"))
    print(findSolution(None, objectiveValue))


# Code used for debugging issues
# playerDict = {0: [], 1: [], 2: [], 3: []}
# p0 = ['G4', 'P1', 'B9', 'P2', 'R2', 'P3', 'R1', 'B8', 'P8', 'B2']
# p1 = ['R4', 'G5', 'G9', 'Y6', 'B3', 'Y3', 'G2', 'Y2', 'P4', 'B7']
# p2 = ['B6', 'R3', 'G7', 'Y7', 'G3', 'Y5', 'Y1', 'G1', 'B4', 'B1']
# p3 = ['P9', 'Y4', 'P5', 'G8', 'Y8', 'G6', 'Y9', 'P6', 'P7', 'B5']
# for item in p0:
#     newCard = Card(item[0], int(item[1]))
#     playerDict[0].append(newCard)
# for item in p1:
#     newCard = Card(item[0], int(item[1]))
#     playerDict[1].append(newCard)
# for item in p2:
#     newCard = Card(item[0], int(item[1]))
#     playerDict[2].append(newCard)
# for item in p3:
#     newCard = Card(item[0], int(item[1]))
#     playerDict[3].append(newCard)
# obj1 = Objective(0, None, 'P', 7)
# obj2 = Objective(0, None, 'B', 6)
# obj3 = Objective(0, None, 'B', 2)
# obj4 = Objective(0, None, 'Y', 7)
# objectives = [obj1, obj2, obj3]
