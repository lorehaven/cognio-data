"""Stage IV-VI, area 1 (Liczby): natural numbers - notation, operations, divisibility.
Objectives: IV-VI.1.1-1.15, 1.36-1.37.  Texts are Polish; the DSL is documented in docs/02-course-format.md."""
from dsl import *

S = 'IV-VI'
A1 = 'IV-VI.1'

# ============================================================================ unit 1: zapis liczb
skill('n46-write-digits', S, 'Zapisz liczbę cyframi', ['IV-VI.1.1'],
      [lvl('Do 9 999', 'IV-VI.1.1', lo=1000, hi=9999), lvl('Do 999 999', 'IV-VI.1.1', lo=10000, hi=999999),
       lvl('Do 999 999 999', 'IV-VI.1.1', lo=1000000, hi=999999999)],
      [('b', 'randint(lo, hi)'), ('n', '(b // 1000) * 1000 + (b % 1000) * randint(0, 1)')],
      number('Zapisz cyframi liczbę: „@{words(n)}”.', 'n',
             [('idea', 'Czytamy liczbę grupami: najpierw miliony, potem tysiące, na końcu setki, dziesiątki i jedności.'),
              ('conclude', 'To liczba @{n|int}.')]),
      selfCheck=['n >= 1000'], area=A1,
      intro='Duże liczby zapisujemy w grupach po trzy cyfry: jedności, tysiące, miliony. Czytamy od lewej, grupa po grupie. Jeśli czegoś brakuje (np. setek), na tym miejscu piszemy zero.',
      ideas=['Każda grupa ma setki, dziesiątki i jedności.', 'Zero zajmuje miejsce, gdy w danym rzędzie nic nie ma.'])

skill('n46-read-number', S, 'Przeczytaj liczbę', ['IV-VI.1.1'],
      [lvl('Do 9 999', lo=1000, hi=9999), lvl('Do 999 999', lo=10000, hi=999999), lvl('Do 99 999 999', lo=1000000, hi=99999999)],
      [('n', 'randint(lo, hi)'), ('p', 'randint(0, 3)')],
      choice('Jak poprawnie przeczytać liczbę @{n|int}?', 'words(n)',
             ['words(n + pow(10, p))', 'words(n - pow(10, p))', 'words(n * 10)'],
             [('idea', 'Dzielimy liczbę na grupy po trzy cyfry od prawej strony i czytamy grupa po grupie.'),
              ('conclude', 'Liczbę @{n|int} czytamy: @{words(n)}.')],
             extra_constraints=['n > pow(10, p)']),
      area=A1, prereq=['n46-write-digits'])

skill('n46-digit-place', S, 'Cyfra na danym miejscu', ['IV-VI.1.1'],
      [lvl('Liczby czterocyfrowe', k=4), lvl('Liczby sześciocyfrowe', k=6), lvl('Liczby dziewięciocyfrowe', k=9)],
      [('n', 'randint(pow(10, k - 1), pow(10, k) - 1)'), ('p', 'randint(0, k - 1)'),
       ('pn', "['jedności', 'dziesiątek', 'setek', 'tysięcy', 'dziesiątek tysięcy', 'setek tysięcy', 'milionów', 'dziesiątek milionów', 'setek milionów'][p]"),
       ('ds', 'digits(n)'), ('d', 'ds[k - 1 - p]')],
      number('Jaka cyfra stoi na miejscu @{pn} w liczbie @{n|int}?', 'd',
             [('idea', 'Miejsca liczymy od prawej: jedności, dziesiątki, setki, tysiące…'),
              ('conclude', 'Na miejscu @{pn} stoi cyfra @{d}.')],
             errors=[('from_left', Int('ds[p]'), 'Miejsca liczymy od prawej strony liczby, a nie od lewej.', 'ds[p] != d')]),
      selfCheck=['(n // pow(10, p)) % 10 == d'], area=A1, prereq=['n46-write-digits'])

skill('n46-compose', S, 'Złóż liczbę z części', ['IV-VI.1.1'],
      [lvl('Do 9 999', thi=9), lvl('Do 999 999', thi=999)],
      [('t', 'randint(1, thi)'), ('s', 'randint(0, 9)'), ('d', 'randint(0, 9)'), ('j', 'randint(0, 9)'),
       ('T', "['tysiąc', 'tysiące', 'tysięcy']"), ('Sx', "['setka', 'setki', 'setek']"),
       ('D', "['dziesiątka', 'dziesiątki', 'dziesiątek']"), ('J', "['jedność', 'jedności', 'jedności']")],
      number('Zapisz liczbę, w której jest: @{t|pl:T}, @{s|pl:Sx}, @{d|pl:D} i @{j|pl:J}.', 't * 1000 + s * 100 + d * 10 + j',
             [('idea', 'Zamieniamy każdą część na liczbę i dodajemy.'),
              ('compute', '@{t * 1000|int} + @{s * 100} + @{d * 10} + @{j} = @{t * 1000 + s * 100 + d * 10 + j|int}')]),
      area=A1, prereq=['n46-digit-place'])

skill('n46-compare', S, 'Porównywanie liczb naturalnych', ['IV-VI.1.1'],
      [lvl('Liczby czterocyfrowe', lo=1000, hi=9999), lvl('Liczby sześciocyfrowe', lo=100000, hi=999999),
       lvl('Liczby siedmiocyfrowe', lo=1000000, hi=9999999)],
      [('a', 'randint(lo, hi)'), ('k', 'randint(0, 2)'), ('delta', 'randint(1, 9) * pow(10, k)'),
       ('b', 'a + delta if randint(0, 1) == 1 else a - delta')],
      choice_text('Porównaj liczby @{a|int} i @{b|int}. Który znak należy wstawić między nie?',
                  [(r'$<$', 'a < b'), (r'$=$', 'a == b'), (r'$>$', 'a > b')],
                  None,
                  [('idea', 'Porównujemy cyfry od najwyższego rzędu. Pierwsza różna cyfra rozstrzyga.'),
                   ('conclude', '@{a|int} @{(\'<\' if a < b else \'>\')} @{b|int}')], fixed_order=True),
      constraints=['b >= lo', 'b <= hi'], area=A1)

skill('n46-order', S, 'Ustaw liczby w kolejności', ['IV-VI.1.1'],
      [lvl('Liczby czterocyfrowe', base_lo=1000, base_hi=9000, spread=900),
       lvl('Liczby sześciocyfrowe', base_lo=100000, base_hi=900000, spread=90000),
       lvl('Liczby siedmiocyfrowe', base_lo=1000000, base_hi=9000000, spread=900000)],
      [('lo', 'randint(base_lo, base_hi)'), ('xs', 'sample(lo, lo + spread, 5)'), ('desc', 'randint(0, 1) == 1')],
      order('@{(\'Ułóż liczby od największej do najmniejszej.\' if desc else \'Ułóż liczby od najmniejszej do największej.\')}',
            'xs', 5, [('idea', 'Najpierw porównaj liczby cyframi od najwyższego rzędu, potem ustaw je po kolei.'),
                      ('conclude', 'Kolejność: @{(reverse(sorted(xs)) if desc else sorted(xs))|list:semi}')],
            fmt='int', descending='desc'),
      area=A1)

skill('n46-number-line', S, 'Liczba na osi liczbowej', ['IV-VI.1.1'],
      [lvl('Co 10, od 0', tick=10, step0=0), lvl('Co 100, od 0', tick=100, step0=0),
       lvl('Co 50 lub 500', tick=50, step0=1), lvl('Duże odstępy', tick=1000, step0=1)],
      [('t', 'tick if step0 == 0 else choice([tick, tick * 2, tick * 5])'), ('m', 'randint(0, 9) * 10 * t if step0 == 1 else 0'),
       ('lo', 'm'), ('hi', 'lo + 10 * t'), ('p', 'lo + randint(1, 9) * t')],
      number('Jaką liczbę oznacza punkt A na osi liczbowej?', 'p',
             [('idea', 'Policz, ile wynosi jedna kreska: od @{lo|int} do @{hi|int} jest 10 odcinków, więc jeden ma @{t|int}.'),
              ('compute', '@{lo|int} + @{(p - lo) // t} · @{t|int} = @{p|int}')],
             media=[{'type': 'figure', 'kind': 'number-line', 'essential': True,
                     'alt': 'Oś liczbowa od @{lo|int} do @{hi|int} z dziesięcioma równymi odcinkami i zaznaczonym punktem A.',
                     'params': {'min': E('lo'), 'max': E('hi'), 'tick': E('t'), 'labelEvery': 5, 'points': [{'label': 'A', 'at': E('p')}]}}]),
      selfCheck=['p > lo', 'p < hi', '(p - lo) % t == 0'], min_distinct=9, area=A1)

skill('n46-rounding', S, 'Zaokrąglanie liczb naturalnych', ['IV-VI.1.1'],
      [lvl('Do dziesiątek i setek', pmin=1, pmax=2), lvl('Do tysięcy', pmin=3, pmax=3), lvl('Do większych rzędów', pmin=3, pmax=5)],
      [('pi', 'randint(pmin, pmax)'), ('step', 'pow(10, pi)'), ('n', 'randint(step, step * 1000 - 1)'),
       ('pn', "['dziesiątek', 'setek', 'tysięcy', 'dziesiątek tysięcy', 'setek tysięcy'][pi - 1]"),
       ('r', '(n + step // 2) // step * step')],
      number('Zaokrąglij liczbę @{n|int} do @{pn}.', 'r',
             [('idea', 'Patrzymy na cyfrę po prawej stronie rzędu zaokrąglania: 0–4 zostawiamy, 5–9 zwiększamy o 1.'),
              ('conclude', '@{n|int} ≈ @{r|int}')],
             errors=[('always_down', Int('n // step * step'), 'Cyfra 5 lub większa oznacza zaokrąglenie w górę.', 'n // step * step != r'),
                     ('always_up', Int('-(-n // step) * step'), 'Cyfra mniejsza niż 5 oznacza zaokrąglenie w dół.', '-(-n // step) * step != r')]),
      constraints=['n % step != 0', 'n >= 2 * step'], selfCheck=['r % step == 0', 'abs(r - n) <= step // 2'], area=A1)

skill('n46-roman-read', S, 'Z rzymskich na dziesiątkowe', ['IV-VI.1.2'],
      [lvl('Do 39', lo=1, hi=39), lvl('Do 399', lo=40, hi=399), lvl('Do 3000', lo=400, hi=3000)],
      [('n', 'randint(lo, hi)')],
      number('Zapisz liczbę @{roman(n)} w systemie dziesiątkowym.', 'n',
             [('idea', 'I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. Mniejsza cyfra przed większą się odejmuje (IV = 4).'),
              ('conclude', '@{roman(n)} = @{n|int}')]),
      area=A1, prereq=[],
      intro='Cyfry rzymskie: I = 1, V = 5, X = 10, L = 50, C = 100, D = 500, M = 1000. Dodajemy je od lewej do prawej. Gdy mniejsza cyfra stoi przed większą, odejmujemy ją (IV = 4, IX = 9, XL = 40).')

skill('n46-roman-write', S, 'Z dziesiątkowych na rzymskie', ['IV-VI.1.2'],
      [lvl('Do 39', lo=2, hi=39), lvl('Do 399', lo=41, hi=399), lvl('Do 3000', lo=401, hi=2990)],
      [('n', 'randint(lo, hi)')],
      choice('Który zapis rzymski przedstawia liczbę @{n|int}?', 'roman(n)',
             ['roman(n + 1)', 'roman(n - 1)', 'roman(n + 10)'],
             [('idea', 'Rozkładamy liczbę na tysiące, setki, dziesiątki i jedności i zapisujemy każdą część cyframi rzymskimi.'),
              ('conclude', '@{n|int} = @{roman(n)}')]),
      area=A1, prereq=['n46-roman-read'])

skill('n46-diff', S, 'O ile większa, o ile mniejsza', ['IV-VI.1.14'],
      [lvl('Małe liczby', lo=20, hi=200, dhi=60), lvl('Trzycyfrowe', lo=100, hi=999, dhi=400), lvl('Wielocyfrowe', lo=1000, hi=99999, dhi=9999)],
      [('y', 'randint(lo, hi)'), ('d', 'randint(2, dhi)'), ('big', 'randint(0, 1) == 1'),
       ('x', 'y + d if big else y - d'), ('adj', "'większa' if big else 'mniejsza'")],
      number('O ile liczba @{x|int} jest @{adj} od liczby @{y|int}?', 'd',
             [('idea', 'Porównanie różnicowe: odejmujemy mniejszą liczbę od większej.'),
              ('compute', '@{max(x, y)|int} − @{min(x, y)|int} = @{d|int}')]),
      constraints=['x > 0'], area=A1)

skill('n46-ratio', S, 'Ile razy większa, ile razy mniejsza', ['IV-VI.1.14'],
      [lvl('Małe liczby', bhi=12, khi=9), lvl('Większe liczby', bhi=60, khi=12), lvl('Duże liczby', bhi=500, khi=20)],
      [('y', 'randint(2, bhi)'), ('k', 'randint(2, khi)'), ('big', 'randint(0, 1) == 1'),
       ('x', 'y * k if big else y'), ('z', 'y if big else y * k'), ('adj', "'większa' if big else 'mniejsza'")],
      number('Ile razy liczba @{x|int} jest @{adj} od liczby @{z|int}?', 'k',
             [('idea', 'Porównanie ilorazowe: dzielimy większą liczbę przez mniejszą.'),
              ('compute', '@{max(x, z)|int} : @{min(x, z)|int} = @{k}')]),
      area=A1, prereq=['n46-diff'])

# ============================================================================ unit 2: działania
skill('n46-add-mental', S, 'Dodawanie w pamięci', ['IV-VI.1.9'],
      [lvl('Dwie liczby dwucyfrowe', alo=11, ahi=99, blo=11, bhi=99), lvl('Trzycyfrowa i dwucyfrowa', alo=101, ahi=999, blo=11, bhi=99),
       lvl('Dwie liczby trzycyfrowe', alo=101, ahi=999, blo=101, bhi=999)],
      [('a', 'randint(alo, ahi)'), ('b', 'randint(blo, bhi)'), ('b0', 'b - b % 10'), ('s', 'a + b')],
      number('Oblicz w pamięci: @{a|int} + @{b|int}', 's',
             [('idea', 'Dodajemy etapami: najpierw dziesiątki, potem jedności.'),
              ('compute', '@{a|int} + @{b0|int} = @{a + b0|int}, a potem + @{b % 10} = @{s|int}')],
             errors=[('no_carry_10', Int('s - 10'), 'Sprawdź jeszcze raz przeniesienie: 10 jedności to 1 dziesiątka.', 's - 10 != s'),
                     ('extra_10', Int('s + 10'), 'Za dużo o 10 – sprawdź dodawanie dziesiątek.')]),
      constraints=['b % 10 != 0'], area=A1)

skill('n46-sub-mental', S, 'Odejmowanie w pamięci', ['IV-VI.1.9'],
      [lvl('Liczby dwucyfrowe', alo=30, ahi=99, blo=11, bhi=29), lvl('Trzycyfrowa minus dwucyfrowa', alo=101, ahi=999, blo=11, bhi=99),
       lvl('Dwie liczby trzycyfrowe', alo=300, ahi=999, blo=101, bhi=299)],
      [('a', 'randint(alo, ahi)'), ('b', 'randint(blo, bhi)'), ('b0', 'b - b % 10'), ('r', 'a - b')],
      number('Oblicz w pamięci: @{a|int} − @{b|int}', 'r',
             [('idea', 'Odejmujemy etapami: najpierw dziesiątki, potem jedności.'),
              ('compute', '@{a|int} − @{b0|int} = @{a - b0|int}, a potem − @{b % 10} = @{r|int}')],
             errors=[('borrow_10', Int('r + 10'), 'Przy pożyczaniu z dziesiątek pamiętaj, że oddajesz 1 dziesiątkę.'),
                     ('extra_10', Int('r - 10'), 'Za mało o 10 – sprawdź odejmowanie dziesiątek.')]),
      constraints=['r > 0', 'b % 10 != 0'], area=A1)

skill('n46-add-written', S, 'Dodawanie pisemne', ['IV-VI.1.9'],
      [lvl('Do 4 cyfr', lo=1000, hi=9999), lvl('Do 6 cyfr', lo=10000, hi=999999), lvl('Trzy składniki', lo=1000, hi=99999)],
      [('a', 'randint(lo, hi)'), ('b', 'randint(lo, hi)'), ('c', 'randint(lo, hi) if lo == 1000 and hi == 99999 else 0')],
      number('Dodaj pisemnie: @{a|int} + @{b|int}@{(\' + \' + fmt(c) if c > 0 else \'\')}', 'a + b + c',
             [('idea', 'Zapisujemy liczby jedna pod drugą (jedności pod jednościami) i dodajemy od prawej, pamiętając o przeniesieniach.'),
              ('conclude', 'Wynik: @{a + b + c|int}')],
             errors=[('forgot_carry_10', Int('a + b + c - 10'), 'Sprawdź przeniesienie z kolumny jedności.', '(a % 10) + (b % 10) + (c % 10) >= 10'),
                     ('forgot_carry_100', Int('a + b + c - 100'), 'Sprawdź przeniesienie z kolumny dziesiątek.', '(a % 100) + (b % 100) + (c % 100) >= 100')]),
      area=A1, prereq=['n46-add-mental'])

skill('n46-sub-written', S, 'Odejmowanie pisemne', ['IV-VI.1.9'],
      [lvl('Do 4 cyfr', lo=1000, hi=9999, zeros=0), lvl('Do 6 cyfr', lo=10000, hi=999999, zeros=0),
       lvl('Ze zerami w odjemnej', lo=10000, hi=999999, zeros=1)],
      [('a0', 'randint(lo, hi)'), ('a', '(a0 // 100) * 100 if zeros == 1 else a0'), ('b', 'randint(lo // 10, hi // 10)'), ('r', 'a - b')],
      number('Odejmij pisemnie: @{a|int} − @{b|int}', 'r',
             [('idea', 'Odejmujemy od prawej. Gdy nie można odjąć, pożyczamy z sąsiedniego rzędu (a gdy tam jest zero – z następnego).'),
              ('conclude', 'Wynik: @{r|int}')],
             errors=[('borrow_10', Int('r + 10'), 'Przy pożyczaniu zmniejsz sąsiednią cyfrę o 1.', 'a % 10 < b % 10'),
                     ('borrow_100', Int('r + 100'), 'Przy pożyczaniu z setek pamiętaj o zmniejszeniu cyfry setek.', '(a % 1000) // 100 < (b % 1000) // 100')]),
      constraints=['r > 0'], selfCheck=['r + b == a'], area=A1, prereq=['n46-sub-mental'])

skill('n46-mul', S, 'Mnożenie liczb naturalnych', ['IV-VI.1.10'],
      [lvl('Dwucyfrowa · jednocyfrowa', alo=11, ahi=99, blo=2, bhi=9), lvl('Trzycyfrowa · jednocyfrowa', alo=101, ahi=999, blo=2, bhi=9),
       lvl('Dwucyfrowa · dwucyfrowa', alo=11, ahi=99, blo=11, bhi=99), lvl('Trzycyfrowa · dwucyfrowa', alo=101, ahi=999, blo=11, bhi=99),
       lvl('Trzycyfrowa · trzycyfrowa', alo=101, ahi=999, blo=101, bhi=999)],
      [('a', 'randint(alo, ahi)'), ('b', 'randint(blo, bhi)')],
      number('Oblicz: @{a|int} · @{b|int}', 'a * b',
             [('idea', 'Mnożymy przez każdą cyfrę drugiej liczby i dodajemy wyniki cząstkowe (pamiętaj o przesunięciu).'),
              ('compute', '@{a|int} · @{b|int} = @{a * b|int}')],
             errors=[('no_shift', Int('a * ((b % 10) + (b // 10))'), 'Mnożąc przez cyfrę dziesiątek, przesuń wynik o jedno miejsce w lewo (dopisz zero).',
                      'b >= 10 and b < 100 and a * ((b % 10) + (b // 10)) != a * b')]),
      area=A1, prereq=[])

skill('n46-div', S, 'Dzielenie liczb naturalnych', ['IV-VI.1.10'],
      [lvl('Dwucyfrowa : jednocyfrowa', qlo=2, qhi=33, blo=2, bhi=9), lvl('Trzycyfrowa : jednocyfrowa', qlo=34, qhi=333, blo=2, bhi=9),
       lvl('Czterocyfrowa : jednocyfrowa', qlo=100, qhi=1111, blo=2, bhi=9), lvl('Przez liczbę dwucyfrową', qlo=2, qhi=99, blo=11, bhi=99),
       lvl('Przez liczbę trzycyfrową', qlo=2, qhi=99, blo=101, bhi=300)],
      [('b', 'randint(blo, bhi)'), ('q', 'randint(qlo, qhi)'), ('a', 'b * q')],
      number('Oblicz: @{a|int} : @{b|int}', 'q',
             [('idea', 'Dzielenie sprawdzamy mnożeniem: wynik · dzielnik = dzielna.'),
              ('compute', '@{q|int} · @{b|int} = @{a|int}')],
             errors=[('off_by_one', Int('q + 1'), 'Sprawdź mnożeniem: wynik razy dzielnik powinien dać dzielną.'),
                     ('digit_zero', Int('q * 10'), 'Sprawdź, ile cyfr powinien mieć wynik (oszacuj).')]),
      selfCheck=['q * b == a'], area=A1)

skill('n46-div-rem', S, 'Dzielenie z resztą', ['IV-VI.1.13'],
      [lvl('Przez jednocyfrową', blo=2, bhi=9, qhi=20), lvl('Przez dwucyfrową', blo=11, bhi=30, qhi=40), lvl('Większe liczby', blo=12, bhi=99, qhi=200)],
      [('b', 'randint(blo, bhi)'), ('q', 'randint(2, qhi)'), ('r', 'randint(1, b - 1)'), ('a', 'b * q + r'), ('ask', 'randint(0, 1)'),
       ('what', "'iloraz niepełny' if ask == 0 else 'reszta'")],
      number('Podziel z resztą @{a|int} przez @{b|int}. Ile wynosi @{what}?', 'q if ask == 0 else r',
             [('idea', 'Szukamy największej wielokrotności @{b}, która mieści się w @{a|int}.'),
              ('compute', '@{a|int} = @{b} · @{q} + @{r}, więc iloraz niepełny to @{q}, a reszta to @{r}.')],
             errors=[('swap', Int('r if ask == 0 else q'), 'Iloraz niepełny to „ile razy się mieści”, a reszta to to, co zostaje.')]),
      selfCheck=['a == b * q + r', 'r < b'], area=A1, prereq=['n46-div'])

skill('n46-div-meaning', S, 'Podział czy mieszczenie?', ['IV-VI.1.11'],
      [lvl('Małe liczby', qhi=9, bhi=6), lvl('Większe liczby', qhi=30, bhi=12)],
      [('b', 'randint(2, bhi)'), ('q', 'randint(2, qhi)'), ('a', 'b * q'), ('mode', 'randint(0, 1)'),
       ('it', "choice([['cukierek', 'cukierki', 'cukierków'], ['naklejka', 'naklejki', 'naklejek'], ['jabłko', 'jabłka', 'jabłek'], ['kartka', 'kartki', 'kartek']])"),
       ('bag', "choice([['torebki', 'torebek'], ['paczki', 'paczek'], ['koperty', 'kopert'], ['skrzynki', 'skrzynek']])"),
       ('txt', "('Rozdzielono po równo ' + pln(a, it) + ' między ' + pln(b, ['osoba', 'osoby', 'osób']) + '. Ile dostała każda osoba?') if mode == 0 else "
               "('Mamy ' + pln(a, it) + '. Do każdej ' + bag[0] + ' wkładamy po ' + pln(b, it) + '. Ile ' + bag[1] + ' potrzeba?')"),
       ('idea', "'To podział na równe części: dzielimy ' + str(a) + ' przez ' + str(b) + '.' if mode == 0 else "
                "'To mieszczenie: sprawdzamy, ile razy ' + str(b) + ' mieści się w ' + str(a) + '.'")],
      number('@{txt}', 'q', [('idea', '@{idea}'), ('compute', '@{a|int} : @{b} = @{q}')]),
      selfCheck=['a == b * q'], area=A1, prereq=['n46-div'])

skill('n46-strat-assoc', S, 'Wygodne mnożenie: łączność', ['IV-VI.1.12'],
      [lvl('Mnożniki 25 i 4', f=25), lvl('Mnożniki 5, 20, 50, 125', f=0)],
      [('a', 'f if f > 0 else choice([5, 20, 50, 125])'),
       ('c', '4 if a == 25 else (2 if a in [5, 50] else (5 if a == 20 else 8))'),
       ('m', 'randint(2, 12)'), ('b', 'c * m')],
      choice_text('Który zapis pokazuje wygodny i poprawny sposób obliczenia @{a} · @{b}?',
                  [(r'$@{a} \cdot @{b} = (@{a} \cdot @{c}) \cdot @{m}$', 'true'),
                   (r'$@{a} \cdot @{b} = (@{a} \cdot @{c}) + @{m}$', 'false'),
                   (r'$@{a} \cdot @{b} = (@{a} + @{c}) \cdot @{m}$', 'false'),
                   (r'$@{a} \cdot @{b} = @{a} \cdot @{c} \cdot @{c}$', 'false')],
                  None, [('idea', 'Rozkładamy @{b} na iloczyn @{c} · @{m}, a potem najpierw mnożymy @{a} · @{c} – to daje okrągłą liczbę.'),
                         ('compute', '@{a} · @{c} = @{a * c}, a @{a * c} · @{m} = @{a * b}')]),
      constraints=['c != m'],
      selfCheck=['c * m == b', 'a * c + m != a * b', '(a + c) * m != a * b', 'a * c * c != a * b'], min_distinct=10, area=A1)

skill('n46-strat-near', S, 'Wygodne mnożenie: blisko 100', ['IV-VI.1.12'],
      [lvl('Liczby 97–99', tlo=1, thi=3), lvl('Liczby 91–99', tlo=1, thi=9)],
      [('c', 'randint(3, 9)'), ('t', 'randint(tlo, thi)'), ('b', '100 - t')],
      choice_text('Który zapis jest poprawnym, wygodnym sposobem obliczenia @{c} · @{b}?',
                  [(r'$@{c} \cdot @{b} = @{c} \cdot 100 - @{c} \cdot @{t}$', 'true'),
                   (r'$@{c} \cdot @{b} = @{c} \cdot 100 - @{t}$', 'false'),
                   (r'$@{c} \cdot @{b} = @{c} \cdot 100 + @{c} \cdot @{t}$', 'false'),
                   (r'$@{c} \cdot @{b} = (@{c} + 100) \cdot @{t}$', 'false')],
                  None, [('idea', '@{b} jest blisko 100, więc liczymy @{c} · 100 i odejmujemy to, co za dużo: @{c} · @{t}.'),
                         ('compute', '@{c * 100} − @{c * t} = @{c * b}')]),
      selfCheck=['c * 100 - t != c * b', 'c * 100 + c * t != c * b', '(c + 100) * t != c * b'], area=A1)

skill('n46-strat-split', S, 'Wygodne mnożenie: rozbicie liczby', ['IV-VI.1.12'],
      [lvl('Jednocyfrowa · dwucyfrowa', clo=3, chi=9)],
      [('c', 'randint(clo, chi)'), ('u', 'randint(2, 9) * 10'), ('w', 'randint(2, 9)'), ('b', 'u + w')],
      choice_text('Który zapis jest poprawnym sposobem obliczenia @{c} · @{b} przez rozbicie liczby @{b}?',
                  [(r'$@{c} \cdot @{b} = @{c} \cdot @{u} + @{c} \cdot @{w}$', 'true'),
                   (r'$@{c} \cdot @{b} = @{c} \cdot @{u} + @{w}$', 'false'),
                   (r'$@{c} \cdot @{b} = (@{c} + @{u}) \cdot @{w}$', 'false'),
                   (r'$@{c} \cdot @{b} = @{c} \cdot @{u} \cdot @{w}$', 'false')],
                  None, [('idea', 'Rozbijamy @{b} na @{u} + @{w} i mnożymy każdą część osobno (rozdzielność mnożenia względem dodawania).'),
                         ('compute', '@{c * u} + @{c * w} = @{c * b}')]),
      constraints=['w != c'],
      selfCheck=['c * u + w != c * b', '(c + u) * w != c * b', 'c * u * w != c * b'], area=A1)


# ============================================================================ ścieżka: działy 1-5
un = Unit(S, 'n46-u1', 'Zapis i odczyt liczb', 'Czytamy i zapisujemy duże liczby naturalne.', 'numbers', area=A1)
un.learn('n46-write-digits').learn('n46-read-number').learn('n46-digit-place').learn('n46-compose')
un.review('Powtórka: zapis liczb', ['n46-write-digits', 'n46-read-number', 'n46-digit-place', 'n46-compose'])
un.checkpoint(['n46-write-digits', 'n46-read-number', 'n46-digit-place', 'n46-compose'])

un = Unit(S, 'n46-u2', 'Porównywanie i zaokrąglanie', 'Porównujemy liczby, ustawiamy je w kolejności, zaznaczamy na osi i zaokrąglamy.', 'compare', area=A1)
un.learn('n46-compare').learn('n46-order').learn('n46-number-line').learn('n46-rounding')
un.learn('n46-diff').learn('n46-ratio')
un.checkpoint(['n46-compare', 'n46-order', 'n46-number-line', 'n46-rounding', 'n46-diff', 'n46-ratio'])

un = Unit(S, 'n46-u3', 'Liczby rzymskie', 'Zamieniamy liczby rzymskie na dziesiątkowe i odwrotnie.', 'roman', area=A1)
un.learn('n46-roman-read').learn('n46-roman-write').review('Powtórka: liczby rzymskie', ['n46-roman-read', 'n46-roman-write'])
un.checkpoint(['n46-roman-read', 'n46-roman-write'])

un = Unit(S, 'n46-u4', 'Dodawanie i odejmowanie', 'Rachunki w pamięci i pisemnie.', 'plusminus', area=A1)
un.learn('n46-add-mental').learn('n46-sub-mental').review('Powtórka: w pamięci', ['n46-add-mental', 'n46-sub-mental'])
un.learn('n46-add-written').learn('n46-sub-written')
un.checkpoint(['n46-add-mental', 'n46-sub-mental', 'n46-add-written', 'n46-sub-written'])

un = Unit(S, 'n46-u5', 'Mnożenie i dzielenie', 'Mnożymy i dzielimy liczby naturalne, także z resztą, i liczymy sprytnie.', 'timesdiv', area=A1)
un.learn('n46-mul').learn('n46-div').learn('n46-div-meaning').learn('n46-div-rem')
un.review('Powtórka: mnożenie i dzielenie', ['n46-mul', 'n46-div', 'n46-div-meaning', 'n46-div-rem'])
un.learn('n46-strat-assoc').learn('n46-strat-near').learn('n46-strat-split')
un.checkpoint(['n46-mul', 'n46-div', 'n46-div-rem', 'n46-strat-assoc', 'n46-strat-near', 'n46-strat-split'])
