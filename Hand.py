# Displaying with tk:
# Use Toplevel() in construction, and root.lift() as a backup

class card():
    def __init__(self, id, note=None, cost=0):
        global turn, notes
        self.id = id
        self.turn = turn/2
        if note:
            self.note = note
        elif len(notes) > 0:
            self.note = notes.pop() + ' '
        else:
            self.note = ''
        self.cost = cost

    def __repr__(self):
        params = ''
        if self.note:
            params += ', note=\'%s\'' % self.note
        if self.cost:
            params += ', cost=%d' % self.cost
        return 'card(%s%s)' % (self.id, params)

def reset():
    global turn, hand, notes, us, them, wentFirst
    turn = 0
    hand = []
    notes = [] # Push to this to signal information about the next draw.
    us = '0' # player id
    them = '0' # player id
    wentFirst = None

reset()

def wentFirstFunc(truth):
    global notes, hand, wentFirst
    if truth:
        notes = ['The Coin', 'Mulliganned', 'Mulliganned', 'Mulliganned', 'Mulliganned']
        hand = [card(-1) for _ in range(5)]
        wentFirst = True
    else:
        notes = ['Mulliganned', 'Mulliganned', 'Mulliganned']
        hand = [card(-1) for _ in range(3)]
        wentFirst = False

def draw(entity, position=None, note=None, cost=0):
    global hand, them
    if len(hand) == 10:
        return
    if entity['player'] == them:
        # Ovewriting a card because it was mulliganned
        if position and position < len(hand):
            hand[position].id = entity['id']
        else:
            hand.append(card(int(entity['id']), note=note, cost=cost))

# When a card is removed from a player's hand
def play(entity):
    global hand
    if entity['player'] == them:
        hand.pop(int(entity['zonePos'])-1)

def discard(entity):
    global hand
    if entity['player'] == them:
        hand.pop(int(entity['zonePos'])-1)
        
# The mulligan works backwards, with cards that are kept appearing in the log file. Thus I initialize the cards in hand to be 'Mulliganned', and replace them if they appear.
def keep(entity):
    global hand
    if entity['player'] == them:
        hand[int(entity['zonePos'])-1] = card(entity['id'])

# TODO: Delay going first until after mulligan resolves, since the mulligan labels are wrong
def turnover(turn):
    globals()['turn'] = turn # https://docs.python.org/2/library/functions.html#globals
    global hand
    offset = 1 if wentFirst else 0
    if turn%2 == offset:
        print 'Current Turn:', turn/2
        if len(hand) > 0:
            print 'Card No. | Turn | Notes'
        for i in range(len(hand)):
            print ' %s | %s | %s %s' % (
            ('%d' % (i+1)).ljust(7),
            ('%d' % hand[i].turn).ljust(4),
            hand[i].note,
            '' if hand[i].cost == 0 else 'cost %d' % hand[i].cost)
            # print ' %s | %s | %s' % ('%d'.ljust(8) % (i+1), '%d'.ljust(5) % hand[i].turn, ' %s' % hand[i].notes)
