#!/usr/bin/env python
#
#       alphasign.py
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

import serial
import time


class AlphaMemSetup:
	"configuration for alpha sign memory"
	
	FIRSTLABEL = 0x40
	
	currentlabel = FIRSTLABEL
	configlist = list() # list of tuples ( type, label, size )
	
	TYPE_TEXT = "\x41"
	TYPE_STRING = "\x42"
	TYPE_SMALLDOTS = "\x43"
	
	
	def clear ( self ):
		self.currentlabel = FIRSTLABEL
		return
	
	
	def pushTextFile ( self, size = 100 ):
		"add a text file to the configuration, return the file label"
		if size < 1:
			return ''
		label = self.getNextLabel()
		if not label:
			return ''
		entry = ( self.TYPE_TEXT, label, "%04X" % size )
		self.configlist.append( entry )
		return label
	
	
	def pushStringFile ( self, size = 125 ):
		"add a string file to the configuration, return the file label"
		if size < 1:
			return ''
		label = self.getNextLabel()
		if not label:
			return ''
		entry = ( self.TYPE_STRING, label, "%04X" % size )
		self.configlist.append( entry )
		return label

	
	def pushSmallDotsFile ( self, size = ( 1, 1 ) ):
		"add a small dots file to the configuration, return the file label"
		if len( size ) != 2:
			return ''
		if size[0] < 1 or size[1] < 1 or size[0] > 255 or size[1] > 31:
			return ''
		return
	
	
	def getNextLabel ( self ):
		"get next available file label"
		if self.currentlabel > 0x7e:
			return ''
		label = chr( self.currentlabel )
		self.currentlabel = self.currentlabel + 1
		return label


###########################################################

class AlphaSign:
  "interface to BetaBrite model 1036 on serial port"

  PORTNUM  = 0 # 0 = COM1, or file name
  PORTBAUD = 9600

  # various constants for Alpha protocol
  ALPHA_PREAMBLE = "\x00" * 5 # may also be = "\x01" * 5
  ALPHA_TYPEALL = "Z00" # all sign types, all addresses
  ALPHA_SOH = "\x01" # start of header
  ALPHA_STX = "\x02" # start of text (note: have >100ms delay after STX for nested packets)
  ALPHA_ETX = "\x03" # end of text
  ALPHA_EOT = "\x04" # end of transmission
  ALPHA_ESC = "\x1b" # escape

  comport = 0 # serial.Serial( PORTNUM, PORTBAUD )
  
  def __init__ ( self, comport = 0 ):
  	self.PORTNUM = comport
  	self.comport = serial.Serial( self.PORTNUM, self.PORTBAUD )
  	return
  
  
  def sendRaw ( self, data = "" ):
    "send raw data to the sign"
    if len(data) > 0:
      self.comport.write( data )
      time.sleep( 0.1 )
    return


  def sendPacket ( self, contents = "" ):
    "form a packet and send"
    dat = self.ALPHA_PREAMBLE + self.ALPHA_SOH + self.ALPHA_TYPEALL + self.ALPHA_STX
    dat = dat + contents + self.ALPHA_EOT
    self.sendRaw( dat )
    return


  def clearMem ( self ):
    "clear sign memory"
    self.sendPacket( "E$" ) # write special function, clear memory
    time.sleep( 0.1 )
    return


  def setupMem ( self, config = AlphaMemSetup ):
    "set up sign memory, return list of labels"
    qqqq = { AlphaMemSetup.TYPE_TEXT : "FFFF", # display always
    				 AlphaMemSetup.TYPE_STRING : "0000", # ignored
    				 AlphaMemSetup.TYPE_SMALLDOTS : "2000" } # 3-color image
    dat = "E$" # write special function, setup memory
    for entry in config.configlist:
      dat = dat + entry[1] + entry[0] + "L" # label, type, locked
      dat = dat + entry[2] # size
      dat = dat + qqqq[ entry[0] ]
    self.sendPacket( dat )
    time.sleep( 0.1 )
    return


  # time format is "HHMM", 24 hour format, or none to use current local time
  def setClock ( self, settime = "" ):
    "set sign clock"
    if len( settime ) != 4:
      settime = time.strftime( "%H%M", time.localtime() )
    self.sendPacket( "E\x20" + settime )
    return


  # mode is [a, v], n -> special, o = auto
  # special is n[1,9]  a,b,c, s,u,v,w,x,y,z
  def sendText ( self, msg = "text", mode = "o", label = "0" ):
    "write a text file"
    dat = "\x41" + label # write text
    if len( msg ) > 0 and len( mode ) > 0:
      dat = dat + self.ALPHA_ESC + "0" # display position, ignored on 213C
      dat = dat + mode + msg
    self.sendPacket( dat )
    return


  def sendString ( self, msg, label ):
    "write a string file"
    dat = "\x47" + label # write string
    dat = dat + msg
    self.sendPacket( dat )
    return


  # sequence is a string of file labels
  def setSequence ( self, sequence = "a" ):
    "set up message display sequence"
    dat = "E\x2eSL" # write special function, run in order, locked
    dat = dat + sequence
    self.sendPacket( dat )
    return


######################################################

class AlphaCode:
  "a collection of functions for generating Alpha text control codes"
  
  ALPHA_NOHOLD = "\x09"
  ALPHA_FIXLEFT = "\x1e\x31"
  ALPHA_CALLSTRING = "\x10"
  
  # color is [0, 11]
  # 0 = red, green, amber, dim red, dim green, brown, orange, yellow,
  # 8 = rainbow1, rainbow2, mix, auto
  def Color ( self, color = 11 ):
    "generate a color control code"
    code = ''
    if color >= 0:
      if color < 9:
        code = '\x1c' + chr(49 + color) # 49 = 31H (red)
      else:
        if color < 12:
          code = '\x1c' + chr(65 + color - 9) # 65 = 41H (rainbow2)
    return code


  # font is [0, 13]
  # 0 = 5 high std, 5 stroke, 7 slim, 7 stroke, 7 slim fancy, 7 stroke fancy, 7 shadow,
  # 7 = wide stroke 7 fancy, wide stroke 7, 7 shadow fancy, 5 wide, 7 wide
  # 12 = 7 fancy wide, wide stroke 5
  def Font ( self, font = 0 ):
    "generate a font control code"
    code = ''
    if font >= 0 and font < 14:
      code = '\x1a' + chr( 49 + font )
    return code
  

  # speed is [1, 5], default 4
  def Speed ( self, speed = 4 ):
    "generate a speed control code"
    code = ''
    if speed > 0 and speed < 6:
      code = chr( 20 + speed )
    return code




