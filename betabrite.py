#!/usr/bin/env python
#
#       betabrite.py
#       Alpha marquee sign serial protocol implementation
#         specifically targeted to model 1036 BetaBrite
#       by anescient

import serial
import time


# formatting strings
FONT_5STD = '\x1a\x31'
FONT_5STROKE = '\x1a\x32'
FONT_7SLIM = '\x1a\x33'  # sign default
FONT_7STROKE = '\x1a\x34'
FONT_7SLIMFANCY = '\x1a\x35'
FONT_7STROKEFANCY = '\x1a\x36'
FONT_7SHADOW = '\x1a\x37'
FONT_7WIDESTROKEFANCY = '\x1a\x38'
FONT_7WIDESTROKE = '\x1a\x39'
FONT_7SHADOWFANCY = '\x1a\x3a'
FONT_5WIDE = '\x1a\x3b'
FONT_7WIDE = '\x1a\x3c'
FONT_7WIDEFANCY = '\x1a\x3d'
FONT_5WIDESTROKE = '\x1a\x3e'

COLOR_RED = '\x1c\x31'
COLOR_GREEN = '\x1c\x32'
COLOR_AMBER = '\x1c\x33'
COLOR_DIMRED = '\x1c\x34'
COLOR_DIMGREEN = '\x1c\x35'
COLOR_BROWN = '\x1c\x36'
COLOR_ORANGE = '\x1c\x37'
COLOR_YELLOW = '\x1c\x38'
COLOR_RAINBOW1 = '\x1c\x39'  # gradient
COLOR_RAINBOW2 = '\x1c\x41'  # mixed patches
COLOR_MIX = '\x1c\x42'  # mixed solid characters
COLOR_AUTO = '\x1c\x43'  # sign default

SPEED_1 = '\x15'
SPEED_2 = '\x16'
SPEED_3 = '\x17'
SPEED_4 = '\x18'  # sign default
SPEED_5 = '\x19'

TEXT_NOHOLD = '\x09'  # no delay before next message
TEXT_FIXLEFT = '\x1e\x31'
TEXT_CALLSTRING = '\x10'  # follow with a string file label
TEXT_CALLSMALLDOTS = '\x14'  # follow with a smalldots file label
TEXT_CLOCK = '\x13'  # show time
TEXT_NEWLINE = '\x0d'

# text between these two will flash
TEXT_FLASHON = '\x071'
TEXT_FLASHOFF = '\x070'

CHR_BLOCK = '\x7f'  # not available in size 5 fonts

# transition effects, used at text loading time, not in-line formatting
MODE_ROTATE = 'a'
MODE_HOLD = 'b'
MODE_FLASH = 'c'
MODE_ROLLUP = 'e'
MODE_ROLLDOWN = 'f'
MODE_ROLLLEFT = 'g'
MODE_ROLLRIGHT = 'h'
MODE_WIPEUP = 'i'
MODE_WIPEDOWN = 'j'
MODE_WIPELEFT = 'k'
MODE_WIPERIGHT = 'l'
MODE_SCROLL = 'm'
MODE_AUTO = 'o'
#MODE_ROLLIN = 'p'  # not available on betabrite 1036
#MODE_ROLLOUT = 'q'  # not available on betabrite 1036
#MODE_WIPEIN = 'r'  # not available on betabrite 1036
#MODE_WIPEOUT = 's'  # not available on betabrite 1036
MODE_ROTATECOMPRESSED = 't'
#MODE_EXPLODE = 'u'  # not available on betabrite 1036
#MODE_CLOCK = 'v'  # not available on betabrite 1036
MODE_TWINKLE = 'n0'
MODE_SPARKLE = 'n1'
MODE_SNOW = 'n2'
MODE_INTERLOCK = 'n3'
#MODE_SWITCH = 'n4'  # not available on betabrite 1036
#MODE_SLIDE = 'n5'  # not available on betabrite 1036
MODE_SPRAY = 'n6'
MODE_STARBURST = 'n7'
MODE_WELCOME = 'n8'
MODE_SLOTMACHINE = 'n9'
MODE_NEWSFLASH = 'nA'
MODE_TRUMPET = 'nB'
#MODE_CYCLECOLORS = 'nC'  # not available on betabrite 1036
MODE_THANKYOU = 'nS'
MODE_NOSMOKING = 'nU'
MODE_DRINKDRIVE = 'nV'
MODE_FISH = 'nW'
MODE_FIREWORKS = 'nX'
MODE_BALLOONS = 'nY'
MODE_BOMB = 'nZ'

SND_LONGBEEP = '\x30'
SND_3BEEPS = '\x31'

# protocol note: have >100ms delay after STX for nested packets
ALPHA_PREAMBLE = '\x00' * 5  # may also be = '\x01' * 5
ALPHA_TYPEALL = 'Z00'  # all sign types, all addresses
ALPHA_SOH = '\x01'  # start of header
ALPHA_STX = '\x02'  # start of text
ALPHA_ETX = '\x03'  # end of text
ALPHA_EOT = '\x04'  # end of transmission
ALPHA_ESC = '\x1b'  # escape
ALPHA_CR = '\x0d'
ALPHA_LF = '\x0a'

# image file types
DOTS_MONO = '1000'
DOTS_3COLOR = '2000'
DOTS_8COLOR = '4000'

# image pixel colors
DOTC_BLACK = '0'
DOTC_RED = '1'
DOTC_GREEN = '2'
DOTC_AMBER = '3'
DOTC_DIMRED = '4'
DOTC_DIMGREEN = '5'
DOTC_BROWN = '6'
DOTC_ORANGE = '7'
DOTC_YELLOW = '8'

textcode = {}
#fonts
textcode['<5>'] = FONT_5STD
textcode['<5bold>'] = FONT_5STROKE
textcode['<5wide>'] = FONT_5WIDE
textcode['<5huge>'] = FONT_5WIDESTROKE
textcode['<7>'] = FONT_7SLIM
textcode['<7bold>'] = FONT_7STROKE
textcode['<7wide>'] = FONT_7WIDE
textcode['<7huge>'] = FONT_7WIDESTROKE
#colors
textcode['<autocolor>'] = COLOR_AUTO
textcode['<red>'] = COLOR_RED
textcode['<dimred>'] = COLOR_DIMRED
textcode['<green>'] = COLOR_GREEN
textcode['<dimgreen>'] = COLOR_DIMGREEN
textcode['<yellow>'] = COLOR_YELLOW
textcode['<amber>'] = COLOR_AMBER
textcode['<orange>'] = COLOR_ORANGE
textcode['<brown>'] = COLOR_BROWN
textcode['<mixcolor>'] = COLOR_MIX
textcode['<rainbow>'] = COLOR_RAINBOW1
textcode['<patchcolor>'] = COLOR_RAINBOW2
#special characters
textcode['<block>'] = CHR_BLOCK
#etc
textcode['<clock>'] = TEXT_CLOCK
textcode['<slowest>'] = SPEED_1
textcode['<fast>'] = SPEED_5
textcode['<fastest>'] = TEXT_NOHOLD
textcode['<string>'] = TEXT_CALLSTRING
textcode['<smalldots>'] = TEXT_CALLSMALLDOTS
textcode['<fixleft>'] = TEXT_FIXLEFT


def encodeText(text):
    for code, decode in textcode.iteritems():
        text = text.replace(code, decode)
    return text


# sign memory must be configured completely before data is loaded
class _MemConfig(object):
    """a helper class to compose a sign's memory configuration"""

    LABEL_PRIORITY = '0'

    def __init__(self):
        # usable, open file labels
        self._labels_available = set(chr(c) for c in xrange(0x20, 0x7f))
        # exclude labels with any special function
        self._labels_available -= set('A012345?')
        # exclude labels that act 'weird' in experimentation
        self._labels_available -= set(' \x7e')

        # label : configstring including label
        self._allocated_text = {}
        self._allocated_string = {}
        self._allocated_image = {}

    def newText(self, size=100):
        """add a text file, return the file label"""
        if size < 1:
            raise Exception('bad text file len {0}'.format(size))
        label = self._popFileLabel()
        self._allocated_text[label] = '{0}AL{1:04X}FFFF'.format(label, size)
        return label

    def newString(self, size=100):
        """add a string file, return the file label"""
        if size < 1:
            raise Exception('bad string file len {0}'.format(size))
        label = self._popFileLabel()
        self._allocated_string[label] = '{0}BL{1:04X}0000'.format(label, size)
        return label

    def newSmalldots(self, width, height, dotsformat=None):
        """add a SMALLDOTS image file, return the file label"""
        if dotsformat is None:
            dotsformat = DOTS_8COLOR
        if width < 0 or width > 255 or height < 0 or height > 31:
            raise Exception('bad smalldots dimensions {0} by {1}'.format(\
                width, height))
        if dotsformat not in [DOTS_MONO, DOTS_3COLOR, DOTS_8COLOR]:
            raise Exception('bad dots color mode {0}'.format(dotsformat))
        label = self._popFileLabel()
        self._allocated_image[label] = '{0}DL{1:02X}{2:02X}{3}'.format(\
            label, height, width, dotsformat)
        return label

    def _popFileLabel(self):
        if not self._labels_available:
            raise Exception('file labels exhausted')
        # file labels seem to be arbitrary in the sign
        #  (any label for any file type)
        return self._labels_available.pop()

    def getSetupString(self):
        """return entire memory configuration string for current state"""
        # the order in which file configs are presented to the sign is relevant
        # the order _seems_ to be text then images then strings
        # ... finally, according to docs, something called counter-text files
        configStrings = []
        configStrings += self._allocated_text.values()
        configStrings += self._allocated_image.values()
        configStrings += self._allocated_string.values()
        return ''.join(configStrings)


class Sign(object):
    """interface to BetaBrite model 1036 on serial port"""

    # nest memory config class
    MemConfig = _MemConfig

    def __init__(self, port=0):
        """port may be index or a device file name"""
        self._comm = serial.Serial(port, 9600)
        self._commwait = 0.1  # certain transmissions call for a short delay

    def clear(self):
        """clear memory, leave sign blank"""
        self.clearMem()
        self.clearPriority()

    def clearMem(self):
        # write special function, setup memory
        self._sendPacket('E$')
        time.sleep(self._commwait)

    def setupMem(self, config):
        if type(config) != self.MemConfig:
            raise Exception('config is not a MemConfig')
        self._sendPacket('E$' + config.getSetupString())
        time.sleep(self._commwait)

    def sendText(self, label, msg, mode=None):
        """write a text file"""
        if type(label) != str or len(label) != 1:
            raise Exception('label is not a file label character')
        if type(msg) != str:
            raise Exception('msg is not a string')
        if mode is None:
            mode = MODE_HOLD
        if label == self.MemConfig.LABEL_PRIORITY and len(msg) > 125:
            raise Exception('text too long for priority file')
        dat = 'A' + label  # write text
        if msg and mode:
            dat = dat + ALPHA_ESC + '0'  # display position, ignored on 213C
            dat = dat + mode + msg
        self._sendPacket(dat)

    def sendTextPriority(self, msg, mode=None):
        self.sendText(self.MemConfig.LABEL_PRIORITY, msg, mode)

    def clearPriority(self):
        self.sendTextPriority('')

    def getText(self, label, stripmode=True):
        if type(label) != str or len(label) != 1:
            raise Exception('label is not a file label character')
        self._sendPacket('B' + label)  # read text
        txt = self._recvPacket()
        if not txt.startswith('A' + label):
            return ''
        txt = txt[2:]  # strip type/label
        if stripmode and txt[0] == ALPHA_ESC:
            txt = txt[2:]  # strip ESC and disp. pos.
            if txt[0] == 'n':  # special mode
                txt = txt[2:]  # strip special mode
            else:
                txt = txt[1:]  # strip normal mode
        return txt

    def sendString(self, label, msg):
        """write a string file"""
        self._sendPacket('G' + label + msg)

    def sendSmalldots(self, label, rows):
        """rows is a list of strings"""
        dat = 'I{0}{1:02X}{2:02X}'.format(label, len(rows), len(rows[0]))
        for row in rows:
            dat = dat + row + ALPHA_CR
        self._sendPacket(dat)

    def getSmalldots(self, label):
        """returns the format sendSmalldots accepts"""
        self._sendPacket('J' + label)
        dots = self._recvPacket()
        if not dots.startswith('I' + label):
            return []
        dots = dots[2:]  # strip type/label
        if len(dots) < 4:
            return []
        #height = int(dots[0:2], 16)
        #width = int(dots[2:4], 16)
        dots = dots[4:]  # strip dimensions
        dots = dots.rstrip(ALPHA_CR)
        rows = dots.split(ALPHA_CR)
        return rows

    def setSequence(self, sequence):
        """set message display sequence, sequence is a string of file labels"""
        if type(sequence) != str:
            raise Exception('sequence is not a string')
        # write special function, run in order, locked
        self._sendPacket('E.SL' + sequence)

    def setClock(self, settime=None):
        """# time format is 'HHMM', 24 hour format, or None for current time"""
        if settime is None:
            settime = time.strftime('%H%M', time.localtime())
        if len(settime) != 4:
            raise Exception('not a valid time')
        self._sendPacket('E ' + settime)

    def getClock(self):
        """# time format is 'HHMM', 24 hour format"""
        dat = self._getSpecialFunc(' ')
        if len(dat) != 4:
            raise Exception('Couldn\'t get time. Sign clock may not be set.')
        return dat

    def getMeminfo(self):
        """query sign, return tuple (bytestotal, bytesfree)"""
        meminfo = self._getSpecialFunc('#')
        if len(meminfo) != 9:
            raise Exception('Couldn\'t get memory status.')
        return (int(meminfo[0:4], 16), int(meminfo[5:9], 16))

    def enableSpeaker(self):
        self._sendPacket('E!00')
        self._sendPacket('E(A')

    def disableSpeaker(self):
        self._sendPacket('E!FF')
        self._sendPacket('E(B')

    def beep(self):
        self._sendPacket('E(' + SND_LONGBEEP)

    def beepTriple(self):
        self._sendPacket('E(' + SND_3BEEPS)

    def _sendPacket(self, contents):
        preamble = ALPHA_PREAMBLE + ALPHA_SOH + ALPHA_TYPEALL + ALPHA_STX
        if self._commwait > 0 and contents.startswith('I'):
            # sending smalldots
            self._comm.write(preamble + contents[:5])
            time.sleep(self._commwait)
            self._comm.write(contents[5:] + ALPHA_EOT)
        else:
            self._comm.write(preamble + contents + ALPHA_EOT)
        time.sleep(self._commwait)

    def _recvPacket(self):
        self._comm.timeout = 1
        got = ''
        while True:
            c = self._comm.read()
            got += c
            if not c or c == ALPHA_EOT:
                break

        leadin = ALPHA_SOH + '000' + ALPHA_STX
        leadinpos = got.find(leadin)
        if leadinpos == -1:
            return ''
        startpos = leadinpos + len(leadin)
        endpos = got.find(ALPHA_ETX, startpos)
        if endpos == -1:
            return ''
        return got[startpos:endpos]

    def _getSpecialFunc(self, specialfunc):
        self._sendPacket('F' + specialfunc)
        dat = self._recvPacket()
        if not dat.startswith('E' + specialfunc):
            return ''
        return dat[len(specialfunc) + 1:]
