if __name__ == '__main__': # pragma: no cover
    from os import listdir, sep
    from json import load
    from sys import argv
    rootDir = __file__.rpartition(sep)[0]
    # If rootDir is nothing, then ''+'/' = '/', which is not the current directory.
    if rootDir:
        rootDir += sep
    if len(argv) == 1 or argv[1] == 'all':
        files = listdir(rootDir+'tests')
    elif argv[1] == 'import': # pragma: no cover
        config = load(open(rootDir+sep+'config.cfg'))
        files = [config['log']]
    elif len(argv) > 1:
        files = argv[1:]
    config = load(open(rootDir+'config.cfg'))
    card_list = open(rootDir+'Cards.py', 'rb').read()
    card_list += open(rootDir+'Dragons.py', 'rb').read()
    for file in files:
        if file[-4:] != '.log':
            continue
        buffer = ''
        cards = set()
        spectating = False
        with open(rootDir+'tests'+sep+file, 'rb') as f:
            for line in f:
                buffer += line
                if line[19:54] == '================== Begin Spectating':
                    spectating = True
                elif line[19:75] == '================== End Spectator Mode ==================':
                    spectating = False
                elif spectating:
                    continue
                if line[19:115] == 'PowerTaskList.DebugPrintPower() -     TAG_CHANGE Entity=GameEntity tag=STEP value=FINAL_GAMEOVER':
                    name = ', '.join(sorted(cards))
                    with open(rootDir+'tests'+sep+name+'.log', 'wb') as g:
                        g.write(buffer)
                    buffer = ''
                    cards = set()
                elif 'ChoiceType=MULLIGAN' in line and config['username'] in line.decode('utf-8'):
                    us = line[60]
                elif 'Entity=[name=' in line and 'player='+us not in line:
                    card = line.split('=')[3][:-3]
                    if '"'+card+'"' in card_list:
                        cards.add(card)
