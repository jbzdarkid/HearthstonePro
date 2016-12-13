# Contains a lot of one-offs that aren't easy to deal with.
import logging
import Hand
def reset():
    global overload, resources, combo, turn, turnOffset, us, them, numMinions
    overload = 0
    resources = '0' # Relevant for Wild Growth, which gives a card if at full.
    combo = False # Relevant for Rogues, where Combo can change how cards work
    turn = 0
    turnOffset = 0 # Only tell the user what's happening before their turn
    us = '0' # player id
    them = '0' # player id
    numMinions = 0

reset()

def ourTurn():
    global turn, turnOffset
    return (turn + 1*turnOffset)%2 == 0

def wentFirst(truth):
    global turnOffset
    if truth:
        logging.info("You are going first")
        Hand.hand = [Hand.card(-1, note='Mulliganned') for _ in range(4)] + [Hand.card(-1, note='The Coin')]
        turnOffset = 1
    else:
        logging.info("You are going second")
        Hand.hand = [Hand.card(-1, note='Mulliganned') for _ in range(3)]
        turnOffset = 0
