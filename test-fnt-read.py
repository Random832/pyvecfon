#!/usr/local/bin/python3
from pyvecfon import fntreader
font = fntreader.load_file('msft/modern.fnt')

for field in fntreader.fixed_fields:
    print(field, '=', repr(getattr(font,field)))
#print('chardata = ', font.chardata)
print('facename = ', font.facename)
print('devicename = ', font.devicename)
