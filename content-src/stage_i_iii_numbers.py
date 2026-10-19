"""Stage I-III (edukacja wczesnoszkolna), area 1 (Liczby).  Objectives: I-III.1.a - 1.p.
Levels are number ranges (to 20, to 100, to 1000, to 10 000), not school years: the regulation does not assign them."""
from dsl import *

S = 'I-III'
A1 = 'I-III.1'
NOTE = 'I-III.1'

# ============================================================================ zapis, porównywanie, kolejność (1.a, 1.b, 1.c)
skill('ew-write-number', S, 'Zapisz liczbę cyframi', ['I-III.1.a'],
      [lvl('Do 20', lo=11, hi=20), lvl('Do 100', lo=21, hi=99), lvl('Do 1000', lo=100, hi=999), lvl('Do 10 000', lo=1000, hi=9999)],
      [('n', 'randint(lo, hi)')],
      number('Zapisz cyframi liczbę: „@{words(n)}”.', 'n',
             [('idea', 'Czytamy liczbę po kolei: najpierw tysiące, potem setki, dziesiątki i jedności.'), ('conclude', 'To liczba @{n|int}.')]),
      min_distinct=9, area=A1,
      intro='Liczby zapisujemy cyframi. Cyfra stoi na swoim miejscu: jedności, dziesiątki, setki, tysiące. Zero oznacza, że w danym rzędzie nic nie ma.')

skill('ew-compare', S, 'Która liczba jest większa?', ['I-III.1.a', 'I-III.1.m'],
      [lvl('Do 20', hi=20), lvl('Do 100', hi=100), lvl('Do 1000', hi=1000), lvl('Do 10 000', hi=10000)],
      [('a', 'randint(1, hi)'), ('b', 'randint(max(1, a - hi // 5), min(hi, a + hi // 5))')],
      choice_text('Porównaj liczby @{a|int} i @{b|int}. Który znak należy wstawić między nie?',
                  [(r'$<$', 'a < b'), (r'$=$', 'a == b'), (r'$>$', 'a > b')], None,
                  [('idea', 'Najpierw patrzymy, która liczba ma więcej cyfr. Jeśli tyle samo – porównujemy cyfry od lewej.'), ('conclude', '@{a|int} @{(\'<\' if a < b else \'>\')} @{b|int}')], fixed_order=True),
      constraints=['a != b'], min_distinct=12, area=A1)

skill('ew-order', S, 'Ustaw liczby w kolejności', ['I-III.1.a'],
      [lvl('Do 20', hi=20, sp=14), lvl('Do 100', hi=100, sp=60), lvl('Do 1000', hi=1000, sp=500), lvl('Do 10 000', hi=10000, sp=4000)],
      [('lo', 'randint(1, hi - sp)'), ('xs', 'sample(lo, lo + sp, 4)'), ('desc', 'randint(0, 1) == 1')],
      order("@{('Ułóż liczby od największej do najmniejszej.' if desc else 'Ułóż liczby od najmniejszej do największej.')}", 'xs', 4,
            [('idea', 'Porównuj liczby po kolei. Najmniejsza ma najmniej dziesiątek (setek, tysięcy).'), ('conclude', 'Kolejność: @{(reverse(sorted(xs)) if desc else sorted(xs))|list:semi}')],
            fmt='int', descending='desc'),
      min_distinct=20, area=A1, prereq=['ew-compare'])

skill('ew-place-value', S, 'Rzędy liczby', ['I-III.1.b'],
      [lvl('Dziesiątki i jedności', k=2), lvl('Setki', k=3), lvl('Tysiące', k=4)],
      [('n', 'randint(pow(10, k - 1) + 1, pow(10, k) - 1)'), ('mode', 'randint(0, 1)'), ('p', 'randint(0, k - 1)'),
       ('pn', "['jedności', 'dziesiątek', 'setek', 'tysięcy'][p]"), ('d', '(n // pow(10, p)) % 10'), ('ds', 'digits(n)'),
       ('forms', "[['tysiąc', 'tysiące', 'tysięcy'], ['setka', 'setki', 'setek'], ['dziesiątka', 'dziesiątki', 'dziesiątek'], ['jedność', 'jedności', 'jedności']]"),
       ('compose', "'Zapisz liczbę, w której jest: ' + pln(ds[0], forms[4 - k]) + ', ' + pln(ds[1], forms[5 - k]) + (', ' + pln(ds[2], forms[6 - k]) if k > 2 else '') + (' i ' + pln(ds[3], forms[7 - k]) if k > 3 else '') + '.'")],
      number("@{('Jaka cyfra stoi na miejscu ' + pn + ' w liczbie ' + fmt(n) + '?') if mode == 0 else compose}",
             'd if mode == 0 else n',
             [('idea', 'Miejsca w liczbie od prawej: jedności, dziesiątki, setki, tysiące.'), ('conclude', "@{(str(d) if mode == 0 else fmt(n))}")]),
      min_distinct=30, area=A1, prereq=['ew-write-number'])

skill('ew-odd-even', S, 'Parzysta czy nieparzysta?', ['I-III.1.c'],
      [lvl('Do 20', hi=20), lvl('Do 100', hi=100), lvl('Do 1000', hi=1000), lvl('Do 10 000', hi=10000)],
      [('n', 'randint(2, hi)'), ('even', 'n % 2 == 0'), ('ask', 'randint(0, 1)')],
      choice_text("@{('Czy liczba ' + fmt(n) + ' jest parzysta?' if ask == 0 else 'Czy liczba ' + fmt(n) + ' jest nieparzysta?')}",
                  [('Tak', "even if ask == 0 else not even"), ('Nie', "not even if ask == 0 else even")], None,
                  [('idea', 'Liczba parzysta kończy się cyfrą 0, 2, 4, 6 lub 8. Nieparzysta – 1, 3, 5, 7 lub 9.'), ('conclude', 'Ostatnia cyfra liczby @{n|int} to @{n % 10}.')], fixed_order=True),
      min_distinct=10, area=A1,
      intro='Liczby parzyste można podzielić na dwie równe części lub połączyć w pary (2, 4, 6…). Liczby nieparzyste zawsze jedna zostaje bez pary (1, 3, 5…).')

# ============================================================================ liczenie, oś liczbowa (1.d, 1.e)
skill('ew-skip-count', S, 'Liczenie co 2, co 5, co 10…', ['I-III.1.d'],
      [lvl('W przód do 100', mode=0), lvl('W tył do 100', mode=1), lvl('Przez zero w stronę liczb ujemnych', md=12, mode=2)],
      [('st', 'choice([1, 2, 3, 4, 5, 10])'), ('s0', 'randint(0, 9) * st if mode == 0 else (randint(10, 20) * st if mode == 1 else randint(1, 4) * st)'),
       ('d', 'st if mode == 0 else -st'), ('seq', '[s0, s0 + d, s0 + 2 * d, s0 + 3 * d, s0 + 4 * d]'), ('shown', 'take(seq, 3)'), ('nxt', 'seq[3]')],
      number('Dopisz brakującą liczbę: @{shown|list}, ___', 'nxt',
             [('idea', "@{('Liczymy co ' + str(st) + ' w przód.' if mode == 0 else 'Liczymy co ' + str(st) + ' w tył.')}"), ('conclude', 'Następna liczba: @{nxt}.')]),
      constraints=['mode != 0 or seq[3] <= 100', 'mode != 1 or seq[3] >= 0', 'mode != 2 or seq[3] < 0'], min_distinct=15, area=A1)

skill('ew-number-line-diff', S, 'Skoki po osi liczbowej', ['I-III.1.e'],
      [lvl('Do 20', hi=20), lvl('Do 100', hi=100), lvl('Do 1000', hi=1000)],
      [('a', 'randint(1, hi // 2)'), ('d', 'randint(1, hi // 3)'), ('b', 'a + d'), ('mode', 'randint(0, 2)'),
       ('txt', "('O ile liczba ' + fmt(b) + ' jest większa od liczby ' + fmt(a) + '?') if mode == 0 else "
               "(('O ile liczba ' + fmt(a) + ' jest mniejsza od liczby ' + fmt(b) + '?') if mode == 1 else "
               "('Która liczba jest o ' + fmt(d) + ' większa od ' + fmt(a) + '?'))"),
       ('ans', 'd if mode < 2 else b')],
      number('@{txt}', 'ans', [('idea', 'Na osi liczbowej policz, o ile skoków trzeba przesunąć się z jednej liczby do drugiej.'), ('compute', '@{a|int} → @{b|int}: skok o @{d|int}.')]),
      min_distinct=30, area=A1)

skill('ew-number-line-read', S, 'Liczba na osi liczbowej', ['I-III.1.e'],
      [lvl('Od 0 do 20', t=1, n=20), lvl('Od 0 do 100', t=10, n=10), lvl('Od 0 do 1000', t=100, n=10)],
      [('hi', 't * n'), ('p', 'randint(1, n - 1) * t')],
      number('Jaką liczbę oznacza punkt A na osi liczbowej?', 'p',
             [('idea', 'Policz, ile wynosi jedna kreska. Potem policz kreski od zera do punktu A.'), ('compute', '@{p // t} · @{t} = @{p}')],
             media=[{'type': 'figure', 'kind': 'number-line', 'essential': True, 'alt': 'Oś liczbowa od 0 do @{hi} z zaznaczonym punktem A.',
                     'params': {'min': 0, 'max': E('hi'), 'tick': E('t'), 'labelEvery': 5, 'points': [{'label': 'A', 'at': E('p')}]}}]),
      min_distinct=9, area=A1)

# ============================================================================ działania (1.f - 1.i)
skill('ew-add', S, 'Dodawanie', ['I-III.1.f'],
      [lvl('Do 10', alo=1, ahi=9, blo=1, bhi=9, cap=10), lvl('Do 20', alo=2, ahi=19, blo=2, bhi=9, cap=20), lvl('Dwucyfrowa i jednocyfrowa', alo=11, ahi=95, blo=2, bhi=9, cap=100),
       lvl('Dwie liczby dwucyfrowe', alo=11, ahi=89, blo=11, bhi=89, cap=100), lvl('Liczby trzycyfrowe', alo=101, ahi=899, blo=11, bhi=99, cap=1000)],
      [('a', 'randint(alo, ahi)'), ('b', 'randint(blo, bhi)'), ('s', 'a + b'), ('b0', 'b - b % 10')],
      number('Oblicz: @{a} + @{b}', 's',
             [('idea', '@{(\'Dodajemy dziesiątki, potem jedności.\' if b >= 10 else \'Dodajemy po kolei.\')}'),
              ('compute', "@{(str(a) + ' + ' + str(b0) + ' = ' + str(a + b0) + ', a potem + ' + str(b % 10) + ' = ' + str(s) if b >= 10 and b % 10 != 0 else str(a) + ' + ' + str(b) + ' = ' + str(s))}")],
             errors=[('off_by_one', Int('s + 1'), 'Sprawdź jeszcze raz – możesz policzyć na palcach lub na osi liczbowej.'), ('off_by_ten', Int('s - 10'), 'Pamiętaj o przejściu przez dziesiątkę.', 's > 10')]),
      constraints=['s <= cap', 'b % 10 != 0 or b < 10'], min_distinct=30, area=A1,
      intro='Dodawanie to łączenie. Możemy dodawać po kolei, przechodząc przez dziesiątkę: 8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.')

skill('ew-sub', S, 'Odejmowanie', ['I-III.1.g'],
      [lvl('Do 10', alo=2, ahi=10, blo=1, bhi=9), lvl('Do 20', alo=11, ahi=20, blo=2, bhi=9), lvl('Dwucyfrowa minus jednocyfrowa', alo=21, ahi=99, blo=2, bhi=9),
       lvl('Dwucyfrowa minus dwucyfrowa', alo=30, ahi=99, blo=11, bhi=29)],
      [('a', 'randint(alo, ahi)'), ('b', 'randint(blo, bhi)'), ('r', 'a - b'), ('b0', 'b - b % 10')],
      number('Oblicz: @{a} − @{b}', 'r',
             [('idea', "@{('Odejmujemy dziesiątki, potem jedności.' if b >= 10 else 'Odejmujemy po kolei, przechodząc przez dziesiątkę.')}"),
              ('compute', "@{(str(a) + ' − ' + str(b0) + ' = ' + str(a - b0) + ', a potem − ' + str(b % 10) + ' = ' + str(r) if b >= 10 and b % 10 != 0 else str(a) + ' − ' + str(b) + ' = ' + str(r))}")],
             errors=[('off_by_one', Int('r + 1'), 'Sprawdź jeszcze raz – możesz policzyć na osi liczbowej.'), ('off_by_ten', Int('r + 10'), 'Przy przejściu przez dziesiątkę pamiętaj o pożyczce.', 'a % 10 < b % 10')]),
      constraints=['r > 0', 'b % 10 != 0 or b < 10'], min_distinct=25, area=A1, prereq=['ew-add'])

skill('ew-mul-table', S, 'Tabliczka mnożenia', ['I-III.1.h'],
      [lvl('Razy 2, 5 i 10', fs='[2, 5, 10]'), lvl('Razy 3 i 4', fs='[3, 4]'), lvl('Razy 6, 7, 8, 9', fs='[6, 7, 8, 9]'), lvl('Cała tabliczka', fs='[2, 3, 4, 5, 6, 7, 8, 9, 10]')],
      [('f', 'choice(fs)'), ('m', 'randint(1, 10)'), ('sw', 'randint(0, 1) == 1')],
      number("@{('Oblicz: ' + str(m) + ' · ' + str(f) if sw else 'Oblicz: ' + str(f) + ' · ' + str(m))}", 'f * m',
             [('idea', 'Mnożenie to dodawanie takich samych liczb: @{f} · @{m} to @{m} razy po @{f}.'), ('compute', '@{f} · @{m} = @{f * m}')],
             errors=[('add_instead', Int('f + m'), 'Mnożenie to nie dodawanie. Policz @{m} razy po @{f}.', 'f + m != f * m'), ('neighbor', Int('f * m + f'), 'Wynik o jedną „grupę” za duży – sprawdź tabliczkę.')]),
      min_distinct=18, area=A1,
      intro='Mnożenie to skrócony zapis dodawania takich samych liczb: 4 · 3 = 3 + 3 + 3 + 3 = 12. Tabliczkę mnożenia warto znać na pamięć.')

skill('ew-div-table', S, 'Dzielenie w zakresie tabliczki mnożenia', ['I-III.1.h'],
      [lvl('Przez 2, 5 i 10', fs='[2, 5, 10]'), lvl('Przez 3 i 4', fs='[3, 4]'), lvl('Przez 6, 7, 8, 9', fs='[6, 7, 8, 9]'), lvl('Cała tabliczka', fs='[2, 3, 4, 5, 6, 7, 8, 9, 10]')],
      [('f', 'choice(fs)'), ('q', 'randint(1, 10)'), ('a', 'f * q')],
      number('Oblicz: @{a} : @{f}', 'q',
             [('idea', 'Pomyśl: przez jaką liczbę trzeba pomnożyć @{f}, żeby dostać @{a}?'), ('compute', '@{f} · @{q} = @{a}, więc @{a} : @{f} = @{q}')],
             errors=[('subtract', Int('a - f'), 'Dzielenie to nie odejmowanie. Szukaj w tabliczce mnożenia.', 'a - f != q')]),
      min_distinct=18, area=A1, prereq=['ew-mul-table'])

skill('ew-mul-two-digit', S, 'Mnożenie liczby dwucyfrowej', ['I-III.1.h'],
      [lvl('Razy 2 i 10', fs='[2, 10]'), lvl('Razy 3 i 5', fs='[3, 5]')],
      [('f', 'choice(fs)'), ('a', 'randint(11, 40) if f != 10 else randint(11, 99)')],
      number('Oblicz: @{a} · @{f}', 'a * f',
             [('idea', 'Rozbij liczbę na dziesiątki i jedności i pomnóż każdą część.'), ('compute', '@{a - a % 10} · @{f} = @{(a - a % 10) * f}, @{a % 10} · @{f} = @{(a % 10) * f}; razem @{a * f}')]),
      constraints=['a % 10 != 0'], min_distinct=30, area=A1, prereq=['ew-mul-table'])

skill('ew-div-two-digit', S, 'Dzielenie liczby dwucyfrowej', ['I-III.1.i'],
      [lvl('Przez 2 i 10', fs='[2, 10]'), lvl('Przez 3 i 5', fs='[3, 5]')],
      [('f', 'choice(fs)'), ('q', 'randint(2, 33) if f != 10 else randint(2, 9)'), ('a', 'f * q')],
      number('Oblicz: @{a} : @{f}', 'q',
             [('idea', 'Sprawdź mnożeniem: wynik razy @{f} ma dać @{a}.'), ('compute', '@{q} · @{f} = @{a}')]),
      constraints=['a >= 10', 'a <= 99'], min_distinct=15, area=A1, prereq=['ew-div-table'])

skill('ew-div-meaning', S, 'Podział po równo i mieszczenie', ['I-III.1.h'],
      [lvl('Do 20', hi=20), lvl('Do 50', hi=50)],
      [('f', 'randint(2, 5)'), ('q', 'randint(2, hi // f)'), ('a', 'f * q'), ('mode', 'randint(0, 1)'),
       ('it', "choice([['jabłko', 'jabłka', 'jabłek'], ['ciastko', 'ciastka', 'ciastek'], ['naklejka', 'naklejki', 'naklejek'], ['kredka', 'kredki', 'kredek']])"),
       ('bag', "choice([['torebki', 'torebek'], ['pudełka', 'pudełek'], ['koperty', 'kopert']])"),
       ('txt', "('Rozdzielono po równo ' + pln(a, it) + ' między ' + pln(f, ['dziecko', 'dzieci', 'dzieci']) + '. Ile ' + it[2] + ' dostało każde dziecko?') if mode == 0 else "
               "('Mamy ' + pln(a, it) + '. Do każdej ' + bag[0] + ' wkładamy po ' + pln(f, it) + '. Ile ' + bag[1] + ' potrzeba?')")],
      number('@{txt}', 'q',
             [('idea', "@{('To podział po równo: dzielimy wszystkie rzeczy na równe części.' if mode == 0 else 'To mieszczenie: sprawdzamy, ile razy ' + str(f) + ' mieści się w ' + str(a) + '.')}"), ('compute', '@{a} : @{f} = @{q}')]),
      min_distinct=20, area=A1, prereq=['ew-div-table'])

skill('ew-div-share-or-fit', S, 'Podział czy mieszczenie?', ['I-III.1.h'],
      [lvl('Rozpoznaj sytuację', md=20)],
      [('it', "choice([['jabłko', 'jabłka', 'jabłek'], ['cukierek', 'cukierki', 'cukierków'], ['naklejka', 'naklejki', 'naklejek'], ['ciastko', 'ciastka', 'ciastek'], ['kulka', 'kulki', 'kulek'], ['gruszka', 'gruszki', 'gruszek']])"),
       ('rc', "choice(['talerzy', 'pudełek', 'koszyków', 'misek'])"), ('pk', "choice(['woreczka', 'pudełka', 'koszyka', 'torebki'])"),
       ('q', 'randint(2, 6)'), ('k', 'randint(2, 6)'), ('tot', 'q * k'), ('kind', 'randint(0, 1)'),
       ('ctx', "('Rozłożono ' + pln(tot, it) + ' po równo do ' + str(k) + ' ' + rc + '.') if kind == 0 else ('Mamy ' + pln(tot, it) + ' i pakujemy je po ' + str(q) + ' do jednego ' + pk + '.')")],
      choice_text('@{ctx} Czy to jest dzielenie jako podział po równo, czy jako mieszczenie?',
                  [('Podział po równo', 'kind == 0'), ('Mieszczenie (ile razy mieści się)', 'kind == 1')], None,
                  [('idea', 'Podział: znamy liczbę części i szukamy, ile w każdej. Mieszczenie: znamy wielkość porcji i szukamy, ile porcji.'),
                   ('conclude', "@{('To jest podział po równo.' if kind == 0 else 'To jest mieszczenie.')}")], fixed_order=True),
      area=A1, prereq=['ew-div-meaning'])

# ============================================================================ strategie, regularności, równości (1.j, 1.k, 1.l, 1.m, 1.o)
skill('ew-strategy', S, 'Sprytne liczenie', ['I-III.1.j'],
      [lvl('Dodawanie: liczba bliska okrągłej', op=0), lvl('Odejmowanie: liczba bliska okrągłej', op=1)],
      [('x', 'randint(20, 60)'), ('y0', 'randint(2, 5) * 10'), ('dl', 'randint(1, 2)'), ('y', 'y0 - dl'),
       ('sg', "'+' if op == 0 else '−'"), ('inv', "'−' if op == 0 else '+'"),
       ('base', "str(x) + ' ' + sg + ' ' + str(y) + ' = ' + str(x) + ' ' + sg + ' ' + str(y0) + ' '"),
       ('good', "base + inv + ' ' + str(dl)"), ('w1', "base + sg + ' ' + str(dl)"), ('w2', "base + inv + ' ' + str(dl + 1)"), ('w3', "base + sg + ' ' + str(dl + 1)")],
      choice('Jak wygodnie obliczyć @{x} @{sg} @{y}? Wskaż poprawny zapis.', 'good', ['w1', 'w2', 'w3'],
             [('idea', "@{y} to prawie @{y0}: brakuje @{dl}. Policz z okrągłą liczbą, a potem popraw wynik o @{dl}."),
              ('conclude', 'Poprawny zapis: @{good}.')]),
      constraints=['op == 0 or x > y'], selfCheck=['op == 1 or (x + y == x + y0 - dl)', 'op == 0 or (x - y == x - y0 + dl)'], min_distinct=20, area=A1, prereq=['ew-add'])

