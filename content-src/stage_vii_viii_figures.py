"""Stage VII-VIII, area 3 (Figury).  Objectives: VII-VIII.3.1 - 3.14."""
from dsl import *

S = 'VII-VIII'
A3 = 'VII-VIII.3'
UN = "choice(['mm', 'cm', 'dm', 'm'])"
TRIPLES = '[[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25], [20, 21, 29]]'

# ============================================================================ symetralna, dwusieczna, symetrie (3.1, 3.2)
skill('vh-bisector', S, 'Symetralna odcinka i dwusieczna kąta', ['VII-VIII.3.1'],
      [lvl('Symetralna odcinka', mode=0), lvl('Dwusieczna kąta', mode=1), lvl('Dwusieczna i ramię kąta', mode=2)],
      [('d', 'randint(3, 40)'), ('al', '2 * randint(10, 85)'), ('b', 'randint(5, 85)'), ('un', UN),
       ('txt', "('Punkt P leży na symetralnej odcinka AB. Odległość PA wynosi ' + str(d) + ' ' + un + '. Ile wynosi odległość PB?') if mode == 0 else "
               "(('Dwusieczna kąta o mierze ' + str(al) + '° dzieli go na dwa kąty. Ile stopni ma każdy z nich?') if mode == 1 else "
               "('Dwusieczna kąta tworzy z jednym z jego ramion kąt o mierze ' + str(b) + '°. Ile stopni ma cały kąt?'))"),
       ('ans', 'd if mode == 0 else (al // 2 if mode == 1 else 2 * b)'),
       ('u', "un if mode == 0 else '°'"), ('sp', "' ' if mode == 0 else ''")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('Każdy punkt symetralnej jest tak samo oddalony od końców odcinka.' if mode == 0 else 'Dwusieczna dzieli kąt na dwa kąty o równych miarach.')}"),
                ('conclude', 'Odpowiedź: @{ans}@{sp}@{u}.')], unit_expr=True),
      min_distinct=15, area=A3, prereq=['n46-angle-types'])

SHAPES = ("[['kwadrat', 4, 1], ['prostokąt, który nie jest kwadratem', 2, 1], ['trójkąt równoboczny', 3, 0], ['trójkąt równoramienny, który nie jest równoboczny', 1, 0], "
          "['romb, który nie jest kwadratem', 2, 1], ['równoległobok, który nie jest rombem ani prostokątem', 0, 1], ['trapez równoramienny, który nie jest równoległobokiem', 1, 0], "
          "['pięciokąt foremny', 5, 0], ['sześciokąt foremny', 6, 1], ['trójkąt różnoboczny', 0, 0], ['deltoid, który nie jest rombem', 1, 0]]")

skill('vh-symmetry-axes', S, 'Liczba osi symetrii', ['VII-VIII.3.2'],
      [lvl('Figury płaskie')],
      [('sh', SHAPES), ('i', 'randint(0, len(sh) - 1)'), ('nm', 'sh[i][0]'), ('axes', 'sh[i][1]')],
      number('Ile osi symetrii ma ten wielokąt: @{nm}?', 'axes',
             [('idea', 'Oś symetrii dzieli figurę na dwie części, które pokrywają się po złożeniu wzdłuż tej osi.'), ('conclude', 'Liczba osi symetrii: @{axes}.')]),
      min_distinct=10, area=A3, prereq=['n46-symmetry-axes'])

skill('vh-symmetry-centre', S, 'Środek symetrii', ['VII-VIII.3.2'],
      [lvl('Figury płaskie')],
      [('sh', SHAPES), ('i', 'randint(0, len(sh) - 1)'), ('nm', 'sh[i][0]'), ('centre', 'sh[i][2]')],
      choice_text('Czy ten wielokąt ma środek symetrii: @{nm}?', [('Tak', 'centre == 1'), ('Nie', 'centre == 0')], None,
                  [('idea', 'Figura ma środek symetrii, jeśli po obrocie o 180° wokół pewnego punktu wygląda tak samo jak przed obrotem.'),
                   ('conclude', "@{('Tak, ma środek symetrii.' if centre == 1 else 'Nie, nie ma środka symetrii.')}")], fixed_order=True),
      min_distinct=10, area=A3, prereq=['vh-symmetry-axes'])

# ============================================================================ kąty wielokątów foremnych (3.3)
skill('vh-regular-angle', S, 'Kąty wielokąta foremnego', ['VII-VIII.3.3'],
      [lvl('Kąt wewnętrzny', mode=0), lvl('Kąt zewnętrzny', mode=1), lvl('Ile boków ma wielokąt?', mode=2)],
      [('ns', '[3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36]'), ('n', 'choice(ns)'), ('inner', '180 - 360 // n'), ('outer', '360 // n'),
       ('txt', "('Oblicz miarę kąta wewnętrznego wielokąta foremnego o ' + str(n) + ' bokach.') if mode == 0 else "
               "(('Oblicz miarę kąta zewnętrznego wielokąta foremnego o ' + str(n) + ' bokach.') if mode == 1 else "
               "('Kąt wewnętrzny wielokąta foremnego ma ' + str(inner) + '°. Ile boków ma ten wielokąt?'))"),
       ('ans', 'inner if mode == 0 else (outer if mode == 1 else n)'), ('u', "'°' if mode < 2 else 'boków'")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('Suma kątów zewnętrznych każdego wielokąta wypukłego to 360°. W wielokącie foremnym wszystkie kąty są równe: kąt zewnętrzny = 360° : n, a wewnętrzny = 180° − kąt zewnętrzny.')}"),
                ('compute', '360 : @{n} = @{outer}; 180 − @{outer} = @{inner}')], unit_expr=True),
      selfCheck=['inner * n == 180 * (n - 2)'], min_distinct=10, area=A3, prereq=['n46-quad-angle'])

# ============================================================================ twierdzenie Pitagorasa (3.4) i trójkąty szczególne (3.5)
skill('vh-pyth-basic', S, 'Twierdzenie Pitagorasa: przeciwprostokątna i przyprostokątna', ['VII-VIII.3.4'],
      [lvl('Przeciwprostokątna', mode=0), lvl('Przyprostokątna', mode=1)],
      [('t', 'choice(' + TRIPLES + ')'), ('k', 'randint(1, 4)'), ('un', UN), ('sw', 'randint(0, 1)'),
       ('a', 't[0] * k'), ('b', 't[1] * k'), ('c', 't[2] * k'),
       ('given1', 'a if mode == 1 else a'), ('given2', 'c if mode == 1 else b'), ('ans', 'c if mode == 0 else b')],
      quantity("@{('Przyprostokątne trójkąta prostokątnego mają długości ' + str(a) + ' ' + un + ' i ' + str(b) + ' ' + un + '. Oblicz długość przeciwprostokątnej.') if mode == 0 else "
               "('W trójkącie prostokątnym przeciwprostokątna ma ' + str(c) + ' ' + un + ', a jedna z przyprostokątnych ' + str(a) + ' ' + un + '. Oblicz długość drugiej przyprostokątnej.')}",
               'ans', 'un',
               [('idea', "@{('Twierdzenie Pitagorasa: a² + b² = c², gdzie c to przeciwprostokątna.' if mode == 0 else 'Z a² + b² = c² wynika b² = c² − a². Odejmij kwadraty i wyciągnij pierwiastek.')}"),
                ('compute', "@{(str(a) + '² + ' + str(b) + '² = ' + str(a * a + b * b) + ' = ' + str(c) + '²') if mode == 0 else (str(c) + '² − ' + str(a) + '² = ' + str(c * c - a * a) + ' = ' + str(b) + '²')}")],
               unit_expr=True,
               errors=[('sum', Qty('a + b', 'un', True), 'To suma długości przyprostokątnych. Zastosuj twierdzenie Pitagorasa: dodaj kwadraty i wyciągnij pierwiastek.', 'mode == 0'),
                       ('added_squares', Qty('isqrt(c * c + a * a) if is_square(c * c + a * a) else c + a', 'un', True), 'Przeciwprostokątna jest najdłuższym bokiem – kwadraty odejmujemy, nie dodajemy.', 'mode == 1 and is_square(c * c + a * a)')]),
      selfCheck=['a * a + b * b == c * c'], min_distinct=20, area=A3, prereq=['n46-triangle-by-angles', 'vh-sqrt-exact'],
      intro='W trójkącie prostokątnym kwadrat długości przeciwprostokątnej jest równy sumie kwadratów długości przyprostokątnych: a² + b² = c².')

skill('vh-pyth-context', S, 'Pitagoras w różnych figurach', ['VII-VIII.3.4', 'VII-VIII.3.9'],
      [lvl('Przekątna i drabina', c0=0), lvl('Wysokość trójkąta równoramiennego i bok rombu', c0=2)],
      [('t', 'choice(' + TRIPLES + ')'), ('k', 'randint(1, 3)'), ('sc', 'randint(c0, c0 + 1)'),
       ('a', 't[0] * k'), ('b', 't[1] * k'), ('c', 't[2] * k'),
       ('txt', "['Prostokąt ma boki ' + str(a) + ' cm i ' + str(b) + ' cm. Jaką długość ma jego przekątna?', "
               "'Drabina o długości ' + str(c) + ' dm opiera się o pionową ścianę. Jej dolny koniec jest oddalony od ściany o ' + str(a) + ' dm. Na jakiej wysokości (w dm) drabina dotyka ściany?', "
               "'Trójkąt równoramienny ma ramiona długości ' + str(c) + ' cm i podstawę ' + str(2 * a) + ' cm. Jaką długość ma wysokość opuszczona na podstawę?', "
               "'Romb ma przekątne długości ' + str(2 * a) + ' cm i ' + str(2 * b) + ' cm. Jaką długość ma bok rombu?']"),
       ('ans', '[c, b, b, c][sc]'),
       ('ideas', "['Przekątna dzieli prostokąt na dwa trójkąty prostokątne, w których jest przeciwprostokątną.', "
                 "'Ściana, ziemia i drabina tworzą trójkąt prostokątny; drabina jest jego przeciwprostokątną.', "
                 "'Wysokość dzieli podstawę na połowy i tworzy trójkąt prostokątny: ramię jest przeciwprostokątną, a przyprostokątne to wysokość i połowa podstawy.', "
                 "'Przekątne rombu dzielą się na połowy pod kątem prostym. Bok rombu to przeciwprostokątna trójkąta o przyprostokątnych równych połowom przekątnych.']")],
      number('@{txt[sc]}', 'ans', [('idea', '@{ideas[sc]}'), ('conclude', 'Odpowiedź: @{ans}.')]),
      selfCheck=['a * a + b * b == c * c'], min_distinct=20, area=A3, prereq=['vh-pyth-basic'])

skill('vh-special-numeric', S, 'Trójkąty 30°–60°–90° i 45°–45°–90°', ['VII-VIII.3.5'],
      [lvl('Krótsza przyprostokątna i przeciwprostokątna', mode=0), lvl('Przeciwprostokątna i krótsza przyprostokątna', mode=1), lvl('Pole trójkąta 45°–45°–90°', mode=2)],
      [('a', 'randint(2, 30)'), ('h', '2 * randint(2, 15)'),
       ('txt', "('W trójkącie prostokątnym o kątach ostrych 30° i 60° krótsza przyprostokątna ma ' + str(a) + ' cm. Ile centymetrów ma przeciwprostokątna?') if mode == 0 else "
               "(('W trójkącie prostokątnym o kątach ostrych 30° i 60° przeciwprostokątna ma ' + str(2 * a) + ' cm. Ile centymetrów ma krótsza przyprostokątna?') if mode == 1 else "
               "('W trójkącie prostokątnym równoramiennym przeciwprostokątna ma ' + str(h) + ' cm. Ile centymetrów kwadratowych wynosi pole tego trójkąta?'))"),
       ('ans', '2 * a if mode == 0 else (a if mode == 1 else h * h // 4)'), ('u', "'cm' if mode < 2 else 'cm²'")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('W trójkącie 30°–60°–90° przyprostokątna leżąca naprzeciw kąta 30° jest dwa razy krótsza od przeciwprostokątnej.' if mode < 2 else 'Dwa takie trójkąty złożone przeciwprostokątnymi tworzą kwadrat o przekątnej równej tej przeciwprostokątnej. Pole kwadratu o przekątnej d to d² : 2, a trójkąt jest jego połową.')}"),
                ('conclude', 'Odpowiedź: @{ans} @{u}.')], unit_expr=True),
      min_distinct=12, area=A3, prereq=['vh-pyth-basic'])

skill('vh-special-exact', S, 'Dokładne długości w trójkątach szczególnych', ['VII-VIII.3.5'],
      [lvl('Trójkąt równoramienny prostokątny', mode=0), lvl('Dłuższa przyprostokątna', mode=1), lvl('Wysokość trójkąta równobocznego', mode=2)],
      [('a', 'randint(2, 12)'),
       ('txt', "('Przyprostokątne trójkąta prostokątnego równoramiennego mają po ' + str(a) + ' cm. Jaką długość ma jego przeciwprostokątna?') if mode == 0 else "
               "(('W trójkącie prostokątnym o kątach ostrych 30° i 60° krótsza przyprostokątna ma ' + str(a) + ' cm. Jaką długość ma dłuższa przyprostokątna?') if mode == 1 else "
               "('Trójkąt równoboczny ma bok ' + str(2 * a) + ' cm. Jaką długość ma jego wysokość?'))"),
       ('good', "str(a) + '√2 cm' if mode == 0 else str(a) + '√3 cm'"),
       ('w1', "str(2 * a) + ' cm' if mode == 0 else str(a) + '√2 cm'"), ('w2', "str(a) + '√3 cm' if mode == 0 else str(2 * a) + ' cm'"),
       ('w3', "str(a * a) + ' cm' if mode == 0 else str(2 * a) + '√3 cm'")],
      choice('@{txt}', 'good', ['w1', 'w2', 'w3'],
             [('idea', "@{('Z twierdzenia Pitagorasa: c² = a² + a² = 2a², więc c = a√2.' if mode == 0 else 'Jeśli krótsza przyprostokątna ma a, to przeciwprostokątna ma 2a, a dłuższa przyprostokątna: (2a)² − a² = 3a², czyli a√3. Wysokość trójkąta równobocznego o boku 2a ma tę samą długość.')}"),
              ('conclude', 'Poprawna odpowiedź: @{good}.')]),
      constraints=['len(uniq([good, w1, w2, w3])) == 4'], min_distinct=8, area=A3, prereq=['vh-special-numeric', 'vh-root-multiply'])

# ============================================================================ przystawanie trójkątów (3.6)
skill('vh-congruent-find', S, 'Trójkąty przystające: odpowiadające boki i kąty', ['VII-VIII.3.6'],
      [lvl('Trzeci kąt', mode=0), lvl('Odpowiadający bok', mode=1)],
      [('al', 'randint(30, 80)'), ('be', 'randint(30, 80)'), ('ga', '180 - al - be'),
       ('a', 'randint(3, 12)'), ('b', 'randint(3, 12)'), ('c', 'randint(3, 12)'), ('r', 'randint(1, 2)'), ('s', 'randint(0, 2)'),
       ('pm', "drop(['P', 'Q', 'R'], r) + take(['P', 'Q', 'R'], r)"), ('side', "pm[s] + pm[(s + 1) % 3]"),
       ('lens', '[c, a, b]'), ('vert', "['A', 'B', 'C']"),
       ('mapping', "'A i ' + pm[0] + ', B i ' + pm[1] + ', C i ' + pm[2]"),
       ('txt', "('Trójkąty ABC i PQR są przystające, przy czym kątowi A odpowiada kąt ' + pm[0] + ', kątowi B odpowiada kąt ' + pm[1] + ', a kątowi C odpowiada kąt ' + pm[2] + '. W trójkącie ABC kąt A ma ' + str(al) + '°, a kąt B ma ' + str(be) + '°. Ile stopni ma kąt ' + pm[2] + '?') if mode == 0 else "
               "('Trójkąty ABC i PQR są przystające, przy czym kątowi A odpowiada kąt ' + pm[0] + ', kątowi B odpowiada kąt ' + pm[1] + ', a kątowi C odpowiada kąt ' + pm[2] + '. W trójkącie ABC: AB = ' + str(c) + ' cm, BC = ' + str(a) + ' cm, CA = ' + str(b) + ' cm. Ile centymetrów ma odcinek ' + side + '?')"),
       ('ans', 'ga if mode == 0 else lens[s]'), ('u', "'°' if mode == 0 else 'cm'"), ('sp', "'' if mode == 0 else ' '")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('Odpowiadające sobie kąty w trójkątach przystających mają równe miary, a suma kątów trójkąta to 180°.' if mode == 0 else 'W trójkątach przystających odpowiadające sobie boki mają równe długości. Ustal, którym wierzchołkom ABC odpowiadają końce odcinka.')}"),
                ('conclude', 'Odpowiedź: @{ans}@{sp}@{u}.')], unit_expr=True),
      constraints=['a + b > c and a + c > b and b + c > a', 'mode == 1 or ga > 0', 'mode == 0 or len(uniq([a, b, c])) == 3'], min_distinct=20, area=A3, prereq=['n46-triangle-angle'])

CONG = [
    bank_choice('Dwa trójkąty mają odpowiednio równe wszystkie trzy boki. Czy na pewno są przystające?',
                [('Tak – to cecha przystawania „bok, bok, bok”.', True), ('Nie – potrzebne są jeszcze kąty.', False), ('Tylko jeśli oba są prostokątne.', False), ('Tylko jeśli oba są równoramienne.', False)],
                [('idea', 'Trzy boki jednoznacznie wyznaczają trójkąt. Cecha BBB wystarcza.')]),
    bank_choice('Dwa trójkąty mają odpowiednio równe dwa boki i kąt zawarty między nimi. Co możemy powiedzieć?',
                [('Są przystające (cecha „bok, kąt, bok”).', True), ('Nie wiemy, czy są przystające.', False), ('Są podobne, ale nie muszą być przystające.', False), ('Są przystające tylko wtedy, gdy kąt jest prosty.', False)],
                [('idea', 'Kąt musi leżeć między tymi dwoma bokami – wtedy trójkąt jest wyznaczony jednoznacznie.')]),
    bank_choice('Dwa trójkąty mają dwa odpowiednio równe boki i równy kąt, ale ten kąt NIE leży między tymi bokami. Czy na pewno są przystające?',
                [('Nie – taka informacja nie wystarcza.', True), ('Tak – zawsze.', False), ('Tak, jeśli kąt jest rozwarty.', False), ('Tak, jeśli boki są różne.', False)],
                [('idea', 'Dwa boki i kąt nieleżący między nimi mogą wyznaczać dwa różne trójkąty. Takiej cechy nie ma.')]),
    bank_choice('Dwa trójkąty mają odpowiednio równe bok i dwa kąty do niego przyległe. Co możemy powiedzieć?',
                [('Są przystające (cecha „kąt, bok, kąt”).', True), ('Nie wiemy.', False), ('Nie są przystające.', False), ('Są przystające tylko jeśli są równoboczne.', False)],
                [('idea', 'Bok i dwa kąty przy nim jednoznacznie wyznaczają trójkąt.')]),
    bank_choice('Dwa trójkąty mają odpowiednio równe wszystkie trzy kąty. Czy na pewno są przystające?',
                [('Nie – mogą mieć różne rozmiary (być tylko podobne).', True), ('Tak – kąty wyznaczają trójkąt.', False), ('Tak, jeśli mają ten sam obwód.', False), ('Tak, jeśli są prostokątne.', False)],
                [('idea', 'Równe kąty nie wystarczą: trójkąt można powiększyć lub pomniejszyć, nie zmieniając kątów. Cechy „kąt, kąt, kąt” dla przystawania nie ma.')]),
    bank_choice('Trójkąty ABC i DEF mają: AB = DE = 6 cm, BC = EF = 8 cm i kąt ABC = kąt DEF = 50°. Które stwierdzenie jest poprawne?',
                [('Trójkąty są przystające, bo kąt leży między równymi bokami.', True), ('Trójkąty nie są przystające, bo brak trzeciego boku.', False), ('Nie da się nic stwierdzić.', False), ('Trójkąty są przystające, bo mają równe kąty.', False)],
                [('idea', 'Kąt ABC leży między bokami AB i BC, kąt DEF między DE i EF – cecha BKB jest spełniona.')]),
    bank_choice('W trójkątach ABC i DEF: kąt A = kąt D = 40°, kąt B = kąt E = 60°, AB = DE = 7 cm. Czy są przystające?',
                [('Tak – bok AB i przyległe do niego kąty są równe odpowiednim.', True), ('Nie – brak trzeciego boku.', False), ('Tak – ale tylko dlatego, że kąt C jest równy.', False), ('Nie – kąty muszą być prostokątne.', False)],
                [('idea', 'Kąty A i B przylegają do boku AB, więc stosujemy cechę KBK. Trzeci kąt wynika z sumy 180°.')]),
    bank_choice('Który zestaw danych wystarczy, aby uzasadnić przystawanie dwóch trójkątów?',
                [('Trzy pary równych boków.', True), ('Trzy pary równych kątów.', False), ('Dwie pary równych kątów.', False), ('Jedna para równych boków i jedna para równych kątów.', False)],
                [('idea', 'Cechy przystawania trójkątów: BBB, BKB, KBK.')]),
]
bank_skill('vh-congruent-criteria', S, 'Cechy przystawania trójkątów', ['VII-VIII.3.6'], CONG, levels=['Cechy przystawania'], tags=('thinking',), area=A3, prereq=['vh-congruent-find'],
           intro='Dwa trójkąty są przystające, gdy jeden da się nałożyć na drugi. Wystarczy sprawdzić jedną z cech: BBB (trzy boki), BKB (dwa boki i kąt między nimi), KBK (bok i dwa przyległe kąty).')

# ============================================================================ okrąg i koło (3.7)
skill('vh-circle-calc', S, 'Długość okręgu i pole koła (π ≈ 3,14)', ['VII-VIII.3.7'],
      [lvl('Długość okręgu', mode=0), lvl('Pole koła', mode=1), lvl('Promień z długości okręgu', mode=2), lvl('Pole koła o danej średnicy', mode=3)],
      [('r', 'randint(2, 30)'), ('un', UN),
       ('c', '314 / 100 * 2 * r'), ('p', '314 / 100 * r * r'),
       ('txt', "('Oblicz długość okręgu o promieniu ' + str(r) + ' ' + un + '. Przyjmij π ≈ 3,14.') if mode == 0 else "
               "(('Oblicz pole koła o promieniu ' + str(r) + ' ' + un + '. Przyjmij π ≈ 3,14.') if mode == 1 else "
               "(('Okrąg ma długość ' + fmt(c) + ' ' + un + '. Oblicz jego promień. Przyjmij π ≈ 3,14.') if mode == 2 else "
               "('Średnica koła wynosi ' + str(2 * r) + ' ' + un + '. Oblicz pole koła. Przyjmij π ≈ 3,14.')))"),
       ('ans', 'c if mode == 0 else (p if mode == 1 else (r if mode == 2 else p))'),
       ('u', "un + '²' if mode == 1 or mode == 3 else un")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('Długość okręgu: L = 2πr.' if mode == 0 else ('Pole koła: P = πr².' if mode == 1 else ('Z L = 2πr wynika r = L : (2π).' if mode == 2 else 'Promień to połowa średnicy. Pole koła: P = πr².')))}"),
                ('conclude', 'Odpowiedź: @{ans|dec} @{u}.')], unit_expr=True,
               errors=[('area_for_length', Qty('p', 'un', True), 'To jest pole koła. Długość okręgu to 2πr.', 'mode == 0'),
                       ('diameter_as_r', Qty('314 / 100 * 4 * r * r', "un + '²'", True), 'Pamiętaj: we wzorze na pole koła występuje promień, a średnica jest dwa razy dłuższa.', 'mode == 3')]),
      min_distinct=20, area=A3, prereq=['n46-circle-diameter', 'n46-dec-mul'],
      intro='Długość okręgu o promieniu r to L = 2πr, a pole koła P = πr². Liczba π jest w przybliżeniu równa 3,14.')

skill('vh-circle-pi', S, 'Wyniki w postaci wielokrotności π', ['VII-VIII.3.7'],
      [lvl('Długość okręgu', mode=0), lvl('Pole koła', mode=1), lvl('Pole z długości okręgu', mode=2)],
      [('r', 'randint(2, 20)'), ('un', UN),
       ('txt', "('Okrąg ma promień ' + str(r) + ' ' + un + '. Jego długość to k·π ' + un + '. Ile wynosi k?') if mode == 0 else "
               "(('Koło ma promień ' + str(r) + ' ' + un + '. Jego pole to k·π ' + un + '². Ile wynosi k?') if mode == 1 else "
               "('Okrąg ma długość ' + str(2 * r) + 'π ' + un + '. Pole koła o tym obwodzie to k·π ' + un + '². Ile wynosi k?')) "),
       ('ans', '2 * r if mode == 0 else r * r')],
      number('@{txt}', 'ans',
             [('idea', "@{('L = 2πr, więc k = 2r.' if mode == 0 else ('P = πr², więc k = r².' if mode == 1 else 'Z 2πr = długość wynika r. Potem P = πr², więc k = r².'))}"),
              ('conclude', 'k = @{ans}.')]),
      min_distinct=15, area=A3, prereq=['vh-circle-calc'])

# ============================================================================ rozkładanie figur na części (3.8) i modele rzeczywistych obiektów (3.9)
skill('vh-area-decompose', S, 'Pole figury złożonej z części', ['VII-VIII.3.8'],
      [lvl('Prostokąt z wyciętym narożnikiem', mode=0), lvl('Trapez prostokątny', mode=1), lvl('Kwadrat wpisany w kwadrat', mode=2)],
      [('a', 'randint(8, 20)'), ('b', 'randint(8, 20)'), ('cc', 'randint(2, 6)'), ('dd', 'randint(2, 6)'), ('h', 'randint(3, 12)'), ('un', UN),
       ('p', '2 * randint(3, 15) * randint(1, 3)'),
       ('txt', "('Z prostokąta o bokach ' + str(a) + ' ' + un + ' i ' + str(b) + ' ' + un + ' wycięto w rogu prostokąt o bokach ' + str(cc) + ' ' + un + ' i ' + str(dd) + ' ' + un + '. Oblicz pole powstałej figury.') if mode == 0 else "
               "(('Trapez prostokątny ma podstawy ' + str(a + cc) + ' ' + un + ' i ' + str(a) + ' ' + un + ' oraz wysokość ' + str(2 * h) + ' ' + un + '. Pole możesz obliczyć, dzieląc trapez na prostokąt i trójkąt. Ile wynosi pole?') if mode == 1 else "
               "('Środki boków kwadratu o polu ' + str(p) + ' ' + un + '² połączono kolejno odcinkami. Powstał mniejszy kwadrat. Oblicz jego pole.'))"),
       ('ans', 'a * b - cc * dd if mode == 0 else ((a + cc + a) * h if mode == 1 else p // 2)')],
      quantity('@{txt}', 'ans', "un + '²'",
               [('idea', "@{('Pole figury = pole dużego prostokąta − pole wyciętego.' if mode == 0 else ('Trapez = prostokąt o bokach a i wysokości + trójkąt o podstawie równej różnicy podstaw.' if mode == 1 else 'Cztery odcięte trójkąty mają razem pole równe połowie pola dużego kwadratu.'))}"),
                ('conclude', 'Odpowiedź: @{ans} @{un}².')], unit_expr=True),
      constraints=['mode != 0 or (cc < a and dd < b)', 'mode != 2 or p % 2 == 0'], min_distinct=30, area=A3, prereq=['n46-area-composite'])

skill('vh-real-model', S, 'Zadania z życia: płytki, farba, ogrodzenie', ['VII-VIII.3.9'],
      [lvl('Płytki na podłodze', mode=0), lvl('Farba na ścianę', mode=1), lvl('Siatka wokół okrągłego placu', mode=2)],
      [('s', 'choice([20, 25, 30, 40, 50])'), ('na', 'randint(4, 14)'), ('nb', 'randint(4, 14)'),
       ('wa', 'randint(3, 8)'), ('wb', 'randint(5, 12)'), ('wd', 'randint(2, 5)'), ('cov', 'randint(4, 9)'),
       ('r', 'randint(3, 20)'),
       ('txt', "('Podłoga ma wymiary ' + str(s * na) + ' cm na ' + str(s * nb) + ' cm. Układamy kwadratowe płytki o boku ' + str(s) + ' cm, bez przycinania i bez fug. Ile płytek potrzeba?') if mode == 0 else "
               "(('Chcemy pomalować ścianę o wymiarach ' + str(wa) + ' m na ' + str(wb) + ' m. Drzwi i okno zajmują razem ' + str(wd) + ' m², których nie malujemy. Jeden litr farby wystarcza na ' + str(cov) + ' m². Ile litrów (w pełnych litrach) trzeba kupić?') if mode == 1 else "
               "('Okrągły plac ma promień ' + str(r) + ' m. Chcemy ogrodzić go siatką sprzedawaną w rolkach po 10 m. Ile rolek trzeba kupić? Przyjmij π ≈ 3,14.')) "),
       ('ans', 'na * nb if mode == 0 else (ceil((wa * wb - wd) / cov) if mode == 1 else ceil(314 / 100 * 2 * r / 10))')],
      number('@{txt}', 'ans',
             [('idea', "@{('Policz, ile płytek mieści się wzdłuż każdego boku, i pomnóż.' if mode == 0 else ('Od pola ściany odejmij pole drzwi i okna, podziel przez wydajność 1 litra i zaokrąglij w górę.' if mode == 1 else 'Długość ogrodzenia to długość okręgu 2πr. Podziel przez 10 m i zaokrąglij w górę – nie można kupić części rolki.'))}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['mode != 0 or na != nb', 'mode != 1 or wa * wb - wd > cov', 'mode != 1 or (wa * wb - wd) % cov != 0'], min_distinct=15, area=A3, prereq=['vh-circle-calc', 'n46-area-rect'])

# ============================================================================ punkty kratowe (3.10, 3.11)
skill('vh-lattice-vertex', S, 'Współrzędne wierzchołków i symetria względem osi', ['VII-VIII.3.10'],
      [lvl('Czwarty wierzchołek równoległoboku', mode=0), lvl('Odbicie względem osi OX', mode=1), lvl('Odbicie względem osi OY', mode=2), lvl('Symetria środkowa względem początku układu', mode=3)],
      [('x', 'randint(-6, 6)'), ('y', 'randint(-6, 6)'), ('p', 'randint(2, 6)'), ('q', 'randint(1, 4)'), ('h', 'randint(2, 5)'),
       ('ax', 'x + q if mode == 0 else (x if mode == 1 else -x)'), ('ay', 'y + h if mode == 0 else (-y if mode == 1 else (y if mode == 2 else -y))')],
      task('point-input',
           "@{('Trzy wierzchołki równoległoboku ABCD to A(' + str(x) + ', ' + str(y) + '), B(' + str(x + p) + ', ' + str(y) + ') i C(' + str(x + p + q) + ', ' + str(y + h) + '). Jakie współrzędne ma wierzchołek D?') if mode == 0 else "
           "(('Punkt A(' + str(x) + ', ' + str(y) + ') odbito symetrycznie względem osi OX. Jakie współrzędne ma obraz punktu A?') if mode == 1 else "
           "(('Punkt A(' + str(x) + ', ' + str(y) + ') odbito symetrycznie względem osi OY. Jakie współrzędne ma obraz punktu A?') if mode == 2 else "
           "('Punkt A(' + str(x) + ', ' + str(y) + ') odbito symetrycznie względem początku układu współrzędnych. Jakie współrzędne ma obraz punktu A?')))}",
           Pt('ax', 'ay'),
           [('idea', "@{('W równoległoboku wektor od A do D jest taki sam jak od B do C.' if mode == 0 else ('Przy odbiciu względem osi OX zmienia się znak współrzędnej y.' if mode == 1 else ('Przy odbiciu względem osi OY zmienia się znak współrzędnej x.' if mode == 2 else 'Przy symetrii względem początku układu zmieniają się znaki obu współrzędnych.')))}"),
            ('conclude', 'Szukany punkt ma współrzędne (@{ax}, @{ay}).')]),
      constraints=['mode == 0 or (x != 0 and y != 0)'], min_distinct=30, area=A3, prereq=['n46-coord-rectangle'])

skill('vh-lattice-area', S, 'Pola i obwody figur o wierzchołkach kratowych', ['VII-VIII.3.11'],
      [lvl('Prostokąt', mode=0), lvl('Trójkąt z poziomą podstawą', mode=1), lvl('Obwód trójkąta prostokątnego', mode=2)],
      [('x1', 'randint(-5, 2)'), ('y1', 'randint(-5, 2)'), ('w', 'randint(2, 8)'), ('h', 'randint(2, 8)'), ('dx', 'randint(0, 8)'),
       ('t', 'choice([[3, 4, 5], [5, 12, 13], [6, 8, 10]])'),
       ('txt', "('Wierzchołki prostokąta ABCD o bokach równoległych do osi układu to A(' + str(x1) + ', ' + str(y1) + '), B(' + str(x1 + w) + ', ' + str(y1) + ') i C(' + str(x1 + w) + ', ' + str(y1 + h) + '). Oblicz pole prostokąta (jednostka: kratka).') if mode == 0 else "
               "(('Trójkąt ABC ma wierzchołki A(' + str(x1) + ', ' + str(y1) + '), B(' + str(x1 + w) + ', ' + str(y1) + ') i C(' + str(x1 + dx) + ', ' + str(y1 + h) + '). Oblicz jego pole (jednostka: kratka).') if mode == 1 else "
               "('Trójkąt prostokątny ma wierzchołki A(' + str(x1) + ', ' + str(y1) + '), B(' + str(x1 + t[0]) + ', ' + str(y1) + ') i C(' + str(x1) + ', ' + str(y1 + t[1]) + '). Oblicz jego obwód (jednostka: długość boku kratki).'))"),
       ('ans', 'w * h if mode == 0 else (w * h // 2 if mode == 1 else t[0] + t[1] + t[2])')],
      number('@{txt}', 'ans',
             [('idea', "@{('Policz długości boków z różnic współrzędnych i pomnóż.' if mode == 0 else ('Podstawa AB jest pozioma, a wysokość to różnica drugich współrzędnych C i A. Pole = podstawa · wysokość : 2.' if mode == 1 else 'Przyprostokątne są równoległe do osi. Przeciwprostokątną oblicz z twierdzenia Pitagorasa.'))}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['mode != 1 or (w * h) % 2 == 0'], min_distinct=30, area=A3, prereq=['vh-lattice-vertex', 'n46-area-triangle'])

# ============================================================================ bryły (3.12 - 3.14)
skill('vh-solid-counts', S, 'Wierzchołki, krawędzie i ściany graniastosłupów i ostrosłupów', ['VII-VIII.3.12'],
      [lvl('Graniastosłup prosty', mode=0), lvl('Ostrosłup prawidłowy', mode=1), lvl('Jaki wielokąt w podstawie?', mode=2)],
      [('n', 'randint(4, 10)'), ('q', 'randint(0, 2)'), ('t', 'randint(0, 1)'),
       ('nm', "['wierzchołków', 'krawędzi', 'ścian']"), ('sn', "['graniastosłup prosty', 'ostrosłup prawidłowy']"),
       ('cnt', '[[2 * n, 3 * n, n + 2], [n + 1, 2 * n, n + 1]][t if mode == 2 else mode][q]'),
       ('kind', 'mode if mode < 2 else t'),
       ('txt', "('Graniastosłup prosty ma w podstawie ' + str(n) + '-kąt. Ile ma ' + nm[q] + '?') if mode == 0 else "
               "(('Ostrosłup prawidłowy ma w podstawie ' + str(n) + '-kąt. Ile ma ' + nm[q] + '?') if mode == 1 else "
               "(cap(sn[t]) + ' ma ' + str(cnt) + ' ' + nm[q] + '. Ile boków ma wielokąt w podstawie?'))"),
       ('ans', 'cnt if mode < 2 else n')],
      number('@{txt}', 'ans',
             [('idea', "@{('Graniastosłup o podstawie n-kątnej ma 2n wierzchołków, 3n krawędzi i n + 2 ściany.' if kind == 0 else 'Ostrosłup o podstawie n-kątnej ma n + 1 wierzchołków, 2n krawędzi i n + 1 ścian.')}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      selfCheck=['kind != 0 or (2 * n) - (3 * n) + (n + 2) == 2', 'kind != 1 or (n + 1) - (2 * n) + (n + 1) == 2'], min_distinct=15, area=A3, prereq=['n46-solid-elements'])

skill('vh-pyramid-heights', S, 'Wysokość ostrosłupa i wysokość ściany bocznej', ['VII-VIII.3.13'],
      [lvl('Wysokość ściany bocznej', mode=0), lvl('Wysokość ostrosłupa', mode=1), lvl('Krawędź podstawy', mode=2)],
      [('tr', 'choice(' + TRIPLES + ')'), ('k', 'randint(1, 3)'), ('sw', 'randint(0, 1)'), ('un', "choice(['cm', 'dm', 'm'])"),
       ('m', 'tr[sw] * k'), ('hh', 'tr[1 - sw] * k'), ('hs', 'tr[2] * k'),
       ('txt', "('Ostrosłup prawidłowy czworokątny ma krawędź podstawy ' + str(2 * m) + ' ' + un + ' i wysokość ' + str(hh) + ' ' + un + '. Oblicz wysokość ściany bocznej.') if mode == 0 else "
               "(('Ostrosłup prawidłowy czworokątny ma krawędź podstawy ' + str(2 * m) + ' ' + un + ' i wysokość ściany bocznej ' + str(hs) + ' ' + un + '. Oblicz wysokość ostrosłupa.') if mode == 1 else "
               "('Ostrosłup prawidłowy czworokątny ma wysokość ' + str(hh) + ' ' + un + ' i wysokość ściany bocznej ' + str(hs) + ' ' + un + '. Oblicz krawędź podstawy.'))"),
       ('ans', 'hs if mode == 0 else (hh if mode == 1 else 2 * m)')],
      quantity('@{txt}', 'ans', 'un',
               [('idea', 'Wysokość ostrosłupa, odcinek łączący spodek wysokości ze środkiem krawędzi podstawy (połowa krawędzi podstawy) i wysokość ściany bocznej tworzą trójkąt prostokątny. Wysokość ściany bocznej jest jego przeciwprostokątną.'),
                ('compute', '@{hh}² + @{m}² = @{hs}²')], unit_expr=True),
      selfCheck=['hh * hh + m * m == hs * hs'], min_distinct=20, area=A3, prereq=['vh-pyth-basic', 'vh-solid-counts'])

skill('vh-prism', S, 'Graniastosłupy proste: objętość i pole powierzchni', ['VII-VIII.3.14'],
      [lvl('Objętość', mode=0), lvl('Pole powierzchni', mode=1), lvl('Wysokość z objętości', mode=2)],
      [('t', 'choice([[3, 4, 5], [5, 12, 13], [6, 8, 10], [8, 15, 17]])'), ('hh', 'randint(2, 12)'), ('un', "choice(['cm', 'dm', 'm'])"),
       ('pb', 't[0] * t[1] // 2'), ('v', 'pb * hh'), ('pc', '2 * pb + (t[0] + t[1] + t[2]) * hh'),
       ('base', "'Podstawą graniastosłupa prostego jest trójkąt prostokątny o przyprostokątnych ' + str(t[0]) + ' ' + un + ' i ' + str(t[1]) + ' ' + un"),
       ('txt', "base + ' (przeciwprostokątna ma ' + str(t[2]) + ' ' + un + '). Wysokość graniastosłupa wynosi ' + str(hh) + ' ' + un + '. Oblicz jego objętość.' if mode == 0 else "
               "(base + ' (przeciwprostokątna ma ' + str(t[2]) + ' ' + un + '). Wysokość graniastosłupa wynosi ' + str(hh) + ' ' + un + '. Oblicz jego pole powierzchni całkowitej.' if mode == 1 else "
               "(base + '. Objętość graniastosłupa wynosi ' + str(v) + ' ' + un + '³. Oblicz jego wysokość.'))"),
       ('ans', 'v if mode == 0 else (pc if mode == 1 else hh)'), ('u', "un + '³' if mode == 0 else (un + '²' if mode == 1 else un)")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('Objętość = pole podstawy · wysokość.' if mode == 0 else ('Pole powierzchni = 2 · pole podstawy + pole powierzchni bocznej (obwód podstawy · wysokość).' if mode == 1 else 'Wysokość = objętość : pole podstawy.'))}"),
                ('compute', 'Pole podstawy: @{pb} @{un}².')], unit_expr=True),
      selfCheck=['t[0] * t[0] + t[1] * t[1] == t[2] * t[2]'], min_distinct=30, area=A3, prereq=['n46-cuboid-volume', 'vh-pyth-basic'])

skill('vh-pyramid', S, 'Ostrosłupy prawidłowe czworokątne: objętość i pole powierzchni', ['VII-VIII.3.14'],
      [lvl('Objętość z wysokości', mode=0), lvl('Pole powierzchni z wysokości ściany', mode=1), lvl('Pole powierzchni z wysokości ostrosłupa', mode=2), lvl('Objętość z wysokości ściany', mode=3)],
      [('tr', 'choice(' + TRIPLES + ')'), ('k', 'randint(1, 3)'), ('sw', 'randint(0, 1)'), ('un', "choice(['cm', 'dm', 'm'])"),
       ('m', 'tr[sw] * k'), ('hh', 'tr[1 - sw] * k'), ('hs', 'tr[2] * k'), ('a', '2 * m'),
       ('v', 'a * a * hh // 3'), ('pc', 'a * a + 2 * a * hs'),
       ('txt', "('Ostrosłup prawidłowy czworokątny ma krawędź podstawy ' + str(a) + ' ' + un + ' i wysokość ' + str(hh) + ' ' + un + '. Oblicz jego objętość.') if mode == 0 else "
               "(('Ostrosłup prawidłowy czworokątny ma krawędź podstawy ' + str(a) + ' ' + un + ' i wysokość ściany bocznej ' + str(hs) + ' ' + un + '. Oblicz jego pole powierzchni całkowitej.') if mode == 1 else "
               "(('Ostrosłup prawidłowy czworokątny ma krawędź podstawy ' + str(a) + ' ' + un + ' i wysokość ' + str(hh) + ' ' + un + '. Oblicz jego pole powierzchni całkowitej.') if mode == 2 else "
               "('Ostrosłup prawidłowy czworokątny ma krawędź podstawy ' + str(a) + ' ' + un + ' i wysokość ściany bocznej ' + str(hs) + ' ' + un + '. Oblicz jego objętość.')))"),
       ('ans', 'v if mode == 0 or mode == 3 else pc'), ('u', "un + '³' if mode == 0 or mode == 3 else un + '²'")],
      quantity('@{txt}', 'ans', 'u',
               [('idea', "@{('Objętość ostrosłupa = jedna trzecia pola podstawy razy wysokość.' if mode == 0 else ('Pole powierzchni = pole podstawy + cztery ściany boczne (każda: krawędź podstawy · wysokość ściany : 2).' if mode == 1 else ('Najpierw oblicz wysokość ściany bocznej z twierdzenia Pitagorasa, potem pole powierzchni.' if mode == 2 else 'Najpierw oblicz wysokość ostrosłupa z twierdzenia Pitagorasa, potem objętość.')))}"),
                ('compute', 'Pole podstawy: @{a * a} @{un}².')], unit_expr=True),
      constraints=['(a * a * hh) % 3 == 0 or mode == 1 or mode == 2'], selfCheck=['hh * hh + m * m == hs * hs'], min_distinct=20, area=A3, prereq=['vh-pyramid-heights', 'vh-prism'])

# ============================================================================ ścieżka
un = Unit(S, 'vh-u8', 'Symetria i kąty', 'Symetralna, dwusieczna, osie i środek symetrii oraz kąty wielokątów foremnych.', 'symmetry', area=A3)
un.learn('vh-bisector').learn('vh-symmetry-axes').learn('vh-symmetry-centre').learn('vh-regular-angle')
un.checkpoint(['vh-bisector', 'vh-symmetry-axes', 'vh-symmetry-centre', 'vh-regular-angle'])

un = Unit(S, 'vh-u9', 'Twierdzenie Pitagorasa i trójkąty', 'Trójkąty prostokątne, trójkąty szczególne i przystawanie trójkątów.', 'triangle', area=A3)
un.learn('vh-pyth-basic').learn('vh-pyth-context').learn('vh-special-numeric').learn('vh-special-exact').learn('vh-congruent-find').learn('vh-congruent-criteria', tasks=8)
un.checkpoint(['vh-pyth-basic', 'vh-pyth-context', 'vh-special-numeric', 'vh-congruent-find'])

un = Unit(S, 'vh-u10', 'Koło, pola i modele', 'Okrąg i koło, pola figur złożonych i zadania z życia.', 'circle', area=A3)
un.learn('vh-circle-calc').learn('vh-circle-pi').learn('vh-area-decompose').learn('vh-real-model')
un.checkpoint(['vh-circle-calc', 'vh-circle-pi', 'vh-area-decompose', 'vh-real-model'])

un = Unit(S, 'vh-u11', 'Układ współrzędnych', 'Wierzchołki, symetrie względem osi oraz pola i obwody figur kratowych.', 'coordinates', area=A3)
un.learn('vh-lattice-vertex').learn('vh-lattice-area')
un.checkpoint(['vh-lattice-vertex', 'vh-lattice-area'])

un = Unit(S, 'vh-u12', 'Bryły', 'Graniastosłupy i ostrosłupy: elementy, wysokości, objętość i pole powierzchni.', 'solid', area=A3)
un.learn('vh-solid-counts').learn('vh-pyramid-heights').learn('vh-prism').learn('vh-pyramid')
un.checkpoint(['vh-solid-counts', 'vh-pyramid-heights', 'vh-prism', 'vh-pyramid'])
