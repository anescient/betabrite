# fry up access to BetaBrite on serial port

import serial
import time

class AlphaSign:
  "interface to BetaBrite model 1036 on serial port"

  PORTNUM = "/dev/ttyUSB0" # 0 = COM1
  PORTBAUD = 9600

  # various constants for Alpha protocol
  ALPHA_PREAMBLE = "\x00" * 5 # may also be = "\x01" * 5
  ALPHA_TYPEALL = "Z00" # all sign types, all addresses
  ALPHA_SOH = "\x01" # start of header
  ALPHA_STX = "\x02" # start of text (note: have >100ms delay after STX for nested packets)
  ALPHA_ETX = "\x03" # end of text
  ALPHA_EOT = "\x04" # end of transmission
  ALPHA_ESC = "\x1b" # escape


  def sendRaw ( self, data = "" ):
    "send raw data to the sign"
    if len(data) > 0:
      comport = serial.Serial( self.PORTNUM, self.PORTBAUD )
      comport.write( data )
      comport.close()
    return


  def sendAll ( self, contents = "" ):
    "form a packet and send"
    dat = self.ALPHA_PREAMBLE + self.ALPHA_SOH + self.ALPHA_TYPEALL + self.ALPHA_STX
    dat = dat + contents
    dat = dat + self.ALPHA_EOT
    self.sendRaw( dat )
    return


  def clear ( self ):
    "clear sign memory"
    self.sendAll( "E$" ) # write special function, clear memory


  def setupMem ( self ):
    "set up sign memory"
    dat = "E" # write special function
    dat = dat + "$"
    for label in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
      dat = dat + label + "AL" # TEXT file, locked
      dat = dat + "0100" # file size in hex, 100h = 256 #TODO actually calculate and convert
      dat = dat + "FF00" # start/stop time, start FFh = always
    self.sendAll( dat )
    return


  # time format is "HHMM", 24 hour format, or none to use current local time
  def setClock ( self, settime = "" ):
    "set sign clock"
    if len(settime) != 4:
      settime = time.strftime( "%H%M", time.localtime() )
    self.sendAll( "E\x20" + settime )


  # mode is [a, v], n -> special, o = auto
  # special is n[1,9]  a,b,c, s,u,v,w,x,y,z
  def sendText ( self, msg = "text", mode = "o", label = "0" ):
    "write a text file"
    dat = "A" + label # write text
    if len(msg) > 0 and len(mode) > 0:
      dat = dat + self.ALPHA_ESC + "0" # display position, ignored on 213C
      dat = dat + mode + msg
    self.sendAll(dat)
    return


  def storeText ( self, msg = "text", mode = "b", label = "a" ):
    "set up memory and store a message"
    dat = "E" # write special function
    dat = dat + "$" + label + "AL" # TEXT file, locked
    dat = dat + "0100" # file size in hex, 100h = 256 #TODO actually calculate and convert
    dat = dat + "FF00" # start/stop time, start FFh = always
    self.sendAll( dat )
    self.sendText( msg, mode, label )
    return


  # sequence is a list of file labels
  def setSequence ( self, sequence = "a" ):
    "set up message display sequence"
    dat = "E\x2eSL" # write special function, run in order, locked
    dat = dat + sequence
    self.sendAll( dat )
    return


######################################################

class AlphaCode:
  "a collection of functions for generating Alpha text control codes"
  # color is [0, 11]
  # 0 = red, green, amber, dim red, dim green, brown, orange, yellow,
  # 8 = rainbow1, rainbow2, mix, auto
  def Color ( self, color = 11 ):
    "generate a color control code"
    code = ""
    if color >= 0:
      if color < 9:
        code = "\x1c" + chr(49 + color) # 49 = 31H (red)
      else:
        if color < 12:
          code = "\x1c" + chr(65 + color - 9) # 65 = 41H (rainbow2)
    return code


  # font is [0, 13]
  # 0 = 5 high std, 5 stroke, 7 slim, 7 stroke, 7 slim fancy, 7 stroke fancy, 7 shadow,
  # 7 = wide stroke 7 fancy, wide stroke 7, 7 shadow fancy, 5 wide, 7 wide
  # 12 = 7 fancy wide, wide stroke 5
  def Font ( self, font = 0 ):
    "generate a font control code"
    code = ""
    if font >= 0 and font < 14:
      code = "\x1a" + chr( 49 + font )
    return code
  

  # speed is [1, 5], default 4
  def Speed ( self, speed = 4 ):
    "generate a speed control code"
    code = ""
    if speed > 0 and speed < 6:
      code = chr( 20 + speed )
    return code




