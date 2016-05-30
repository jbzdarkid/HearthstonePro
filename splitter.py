if __name__ == '__main__': # pragma: no cover
    from os import listdir, sep
    from json import load
    rootDir = __file__.rpartition(sep)[0]
    # If rootDir is nothing, then ''+'/' = '/', which is not the current directory.
    if rootDir:
        rootDir += sep
    config = load(open(rootDir+'config.cfg'))
    cardspy = open(rootDir+'Cards.py', 'rb').read()
    for file in listdir(rootDir+'tests'):
        if file[-4:] != '.log':
            continue
        buffer = ''
        cards = set()
        j = 0
        with open(rootDir+'tests'+sep+file, 'rb') as f:
            data = f.read().split('\n')
            for i in range(len(data)):
                if 'PowerTaskList.DebugPrintPower() -     TAG_CHANGE Entity=GameEntity tag=STEP value=FINAL_GAMEOVER' in data[i]:
                    with open(rootDir+'tests'+sep+file+'-%d' % j, 'wb') as g:
                        g.write(buffer)
                        print 'Cards used in %s-%d:' % (file, j)
                        for card in sorted(list(cards)):
                            if '%s' % card in cardspy:
                                print '    *', card
                            else:
                                print '\t', card
                        j += 1
                        buffer = ''
                        cards = set()
                else:
                    buffer += '\n'+data[i]
                    if 'PLAYER_ID' in data[i] and 'GameState.DebugPrintPower()' in data[i]:
                        if config['username'] not in data[i]:
                            them = data[i][-2]
                    if 'Entity=[name=' in data[i] and 'player='+them in data[i]:
                        cards.add(data[i].split('name=', 1)[1].split('=', 1)[0][:-3])
        raw_input()
