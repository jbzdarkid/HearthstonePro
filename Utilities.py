# Contains a lot of one-offs that aren't easy to deal with.

import Hand
def reset():
    global overload, resources, combo, numMinions, turn, turnOffset, us, them, varianWrynn
    overload = 0
    resources = '0' # Relevant for Wild Growth, which gives a card if at full.
    combo = False # Relevant for Rogues, where Combo can change how cards work
    turn = 0
    turnOffset = None # Only tell the user what's happening before their turn
    us = '0' # player id
    them = '0' # player id

reset()


def wentFirst(truth):
    global turnOffset
    if truth:
        Hand.hand = [Hand.card(-1, note='The Coin')]+[Hand.card(-1, note='Mulliganned') for _ in range(4)]
        turnOffset = 1
    else:
        Hand.hand = [Hand.card(-1, note='Mulliganned') for _ in range(3)]
        turnOffset = 0
