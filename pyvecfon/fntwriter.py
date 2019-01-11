"Writer for FNT files"
import struct

def encsz(s):
    return s.encode('ascii').rstrip(b'\0')+b'\0'

class _FontWriter:
    def __init__(self, font):
        self.font = font
    def doAll(self, wf):
        self.doMakeBits()
        self.doMeasurePass()
        self.doActualWrite(wf)
    def doMakeBits(self):
        cbits = []
        bbits = []
        offset = 0
        nEntries = self.font.dfLastChar-self.font.dfFirstChar+2
        for i in range(self.font.dfFirstChar, self.font.dfLastChar+1):
            width, data = self.font.chardata[i] # TODO default?
            #print("char", chr(i), i, width, data)
            bbits.append(struct.pack(len(data)*'b', *data))
            cbits.append(struct.pack('<HH', offset, width))
            offset += len(data)
        cbits.append(struct.pack('<HH', offset, 0)) # sentinel
        self.cbits = b''.join(cbits)
        self.bbits = b''.join(bbits)
        assert(len(self.cbits) == 4 * nEntries)
    def doMeasurePass(self):
        font = self.font
        self.bCopyright = encsz(font.dfCopyright).rstrip(b'\0')
        assert(len(self.bCopyright) <= 60)
        self.bfacename = encsz(font.facename)
        if font.devicename:
            self.bdevname = encsz(font.devicename)
        else:
            self.bdevname = b''
        # 117        length of fixed header
        font.dfFace = 117 + len(self.cbits)
        if self.bdevname:
            font.dfDevice = font.dfFace + len(self.bfacename)
            font.dfBitsOffset = font.dfDevice + len(self.bdevname)
        else:
            font.dfDevice = 0
            font.dfBitsOffset = font.dfFace + len(self.bfacename)
        if font.dfBitsOffset % 2:
            font.dfBitsOffset += 1
            self.bpad = b'\0'
        else:
            self.bpad = b''
        font.dfSize = font.dfBitsOffset + len(self.bbits)
        assert(font.dfSize == 117 + len(self.cbits) + len(self.bfacename) + len(self.bdevname) + len(self.bpad) + len(self.bbits))
    def doActualWrite(self, wf):
        f = self.font
        headerData = [
                f.dfVersion,
                f.dfSize,
                self.bCopyright,
                f.dfType,
                f.dfPoints,
                f.dfVertRes,
                f.dfHorizRes,
                f.dfAscent,
                f.dfInternalLeading,
                f.dfExternalLeading,
                f.dfItalic,
                f.dfUnderline,
                f.dfStrikeOut,
                f.dfWeight,
                f.dfCharSet,
                f.dfPixWidth,
                f.dfPixHeight,
                f.dfPitchAndFamily,
                f.dfAvgWidth,
                f.dfMaxWidth,
                f.dfFirstChar,
                f.dfLastChar,
                f.dfDefaultChar,
                f.dfBreakChar,
                f.dfWidthBytes,
                f.dfDevice,
                f.dfFace,
                f.dfBitsPointer,
                f.dfBitsOffset,
                ]
        fixedHeader = struct.pack('<HI60sHHHHHHHBBBHBHHBHHBBBBHIIII', *headerData)
        assert(len(fixedHeader) == 117)
        wf.write(fixedHeader)
        wf.write(self.cbits)
        wf.write(self.bfacename)
        wf.write(self.bdevname)
        wf.write(self.bpad)
        wf.write(self.bbits)

# Class API is unstable, I will probably consolidate some functions or deal with state differently.
# Consider this the only public API.
def write_fnt(font, wf):
    _FontWriter(font).doAll(wf)
