#!/usr/bin/env python

import betabrite
import time
import random

def main():
	s = betabrite.Sign( '/dev/ttyUSB0' )
	s.clearMem()

	imgw = 80
	imgh = 7
	framecount = 4
	
	mem = betabrite.Sign.MemConfig()
	frames = [ mem.pushSmalldots( imgw, imgh ) for i in xrange( framecount ) ]
	txtfile = mem.pushText( framecount * 10 )
	s.setupMem( mem )
	
	for f in frames:
		cut = set( random.sample( range( imgw ), imgw / 3 ) )
		img = [ ''.join( random.choice( '005' if col not in cut else '0' ) for col in xrange( imgw ) ) for row in xrange( imgh ) ]
		s.sendSmalldots( f, img )
	
	txt = betabrite.encodeText('<fastest>')
	for f in frames[ 3:4 ]:
		txt += betabrite.encodeText('<smalldots>{0}'.format( f ))
	print ' '.join( '{0:02X}'.format(ord(c)) for c in txt )
	#print betabrite.encodeText( txt )
	s.sendText( txtfile, txt, betabrite.MODE_ROLLDOWN )
	
	s.setSequence( txtfile )

	return 0

if __name__ == '__main__': main()
