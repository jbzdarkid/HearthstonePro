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
    if entity['name'] in [
        'Abomination', 'Anomalus', 'Anub\'ar Ambusher', 'Anub\'arak', 'Anubisath Sentinel',
        'Bloodmage Thalnos', 'Boom Bot',
        'Cairne Bloodhoof', 'Chillmaw', 'Clockwork Gnome', 'Corrupted Healbot',
        'Dancing Swords', 'Dark Cultist', 'Darkshire Librarian', 'Darnassus Aspirant', 'Deathlord', 'Deathwing, Dragonlord', 'Dreadsteed',
        'Explosive Sheep',
        'Feugen', 'Fiery Bat',
        'Harvest Golem', 'Haunted Creeper', 'Huge Toad',
        'Infested Tauren', 'Infested Wolf',
        'Leper Gnome', 'Loot Hoarder',
        'Mad Scientist', 'Majordomo Executus', 'Malorne', 'Mechanical Yeti', 'Mounted Raptor',
        'Nerubain Egg',
        'Piloted Shredder', 'Piloted Sky Golem', 'Polluted Hoarder', 'Possessed Villager',
        'Rhonin',
        'Savannah Highmane', 'Selfless Hero', 'Shifting Shade', 'Sludge Belcher', 'Sneed\'s Old Shredder', 'Southsea Squidface', 'Spawn of N\'Zoth', 'Stalagg', 'Sylvannas Windrunner',
        'Tentacle of N\'Zoth', 'The Beast', 'The Skeleton Knight', 'Tirion Fordring', 'Tomb Pillager', 'Toshley', 'Twilight Summoner',
        'Undercity Huckster', 'Unstable Ghoul',
        'Voidcaller',
        'Webspinner', 'Wobbling Runts',
        'Xaril, Poisoned Mind',
        'Zealous Initiate', 'Zombie Chow'
    ]:
        global nzoth
        if entity['player'] == Utilities.them:
            nzoth[0].append(entity['name'])
        elif entity['player'] == Utilities.us:
            nzoth[1].append(entity['name'])

def play2(entity):
    global cthun, yogg, reno, renoDuplicates
    # Verify that this card was actually from opp's deck, not generated
    if entity['name'] in reno:
        renoDuplicates.append(entity['name'])
    reno.append(entity['name'])

def turnover():
    pass
    # print 'Reno: %s, C'Thun: %d/%d, Yogg-Saron: %d spells\nN'Zoth: %s' % (', '.join(sorted(renoDuplicates)), cthun, cthun, yogg, ', '.join(sorted(nzoth)))
