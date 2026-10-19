"""Stage IV-VI, area 4 (Figury), part 2: perimeters, areas, coordinates, solids.  Objectives: IV-VI.4.14-4.22."""
from dsl import *

S = 'IV-VI'
A4 = 'IV-VI.4'
UN = "choice(['mm', 'cm', 'dm', 'm'])"

# ============================================================================ obwody i pola (4.14, 4.15)
skill('n46-perimeter-polygon', S, 'Obwód wielokąta', ['IV-VI.4.15'],
      [lvl('Czworokąt', k=4), lvl('Pięciokąt i sześciokąt', k=6)],
      [('n', 'randint(4, k)'), ('xs', 'sample(2, 20, 6)'), ('sides', 'take(xs, n)'), ('un', UN),
       ('names', "['', '', '', '', 'Czworokąt', 'Pięciokąt', 'Sześciokąt']"),
       ('lst', "join(sides, ' ' + un + ', ') + ' ' + un")],
      quantity('@{names[n]} ma boki o długościach: @{lst}. Oblicz jego obwód.', 'sum(sides)', 'un',
               [('idea', 'Obwód to suma długości wszystkich boków.'), ('compute', "@{join(sides, ' + ')} = @{sum(sides)} @{un}")], unit_expr=True),
      min_distinct=40, area=A4, prereq=['n46-dec-add'])

skill('n46-perimeter-regular', S, 'Obwód kwadratu i trójkąta równobocznego', ['IV-VI.4.15'],
      [lvl('Z długości boku', rev=0), lvl('Długość boku z obwodu', rev=1)],
      [('f', 'randint(0, 2)'), ('side', 'randint(2, 25)'), ('n', '[3, 4, 6][f]'), ('nm', "['trójkąta równobocznego', 'kwadratu', 'sześciokąta foremnego'][f]"), ('un', UN),
       ('per', 'n * side'),
       ('txt', "('Bok ' + ['trójkąta równobocznego', 'kwadratu', 'sześciokąta foremnego'][f] + ' ma długość ' + str(side) + ' ' + un + '. Oblicz obwód.') if rev == 0 else "
               "('Obwód ' + ['trójkąta równobocznego', 'kwadratu', 'sześciokąta foremnego'][f] + ' wynosi ' + str(per) + ' ' + un + '. Ile wynosi długość jego boku?')"),
       ('ans', 'per if rev == 0 else side')],
      quantity('@{txt}', 'ans', 'un', [('idea', "@{('Obwód = liczba boków · długość boku.' if rev == 0 else 'Długość boku = obwód : liczba boków.')}"),
                                      ('compute', "@{(str(n) + ' · ' + str(side) + ' = ' + str(per) if rev == 0 else str(per) + ' : ' + str(n) + ' = ' + str(side))}")], unit_expr=True),
      min_distinct=40, area=A4, prereq=['n46-perimeter-polygon'])

skill('n46-perimeter-unknown', S, 'Brakujący bok prostokąta', ['IV-VI.4.15'],
      [lvl('Obwód i jeden bok')],
      [('a', 'randint(3, 20)'), ('b', 'randint(2, 20)'), ('per', '2 * (a + b)'), ('un', UN)],
      quantity('Obwód prostokąta wynosi @{per} @{un}, a jeden z jego boków ma @{a} @{un}. Ile wynosi długość drugiego boku?', 'b', 'un',
               [('idea', 'Obwód prostokąta to 2 · (a + b). Połowa obwodu to a + b.'), ('compute', '@{per} : 2 = @{per // 2}; @{per // 2} − @{a} = @{b}')], unit_expr=True,
               errors=[('half_only', Qty('per // 2', 'un', True), 'To jest suma dwóch różnych boków. Odejmij jeszcze znany bok.')]),
      constraints=['a != b'], selfCheck=['2 * (a + b) == per'], min_distinct=40, area=A4, prereq=['n46-perimeter-polygon'])

skill('n46-area-rect', S, 'Pole prostokąta i kwadratu', ['IV-VI.4.14'],
      [lvl('Prostokąt', mode=0, dec=0), lvl('Kwadrat', mode=1, dec=0), lvl('Boki z ułamkami dziesiętnymi', mode=0, dec=1)],
      [('a', 'randint(2, 30) / pow(10, dec) if dec > 0 else randint(2, 30)'), ('b', 'randint(2, 30) / pow(10, dec) if dec > 0 else randint(2, 30)'), ('un', UN),
       ('ar', 'a * a if mode == 1 else a * b')],
      quantity("@{('Kwadrat ma bok długości ' + fmt(a) + ' ' + un + '. Oblicz jego pole.' if mode == 1 else 'Prostokąt ma boki ' + fmt(a) + ' ' + un + ' i ' + fmt(b) + ' ' + un + '. Oblicz jego pole.')}", 'ar', "un + '²'",
               [('idea', 'Pole prostokąta to iloczyn jego boków (kwadratu – bok razy bok).'), ('compute', "@{(fmt(a) + ' · ' + fmt(a) if mode == 1 else fmt(a) + ' · ' + fmt(b))} = @{fmt(ar)} @{un}²")], unit_expr=True,
               errors=[('perimeter', Qty('2 * (a + b) if mode == 0 else 4 * a', "un + '²'", True), 'To jest obwód. Pole to iloczyn boków.', '(2 * (a + b) if mode == 0 else 4 * a) != ar')],
               media=[{'type': 'figure', 'kind': 'rect', 'essential': False, 'alt': 'Prostokąt o bokach @{a} i @{b}.', 'params': {'w': E('a'), 'h': E('a if mode == 1 else b'), 'unit': E('un')}}]),
      constraints=['mode == 1 or a != b', 'denom(ar) in divisors(10000)'], min_distinct=40, area=A4, prereq=['n46-dec-mul'])

skill('n46-area-triangle', S, 'Pole trójkąta', ['IV-VI.4.14'],
      [lvl('Podstawa i wysokość (parzysty iloczyn)', half=0), lvl('Dowolne liczby', half=1), lvl('Trójkąt prostokątny', half=2)],
      [('a', 'randint(2, 20)'), ('h', 'randint(2, 20)'), ('un', UN), ('ar', 'a * h / 2')],
      quantity("@{('Podstawa trójkąta ma ' + str(a) + ' ' + un + ', a wysokość poprowadzona do tej podstawy ' + str(h) + ' ' + un + '. Oblicz pole trójkąta.' if half < 2 else 'Przyprostokątne trójkąta prostokątnego mają ' + str(a) + ' ' + un + ' i ' + str(h) + ' ' + un + '. Oblicz pole tego trójkąta.')}",
               'ar', "un + '²'",
               [('idea', 'Pole trójkąta = połowa iloczynu podstawy i wysokości (w trójkącie prostokątnym – połowa iloczynu przyprostokątnych).'),
                ('compute', '@{a} · @{h} : 2 = @{ar|dec}')], unit_expr=True,
               errors=[('forgot_half', Qty('a * h', "un + '²'", True), 'Trójkąt to połowa prostokąta o tej samej podstawie i wysokości – podziel iloczyn przez 2.')]),
      constraints=['half != 0 or (a * h) % 2 == 0', 'a != h'], min_distinct=40, area=A4, prereq=['n46-area-rect', 'n46-height-id'])

skill('n46-area-parallelogram', S, 'Pole równoległoboku', ['IV-VI.4.14'],
      [lvl('Podstawa i wysokość')],
      [('a', 'randint(3, 25)'), ('h', 'randint(2, 15)'), ('side', 'h + randint(1, 6)'), ('un', UN)],
      quantity('Równoległobok ma podstawę długości @{a} @{un}, drugi bok długości @{side} @{un} i wysokość opuszczoną na podstawę równą @{h} @{un}. Oblicz jego pole.', 'a * h', "un + '²'",
               [('idea', 'Pole równoległoboku = podstawa · wysokość opuszczona na tę podstawę. Drugi bok nie jest potrzebny.'), ('compute', '@{a} · @{h} = @{a * h}')], unit_expr=True,
               errors=[('use_side', Qty('a * side', "un + '²'", True), 'Do pola potrzebna jest wysokość (prostopadła do podstawy), a nie drugi bok.')]),
      min_distinct=40, area=A4, prereq=['n46-area-rect'])

skill('n46-area-rhombus-trapezoid', S, 'Pole rombu i trapezu', ['IV-VI.4.14'],
      [lvl('Romb z przekątnych', mode=0), lvl('Trapez', mode=1)],
      [('e', '2 * randint(2, 10)'), ('f', 'randint(2, 14)'), ('a', 'randint(3, 14)'), ('b', 'randint(2, 14)'), ('h', '2 * randint(1, 6)'), ('un', UN),
       ('ar', 'e * f / 2 if mode == 0 else (a + b) * h / 2')],
      quantity("@{('Przekątne rombu mają długości ' + str(e) + ' ' + un + ' i ' + str(f) + ' ' + un + '. Oblicz pole rombu.' if mode == 0 else 'Podstawy trapezu mają ' + str(a) + ' ' + un + ' i ' + str(b) + ' ' + un + ', a jego wysokość ' + str(h) + ' ' + un + '. Oblicz pole trapezu.')}",
               'ar', "un + '²'",
               [('idea', "@{('Pole rombu = połowa iloczynu przekątnych.' if mode == 0 else 'Pole trapezu = połowa iloczynu sumy podstaw i wysokości.')}"),
                ('compute', "@{(str(e) + ' · ' + str(f) + ' : 2 = ' + fmt(ar) if mode == 0 else '(' + str(a) + ' + ' + str(b) + ') · ' + str(h) + ' : 2 = ' + fmt(ar))}")], unit_expr=True),
      constraints=['mode != 1 or a != b'], min_distinct=40, area=A4, prereq=['n46-area-triangle'])

skill('n46-area-composite', S, 'Pole figury złożonej', ['IV-VI.4.14'],
      [lvl('Dwa prostokąty', mode=0), lvl('Prostokąt z wyciętym kwadratem', mode=1)],
      [('a', 'randint(5, 14)'), ('b', 'randint(4, 12)'), ('c', 'randint(2, 4)'), ('d', 'randint(2, 6)'), ('un', UN),
       ('ar', 'a * b + c * d if mode == 0 else a * b - c * c')],
      quantity("@{('Figura składa się z dwóch prostokątów: jeden ma wymiary ' + str(a) + ' ' + un + ' × ' + str(b) + ' ' + un + ', a drugi ' + str(c) + ' ' + un + ' × ' + str(d) + ' ' + un + '. Prostokąty się nie nakładają. Oblicz pole figury.' if mode == 0 else 'Z prostokąta o wymiarach ' + str(a) + ' ' + un + ' × ' + str(b) + ' ' + un + ' wycięto kwadrat o boku ' + str(c) + ' ' + un + '. Oblicz pole pozostałej figury.')}",
               'ar', "un + '²'",
               [('idea', "@{('Pola figur składowych dodajemy.' if mode == 0 else 'Od pola prostokąta odejmujemy pole wyciętego kwadratu.')}"),
                ('compute', "@{(str(a * b) + ' + ' + str(c * d) + ' = ' + str(ar) if mode == 0 else str(a * b) + ' − ' + str(c * c) + ' = ' + str(ar))}")], unit_expr=True),
      constraints=['mode != 1 or (c < a and c < b)'], min_distinct=40, area=A4, prereq=['n46-area-rect'])

skill('n46-area-unknown-side', S, 'Brakujący bok lub wysokość', ['IV-VI.4.14'],
      [lvl('Prostokąt', mode=0), lvl('Trójkąt', mode=1)],
      [('a', 'randint(3, 20)'), ('x', 'randint(2, 15)'), ('un', UN),
       ('txt', "('Pole prostokąta wynosi ' + str(a * x) + ' ' + un + '², a jeden z jego boków ' + str(a) + ' ' + un + '. Ile wynosi długość drugiego boku?') if mode == 0 else "
               "('Pole trójkąta wynosi ' + str(a * x // 2) + ' ' + un + '², a jego podstawa ma ' + str(a) + ' ' + un + '. Ile wynosi wysokość poprowadzona do tej podstawy?')")],
      quantity('@{txt}', 'x', 'un',
               [('idea', "@{('Pole = bok · bok, więc drugi bok to pole : znany bok.' if mode == 0 else 'Pole = podstawa · wysokość : 2, więc wysokość = 2 · pole : podstawa.')}"),
                ('conclude', 'Odpowiedź: @{x} @{un}.')], unit_expr=True),
      constraints=['mode != 1 or (a * x) % 2 == 0'], min_distinct=40, area=A4, prereq=['n46-area-triangle'])

# ============================================================================ układ współrzędnych (4.16, 4.17)
skill('n46-coord-read', S, 'Współrzędne punktu', ['IV-VI.4.16'],
      [lvl('Pierwsza ćwiartka', lo=0, hi=8), lvl('Cały układ współrzędnych', lo=-7, hi=7)],
      [('x', 'randint(lo, hi)'), ('y', 'randint(lo, hi)')],
      task('point-input', 'Jakie współrzędne ma punkt A zaznaczony w układzie współrzędnych? Najpierw podaj współrzędną x (poziomą), potem y (pionową).', Pt('x', 'y'),
           [('idea', 'Odczytaj, ile kratek w prawo (lub w lewo) od początku układu, a potem ile w górę (lub w dół).'), ('conclude', 'A = (@{x}, @{y})')],
           media=[{'type': 'figure', 'kind': 'coordinate-plane', 'essential': True, 'alt': 'Układ współrzędnych z zaznaczonym punktem A.',
                   'params': {'min': E('lo - 1'), 'max': E('hi + 1'), 'points': [{'label': 'A', 'x': E('x'), 'y': E('y')}]}}],
           errors=[('swapped', Pt('y', 'x'), 'Najpierw podajemy współrzędną poziomą x, potem pionową y.', 'x != y')]),
      min_distinct=40, area=A4, prereq=['n46-int-compare'])

skill('n46-coord-distance', S, 'Odległość punktów o wspólnej współrzędnej', ['IV-VI.4.17'],
      [lvl('Pierwsza ćwiartka', lo=0, hi=12), lvl('Cały układ współrzędnych', lo=-10, hi=10)],
      [('horiz', 'randint(0, 1) == 1'), ('c', 'randint(lo, hi)'), ('p', 'randint(lo, hi)'), ('q', 'randint(lo, hi)'),
       ('ax', 'p if horiz else c'), ('ay', 'c if horiz else p'), ('bx', 'q if horiz else c'), ('by', 'c if horiz else q')],
      number('Punkty A(@{ax}, @{ay}) i B(@{bx}, @{by}) leżą w układzie współrzędnych. Jaka jest długość odcinka AB (w jednostkach układu)?', 'abs(p - q)',
             [('idea', 'Punkty mają jedną współrzędną taką samą, więc leżą na prostej poziomej lub pionowej. Odległość to różnica drugich współrzędnych.'),
              ('compute', '|@{p} − (@{q})| = @{abs(p - q)}')],
             errors=[('sum_instead', Int('abs(p) + abs(q)'), 'Jeśli obie liczby leżą po tej samej stronie zera, nie dodajemy ich – odejmujemy.', 'abs(p) + abs(q) != abs(p - q)')]),
      constraints=['p != q'], min_distinct=40, area=A4, prereq=['n46-coord-read', 'n46-int-distance'])

skill('n46-coord-rectangle', S, 'Czwarty wierzchołek prostokąta', ['IV-VI.4.16', 'IV-VI.4.17'],
      [lvl('Pierwsza ćwiartka', lo=0, hi=9), lvl('Cały układ współrzędnych', lo=-8, hi=8)],
      [('x1', 'randint(lo, hi - 3)'), ('y1', 'randint(lo, hi - 3)'), ('w', 'randint(2, 6)'), ('h', 'randint(2, 6)')],
      task('point-input', 'Trzy wierzchołki prostokąta ABCD o bokach równoległych do osi układu to A(@{x1}, @{y1}), B(@{x1 + w}, @{y1}) i C(@{x1 + w}, @{y1 + h}). Jakie współrzędne ma wierzchołek D?', Pt('x1', 'y1 + h'),
           [('idea', 'Wierzchołek D leży nad A (taka sama współrzędna x) i obok C (taka sama współrzędna y).'), ('conclude', 'D = (@{x1}, @{y1 + h})')],
           errors=[('wrong_corner', Pt('x1 + w', 'y1'), 'To wierzchołek B. D leży naprzeciwko B.')]),
      constraints=['x1 + w <= hi', 'y1 + h <= hi'], min_distinct=40, area=A4, prereq=['n46-coord-read'])

# ============================================================================ bryły (4.18-4.22)
SOLIDS = "['prostopadłościan', 'sześcian', 'graniastosłup trójkątny', 'ostrosłup czworokątny', 'walec', 'stożek', 'kula']"
skill('n46-solid-recognize', S, 'Rozpoznaj bryłę', ['IV-VI.4.18'],
      [lvl('Opis bryły')],
      [('names', SOLIDS),
       ('descs', "[['Ma 6 ścian, a każda ściana jest prostokątem.', 'Ma 8 wierzchołków i 12 krawędzi, a jego ściany to prostokąty.'], "
                 "['Ma 6 ścian i wszystkie są kwadratami.', 'Wszystkie jego 12 krawędzi są jednakowej długości.'], "
                 "['Ma dwie podstawy w kształcie trójkątów, a ściany boczne są prostokątami.', 'Ma 5 ścian i 9 krawędzi.'], "
                 "['Ma podstawę w kształcie kwadratu, a ściany boczne to trójkąty o wspólnym wierzchołku.', 'Ma 5 wierzchołków i 8 krawędzi.'], "
                 "['Ma dwie podstawy w kształcie kół i jedną powierzchnię zakrzywioną.', 'Puszka konserwowa ma taki kształt.'], "
                 "['Ma jedną podstawę w kształcie koła i jeden wierzchołek.', 'Lejek do wlewania płynów (rożek lodów) ma taki kształt.'], "
                 "['Nie ma ani ścian płaskich, ani krawędzi.', 'Piłka do koszykówki ma taki kształt.']]"),
       ('s', 'randint(0, 6)'), ('d', 'randint(0, 1)')],
      choice('Jaką bryłę opisuje zdanie: „@{descs[s][d]}”?', 'names[s]', ['names[(s + 1) % 7]', 'names[(s + 3) % 7]', 'names[(s + 5) % 7]'],
             [('idea', 'Zwróć uwagę na kształt podstaw i ścian bocznych oraz liczbę ścian, krawędzi i wierzchołków.'), ('conclude', 'To @{names[s]}.')]),
      min_distinct=14, area=A4,
      intro='Graniastosłupy mają dwie takie same podstawy i ściany boczne w kształcie prostokątów. Ostrosłupy mają jedną podstawę, a ściany boczne to trójkąty. Walec, stożek i kula to bryły obrotowe.')

skill('n46-solid-elements', S, 'Wierzchołki, krawędzie i ściany', ['IV-VI.4.19'],
      [lvl('Graniastosłupy', pyr=0, ask=0), lvl('Ostrosłupy', pyr=1, ask=0), lvl('Dowolna bryła, dowolny element', pyr=2, ask=1)],
      [('n', 'randint(3, 8)'), ('isp', 'randint(0, 1) if pyr == 2 else pyr'), ('el', 'randint(0, 2)'),
       ('kind', "('graniastosłup' if isp == 0 else 'ostrosłup')"),
       ('base', "['trójkątną', 'czworokątną', 'pięciokątną', 'sześciokątną', 'siedmiokątną', 'ośmiokątną'][n - 3]"),
       ('what', "['wierzchołków', 'krawędzi', 'ścian'][el]"),
       ('cnt', '[[2 * n, 3 * n, n + 2], [n + 1, 2 * n, n + 1]][isp][el]')],
      number("Ile @{what} ma @{('graniastosłup' if isp == 0 else 'ostrosłup')} o podstawie @{('trójkątnej' if n == 3 else ('czworokątnej' if n == 4 else ('pięciokątnej' if n == 5 else ('sześciokątnej' if n == 6 else ('siedmiokątnej' if n == 7 else 'ośmiokątnej')))))}?", 'cnt',
             [('idea', "@{('Graniastosłup o podstawie n-kątnej ma 2n wierzchołków, 3n krawędzi i n + 2 ścian.' if isp == 0 else 'Ostrosłup o podstawie n-kątnej ma n + 1 wierzchołków, 2n krawędzi i n + 1 ścian.')}"),
              ('conclude', 'Odpowiedź: @{cnt}.')]),
      selfCheck=['[2 * n - 3 * n + n + 2, n + 1 - 2 * n + n + 1][isp] == 2'], min_distinct=18, area=A4, prereq=['n46-solid-recognize'])

skill('n46-net-solid', S, 'Siatka bryły', ['IV-VI.4.20'],
      [lvl('Z czego składa się siatka?', md=40, dirn=0), lvl('Siatka danej bryły', md=40, dirn=1)],
      [('names', "['sześcian', 'graniastosłup sześciokątny', 'ostrosłup czworokątny prawidłowy', 'graniastosłup trójkątny', 'prostopadłościan', 'ostrosłup trójkątny prawidłowy']"),
       ('nets', "['sześciu jednakowych kwadratów', 'dwóch sześciokątów foremnych i sześciu prostokątów', 'jednego kwadratu i czterech trójkątów równoramiennych', "
                "'dwóch trójkątów i trzech prostokątów', 'sześciu prostokątów (trzy pary jednakowych)', 'czterech trójkątów równobocznych']"),
       ('s', 'randint(0, 5)'), ('sh', 'shuffle([1, 2, 3, 4, 5])')],
      choice("@{('Siatka składa się z ' + nets[s] + '. Jaką bryłę można z niej zbudować?' if dirn == 0 else 'Z jakich figur składa się siatka bryły: ' + names[s] + '?')}",
             'names[s] if dirn == 0 else nets[s]',
             ['names[(s + sh[0]) % 6] if dirn == 0 else nets[(s + sh[0]) % 6]', 'names[(s + sh[1]) % 6] if dirn == 0 else nets[(s + sh[1]) % 6]', 'names[(s + sh[2]) % 6] if dirn == 0 else nets[(s + sh[2]) % 6]'],
             [('idea', 'Policz i nazwij ściany: podstawy i ściany boczne wskażą rodzaj bryły.'), ('conclude', 'Siatka bryły @{names[s]} składa się z @{nets[s]}.')]),
      area=A4, prereq=['n46-solid-elements'])

skill('n46-net-faces', S, 'Ile figur ma siatka?', ['IV-VI.4.20'],
      [lvl('Liczba ścian siatki', md=10)],
      [('names', "['sześcian', 'graniastosłup sześciokątny', 'ostrosłup czworokątny prawidłowy', 'graniastosłup trójkątny', 'prostopadłościan', 'ostrosłup trójkątny prawidłowy', 'graniastosłup pięciokątny', 'ostrosłup sześciokątny prawidłowy']"),
       ('faces', '[6, 8, 5, 5, 6, 4, 7, 7]'), ('s', 'randint(0, 7)'), ('ph', 'randint(0, 1)')],
      number("@{('Z ilu figur (ścian) składa się siatka bryły: ' + names[s] + '?' if ph == 0 else 'Ile wielokątów trzeba wyciąć z papieru, aby zbudować siatkę bryły: ' + names[s] + '?')}", 'faces[s]',
             [('idea', 'Siatka ma tyle figur, ile ścian ma bryła: podstawy i ściany boczne.'), ('conclude', 'Odpowiedź: @{faces[s]}.')]),
      area=A4, prereq=['n46-net-solid'])

skill('n46-cuboid-surface', S, 'Pole powierzchni prostopadłościanu', ['IV-VI.4.21'],
      [lvl('Prostopadłościan', mode=0), lvl('Sześcian', md=30, mode=1), lvl('Krawędź sześcianu z pola powierzchni', md=30, mode=2)],
      [('a', 'randint(2, 12)'), ('b', 'randint(2, 12)'), ('c', 'randint(2, 12)'), ('e', 'randint(2, 9)'), ('un', UN),
       ('ans', '2 * (a * b + b * c + a * c) if mode == 0 else (6 * e * e if mode == 1 else e)'),
       ('txt', "('Prostopadłościan ma krawędzie ' + str(a) + ' ' + un + ', ' + str(b) + ' ' + un + ' i ' + str(c) + ' ' + un + '. Oblicz pole jego powierzchni całkowitej.') if mode == 0 else "
               "(('Krawędź sześcianu ma ' + str(e) + ' ' + un + '. Oblicz pole jego powierzchni całkowitej.') if mode == 1 else "
               "('Pole powierzchni całkowitej sześcianu wynosi ' + str(6 * e * e) + ' ' + un + '². Ile wynosi długość krawędzi tego sześcianu?'))")],
      quantity('@{txt}', 'ans', "un + '²' if mode < 2 else un",
               [('idea', "@{('Powierzchnia składa się z 6 prostokątów: dwa o wymiarach a×b, dwa b×c i dwa a×c.' if mode == 0 else ('Sześcian ma 6 jednakowych kwadratowych ścian.' if mode == 1 else 'Pole jednej ściany to pole powierzchni : 6, a krawędź to bok tej ściany.'))}"),
                ('conclude', 'Odpowiedź: @{ans}.')], unit_expr=True,
               errors=[('one_face', Qty('a * b if mode == 0 else e * e', "un + '²'", True), 'To pole tylko jednej ściany. Powierzchnia całkowita to wszystkie ściany.', 'mode < 2')]),
      constraints=['len(uniq([a, b, c])) == 3 or mode > 0'], min_distinct=40, area=A4, prereq=['n46-area-rect', 'n46-net-solid'])

skill('n46-cuboid-volume', S, 'Objętość prostopadłościanu', ['IV-VI.4.22'],
      [lvl('Prostopadłościan', mode=0), lvl('Sześcian', mode=1), lvl('Brakująca krawędź', mode=2)],
      [('a', 'randint(2, 12)'), ('b', 'randint(2, 12)'), ('c', 'randint(2, 12)'), ('un', UN),
       ('txt', "('Prostopadłościan ma krawędzie ' + str(a) + ' ' + un + ', ' + str(b) + ' ' + un + ' i ' + str(c) + ' ' + un + '. Oblicz jego objętość.') if mode == 0 else "
               "(('Krawędź sześcianu ma ' + str(a) + ' ' + un + '. Oblicz jego objętość.') if mode == 1 else "
               "('Objętość prostopadłościanu wynosi ' + str(a * b * c) + ' ' + un + '³. Dwie krawędzie mają ' + str(a) + ' ' + un + ' i ' + str(b) + ' ' + un + '. Ile wynosi trzecia krawędź?'))"),
       ('ans', 'a * b * c if mode == 0 else (a * a * a if mode == 1 else c)')],
      quantity('@{txt}', 'ans', "un + '³' if mode < 2 else un",
               [('idea', "@{('Objętość = długość · szerokość · wysokość.' if mode < 2 else 'Objętość : (a · b) daje trzecią krawędź.')}"), ('conclude', 'Odpowiedź: @{ans}.')], unit_expr=True),
      constraints=['mode != 2 or len(uniq([a, b, c])) == 3'], min_distinct=40, area=A4, prereq=['n46-cuboid-surface'])

skill('n46-cuboid-compound', S, 'Objętość bryły złożonej i pojemność', ['IV-VI.4.22', 'IV-VI.2.5'],
      [lvl('Dwa prostopadłościany', mode=0), lvl('Akwarium: litry', mode=1)],
      [('a', 'randint(2, 8)'), ('b', 'randint(2, 8)'), ('c', 'randint(2, 8)'), ('d', 'randint(2, 5)'), ('l', 'randint(2, 6) * 10'), ('w', 'randint(2, 5) * 10'), ('hh', 'randint(2, 5) * 10'),
       ('vol', 'l * w * hh'),
       ('txt', "('Bryła składa się z dwóch prostopadłościanów, które się nie nakładają: pierwszy ma wymiary ' + str(a) + ' cm × ' + str(b) + ' cm × ' + str(c) + ' cm, a drugi ' + str(d) + ' cm × ' + str(b) + ' cm × ' + str(c) + ' cm. Oblicz objętość bryły w cm³.') if mode == 0 else "
               "('Akwarium ma wymiary dna ' + str(l) + ' cm × ' + str(w) + ' cm i wysokość ' + str(hh) + ' cm. Ile litrów wody zmieści się w nim po brzegi? (1 l = 1000 cm³)')"),
       ('ans', '(a + d) * b * c if mode == 0 else vol / 1000'), ('u', "'cm³' if mode == 0 else 'l'")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('Objętości dodajemy: a·b·c + d·b·c.' if mode == 0 else 'Najpierw objętość w cm³, potem na litry: 1000 cm³ = 1 l.')}"),
                ('conclude', "@{('Razem: ' + str(ans) + ' cm³.' if mode == 0 else str(vol) + ' cm³ : 1000 = ' + fmt(ans) + ' l.')}")], unit_expr=True),
      constraints=['denom(ans) == 1 or mode == 0'], min_distinct=40, area=A4, prereq=['n46-cuboid-volume', 'n46-capacity-units'])

# ============================================================================ ścieżka
un = Unit(S, 'n46-u22', 'Proste i kąty', 'Punkt, prosta, kąty, proste prostopadłe i równoległe.', 'angle', area=A4)
un.learn('n46-line-terms').learn('n46-angle-types').learn('n46-angle-convex').learn('n46-angle-vertex')
un.review('Powtórka: figury i kąty', ['n46-line-terms', 'n46-angle-types', 'n46-angle-vertex'])
un.learn('n46-line-relations').learn('n46-angle-pairs')
un.checkpoint(['n46-line-terms', 'n46-angle-types', 'n46-angle-vertex', 'n46-line-relations', 'n46-angle-pairs'])

un = Unit(S, 'n46-u23', 'Trójkąty i koła', 'Rodzaje trójkątów, suma kątów, nierówność trójkąta oraz koło i okrąg.', 'triangle', area=A4)
un.learn('n46-polygon-parts').learn('n46-circle-diameter').learn('n46-circle-terms')
un.learn('n46-triangle-by-angles').learn('n46-triangle-by-sides').learn('n46-triangle-angle').learn('n46-isosceles')
un.learn('n46-triangle-exists').learn('n46-triangle-third-side')
un.checkpoint(['n46-circle-diameter', 'n46-triangle-by-angles', 'n46-triangle-by-sides', 'n46-triangle-angle', 'n46-isosceles', 'n46-triangle-exists'])

un = Unit(S, 'n46-u24', 'Czworokąty i symetria', 'Własności czworokątów, osie symetrii, wysokości.', 'square', area=A4)
un.learn('n46-quad-properties').learn('n46-quad-angle').learn('n46-symmetry-axes').learn('n46-height-id')
un.checkpoint(['n46-quad-properties', 'n46-quad-angle', 'n46-symmetry-axes', 'n46-height-id'])

un = Unit(S, 'n46-u25', 'Obwody i pola figur', 'Obwód wielokąta, pola prostokąta, trójkąta, równoległoboku, rombu i trapezu.', 'area', area=A4)
un.learn('n46-perimeter-polygon').learn('n46-perimeter-regular').learn('n46-perimeter-unknown')
un.review('Powtórka: obwody', ['n46-perimeter-polygon', 'n46-perimeter-regular', 'n46-perimeter-unknown'])
un.learn('n46-area-rect').learn('n46-area-triangle').learn('n46-area-parallelogram').learn('n46-area-rhombus-trapezoid')
un.learn('n46-area-composite').learn('n46-area-unknown-side')
un.checkpoint(['n46-perimeter-polygon', 'n46-area-rect', 'n46-area-triangle', 'n46-area-parallelogram', 'n46-area-rhombus-trapezoid', 'n46-area-composite'])

un = Unit(S, 'n46-u26', 'Układ współrzędnych', 'Zaznaczanie i odczytywanie punktów oraz odległości.', 'grid', area=A4)
un.learn('n46-coord-read').learn('n46-coord-distance').learn('n46-coord-rectangle')
un.checkpoint(['n46-coord-read', 'n46-coord-distance', 'n46-coord-rectangle'])

un = Unit(S, 'n46-u27', 'Bryły', 'Graniastosłupy, ostrosłupy, siatki, pole powierzchni i objętość.', 'cube', area=A4)
un.learn('n46-solid-recognize').learn('n46-solid-elements').learn('n46-net-solid').learn('n46-net-faces')
un.learn('n46-cuboid-surface').learn('n46-cuboid-volume').learn('n46-cuboid-compound')
un.checkpoint(['n46-solid-recognize', 'n46-solid-elements', 'n46-net-solid', 'n46-net-faces', 'n46-cuboid-surface', 'n46-cuboid-volume', 'n46-cuboid-compound'])
