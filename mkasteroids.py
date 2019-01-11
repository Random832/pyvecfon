#!/usr/local/bin/python3
from pyvecfon.fntreader import load_file
from pyvecfon.fntwriter import write_fnt
import json
# TODO make this work without modern as a starting point.
# My placeholder glyphs keep crashing
font = load_file('msft/modern.fnt')
font.facename = 'Asteroids'
UP = -128

letters = json.load(open('letters.json'))
def cc(f):
    return int(round(f*10))
def cl(line, vertices):
    # TODO clean up
    xa = cc(vertices[line[0]][0])
    ya = 30 - cc(vertices[line[0]][1])
    xb = cc(vertices[line[1]][0])
    yb = 30 - cc(vertices[line[1]][1])
    return xa, ya, xb, yb

# WHY WONT YOU WORK
placeholder = 30, (UP, 0, 0, 20, 30)
for c in range(32, 225):
    font.chardata[c] = placeholder
##for c in [225, 226, 227, 228, 229]: font.chardata[c] = placeholder
##for c in [230, 231, 232, 233, 234]: font.chardata[c] = placeholder
##for c in [235, 236, 237, 238, 239]: font.chardata[c] = placeholder
##for c in [240, 241, 242, 243, 244]: font.chardata[c] = placeholder
##for c in [245, 246, 247, 248, 249]: font.chardata[c] = placeholder
##for c in [250, 251, 252, 253, 254]: font.chardata[c] = placeholder
for c in [255]: font.chardata[c] = placeholder

font.chardata[32] = 30, [] # Blank space is a very special case

for letter in letters:
    char = letter['char']
    ii = iter(letter['lines'])
    lines = list(zip(ii, ii))
    ii = iter(letter['vertices'])
    vertices = list(zip(ii, ii))
    cx, cy = 0, 0
    if vertices[lines[0][0]] == (0, 3):
        # Windows wants *every* character to start with an upstroke, but our
        # logic below doesn't do it if the first point happens to be on the
        # origin.
        data = [UP, 0, 0]
    else:
        data = []
    for line in lines:
        xa, ya, xb, yb = cl(line, vertices)
        if (xa, ya) != (cx, cy):
            data.append(UP)
            data.append(xa - cx)
            data.append(ya - cy)
            cx = xa
            cy = ya
        data.append(xb - cx)
        data.append(yb - cy)
        cx = xb
        cy = yb
    font.chardata[ord(char)] = font.chardata[ord(char.upper())] = 30, data

# At least make it monospaced.
for c in range(font.dfFirstChar, font.dfLastChar+1):
    font.chardata[c] = 30, font.chardata[c][1]

font.dfLastChar = 252
with open('asteroids.fnt', 'wb') as wf:
    write_fnt(font, wf)
