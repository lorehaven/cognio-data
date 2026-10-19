"""Stage I-III, area 1 (Liczby), part 2: regularities, missing numbers, signs, Roman numerals, inverse operations, unit fractions.
Objectives: I-III.1.k, 1.l, 1.m, 1.n, 1.o, 1.p."""
from dsl import *

S = 'I-III'
A1 = 'I-III.1'

skill('ew-pattern-rule', S, 'Odkrywamy prawidłowości', ['I-III.1.k'],
      [lvl('Zamiana miejsc składników', mode=0), lvl('Zmieniamy jeden składnik', mode=1), lvl('Podwajamy czynnik', mode=2), lvl('Zero i jedynka', mode=3)],
      [('a', 'randint(3, 20)'), ('b', 'randint(3, 20)'), ('c', 'randint(2, 9)'), ('d', 'randint(2, 9)'),
       ('txt', "('Wiesz, że ' + str(a) + ' + ' + str(b) + ' = ' + str(a + b) + '. Ile wynosi ' + str(b) + ' + ' + str(a) + '?') if mode == 0 else "
               "(('Wiesz, że ' + str(a) + ' + ' + str(b) + ' = ' + str(a + b) + '. Ile wynosi ' + str(a) + ' + ' + str(b + 1) + '?') if mode == 1 else "
               "(('Wiesz, że ' + str(c) + ' · ' + str(d) + ' = ' + str(c * d) + '. Ile wynosi ' + str(2 * c) + ' · ' + str(d) + '?') if mode == 2 else "
               "('Ile wynosi ' + str(a) + ' · 1 + ' + str(b) + ' · 0?')))"),
       ('ans', 'a + b if mode == 0 else (a + b + 1 if mode == 1 else (2 * c * d if mode == 2 else a))')],
      number('@{txt}', 'ans',
             [('idea', "@{('Dodawanie można wykonać w dowolnej kolejności.' if mode == 0 else ('Gdy jeden składnik rośnie o 1, suma też rośnie o 1.' if mode == 1 else ('Gdy jeden czynnik podwajamy, iloczyn też się podwaja.' if mode == 2 else 'Mnożenie przez 1 nic nie zmienia, a przez 0 daje zero.')))}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['a != b', 'c != d'], min_distinct=20, area=A1, prereq=['ew-add', 'ew-mul-table'])

skill('ew-missing', S, 'Brakująca liczba', ['I-III.1.l'],
      [lvl('Dodawanie i odejmowanie do 20', ops='[0, 1]', hi=20), lvl('Dodawanie i odejmowanie do 100', ops='[0, 1]', hi=100),
       lvl('Mnożenie i dzielenie', ops='[2, 3]', hi=10), lvl('Wszystkie działania', ops='[0, 1, 2, 3]', hi=10)],
      [('op', 'choice(ops)'), ('a', 'randint(2, hi)'), ('b', 'randint(2, hi)'), ('pos', 'randint(0, 1)'), ('i', 'pos + 2 * (op % 2)'),
       ('big', 'a + b'), ('prod', 'a * b'),
       ('eq1', "[str(a) + ' + □ = ' + str(big), '□ + ' + str(b) + ' = ' + str(big), str(big) + ' − □ = ' + str(a), '□ − ' + str(b) + ' = ' + str(a)]"),
       ('eq2', "[str(a) + ' · □ = ' + str(prod), '□ · ' + str(b) + ' = ' + str(prod), str(prod) + ' : □ = ' + str(a), '□ : ' + str(b) + ' = ' + str(a)]"),
       ('an1', '[b, a, b, big]'), ('an2', '[b, a, b, prod]'),
       ('text', 'eq1[i] if op < 2 else eq2[i]'), ('ans', 'an1[i] if op < 2 else an2[i]')],
      number('Jaka liczba pasuje w miejsce kwadratu? @{text}', 'ans',
             [('idea', 'Użyj działania odwrotnego do znalezienia brakującej liczby.'), ('conclude', 'Brakuje liczby @{ans}.')]),
      constraints=['op >= 2 or big <= hi', 'op < 2 or (a >= 2 and b >= 2)', 'op != 2 or a != b'], min_distinct=20, area=A1, prereq=['ew-add', 'ew-sub'])

skill('ew-compare-expr', S, 'Znaki <, > i =', ['I-III.1.m'],
      [lvl('Dodawanie', kind=0), lvl('Dodawanie i odejmowanie', kind=1), lvl('Z mnożeniem', kind=2)],
      [('a', 'randint(2, 12)'), ('b', 'randint(2, 12)'), ('c', 'randint(2, 12)'), ('d', 'randint(2, 12)'),
       ('l', 'a * 2 if kind == 2 else a + b'), ('r', 'c - d if kind == 1 else c + d'),
       ('lt', "str(a) + ' · 2' if kind == 2 else str(a) + ' + ' + str(b)"), ('rt', "str(c) + ' − ' + str(d) if kind == 1 else str(c) + ' + ' + str(d)")],
      choice_text('Wstaw odpowiedni znak między wyrażenia: @{lt} … @{rt}.',
                  [(r'$<$', 'l < r'), (r'$=$', 'l == r'), (r'$>$', 'l > r')], None,
                  [('idea', 'Oblicz wartość każdego wyrażenia i porównaj wyniki.'), ('compute', "@{l} @{('<' if l < r else ('=' if l == r else '>'))} @{r}")], fixed_order=True),
      constraints=['kind != 1 or c > d'], min_distinct=30, area=A1, prereq=['ew-compare'])

skill('ew-roman', S, 'Zapisz liczbę po rzymsku', ['I-III.1.n'],
      [lvl('Liczby od 1 do 12')],
      [('n', 'randint(1, 12)')],
      choice('Którym zapisem rzymskim przedstawimy liczbę @{n}?', 'roman(n)', ['roman(n % 12 + 1)', 'roman((n + 2) % 12 + 1)', 'roman((n + 4) % 12 + 1)'],
             [('idea', 'I = 1, V = 5, X = 10. Gdy mniejsza cyfra stoi przed większą, odejmujemy (IV = 4, IX = 9).'), ('conclude', '@{n} = @{roman(n)}')]),
      min_distinct=12, area=A1, prereq=['ew-roman-read'])

skill('ew-roman-read', S, 'Przeczytaj liczbę rzymską', ['I-III.1.n'],
      [lvl('Na tarczy zegara')],
      [('n', 'randint(1, 12)'), ('rom', 'roman(n)')],
      number('Na tarczy zegara napisano @{rom}. Jaka to liczba?', 'n',
             [('idea', 'I = 1, V = 5, X = 10. Gdy mniejsza cyfra stoi przed większą, odejmujemy (IV = 4, IX = 9).'), ('conclude', '@{rom} = @{n}')]),
      min_distinct=12, area=A1)

skill('ew-inverse-check', S, 'Sprawdzamy działaniem odwrotnym', ['I-III.1.o'],
      [lvl('Dodawanie i odejmowanie', mode=0), lvl('Mnożenie i dzielenie', mode=1)],
      [('a', 'randint(5, 40)'), ('b', 'randint(5, 40)'), ('c', 'randint(3, 9)'), ('d', 'randint(3, 9)'), ('which', 'randint(0, 1)'),
       ('txt', "('Wiesz, że ' + str(a) + ' + ' + str(b) + ' = ' + str(a + b) + '. Ile wynosi ' + str(a + b) + ' − ' + str(b) + '?') if mode == 0 and which == 0 else "
               "(('Wiesz, że ' + str(a + b) + ' − ' + str(b) + ' = ' + str(a) + '. Ile wynosi ' + str(a) + ' + ' + str(b) + '?') if mode == 0 else "
               "(('Wiesz, że ' + str(c) + ' · ' + str(d) + ' = ' + str(c * d) + '. Ile wynosi ' + str(c * d) + ' : ' + str(d) + '?') if which == 0 else "
               "('Wiesz, że ' + str(c * d) + ' : ' + str(d) + ' = ' + str(c) + '. Ile wynosi ' + str(c) + ' · ' + str(d) + '?')))"),
       ('ans', '(a if which == 0 else a + b) if mode == 0 else (c if which == 0 else c * d)')],
      number('@{txt}', 'ans',
             [('idea', 'Dodawanie i odejmowanie są działaniami odwrotnymi, tak samo jak mnożenie i dzielenie.'), ('conclude', 'Odpowiedź: @{ans}.')]),
      min_distinct=25, area=A1, prereq=['ew-sub'])

skill('ew-unit-fraction-name', S, 'Ułamki o liczniku 1', ['I-III.1.p'],
      [lvl('Połowa, trzecia i czwarta część', ds='[2, 3, 4]'), lvl('Także piąta i ósma część', ds='[2, 3, 4, 5, 8]')],
      [('pool', '[2, 3, 4, 5, 8]'), ('d', 'choice(ds)'), ('idx', 'index(pool, d)'),
       ('names', "['połowa', 'jedna trzecia', 'jedna czwarta', 'jedna piąta', 'jedna ósma']"),
       ('ts', "['$\\\\frac{1}{2}$', '$\\\\frac{1}{3}$', '$\\\\frac{1}{4}$', '$\\\\frac{1}{5}$', '$\\\\frac{1}{8}$']"),
       ('shape', "choice(['Pizzę', 'Tabliczkę czekolady', 'Tort', 'Pasek papieru'])"), ('eqp', "'równe' if d in [2, 3, 4] else 'równych'")],
      choice('@{shape} podzielono na @{d} @{eqp} części. Jaką częścią całości jest jedna z tych części?', 'ts[idx]', ['ts[(idx + 1) % 5]', 'ts[(idx + 2) % 5]', 'ts[(idx + 3) % 5]'],
             [('idea', 'Całość podzielono na równe części. Jedna część z @{d} to ułamek o mianowniku @{d}.'), ('conclude', '@{names[idx]} = @{ts[idx]}')],
             media=[{'type': 'figure', 'kind': 'fraction-bar', 'essential': False, 'alt': 'Figura podzielona na równe części, jedna zacieniowana.', 'params': {'parts': E('d'), 'shaded': 1}}]),
      min_distinct=5, area=A1)

skill('ew-unit-fraction-of', S, 'Połowa, trzecia, czwarta część liczby', ['I-III.1.p'],
      [lvl('Połowa i czwarta część', ds='[2, 4]'), lvl('Trzecia, piąta i ósma część', ds='[2, 3, 4, 5, 8]')],
      [('pool', '[2, 3, 4, 5, 8]'), ('d', 'choice(ds)'), ('idx', 'index(pool, d)'), ('q', 'randint(2, 12)'), ('n', 'd * q'),
       ('nm', "['połowa', 'jedna trzecia', 'jedna czwarta', 'jedna piąta', 'jedna ósma']")],
      number('Ile wynosi @{nm[idx]} liczby @{n}?', 'q',
             [('idea', 'Podziel liczbę przez @{d}.'), ('compute', '@{n} : @{d} = @{q}')]),
      constraints=['n <= 100'], min_distinct=20, area=A1, prereq=['ew-div-table'])

# ============================================================================ ścieżka (liczby)
un = Unit(S, 'ew-u1', 'Liczby i ich zapis', 'Czytamy, zapisujemy, porównujemy i układamy liczby.', 'numbers', area=A1)
un.learn('ew-write-number').learn('ew-place-value').learn('ew-compare').learn('ew-order')
un.review('Powtórka: liczby', ['ew-write-number', 'ew-place-value', 'ew-compare', 'ew-order'])
un.learn('ew-odd-even').learn('ew-skip-count').learn('ew-number-line-diff').learn('ew-number-line-read')
un.checkpoint(['ew-write-number', 'ew-place-value', 'ew-compare', 'ew-order', 'ew-odd-even', 'ew-skip-count'])

un = Unit(S, 'ew-u2', 'Dodawanie i odejmowanie', 'Rachunki w pamięci, także z przejściem przez dziesiątkę.', 'plusminus', area=A1)
un.learn('ew-add').learn('ew-sub').review('Powtórka: dodawanie i odejmowanie', ['ew-add', 'ew-sub'])
un.learn('ew-strategy').learn('ew-missing').learn('ew-inverse-check')
un.checkpoint(['ew-add', 'ew-sub', 'ew-strategy', 'ew-missing', 'ew-inverse-check'])

un = Unit(S, 'ew-u3', 'Mnożenie i dzielenie', 'Tabliczka mnożenia i dzielenie jako podział i mieszczenie.', 'timesdiv', area=A1)
un.learn('ew-mul-table').learn('ew-div-table').learn('ew-div-meaning').learn('ew-div-share-or-fit')
un.review('Powtórka: mnożenie i dzielenie', ['ew-mul-table', 'ew-div-table', 'ew-div-meaning'])
un.learn('ew-mul-two-digit').learn('ew-div-two-digit').learn('ew-pattern-rule')
un.checkpoint(['ew-mul-table', 'ew-div-table', 'ew-div-meaning', 'ew-mul-two-digit', 'ew-div-two-digit'])

un = Unit(S, 'ew-u4', 'Znaki, liczby rzymskie i ułamki', 'Porównujemy wyrażenia, czytamy liczby rzymskie i poznajemy połowę, trzecią i czwartą część.', 'fractions', area=A1)
un.learn('ew-compare-expr').learn('ew-roman-read').learn('ew-roman').learn('ew-unit-fraction-name').learn('ew-unit-fraction-of')
un.checkpoint(['ew-compare-expr', 'ew-roman-read', 'ew-roman', 'ew-unit-fraction-name', 'ew-unit-fraction-of'])
