"""Figure layer: attaches drawings (tools/render.py kinds) to skills defined in the other modules.  Must be loaded last.

All figures here are illustrations of the situation described in the prompt (essential=False): the prompt alone is
enough to answer, the figure helps to see it.  A '?' in a label marks the unknown; no figure shows the answer."""
from dsl import *

# ============================================================================ I-III
add_media('ew-shape-count',
          fig('polygon', 'Rysunek figury.',
              pts=E("[[[0, 0], [4, 0], [2, 3]], [[0, 0], [3, 0], [3, 3], [0, 3]], [[0, 0], [5, 0], [5, 3], [0, 3]], [[0, 0], [5, 0], [6, 3], [1, 3]]]"
                    "[index(['trójkąt', 'kwadrat', 'prostokąt', 'czworokąt'], sh[0])]")))

add_media('ew-perimeter',
          fig('rect', 'Prostokąt (lub kwadrat) z podanymi bokami.', when='f != 1',
              w=E('a'), h=E('a if (f == 0 and sq) else b'), unit=E('un')),
          fig('triangle-sides', 'Trójkąt z podanymi bokami.', when='f == 1',
              sides=[E('a'), E('b'), E('c')], labels=[E("str(a) + ' ' + un"), E("str(b) + ' ' + un"), E("str(c) + ' ' + un")]))

# ============================================================================ IV-VI: angles, triangles
add_media('n46-angle-pairs',
          fig('angle-pair', 'Dwie proste i zaznaczone kąty α i β.', when='kind < 3',
              kind=E("['adjacent', 'vertical', 'corresponding'][kind]"), alpha=E('al')))

add_media('n46-triangle-angle',
          fig('triangle-angles', 'Trójkąt z zaznaczonymi kątami; znak zapytania oznacza szukany kąt.', when='mode < 2',
              angles=E('[a, b, 180 - a - b] if mode == 0 else [90, a, 90 - a]'),
              labels=E("[str(a) + '°', str(b) + '°', '?'] if mode == 0 else ['', str(a) + '°', '?']")))

add_media('n46-isosceles',
          fig('triangle-angles', 'Trójkąt równoramienny z zaznaczonymi kątami.', when='mode < 2',
              angles=E('[(180 - apex) // 2, (180 - apex) // 2, apex] if mode == 0 else [base, base, 180 - 2 * base]'),
              labels=E("['?', '?', str(apex) + '°'] if mode == 0 else [str(base) + '°', str(base) + '°', '?']")))

add_media('n46-triangle-by-angles',
          fig('triangle-angles', 'Trójkąt z podanymi kątami.', angles=E('angs'),
              labels=E("[str(angs[0]) + '°', str(angs[1]) + '°', str(angs[2]) + '°']")))

add_media('n46-triangle-by-sides',
          fig('triangle-sides', 'Trójkąt z podanymi bokami.', sides=E('sides'),
              labels=E("[str(sides[0]) + ' ' + un, str(sides[1]) + ' ' + un, str(sides[2]) + ' ' + un]")))

# ============================================================================ IV-VI: circle, polygons, symmetry
add_media('n46-circle-diameter',
          fig('circle', 'Koło z zaznaczonym promieniem lub średnicą.',
              draw=E("['diameter'] if toR else ['radius']"),
              labels={'diameter': E("fmt(x) + ' ' + un"), 'radius': E("fmt(x) + ' ' + un")}))

add_media('n46-polygon-parts',
          fig('regular-polygon', 'Wielokąt foremny.', n=E('n'), names=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']))

SYM_PTS = ("[[[0, 0], [3, 0], [3, 3], [0, 3]], [[0, 0], [5, 0], [5, 3], [0, 3]], [[0, 2], [3, 0], [6, 2], [3, 4]], "
           "[[0, 0], [4, 0], [2, 3.46]], [[0, 0], [6, 0], [5, 3], [1, 3]], [[0, 0], [5, 0], [7, 3], [2, 3]]]")
add_media('n46-symmetry-axes',
          fig('polygon', 'Rysunek figury.', when='f < 6', pts=E(SYM_PTS + '[f]')),
          fig('regular-polygon', 'Wielokąt foremny.', when='f == 6', n=E('n')))

# ============================================================================ IV-VI: areas
add_media('n46-area-triangle',
          fig('triangle', 'Trójkąt z podstawą i wysokością.', A=[0, 0], B=[E('a'), 0], C=[E('0 if half == 2 else a // 2'), E('h')],
              feet=[{'label': E("str(h) + ' ' + un"), 'x': E('0 if half == 2 else a // 2')}], baseLabel=E("str(a) + ' ' + un"), names=['', '', '']))

add_media('n46-area-parallelogram',
          fig('polygon', 'Równoległobok z podstawą, bokiem i wysokością.', pts=[[0, 0], [E('a'), 0], [E('a + side - h'), E('h')], [E('side - h'), E('h')]],
              sides=[{'i': 0, 'text': E("str(a) + ' ' + un")}, {'i': 1, 'text': E("str(side) + ' ' + un")}],
              segments=[{'from': [E('side - h'), E('h')], 'to': [E('side - h'), 0], 'text': E("str(h) + ' ' + un")}]))

add_media('n46-area-rhombus-trapezoid',
          fig('polygon', 'Romb z przekątnymi.', when='mode == 0', pts=[[E('e / 2'), 0], [E('e'), E('f / 2')], [E('e / 2'), E('f')], [0, E('f / 2')]],
              segments=[{'from': [0, E('f / 2')], 'to': [E('e'), E('f / 2')], 'text': E("str(e) + ' ' + un")},
                        {'from': [E('e / 2'), 0], 'to': [E('e / 2'), E('f')], 'text': E("str(f) + ' ' + un")}]),
          fig('polygon', 'Trapez z podstawami i wysokością.', when='mode == 1',
              pts=[[0, 0], [E('max(a, b)'), 0], [E('(max(a, b) + min(a, b)) / 2'), E('h')], [E('(max(a, b) - min(a, b)) / 2'), E('h')]],
              sides=[{'i': 0, 'text': E("str(max(a, b)) + ' ' + un")}, {'i': 2, 'text': E("str(min(a, b)) + ' ' + un")}],
              segments=[{'from': [E('(max(a, b) - min(a, b)) / 2'), E('h')], 'to': [E('(max(a, b) - min(a, b)) / 2'), 0], 'text': E("str(h) + ' ' + un")}]))

add_media('n46-area-composite',
          fig('polygon', 'Dwa prostokąty obok siebie.', when='mode == 0', pts=[[0, 0], [E('a'), 0], [E('a'), E('b')], [0, E('b')]],
              extras=[{'pts': [[E('a'), 0], [E('a + c'), 0], [E('a + c'), E('d')], [E('a'), E('d')]], 'fill': 'fill2'}],
              sides=[{'i': 0, 'text': E("str(a) + ' ' + un")}, {'i': 3, 'text': E("str(b) + ' ' + un")}]),
          fig('polygon', 'Prostokąt z wyciętym kwadratem w rogu.', when='mode == 1',
              pts=[[0, 0], [E('a'), 0], [E('a'), E('b - c')], [E('a - c'), E('b - c')], [E('a - c'), E('b')], [0, E('b')]],
              sides=[{'i': 0, 'text': E("str(a) + ' ' + un")}, {'i': 5, 'text': E("str(b) + ' ' + un")}, {'i': 3, 'text': E("str(c) + ' ' + un")}]))

# ============================================================================ IV-VI: solids
add_media('n46-solid-elements',
          fig('solid', 'Bryła o podstawie n-kątnej.', kind=E("'prism' if isp == 0 else 'pyramid'"), n=E('n')))

add_media('n46-cuboid-surface',
          fig('cuboid', 'Prostopadłościan (sześcian) z podanymi krawędziami.', a=E('a if mode == 0 else e'), b=E('b if mode == 0 else e'), c=E('c if mode == 0 else e'),
              labels={'a': E("str(a if mode == 0 else e) + ' ' + un"), 'b': E("str(b if mode == 0 else e) + ' ' + un"), 'c': E("str(c if mode == 0 else e) + ' ' + un")}, when='mode < 2'))

add_media('n46-cuboid-volume',
          fig('cuboid', 'Prostopadłościan z podanymi krawędziami.', a=E('a'), b=E('b if mode != 1 else a'), c=E('c if mode == 0 else (a if mode == 1 else c)'),
              labels={'a': E("str(a) + ' ' + un"), 'b': E("str(b if mode != 1 else a) + ' ' + un"), 'c': E("str(c) + ' ' + un if mode == 0 else ('?' if mode == 2 else str(a) + ' ' + un)")}))

# ============================================================================ VII-VIII: Pythagoras, circle, composite areas
add_media('vh-pyth-basic',
          fig('right-triangle', 'Trójkąt prostokątny z zaznaczonymi bokami; znak zapytania oznacza szukany bok.', a=E('a'), b=E('b'),
              labels={'a': E("str(a) + ' ' + un"), 'b': E("(str(b) + ' ' + un) if mode == 0 else '?'"), 'c': E("'?' if mode == 0 else (str(c) + ' ' + un)")}))

add_media('vh-pyth-context',
          fig('right-triangle', 'Trójkąt prostokątny modelujący sytuację z zadania; znak zapytania oznacza szukaną długość.', a=E('a'), b=E('b'),
              labels={'a': E('str(a)'), 'b': E("'?' if sc == 1 or sc == 2 else str(b)"), 'c': E("'?' if sc == 0 or sc == 3 else str(c)")}))

add_media('vh-circle-calc',
          fig('circle', 'Koło z zaznaczonym promieniem lub średnicą.', draw=E("['diameter'] if mode == 3 else ['radius']"),
              labels={'radius': E("'r = ?' if mode == 2 else 'r = ' + str(r) + ' ' + un"), 'diameter': E("'d = ' + str(2 * r) + ' ' + un")}))

add_media('vh-regular-angle',
          fig('regular-polygon', 'Wielokąt foremny.', when='mode < 2', n=E('n'), angles=[{'i': 0, 'text': '?', 'show': E('mode == 0')}]))

add_media('vh-area-decompose',
          fig('polygon', 'Prostokąt z wyciętym narożnikiem.', when='mode == 0',
              pts=[[0, 0], [E('a'), 0], [E('a'), E('b - dd')], [E('a - cc'), E('b - dd')], [E('a - cc'), E('b')], [0, E('b')]],
              sides=[{'i': 0, 'text': E("str(a) + ' ' + un")}, {'i': 5, 'text': E("str(b) + ' ' + un")}, {'i': 2, 'text': E("str(cc) + ' ' + un")}, {'i': 3, 'text': E("str(dd) + ' ' + un")}]),
          fig('polygon', 'Trapez prostokątny.', when='mode == 1', pts=[[0, 0], [E('a + cc'), 0], [E('a'), E('2 * h')], [0, E('2 * h')]],
              sides=[{'i': 0, 'text': E("str(a + cc) + ' ' + un")}, {'i': 2, 'text': E("str(a) + ' ' + un")}, {'i': 3, 'text': E("str(2 * h) + ' ' + un")}]),
          fig('polygon', 'Kwadrat z połączonymi środkami boków.', when='mode == 2', pts=[[0, 0], [2, 0], [2, 2], [0, 2]],
              extras=[{'pts': [[1, 0], [2, 1], [1, 2], [0, 1]], 'fill': 'fill2'}]))

# ============================================================================ VII-VIII: symmetry, lattice, solids
VH_SYM_PTS = ("[[[0, 0], [3, 0], [3, 3], [0, 3]], [[0, 0], [5, 0], [5, 3], [0, 3]], [[0, 0], [4, 0], [2, 3.46]], [[1, 0], [3, 0], [2, 3]], "
              "[[0, 2], [3, 0], [6, 2], [3, 4]], [[0, 0], [5, 0], [7, 3], [2, 3]], [[0, 0], [6, 0], [5, 3], [1, 3]], [[0, 0], [4, 0], [5, 2.9], [2, 4.7], [-1, 2.9]], "
              "[[0, 0], [2, 0], [3, 1.73], [2, 3.46], [0, 3.46], [-1, 1.73]], [[0, 0], [5, 0], [1.5, 3]], [[0, 1.5], [2, 0], [4, 1.5], [2, 5]]]")
add_media('vh-symmetry-axes', fig('polygon', 'Rysunek figury.', pts=E(VH_SYM_PTS + '[i]')))
add_media('vh-symmetry-centre', fig('polygon', 'Rysunek figury.', pts=E(VH_SYM_PTS + '[i]')))

add_media('vh-lattice-vertex',
          fig('coordinate-plane', 'Układ współrzędnych z zaznaczonymi punktami.',
              xMin=E('min(x, -x, 0) - 2'), xMax=E('max(x + p + q, -x, 0) + 2'), yMin=E('min(y, -y, 0) - 2'), yMax=E('max(y + h, -y, 0) + 2'),
              points=[{'label': 'A', 'x': E('x'), 'y': E('y')},
                      {'label': 'B', 'x': E('x + p'), 'y': E('y'), 'show': E('mode == 0')},
                      {'label': 'C', 'x': E('x + p + q'), 'y': E('y + h'), 'show': E('mode == 0')}]))

add_media('vh-lattice-area',
          fig('coordinate-plane', 'Układ współrzędnych z figurą.',
              xMin=E('x1 - 1'), xMax=E('x1 + max(w, dx, t[0]) + 1'), yMin=E('y1 - 1'), yMax=E('y1 + max(h, t[1]) + 1'),
              polygons=[{'pts': [[E('x1'), E('y1')], [E('x1 + w'), E('y1')], [E('x1 + w'), E('y1 + h')], [E('x1'), E('y1 + h')]], 'show': E('mode == 0')},
                        {'pts': [[E('x1'), E('y1')], [E('x1 + w'), E('y1')], [E('x1 + dx'), E('y1 + h')]], 'show': E('mode == 1')},
                        {'pts': [[E('x1'), E('y1')], [E('x1 + t[0]'), E('y1')], [E('x1'), E('y1 + t[1]')]], 'show': E('mode == 2')}]))

add_media('vh-solid-counts',
          fig('solid', 'Bryła o podstawie n-kątnej.', when='mode < 2', kind=E("'prism' if mode == 0 else 'pyramid'"), n=E('n')))

add_media('vh-pyramid-heights',
          fig('solid', 'Ostrosłup prawidłowy czworokątny z wysokością i wysokością ściany bocznej.', kind='pyramid', n=4, show=['height', 'slant'],
              labels={'h': E("'H = ?' if mode == 1 else 'H = ' + str(hh) + ' ' + un"), 's': E("'h = ?' if mode == 0 else 'h = ' + str(hs) + ' ' + un"),
                      'e': E("'a = ?' if mode == 2 else 'a = ' + str(2 * m) + ' ' + un")}))

add_media('vh-prism',
          fig('solid', 'Graniastosłup prosty o podstawie trójkątnej.', kind='prism', n=3, show=['height'],
              labels={'h': E("'H = ?' if mode == 2 else 'H = ' + str(hh) + ' ' + un")}))

add_media('vh-pyramid',
          fig('solid', 'Ostrosłup prawidłowy czworokątny.', kind='pyramid', n=4, show=['height', 'slant'],
              labels={'h': E("'H = ' + str(hh) + ' ' + un if mode == 0 or mode == 2 else 'H = ?'"), 's': E("'h = ' + str(hs) + ' ' + un if mode == 1 or mode == 3 else 'h = ?'"),
                      'e': E("'a = ' + str(a) + ' ' + un")}))

add_media('vh-congruent-find',
          fig('triangle-angles', 'Trójkąt ABC z zaznaczonymi kątami A i B.', when='mode == 0', angles=E('[al, be, ga]'),
              labels=[E("str(al) + '°'"), E("str(be) + '°'"), ''], names=['A', 'B', 'C']),
          fig('triangle-sides', 'Trójkąt ABC z podanymi bokami.', when='mode == 1', sides=[E('a'), E('b'), E('c')],
              labels=[E("str(a) + ' cm'"), E("str(b) + ' cm'"), E("str(c) + ' cm'")], names=['A', 'B', 'C']))
