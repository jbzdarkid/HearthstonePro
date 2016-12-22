# Contains a lot of one-offs that aren't easy to deal with.
import logging
import Hand
HEROS = {
    'HERO_01':  'warrior', # Garrosh Hellscream
    'HERO_01a': 'warrior', # Magni Bronzebeard
    'HERO_02':  'shaman',  # Thrall
    'HERO_02a': 'shaman',  # Morgl the Oracle
    'HERO_03':  'rogue',   # Valeera Sanguinar
    'HERO_04':  'paladin', # Uther Lightbringer
    'HERO_04a': 'paladin', # Lady Liadrin
    'HERO_05':  'hunter',  # Rexxar
    'HERO_05a': 'hunter',  # Alleria Windrunner
    'HERO_06':  'druid',   # Malfurian Stormrage
    'HERO_07':  'warlock', # Gul'dan
    'HERO_08':  'mage',    # Jaina Proudmoore
    'HERO_08a': 'mage',    # Medivh
    'HERO_08b': 'mage',    # Khadgar
    'HERO_09':  'priest',  # Anduin Wrynn
    'HERO_09a': 'priest',  # Tyrande Whisperwind
    
    'BRM_027h': 'ragnaros', # Majordomo Executus
    'EX1_323':  'warlock', # Lord Jaraxxus
}
    
def reset():
    global overload, resources, combo, turn, turnOffset, us, them, numMinions, our_hero, their_hero
    overload = 0
    resources = '0' # Relevant for Wild Growth, which gives a card if at full.
    combo = False # Relevant for Rogues, where Combo can change how cards work
    turn = 0
    turnOffset = 0 # Only tell the user what's happening before their turn
    us = '0' # player id
    them = '0' # player id
    numMinions = 0
    our_hero = None
    their_hero = None

reset()

def set_hero(entity):
    global our_hero, their_hero
    try: # Can be called incorrectly, so watch out for invalid heros
        if entity['player'] == us:
            our_hero = HEROS[entity['cardId']]
        else:
            their_hero = HEROS[entity['cardId']]
    except KeyError:
        pass

def ourTurn():
    global turn, turnOffset
    return (turn + 1*turnOffset)%2 == 0

def wentFirst(truth):
    global turnOffset
    if truth:
        logging.warning("You are going first")
        Hand.hand = [Hand.card('Mulliganned') for _ in range(4)] + [Hand.card('The Coin')]
        turnOffset = 1
    else:
        logging.warning("You are going second")
        Hand.hand = [Hand.card('Mulliganned') for _ in range(3)]
        turnOffset = 0
