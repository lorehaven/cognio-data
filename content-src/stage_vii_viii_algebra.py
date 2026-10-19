"""Stage VII-VIII, area 2 (Algebra).  Objectives: VII-VIII.2.1 - 2.12.  Polynomial text is built with the DSL helper poly()."""
from dsl import *

S = 'VII-VIII'
A2 = 'VII-VIII.2'

# ============================================================================ wyrażenia (2.1 - 2.3)
skill('vh-alg-build', S, 'Wyrażenie z dwiema zmiennymi', ['VII-VIII.2.1'],
      [lvl('Zakupy i wiek', pmin=0, pmax=2), lvl('Geometria i ruch', pmin=3, pmax=5)],
      [('k', 'randint(2, 9)'), ('m', 'randint(2, 9)'), ('p', 'randint(pmin, pmax)'),
       ('texts', "['Zeszyt kosztuje a zł, a długopis b zł. Jakie wyrażenie opisuje koszt ' + str(k) + ' zeszytów i ' + str(m) + ' długopisów?', "
                 "'Ola ma x lat, a jej brat y lat. Jakie wyrażenie opisuje sumę ich wieku za ' + str(k) + ' lat?', "
                 "'W kinie jest x rzędów po y miejsc. Liczbę miejsc zwiększono o ' + str(k) + '. Jakie wyrażenie opisuje liczbę miejsc?', "
                 "'Prostokąt ma boki a i b. Jedną z jego długości zwiększono o ' + str(k) + '. Jakie wyrażenie opisuje nowy obwód?', "
                 "'Pociąg jechał v km/h przez t godzin, a potem jeszcze ' + str(k) + ' km. Jakie wyrażenie opisuje całą przebytą drogę?', "
                 "'Pole kwadratu o boku a zmniejszono o pole kwadratu o boku b. Jakie wyrażenie opisuje różnicę pól?']"),
       ('opts', "[[str(k) + 'a + ' + str(m) + 'b', str(k) + 'a · ' + str(m) + 'b', str(k + m) + 'ab', 'a + b + ' + str(k + m)], "
                "['x + y + ' + str(2 * k), 'x + y + ' + str(k), '2(x + y) + ' + str(k), '(x + ' + str(k) + ')(y + ' + str(k) + ')'], "
                "['xy + ' + str(k), 'x + y + ' + str(k), 'x · (y + ' + str(k) + ')', '(x + ' + str(k) + ') · y'], "
                "['2a + 2b + ' + str(k), '2(a + b + ' + str(k) + ')', 'a + b + ' + str(k), '4a + ' + str(k)], "
                "['vt + ' + str(k), 'v + t + ' + str(k), '(v + ' + str(k) + ')t', 'v · (t + ' + str(k) + ')'], "
                "['a² − b²', '(a − b)²', 'a − b', '2a − 2b']]")],
      choice('@{texts[p]}', 'opts[p][0]', ['opts[p][1]', 'opts[p][2]', 'opts[p][3]'],
             [('idea', 'Zapisz każdą wielkość z zadania literą lub liczbą i połącz je działaniami z treści.'), ('conclude', 'Poprawne wyrażenie: @{opts[p][0]}.')]),
      constraints=['p != 3 or k != 2'], min_distinct=12, area=A2, prereq=['n46-alg-expression'])

skill('vh-alg-evaluate', S, 'Wartość wyrażenia algebraicznego', ['VII-VIII.2.2'],
      [lvl('Dwa jednomiany', terms=2), lvl('Trzy jednomiany', terms=3)],
      [('x', 'randint(-4, 4)'), ('y', 'randint(-4, 4)'), ('a', 'randint(-5, 5)'), ('b', 'randint(-5, 5)'), ('c', 'randint(-5, 5)'),
       ('cs', '[a, b, c] if terms == 3 else [a, b, 0]'), ('vs', "['x²', 'xy', 'y']"),
       ('v', 'cs[0] * x * x + cs[1] * x * y + cs[2] * y')],
      number('Oblicz wartość wyrażenia @{poly(cs, vs)} dla x = @{x} i y = @{y}.', 'v',
             [('idea', 'Podstaw liczby w miejsce liter (liczby ujemne wstaw w nawiasach) i wykonaj działania we właściwej kolejności.'),
              ('compute', "@{(str(cs[0]) + ' · ' + par(x) + '² + ' + par(cs[1]) + ' · ' + par(x) + ' · ' + par(y) + (' + ' + par(cs[2]) + ' · ' + par(y) if terms == 3 else '') + ' = ' + str(v))}")],
             errors=[('square_sign', Int('cs[0] * (-x * x) + cs[1] * x * y + cs[2] * y'), 'Kwadrat liczby ujemnej jest dodatni: (−2)² = 4, a nie −4.', 'x < 0 and cs[0] != 0')]),
      constraints=['a != 0 and b != 0', 'terms == 2 or c != 0', 'x != 0 and y != 0'], min_distinct=40, area=A2, prereq=['vh-alg-build'])

skill('vh-alg-simplify', S, 'Redukcja wyrazów podobnych', ['VII-VIII.2.3'],
      [lvl('Jedna zmienna', two=0), lvl('Dwie zmienne', two=1)],
      [('a', 'randint(-6, 6)'), ('b', 'randint(-6, 6)'), ('c', 'randint(-6, 6)'), ('d', 'randint(-6, 6)'), ('e', 'randint(-9, 9)'),
       ('orig', "poly([a, b, c, d, e], ['x', 'y', 'x', 'y', '']) if two == 1 else poly([a, b, c, d, e], ['x', 'x²', 'x', 'x²', ''])"),
       ('v2', "'y' if two == 1 else 'x²'"),
       ('good', "poly([a + c, b + d, e], ['x', v2, ''])"), ('w1', "poly([a - c, b + d, e], ['x', v2, ''])"), ('w2', "poly([a + c, b - d, e], ['x', v2, ''])"),
       ('w3', "poly([a + b + c + d, e], ['x', ''])")],
      choice('Zredukuj wyrazy podobne w wyrażeniu: @{orig}', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Wyrazy podobne mają tę samą część literową (np. wszystkie z x, wszystkie z y). Dodaj ich współczynniki.'), ('conclude', 'Po redukcji: @{good}.')]),
      constraints=['a != 0 and b != 0 and c != 0 and d != 0', 'a + c != 0 and b + d != 0', 'len(uniq([good, w1, w2, w3])) == 4'], min_distinct=40, area=A2, prereq=['vh-alg-build'],
      intro='Wyrazy podobne to jednomiany z taką samą częścią literową, np. 3x i −5x. Dodajemy je, dodając współczynniki: 3x − 5x = −2x.')

skill('vh-alg-addsub', S, 'Dodawanie i odejmowanie sum algebraicznych', ['VII-VIII.2.4'],
      [lvl('Dodawanie', minus=0), lvl('Odejmowanie', minus=1)],
      [('a', 'randint(-5, 6)'), ('b', 'randint(-5, 6)'), ('c', 'randint(-5, 6)'), ('d', 'randint(-5, 6)'), ('e', 'randint(-6, 6)'), ('f', 'randint(-6, 6)'),
       ('s', '1 if minus == 0 else -1'),
       ('txt', "'(' + poly([a, b, e], ['x', 'y', '']) + ') ' + ('+' if minus == 0 else '−') + ' (' + poly([c, d, f], ['x', 'y', '']) + ')'"),
       ('good', "poly([a + s * c, b + s * d, e + s * f], ['x', 'y', ''])"), ('w1', "poly([a + s * c, b + s * d, e - s * f], ['x', 'y', ''])"),
       ('w2', "poly([a - s * c, b - s * d, e + s * f], ['x', 'y', ''])"), ('w3', "poly([a + s * c, b - s * d, e + s * f], ['x', 'y', ''])")],
      choice('Wykonaj działanie: @{txt}', 'good', ['w1', 'w2', 'w3'],
             [('idea', "@{('Opuść nawiasy i zredukuj wyrazy podobne.' if minus == 0 else 'Minus przed nawiasem zmienia znaki wszystkich wyrazów w nawiasie. Potem zredukuj wyrazy podobne.')}"), ('conclude', 'Wynik: @{good}.')]),
      constraints=['a != 0 and b != 0 and c != 0 and d != 0', 'e != 0 and f != 0', 'len(uniq([good, w1, w2, w3])) == 4'], min_distinct=40, area=A2, prereq=['vh-alg-simplify'])

skill('vh-alg-mul-mono', S, 'Mnożenie jednomianu przez sumę', ['VII-VIII.2.5'],
      [lvl('Suma dwóch wyrazów', terms=2), lvl('Suma trzech wyrazów', terms=3)],
      [('k', 'choice([-3, -2, 2, 3, 4])'), ('a', 'randint(-4, 5)'), ('b', 'randint(-4, 5)'), ('c', 'randint(-5, 5)'),
       ('cs', '[a, b, c] if terms == 3 else [a, b, 0]'),
       ('sumtxt', "poly(cs, ['x', 'y', '']) if terms == 3 else poly([a, b], ['x', 'y'])"),
       ('mono', "(str(k) if k > 0 else '(−' + str(abs(k)) + ')') + 'x'"),
       ('good', "poly([k * cs[0], k * cs[1], k * cs[2]], ['x²', 'xy', 'x'])"),
       ('w1', "poly([k * cs[0], cs[1], k * cs[2]], ['x²', 'xy', 'x'])"), ('w2', "poly([cs[0], k * cs[1], k * cs[2]], ['x²', 'xy', 'x'])"),
       ('w3', "poly([k * cs[0], -k * cs[1], k * cs[2]], ['x²', 'xy', 'x'])")],
      choice('Wymnóż: @{mono}(@{sumtxt})', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Mnożymy jednomian przez każdy wyraz w nawiasie osobno: x · x = x², x · y = xy.'), ('conclude', 'Wynik: @{good}.')]),
      constraints=['a != 0 and b != 0', 'terms == 2 or c != 0', 'k != 1 and k != -1', 'len(uniq([good, w1, w2, w3])) == 4'], min_distinct=40, area=A2, prereq=['vh-alg-addsub'])

skill('vh-alg-factor', S, 'Wyłączanie jednomianu przed nawias', ['VII-VIII.2.6'],
      [lvl('Wspólny czynnik liczbowy', kind=0), lvl('Wspólny czynnik z literą', kind=1)],
      [('g', 'randint(2, 6)'), ('p', 'randint(1, 5)'), ('q', 'randint(1, 6) * choice([-1, 1])'),
       ('orig', "poly([g * p, g * q], ['x', '']) if kind == 0 else poly([g * p, g * q], ['x²', 'x'])"),
       ('inner', "poly([p, q], ['x', '']) if kind == 0 else poly([p, q], ['x', ''])"), ('pre', "str(g) if kind == 0 else str(g) + 'x'"),
       ('good', "pre + '(' + inner + ')'"),
       ('w1', "pre + '(' + poly([p, q + 1], ['x', '']) + ')'"), ('w2', "pre + '(' + poly([p, -q], ['x', '']) + ')'"),
       ('w3', "(str(g * p) if kind == 0 else str(g * p) + 'x') + '(' + poly([1, q], ['x', '']) + ')'")],
      choice('Wyłącz wspólny czynnik przed nawias: @{orig}', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Znajdź największy wspólny czynnik obu wyrazów, wyłącz go i w nawiasie zapisz to, co zostaje.'), ('conclude', 'Po wyłączeniu: @{good}. Sprawdzenie: wymnóż i porównaj.')]),
      constraints=['gcd(abs(p), abs(q)) == 1', 'len(uniq([good, w1, w2, w3])) == 4', 'q != 0 and q != -1'], min_distinct=30, area=A2, prereq=['vh-alg-mul-mono'])

skill('vh-alg-binomials', S, 'Mnożenie dwumianów', ['VII-VIII.2.7'],
      [lvl('Współczynnik przy x', ask=0), lvl('Wyraz wolny', ask=1), lvl('Dowolne dwumiany', ask=2)],
      [('a', 'randint(1, 4)'), ('b', 'randint(-6, 6)'), ('c', 'randint(1, 4)'), ('d', 'randint(-6, 6)'),
       ('l', 'poly([a, b], ["x", ""])'), ('r', 'poly([c, d], ["x", ""])'),
       ('ask2', 'randint(0, 2) if ask == 2 else ask'), ('ans', '[a * d + b * c, b * d, a * c][ask2]'),
       ('what', "['współczynnik przy x', 'wyraz wolny (bez x)', 'współczynnik przy x²'][ask2]")],
      number('Po wymnożeniu (@{l})(@{r}) i uporządkowaniu otrzymamy trójmian $ax^2 + bx + c$. Ile wynosi @{what}?', 'ans',
             [('idea', '(ax + b)(cx + d) = acx² + (ad + bc)x + bd. Wymnóż każdy wyraz z każdym.'),
              ('conclude', "Po wymnożeniu: @{poly([a * c, a * d + b * c, b * d], ['x²', 'x', ''])}.")]),
      constraints=['b != 0 and d != 0', 'a * d + b * c != 0'], selfCheck=['a * c * 1 + (a * d + b * c) + b * d == (a + b) * (c + d)'], min_distinct=40, area=A2, prereq=['vh-alg-mul-mono'])

skill('vh-alg-formula', S, 'Przekształcanie wzorów', ['VII-VIII.2.8'],
      [lvl('Jedno działanie', fs='[0, 1, 2]'), lvl('Dwa działania', fs='[3, 4, 5]')],
      [('f', 'choice(fs)'), ('t', 'randint(2, 12)'), ('v', 'randint(2, 15)'), ('a', 'randint(2, 12)'), ('h', 'randint(2, 12)'),
       ('texts', "['Ze wzoru s = v · t wyznacz t i oblicz jego wartość dla s = ' + str(v * t) + ' i v = ' + str(v) + '.', "
                 "'Ze wzoru P = a · h wyznacz h i oblicz jego wartość dla P = ' + str(a * h) + ' i a = ' + str(a) + '.', "
                 "'Ze wzoru V = a · b · c wyznacz c i oblicz jego wartość dla V = ' + str(a * h * t) + ', a = ' + str(a) + ' i b = ' + str(h) + '.', "
                 "'Ze wzoru O = 2a + 2b wyznacz b i oblicz jego wartość dla O = ' + str(2 * a + 2 * h) + ' i a = ' + str(a) + '.', "
                 "'Ze wzoru P = ½ · a · h wyznacz h i oblicz jego wartość dla P = ' + str(a * h) + ' i a = ' + str(2 * a) + '.', "
                 "'Ze wzoru P = ½ · (a + b) · h wyznacz b i oblicz jego wartość dla P = ' + str((a + t) * h) + ', a = ' + str(a) + ' i h = ' + str(2 * h) + '.']"),
       ('ans', '[t, h, t, h, h, t][f]'),
       ('ideas', "['Podziel obie strony wzoru przez v: t = s : v.', 'Podziel obie strony wzoru przez a: h = P : a.', 'Podziel obie strony wzoru przez a · b: c = V : (a · b).', "
                 "'Odejmij 2a od obu stron, potem podziel przez 2: b = (O − 2a) : 2.', 'Pomnóż obie strony przez 2, potem podziel przez a: h = 2P : a.', 'Pomnóż obie strony przez 2, podziel przez h i odejmij a: b = 2P : h − a.']")],
      number('@{texts[f]}', 'ans', [('idea', '@{ideas[f]}'), ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['f != 3 or h != a'], min_distinct=40, area=A2, prereq=['n46-alg-formula'])

# ============================================================================ równania (2.9 - 2.12)
skill('vh-eq-check', S, 'Czy liczba jest rozwiązaniem równania?', ['VII-VIII.2.9', 'VII-VIII.2.10'],
      [lvl('Równanie pierwszego stopnia', f=0), lvl('Równanie drugiego stopnia', f=1), lvl('Równanie trzeciego stopnia', f=2), lvl('Rozwiązanie ułamkowe', f=3)],
      [('r', 'randint(-4, 5)'), ('b', 'randint(-5, 6)'), ('a', 'randint(2, 5)'), ('yes', 'randint(0, 1) == 1'), ('dd', 'choice([-2, -1, 1, 2])'),
       ('t', 'r if yes else r + dd'),
       ('half', 'choice([4, 5, 8, 10])'),
       ('eq', "poly([a, b], ['x', '']) + ' = ' + str(a * r + b) if f == 0 else (poly([1, b], ['x²', 'x']) + ' = ' + str(r * r + b * r) if f == 1 else "
              "(poly([1, b], ['x³', 'x']) + ' = ' + str(r * r * r + b * r) if f == 2 else poly([a * 2, b], ['x', '']) + ' = ' + str(a + b)))"),
       ('cand', "str(t) if f < 3 else ('1/2' if yes else '1/' + str(half))"),
       ('lhs', "a * t + b if f == 0 else (t * t + b * t if f == 1 else (t * t * t + b * t if f == 2 else (a * 2 * (1 / 2) + b if yes else a * 2 * (1 / half) + b)))"),
       ('rhs', "a * r + b if f == 0 else (r * r + b * r if f == 1 else (r * r * r + b * r if f == 2 else a + b))")],
      choice_text('Czy liczba @{cand} jest rozwiązaniem równania @{eq}?', [('Tak', 'lhs == rhs'), ('Nie', 'lhs != rhs')], None,
                  [('idea', 'Podstaw liczbę w miejsce x po obu stronach równania. Jeśli wyniki są równe – to rozwiązanie.'), ('compute', 'Lewa strona: @{lhs|dec}, prawa strona: @{rhs|dec}.')], fixed_order=True),
      constraints=['f == 3 or b != 0', 'f != 2 or abs(r) <= 3', 'f != 1 or r != 0', 'f == 3 or yes or lhs != rhs'], min_distinct=30, area=A2, prereq=['vh-alg-evaluate'])

skill('vh-eq-solve', S, 'Rozwiązywanie równań pierwszego stopnia', ['VII-VIII.2.11'],
      [lvl('Niewiadoma po jednej stronie', f=1), lvl('Nawias lub ułamek', f=2), lvl('Niewiadoma po obu stronach', f=0)],
      [('r', 'randint(-6, 9)'), ('a', 'randint(2, 6)'), ('c', 'randint(1, 5)'), ('b', 'randint(-8, 9)'), ('mult', 'randint(2, 4)'),
       ('d', 'a * r + b - c * r'),
       ('rhs1', 'a * (r + b)'), ('rhs2', 'a * (r - b) + c'), ('q', 'randint(2, 5)'), ('rr', 'q * mult - b'),
       ('eqs', "[poly([a, b], ['x', '']) + ' = ' + poly([c, d], ['x', '']), str(a) + '(x ' + ('+ ' if b >= 0 else '− ') + str(abs(b)) + ') = ' + str(rhs1), "
               "str(a) + '(x ' + ('− ' if b >= 0 else '+ ') + str(abs(b)) + ') ' + ('+ ' if c >= 0 else '− ') + str(abs(c)) + ' = ' + str(rhs2)]"),
       ('hint', "['Przenieś wyrazy z x na jedną stronę, a liczby na drugą, potem podziel przez współczynnik przy x.', 'Opuść nawias (lub podziel obie strony przez ' + str(a) + ') i rozwiąż równanie.', "
                "'Opuść nawias, przenieś liczby na jedną stronę i podziel.']"),
       ('sol', 'r')],
      number('Rozwiąż równanie: $@{eqs[f]}$', 'sol',
             [('idea', '@{hint[f]}'), ('conclude', 'x = @{sol}. Sprawdzenie: podstaw @{sol} do równania.')]),
      constraints=['f != 0 or a != c', 'c != 0', 'b != 0'], selfCheck=['f != 0 or a * r + b == c * r + d', 'f != 1 or a * (r + b) == rhs1', 'f != 2 or a * (r - b) + c == rhs2'],
      min_distinct=40, area=A2, prereq=['vh-eq-check', 'n46-alg-solve'])

skill('vh-eq-solve-frac', S, 'Równania z rozwiązaniem ułamkowym', ['VII-VIII.2.11'],
      [lvl('Jedno działanie', f=0), lvl('Niewiadoma po obu stronach', f=1)],
      [('a', 'randint(2, 7)'), ('b', 'randint(1, 12)'), ('c', 'randint(1, 6)'), ('d', 'randint(-9, 9)'),
       ('sol', 'b / a if f == 0 else (d + 0) / (a + c)'),
       ('eq', "str(a) + 'x = ' + str(b) if f == 0 else poly([a, 0], ['x', '']) + ' = ' + poly([-c, d], ['x', ''])")],
      fraction('Rozwiąż równanie: $@{eq}$. Podaj wynik jako ułamek nieskracalny.', 'numer(sol)', 'denom(sol)',
               [('idea', "@{('Podziel obie strony przez ' + str(a) + '.' if f == 0 else 'Przenieś wyrazy z x na jedną stronę i podziel obie strony przez ' + str(a + c) + '.')}"), ('conclude', 'x = $@{sol|frac}$')]),
      constraints=['denom(sol) != 1', 'f != 1 or d != 0', 'f != 1 or gcd(abs(d), a + c) != abs(a + c)'], min_distinct=25, area=A2, prereq=['vh-eq-solve'])

skill('vh-eq-word', S, 'Zadania tekstowe i równania', ['VII-VIII.2.12'],
      [lvl('Kolejne liczby i obwód', mode=0), lvl('Liczba zagadka', mode=1), lvl('Bilety i monety (dwa równania w jednym)', mode=2)],
      [('n0', 'randint(3, 30)'), ('d', 'randint(2, 9)'), ('k', 'randint(2, 5)'), ('t', 'randint(2, 12)'),
       ('na', 'randint(10, 60)'), ('x', 'randint(3, na - 3)'), ('pa', 'randint(15, 30)'), ('pb', 'randint(5, pa - 5)'), ('sumt', 'x * pa + (na - x) * pb'), ('which', 'randint(0, 1)'),
       ('side', 'randint(2, 12)'), ('per', '2 * (side + side + d)'),
       ('txt', "(('Suma trzech kolejnych liczb naturalnych wynosi ' + str(3 * n0 + 3) + '. Jaka jest najmniejsza z nich?') if which == 0 else "
               "('Obwód prostokąta wynosi ' + str(per) + ' cm, a jeden bok jest o ' + str(d) + ' cm dłuższy od drugiego. Ile centymetrów ma krótszy bok?')) if mode == 0 else "
               "(('Pomyślałem liczbę, pomnożyłem ją przez ' + str(k) + ', odjąłem ' + str(t) + ' i otrzymałem tyle samo, ile gdy do tej liczby dodam ' + str(k * t + t) + '. Jaką liczbę pomyślałem?') if mode == 1 else "
               "('W kinie sprzedano ' + str(na) + ' biletów: normalnych po ' + str(pa) + ' zł i ulgowych po ' + str(pb) + ' zł. Utarg wyniósł ' + str(sumt) + ' zł. Ile sprzedano biletów normalnych?'))"),
       ('ans', '(n0 if which == 0 else side) if mode == 0 else ((k * t + t + t) // (k - 1) if mode == 1 else x)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Oznacz niewiadomą literą x i zapisz warunek zadania jako równanie.' if mode != 2 else 'Niech x będzie liczbą biletów normalnych, wtedy ulgowych jest ' + str(na) + ' − x. Zapisz utarg jako równanie.')}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['mode != 1 or (k * t + t + t) % (k - 1) == 0', 'mode != 2 or pa != pb'], min_distinct=30, area=A2, prereq=['vh-eq-solve'])

# ============================================================================ ścieżka
un = Unit(S, 'vh-u5', 'Wyrażenia algebraiczne', 'Zapisujemy wielkości literami, obliczamy wartości i upraszczamy.', 'algebra', area=A2)
un.learn('vh-alg-build').learn('vh-alg-evaluate').learn('vh-alg-simplify').learn('vh-alg-addsub')
un.checkpoint(['vh-alg-build', 'vh-alg-evaluate', 'vh-alg-simplify', 'vh-alg-addsub'])

un = Unit(S, 'vh-u6', 'Działania na sumach algebraicznych', 'Mnożenie jednomianu przez sumę, wyłączanie przed nawias, mnożenie dwumianów i przekształcanie wzorów.', 'brackets', area=A2)
un.learn('vh-alg-mul-mono').learn('vh-alg-factor').learn('vh-alg-binomials').learn('vh-alg-formula')
un.checkpoint(['vh-alg-mul-mono', 'vh-alg-factor', 'vh-alg-binomials', 'vh-alg-formula'])

un = Unit(S, 'vh-u7', 'Równania', 'Sprawdzamy rozwiązania, rozwiązujemy równania i zadania tekstowe.', 'equation', area=A2)
un.learn('vh-eq-check').learn('vh-eq-solve').learn('vh-eq-solve-frac').learn('vh-eq-word')
un.checkpoint(['vh-eq-check', 'vh-eq-solve', 'vh-eq-solve-frac', 'vh-eq-word'])
