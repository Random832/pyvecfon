"Loader for FNT files"
import struct
from .font import VectorFont

class StructReader:
    def __init__(self, data):
        self.data = data
        self.pos = 0
    def read(self, fmt):
        size = struct.calcsize(fmt)
        result = struct.unpack_from(fmt, self.data, self.pos)
        self.pos += size
        return result
    def readw(self):
        return self.read('<H')[0]
    def readd(self):
        return self.read('<I')[0]
    def readb(self):
        return self.read('B')[0]
    def reads(self, n):
        s, = self.read('%ds' % n)
        return fixstr(s)
    def readsz(self):
        end = self.data.find(b'\0', self.pos)
        value = self.data[self.pos:end+1]
        self.pos = end+1
        return fixstr(value)

fixed_fields = [
        'dfVersion',
        'dfSize',
        'dfCopyright',
        'dfType',
        'dfPoints',
        'dfVertRes',
        'dfHorizRes',
        'dfAscent',
        'dfInternalLeading',
        'dfExternalLeading',
        'dfItalic',
        'dfUnderline',
        'dfStrikeOut',
        'dfWeight',
        'dfCharSet',
        'dfPixWidth',
        'dfPixHeight',
        'dfPitchAndFamily',
        'dfAvgWidth',
        'dfMaxWidth',
        'dfFirstChar',
        'dfLastChar',
        'dfDefaultChar',
        'dfBreakChar',
        'dfWidthBytes',
        'dfDevice',
        'dfFace',
        'dfBitsPointer',
        'dfBitsOffset',
        ]

def fixstr(s):
    return s.rstrip(b'\0').decode('cp1252', errors='surrogateescape')

def load_file(filename):
    return load_data(open(filename, 'rb').read())

def load_data(data):
    font = VectorFont()
    rd = StructReader(data)
    data0 = rd.read('<HI60sHHHHHHHBBBHBHHBHHBBBBHIIII')
    for i, data1 in enumerate(data0):
        fldName = fixed_fields[i]
        if type(data1) is bytes:
            data1 = fixstr(data1)
        setattr(font, fldName, data1)
    charoffset = {}
    for i in range(font.dfFirstChar, font.dfLastChar+2):
        # TODO support fixed fonts, these get the width from the font
        charoffset[i] = values = rd.read('<HH')
    assert(font.dfFace == rd.pos)
    font.facename = rd.readsz()
    if font.dfDevice:
        assert(font.dfDevice == rd.pos)
        font.devicename = rd.readsz()
    else:
        font.devicename = None
    assert(font.dfBitsOffset == rd.pos + rd.pos % 2)
    chardata = {}
    for char in range(font.dfFirstChar, font.dfLastChar+1):
        offset, width = charoffset[char]
        length = charoffset[char+1][0] - offset
        rd.pos = font.dfBitsOffset + offset
        # TODO support two-byte coords?
        cdata = rd.read('<'+length*'b')
        chardata[char] = (width, cdata)
    font.chardata = chardata
    return font
