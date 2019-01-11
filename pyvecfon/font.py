"Actual Font class and rendering logic"
# Font class mostly for rendering purposes...
# Reader and writer don't use any of the logic here.

class Transformation:
    def __init__(self, origin=(0.0, 0.0), scale=1.0):
        self.origin = origin
        self.scale = scale
    def __call__(self, point):
        ox, oy = self.origin
        px, py = point
        return ox + px*self.scale, oy + py*self.scale
    def xfrm_line(self, line):
        res = []
        for xy in line:
            res.append(self(xy))
        return res
    def xfrm_lines(self, lines):
        return (self.xfrm_line(line, scale) for line in lines)

class VectorFont:
    def _render_char(self, num, xbase=0):
        """Output a character as polylines [(x, y), (x, y)], [(x, y), (x, y)]
        Renders at native resolution, returns integer tuples."""
        data = self.chardata[num][1]
        # Transform the data into a list of polylines.
        cx, cy = xbase, 0
        current_segment = [(cx, cy)]
        it = iter(data)
        for rx in it:
            if rx == -128: # Pen up move
                if len(current_segment) > 1:
                    yield current_segment
                current_segment = []
                rx, ry = next(it), next(it)
            else:
                ry = next(it)
            nx, ny = cx+rx, cy+ry
            current_segment.append((nx, ny))
            cx, cy = nx, ny
        if len(current_segment) > 1:
            yield current_segment

    def render_str(self, mystring, verbose=False):
        x = 0
        for char in mystring:
            num, = char.encode('cp1252')
            if verbose:
                yield 'Char %d %r, x=%d' % (num, char, x)
            width = self.chardata[num][0]
            yield from self._render_char(num, x)
            x += width

    def measure_width_str(self, mystring):
        x = 0
        for char in mystring:
            num, = char.encode('cp1252')
            width = self.chardata[num][0]
            x += width
        return x

    def get_scale(self, desired_height_px):
        physical_height = self.dfPixHeight
        # - self.dfInternalLeading ?
        # + self.dfExternalLeading ?
        return desired_height_px / physical_height
