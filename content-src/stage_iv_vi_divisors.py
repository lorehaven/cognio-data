"""Stage IV-VI, area 1 (Liczby), part 2: order of operations, estimation, powers, divisibility, primes, GCD/LCM.
Objectives: IV-VI.1.3-1.8, 1.15, 1.36, 1.37."""
from dsl import *

S = 'IV-VI'
A1 = 'IV-VI.1'

# ============================================================================ kolejność działań, szacowanie, potęgi
skill('n46-order-ops', S, 'Kolejność wykonywania działań', ['IV-VI.1.36'],
      [lvl('Mnożenie przed dodawaniem', fmax=3, hi=9), lvl('Nawiasy i dzielenie', fmax=5, hi=12), lvl('Złożone wyrażenia', fmax=7, hi=15)],
      [('f', 'randint(0, fmax)'), ('a', 'randint(2, hi)'), ('b', 'randint(2, hi)'), ('c', 'randint(2, hi)'), ('d', 'randint(2, hi)'),
       ('vals', '[a + b * c, (a + b) * c, a * b - c, a - b * c, (a - b) / c, a + b / c, a * (b + c) - d, a / b + c * d]'),
       ('oks', '[True, True, a * b > c, a > b * c, a > b and (a - b) % c == 0, b % c == 0, a * (b + c) > d, a % b == 0]'),
       ('txts', "[str(a) + ' + ' + str(b) + ' · ' + str(c), '(' + str(a) + ' + ' + str(b) + ') · ' + str(c), str(a) + ' · ' + str(b) + ' − ' + str(c), "
                "str(a) + ' − ' + str(b) + ' · ' + str(c), '(' + str(a) + ' − ' + str(b) + ') : ' + str(c), str(a) + ' + ' + str(b) + ' : ' + str(c), "
                "str(a) + ' · (' + str(b) + ' + ' + str(c) + ') − ' + str(d), str(a) + ' : ' + str(b) + ' + ' + str(c) + ' · ' + str(d)]"),
       ('ltr', '[(a + b) * c, (a + b) * c, a * b - c, (a - b) * c, (a - b) / c, (a + b) / c, a * (b + c) - d, (a / b + c) * d]'),
       ('v', 'vals[f]'), ('txt', 'txts[f]')],
      number('Oblicz: @{txt}', 'v',
             [('idea', 'Najpierw wykonujemy działania w nawiasach, potem mnożenie i dzielenie (od lewej do prawej), na końcu dodawanie i odejmowanie.'),
              ('compute', '@{txt} = @{v}')],
             errors=[('left_to_right', Int('ltr[f]'), 'Mnożenie i dzielenie wykonujemy przed dodawaniem i odejmowaniem – nie po kolei od lewej.', 'ltr[f] != v')]),
      constraints=['oks[f]', 'v > 0', 'denom(v) == 1'], area=A1,
      intro='Kolejność działań: 1) nawiasy, 2) mnożenie i dzielenie od lewej do prawej, 3) dodawanie i odejmowanie od lewej do prawej.',
      ideas=['Mnożenie i dzielenie są „silniejsze” niż dodawanie i odejmowanie.'])

skill('n46-estimate-product', S, 'Oszacuj iloczyn', ['IV-VI.1.37', 'IV-VI.6.1.c'],
      [lvl('Dwie liczby dwucyfrowe', alo=12, ahi=99, blo=12, bhi=99), lvl('Trzycyfrowa i dwucyfrowa', alo=101, ahi=999, blo=12, bhi=99)],
      [('a', 'randint(alo, ahi)'), ('b', 'randint(blo, bhi)'),
       ('pa', 'pow(10, len(digits(a)) - 1)'), ('pb', 'pow(10, len(digits(b)) - 1)'),
       ('ra', '(a + pa // 2) // pa * pa'), ('rb', '(b + pb // 2) // pb * pb'), ('est', 'ra * rb')],
      choice('Które oszacowanie jest najbliższe wynikowi działania @{a} · @{b}?', 'est', ['est * 10', 'est // 10', 'est * 100'],
             [('idea', 'Zaokrąglamy obie liczby do najwyższego rzędu: @{a} ≈ @{ra}, @{b} ≈ @{rb}.'),
              ('compute', '@{ra} · @{rb} = @{est|int}')], fmt='int'),
      selfCheck=['abs(a * b - est) * 2 < est * 3', 'est >= 100'], constraints=['est >= 100', 'est % 100 == 0'], area=A1,
      ideas=['Szacowanie pomaga sprawdzić, czy wynik ma sensowną wielkość.'])

skill('n46-estimate-sum', S, 'Oszacuj sumę lub różnicę', ['IV-VI.1.37', 'IV-VI.6.1.c'],
      [lvl('Do setek', pw=100, lo=1000, hi=9999), lvl('Do tysięcy', pw=1000, lo=10000, hi=99999)],
      [('a', 'randint(lo, hi)'), ('b', 'randint(lo // 4, hi // 2)'), ('plus', 'randint(0, 1) == 1'),
       ('ra', '(a + pw // 2) // pw * pw'), ('rb', '(b + pw // 2) // pw * pw'), ('est', 'ra + rb if plus else ra - rb'),
       ('sign', "'+' if plus else '−'")],
      choice('Oszacuj wynik działania @{a|int} @{sign} @{b|int}, zaokrąglając składniki do @{(\'setek\' if pw == 100 else \'tysięcy\')}. Który wynik jest najlepszy?',
             'est', ['est + pw', 'est - pw', 'est * 10'],
             [('idea', 'Zaokrąglamy obie liczby: @{a|int} ≈ @{ra|int}, @{b|int} ≈ @{rb|int}.'),
              ('compute', '@{ra|int} @{sign} @{rb|int} = @{est|int}')], fmt='int'),
      constraints=['a > b', 'est > pw'], selfCheck=['abs((a + b if plus else a - b) - est) <= pw'], area=A1)

skill('n46-power-calc', S, 'Obliczanie potęg', ['IV-VI.1.15'],
      [lvl('Małe podstawy', md=8, bmin=2, bmax=5, emin=2, emax=3), lvl('Kwadraty liczb od 6 do 15', md=10, bmin=6, bmax=15, emin=2, emax=2),
       lvl('Wyższe wykładniki', bmin=2, bmax=10, emin=3, emax=5)],
      [('base', 'randint(bmin, bmax)'), ('e', 'randint(emin, emax)'), ('v', 'pow(base, e)')],
      number('Oblicz: $@{base}^{@{e}}$', 'v',
             [('idea', r'Potęga to iloczyn tylu jednakowych czynników, ile wynosi wykładnik: $@{base}^{@{e}} = @{join(repeat(base, e), " \\cdot ")}$.'),
              ('conclude', '$@{base}^{@{e}} = @{v|int}$')],
             errors=[('multiply_exponent', Int('base * e'), 'Wykładnik mówi, ile razy mnożymy podstawę przez siebie – to nie jest mnożenie przez wykładnik.', 'base * e != v')]),
      selfCheck=['v == product(repeat(base, e))'], area=A1,
      intro='Potęga $a^n$ to iloczyn n czynników równych a. Na przykład $2^4 = 2 \\cdot 2 \\cdot 2 \\cdot 2 = 16$. Kwadrat to druga potęga, sześcian – trzecia.')

skill('n46-power-recognize', S, 'Kwadraty i sześciany liczb', ['IV-VI.1.15'],
      [lvl('Kwadraty', kind=2), lvl('Sześciany', kind=3)],
      [('s1', 'randint(3, 30)'), ('s2', 'randint(3, 30)'),
       ('x1', 'pow(s1, kind)'), ('x2', 'pow(s2, kind) + randint(1, 3)'), ('x3', 'randint(20, 900)'), ('x4', 'randint(20, 900)'), ('x5', 'randint(20, 900)'),
       ('word', "'kwadratami' if kind == 2 else 'sześcianami'")],
      choice_text('Które z liczb są @{word} liczb naturalnych? Zaznacz wszystkie.',
                  [(f'@{{x{i}|int}}', f'(is_square(x{i}) if kind == 2 else pow(icbrt(x{i}), 3) == x{i})') for i in range(1, 6)],
                  None, [('idea', 'Sprawdzamy, czy liczba jest iloczynem dwóch (trzech) jednakowych czynników.'),
                         ('conclude', 'Na przykład @{x1|int} = $@{s1}^{@{kind}}$.')], multi=True),
      constraints=['len(uniq([x1, x2, x3, x4, x5])) == 5'], area=A1, prereq=['n46-power-calc'])

# ============================================================================ podzielność
skill('n46-divisible-pick', S, 'Która liczba jest podzielna?', ['IV-VI.1.3'],
      [lvl('Przez 2, 5 lub 10', ds='[2, 5, 10]'), lvl('Przez 3 lub 9', ds='[3, 9]'), lvl('Przez 4', ds='[4]'),
       lvl('Przez 2, 3, 4, 5, 9, 10', ds='[2, 3, 4, 5, 9, 10]')],
      [('d', 'choice(ds)'), ('c', 'd * randint(12, 800)'),
       ('rule', "['', '', 'ostatnia cyfra jest parzysta', 'suma cyfr dzieli się przez 3', 'dwie ostatnie cyfry tworzą liczbę podzielną przez 4', "
                "'ostatnia cyfra to 0 lub 5', '', '', '', 'suma cyfr dzieli się przez 9', 'ostatnia cyfra to 0'][d]")],
      choice('Która z liczb jest podzielna przez @{d}?', 'c', ['c + 1', 'c + d + 1', 'c + 3 * d - 1'],
             [('idea', 'Cecha podzielności przez @{d}: @{rule}.'), ('conclude', 'Liczba @{c|int} jest podzielna przez @{d}.')], fmt='int'),
      selfCheck=['c % d == 0', '(c + 1) % d != 0', '(c + d + 1) % d != 0', '(c + 3 * d - 1) % d != 0'], area=A1,
      intro='Cechy podzielności: przez 2 – ostatnia cyfra parzysta; przez 3 – suma cyfr dzieli się przez 3; przez 4 – dwie ostatnie cyfry tworzą liczbę podzielną przez 4; przez 5 – ostatnia cyfra 0 lub 5; przez 9 – suma cyfr dzieli się przez 9; przez 10 – ostatnia cyfra 0.')

skill('n46-divisible-yesno', S, 'Czy liczba jest podzielna?', ['IV-VI.1.3'],
      [lvl('Przez 2, 5, 10', ds='[2, 5, 10]'), lvl('Przez 3 lub 9', ds='[3, 9]'), lvl('Przez 4', ds='[4]'), lvl('Wszystkie cechy', ds='[2, 3, 4, 5, 9, 10]')],
      [('d', 'choice(ds)'), ('n', 'randint(100, 99999)'), ('yes', 'n % d == 0'),
       ('res', "'daje resztę 0' if yes else 'daje resztę ' + str(n % d)")],
      choice_text('Czy liczba @{n|int} jest podzielna przez @{d}?', [('Tak', 'yes'), ('Nie', 'not yes')], None,
                  [('idea', 'Sprawdzamy cechę podzielności przez @{d}.'), ('conclude', '@{n|int} : @{d} @{res}.')], fixed_order=True),
      area=A1, prereq=['n46-divisible-pick'])

skill('n46-divisible-digit', S, 'Brakująca cyfra', ['IV-VI.1.3'],
      [lvl('Podzielność przez 3', d=3), lvl('Podzielność przez 9', d=9)],
      [('k', 'randint(3, 5)'), ('n', 'randint(pow(10, k - 1), pow(10, k) - 1)'), ('ds', 'digits(n)'), ('i', 'randint(1, k - 1)'),
       ('rest', 'sum(ds) - ds[i]'), ('x', '(d - rest % d) % d'), ('pattern', "join(setat(ds, i, 'x'), '')")],
      number('Jaka jest najmniejsza cyfra x, dla której liczba @{pattern} jest podzielna przez @{d}?', 'x',
             [('idea', 'Suma cyfr musi dzielić się przez @{d}. Suma pozostałych cyfr to @{rest}.'),
              ('conclude', '@{rest} + @{x} = @{rest + x}, a @{rest + x} dzieli się przez @{d}.')]),
      selfCheck=['(rest + x) % d == 0', 'x < d'], area=A1, prereq=['n46-divisible-pick'])

skill('n46-prime-pick', S, 'Liczby pierwsze i złożone', ['IV-VI.1.4'],
      [lvl('Do 50', pr='[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]', co='[9, 15, 21, 25, 27, 33, 35, 39, 45, 49]'),
       lvl('Do 100 (podstępne złożone)', pr='[53, 59, 61, 67, 71, 73, 79, 83, 89, 97]', co='[51, 57, 63, 65, 69, 77, 81, 85, 87, 91, 93, 95, 99]')],
      [('p', 'choice(pr)'), ('c1', 'choice(co)'), ('c2', 'choice(co)'), ('c3', 'choice(co)'), ('dv', 'divisors(c1)[1]')],
      choice_text('Która z liczb jest liczbą pierwszą?',
                  [('@{p}', 'true'), ('@{c1}', 'false'), ('@{c2}', 'false'), ('@{c3}', 'false')], None,
                  [('idea', 'Liczba pierwsza ma dokładnie dwa dzielniki: 1 i samą siebie.'),
                   ('conclude', 'Na przykład @{c1} = @{dv} · @{c1 // dv}, więc @{c1} nie jest pierwsza.')]),
      constraints=['len(uniq([c1, c2, c3])) == 3'], selfCheck=['is_prime(p)', 'not is_prime(c1)', 'not is_prime(c2)', 'not is_prime(c3)'], area=A1,
      intro='Liczba pierwsza ma dokładnie dwa dzielniki: 1 i samą siebie (np. 2, 3, 5, 7, 11). Liczba złożona ma więcej dzielników (np. 9 = 3 · 3). Liczba 1 nie jest ani pierwsza, ani złożona.')

skill('n46-smallest-divisor', S, 'Najmniejszy dzielnik większy od 1', ['IV-VI.1.4'],
      [lvl('Liczby do 60', lo=10, hi=60), lvl('Liczby do 99', lo=40, hi=99)],
      [('n', 'randint(lo, hi)'), ('d', 'divisors(n)[1]')],
      number('Jaki jest najmniejszy dzielnik liczby @{n} większy od 1?', 'd',
             [('idea', 'Sprawdzamy kolejne liczby: 2, 3, 5, 7… (cechy podzielności).'), ('conclude', '@{n} : @{d} = @{n // d}')]),
      constraints=['not is_prime(n)'], selfCheck=['n % d == 0', 'is_prime(d)'], area=A1, prereq=['n46-prime-pick'])

skill('n46-factorization-pick', S, 'Rozkład na czynniki pierwsze', ['IV-VI.1.5'],
      [lvl('Liczby do 60', lo=12, hi=60), lvl('Liczby do 99', lo=40, hi=99)],
      [('n', 'randint(lo, hi)'), ('f', 'factorize(n)'), ('m', 'len(f)'), ('ok', 'm >= 3', 'require'),
       ('good', "join(f, ' · ')"), ('w1', "join([f[0] * f[1]] + drop(f, 2), ' · ')"),
       ('w2', "join(take(f, m - 2) + [f[m - 2] * f[m - 1]], ' · ')"), ('w3', "join(take(f, m - 1) + [f[m - 1] + 2], ' · ')")],
      choice('Który zapis jest rozkładem liczby @{n} na czynniki pierwsze?', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Dzielimy przez kolejne liczby pierwsze (2, 3, 5, 7…), aż dojdziemy do 1.'), ('conclude', '@{n} = @{good}')]),
      selfCheck=['product(f) == n', 'is_prime(f[m - 1])'], area=A1, prereq=['n46-prime-pick'],
      intro='Rozkład na czynniki pierwsze to zapis liczby jako iloczynu liczb pierwszych, np. $60 = 2 \\cdot 2 \\cdot 3 \\cdot 5$. Dzielimy liczbę przez kolejne liczby pierwsze.')

skill('n46-factorization-fact', S, 'Czynniki pierwsze: pytania', ['IV-VI.1.5'],
      [lvl('Liczby do 60', lo=12, hi=60), lvl('Liczby do 99', lo=40, hi=99)],
      [('n', 'randint(lo, hi)'), ('f', 'factorize(n)'), ('u', 'uniq(f)'), ('ask', 'randint(0, 2)'),
       ('q', "'Ile różnych liczb pierwszych występuje w rozkładzie liczby ' + str(n) + ' na czynniki pierwsze?' if ask == 0 else "
             "('Jaki jest największy czynnik pierwszy liczby ' + str(n) + '?' if ask == 1 else 'Ile czynników (licząc powtórzenia) ma rozkład liczby ' + str(n) + ' na czynniki pierwsze?')"),
       ('ans', 'len(u) if ask == 0 else (max(f) if ask == 1 else len(f))')],
      number('@{q}', 'ans', [('idea', 'Rozkładamy liczbę: @{n} = @{join(f, " · ")}.'), ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['len(f) >= 2'], selfCheck=['product(f) == n'], area=A1, prereq=['n46-factorization-pick'])

skill('n46-gcd', S, 'Największy wspólny dzielnik', ['IV-VI.1.6'],
      [lvl('Liczby do 40', ghi=8, xhi=6), lvl('Liczby do 99', ghi=20, xhi=9)],
      [('g', 'randint(2, ghi)'), ('x', 'randint(2, xhi)'), ('y', 'randint(2, xhi)'), ('a', 'g * x'), ('b', 'g * y')],
      number('Znajdź największy wspólny dzielnik liczb @{a} i @{b}.', 'g',
             [('idea', 'Wypisz dzielniki obu liczb i wybierz największy wspólny.'),
              ('compute', 'Dzielniki @{a}: @{divisors(a)|list}. Dzielniki @{b}: @{divisors(b)|list}.'), ('conclude', 'NWD(@{a}, @{b}) = @{g}')],
             errors=[('lcm_instead', Int('lcm(a, b)'), 'Szukamy największej liczby, przez którą dzielą się obie liczby (dzielnika), a nie wielokrotności.', 'lcm(a, b) != g')]),
      constraints=['gcd(x, y) == 1', 'x != y', 'a <= 99', 'b <= 99'], selfCheck=['a % g == 0', 'b % g == 0', 'gcd(a // g, b // g) == 1'], area=A1, prereq=['n46-divisible-pick'],
      intro='NWD to największa liczba, przez którą dzielą się obie liczby. Wypisz dzielniki każdej z nich i znajdź największy wspólny.')

skill('n46-lcm', S, 'Najmniejsza wspólna wielokrotność', ['IV-VI.1.6'],
      [lvl('Liczby do 12', hi=12), lvl('Liczby do 30', hi=30), lvl('Liczby do 99', hi=99)],
      [('a', 'randint(2, hi)'), ('b', 'randint(2, hi)'), ('l', 'lcm(a, b)')],
      number('Znajdź najmniejszą wspólną wielokrotność liczb @{a} i @{b}.', 'l',
             [('idea', 'Wypisuj kolejne wielokrotności większej liczby, aż trafisz na taką, która dzieli się przez drugą.'),
              ('conclude', 'NWW(@{a}, @{b}) = @{l|int}')],
             errors=[('product', Int('a * b'), 'Iloczyn jest wspólną wielokrotnością, ale nie zawsze najmniejszą.', 'a * b != l'),
                     ('gcd_instead', Int('gcd(a, b)'), 'Szukamy wielokrotności (liczby, na którą obie liczby się dzielą), a nie dzielnika.', 'gcd(a, b) != l')]),
      constraints=['a != b', 'a % b != 0', 'b % a != 0'], selfCheck=['l % a == 0', 'l % b == 0', 'l // a * a == l', 'gcd(l // a, l // b) == 1'], area=A1,
      prereq=['n46-gcd'])

skill('n46-common-divisors', S, 'Wspólne dzielniki', ['IV-VI.1.6'],
      [lvl('Mniejsze liczby', gmax=6), lvl('Większe liczby', gmax=12)],
      [('g', 'randint(4, gmax)'), ('x', 'randint(2, 8)'), ('y', 'randint(2, 8)'), ('a', 'g * x'), ('b', 'g * y'),
       ('c', 'sample(2, 20, 6)')],
      choice_text('Które z liczb są wspólnymi dzielnikami liczb @{a} i @{b}? Zaznacz wszystkie.',
                  [(f'@{{c[{i}]}}', f'a % c[{i}] == 0 and b % c[{i}] == 0') for i in range(6)], None,
                  [('idea', 'Wspólny dzielnik musi dzielić jednocześnie @{a} i @{b}.'),
                   ('conclude', 'NWD(@{a}, @{b}) = @{gcd(a, b)}, a wspólne dzielniki to dzielniki NWD.')], multi=True),
      constraints=['a != b', 'a <= 99', 'b <= 99'], area=A1, prereq=['n46-gcd'])

skill('n46-gcd-lcm-word', S, 'Dzielniki i wielokrotności w zadaniach', ['IV-VI.1.7'],
      [lvl('Pakowanie i dzielenie (NWD)', mode=0), lvl('Jednoczesne zdarzenia (NWW)', mode=1)],
      [('g', 'randint(2, 9)'), ('x', 'randint(2, 6)'), ('y', 'randint(2, 6)'), ('a', 'g * x'), ('b', 'g * y'),
       ('pr', "choice([[['jabłko', 'jabłka', 'jabłek'], ['gruszka', 'gruszki', 'gruszek']], [['ciastko', 'ciastka', 'ciastek'], ['wafelek', 'wafelki', 'wafelków']], "
              "[['cukierek', 'cukierki', 'cukierków'], ['draże', 'draże', 'draży']], [['długopis', 'długopisy', 'długopisów'], ['ołówek', 'ołówki', 'ołówków']]])"),
       ('it1', 'pr[0]'), ('it2', 'pr[1]'),
       ('who', "choice(['Latarnia', 'Boja', 'Dzwonek'])"),
       ('txt', "('Mamy ' + pln(a, it1) + ' i ' + pln(b, it2) + '. Chcemy zrobić jak najwięcej jednakowych paczek: w każdej ma być tyle samo ' + it1[2] + ' i tyle samo ' + it2[2] + ', a nic nie może zostać. Ile paczek zrobimy?') if mode == 0 else "
               "('Dwa sygnały świetlne błysnęły jednocześnie. Pierwszy błyska co ' + str(a) + ' s, a drugi co ' + str(b) + ' s. Po ilu sekundach błysną znowu jednocześnie po raz pierwszy?')"),
       ('ans', 'gcd(a, b) if mode == 0 else lcm(a, b)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Liczba paczek musi być dzielnikiem obu liczb, a ma być jak największa: szukamy NWD.' if mode == 0 else 'Szukamy najmniejszej liczby, która jest wielokrotnością obu okresów: NWW.')}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['gcd(x, y) == 1', 'x != y', 'a != b'], selfCheck=['mode == 1 or (a % ans == 0 and b % ans == 0)', 'mode == 0 or (ans % a == 0 and ans % b == 0)'],
      area=A1, prereq=['n46-lcm'])

skill('n46-count-multiples', S, 'Ile jest takich liczb?', ['IV-VI.1.8'],
      [lvl('Od 1 do n', kind=0), lvl('Liczby dwu- i trzycyfrowe', kind=1), lvl('Podzielne przez dwie liczby', kind=2)],
      [('k', 'randint(3, 9)'), ('k2', 'randint(2, 6)'), ('n', 'randint(30, 150)'), ('digits3', 'randint(0, 1)'),
       ('q', "('Ile liczb od 1 do ' + str(n) + ' jest podzielnych przez ' + str(k) + '?') if kind == 0 else "
             "(('Ile jest liczb ' + ('trzycyfrowych' if digits3 == 1 else 'dwucyfrowych') + ' podzielnych przez ' + str(k) + '?') if kind == 1 else "
             "('Ile liczb od 1 do ' + str(n) + ' jest podzielnych jednocześnie przez ' + str(k) + ' i przez ' + str(k2) + '?'))"),
       ('ans', 'n // k if kind == 0 else ((999 // k - 99 // k if digits3 == 1 else 99 // k - 9 // k) if kind == 1 else n // lcm(k, k2))')],
      number('@{q}', 'ans',
             [('idea', 'Takie liczby to kolejne wielokrotności. Sprawdź, ile ich mieści się w podanym zakresie.'), ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['k % k2 != 0', 'k2 % k != 0', 'ans >= 2'], area=A1, prereq=['n46-divisible-pick'])


# ============================================================================ ścieżka: działy 4-8 (liczby naturalne)
un = Unit(S, 'n46-u6', 'Kolejność działań, szacowanie, potęgi', 'Obliczamy w dobrej kolejności, szacujemy wyniki i poznajemy potęgi.', 'calculator', area=A1)
un.learn('n46-order-ops').learn('n46-estimate-product').learn('n46-estimate-sum').review('Powtórka: działania', ['n46-order-ops', 'n46-estimate-product', 'n46-estimate-sum'])
un.learn('n46-power-calc').learn('n46-power-recognize').checkpoint(['n46-order-ops', 'n46-estimate-product', 'n46-estimate-sum', 'n46-power-calc', 'n46-power-recognize'])

un = Unit(S, 'n46-u7', 'Podzielność i liczby pierwsze', 'Cechy podzielności, liczby pierwsze i rozkład na czynniki pierwsze.', 'divide', area=A1)
un.learn('n46-divisible-pick').learn('n46-divisible-yesno').learn('n46-divisible-digit').review('Powtórka: podzielność', ['n46-divisible-pick', 'n46-divisible-yesno', 'n46-divisible-digit'])
un.learn('n46-prime-pick').learn('n46-smallest-divisor').learn('n46-factorization-pick').learn('n46-factorization-fact')
un.checkpoint(['n46-divisible-pick', 'n46-divisible-digit', 'n46-prime-pick', 'n46-smallest-divisor', 'n46-factorization-pick'])

un = Unit(S, 'n46-u8', 'NWD i NWW', 'Wspólne dzielniki i wielokrotności oraz zadania z ich użyciem.', 'overlap', area=A1)
un.learn('n46-gcd').learn('n46-lcm').learn('n46-common-divisors').review('Powtórka: NWD i NWW', ['n46-gcd', 'n46-lcm', 'n46-common-divisors'])
un.learn('n46-gcd-lcm-word').learn('n46-count-multiples').checkpoint(['n46-gcd', 'n46-lcm', 'n46-common-divisors', 'n46-gcd-lcm-word', 'n46-count-multiples'])
