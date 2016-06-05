import Utilities

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
        # Ovewriting a card because it was mulliganned
        if position and position < len(hand):
            hand[position].id = entity['id']
        else:
            c = card(int(entity['id']))
            if note:
                c.note += note
            if Legendaries.varianWrynn and Utilities.numMinions != 7:
                c.note += ', Not a minion'
            if cost:
                c.cost += cost
            hand.append(c)

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
        hand[int(entity['zonePos'])-1] = card(entity['id'])

def turnover():
    global hand
    print 'Current Turn:', Utilities.turn/2
    if len(hand) > 0:
        print 'Card No. | Turn | Notes'
    for i in range(len(hand)):
        print ' %s | %s | %s %s' % (
        ('%d' % (i+1)).ljust(7),
        ('%d' % hand[i].turn).ljust(4),
        hand[i].note,
        '' if hand[i].cost == 0 else 'cost %d' % hand[i].cost)
        # print ' %s | %s | %s' % ('%d'.ljust(8) % (i+1), '%d'.ljust(5) % hand[i].turn, ' %s' % hand[i].notes)
