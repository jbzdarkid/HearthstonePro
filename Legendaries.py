# Contains more long-term tracking cards.

def reset():
    global reno, renoDuplicates, cthun, nzoth, yogg, varianWrynn
    reno = []
    renoDuplicates = 0
    cthun = 6
    nzoth = []
    yogg = 0
    varianWrynn = False # Start of a Varian Wrynn block, where minions are put directly into play.

reset()

def blockEnd():
    global varianWrynn
    varianWrynn = False

def die(entity):
    global nzoth
    # Hard-code a list of deathrattle creatures
    nzoth.append(entity['name'])

def play2(entity):
    global cthun, yogg, reno, renoDuplicates
    # Verify that this card was actually played by the opponent
    if entity['name'] in reno:
        renoDuplicates += 1
    reno.append(entity['name'])

def turnover():
    pass
    # print 'Reno: %d duplicates, C'Thun: %d/%d, Yogg-Saron: %d spells\nN'Zoth: %s' % (renoDuplicates, cthun, cthun, yogg, ', '.join(nzoth))
