#!/usr/bin/env python
#
#       totalbar.py
#       
#       Copyright 2008 anescient <anescient@bolysk>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.

import alphasign
import time
import cpustat


class TotalBar:

	sign = 0 # alphasign.AlphaSign()
	code = alphasign.AlphaCode()
	cpustat = cpustat.cpuStat()
	barstring = " "
	holdtxtlabel = ''
	centertxtlabel = ''
	wipetxtlabel = ''
	stringlabel = ''
	style = 0


	def __init__ ( self, comport = '' ):
		if len( comport ) > 0:
			self.sign = alphasign.AlphaSign( comport )
		else:
			self.sign = alphasign.AlphaSign()
		self.sign.clearMem()
		
		memconfig = alphasign.AlphaMemSetup()
		self.lefttxtlabel = memconfig.pushTextFile( 16 )
		self.centertxtlabel = memconfig.pushTextFile( 16 )
		self.wipetxtlabel = memconfig.pushTextFile( 16 )
		self.stringlabel = memconfig.pushStringFile( 72 )
		self.sign.setupMem( memconfig )
		
		base = self.code.Color(3) + self.code.Font(2) + self.code.ALPHA_NOHOLD
		fixed = self.code.ALPHA_FIXLEFT
		stringcall = self.code.ALPHA_CALLSTRING + self.stringlabel
		
		self.sign.sendText( base + fixed + stringcall, 'b', self.lefttxtlabel )
		self.sign.sendText( base + stringcall, 'b', self.centertxtlabel )
		self.sign.sendText( base + stringcall, 'i', self.wipetxtlabel )
		self.sign.sendString( self.barstring, self.stringlabel )
		self.setStyle( 0 )
		return


	def setStyle ( self, style ):
		"set style, 0-2"
		self.style = style
		
		if self.style == 0:
			self.sign.setSequence( self.lefttxtlabel )
		
		if self.style == 1:
			self.sign.setSequence( self.centertxtlabel )
			
		if self.style == 2:
			self.sign.setSequence( self.wipetxtlabel )
			
		self.updateBar()
		return

		
	def updateBar ( self ):
		"attempt bar update. if bar actually changes, return true"
		bar = self.barstring
		
		if self.style == 0:
			bardata = self.getBarData( 13 )
			bar = self.generateBar( bardata, 0 )
		
		if self.style == 1:
			bardata = self.getBarData( 16 )
			bar = self.generateBar( bardata, 1 )
			
		if self.style == 2:
			bardata = self.getBarData( 15 )
			bar = self.generateBar( bardata, 1 )
			
		if bar != self.barstring:
			self.barstring = bar
			self.sign.sendString( self.barstring, self.stringlabel )
			return True
		else:
			return False
		
		
	def generateBar ( self, bardata, bartype ):
		"return a bar string"
		block = chr( 127 )
		halfspace = chr( 126 )
		colormap = { 0 : self.code.Color( 4 ),
								 1 : self.code.Color( 3 ) }
		txt = ''
		
		if bartype == 0: # plain red segmented bar
			txt = colormap[ 1 ]
			for i in bardata:
				if i > 0:
					txt = txt + block
				else:
					txt = txt + ' '
		
		if bartype == 1: # red-over-green solid bar
			for i in bardata:
				txt = txt + colormap[ i ] + block + halfspace
				
		if txt == '':
			txt = ' '
		return txt
		
	
	def getBarData ( self, barsize ):
		"return current data for a bar of given size"
		data = list( self.cpustat.getStats() )
		if data[ 2 ] > 0:
			for i in range( 2 ):
				data[ i ] = float( data[ i ] ) / data[ 2 ]
		mark = int( ( barsize + 0.5 ) * ( data[0] + data[1] ) )
		bardata = [ 1 ] * mark + [ 0 ] * ( barsize - mark )
		return bardata



def main():
	bar = TotalBar( "/dev/ttyUSB0" )

	bar.setStyle( 0 )
	interval = 0.3

	while 1:
		if bar.updateBar():
			time.sleep( interval - 0.1 )
		else:
			time.sleep( interval )
	
	return 0

if __name__ == '__main__': main()
