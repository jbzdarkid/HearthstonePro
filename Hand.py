import logging
import Utilities, Legendaries

# There's a few things to do about dragons.
# 1. When a card is played that has a triggered effect, >= 1 card in hand must be a dragon.
# 1a. If (at some later date) a card is played from that set which is a dragon, no information is known about the remaining cards.
# 1b. If (at some later date) all cards but one are played from that set and are not dragons, then the remaining card is a dragon.
# 1c. Info from 1b. may be relevant with 2 cards remaining.
# 2. When a card is played that fails to have a triggered effect, 0 cards in hand are dragons.
# 2a. If (at some later date) a card is played which does have a triggered effect, these cards are excluded from the set.
# 3. If a card which is not a dragon is returned to hand, we know that it still isn't a dragon.

# So, each card needs a dragonSets and a notDragon field.
# When a card is played and it fails to have a triggered effect, all cards in the hand set notDragon=True and dragonSets=[].
# When a card is played and has a triggered effect, all cards in the hand with notDragon=False have dragonSets.append(newSet)
# When a card is played and it's a dragon, for each set it's a part of, all cards in hand have dragonSets.remove(set). If the sets becomes empty, this DOES NOT mean the card isn't a dragon.
# Each printout, any sets with 2 or 1 members should be mentioned.

class card():
    def __init__(self, note='', cost=0, source='', hero='', kind='', buff=0):
        global notes
        self.turn = Utilities.turn/2
        self.note = note
        if len(notes) > 0:
            self.note += ' '+notes.pop()
        self.cost = cost # Cost modifier for freezing trap / thaurissan
        self.hero = hero
        self.source = source
        self.kind = kind # minion, spell, weapon
        self.buff = buff # +1/+1, e.g.
        self.isDragon = False

    def __str__(self):
        description = ''
        if self.note != '':
            description += self.note
        else:
            description += 'A'
            if self.source != '':
                description += ' ' + self.source
            if self.hero != '':
                description += ' ' + self.hero
            if self.kind != '':
                description += ' ' + self.kind
            else:
                description += ' card'
        if self.buff != 0:
            description += ' with +%d/+%d' % (self.buff, self.buff)
        if self.cost > 0:
            description += ' which costs %d more' % self.cost
        elif self.cost < 0:
            description += ' which costs %d less' % self.cost
        return description

def reset():
    logging.debug('Resetting hand')
    global hand, notes
    hand = []
    notes = [] # Push to this to signal information about the next draw.
    # N.B. notes is only used for Far Sight, at present. Other cards do affect it though.

reset()

def draw(entity=None, position=None, **kwargs):
    global hand
    new_card = None
    if entity == None: # Passed from Cards.py, probably
        new_card = card(**kwargs)
    elif entity['player'] == Utilities.them:
        if len(hand) == 10:
            logging.info('Opponent drew a card with 10 cards in hand')
            return
        if position is None or position >= len(hand): # A card was drawn
            new_card = card()
            if Legendaries.varianWrynn and Utilities.numMinions != 7:
                new_card.kind = 'Spell or Weapon'
    if new_card:
        hand.append(new_card)
        logging.info('Opponent draws %s' % new_card)
        logging.info('Cards in hand: %d' % len(hand))
        logging.debug('Hand after draw: '+'|'.join([str(c) for c in hand]))

# When a card is removed from a player's hand
def play(entity):
    global hand
    if entity['player'] == Utilities.them:
        hand.pop(int(entity['zonePos'])-1)

def discard(entity):
    global hand
    if entity['player'] == Utilities.them:
        hand.pop(int(entity['zonePos'])-1)

# The mulligan works backwards, with cards that are kept appearing in the log file. Thus I initialize the cards in hand to be 'Mulliganned', and replace them if they appear.
def keep(entity):
    global hand
    if entity['player'] == Utilities.them:
        logging.info('Opponent keeps card #%d' % int(entity['zonePos']))
        hand[int(entity['zonePos'])-1] = card()

def turnover():
    global hand
    logging.warning('Current Turn: %d' % (Utilities.turn//2))
    if len(hand) > 0:
        logging.warning('Card No. | Turn | Notes')
    for i in range(len(hand)):
        logging.warning(' %s | %s | %s %s' % (
        ('%d' % (i+1)).ljust(7),
        ('%d' % hand[i].turn).ljust(4),
        '' if str(hand[i]) == 'A card' else hand[i],
        '' if hand[i].cost == 0 else 'cost %d' % hand[i].cost))
