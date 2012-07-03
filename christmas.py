#!/usr/bin/env python

import AlphaSign
import time
import random

def main():
	s = AlphaSign.Sign( '/dev/ttyUSB0' )
	s.clearMem()
	
	tree = [
	'000080000',
	'005555500',
	'000555000',
	'055455550',
	'005554500',
	'555555555',
	'000666000'
	]
	tree2 = [
	'000060000',
	'005555500',
	'000555000',
	'055455550',
	'005554500',
	'555555555',
	'000666000'
	]
	holly = [
	'00005000000000000',
	'00505550440050500',
	'05555500440555550',
	'55555000005555555',
	'05050004455555500',
	'00000004400505000',
	'00000000000000000'
	]
	wreath = [
	'000555050',
	'505555500',
	'055005550',
	'055000550',
	'055500550',
	'005555505',
	'050555000'
	]
	
	mem = AlphaSign.Sign.MemConfig()
	treefile = mem.pushSmalldots( len(tree[0]), len(tree) )
	#tree2file = mem.pushSmalldots( len(tree2[0]), len(tree2) )
	hollyfile = mem.pushSmalldots( len(holly[0]), len(holly) )
	wreathfile = mem.pushSmalldots( len(wreath[0]), len(wreath) )
	print wreathfile
	frame1 = mem.pushText()
	#frame2 = mem.pushText()
	s.setupMem( mem )
	
	s.sendSmalldots( treefile, tree )
	#s.sendSmalldots( tree2file, tree2 )
	s.sendSmalldots( hollyfile, holly )
	s.sendSmalldots( wreathfile, wreath )
	#s.sendText( frame1, AlphaSign.encodeText( '<fastest><smalldots>{0} <smalldots>{1} <smalldots>{2}'.format(treefile,hollyfile,wreathfile) ) )
	s.sendText( frame1, AlphaSign.encodeText( '<smalldots>{0}'.format(wreathfile) ) )
	#s.sendText( frame2, AlphaSign.encodeText( ' '.join( ['<fastest><smalldots>{0} <smalldots>{1}'.format(tree2file,hollyfile)] * 2 ) ) )
	s.setSequence( frame1 )
	#s.setSequence( frame1 + frame2 )
	
	print s.getSmalldots( wreathfile )
	
	return 0

if __name__ == '__main__': main()
