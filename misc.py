# Scratchpad for the stuff that I had before importing @Hypothete's data

def convbits(*strokes):
    if not strokes:
        return []
    cx = cy = 0
    data = []
    for stroke in strokes:
        # It really doesn't like skipping this
        data.append(UP)
        for x, y in stroke:
            rx, ry = x - cx, y - cy
            data.append(rx)
            data.append(ry)
            cx = x
            cy = y
    return data
def put(chars, *strokes, width=30):
    bits = convbits(*strokes)
    for char in chars:
        font.chardata[ord(char)] = width, bits
#font.chardata = {}
#for c in range(font.dfFirstChar, font.dfLastChar+1):
#    font.chardata[c] = 30, []
put(' ')
put('Aa', [(0, 30), (0, 10), (10, 0), (20, 10), (20, 30)], [(0, 20), (20, 20)])
PUT('Bb', [(0, 0), (0, 30), (15, 30), (20, 25), (20, 20), (15, 15), (0, 15), (15, 15), (20, 10), (20, 5), (15, 0), (0, 0)])
