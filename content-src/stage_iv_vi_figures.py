"""Stage IV-VI, area 4 (Figury).  Objectives: IV-VI.4.1-4.22 (+ 2.3 angle reading lives in the measures module)."""
from dsl import *

S = 'IV-VI'
A4 = 'IV-VI.4'
UN = "choice(['mm', 'cm', 'dm', 'm'])"


def area_unit_skill(*a, **kw):
    return skill(*a, **kw)


# ============================================================================ proste, kąty, wielokąty (4.1-4.6)
skill('n46-line-terms', S, 'Punkt, prosta, półprosta, odcinek', ['IV-VI.4.1'],
      [lvl('Poznaj figury')],
      [('terms', "['punkt', 'prosta', 'półprosta', 'odcinek']"),
       ('descs', "[['Zaznaczamy go kropką i oznaczamy wielką literą.', 'Nie ma długości ani szerokości.', 'Wyznacza miejsce na rysunku, np. na mapie.'], "
                 "['Nie ma początku ani końca.', 'Ciągnie się bez końca w obie strony.', 'Przez dwa różne punkty można poprowadzić dokładnie jedną taką figurę.'], "
                 "['Ma początek, ale nie ma końca.', 'Ciągnie się bez końca tylko w jedną stronę.', 'Ma jeden koniec i biegnie w nieskończoność.'], "
                 "['Ma dwa końce i można zmierzyć jego długość.', 'Jest częścią prostej ograniczoną dwoma punktami.', 'Łączy dwa punkty najkrótszą drogą.']]"),
       ('ti', 'randint(0, 3)'), ('di', 'randint(0, 2)')],
      choice('Którą figurę opisuje zdanie: „@{descs[ti][di]}”?', 'terms[ti]', ['terms[(ti + 1) % 4]', 'terms[(ti + 2) % 4]', 'terms[(ti + 3) % 4]'],
             [('idea', 'Punkt – bez wymiarów. Prosta – bez końców. Półprosta – jeden koniec. Odcinek – dwa końce.'), ('conclude', 'To: @{terms[ti]}.')]),
      min_distinct=12, area=A4,
      intro='Punkt nie ma wymiarów. Prosta nie ma początku ani końca. Półprosta ma początek, ale nie ma końca. Odcinek ma początek i koniec, więc możemy zmierzyć jego długość.')

skill('n46-angle-types', S, 'Rodzaje kątów', ['IV-VI.4.2'],
      [lvl('Ostry, prosty, rozwarty', ts='[0, 1, 2]'), lvl('Także półpełny i pełny', ts='[0, 1, 2, 3, 4]')],
      [('names', "['ostry', 'prosty', 'rozwarty', 'półpełny', 'pełny']"), ('t', 'choice(ts)'),
       ('deg', '[randint(5, 85), 90, randint(95, 175), 180, 360][t]')],
      choice('Kąt ma miarę @{deg}°. Jaki to kąt?', "'kąt ' + names[t]", ["'kąt ' + names[(t + 1) % 5]", "'kąt ' + names[(t + 2) % 5]", "'kąt ' + names[(t + 3) % 5]"],
             [('idea', 'Ostry: mniej niż 90°. Prosty: 90°. Rozwarty: między 90° a 180°. Półpełny: 180°. Pełny: 360°.'), ('conclude', '@{deg}° – kąt @{names[t]}.')],
             media=[{'type': 'figure', 'kind': 'angle', 'essential': False, 'alt': 'Kąt o mierze @{deg}°.', 'params': {'degrees': E('deg')}}]),
      min_distinct=40, area=A4)

skill('n46-angle-convex', S, 'Kąt wypukły czy wklęsły?', ['IV-VI.4.2'],
      [lvl('Wypukły lub wklęsły')],
      [('deg', 'randint(10, 350)')],
      choice_text('Kąt ma miarę @{deg}°. Jaki to kąt?', [('Wypukły (mniejszy niż 180°)', 'deg < 180'), ('Wklęsły (większy niż 180°)', 'deg > 180')], None,
                  [('idea', 'Kąt wypukły ma miarę mniejszą niż 180°, a wklęsły – większą niż 180° (i mniejszą niż 360°).'), ('conclude', '@{deg}° – kąt @{(\'wypukły\' if deg < 180 else \'wklęsły\')}.')],
                  fixed_order=True, media=[{'type': 'figure', 'kind': 'angle', 'essential': False, 'alt': 'Kąt o mierze @{deg}°.', 'params': {'degrees': E('deg')}}]),
      constraints=['deg != 180'], min_distinct=40, area=A4, prereq=['n46-angle-types'])

skill('n46-angle-vertex', S, 'Wierzchołek i ramiona kąta', ['IV-VI.4.2'],
      [lvl('Wierzchołek', ask=0), lvl('Ramiona', ask=1)],
      [('ls', "shuffle(['A', 'B', 'C', 'D', 'K', 'L', 'M', 'P', 'R', 'S'])"), ('p1', 'ls[0]'), ('p2', 'ls[1]'), ('p3', 'ls[2]'), ('p4', 'ls[3]'),
       ('q', "('W kącie ' + p1 + p2 + p3 + ' wierzchołkiem jest punkt:') if ask == 0 else ('Które półproste są ramionami kąta ' + p1 + p2 + p3 + '?')")],
      choice('@{q}', 'p2 if ask == 0 else "półproste " + p2 + p1 + " i " + p2 + p3',
             ['p1 if ask == 0 else "półproste " + p1 + p2 + " i " + p1 + p3', 'p3 if ask == 0 else "półproste " + p3 + p1 + " i " + p3 + p2', 'p4 if ask == 0 else "półproste " + p2 + p4 + " i " + p2 + p3'],
             [('idea', 'W zapisie kąta literę wierzchołka piszemy w środku. Ramiona to półproste wychodzące z wierzchołka.'),
              ('conclude', 'Wierzchołek: @{p2}. Ramiona: @{p2}@{p1} i @{p2}@{p3}.')]),
      min_distinct=30, area=A4, prereq=['n46-line-terms'])

skill('n46-line-relations', S, 'Proste prostopadłe i równoległe', ['IV-VI.4.3'],
      [lvl('Dwie zależności', md=10, n=2), lvl('Trzy zależności', md=20, n=3)],
      [('ns', "choice([['a', 'b', 'c', 'd'], ['k', 'l', 'm', 'n'], ['p', 'q', 'r', 's']])"),
       ('r1', 'randint(0, 1)'), ('r2', 'randint(0, 1)'), ('r3', 'randint(0, 1)'), ('perp', '(r1 + r2 + r3 * (n - 2)) % 2'),
       ('rel', "['równoległe', 'prostopadłe']"),
       ('txt', "('Proste ' + ns[0] + ' i ' + ns[1] + ' są ' + rel[r1] + '. Proste ' + ns[1] + ' i ' + ns[2] + ' są ' + rel[r2] + '. Jak ustawione są proste ' + ns[0] + ' i ' + ns[2] + '?') if n == 2 else "
               "('Proste ' + ns[0] + ' i ' + ns[1] + ' są ' + rel[r1] + ', proste ' + ns[1] + ' i ' + ns[2] + ' są ' + rel[r2] + ', a proste ' + ns[2] + ' i ' + ns[3] + ' są ' + rel[r3] + '. Jak ustawione są proste ' + ns[0] + ' i ' + ns[3] + '?')")],
      choice_text('@{txt}',
                  [('Są prostopadłe', 'perp == 1'), ('Są równoległe', 'perp == 0'), ('Nie da się tego określić', 'false')], None,
                  [('idea', 'Dwie proste równoległe do trzeciej są równoległe do siebie. Każde „przejście” przez prostopadłość obraca kierunek o 90°: nieparzysta liczba prostopadłości daje proste prostopadłe, parzysta – równoległe.'),
                   ('conclude', "@{('Proste są prostopadłe.' if perp == 1 else 'Proste są równoległe.')}")], fixed_order=True),
      area=A4, prereq=['n46-line-terms'])

skill('n46-angle-pairs', S, 'Kąty przyległe, wierzchołkowe, odpowiadające', ['IV-VI.4.4'],
      [lvl('Przyległe', kind=0), lvl('Wierzchołkowe', kind=1), lvl('Odpowiadające i naprzemianległe', kind=2), lvl('Różnica kątów przyległych', md=20, kind=3)],
      [('al', 'randint(20, 160)'), ('d', 'randint(1, 17) * 10'), ('big', 'randint(0, 1)'),
       ('txt', "('Kąty α i β są przyległe. Kąt α ma miarę ' + str(al) + '°. Ile stopni ma kąt β?') if kind == 0 else "
               "(('Kąty α i β są wierzchołkowe. Kąt α ma miarę ' + str(al) + '°. Ile stopni ma kąt β?') if kind == 1 else "
               "(('Dwie proste równoległe przecięto trzecią prostą. Kąt α ma miarę ' + str(al) + '°, a kąt β jest jego kątem ' + choice(['odpowiadającym', 'naprzemianległym']) + '. Ile stopni ma kąt β?') if kind == 2 else "
               "('Kąty przyległe różnią się o ' + str(d) + '°. Ile stopni ma ' + ('większy' if big == 1 else 'mniejszy') + ' z nich?')))"),
       ('ans', '180 - al if kind == 0 else (al if kind < 3 else ((180 + d) // 2 if big == 1 else (180 - d) // 2))')],
      number('@{txt}', 'ans',
             [('idea', '@{(\'Kąty przyległe razem dają 180°.\' if kind == 0 else (\'Kąty wierzchołkowe są równe.\' if kind == 1 else (\'Kąty odpowiadające i naprzemianległe przy prostych równoległych są równe.\' if kind == 2 else \'Dwa kąty przyległe dają razem 180°; jeden jest o różnicę większy od drugiego.\')))}'),
              ('conclude', 'Odpowiedź: @{ans}°.')],
             errors=[('wrong_relation', Int('al if kind == 0 else 180 - al'), 'Sprawdź, czy kąty mają być równe (wierzchołkowe, odpowiadające, naprzemianległe), czy mają dawać razem 180° (przyległe).', 'kind < 3 and al != 90')]),
      constraints=['kind != 3 or (180 - d) % 2 == 0', 'al != 90'], selfCheck=['ans > 0'], min_distinct=30, area=A4, prereq=['n46-angle-types'])

skill('n46-polygon-parts', S, 'Przekątne wielokąta', ['IV-VI.4.5'],
      [lvl('Przekątne z jednego wierzchołka', ask=0), lvl('Wszystkie przekątne', ask=1)],
      [('n', 'randint(4, 20)'), ('ans', 'n - 3 if ask == 0 else n * (n - 3) // 2')],
      number("@{('Ile przekątnych można poprowadzić z jednego wierzchołka wielokąta o ' + str(n) + ' bokach?' if ask == 0 else 'Ile wszystkich przekątnych ma wielokąt o ' + str(n) + ' bokach?')}", 'ans',
             [('idea', "@{('Z wierzchołka nie rysujemy przekątnych do niego samego ani do dwóch sąsiednich wierzchołków: n − 3.' if ask == 0 else 'Z każdego z n wierzchołków wychodzi n − 3 przekątnych, ale każdą policzyliśmy dwa razy.')}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      min_distinct=15, area=A4, prereq=['n46-angle-vertex'])

skill('n46-circle-diameter', S, 'Promień i średnica', ['IV-VI.4.6'],
      [lvl('Liczby całkowite', hi=40, dec=0), lvl('Ułamki dziesiętne', hi=99, dec=1)],
      [('x', 'randint(2, hi) / pow(10, dec) if dec > 0 else randint(2, hi)'), ('un', UN), ('toR', 'randint(0, 1) == 1')],
      quantity("@{('Średnica koła ma ' if toR else 'Promień koła ma ')}@{x|dec} @{un}. Ile @{('wynosi jego promień' if toR else 'wynosi jego średnica')}?", "x / 2 if toR else x * 2", 'un',
               [('idea', 'Średnica jest dwa razy dłuższa niż promień: d = 2r.'), ('compute', "@{(fmt(x) + ' : 2 = ' + fmt(x / 2) if toR else fmt(x) + ' · 2 = ' + fmt(x * 2))} @{un}")], unit_expr=True,
               errors=[('swapped', Qty('x * 2 if toR else x / 2', 'un', True), 'Średnica to dwa promienie. Pytasz o promień (połowa) czy o średnicę (podwójna)?')]),
      constraints=['not toR or denom(x / 2) in divisors(100)'], min_distinct=30, area=A4, prereq=['n46-line-terms'])

skill('n46-circle-terms', S, 'Okrąg, koło, cięciwa, średnica', ['IV-VI.4.6'],
      [lvl('Nazwy elementów')],
      [('terms', "['promień', 'średnica', 'cięciwa', 'środek okręgu']"),
       ('descs', "[['Odcinek łączący środek okręgu z punktem na okręgu.', 'Odcinek od środka okręgu do okręgu.'], "
                 "['Cięciwa przechodząca przez środek okręgu.', 'Najdłuższa cięciwa okręgu.'], "
                 "['Odcinek łączący dowolne dwa punkty okręgu.', 'Odcinek o końcach na okręgu.'], "
                 "['Punkt równo oddalony od wszystkich punktów okręgu.', 'Punkt, od którego mierzymy promień.']]"),
       ('ti', 'randint(0, 3)'), ('di', 'randint(0, 1)')],
      choice('Który element okręgu opisuje zdanie: „@{descs[ti][di]}”?', 'terms[ti]', ['terms[(ti + 1) % 4]', 'terms[(ti + 2) % 4]', 'terms[(ti + 3) % 4]'],
             [('idea', 'Promień – od środka do okręgu. Średnica – przez środek, dwa promienie. Cięciwa – dowolne dwa punkty okręgu.'), ('conclude', 'To: @{terms[ti]}.')]),
      min_distinct=8, area=A4, prereq=['n46-circle-diameter'])

# ============================================================================ trójkąty (4.7-4.10)
skill('n46-triangle-by-angles', S, 'Trójkąt: ostrokątny, prostokątny czy rozwartokątny?', ['IV-VI.4.7'],
      [lvl('Znane trzy kąty')],
      [('t', 'randint(0, 2)'), ('a0', '[randint(45, 75), 90, randint(95, 140)][t]'), ('b0', '[randint(45, 75), randint(15, 75), randint(10, 40)][t]'),
       ('c0', '180 - a0 - b0'), ('angs', 'shuffle([a0, b0, c0])')],
      choice_text('Trójkąt ma kąty: @{angs[0]}°, @{angs[1]}° i @{angs[2]}°. Jaki to trójkąt?',
                  [('Ostrokątny', 'max(angs) < 90'), ('Prostokątny', 'max(angs) == 90'), ('Rozwartokątny', 'max(angs) > 90')], None,
                  [('idea', 'Sprawdź największy kąt: mniejszy niż 90° – ostrokątny, równy 90° – prostokątny, większy niż 90° – rozwartokątny.'),
                   ('conclude', 'Suma: @{angs[0] + angs[1] + angs[2]}°. Największy kąt: @{max(angs)}°.')], fixed_order=True),
      constraints=['t != 0 or (c0 > 20 and c0 < 90)', 't != 2 or c0 > 5'], selfCheck=['a0 + b0 + c0 == 180'], min_distinct=40, area=A4, prereq=['n46-angle-types'])

skill('n46-triangle-by-sides', S, 'Trójkąt: równoboczny, równoramienny czy różnoboczny?', ['IV-VI.4.7'],
      [lvl('Trzy długości boków')],
      [('t', 'randint(0, 2)'), ('a', 'randint(3, 12)'), ('b', 'randint(3, 12)'), ('c', 'randint(3, 12)'),
       ('sides', 'shuffle([a, a, a] if t == 0 else ([a, a, b] if t == 1 else [a, b, c]))'), ('un', "choice(['cm', 'dm', 'm'])")],
      choice_text('Trójkąt ma boki długości @{sides[0]} @{un}, @{sides[1]} @{un} i @{sides[2]} @{un}. Wybierz najdokładniejszą nazwę tego trójkąta.',
                  [('Równoboczny', 'sides[0] == sides[1] and sides[1] == sides[2]'),
                   ('Równoramienny (ale nie równoboczny)', '(sides[0] == sides[1] or sides[1] == sides[2] or sides[0] == sides[2]) and not (sides[0] == sides[1] and sides[1] == sides[2])'),
                   ('Różnoboczny', 'sides[0] != sides[1] and sides[1] != sides[2] and sides[0] != sides[2]')], None,
                  [('idea', 'Porównaj długości boków: wszystkie równe – równoboczny; dwa równe – równoramienny; wszystkie różne – różnoboczny.'),
                   ('conclude', 'Boki: @{sides|list:semi}.')], fixed_order=True),
      constraints=['t != 1 or b != a', 't != 2 or (a != b and b != c and a != c)', 'max(sides) < sum(sides) - max(sides)'], min_distinct=40, area=A4, prereq=['n46-triangle-by-angles'])

skill('n46-triangle-angle', S, 'Trzeci kąt trójkąta', ['IV-VI.4.8'],
      [lvl('Dwa znane kąty', mode=0), lvl('Trójkąt prostokątny', mode=1), lvl('Kąty w zależności od siebie', mode=2)],
      [('a', 'randint(25, 100)'), ('b', 'randint(20, 100)'), ('r', 'randint(2, 4)'), ('x', 'randint(15, 40)'),
       ('txt', "('W trójkącie dwa kąty mają miary ' + str(a) + '° i ' + str(b) + '°. Ile stopni ma trzeci kąt?') if mode == 0 else "
               "(('W trójkącie prostokątnym jeden z kątów ostrych ma ' + str(a) + '°. Ile stopni ma drugi kąt ostry?') if mode == 1 else "
               "('W trójkącie jeden kąt ma ' + str(x) + '°, a drugi jest ' + str(r) + ' razy większy. Ile stopni ma trzeci kąt?'))"),
       ('ans', '180 - a - b if mode == 0 else (90 - a if mode == 1 else 180 - x - r * x)')],
      number('@{txt}', 'ans',
             [('idea', 'Suma kątów w trójkącie wynosi 180°.'), ('conclude', 'Odpowiedź: @{ans}°.')],
             errors=[('sum_360', Int('360 - a - b if mode == 0 else ans'), 'W trójkącie suma kątów to 180°, nie 360°.', 'mode == 0 and 360 - a - b != ans')]),
      constraints=['mode != 0 or a + b < 175', 'mode != 1 or a < 80', 'mode != 2 or x * (1 + r) < 170'], min_distinct=40, area=A4, prereq=['n46-triangle-by-angles'])

skill('n46-quad-angle', S, 'Czwarty kąt czworokąta', ['IV-VI.4.8', 'IV-VI.4.11'],
      [lvl('Trzy znane kąty', mode=0), lvl('Równoległobok i romb', mode=1), lvl('Trapez prostokątny', mode=2)],
      [('a', 'randint(40, 120)'), ('b', 'randint(40, 120)'), ('c', 'randint(40, 120)'), ('al', 'randint(40, 140)'),
       ('txt', "('W czworokącie trzy kąty mają miary ' + str(a) + '°, ' + str(b) + '° i ' + str(c) + '°. Ile stopni ma czwarty kąt?') if mode == 0 else "
               "(('W równoległoboku jeden kąt ma ' + str(al) + '°. Ile stopni ma kąt sąsiedni?') if mode == 1 else "
               "('W trapezie prostokątnym jeden z kątów przy dłuższej podstawie ma ' + str(al) + '°. Ile stopni ma kąt przy tym samym ramieniu, ale przy krótszej podstawie?'))"),
       ('ans', '360 - a - b - c if mode == 0 else 180 - al')],
      number('@{txt}', 'ans',
             [('idea', '@{(\'Suma kątów w czworokącie wynosi 360°.\' if mode == 0 else \'Kąty leżące przy jednym ramieniu (przy jednym boku równoległoboku lub trapezu) dają razem 180°.\')}'),
              ('conclude', 'Odpowiedź: @{ans}°.')]),
      constraints=['mode != 0 or (360 - a - b - c > 30 and 360 - a - b - c < 170)', 'al != 90', 'mode != 2 or al < 90'], min_distinct=40, area=A4, prereq=['n46-triangle-angle'])

skill('n46-isosceles', S, 'Trójkąt równoramienny', ['IV-VI.4.9'],
      [lvl('Kąt przy wierzchołku → kąty przy podstawie', mode=0), lvl('Kąt przy podstawie → kąt przy wierzchołku', mode=1), lvl('Obwód i ramię → podstawa', mode=2)],
      [('apex', '2 * randint(10, 85)'), ('base', 'randint(25, 85)'), ('leg', 'randint(4, 20)'), ('b', 'randint(2, leg * 2 - 1)'), ('per', '2 * leg + b'),
       ('txt', "('W trójkącie równoramiennym kąt między ramionami ma ' + str(apex) + '°. Ile stopni ma każdy z kątów przy podstawie?') if mode == 0 else "
               "(('W trójkącie równoramiennym kąt przy podstawie ma ' + str(base) + '°. Ile stopni ma kąt między ramionami?') if mode == 1 else "
               "('Obwód trójkąta równoramiennego wynosi ' + str(per) + ' cm, a jego ramię ma ' + str(leg) + ' cm. Ile centymetrów ma podstawa?'))"),
       ('ans', '(180 - apex) // 2 if mode == 0 else (180 - 2 * base if mode == 1 else per - 2 * leg)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Kąty przy podstawie są równe, a razem z kątem przy wierzchołku dają 180°.' if mode < 2 else 'Obwód to suma wszystkich boków: dwa ramiona i podstawa.')}"), ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['mode != 1 or base < 89', 'mode != 2 or b != leg'], min_distinct=40, area=A4, prereq=['n46-triangle-angle'])

skill('n46-triangle-exists', S, 'Czy da się zbudować trójkąt?', ['IV-VI.4.10'],
      [lvl('Trzy odcinki')],
      [('a', 'randint(2, 15)'), ('b', 'randint(2, 15)'), ('c', 'randint(2, 25)'), ('un', "choice(['cm', 'dm', 'm'])"),
       ('ok', 'a + b > c and a + c > b and b + c > a')],
      choice_text('Czy z odcinków o długościach @{a} @{un}, @{b} @{un} i @{c} @{un} można zbudować trójkąt?', [('Tak', 'ok'), ('Nie', 'not ok')], None,
                  [('idea', 'Trójkąt istnieje, gdy każdy bok jest krótszy niż suma dwóch pozostałych. Wystarczy sprawdzić najdłuższy bok.'),
                   ('compute', 'Najdłuższy bok: @{max([a, b, c])}, suma pozostałych: @{a + b + c - max([a, b, c])}.')], fixed_order=True),
      constraints=['a + b + c - max([a, b, c]) != max([a, b, c])'], min_distinct=40, area=A4, prereq=['n46-triangle-by-sides'])

skill('n46-triangle-third-side', S, 'Ile możliwości ma trzeci bok?', ['IV-VI.4.10', 'IV-VI.6.3.c'],
      [lvl('Boki całkowite')],
      [('a', 'randint(3, 12)'), ('b', 'randint(3, 12)'), ('lo', 'abs(a - b) + 1'), ('hi', 'a + b - 1')],
      number('Dwa boki trójkąta mają długości @{a} cm i @{b} cm. Trzeci bok ma całkowitą długość w centymetrach. Ile różnych długości może mieć trzeci bok?', 'hi - lo + 1',
             [('idea', 'Trzeci bok musi być krótszy niż suma dwóch boków i dłuższy niż ich różnica.'), ('compute', 'Od @{lo} do @{hi} cm: to @{hi - lo + 1} możliwości.')]),
      constraints=['a != b'], min_distinct=30, area=A4, prereq=['n46-triangle-exists'])

# ============================================================================ czworokąty, symetria, wysokości (4.11-4.13)
QUADS = "['kwadrat', 'prostokąt', 'romb', 'równoległobok', 'trapez', 'trapez równoramienny', 'trapez prostokątny']"
QPROPS = "[[1, 0, 1, 0, 0, 0, 0], [1, 1, 1, 1, 0, 0, 0], [1, 1, 0, 0, 0, 0, 0], [1, 0, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 0, 0, 1, 0]]"
skill('n46-quad-properties', S, 'Własności czworokątów', ['IV-VI.4.11'],
      [lvl('Które czworokąty mają daną własność?')],
      [('names', QUADS), ('props', QPROPS), ('p', 'choice([0, 1, 2, 3, 4, 6])'),
       ('ptxt', "['wszystkie boki równe', 'dwie pary boków równoległych', 'wszystkie kąty proste', 'przekątne prostopadłe', 'przekątne równej długości', 'co najmniej jedną parę boków równoległych', 'co najmniej jedną oś symetrii'][p]"),
       ('idx', 'shuffle([0, 1, 2, 3, 4, 5, 6])')],
      choice_text('Które z poniższych czworokątów mają @{ptxt}? Zaznacz wszystkie.',
                  [(f'@{{names[idx[{i}]]}}', f'props[p][idx[{i}]] == 1') for i in range(5)], None,
                  [('idea', 'Przypomnij sobie rysunki: kwadrat i romb mają równe boki; prostokąt i kwadrat – cztery kąty proste; romb i kwadrat – prostopadłe przekątne.'),
                   ('conclude', 'Sprawdź każdy czworokąt po kolei: czy ma własność „@{ptxt}”?')], multi=True),
      min_distinct=40, area=A4, prereq=['n46-triangle-by-sides'],
      intro='Kwadrat ma wszystkie boki równe i wszystkie kąty proste. Prostokąt ma kąty proste i równe przeciwległe boki. Romb ma wszystkie boki równe. Równoległobok ma dwie pary boków równoległych. Trapez ma co najmniej jedną parę boków równoległych.')

skill('n46-symmetry-axes', S, 'Osie symetrii figur', ['IV-VI.4.12'],
      [lvl('Figury płaskie', md=20, fs='[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]'), lvl('Wielokąty foremne', md=15, fs='[11]')],
      [('names', "['kwadrat', 'prostokąt (niebędący kwadratem)', 'romb (niebędący kwadratem)', 'trójkąt równoboczny', 'trapez równoramienny (niebędący prostokątem)', 'równoległobok (niebędący rombem ani prostokątem)', "
                 "'deltoid (niebędący rombem)', 'trójkąt równoramienny (niebędący równobocznym)', 'trójkąt różnoboczny', 'trapez prostokątny (niebędący prostokątem)', 'trójkąt prostokątny równoramienny']"),
       ('axes', '[4, 2, 2, 3, 1, 0, 1, 1, 0, 0, 1]'), ('f', 'choice(fs)'), ('n', 'randint(3, 20)'), ('ph', 'randint(0, 1)'),
       ('ans', 'axes[f] if f < 11 else n'),
       ('desc', "names[f] if f < 11 else 'wielokąt foremny o ' + str(n) + ' bokach'")],
      number("@{('Ile osi symetrii ma ' + desc + '?' if ph == 0 else 'Na ile sposobów można złożyć ' + desc + ' wzdłuż prostej tak, aby obie części się pokryły?')}", 'ans',
             [('idea', "@{('Oś symetrii dzieli figurę na dwie części, które pokrywają się po złożeniu.' if f < 11 else 'Wielokąt foremny o n bokach ma n osi symetrii.')}"), ('conclude', 'Odpowiedź: @{ans}.')]),
      area=A4, prereq=['n46-quad-properties'])

skill('n46-height-id', S, 'Wysokość trójkąta', ['IV-VI.4.13'],
      [lvl('Wskaż wysokość')],
      [('b', 'randint(8, 12)'), ('cx', 'randint(3, b - 3)'), ('h', 'randint(4, 8)'), ('ok', 'randint(0, 2)'),
       ('x1', 'cx if ok == 0 else cx + 1'), ('x2', 'cx if ok == 1 else cx - 1'), ('x3', 'cx if ok == 2 else cx + 2'), ('lab', "['D', 'E', 'F'][ok]")],
      choice_text('Na rysunku z wierzchołka C poprowadzono trzy odcinki: CD, CE i CF do podstawy AB. Który z nich jest wysokością trójkąta ABC?',
                  [('CD', 'ok == 0'), ('CE', 'ok == 1'), ('CF', 'ok == 2')], None,
                  [('idea', 'Wysokość trójkąta to odcinek poprowadzony z wierzchołka prostopadle do podstawy (lub jej przedłużenia).'),
                   ('conclude', 'Prostopadły do AB jest odcinek C@{lab}.')], fixed_order=True,
                  media=[{'type': 'figure', 'kind': 'triangle', 'essential': True, 'alt': 'Trójkąt ABC z trzema odcinkami CD, CE, CF poprowadzonymi do podstawy.',
                          'params': {'A': [0, 0], 'B': [E('b'), 0], 'C': [E('cx'), E('h')], 'feet': [{'label': 'D', 'x': E('x1')}, {'label': 'E', 'x': E('x2')}, {'label': 'F', 'x': E('x3')}]}}]),
      min_distinct=3, area=A4, prereq=['n46-line-relations'])

