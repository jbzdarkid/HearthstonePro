import logging
import Utilities, Legendaries

class card():
    def __init__(self, id, note=None):
        global notes
        self.id = id
        self.turn = Utilities.turn/2
        if note:
            self.note = note
        elif len(notes) > 0:
            self.note = notes.pop()
        else:
            self.note = ''
        self.cost = 0

    def __repr__(self): # pragma: no cover
        params = ''
        if self.note:
            params += ', note=\'%s\'' % self.note
        if self.cost:
            params += ', cost=%d' % self.cost
        return 'card(%s%s)' % (self.id, params)

def reset():
    logging.debug('Resetting hand')
    global hand, notes
    hand = []
    notes = [] # Push to this to signal information about the next draw.
    # N.B. notes is only used for Far Sight, at present. Other cards do affect it though.

reset()

def draw(entity, position=None, note=None, cost=None):
    global hand
    if len(hand) == 10:
        return
    if entity['player'] == Utilities.them:
        if position and position < len(hand):
            logging.info('Opponent mulligans card #%d' % position)
            hand[position].id = entity['id']
        else:
            logging.info('Opponent draws a card (id %s)' % entity['id'])
            c = card(int(entity['id']))
            if note:
                c.note += note
            if Legendaries.varianWrynn and Utilities.numMinions != 7:
                if note:
                    c.note += ', '
                c.note += 'Not a minion'
            if cost:
                c.cost += cost
            hand.append(c)
            logging.debug('Hand after draw: ' + str(hand))

# When a card is removed from a player's hand
def play(entity):
    global hand
    if entity['player'] == Utilities.them:
        logging.info('Opponent plays card #%d' % (int(entity['zonePos'])-1))
        hand.pop(int(entity['zonePos'])-1)

def discard(entity):
    global hand
    if entity['player'] == Utilities.them:
        logging.info('Opponent discards card #%d' % (int(entity['zonePos'])-1))
        hand.pop(int(entity['zonePos'])-1)

# The mulligan works backwards, with cards that are kept appearing in the log file. Thus I initialize the cards in hand to be 'Mulliganned', and replace them if they appear.
def keep(entity):
    global hand
    if entity['player'] == Utilities.them:
        logging.info('Opponent keeps card #%d' % (int(entity['zonePos'])-1))
        hand[int(entity['zonePos'])-1] = card(entity['id'])

def turnover():
    global hand
    logging.warning('Current Turn: %d' % (Utilities.turn//2))
    if len(hand) > 0:
        logging.warning('Card No. | Turn | Notes')
    for i in range(len(hand)):
        logging.warning(' %s | %s | %s %s' % (
        ('%d' % (i+1)).ljust(7),
        ('%d' % hand[i].turn).ljust(4),
        hand[i].note,
        '' if hand[i].cost == 0 else 'cost %d' % hand[i].cost))
