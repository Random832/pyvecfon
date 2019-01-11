#!/usr/local/bin/python3
import sys
import struct
import PIL, PIL.ImageDraw, PIL.Image
from pyvecfon.font import Transformation
from pyvecfon.fntreader import load_file

roman = load_file("msft/roman.fnt")
modern = load_file("msft/modern.fnt")
script = load_file("msft/script.fnt")
lines = [
        (script, script.dfPoints/.75, "Jackdaws love my big sphinx of quartz."),
        #(modern, modern.dfPoints/.75, "I am the very model of a modern major general"),
        (roman, roman.dfPoints/.75, "Senatvs Popvlvsqve Romanvs"),
        ]

def measure_lines(lines):
    width = height = 0
    for font, size, text in lines:
        scale = font.get_scale(size)
        width = max(width, scale*font.measure_width_str(text))
        height += size

    width = int(max(width+1, 16))
    height = int(max(height+1, 16))
    return width, height

def draw_png(filename, lines):
    width, height = measure_lines(lines)
    im = PIL.Image.new("L", (width, height))
    dr = PIL.ImageDraw.Draw(im)

    y = 0
    for font, size, text in lines:
        t = Transformation((0, y), scale=font.get_scale(size))
        for line in font.render_str(text):
            dr.line(t.xfrm_line(line), 255)
        y += size
    im.save(filename)

def write_svg(wf, lines):
    width, height = measure_lines(lines)
    wf.write('<svg height="%d" width="%d" xmlns="http://www.w3.org/2000/svg">\n' % (height, width))
    y = 0
    wf.write('<style>\n')
    for i, (font, size, text) in enumerate(lines):
        scale = font.get_scale(size)
        wf.write('.L%d {fill: none; stroke: black; stroke-width: %f; stroke-linecap: round; stroke-linejoin: round}\n' % (i, scale))
    wf.write('</style>\n')
    for i, (font, size, text) in enumerate(lines):
        wf.write('<!-- %s %d: %s -->\n' % (font.facename, size, text))
        scale = font.get_scale(size)
        t = Transformation((0, y), scale=scale)
        for line in font.render_str(text, True):
            if type(line) is str:
                # Injected comments
                wf.write('<!-- %s -->\n' % line)
            else:
                line = t.xfrm_line(line)
                pointstr = ' '.join('%r,%r'%p for p in line)
                wf.write('<polyline class="L%d" points="%s"/>\n' % (i, pointstr))
        y += size
    wf.write('</svg>\n')

write_svg(sys.stdout, lines)
