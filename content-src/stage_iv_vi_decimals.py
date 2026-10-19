"""Stage IV-VI, area 1 (Liczby), part 4: decimal fractions.
Objectives: IV-VI.1.21-1.26, 1.28, 1.29, 1.32.  Caps from the regulation: at most three digits after the decimal comma;
division only where it reduces to a natural divisor of at most three digits."""
from dsl import *

S = 'IV-VI'
A1 = 'IV-VI.1'

skill('n46-dec-place-value', S, 'Cyfra na miejscu dziesiętnym', ['IV-VI.1.22'],
      [lvl('Dziesiąte', k=1), lvl('Setne', k=2), lvl('Tysięczne', k=3)],
      [('nn', 'randint(pow(10, k + 1), pow(10, k + 3) - 1)'), ('x', 'nn / pow(10, k)'), ('pos', 'randint(-k, 1)'),
       ('pn', "['tysięcznych', 'setnych', 'dziesiątych', 'jedności', 'dziesiątek', 'setek'][pos + 3]"),
       ('d', '(nn // pow(10, pos + k)) % 10')],
      number('Jaka cyfra stoi na miejscu @{pn} w liczbie @{x|dec:k}?', 'd',
             [('idea', 'Za przecinkiem kolejne miejsca to: dziesiąte, setne, tysięczne. Przed przecinkiem: jedności, dziesiątki, setki.'),
              ('conclude', 'Na miejscu @{pn} stoi cyfra @{d}.')]),
      constraints=['nn % 10 != 0'], selfCheck=['d < 10'], min_distinct=40, area=A1,
      intro='Ułamek dziesiętny ma część całkowitą i część ułamkową oddzielone przecinkiem. Pierwsza cyfra po przecinku to dziesiąte, druga – setne, trzecia – tysięczne części całości.')

skill('n46-dec-from-fraction', S, 'Ułamek zwykły na dziesiętny', ['IV-VI.1.23'],
      [lvl('Mianowniki 10 i 100', ds='[10, 100]'), lvl('Mianownik 1000', ds='[1000]'), lvl('Rozszerzanie do 10, 100, 1000', ds='[2, 4, 5, 8, 20, 25, 50]')],
      [('d', 'choice(ds)'), ('k', 'randint(1, d - 1)'),
       ('p10', '10 if 10 % d == 0 else (100 if 100 % d == 0 else 1000)'), ('m', 'p10 // d'), ('v', 'k / d')],
      decimal('Zapisz ułamek $\\frac{@{k}}{@{d}}$ w postaci dziesiętnej.', 'v',
              [('idea', "@{('Mianownik wynosi już ' + str(d) + ', więc zapisujemy ułamek od razu dziesiętnie: tyle miejsc po przecinku, ile zer w mianowniku.' if m == 1 else 'Rozszerzamy ułamek tak, aby mianownik wynosił ' + str(p10) + ' (mnożymy licznik i mianownik przez ' + str(m) + ').')}"),
               ('compute', '$\\frac{@{k}}{@{d}} = @{v|dec}$')],
              errors=[('wrong_places', Dec('k / (d * 10)'), 'Policz zera w mianowniku: tyle miejsc po przecinku musi mieć wynik.', 'k / (d * 10) != v')]),
      constraints=['k % 10 != 0 or d < 100'], selfCheck=['v * d == k', 'denom(v) in divisors(1000)'], min_distinct=30, area=A1, prereq=['n46-frac-extend', 'n46-dec-place-value'],
      intro='Ułamek o mianowniku 10, 100 lub 1000 zapisujemy od razu dziesiętnie: $\\frac{7}{100} = 0{,}07$. Inne mianowniki (np. 4, 5, 20, 25) rozszerzamy do 10, 100 lub 1000.')

skill('n46-dec-to-fraction', S, 'Ułamek dziesiętny na zwykły', ['IV-VI.1.22'],
      [lvl('Do setnych', k=2, kmin=1), lvl('Do tysięcznych', k=3, kmin=2)],
      [('kk', 'randint(kmin, k)'), ('nn', 'randint(1, pow(10, kk) - 1)'), ('x', 'nn / pow(10, kk)')],
      fraction('Zapisz liczbę @{x|dec} w postaci ułamka zwykłego nieskracalnego.', 'numer(x)', 'denom(x)',
               [('idea', 'Liczbę po przecinku zapisujemy w liczniku, a w mianowniku piszemy 1 i tyle zer, ile jest miejsc po przecinku. Potem skracamy.'),
                ('compute', '@{x|dec} = $\\frac{@{nn}}{@{pow(10, kk)}}$'),
                ('conclude', 'Po skróceniu: $\\frac{@{numer(x)}}{@{denom(x)}}$')],
               errors=[('not_simplified', Rat('nn', 'pow(10, kk)', False), 'Skróć jeszcze ten ułamek.', 'numer(x) != nn')]),
      constraints=['nn % 10 != 0'], selfCheck=['x == nn / pow(10, kk)'], min_distinct=30, area=A1, prereq=['n46-dec-from-fraction', 'n46-frac-simplify'])

skill('n46-dec-to-mixed', S, 'Ułamek dziesiętny na liczbę mieszaną', ['IV-VI.1.22'],
      [lvl('Dziesiąte i setne', k=2)],
      [('w', 'randint(1, 9)'), ('kk', 'randint(1, k)'), ('nn', 'randint(1, pow(10, kk) - 1)'), ('f', 'nn / pow(10, kk)'), ('x', 'w + f')],
      task('mixed-number-input', 'Zapisz liczbę @{x|dec} w postaci liczby mieszanej z ułamkiem nieskracalnym.', Mixed('w', 'numer(f)', 'denom(f)'),
           [('idea', 'Część całkowita zostaje, a część po przecinku zamieniamy na ułamek i skracamy.'),
            ('conclude', '@{x|dec} = $@{w}\\frac{@{numer(f)}}{@{denom(f)}}$')]),
      constraints=['nn % 10 != 0'], min_distinct=30, area=A1, prereq=['n46-dec-to-fraction', 'n46-frac-to-mixed'])

skill('n46-dec-compare', S, 'Porównywanie ułamków dziesiętnych', ['IV-VI.1.26'],
      [lvl('Tyle samo miejsc po przecinku', kind=0), lvl('Różna liczba miejsc', kind=1), lvl('Także zapisy równe', kind=2)],
      [('ka', 'randint(1, 3)'), ('kb', 'ka if kind == 0 else randint(1, 3)'),
       ('na', 'randint(1, pow(10, ka + 1) - 1)'), ('x', 'na / pow(10, ka)'),
       ('eq', 'randint(0, 3) == 0 if kind == 2 else False'),
       ('near', 'randint(0, 1) == 1'),
       ('y', 'x if eq else ((x + randint(-9, 9) / pow(10, kb)) if near and kind > 0 else randint(1, pow(10, kb + 1) - 1) / pow(10, kb))'),
       ('ky', 'max(kb, ka) if eq else kb')],
      choice_text('Porównaj liczby @{x|dec} i @{y|dec:ky}. Który znak należy wstawić między nie?',
                  [(r'$<$', 'x < y'), (r'$=$', 'x == y'), (r'$>$', 'x > y')], None,
                  [('idea', 'Porównuj cyfry od lewej: najpierw część całkowita, potem dziesiąte, setne… Dopisanie zer na końcu nie zmienia wartości.'),
                   ('conclude', '@{x|dec:3} @{(\'<\' if x < y else (\'=\' if x == y else \'>\'))} @{y|dec:3}')], fixed_order=True),
      constraints=['eq or x != y', 'na % 10 != 0', 'y > 0'], min_distinct=30, area=A1, prereq=['n46-dec-place-value'])

skill('n46-dec-order', S, 'Ustaw ułamki dziesiętne w kolejności', ['IV-VI.1.26'],
      [lvl('Jedno miejsce po przecinku', k=1), lvl('Do trzech miejsc po przecinku', k=3)],
      [('base', 'randint(1, 9)'), ('ns', 'sample(1, pow(10, k) * 2 - 1, 5)'), ('xs', '[base + ns[0] / pow(10, k), base + ns[1] / pow(10, k), base + ns[2] / pow(10, k), base + ns[3] / pow(10, k), base + ns[4] / pow(10, k)]'),
       ('desc', 'randint(0, 1) == 1')],
      order("@{('Ułóż liczby od największej do najmniejszej.' if desc else 'Ułóż liczby od najmniejszej do największej.')}", 'xs', 5,
            [('idea', 'Porównuj cyfry od lewej: najpierw część całkowita, potem dziesiąte, setne, tysięczne.'),
             ('conclude', 'Kolejność: @{(reverse(sorted(xs)) if desc else sorted(xs))|list:semi}')], fmt='dec', descending='desc'),
      min_distinct=30, area=A1, prereq=['n46-dec-compare'])

skill('n46-dec-vs-fraction', S, 'Ułamek zwykły czy dziesiętny – który większy?', ['IV-VI.1.26'],
      [lvl('Ułamki o mianownikach 2, 4, 5, 10', ds='[2, 4, 5, 10]'), lvl('Mianowniki 8, 20, 25', ds='[8, 20, 25, 4, 5]')],
      [('b', 'choice(ds)'), ('a', 'randint(1, b - 1)'), ('x', 'a / b'), ('kk', 'randint(1, 2)'), ('y', 'randint(1, pow(10, kk) - 1) / pow(10, kk)')],
      choice_text('Porównaj liczby $\\frac{@{a}}{@{b}}$ i @{y|dec}. Który znak należy wstawić między nie?',
                  [(r'$<$', 'x < y'), (r'$=$', 'x == y'), (r'$>$', 'x > y')], None,
                  [('idea', 'Zamień ułamek zwykły na dziesiętny (albo odwrotnie) i porównaj.'), ('compute', '$\\frac{@{a}}{@{b}} = @{x|dec}$')], fixed_order=True),
      min_distinct=30, area=A1, prereq=['n46-dec-compare', 'n46-dec-from-fraction'])

skill('n46-dec-number-line', S, 'Ułamek dziesiętny na osi liczbowej', ['IV-VI.1.21'],
      [lvl('Co 0,1', t='1 / 10'), lvl('Co 0,01', t='1 / 100'), lvl('Co 0,001', t='1 / 1000')],
      [('lo0', 'randint(0, 9)'), ('lo', 'lo0 * 10 * t'), ('hi', 'lo + 10 * t'), ('j', 'randint(1, 9)'), ('p', 'lo + j * t')],
      decimal('Jaką liczbę oznacza punkt A na osi liczbowej?', 'p',
              [('idea', 'Jeden odcinek osi to @{t|dec}. Od @{lo|dec} przesuwamy się o @{j} takich odcinków.'), ('compute', '@{lo|dec} + @{j} · @{t|dec} = @{p|dec}')],
              media=[{'type': 'figure', 'kind': 'number-line', 'essential': True, 'alt': 'Oś liczbowa od @{lo|dec} do @{hi|dec} z dziesięcioma równymi odcinkami i punktem A.',
                      'params': {'min': E('lo'), 'max': E('hi'), 'tick': E('t'), 'labelEvery': 5, 'points': [{'label': 'A', 'at': E('p')}]}}]),
      selfCheck=['p > lo', 'p < hi'], min_distinct=9, area=A1, prereq=['n46-dec-place-value'])

skill('n46-dec-round', S, 'Zaokrąglanie ułamków dziesiętnych', ['IV-VI.1.25'],
      [lvl('Do jedności', pl=0), lvl('Do części dziesiątych', pl=1), lvl('Do części setnych', pl=2)],
      [('kx', 'pl + randint(1, 2)'), ('nn', 'randint(pow(10, kx), pow(10, kx + 2) - 1)'), ('x', 'nn / pow(10, kx)'),
       ('pn', "['jedności', 'części dziesiątych', 'części setnych'][pl]"), ('r', 'round(x, pl)')],
      decimal('Zaokrąglij liczbę @{x|dec:kx} do @{pn}.', 'r',
              [('idea', 'Patrzymy na cyfrę po miejscu zaokrąglania: 0–4 – zostawiamy, 5–9 – zwiększamy o 1.'), ('conclude', '@{x|dec:kx} ≈ @{r|dec:pl}')],
              errors=[('truncate', Dec('floor(x * pow(10, pl)) / pow(10, pl)'), 'Przy cyfrze 5 lub większej zaokrąglamy w górę.', 'floor(x * pow(10, pl)) / pow(10, pl) != r')]),
      constraints=['(x * pow(10, pl)) != floor(x * pow(10, pl))', 'nn % 10 != 0'], selfCheck=['abs(r - x) * 2 <= 1 / pow(10, pl)'], min_distinct=40, area=A1, prereq=['n46-dec-place-value'])

# ============================================================================ działania (1.28)
skill('n46-dec-add', S, 'Dodawanie ułamków dziesiętnych', ['IV-VI.1.28.a'],
      [lvl('Dziesiąte', max_places=1, hi=99), lvl('Do setnych', max_places=2, hi=999), lvl('Do tysięcznych', max_places=3, hi=9999)],
      [('da', 'randint(1, max_places)'), ('db', 'randint(1, max_places)'), ('x', 'randint(1, hi) / pow(10, da)'), ('y', 'randint(1, hi) / pow(10, db)')],
      decimal('Oblicz: $@{x|dec} + @{y|dec}$', 'x + y',
              [('idea', 'Zapisujemy liczby jedna pod drugą tak, by przecinek był pod przecinkiem. Brakujące miejsca uzupełniamy zerami.'),
               ('compute', '@{x|dec} + @{y|dec} = @{(x + y)|dec}')],
              errors=[('misaligned', Dec('(x * pow(10, da) + y * pow(10, db)) / pow(10, max(da, db))'),
                       'Przecinek pod przecinkiem! Cyfry o tej samej wartości (dziesiąte, setne…) muszą stać w jednej kolumnie.', 'da != db')]),
      constraints=['x != y', 'x + y >= 1'], selfCheck=['x + y > x', 'denom(x + y) in divisors(1000)'], min_distinct=40, area=A1, prereq=['n46-dec-place-value', 'n46-add-written'])

skill('n46-dec-sub', S, 'Odejmowanie ułamków dziesiętnych', ['IV-VI.1.28.a'],
      [lvl('Dziesiąte', max_places=1, hi=99), lvl('Do setnych', max_places=2, hi=999), lvl('Do tysięcznych', max_places=3, hi=9999)],
      [('da', 'randint(1, max_places)'), ('db', 'randint(1, max_places)'), ('x', 'randint(10, hi) / pow(10, da)'), ('y', 'randint(1, hi) / pow(10, db)')],
      decimal('Oblicz: $@{x|dec} - @{y|dec}$', 'x - y',
              [('idea', 'Zapisujemy liczby jedna pod drugą: przecinek pod przecinkiem. Brakujące miejsca uzupełniamy zerami.'),
               ('compute', '@{x|dec} − @{y|dec} = @{(x - y)|dec}')],
              errors=[('misaligned', Dec('abs(x * pow(10, da) - y * pow(10, db)) / pow(10, max(da, db))'),
                       'Przecinek pod przecinkiem! Cyfry o tej samej wartości muszą stać w jednej kolumnie.', 'da != db and x * pow(10, da) > y * pow(10, db)')]),
      constraints=['x > y'], selfCheck=['x - y + y == x'], min_distinct=40, area=A1, prereq=['n46-dec-add', 'n46-sub-written'])

skill('n46-dec-mul', S, 'Mnożenie ułamków dziesiętnych', ['IV-VI.1.28.a'],
      [lvl('Ułamek razy liczba naturalna', ka=1, kb=0), lvl('Dziesiąte razy dziesiąte', ka=1, kb=1), lvl('Setne razy dziesiąte', ka=2, kb=1), lvl('Do trzech miejsc po przecinku', ka=3, kb=1)],
      [('na', 'randint(11, pow(10, ka + 1) - 1)'), ('x', 'na / pow(10, ka)'),
       ('nb', 'randint(2, 9) if kb == 0 else randint(2, 19)'), ('y', 'nb / pow(10, kb)'), ('r', 'x * y')],
      decimal('Oblicz: $@{x|dec} \\cdot @{y|dec}$', 'r',
              [('idea', 'Mnożymy tak, jakby przecinków nie było, a w wyniku zostawiamy tyle miejsc po przecinku, ile mają razem oba czynniki.'),
               ('compute', '@{na} · @{nb} = @{na * nb}; miejsc po przecinku: @{ka + kb}; więc @{r|dec}')],
              errors=[('comma_shift', Dec('r * 10'), 'Policz miejsca po przecinku w obu czynnikach razem – tyle ma wynik.'),
                      ('comma_shift_down', Dec('r / 10'), 'Policz miejsca po przecinku w obu czynnikach razem – tyle ma wynik.')]),
      constraints=['na % 10 != 0', 'nb % 10 != 0 or kb == 0'], selfCheck=['denom(r) in divisors(10000)'], min_distinct=40, area=A1, prereq=['n46-mul', 'n46-dec-add'])

skill('n46-dec-shift', S, 'Mnożenie i dzielenie przez 10, 100, 1000', ['IV-VI.1.28'],
      [lvl('Mnożenie', mode=0), lvl('Dzielenie', mode=1), lvl('Mnożenie lub dzielenie', mode=2)],
      [('k', 'randint(1, 3)'), ('p', 'pow(10, k)'), ('md', 'randint(0, 1) if mode == 2 else mode'), ('places', 'randint(1, 3)'),
       ('x', 'randint(11, 9999) / pow(10, places)'), ('r', 'x * p if md == 0 else x / p')],
      decimal("Oblicz: $@{x|dec} @{('\\\\cdot' if md == 0 else ':')} @{p|int}$", 'r',
              [('idea', "@{('Mnożenie przez ' + str(p) + ' przesuwa przecinek o ' + pln(k, ['miejsce', 'miejsca', 'miejsc']) + ' w prawo.' if md == 0 else 'Dzielenie przez ' + str(p) + ' przesuwa przecinek o ' + pln(k, ['miejsce', 'miejsca', 'miejsc']) + ' w lewo.')}"),
               ('conclude', '@{r|dec}')],
              errors=[('wrong_direction', Dec('x / p if md == 0 else x * p'), 'Mnożenie przesuwa przecinek w prawo, a dzielenie – w lewo.')]),
      constraints=['denom(x) != 1'], min_distinct=40, area=A1, prereq=['n46-dec-place-value'])

skill('n46-dec-div-nat', S, 'Dzielenie ułamka dziesiętnego przez liczbę naturalną', ['IV-VI.1.28.b'],
      [lvl('Dzielnik jednocyfrowy', blo=2, bhi=9), lvl('Dzielnik dwucyfrowy', blo=11, bhi=99), lvl('Dzielnik trzycyfrowy', blo=101, bhi=300)],
      [('b', 'randint(blo, bhi)'), ('kq', 'randint(1, 2)'), ('qn', 'randint(2, 99)'), ('q', 'qn / pow(10, kq)'), ('x', 'q * b')],
      decimal('Oblicz: $@{x|dec} : @{b}$', 'q',
              [('idea', 'Dzielimy jak liczby naturalne, a przecinek w wyniku stawiamy dokładnie nad przecinkiem dzielnej.'), ('compute', '@{q|dec} · @{b} = @{x|dec}')],
              errors=[('comma_shift', Dec('q * 10'), 'Sprawdź mnożeniem: wynik razy dzielnik powinien dać dzielną.'), ('comma_shift_down', Dec('q / 10'), 'Sprawdź mnożeniem: wynik razy dzielnik powinien dać dzielną.')]),
      constraints=['qn % 10 != 0', 'denom(x) in divisors(1000)'], selfCheck=['q * b == x'], min_distinct=40, area=A1, prereq=['n46-dec-mul', 'n46-div'])

skill('n46-dec-div-dec', S, 'Dzielenie przez ułamek dziesiętny', ['IV-VI.1.28.b'],
      [lvl('Dzielnik z jednym miejscem po przecinku', ky=1), lvl('Dzielnik z dwoma miejscami po przecinku', ky=2)],
      [('yn', 'randint(2, 9)'), ('y', 'yn / pow(10, ky)'), ('qn', 'randint(2, 60)'), ('q', 'qn'), ('x', 'q * y')],
      decimal('Oblicz: $@{x|dec} : @{y|dec}$', 'q',
              [('idea', 'Przesuwamy przecinki w dzielnej i dzielniku o tyle samo miejsc w prawo, aż dzielnik będzie liczbą naturalną.'),
               ('compute', '@{x * pow(10, ky)|dec} : @{yn} = @{q}')],
              errors=[('comma_shift', Dec('q / pow(10, ky)'), 'Przesunięcie przecinków w obu liczbach nie zmienia wyniku dzielenia.')]),
      constraints=['yn % 10 != 0'], selfCheck=['q * y == x'], min_distinct=40, area=A1, prereq=['n46-dec-div-nat'])

skill('n46-dec-infinite', S, 'Rozwinięcie dziesiętne nieskończone', ['IV-VI.1.24'],
      [lvl('Wybierz poprawny zapis')],
      [('b', 'choice([3, 6, 9, 11])'), ('a', 'randint(1, b - 1)'), ('x', 'a / b'),
       ('good', 'expand(x, 4)'), ('w1', 'expand(x, 2)'), ('w2', 'expand(round(x, 1), 1)'), ('w3', 'expand(x + 1 / 100, 4)')],
      choice_text('Który zapis jest początkiem rozwinięcia dziesiętnego ułamka $\\frac{@{a}}{@{b}}$?',
                  [('@{good}', 'true'), ('@{w1}', 'false'), ('@{w2}', 'false'), ('@{w3}', 'false')], None,
                  [('idea', 'Dzielimy licznik przez mianownik. Reszty się powtarzają, więc cyfry wracają – dlatego dopisujemy wielokropek.'),
                   ('conclude', '$\\frac{@{a}}{@{b}}$ = @{good}')]),
      constraints=['gcd(a, b) == 1', 'len(uniq([good, w1, w2, w3])) == 4', 'denom(x) in [3, 6, 9, 11, 18, 33]'], min_distinct=15, area=A1, prereq=['n46-dec-from-fraction'])

skill('n46-dec-infinite-round', S, 'Zaokrąglanie rozwinięcia nieskończonego', ['IV-VI.1.24', 'IV-VI.1.25'],
      [lvl('Do części dziesiątych', pl=1), lvl('Do części setnych', pl=2)],
      [('b', 'choice([3, 6, 7, 9, 11, 12])'), ('a', 'randint(1, b - 1)'), ('x', 'a / b'),
       ('pn', "['jedności', 'części dziesiątych', 'części setnych'][pl]"), ('r', 'round(x, pl)')],
      decimal('Zapisz ułamek $\\frac{@{a}}{@{b}}$ w postaci dziesiętnej, zaokrąglając do @{pn}.', 'r',
              [('idea', 'Dzielimy licznik przez mianownik z jednym miejscem więcej niż potrzeba i zaokrąglamy.'), ('conclude', '$\\frac{@{a}}{@{b}} \\approx @{r|dec:pl}$')]),
      constraints=['gcd(a, b) == 1', 'denom(x) != 1', 'denom(x) not in divisors(1000)'], selfCheck=['abs(r - x) * 2 <= 1 / pow(10, pl)'], min_distinct=20, area=A1, prereq=['n46-dec-infinite', 'n46-dec-round'])

skill('n46-dec-power', S, 'Potęgi ułamków dziesiętnych', ['IV-VI.1.29'],
      [lvl('Kwadraty', e=2, bhi=19), lvl('Sześciany', e=3, bhi=19)],
      [('bn', 'randint(2, bhi)'), ('b', 'bn / 10'), ('v', 'pow(b, e)')],
      decimal('Oblicz: $@{b|dec}^{@{e}}$', 'v',
              [('idea', 'Mnożymy podstawę przez siebie @{e} razy. Liczbę miejsc po przecinku w wyniku liczymy tak jak przy mnożeniu.'),
               ('compute', "@{b|dec}@{('²' if e == 2 else '³')} = @{v|dec}")],
              errors=[('multiply_exponent', Dec('b * e'), 'Wykładnik mówi, ile razy mnożymy podstawę przez siebie – to nie jest mnożenie przez wykładnik.')]),
      constraints=['bn % 10 != 0'], min_distinct=15, area=A1, prereq=['n46-dec-mul', 'n46-power-calc'])

skill('n46-frac-power', S, 'Potęgi ułamków zwykłych', ['IV-VI.1.29'],
      [lvl('Kwadraty', e=2), lvl('Sześciany', e=3)],
      [('b', 'randint(2, 6)'), ('a', 'randint(1, b - 1)'), ('x', 'a / b'), ('v', 'pow(x, e)')],
      fraction('Oblicz: $\\left(\\frac{@{a}}{@{b}}\\right)^{@{e}}$', 'numer(v)', 'denom(v)',
               [('idea', 'Potęgujemy osobno licznik i mianownik.'), ('conclude', '$\\frac{@{pow(a, e)}}{@{pow(b, e)}}$')],
               errors=[('only_denominator', Rat('a', 'pow(b, e)', False), 'Do potęgi podnosimy zarówno licznik, jak i mianownik.', 'a != 1')]),
      constraints=['gcd(a, b) == 1'], min_distinct=10, area=A1, prereq=['n46-frac-mul', 'n46-power-calc'])

skill('n46-rational-mix', S, 'Działania na ułamkach zwykłych i dziesiętnych', ['IV-VI.1.32'],
      [lvl('Dodawanie i odejmowanie', op=0), lvl('Mnożenie', op=1)],
      [('b', 'choice([2, 4, 5, 10, 20, 25])'), ('a', 'randint(1, b - 1)'), ('x', 'a / b'), ('ky', 'randint(1, 2)'), ('y', 'randint(1, pow(10, ky + 1) - 1) / pow(10, ky)'),
       ('plus', 'randint(0, 1) == 1'), ('r', 'x + y if op == 0 and plus else (x - y if op == 0 else x * y)'),
       ('sg', "'+' if plus else '-'"), ('sgn', "'\\\\cdot' if op == 1 else sg")],
      decimal('Oblicz: $\\frac{@{a}}{@{b}} @{sgn} @{y|dec}$', 'r',
              [('idea', 'Zamień ułamek zwykły na dziesiętny (albo odwrotnie) i licz w jednej postaci.'), ('compute', '$\\frac{@{a}}{@{b}} = @{x|dec}$, więc @{r|dec}')]),
      constraints=['op == 1 or plus or x > y', 'y != x', 'denom(r) in divisors(10000)', 'r > 0', 'gcd(a, b) == 1'], min_distinct=30, area=A1, prereq=['n46-dec-from-fraction', 'n46-dec-mul'])

# ============================================================================ ścieżka
un = Unit(S, 'n46-u9', 'Liczby całkowite', 'Liczby ujemne, ich porównywanie i rachunki na osi liczbowej.', 'negative', area=A1)
un.learn('n46-int-context').learn('n46-int-compare').learn('n46-int-order').learn('n46-int-distance')
un.review('Powtórka: liczby ujemne', ['n46-int-context', 'n46-int-compare', 'n46-int-order', 'n46-int-distance'])
un.learn('n46-int-addsub').learn('n46-int-muldiv')
un.checkpoint(['n46-int-context', 'n46-int-compare', 'n46-int-order', 'n46-int-distance', 'n46-int-addsub'])

un = Unit(S, 'n46-u10', 'Ułamki zwykłe – pojęcie', 'Część całości, skracanie, rozszerzanie, liczby mieszane i oś liczbowa.', 'pie', area=A1)
un.learn('n46-frac-part-figure').learn('n46-frac-part-set').learn('n46-frac-quotient')
un.learn('n46-frac-simplify').learn('n46-frac-extend').learn('n46-lcd')
un.review('Powtórka: pojęcie ułamka', ['n46-frac-part-figure', 'n46-frac-part-set', 'n46-frac-simplify', 'n46-frac-extend'])
un.learn('n46-frac-to-mixed').learn('n46-mixed-to-frac').learn('n46-frac-number-line')
un.checkpoint(['n46-frac-part-set', 'n46-frac-simplify', 'n46-frac-extend', 'n46-lcd', 'n46-frac-to-mixed', 'n46-mixed-to-frac', 'n46-frac-number-line'])

un = Unit(S, 'n46-u11', 'Porównywanie ułamków', 'Który ułamek jest większy i o ile?', 'scale', area=A1)
un.learn('n46-frac-compare').learn('n46-frac-order').learn('n46-frac-diff')
un.checkpoint(['n46-frac-compare', 'n46-frac-order', 'n46-frac-diff'])

un = Unit(S, 'n46-u12', 'Działania na ułamkach zwykłych', 'Dodajemy, odejmujemy, mnożymy i dzielimy ułamki i liczby mieszane.', 'fractions', area=A1)
un.learn('n46-frac-addsub').learn('n46-frac-addsub-mixed').review('Powtórka: dodawanie i odejmowanie', ['n46-frac-addsub', 'n46-frac-addsub-mixed'])
un.learn('n46-frac-mul').learn('n46-frac-div').learn('n46-frac-of-number').learn('n46-frac-of-quantity')
un.checkpoint(['n46-frac-addsub', 'n46-frac-addsub-mixed', 'n46-frac-mul', 'n46-frac-div', 'n46-frac-of-number', 'n46-frac-of-quantity'])

un = Unit(S, 'n46-u13', 'Ułamki dziesiętne – zapis', 'Miejsca po przecinku, zamiana na ułamki zwykłe, porównywanie i zaokrąglanie.', 'decimal', area=A1)
un.learn('n46-dec-place-value').learn('n46-dec-from-fraction').learn('n46-dec-to-fraction').learn('n46-dec-to-mixed')
un.review('Powtórka: zapis dziesiętny', ['n46-dec-place-value', 'n46-dec-from-fraction', 'n46-dec-to-fraction'])
un.learn('n46-dec-compare').learn('n46-dec-order').learn('n46-dec-vs-fraction').learn('n46-dec-number-line').learn('n46-dec-round')
un.checkpoint(['n46-dec-place-value', 'n46-dec-from-fraction', 'n46-dec-to-fraction', 'n46-dec-compare', 'n46-dec-order', 'n46-dec-round'])

un = Unit(S, 'n46-u14', 'Działania na ułamkach dziesiętnych', 'Dodajemy, odejmujemy, mnożymy i dzielimy ułamki dziesiętne.', 'calc-decimal', area=A1)
un.learn('n46-dec-add').learn('n46-dec-sub').learn('n46-dec-mul').learn('n46-dec-shift')
un.review('Powtórka: dodawanie, odejmowanie, mnożenie', ['n46-dec-add', 'n46-dec-sub', 'n46-dec-mul', 'n46-dec-shift'])
un.learn('n46-dec-div-nat').learn('n46-dec-div-dec').learn('n46-dec-infinite').learn('n46-dec-infinite-round')
un.learn('n46-dec-power').learn('n46-frac-power').learn('n46-rational-mix')
un.checkpoint(['n46-dec-add', 'n46-dec-sub', 'n46-dec-mul', 'n46-dec-div-nat', 'n46-dec-div-dec', 'n46-dec-infinite-round', 'n46-rational-mix'])
