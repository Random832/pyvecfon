#!/usr/local/bin/python3
from pyvecfon import fntreader, fntwriter
myfont = fntreader.load_file('msft/modern.fnt')
with open('modern2.fnt', 'wb') as wf:
    fntwriter.write_fnt(myfont, wf)
