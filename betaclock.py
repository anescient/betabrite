#!/usr/bin/env python

import betabrite


def main():
    s = betabrite.Sign('/dev/ttyUSB0')
    s.clearMem()
    s.setClock()
    print s.getClock()
    s.sendTextPriority(betabrite.encodeText('<slowest><dimred><7bold><clock>'))
    return 0

if __name__ == '__main__':
    main()
