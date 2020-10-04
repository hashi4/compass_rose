'''draw a compass rose in svg format'''
import math
import svgwrite

# config
BASE_RADIUS = 360
CENTER = (0, 0)
NUM_TRIANGLES = 8  # 32 points
UNIT_ANGLE = 90 / NUM_TRIANGLES
TRIANGLE_RATIO = math.sin(math.radians(60))  # Equilateral
# TRIANGLE_RATIO = 1  # Isosceles

RING0 = BASE_RADIUS / (
    1 + (math.sin(math.radians(UNIT_ANGLE / 2)) * 2 * TRIANGLE_RATIO))

# svg attributes
COLOR0 = '#b13136'
COLOR1 = '#CCCCCC'
COLOR2 = '#EEEEEE'

STYLES = {
    '.triangle': {
        'fill': COLOR0, 'stroke': 'none'},
    '.circle0': {
        'fill': COLOR2, 'stroke': COLOR1,
        'stroke-width': '{}'.format(BASE_RADIUS/120)},
    '.circle1': {
        'fill': 'none', 'stroke': COLOR0,
        'stroke-width': '{}'.format(BASE_RADIUS/40)},
    '.circle2': {
        'fill': 'none', 'stroke': COLOR1,
        'stroke-width': '{}'.format(BASE_RADIUS/40)},
    '.circle3': {
        'fill': 'none', 'stroke': COLOR1,
        'stroke-width': '{}'.format(BASE_RADIUS/120)},
    '.line': {
        'fill': 'none', 'stroke': COLOR1,
        'stroke-width': '{}'.format(BASE_RADIUS/120)},
    '.line_deg': {
        'fill': 'none', 'stroke': COLOR1,
        'stroke-width': '{}'.format(BASE_RADIUS/360)},
    '.line_deg_thick': {
        'fill': 'none', 'stroke': COLOR1,
        'stroke-width': '{}'.format(BASE_RADIUS/120)},
    '.text_large': {
        'font-family': 'serif', 'fill': 'white',
        'text-anchor': 'middle', 'dominant-baseline': 'baseline',
        'font-size': '{}px'.format(RING0 / 5)},
    '.text_small': {
        'font-family': 'serif', 'fill': 'white',
        'text-anchor': 'middle', 'dominant-baseline': 'baseline',
        'font-size': '{}px'.format(RING0 / 7)},
}


def dict2styles(d):
    def mkcontent(cd):
        s = '{ '
        for key, value in cd.items():
            s += '{}: {}; '.format(key, value)
        s += '}'
        return s

    str = ''
    for class_name, content in d.items():
        str += '{} {}\n'.format(class_name, mkcontent(content))
    return str


def draw_small_triangles(dwg, g):
    x_pos = -RING0 * math.sin(math.radians(UNIT_ANGLE / 2))
    length = -x_pos * 2
    height = TRIANGLE_RATIO * length
    points = [(x_pos, 0), (-x_pos, 0), (0, height)]
    y_pos = RING0

    symbol_small_triangle = dwg.symbol(id='small_triangle')
    dwg.defs.add(symbol_small_triangle)
    symbol_small_triangle.viewbox(x_pos, 0, length, height)
    symbol_small_triangle.add(dwg.polygon(points=points, class_='triangle'))

    for i in range(NUM_TRIANGLES * 2):
        rot = UNIT_ANGLE + UNIT_ANGLE * 2 * i
        g.add(dwg.use(
            symbol_small_triangle, insert=(x_pos, y_pos),
            size=(length, height),
            transform='rotate({})'.format(rot)))
    return


def draw_large_triangles(dwg, g):
    x_pos = -RING0 * math.sin(math.radians(UNIT_ANGLE))
    length = -x_pos * 2
    height = TRIANGLE_RATIO * length
    points = [(x_pos, 0), (-x_pos, 0), (0, height)]
    y_pos = RING0 - length * TRIANGLE_RATIO / 2

    symbol_large_triangle = dwg.symbol(id='large_triangle')
    dwg.defs.add(symbol_large_triangle)
    symbol_large_triangle.viewbox(x_pos, 0, length, height)
    symbol_large_triangle.add(dwg.polygon(points=points, class_='triangle'))

    for i in range(NUM_TRIANGLES):
        rot = UNIT_ANGLE * 4 * i
        g.add(dwg.use(
            symbol_large_triangle, insert=(x_pos, y_pos),
            size=(length, height),
            transform='rotate({})'.format(rot)))
    return


def draw_diamonds(dwg, g):
    x_pos = -RING0 * math.sin(math.radians(UNIT_ANGLE/2))
    length = -x_pos * 2
    height = TRIANGLE_RATIO * length
    points = [
        (x_pos, 0), (0, -height),
        (-x_pos, 0), (0, height)]
    y_pos = RING0 - height

    symbol_diamond = dwg.symbol(id='diamond')
    dwg.defs.add(symbol_diamond)
    symbol_diamond.viewbox(x_pos, -height, length, height * 2)
    symbol_diamond.add(dwg.polygon(points=points, class_='triangle'))

    for i in range(NUM_TRIANGLES):
        rot = UNIT_ANGLE * 2 + UNIT_ANGLE * 4 * i
        g.add(dwg.use(
            symbol_diamond, insert=(x_pos, y_pos),
            size=(length, height * 2),
            transform='rotate({})'.format(rot)))
    return


def draw_wind_lines(dwg, g):
    length = RING0 * math.sin(math.radians(UNIT_ANGLE)) * 2
    h = length * TRIANGLE_RATIO / 2
    h = RING0 - h
    for i in range(NUM_TRIANGLES * 4):
        r = UNIT_ANGLE * i
        g.add(dwg.line(
            (0, 0), (0, h), transform='rotate({})'.format(r), class_='line'))
    return


def draw_circles(dwg, g):
    g.add(dwg.circle((0, 0), BASE_RADIUS * 0.1, class_='circle0'))
    length = RING0 * math.sin(math.radians(UNIT_ANGLE)) * 2
    h = length * TRIANGLE_RATIO / 2
    g.add(dwg.circle((0, 0), RING0 - h, class_='circle1'))
    g.add(dwg.circle((0, 0), (RING0 - h) * 1.05, class_='circle2'))
    g.add(dwg.circle((0, 0), RING0, class_='circle2'))
    g.add(dwg.circle((0, 0), RING0 + h, class_='circle2'))
    g.add(dwg.circle((0, 0), (RING0 - h) * 0.8, class_='circle3'))
    return


def draw_32_wind_points(dwg, g):
    letters = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', ]
    length = RING0 * math.sin(math.radians(UNIT_ANGLE)) * 2
    h = length * TRIANGLE_RATIO / 2
    y_pos = -(RING0 - h * 0.8)
    for index, letter in enumerate(letters):
        rot = UNIT_ANGLE * 4 * index
        class_ = 'text_large' if 0 == index % 2 else 'text_small'
        g.add(dwg.text(
            letter, insert=(0, 0), class_=class_,
            transform='rotate({0}) translate(0, {1})'.format(rot, y_pos)))
    return


def draw_360_degs(dwg, g):
    h = BASE_RADIUS * 0.1

    start = (0, BASE_RADIUS)
    end = (0, BASE_RADIUS + h)
    for deg in range(360):
        cls = 'line_deg' if deg % 10 != 0 else 'line_deg_thick'
        g.add(dwg.line(
            start, end, transform='rotate({})'.format(deg), class_=cls))
    g.add(dwg.circle((0, 0), BASE_RADIUS + h, class_='circle2'))


if '__main__' == __name__:
    dwg = svgwrite.Drawing("compass_rose.svg", debug=True)
    dwg.defs.add(dwg.style(dict2styles(STYLES)))
    top = BASE_RADIUS * 1.2
    dwg.viewbox(-top, -top, top * 2, top * 2)

    g = svgwrite.container.Group(
        transform='translate({}, {})'.format(*CENTER))
    dwg.add(g)

    draw_wind_lines(dwg, g)
    draw_circles(dwg, g)

    g = svgwrite.container.Group(
        transform='translate({}, {}) rotate(0)'.format(*CENTER))
    dwg.add(g)

    draw_small_triangles(dwg, g)
    draw_large_triangles(dwg, g)
    draw_diamonds(dwg, g)

    if 8 == NUM_TRIANGLES:  # 32 points
        g = svgwrite.container.Group(
            transform='translate({}, {}) rotate(0)'.format(*CENTER))
        dwg.add(g)
        draw_32_wind_points(dwg, g)

    g = svgwrite.container.Group(
        transform='translate({}, {})'.format(*CENTER))
    dwg.add(g)
    draw_360_degs(dwg, g)

    dwg.save(pretty=True)
