if __name__ == '__main__': # pragma: no cover
    from os import listdir, sep
    from json import load
    from sys import argv
    rootDir = __file__.rpartition(sep)[0]
    # If rootDir is nothing, then ''+'/' = '/', which is not the current directory.
    if rootDir:
        rootDir += sep
    if len(argv) == 1 or argv[1] == 'all':
        from os import listdir
        files = listdir(rootDir+'tests')
    # elif argv[1] == 'latest':
    #   from os.path import getmtime
    elif len(argv) > 1:
        files = argv[1:]
    config = load(open(rootDir+'config.cfg'))
    cardspy = open(rootDir+'Cards.py', 'rb').read()
    for file in files:
        if file[-4:] != '.log':
            continue
        buffer = ''
        cards = set()
        with open(rootDir+'tests'+sep+file, 'rb') as f:
            data = f.read().split('\n')
            for i in range(len(data)):
                buffer += '\n'+data[i]
                if 'PowerTaskList.DebugPrintPower() -     TAG_CHANGE Entity=GameEntity tag=STEP value=FINAL_GAMEOVER' in data[i]:
                    if len(cards) == 0:
                        break
                    name = ', '.join(sorted(cards))
                    with open(rootDir+'tests'+sep+name+'.log', 'wb') as g:
                        g.write(buffer)
                    buffer = ''
                    cards = set()
                else:
                    if 'PLAYER_ID' in data[i] and 'GameState.DebugPrintPower()' in data[i]:
                        if config['username'] in data[i]:
                            us = data[i][-2]
                    if 'Entity=[name=' in data[i] and 'player='+us not in data[i]:
                        card = data[i].split('name=', 1)[1].split('=', 1)[0][:-3]
                        if '"'+card+'"' in cardspy:
                            cards.add(card)
