# Some relevant secret interactions:
# Freezing trap will prevent Misdirection
# Counterspell will prevent Spellbender
# Explosive and bear ?

# Deal with Kezan Mystic
# There's an inherent timing issue going on with secrets, I'm not sure how to deal with it apart from an 'end' trigger?

class secret():
    def __init__(self, id, hero):
        global turn
        self.turn = turn / 2
        if hero == 'MAGE':
            self.possibleValues = [
                'Counterspell',
                'Duplicate',
                'Effigy',
                'Ice Barrier',
                'Ice Block',
                'Mirror Entity',
                'Spellbender',
                'Vaporize'
            ]
        elif hero == 'HUNTER':
            self.possibleValues = [
                'Bear Trap',
                'Dart Trap',
                'Explosive Trap',
                'Freezing Trap',
                'Misdirection',
                'Snake Trap',
                'Snipe'
            ]
        elif hero == 'PALADIN':
            self.possibleValues = [
                'Avenge',
                'Competitive Spirit',
                'Eye for an Eye',
                'Noble Sacrifice',
                'Redemption',
                'Repentance',
                'Sacred Trial'
            ]
        else:
            raise Exception('Invalid hero')

def reset():
    global turn, secrets, wentFirst
    turn = 0
    secrets = []
    wentFirst = 0

reset()

def trigger(entity):
    if entity['player'] == them:
        secrets.pop(int(entity['zonePos']))

def play(entity, hero):
    if entity['player'] == them:
        secrets.append(secret(int(entity['id']), hero))

def turnover():
    global turn, secrets, wentFirst
    turn += 1
    if (turn+wentFirst)%2 == 0:
        if len(secrets) > 0:
            print 'Secret%s:' % ('' if len(secrets) == 1 else 's')
            for i in range(len(secrets)):
                print '%d: %s' % (i+1, secret.possibleValues)

''' Outdated:
    # An action happened which did not trigger the secret. Eliminate secrets that would've triggered.
    # Ice block is not handled because that's irrelevant.
def action(self, event):
    if event.owner != 'Us': # Secrets cannot trigger on their owner's turn. Competitive Spirit triggers on our turn end.
        return
    if event.kind == 'Attack':
        remove(self.possibleValues, ['Ice Barrier', 'Noble Sacrifice'])
        if event.target == 'Hero':
            remove(self.possibleValues, ['Bear Trap', 'Explosive Trap', 'Eye for an Eye', 'Misdirection'])
            if event.source != 'Hero':
                remove(self.possibleValues, ['Vaporize'])
        else:
            remove(self.possibleValues, ['Snake Trap'])
        if event.source != 'Hero':
            remove(self.possibleValues, ['Freezing Trap'])
    elif event.kind == 'Minion Died':
        remove(self.possibleValues, ['Avenge', 'Duplicate', 'Effigy', 'Redemption'])
    elif event.kind == 'Card Played' and event.source.isMinion():
        remove(self.possibleValues, ['Mirror Entity', 'Repentance', 'Snipe'])
        if event.minionCount() > 3:
            remove(self.possibleValues, ['Sacred Trial'])
    elif event.kind == 'Played Spell':
        remove(self.possibleValues, ['Counterspell'])
        if event.target:
            remove(self.possibleValues, ['Spellbender'])
    elif event.kind == 'Used Hero Power':
        remove(self.possibleValues, ['Dart Trap'])
    elif event.kind == 'Turn End': # And opp has creatures in play!
        remove(self.possibleValues, ['Competitive Spirit'])
    elif event.kind == 'Secret Triggered':
        remove(self.possibleValues, [event.args[0]])

'''


