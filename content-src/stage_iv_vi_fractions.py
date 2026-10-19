"""Stage IV-VI, area 1 (Liczby), part 3: integers and common fractions.
Objectives: IV-VI.1.16-1.21, 1.26, 1.27, 1.30, 1.31."""
from dsl import *

S = 'IV-VI'
A1 = 'IV-VI.1'

# ============================================================================ liczby całkowite (1.16)
skill('n46-int-context', S, 'Liczby ujemne w życiu', ['IV-VI.1.16'],
      [lvl('Małe zmiany', smax=10, cmax=10), lvl('Przejście przez zero', smax=15, cmax=20)],
      [('m', 'randint(0, 2)'), ('s', 'randint(-smax, smax)'), ('c', 'randint(-cmax, cmax)'), ('r', 's + c'),
       ('txt', "('Rano termometr wskazywał ' + fmt(s) + ' °C. Do południa temperatura ' + ('wzrosła' if c > 0 else 'spadła') + ' o ' + str(abs(c)) + ' °C. Ile stopni pokazuje termometr w południe?') if m == 0 else "
               "(('Winda stała na poziomie ' + fmt(s) + ' (poziom 0 to parter, poziomy ujemne to piętra podziemne). Pojechała ' + ('w górę' if c > 0 else 'w dół') + ' o ' + pln(abs(c), ['piętro', 'piętra', 'pięter']) + '. Na którym poziomie jest teraz?') if m == 1 else "
               "('Stan konta Oli wynosił ' + fmt(s) + ' zł (liczba ujemna oznacza dług). Ola ' + ('wpłaciła' if c > 0 else 'wydała') + ' ' + str(abs(c)) + ' zł. Jaki jest teraz stan konta w złotych?'))")],
      number('@{txt}', 'r',
             [('idea', 'Zaznacz start na osi liczbowej i przesuń się o zmianę: w prawo, gdy rośnie, w lewo, gdy maleje.'),
              ('compute', '@{s} @{(\'+\' if c > 0 else \'−\')} @{abs(c)} = @{r}')],
             errors=[('sign', Int('-r'), 'Uważaj na znak wyniku: sprawdź, po której stronie zera jesteś.', 'r != 0'),
                     ('ignore_sign_start', Int('abs(s) + c'), 'Liczba ujemna na początku to ruch poniżej zera.', 's < 0 and abs(s) + c != r')]),
      constraints=['c != 0', 's != 0'], min_distinct=20, area=A1,
      intro='Liczby ujemne leżą na osi liczbowej na lewo od zera. Im bardziej na lewo, tym liczba mniejsza. Temperatura poniżej zera, poziom pod ziemią czy dług to przykłady liczb ujemnych.')

skill('n46-int-compare', S, 'Porównywanie liczb całkowitych', ['IV-VI.1.16'],
      [lvl('Małe liczby', m=10), lvl('Większe liczby', m=100)],
      [('a', 'randint(-m, m)'), ('b', 'randint(-m, m)')],
      choice_text('Porównaj liczby @{a} i @{b}. Który znak należy wstawić między nie?',
                  [(r'$<$', 'a < b'), (r'$=$', 'a == b'), (r'$>$', 'a > b')], None,
                  [('idea', 'Na osi liczbowej większa jest ta liczba, która leży bardziej na prawo. Każda liczba dodatnia jest większa od ujemnej.'),
                   ('conclude', '@{a} @{(\'<\' if a < b else \'>\')} @{b}')], fixed_order=True),
      constraints=['a != b', '(a < 0) or (b < 0)'], min_distinct=20, area=A1)

skill('n46-int-order', S, 'Ustaw liczby całkowite w kolejności', ['IV-VI.1.16'],
      [lvl('Od −10 do 10', lo=-10, hi=10), lvl('Od −50 do 50', lo=-50, hi=50)],
      [('xs', 'sample(lo, hi, 5)'), ('desc', 'randint(0, 1) == 1')],
      order('@{(\'Ułóż liczby od największej do najmniejszej.\' if desc else \'Ułóż liczby od najmniejszej do największej.\')}', 'xs', 5,
            [('idea', 'Liczby ujemne są mniejsze od zera: z dwóch ujemnych większa jest ta, która jest bliżej zera (−2 > −7).'),
             ('conclude', 'Kolejność: @{(reverse(sorted(xs)) if desc else sorted(xs))|list:semi}')], fmt='int', descending='desc'),
      constraints=['min(xs) < 0'], area=A1)

skill('n46-int-distance', S, 'Odległość na osi liczbowej', ['IV-VI.1.16'],
      [lvl('Jedna liczba ujemna', m=12), lvl('Dowolne dwie liczby', m=30)],
      [('a', 'randint(-m, m)'), ('b', 'randint(-m, m)'), ('lo', 'min(a, b)'), ('hi', 'max(a, b)')],
      number('Jaka jest odległość między liczbami @{a} i @{b} na osi liczbowej?', 'abs(a - b)',
             [('idea', 'Odległość to różnica większej i mniejszej liczby.'), ('compute', '@{hi} − @{par(lo)} = @{hi - lo}')],
             errors=[('sum_of_abs', Int('abs(a) + abs(b)'), 'Dodajemy wartości bez znaku tylko wtedy, gdy liczby leżą po różnych stronach zera.', 'abs(a) + abs(b) != abs(a - b)')],
             media=[{'type': 'figure', 'kind': 'number-line', 'essential': False, 'alt': 'Oś liczbowa z zaznaczonymi punktami @{a} i @{b}.',
                     'params': {'min': E('min(lo, 0) - 2'), 'max': E('max(hi, 0) + 2'), 'tick': 1, 'labelEvery': 5, 'points': [{'label': 'A', 'at': E('a')}, {'label': 'B', 'at': E('b')}]}}]),
      constraints=['a != b', 'a < 0 or b < 0'], min_distinct=30, area=A1, prereq=['n46-int-compare'])

skill('n46-int-addsub', S, 'Dodawanie i odejmowanie liczb całkowitych', ['IV-VI.1.16'],
      [lvl('Dodawanie', plus=1, m=12), lvl('Odejmowanie', plus=0, m=12), lvl('Dodawanie i odejmowanie', plus=2, m=20)],
      [('a', 'randint(-m, m)'), ('b', 'randint(-m, m)'), ('op', 'randint(0, 1) if plus == 2 else plus'),
       ('r', 'a + b if op == 1 else a - b'), ('sg', "'+' if op == 1 else '−'")],
      number('Oblicz: @{a} @{sg} @{par(b)}', 'r',
             [('idea', '@{(\'Dodać liczbę ujemną to odjąć jej wartość bez znaku.\' if op == 1 else \'Odjąć liczbę to dodać liczbę przeciwną.\')}'),
              ('compute', '@{a} @{sg} @{par(b)} = @{r}')],
             errors=[('wrong_sign_b', Int('a - b if op == 1 else a + b'), 'Sprawdź znak drugiej liczby: odejmowanie liczby ujemnej to dodawanie jej wartości bez znaku.', 'b != 0')]),
      constraints=['a != 0', 'b != 0', 'b < 0 or a < 0 or op == 0', 'op == 1 or a != b'], selfCheck=['r - a == (b if op == 1 else -b)'], min_distinct=40, area=A1, prereq=['n46-int-context'])

skill('n46-int-muldiv', S, 'Mnożenie i dzielenie liczb całkowitych', ['IV-VI.1.16'],
      [lvl('Mnożenie', mul=1), lvl('Dzielenie', mul=0)],
      [('x', 'randint(-9, 9)'), ('y', 'randint(2, 9) * choice([-1, 1])'), ('p', 'x * y'),
       ('a', 'p if mul == 0 else x'), ('b', 'y if mul == 0 else y'), ('r', 'x if mul == 0 else p')],
      number('Oblicz: @{a} @{(\'·\' if mul == 1 else \':\')} @{par(b)}', 'r',
             [('idea', 'Dwie liczby o takich samych znakach dają wynik dodatni, a o różnych znakach – ujemny.'),
              ('conclude', '@{a} @{(\'·\' if mul == 1 else \':\')} @{par(b)} = @{r}')]),
      constraints=['x != 0', 'x != 1', 'x != -1', 'x < 0 or y < 0'], selfCheck=['(r * b == a) if mul == 0 else (a * b == r)'], min_distinct=40, area=A1, prereq=['n46-int-addsub'])

# ============================================================================ ułamki zwykłe: pojęcie (1.17, 1.18, 1.19, 1.20, 1.21)
skill('n46-frac-part-figure', S, 'Jaka część figury?', ['IV-VI.1.17'],
      [lvl('Do ósmych części', dmax=8), lvl('Do dwunastych części', dmax=12)],
      [('d', 'randint(3, dmax)'), ('k', 'randint(1, d - 1)'),
       ('shape', "choice([['Prostokąt', 'prostokąta'], ['Koło', 'koła'], ['Pasek papieru', 'paska']])"),
       ('eqp', "'równe' if d in [2, 3, 4] else 'równych'")],
      fraction('@{shape[0]} podzielono na @{d} @{eqp} części i zacieniowano @{k} z nich. Jaką część @{shape[1]} zacieniowano?', 'k', 'd',
               [('idea', 'Ułamek to liczba zacieniowanych części (licznik) przez liczbę wszystkich równych części (mianownik).'),
                ('conclude', '$\\frac{@{k}}{@{d}}$')], lowest=False,
               media=[{'type': 'figure', 'kind': 'fraction-bar', 'essential': False, 'alt': '@{shape[0]} podzielony na @{d} równych części, @{k} zacieniowane.',
                       'params': {'parts': E('d'), 'shaded': E('k')}}],
               errors=[('flip', Rat('d', 'k', False), 'W liczniku jest liczba zacieniowanych części, a w mianowniku – wszystkich.', 'k != 1'),
                       ('rest', Rat('d - k', 'd', False), 'To jest część niezacieniowana. Zapisz część zacieniowaną.')]),
      area=A1,
      intro='Ułamek zwykły $\\frac{a}{b}$ mówi, że całość podzielono na b równych części i wzięto a z nich. Mianownik (b) pokazuje, na ile części podzielono całość, a licznik (a) – ile części bierzemy.')

skill('n46-frac-part-set', S, 'Jaka część zbioru?', ['IV-VI.1.17'],
      [lvl('Do 12 przedmiotów', thi=12), lvl('Do 30 przedmiotów', thi=30)],
      [('ctx', "choice([[['kredka', 'kredki', 'kredek'], 'czerwonych', 'czerwone'], [['piłka', 'piłki', 'piłek'], 'białych', 'białe'], "
               "[['jabłko', 'jabłka', 'jabłek'], 'zielonych', 'zielone'], [['kartka', 'kartki', 'kartek'], 'żółtych', 'żółte'], [['guzik', 'guziki', 'guzików'], 'niebieskich', 'niebieskie']])"),
       ('t', 'randint(5, thi)'), ('p', 'randint(1, t - 1)')],
      fraction('W pudełku jest @{t|pl:ctx[0]}, w tym @{ctx[1]}: @{p}. Jaką część wszystkich @{ctx[0][2]} stanowią @{ctx[2]}?', 'p', 't',
               [('idea', 'Licznik: ile jest @{ctx[1]}. Mianownik: ile jest wszystkich.'), ('conclude', '$\\frac{@{p}}{@{t}}$')], lowest=False,
               errors=[('rest', Rat('t - p', 't', False), 'To jest część pozostałych. Zapisz część pytaną w zadaniu.')]),
      area=A1, prereq=['n46-frac-part-figure'])

skill('n46-frac-quotient', S, 'Ułamek jako iloraz', ['IV-VI.1.18'],
      [lvl('Podział w zadaniu', mode=0, bhi=9), lvl('Zapis ilorazu', mode=1, bhi=12)],
      [('b', 'randint(3, bhi)'), ('a', 'randint(2, b - 1)'),
       ('txt', "('Podzielono po równo ' + pln(a, ['tabliczkę', 'tabliczki', 'tabliczek']) + ' czekolady między ' + pln(b, ['osobę', 'osoby', 'osób']) + '. Jaką część tabliczki dostała każda osoba?') if mode == 0 "
               "else 'Zapisz iloraz ' + str(a) + ' : ' + str(b) + ' w postaci ułamka zwykłego.'")],
      fraction('@{txt}', 'a', 'b', [('idea', 'Dzielenie liczb naturalnych można zapisać ułamkiem: dzielna to licznik, dzielnik to mianownik.'),
                                   ('conclude', '@{a} : @{b} = $\\frac{@{a}}{@{b}}$')], lowest=False,
               errors=[('flip', Rat('b', 'a', False), 'Dzielna idzie do licznika, a dzielnik do mianownika.')]),
      area=A1, prereq=['n46-frac-part-set'])

skill('n46-frac-simplify', S, 'Skracanie ułamków', ['IV-VI.1.19'],
      [lvl('Małe liczby', max_b=10, max_g=5), lvl('Większe liczby', max_b=12, max_g=9)],
      [('a', 'randint(1, max_b - 1)'), ('b', 'randint(a + 1, max_b)'), ('g', 'randint(2, max_g)'), ('num', 'a * g'), ('den', 'b * g')],
      fraction('Skróć ułamek $\\frac{@{num}}{@{den}}$ do postaci nieskracalnej.', 'a', 'b',
               [('idea', 'Szukamy liczby, przez którą dzielą się i licznik, i mianownik.'), ('compute', 'Największa taka liczba to NWD(@{num}, @{den}) = @{g}.'),
                ('compute', 'Dzielimy: @{num} : @{g} = @{a} oraz @{den} : @{g} = @{b}.'), ('conclude', 'Wynik: $\\frac{@{a}}{@{b}}$ – tego ułamka nie da się już skrócić.')],
               errors=[('flip', Rat('b', 'a', False), 'Licznik z mianownikiem nie zamieniają się miejscami.', 'a != b'),
                       ('subtract', Rat('num - g', 'den - g', False), 'Skracanie to dzielenie licznika i mianownika przez tę samą liczbę – nie odejmowanie.')]),
      constraints=['gcd(a, b) == 1'], selfCheck=['gcd(a, b) == 1', 'num * b == den * a'], min_distinct=40, area=A1, prereq=['n46-gcd'],
      intro='Skrócić ułamek to podzielić licznik i mianownik przez tę samą liczbę różną od zera. Wartość ułamka się nie zmienia, np. $\\frac{6}{8} = \\frac{3}{4}$.')

skill('n46-frac-extend', S, 'Rozszerzanie ułamków', ['IV-VI.1.19'],
      [lvl('Mianowniki do 30', mhi=30), lvl('Mianowniki do 100', mhi=100)],
      [('b', 'randint(2, 12)'), ('a', 'randint(1, b - 1)'), ('k', 'randint(2, mhi // b)'), ('m', 'b * k')],
      number('Rozszerz ułamek $\\frac{@{a}}{@{b}}$ tak, aby jego mianownik był równy @{m}. Jaki będzie licznik?', 'a * k',
             [('idea', 'Mianownik pomnożono przez @{k} (bo @{b} · @{k} = @{m}), więc licznik też mnożymy przez @{k}.'), ('compute', '@{a} · @{k} = @{a * k}')],
             errors=[('add', Int('a + k'), 'Rozszerzanie to mnożenie licznika i mianownika przez tę samą liczbę – nie dodawanie.'),
                     ('unchanged', Int('a'), 'Licznik też trzeba zmienić, żeby wartość ułamka została taka sama.')]),
      constraints=['gcd(a, b) == 1', 'k >= 2'], selfCheck=['a * k * b == a * m'], min_distinct=30, area=A1, prereq=['n46-frac-simplify'])

skill('n46-lcd', S, 'Wspólny mianownik', ['IV-VI.1.19'],
      [lvl('Mianowniki do 12', hi=12, ask=0), lvl('Licznik po sprowadzeniu', hi=12, ask=1), lvl('Mianowniki dwucyfrowe', hi=20, ask=1)],
      [('b', 'randint(2, hi)'), ('d', 'randint(2, hi)'), ('a', 'randint(1, b - 1)'), ('c', 'randint(1, d - 1)'), ('l', 'lcm(b, d)'),
       ('q', "'Jaki jest najmniejszy wspólny mianownik ułamków ' + '$\\\\frac{' + str(a) + '}{' + str(b) + '}$ i $\\\\frac{' + str(c) + '}{' + str(d) + '}$?' if ask == 0 else "
             "'Sprowadź ułamki $\\\\frac{' + str(a) + '}{' + str(b) + '}$ i $\\\\frac{' + str(c) + '}{' + str(d) + '}$ do najmniejszego wspólnego mianownika. Ile wynosi licznik pierwszego ułamka?'"),
       ('ans', 'l if ask == 0 else a * (l // b)')],
      number('@{q}', 'ans',
             [('idea', 'Wspólny mianownik to wspólna wielokrotność mianowników; najmniejszy to NWW(@{b}, @{d}) = @{l}.'),
              ('compute', 'Mnożnik pierwszego ułamka: @{l // b}, drugiego: @{l // d}.')]),
      constraints=['b != d', 'gcd(a, b) == 1 or ask == 0', 'l <= 100'], selfCheck=['l % b == 0', 'l % d == 0'], min_distinct=30, area=A1, prereq=['n46-lcm', 'n46-frac-extend'])

skill('n46-frac-to-mixed', S, 'Ułamek niewłaściwy na liczbę mieszaną', ['IV-VI.1.20'],
      [lvl('Mianowniki do 6', dmax=6), lvl('Mianowniki do 12', dmax=12)],
      [('d', 'randint(2, dmax)'), ('w', 'randint(1, 6)'), ('r', 'randint(1, d - 1)'), ('n', 'w * d + r')],
      task('mixed-number-input', 'Zapisz ułamek niewłaściwy $\\frac{@{n}}{@{d}}$ w postaci liczby mieszanej.', Mixed('w', 'r', 'd'),
           [('idea', 'Dzielimy licznik przez mianownik z resztą: iloraz to część całkowita, reszta to nowy licznik.'),
            ('compute', '@{n} : @{d} = @{w} r @{r}, więc $\\frac{@{n}}{@{d}} = @{w}\\frac{@{r}}{@{d}}$')],
           errors=[('forget_rest', Mixed('w', 'r', 'n'), 'Mianownik zostaje taki sam jak w ułamku niewłaściwym.')]),
      constraints=['gcd(r, d) == 1'], selfCheck=['w * d + r == n'], min_distinct=30, area=A1, prereq=['n46-div-rem', 'n46-frac-part-set'],
      intro='Ułamek niewłaściwy ma licznik większy lub równy mianownikowi, np. $\\frac{7}{3}$. Liczba mieszana składa się z całości i ułamka: $2\\frac{1}{3}$.')

skill('n46-mixed-to-frac', S, 'Liczba mieszana na ułamek niewłaściwy', ['IV-VI.1.20'],
      [lvl('Mianowniki do 6', dmax=6), lvl('Mianowniki do 12', dmax=12)],
      [('d', 'randint(2, dmax)'), ('w', 'randint(1, 8)'), ('r', 'randint(1, d - 1)'), ('n', 'w * d + r')],
      fraction('Zapisz liczbę mieszaną $@{w}\\frac{@{r}}{@{d}}$ w postaci ułamka niewłaściwego.', 'n', 'd',
               [('idea', 'Mnożymy całości przez mianownik i dodajemy licznik: @{w} · @{d} + @{r}.'), ('compute', '@{w * d} + @{r} = @{n}, więc $\\frac{@{n}}{@{d}}$')], lowest=False,
               errors=[('no_add', Rat('w * d', 'd', False), 'Do iloczynu całości i mianownika dodaj jeszcze licznik.')]),
      constraints=['gcd(r, d) == 1'], min_distinct=30, area=A1, prereq=['n46-frac-to-mixed'])

skill('n46-frac-number-line', S, 'Ułamek na osi liczbowej', ['IV-VI.1.21'],
      [lvl('Między 0 i 1', maxv=1), lvl('Między 0 i 2', maxv=2)],
      [('d', 'randint(3, 10)'), ('k', 'randint(1, d * maxv - 1)'), ('mx', 'maxv')],
      fraction('Jaki ułamek oznacza punkt A na osi liczbowej?', 'k', 'd',
               [('idea', 'Każda jednostka jest podzielona na @{d} równych części, więc jedna kreska to $\\frac{1}{@{d}}$.'),
                ('conclude', 'Punkt A leży na @{k}. kresce: $\\frac{@{k}}{@{d}}$.')], lowest=False,
               media=[{'type': 'figure', 'kind': 'number-line', 'essential': True, 'alt': 'Oś liczbowa od 0 do @{mx}, każda jednostka podzielona na @{d} równych części; zaznaczony punkt A.',
                       'params': {'min': 0, 'max': E('mx'), 'partsPerUnit': E('d'), 'points': [{'label': 'A', 'at': {'num': E('k'), 'den': E('d')}}]}}]),
      constraints=['gcd(k, d) == 1'], min_distinct=15, area=A1, prereq=['n46-frac-part-figure'])

# ============================================================================ porównywanie ułamków (1.26, 1.30)
skill('n46-frac-compare', S, 'Porównywanie ułamków zwykłych', ['IV-VI.1.26'],
      [lvl('Jednakowe mianowniki', kind=0), lvl('Jednakowe liczniki', kind=1), lvl('Różne mianowniki', kind=2), lvl('Także równe ułamki', kind=3)],
      [('v1', 'randint(3, 12)'), ('u1', 'randint(1, v1 - 1)'), ('eq', 'randint(0, 3) == 0 if kind == 3 else False'), ('k', 'randint(2, 3)'),
       ('v2', 'v1 * k if eq else (v1 if kind == 0 else (randint(u1 + 1, 12) if kind == 1 else randint(3, 12)))'),
       ('u2', 'u1 * k if eq else (u1 if kind == 1 else randint(1, v2 - 1))')],
      choice_text('Porównaj ułamki $\\frac{@{u1}}{@{v1}}$ i $\\frac{@{u2}}{@{v2}}$. Który znak należy wstawić między nie?',
                  [(r'$<$', 'u1 * v2 < u2 * v1'), (r'$=$', 'u1 * v2 == u2 * v1'), (r'$>$', 'u1 * v2 > u2 * v1')], None,
                  [('idea', "@{('Przy jednakowych mianownikach większy jest ułamek z większym licznikiem.' if kind == 0 else ('Przy jednakowych licznikach większy jest ułamek z mniejszym mianownikiem.' if kind == 1 else 'Sprowadź ułamki do wspólnego mianownika i porównaj liczniki.'))}"),
                   ('compute', 'Po sprowadzeniu do mianownika @{v1 * v2}: liczniki @{u1 * v2} i @{u2 * v1}.')], fixed_order=True),
      constraints=['eq or u1 * v2 != u2 * v1'], min_distinct=30, area=A1, prereq=['n46-frac-part-figure'])

skill('n46-frac-order', S, 'Ustaw ułamki w kolejności', ['IV-VI.1.26'],
      [lvl('Jednakowe mianowniki', kind=0), lvl('Mianowniki 2, 4, 8 lub 3, 6, 12 lub 5, 10, 20', kind=1)],
      [('v', 'randint(8, 16)'), ('n', 'sample(1, v - 1, 4)'), ('fam', 'choice([[2, 4, 8], [3, 6, 12], [5, 10, 20]])'),
       ('m0', 'randint(1, fam[0] - 1)'), ('m1', 'randint(1, fam[1] - 1)'), ('m2', 'randint(1, fam[2] - 1)'), ('m3', 'randint(1, fam[2] - 1)'),
       ('xs', '[n[0] / v, n[1] / v, n[2] / v, n[3] / v] if kind == 0 else [m0 / fam[0], m1 / fam[1], m2 / fam[2], m3 / fam[2]]'),
       ('desc', 'randint(0, 1) == 1')],
      order("@{('Ułóż ułamki od największego do najmniejszego.' if desc else 'Ułóż ułamki od najmniejszego do największego.')}", 'xs', 4,
            [('idea', 'Sprowadź ułamki do wspólnego mianownika i porównaj liczniki.'),
             ('conclude', 'Kolejność: @{(reverse(sorted(xs)) if desc else sorted(xs))|list:semi:frac}')], fmt='frac', descending='desc', math=True),
      min_distinct=30, area=A1, prereq=['n46-frac-compare'])

skill('n46-frac-diff', S, 'O ile jeden ułamek jest większy od drugiego?', ['IV-VI.1.30'],
      [lvl('Jednakowe mianowniki', kind=0), lvl('Mianownik jednego jest wielokrotnością drugiego', kind=1)],
      [('b', 'randint(3, 12)'), ('k', 'randint(2, 3)'), ('a', 'randint(2, b - 1)'),
       ('c', 'randint(1, b - 1) if kind == 0 else randint(1, b * k - 1)'),
       ('x', 'a / b'), ('y', 'c / b if kind == 0 else c / (b * k)'), ('r', 'x - y')],
      fraction('O ile ułamek $\\frac{@{a}}{@{b}}$ jest większy od ułamka $\\frac{@{c}}{@{(b if kind == 0 else b * k)}}$?', 'numer(r)', 'denom(r)',
               [('idea', 'Sprowadzamy ułamki do wspólnego mianownika i odejmujemy liczniki.'), ('conclude', 'Różnica: $\\frac{@{numer(r)}}{@{denom(r)}}$')]),
      constraints=['x > y', 'denom(r) > 1'], selfCheck=['r + y == x'], min_distinct=20, area=A1, prereq=['n46-frac-compare'])

# ============================================================================ działania na ułamkach (1.27)
skill('n46-frac-addsub', S, 'Dodawanie i odejmowanie ułamków', ['IV-VI.1.27'],
      [lvl('Jednakowe mianowniki', kind=0), lvl('Jeden mianownik dzieli drugi', kind=1), lvl('Mianowniki względnie pierwsze', kind=2), lvl('Dowolne mianowniki do 20', kind=3)],
      [('b', 'randint(3, 12) if kind < 3 else randint(4, 20)'),
       ('d', 'b if kind == 0 else (b * randint(2, 3) if kind == 1 else randint(3, 12) if kind == 2 else randint(4, 20))'),
       ('a', 'randint(1, b - 1)'), ('c', 'randint(1, d - 1)'), ('plus', 'randint(0, 1) == 1'),
       ('x', 'a / b'), ('y', 'c / d'), ('r', 'x + y if plus else x - y'), ('sg', "'+' if plus else '-'")],
      fraction('Oblicz: $\\frac{@{a}}{@{b}} @{sg} \\frac{@{c}}{@{d}}$', 'numer(r)', 'denom(r)',
               [('idea', 'Sprowadź ułamki do wspólnego mianownika, potem dodaj (odejmij) liczniki. Mianownik się nie zmienia.'),
                ('compute', 'Wspólny mianownik: @{lcm(b, d)}. @{a * (lcm(b, d) // b)} @{(\'+\' if plus else \'−\')} @{c * (lcm(b, d) // d)} = @{abs(a * (lcm(b, d) // b) + (c * (lcm(b, d) // d) if plus else -c * (lcm(b, d) // d)))} (licznik).')],
               errors=[('add_parts', Rat('a + c if plus else a - c', 'b + d if plus else b - d', False),
                        'Mianowników nie dodajemy ani nie odejmujemy: po sprowadzeniu do wspólnego mianownika zostaje on bez zmian.', 'b + d != 0 and b - d != 0')]),
      constraints=['plus or x > y', 'denom(r) > 1', 'kind != 2 or gcd(b, d) == 1', 'kind != 3 or (b != d and b % d != 0 and d % b != 0)',
                   'kind != 1 or b != d', 'kind != 0 or b == d'], min_distinct=30, area=A1, prereq=['n46-lcd'],
      intro='Aby dodać lub odjąć ułamki o różnych mianownikach, sprowadzamy je do wspólnego mianownika. Przy jednakowych mianownikach dodajemy (odejmujemy) tylko liczniki: $\\frac{2}{7} + \\frac{3}{7} = \\frac{5}{7}$.')

skill('n46-frac-addsub-mixed', S, 'Liczby mieszane: dodawanie i odejmowanie', ['IV-VI.1.27'],
      [lvl('Bez przekraczania całości', hard=0), lvl('Z przenoszeniem całości', hard=1)],
      [('b', 'choice([2, 3, 4, 5, 6, 8, 10])'), ('d', 'b * randint(1, 2) if hard == 0 else choice([2, 3, 4, 5, 6, 8, 10])'),
       ('w1', 'randint(1, 5)'), ('w2', 'randint(1, 4)'), ('a', 'randint(1, b - 1)'), ('c', 'randint(1, d - 1)'),
       ('plus', 'randint(0, 1) == 1'), ('x', 'w1 + a / b'), ('y', 'w2 + c / d'), ('r', 'x + y if plus else x - y'), ('sg', "'+' if plus else '-'"),
       ('rw', 'floor(r)'), ('rf', 'r - rw')],
      task('mixed-number-input', 'Oblicz: $@{w1}\\frac{@{a}}{@{b}} @{sg} @{w2}\\frac{@{c}}{@{d}}$', Mixed('rw', 'numer(rf)', 'denom(rf)'),
           [('idea', 'Dodaj (odejmij) osobno całości i osobno ułamki; w razie potrzeby zamień nadmiar ułamka na całość.'),
            ('conclude', 'Wynik: $@{rw}\\frac{@{numer(rf)}}{@{denom(rf)}}$')]),
      constraints=['plus or x > y', 'denom(rf) > 1', 'rw >= 1', 'gcd(b, d) == 1 or b % d == 0 or d % b == 0', 'gcd(a, b) == 1', 'gcd(c, d) == 1',
                   'hard == 1 or ((a / b + c / d < 1) if plus else (a / b > c / d))', 'hard == 0 or ((a / b + c / d >= 1) if plus else (a / b < c / d))'], selfCheck=['rw + rf == r'], min_distinct=30, area=A1, prereq=['n46-frac-addsub', 'n46-frac-to-mixed'])

skill('n46-frac-mul', S, 'Mnożenie ułamków', ['IV-VI.1.27'],
      [lvl('Ułamek razy liczba naturalna', kind=0), lvl('Ułamek razy ułamek', kind=1), lvl('Liczby mieszane', kind=2)],
      [('b', 'randint(3, 12)'), ('a', 'randint(1, b - 1)'), ('d', 'randint(3, 12)'), ('c', 'randint(1, d - 1)'), ('n', 'randint(2, 9)'), ('w', 'randint(1, 3)'),
       ('x', 'a / b'), ('y', 'n if kind == 0 else (c / d if kind == 1 else w + c / d)'), ('r', 'x * y'),
       ('txt', "'$\\\\frac{' + str(a) + '}{' + str(b) + '} \\\\cdot ' + (str(n) if kind == 0 else ('\\\\frac{' + str(c) + '}{' + str(d) + '}' if kind == 1 else str(w) + '\\\\frac{' + str(c) + '}{' + str(d) + '}')) + '$'")],
      fraction('Oblicz: @{txt}', 'numer(r)', 'denom(r)',
               [('idea', 'Mnożymy liczniki przez siebie i mianowniki przez siebie (liczbę mieszaną najpierw zamieniamy na ułamek niewłaściwy). Skracamy, jeśli można.'),
                ('conclude', 'Wynik: $\\frac{@{numer(r)}}{@{denom(r)}}$')],
               errors=[('only_numerators', Rat('a * c', 'b', False), 'Mianowniki też trzeba pomnożyć (a nie zostawiać).', 'kind == 1')]),
      constraints=['denom(r) > 1', 'gcd(a, b) == 1', 'kind == 0 or gcd(c, d) == 1'], min_distinct=30, area=A1, prereq=['n46-frac-simplify', 'n46-mixed-to-frac'])

skill('n46-frac-div', S, 'Dzielenie ułamków', ['IV-VI.1.27'],
      [lvl('Ułamek podzielony przez liczbę', kind=0), lvl('Ułamek podzielony przez ułamek', kind=1), lvl('Liczby mieszane', kind=2)],
      [('b', 'randint(3, 12)'), ('a', 'randint(1, b - 1)'), ('d', 'randint(3, 12)'), ('c', 'randint(1, d - 1)'), ('n', 'randint(2, 9)'), ('w', 'randint(1, 3)'),
       ('x', 'a / b'), ('y', 'n if kind == 0 else (c / d if kind == 1 else w + c / d)'), ('r', 'x / y'),
       ('txt', "'$\\\\frac{' + str(a) + '}{' + str(b) + '} : ' + (str(n) if kind == 0 else ('\\\\frac{' + str(c) + '}{' + str(d) + '}' if kind == 1 else str(w) + '\\\\frac{' + str(c) + '}{' + str(d) + '}')) + '$'")],
      fraction('Oblicz: @{txt}', 'numer(r)', 'denom(r)',
               [('idea', 'Dzielenie przez ułamek zamieniamy na mnożenie przez odwrotność: odwracamy dzielnik (liczbę zamieniamy na ułamek $\\frac{n}{1}$).'),
                ('conclude', 'Wynik: $\\frac{@{numer(r)}}{@{denom(r)}}$')],
               errors=[('multiply_instead', Rat('numer(x * y)', 'denom(x * y)', False), 'Przy dzieleniu odwracamy drugi ułamek (zamieniamy go na odwrotność), a potem mnożymy.', 'x * y != r')]),
      constraints=['denom(r) > 1', 'gcd(a, b) == 1', 'kind == 0 or gcd(c, d) == 1', 'x != y'], min_distinct=30, area=A1, prereq=['n46-frac-mul'])

skill('n46-frac-of-number', S, 'Ułamek danej liczby', ['IV-VI.1.31'],
      [lvl('Mianowniki do 10', bmax=10, mmax=12), lvl('Większe liczby', bmax=20, mmax=40)],
      [('b', 'randint(2, bmax)'), ('a', 'randint(1, b - 1)'), ('m', 'randint(2, mmax)'), ('n', 'b * m')],
      number('Oblicz $\\frac{@{a}}{@{b}}$ z liczby @{n}.', 'a * m',
             [('idea', 'Najpierw dzielimy liczbę przez @{b}: @{n} : @{b} = @{m}. Potem bierzemy @{a} z tych części.'), ('compute', '@{a} · @{m} = @{a * m}')],
             errors=[('divide_only', Int('m'), 'Podzieliłeś na części, ale trzeba jeszcze wziąć ich tyle, ile mówi licznik.', 'a != 1'),
                     ('multiply_only', Int('a * n'), 'Ułamek mniejszy od 1 daje wynik mniejszy od całości.')]),
      constraints=['gcd(a, b) == 1'], selfCheck=['a * m * b == a * n'], min_distinct=30, area=A1, prereq=['n46-frac-part-set'],
      intro='Aby obliczyć ułamek $\\frac{a}{b}$ z liczby, dzielimy tę liczbę przez b, a wynik mnożymy przez a.')

skill('n46-frac-of-quantity', S, 'Ułamek wielkości w zadaniach', ['IV-VI.1.31'],
      [lvl('Jedna część', two=0), lvl('Dwie części', two=1)],
      [('b', 'choice([2, 3, 4, 5, 6, 8, 10])'), ('a', 'randint(1, b - 1)'), ('m', 'randint(2, 12)'), ('n', 'b * m'),
       ('c', 'randint(1, b - a) if two == 1 else 0'),
       ('ctx', "choice([['Książka ma', 'stron', 'Ola przeczytała'], ['Zbiornik mieści', 'litrów', 'Zużyto'], ['Droga ma długość', 'km', 'Rowerzysta przejechał'], ['Sklep miał', 'kg jabłek', 'Sprzedano']])"),
       ('part', 'n // b * a'), ('part2', 'n // b * c'), ('left', 'n - part - part2'),
       ('txt', "(ctx[0] + ' ' + str(n) + ' ' + ctx[1] + '. ' + ctx[2] + ' $\\\\frac{' + str(a) + '}{' + str(b) + '}$ całości. Ile ' + ctx[1] + ' zostało?') if two == 0 else "
               "(ctx[0] + ' ' + str(n) + ' ' + ctx[1] + '. ' + ctx[2] + ' najpierw $\\\\frac{' + str(a) + '}{' + str(b) + '}$ całości, a potem jeszcze $\\\\frac{' + str(c) + '}{' + str(b) + '}$ całości. Ile ' + ctx[1] + ' zostało?')")],
      number('@{txt}', 'left',
             [('idea', 'Policz, ile to jedna @{b}. część całości, a potem ile jest razem zabrane.'), ('compute', '@{n} : @{b} = @{n // b}; zabrano @{part + part2}; zostało @{n} − @{part + part2} = @{left}')],
             errors=[('answer_part', Int('part + part2'), 'To jest zabrana część. Zadanie pyta o to, co zostało.')]),
      constraints=['left > 0', 'a + c < b'], min_distinct=30, area=A1, prereq=['n46-frac-of-number'])
