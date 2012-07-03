#!/usr/bin/env python

import AlphaSign

def main ():
	s = AlphaSign.Sign( '/dev/ttyUSB0' )
	s.clearMem()
	s.setClock()
	print s.getClock()
	s.sendTextPriority( AlphaSign.encodeText( '<slowest><dimred><5><clock>' ) )
	return 0

if __name__ == '__main__': main()
