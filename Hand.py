import logging
import Utilities, Legendaries, Dragons

class card():
    def __init__(self, note='', cost=0, source='', hero='', kind='', buff=0):
        global notes
        self.turn = Utilities.turn/2
        self.note = note
        if len(notes) > 0:
            self.note = (self.note+' '+notes.pop()).strip()
        self.cost = cost # Cost modifier for freezing trap / thaurissan
        self.hero = hero
        self.source = source
        self.kind = kind # minion, spell, weapon
        if self.note in Dragons.DRAGONS:
            self.kind = 'dragon minion'
        self.buff = buff # +1/+1, e.g.

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
    if entity == None: # Passed from Cards.py
        new_card = card(**kwargs)
    elif entity['player'] == Utilities.them:
        new_card = card()
        if Legendaries.varianWrynn and Utilities.numMinions != 7:
            new_card.kind = 'Spell or Weapon'
    else: # We drew a card, nobody cares
        return
    if position is not None and position < len(hand):
        return # A replacement card (for any reason)
    if len(hand) == 10:
        logging.info('Opponent drew a card with 10 cards in hand')
        return
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
        logging.warning(' %s | %s | %s' % (
        ('%d' % (i+1)).ljust(7),
        ('%d' % hand[i].turn).ljust(4),
        '' if str(hand[i]) == 'A card' else hand[i]))
