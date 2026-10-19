"""Stage VII-VIII, area 1 (Liczby).  Objectives: VII-VIII.1.1 - 1.12."""
from dsl import *

S = 'VII-VIII'
A1 = 'VII-VIII.1'
FIN = ('finance', 'no-calculator')

# ============================================================================ procenty (1.1, 1.2)
skill('vh-percent-what', S, 'Jakim procentem jednej liczby jest druga?', ['VII-VIII.1.1.a'],
      [lvl('Wyniki okrągłe', ps='[10, 20, 25, 40, 50, 60, 75, 80]'), lvl('Dowolne procenty', ps='[5, 12, 15, 24, 35, 45, 48, 64, 85]')],
      [('p', 'choice(ps)'), ('step', '100 // gcd(p, 100)'), ('b', 'step * randint(2, 12)'), ('a', 'b * p / 100'), ('c', 'randint(0, 2)'),
       ('lit', "['litr', 'litry', 'litrów']"), ('pg', "['strona', 'strony', 'stron']"), ('kr', "['kredka', 'kredki', 'kredek']"),
       ('txts', "['Zbiornik pomieści ' + pln(b, lit) + '. Jest w nim ' + pln(a, lit) + ' wody. Na ile procent jest napełniony?', "
                "'Książka ma ' + pln(b, pg) + '. Ola przeczytała ' + pln(a, pg) + '. Jaki procent książki przeczytała?', "
                "'W pudełku jest ' + pln(b, kr) + '. Czerwonych jest ' + str(a) + '. Jaki procent kredek jest czerwonych?']")],
      number('@{txts[c]}', 'p',
             [('idea', 'Procent to część ze 100. Podziel część przez całość i pomnóż przez 100%.'), ('compute', '@{a} : @{b} · 100% = @{p}%')],
             errors=[('inverse', Int('100 - p'), 'Zadanie pyta o część, a nie o resztę.', 'p != 50')]),
      constraints=['denom(a) == 1', 'a < b'], selfCheck=['a * 100 == p * b'], min_distinct=40, area=A1,
      intro='Procent to setna część całości. Żeby sprawdzić, jakim procentem liczby b jest liczba a, dzielimy a przez b i mnożymy przez 100%.')

skill('vh-percent-of', S, 'Procent danej liczby', ['VII-VIII.1.1.b'],
      [lvl('Procenty okrągłe', ps='[10, 20, 25, 50, 75]'), lvl('Dowolne procenty', ps='[3, 8, 12, 15, 35, 45, 120]')],
      [('p', 'choice(ps)'), ('b', 'randint(20, 500)'), ('r', 'b * p / 100')],
      decimal('Oblicz @{p}% liczby @{b}.', 'r',
              [('idea', '@{p}% liczby to $\\frac{@{p}}{100}$ tej liczby.'), ('compute', '@{p} · @{b} : 100 = @{r|dec}')],
              errors=[('divide_by_p', Dec('b / p'), 'Procent to ułamek o mianowniku 100 – nie dzielimy przez liczbę procentów.', 'b / p != r')]),
      selfCheck=['r * 100 == b * p'], min_distinct=40, area=A1, prereq=['vh-percent-what'])

skill('vh-percent-number', S, 'Liczba, gdy znamy jej procent', ['VII-VIII.1.1.c'],
      [lvl('Procenty okrągłe', ps='[10, 20, 25, 50]'), lvl('Dowolne procenty', ps='[5, 15, 30, 35, 40, 60, 120]')],
      [('p', 'choice(ps)'), ('b', '(100 // gcd(p, 100)) * randint(2, 30)'), ('a', 'b * p / 100')],
      number('@{p}% pewnej liczby to @{a}. Jaka to liczba?', 'b',
             [('idea', 'Policz, ile wynosi 1% (podziel przez @{p}), a potem pomnóż przez 100.'), ('compute', '@{a} : @{p} · 100 = @{b}')],
             errors=[('percent_of', Int('a * p // 100') , 'Znamy część, a szukamy całości. Podziel część przez liczbę procentów i pomnóż przez 100.', 'a * p % 100 == 0 and a * p // 100 != b')]),
      constraints=['denom(a) == 1'], selfCheck=['a * 100 == b * p'], min_distinct=40, area=A1, prereq=['vh-percent-of'])

skill('vh-price-change', S, 'Podwyżki i obniżki', ['VII-VIII.1.2'],
      [lvl('Cena po jednej zmianie', mode=0), lvl('Cena początkowa', mode=1), lvl('Dwie zmiany po sobie', mode=2)],
      [('p', 'choice([10, 15, 20, 25, 30, 40, 50])'), ('q', 'choice([10, 20, 25, 50])'), ('up', 'randint(0, 1) == 1'), ('up2', 'randint(0, 1) == 1'),
       ('price0', '20 * randint(2, 30)'),
       ('f', '(100 + p) / 100 if up else (100 - p) / 100'), ('price1', 'price0 * f'),
       ('g', '(100 + q) / 100 if up2 else (100 - q) / 100'), ('price2', 'price1 * g'),
       ('word', "'podniesiono' if up else 'obniżono'"), ('word2', "'podniesiono' if up2 else 'obniżono'"),
       ('txt', "('Cenę kurtki, która kosztowała ' + str(price0) + ' zł, ' + word + ' o ' + str(p) + '%. Ile kosztuje teraz?') if mode == 0 else "
               "(('Po ' + ('podwyżce' if up else 'obniżce') + ' o ' + str(p) + '% kurtka kosztuje ' + fmt(price1, 2) + ' zł. Ile kosztowała przed zmianą?') if mode == 1 else "
               "('Cenę kurtki, która kosztowała ' + str(price0) + ' zł, najpierw ' + word + ' o ' + str(p) + '%, a potem ' + word2 + ' o ' + str(q) + '%. Ile kosztuje na końcu?'))"),
       ('ans', 'price1 if mode == 0 else (price0 if mode == 1 else price2)')],
      quantity('@{txt}', 'ans', 'zł',
               [('idea', "@{('Mnożymy cenę przez współczynnik ' + fmt(f) + ': ' + ('podwyżka o p% to mnożenie przez 1 + p/100' if up else 'obniżka o p% to mnożenie przez 1 − p/100') + '.' if mode == 0 else ('Cena po zmianie to ' + fmt(f) + ' ceny początkowej, więc początkową znajdziemy dzieląc.' if mode == 1 else 'Każdą zmianę liczymy od ceny po poprzedniej zmianie.'))}"),
                ('compute', 'Odpowiedź: @{ans|dec:2} zł.')], decimals=2,
               errors=[('wrong_direction', Qty('price0 * (100 - p) / 100 if up else price0 * (100 + p) / 100', 'zł'), 'Sprawdź, czy cena rośnie (podwyżka), czy maleje (obniżka).', 'mode == 0'),
                       ('apply_to_new', Qty('price1 * f', 'zł'), 'Procent liczymy od ceny przed zmianą, nie po zmianie – tutaj cofamy się do ceny początkowej, więc dzielimy.', 'mode == 1')]),
      constraints=['denom(price1) in divisors(100)', 'denom(price2) in divisors(100)', 'mode != 2 or price2 != price0'], tags=FIN, min_distinct=40, area=A1, prereq=['vh-percent-of'])

skill('vh-interest', S, 'Odsetki, podatek i prowizja', ['VII-VIII.1.2'],
      [lvl('Lokata roczna', mode=0), lvl('Podatek VAT', mode=1), lvl('Prowizja od kredytu', mode=2)],
      [('cap', '100 * randint(5, 100)'), ('rate', 'choice([2, 3, 4, 5, 6, 8])'), ('tax', 'choice([8, 19, 23])'), ('net', '100 * randint(5, 200)'), ('fee', 'choice([2, 3, 5])'),
       ('txt', "('Wpłacasz ' + fmt(cap) + ' zł na lokatę roczną oprocentowaną ' + str(rate) + '% w skali roku. Ile złotych odsetek otrzymasz po roku (bez podatku)?') if mode == 0 else "
               "(('Cena towaru bez podatku wynosi ' + fmt(net) + ' zł. Podatek VAT to ' + str(tax) + '%. Ile złotych wynosi podatek?') if mode == 1 else "
               "('Pożyczasz ' + fmt(cap) + ' zł. Bank pobiera prowizję ' + str(fee) + '% pożyczonej kwoty. Ile złotych wynosi prowizja?'))"),
       ('ans', 'cap * rate / 100 if mode == 0 else (net * tax / 100 if mode == 1 else cap * fee / 100)')],
      quantity('@{txt}', 'ans', 'zł', [('idea', 'Odsetki, podatek i prowizja to procent pewnej kwoty: pomnóż kwotę przez p/100.'), ('compute', 'Odpowiedź: @{ans|dec:2} zł.')], decimals=2),
      constraints=['denom(ans) in divisors(100)'], tags=FIN, min_distinct=40, area=A1, prereq=['vh-percent-of'])

# ============================================================================ potęgi (1.3 - 1.6)
skill('vh-power-calc', S, 'Potęgi liczb całkowitych i ułamków', ['VII-VIII.1.3'],
      [lvl('Podstawa całkowita', kind=0), lvl('Podstawa ułamkowa', kind=1)],
      [('e', 'randint(2, 4)'), ('bi', 'randint(2, 6) * choice([-1, 1])'), ('bn', 'randint(1, 4)'), ('bd', 'randint(2, 5)'), ('neg', 'choice([-1, 1])'),
       ('base', 'bi if kind == 0 else neg * bn / bd'), ('v', 'pow(base, e)'),
       ('bt', "('(' + str(bi) + ')' if bi < 0 else str(bi)) if kind == 0 else ('\\\\left(' + ('-' if neg < 0 else '') + '\\\\frac{' + str(bn) + '}{' + str(bd) + '}\\\\right)')")],
      fraction('Oblicz: $@{bt}^{@{e}}$', 'numer(v)', 'denom(v)',
               [('idea', 'Potęga to wielokrotne mnożenie podstawy. Podstawa ujemna: wykładnik parzysty daje wynik dodatni, nieparzysty – ujemny.'), ('conclude', 'Wynik: $@{v|frac}$')],
               errors=[('sign', Rat('-numer(v)', 'denom(v)', False), 'Sprawdź znak: parzysta liczba minusów daje plus.', 'base < 0')]),
      constraints=['kind == 1 or abs(bi) != 1', 'kind == 0 or gcd(bn, bd) == 1'], min_distinct=30, area=A1)

skill('vh-power-decimal', S, 'Potęgi ułamków dziesiętnych', ['VII-VIII.1.3'],
      [lvl('Kwadraty i sześciany', emax=3), lvl('Czwarta potęga', emax=4)],
      [('e', 'randint(2, emax)'), ('d', 'randint(1, 9)'), ('neg', 'choice([-1, 1])'), ('base', 'neg * d / 10'), ('v', 'pow(base, e)'),
       ('bt', "('(-0{,}' + str(d) + ')') if neg < 0 else ('0{,}' + str(d))")],
      decimal('Oblicz: $@{bt}^{@{e}}$', 'v',
              [('idea', 'Pomnóż podstawę przez siebie @{e} razy; liczba miejsc po przecinku w wyniku to @{e} razy liczba miejsc w podstawie.'), ('conclude', 'Wynik: @{v|dec}')]),
      constraints=['d != 0'], min_distinct=15, area=A1, prereq=['vh-power-calc'])

skill('vh-power-negative', S, 'Potęgi o wykładniku ujemnym', ['VII-VIII.1.4'],
      [lvl('Podstawa całkowita', kind=0), lvl('Podstawa ułamkowa', kind=1)],
      [('e', 'randint(1, 4)'), ('b', 'randint(2, 5)'), ('bn', 'randint(1, 4)'), ('bd', 'randint(2, 5)'), ('base', 'b if kind == 0 else bn / bd'), ('v', 'pow(base, -e)'),
       ('bt', "str(b) if kind == 0 else '\\\\left(\\\\frac{' + str(bn) + '}{' + str(bd) + '}\\\\right)'")],
      fraction('Oblicz: $@{bt}^{-@{e}}$', 'numer(v)', 'denom(v)',
               [('idea', 'Potęga o wykładniku ujemnym to odwrotność potęgi o wykładniku dodatnim: $a^{-n} = \\frac{1}{a^n}$.'), ('conclude', 'Wynik: $@{v|frac}$')],
               errors=[('negative_result', Rat('-numer(v)', 'denom(v)', False), 'Ujemny wykładnik nie zmienia znaku liczby – odwracamy ułamek.')]),
      constraints=['kind == 0 or (gcd(bn, bd) == 1 and bn != 1)'], min_distinct=16, area=A1, prereq=['vh-power-calc'],
      intro='Wykładnik ujemny oznacza odwrotność: $a^{-n} = \\frac{1}{a^n}$, a $\\left(\\frac{a}{b}\\right)^{-n} = \\left(\\frac{b}{a}\\right)^n$.')

skill('vh-power-laws', S, 'Działania na potęgach', ['VII-VIII.1.5'],
      [lvl('Ta sama podstawa', mode=0), lvl('Ten sam wykładnik', mode=1), lvl('Potęga potęgi', mode=2), lvl('Mieszane, z wykładnikami ujemnymi', mode=3)],
      [('b', 'randint(2, 9)'), ('b2', 'randint(2, 9)'), ('m', 'randint(2, 9)'), ('n', 'randint(2, 9)'), ('mm', 'choice([0, 1, 2]) if mode == 3 else 0'),
       ('sg1', 'm if mode != 3 else -m'),
       ('txt', "('$' + str(b) + '^{' + str(m) + '} \\\\cdot ' + str(b) + '^{' + str(n) + '} = ' + str(b) + '^{?}$') if mode == 0 else "
               "(('$' + str(b) + '^{' + str(m) + '} \\\\cdot ' + str(b2) + '^{' + str(m) + '} = (?)^{' + str(m) + '}$') if mode == 1 else "
               "(('$\\\\left(' + str(b) + '^{' + str(m) + '}\\\\right)^{' + str(n) + '} = ' + str(b) + '^{?}$') if mode == 2 else "
               "('$' + str(b) + '^{' + str(sg1) + '} \\\\cdot ' + str(b) + '^{' + str(n) + '} : ' + str(b) + '^{' + str(m + 1) + '} = ' + str(b) + '^{?}$')))"),
       ('ans', 'm + n if mode == 0 else (b * b2 if mode == 1 else (m * n if mode == 2 else sg1 + n - (m + 1)))')],
      number('Uzupełnij wykładnik lub podstawę (zamiast „?”): @{txt}', 'ans',
             [('idea', "@{('Mnożenie potęg o tej samej podstawie: wykładniki dodajemy.' if mode == 0 else ('Mnożenie potęg o tym samym wykładniku: mnożymy podstawy.' if mode == 1 else ('Potęga potęgi: wykładniki mnożymy.' if mode == 2 else 'Mnożąc potęgi dodajemy wykładniki, dzieląc – odejmujemy.')))}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['mode != 1 or b != b2'], min_distinct=40, area=A1, prereq=['vh-power-negative'])

skill('vh-sci-exponent', S, 'Notacja wykładnicza: wykładnik', ['VII-VIII.1.6'],
      [lvl('Duże liczby', big=1), lvl('Małe liczby', big=0)],
      [('a', 'randint(11, 99) / 10'), ('k', 'randint(3, 9)'),
       ('vtxt', "fmt(a * pow(10, k)) if big == 1 else '0,' + join(repeat(0, k - 1), '') + str(a * 10)")],
      number('Zapisz liczbę @{vtxt} w postaci $a \\cdot 10^{k}$, gdzie $1 \\leq a < 10$. Podaj wykładnik k.', 'k if big == 1 else -k',
             [('idea', 'Przesuwaj przecinek tak, aby przed nim została jedna cyfra różna od zera. Liczba przesunięć to wykładnik (dla małych liczb – ujemny).'),
              ('conclude', "Zapis: @{a|dec} · 10^@{(str(k) if big == 1 else '−' + str(k))}.")]),
      selfCheck=['a >= 1 and a < 10'], min_distinct=30, area=A1, prereq=['vh-power-negative'])

skill('vh-sci-compare', S, 'Notacja wykładnicza: która liczba jest większa?', ['VII-VIII.1.6'],
      [lvl('Ten sam wykładnik', same=1), lvl('Różne wykładniki', same=0)],
      [('a1', 'randint(11, 99) / 10'), ('a2', 'randint(11, 99) / 10'), ('k1', 'randint(2, 8)'), ('k2', 'k1 if same == 1 else randint(2, 8)'),
       ('v1', 'a1 * pow(10, k1)'), ('v2', 'a2 * pow(10, k2)')],
      choice_text('Która liczba jest większa: $@{a1|dec} \\cdot 10^{@{k1}}$ czy $@{a2|dec} \\cdot 10^{@{k2}}$?',
                  [('$@{a1|dec} \\cdot 10^{@{k1}}$', 'v1 > v2'), ('$@{a2|dec} \\cdot 10^{@{k2}}$', 'v2 > v1')], None,
                  [('idea', 'Najpierw porównaj wykładniki potęgi dziesięciu: większy wykładnik oznacza (przy a od 1 do 10) większą liczbę. Przy równych wykładnikach porównaj współczynniki.'),
                   ('conclude', 'Większa jest ta z większą wartością: @{max([v1, v2])|int}.')], fixed_order=True),
      constraints=['v1 != v2', 'same == 1 or k1 != k2'], min_distinct=40, area=A1, prereq=['vh-sci-exponent'])

# ============================================================================ pierwiastki (1.7 - 1.9)
skill('vh-sqrt-exact', S, 'Pierwiastki z kwadratów i sześcianów', ['VII-VIII.1.7'],
      [lvl('Kwadraty liczb naturalnych', md=14, mode=0), lvl('Sześciany liczb całkowitych i ułamków', md=20, mode=1), lvl('Ułamki', md=20, mode=2)],
      [('a', 'randint(2, 15)'), ('b', 'randint(2, 9)'), ('c', 'randint(2, 10)'), ('d', 'randint(2, 5)'), ('sg', 'choice([1, -1])'), ('fr', 'randint(0, 1)'),
       ('txt', "('\\\\sqrt{' + str(pow(a, 2)) + '}') if mode == 0 else "
               "((('\\\\sqrt[3]{' + str(sg * pow(c, 3)) + '}') if fr == 0 else ('\\\\sqrt[3]{\\\\frac{' + str(pow(c, 3)) + '}{' + str(pow(d, 3)) + '}}')) if mode == 1 else "
               "'\\\\sqrt{\\\\frac{' + str(pow(b, 2)) + '}{' + str(pow(a, 2)) + '}}')"),
       ('v', 'a if mode == 0 else ((sg * c if fr == 0 else c / d) if mode == 1 else b / a)')],
      fraction('Oblicz: $@{txt}$', 'numer(v)', 'denom(v)',
               [('idea', "@{('Szukamy liczby, której kwadrat jest równy liczbie pod pierwiastkiem.' if mode != 1 else 'Szukamy liczby, której sześcian jest równy liczbie pod pierwiastkiem (może być ujemna).')}"), ('conclude', 'Wynik: $@{v|frac}$')]),
      constraints=['mode != 2 or (gcd(a, b) == 1 and a != b)', 'mode != 1 or fr == 0 or (gcd(c, d) == 1 and c != d)'], min_distinct=14, area=A1,
      intro='Pierwiastek kwadratowy z liczby a to nieujemna liczba, której kwadrat wynosi a. Pierwiastek sześcienny to liczba, której sześcian wynosi a (z liczby ujemnej też można go obliczyć).')

skill('vh-sqrt-between', S, 'Między którymi liczbami całkowitymi leży pierwiastek?', ['VII-VIII.1.8'],
      [lvl('Pierwiastki kwadratowe', cube=0), lvl('Pierwiastki sześcienne', cube=1)],
      [('lo', 'randint(2, 12) if cube == 0 else randint(2, 6)'), ('n', 'randint(lo * lo + 1, (lo + 1) * (lo + 1) - 1) if cube == 0 else randint(pow(lo, 3) + 1, pow(lo + 1, 3) - 1)'),
       ('txt', "'\\\\sqrt{' + str(n) + '}' if cube == 0 else '\\\\sqrt[3]{' + str(n) + '}'")],
      choice_text('Między którymi kolejnymi liczbami całkowitymi leży liczba $@{txt}$?',
                  [('@{lo} i @{lo + 1}', 'true'), ('@{lo + 1} i @{lo + 2}', 'false'), ('@{lo - 1} i @{lo}', 'false'), ('@{lo + 2} i @{lo + 3}', 'false')], None,
                  [('idea', 'Znajdź największy kwadrat (sześcian) mniejszy niż @{n} i najmniejszy większy niż @{n}.'),
                   ('compute', "@{(str(lo * lo) + ' < ' + str(n) + ' < ' + str((lo + 1) * (lo + 1)) if cube == 0 else str(pow(lo, 3)) + ' < ' + str(n) + ' < ' + str(pow(lo + 1, 3)))}")]),
      constraints=['lo > 1'], min_distinct=30, area=A1, prereq=['vh-sqrt-exact'])

skill('vh-sqrt-approx', S, 'Przybliżone wartości pierwiastków (kalkulator)', ['VII-VIII.1.7', 'VII-VIII.1.12'],
      [lvl('Pierwiastek kwadratowy, do części dziesiątych', cube=0, k=1), lvl('Pierwiastek kwadratowy, do części setnych', cube=0, k=2), lvl('Pierwiastek sześcienny, do części setnych', cube=1, k=2)],
      [('n', 'randint(2, 80) if cube == 0 else randint(2, 60)'), ('v', 'sqrt_dec(n, k) if cube == 0 else cbrt_dec(n, k)'),
       ('txt', "'\\\\sqrt{' + str(n) + '}' if cube == 0 else '\\\\sqrt[3]{' + str(n) + '}'")],
      decimal('Za pomocą kalkulatora oblicz przybliżoną wartość liczby $@{txt}$ i zaokrąglij ją do @{(\'części dziesiątych\' if k == 1 else \'części setnych\')}.', 'v',
              [('idea', 'Wpisz pierwiastek w kalkulator, odczytaj wynik i zaokrąglij: 0–4 zostawiamy, 5–9 zwiększamy.'), ('conclude', '$@{txt} \\approx @{v|dec:k}$')]),
      constraints=['cube == 1 or not is_square(n)', 'cube == 0 or pow(icbrt(n), 3) != n'], tags=('calculator-allowed',), min_distinct=40, area=A1, prereq=['vh-sqrt-between'])

skill('vh-root-factor', S, 'Wyłączanie liczby przed znak pierwiastka', ['VII-VIII.1.9.c'],
      [lvl('Pierwiastek kwadratowy')],
      [('a', 'randint(2, 9)'), ('r', 'choice([2, 3, 5, 6, 7])'), ('n', 'a * a * r')],
      number('Zapisz $\\sqrt{@{n}}$ w postaci $a\\sqrt{@{r}}$. Ile wynosi a?', 'a',
             [('idea', 'Rozłóż liczbę pod pierwiastkiem na iloczyn kwadratu liczby naturalnej i innej liczby: @{n} = @{a * a} · @{r}.'), ('conclude', '$\\sqrt{@{n}} = \\sqrt{@{a * a}} \\cdot \\sqrt{@{r}} = @{a}\\sqrt{@{r}}$')]),
      constraints=['n < 400'], min_distinct=20, area=A1, prereq=['vh-sqrt-exact'])

skill('vh-root-bring-in', S, 'Włączanie liczby pod znak pierwiastka', ['VII-VIII.1.9.c'],
      [lvl('Pierwiastek kwadratowy')],
      [('a', 'randint(2, 9)'), ('r', 'choice([2, 3, 5, 6, 7])')],
      number('Zapisz $@{a}\\sqrt{@{r}}$ w postaci $\\sqrt{n}$. Ile wynosi n?', 'a * a * r',
             [('idea', 'Liczbę przed pierwiastkiem podnosimy do kwadratu i mnożymy przez liczbę pod pierwiastkiem.'), ('conclude', '$@{a}\\sqrt{@{r}} = \\sqrt{@{a * a} \\cdot @{r}} = \\sqrt{@{a * a * r}}$')],
             errors=[('no_square', Int('a * r'), 'Liczba przed pierwiastkiem trafia pod pierwiastek podniesiona do kwadratu.')]),
      min_distinct=20, area=A1, prereq=['vh-root-factor'])

skill('vh-root-multiply', S, 'Mnożenie i dzielenie pierwiastków', ['VII-VIII.1.9.a', 'VII-VIII.1.9.b'],
      [lvl('Iloczyn pierwiastków', mode=0), lvl('Iloraz pierwiastków', mode=1)],
      [('a', 'randint(2, 9)'), ('b', 'randint(2, 9)'), ('r', 'choice([2, 3, 5, 6, 7])'), ('s', 'choice([2, 3, 5])'),
       ('txt', "'\\\\sqrt{' + str(a * a * r) + '} \\\\cdot \\\\sqrt{' + str(b * b * r) + '}' if mode == 0 else '\\\\sqrt{' + str(a * a * b * b * s) + '} : \\\\sqrt{' + str(s) + '}'"),
       ('v', 'a * b * r if mode == 0 else a * b'),
       ('rule', "'Mnożymy liczby pod pierwiastkiem: $\\\\sqrt{x} \\\\cdot \\\\sqrt{y} = \\\\sqrt{xy}$.' if mode == 0 else 'Dzielimy liczby pod pierwiastkiem: $\\\\sqrt{x} : \\\\sqrt{y} = \\\\sqrt{x : y}$.'")],
      number('Oblicz: $@{txt}$', 'v', [('idea', '@{rule}'), ('conclude', 'Wynik: @{v}.')]),
      constraints=['mode != 0 or (a * a * r < 500 and b * b * r < 500)', 'mode != 1 or a * a * b * b * s < 2000'], min_distinct=30, area=A1, prereq=['vh-root-factor'])

# ============================================================================ proporcjonalność, zliczanie, kalkulator (1.10 - 1.12)
skill('vh-direct-prop', S, 'Wielkości wprost proporcjonalne', ['VII-VIII.1.10'],
      [lvl('Znajdź brakującą wartość', mode=0), lvl('Dwie pary wartości', mode=1)],
      [('k', 'randint(2, 12)'), ('x1', 'randint(2, 9)'), ('x2', 'randint(x1 + 1, 15)'), ('x3', 'randint(x2 + 1, 20)'), ('y1', 'k * x1'), ('y2', 'k * x2'), ('y3', 'k * x3'),
       ('ctx', "choice([['kilogramów jabłek', 'zł'], ['godzin pracy', 'zł'], ['litrów benzyny', 'km'], ['metrów tkaniny', 'zł']])")],
      number("@{('Za ' + str(x1) + ' ' + ctx[0] + ' płacimy (lub otrzymujemy) ' + str(y1) + ' ' + ctx[1] + '. Ile ' + ctx[1] + ' odpowiada ' + str(x2) + ' ' + ctx[0] + ', jeśli zależność jest wprost proporcjonalna?' if mode == 0 else 'Zależność jest wprost proporcjonalna. Dla ' + str(x1) + ' ' + ctx[0] + ' mamy ' + str(y1) + ' ' + ctx[1] + ', a dla ' + str(x2) + ' ' + ctx[0] + ' mamy ' + str(y2) + ' ' + ctx[1] + '. Ile ' + ctx[1] + ' odpowiada ' + str(x3) + ' ' + ctx[0] + '?')}",
             'y2 if mode == 0 else y3',
             [('idea', 'Wielkości wprost proporcjonalne mają stały iloraz y : x. Policz go dla znanej pary.'),
              ('compute', "@{(str(y1) + ' : ' + str(x1) + ' = ' + str(k) + '; ' + str(k) + ' · ' + str(x2) + ' = ' + str(y2) if mode == 0 else str(y2) + ' : ' + str(x2) + ' = ' + str(k) + '; ' + str(k) + ' · ' + str(x3) + ' = ' + str(y3))}")]),
      min_distinct=40, area=A1, prereq=['n46-wp-proportion'])

skill('vh-prop-divide', S, 'Podział proporcjonalny', ['VII-VIII.1.10'],
      [lvl('Na dwie części', parts=2), lvl('Na trzy części', parts=3)],
      [('a', 'randint(1, 5)'), ('b', 'randint(1, 6)'), ('c', 'randint(1, 4)'), ('unit', 'randint(2, 30) * 10'),
       ('total', '(a + b) * unit if parts == 2 else (a + b + c) * unit'), ('ask', 'randint(0, parts - 1)'),
       ('rs', '[a, b, c]'), ('shares', '[a * unit, b * unit, c * unit]'),
       ('names', "['Ola', 'Kuba', 'Maja']"),
       ('txt', "'Ola i Kuba dzielą ' + str(total) + ' zł w stosunku ' + str(a) + ' : ' + str(b) + '. Ile złotych dostanie ' + ['Ola', 'Kuba'][ask] + '?' if parts == 2 else "
               "'Ola, Kuba i Maja dzielą ' + str(total) + ' zł w stosunku ' + str(a) + ' : ' + str(b) + ' : ' + str(c) + '. Ile złotych dostanie ' + names[ask] + '?'")],
      number('@{txt}', 'shares[ask]',
             [('idea', 'Zsumuj części stosunku, podziel kwotę przez sumę części (to jedna część), a potem pomnóż przez część danej osoby.'),
              ('compute', "@{str(total) + ' : ' + str(sum(take(rs, parts))) + ' = ' + str(unit) + '; ' + str(unit) + ' · ' + str(rs[ask]) + ' = ' + str(shares[ask])}")]),
      constraints=['a != b', 'parts == 2 or (c != a and c != b)'], tags=FIN, min_distinct=40, area=A1, prereq=['vh-direct-prop'])

skill('vh-count-pairs', S, 'Reguła mnożenia', ['VII-VIII.1.11'],
      [lvl('Dwa wybory', k=0), lvl('Dwa wybory z ograniczeniem', k=1)],
      [('a', 'randint(2, 8)'), ('b', 'randint(2, 8)'), ('cx', 'randint(1, 3)'),
       ('g', "choice([[['bluzka', 'bluzki', 'bluzek'], ['spódnica', 'spódnice', 'spódnic'], 'zestawów'], [['zupa', 'zupy', 'zup'], ['sałatka', 'sałatki', 'sałatek'], 'obiadów'], "
             "[['czapka', 'czapki', 'czapek'], ['szalik', 'szaliki', 'szalików'], 'kompletów'], [['kanapka', 'kanapki', 'kanapek'], ['sok', 'soki', 'soków'], 'zestawów lunchowych']])"),
       ('base', "'Do wyboru jest ' + pln(a, g[0]) + ' i ' + pln(b, g[1]) + '. '"),
       ('txt', "base + 'Ile różnych ' + g[2] + ' można utworzyć, wybierając po jednej rzeczy z każdej grupy?' if k == 0 else "
               "base + 'Odrzucamy ' + pln(cx, ['element', 'elementy', 'elementów']) + ' z pierwszej grupy, bo nie pasują do niczego z drugiej. Ile różnych ' + g[2] + ' można utworzyć z pozostałych?'")],
      number('@{txt}', 'a * b if k == 0 else (a - cx) * b',
             [('idea', "@{('Do każdego wyboru z pierwszej grupy można dobrać każdy z drugiej: mnożymy.' if k == 0 else 'Najpierw odrzuć niepasujące elementy, potem pomnóż.')}"),
              ('conclude', "@{('Odpowiedź: ' + str(a * b if k == 0 else (a - cx) * b) + '.')}")]),
      constraints=['k == 0 or a > cx'], min_distinct=30, area=A1, prereq=['n46-count-cases'])

CALC_TASKS = ("[['Chcesz porównać koszt miesięcznych rat trzech kredytów z różnym oprocentowaniem.', 'Kalkulator lub arkusz – to dużo działań na liczbach z przecinkiem.'], "
              "['Chcesz obliczyć √7 z dokładnością do setnych.', 'Kalkulator – pierwiastek nie jest liczbą wymierną.'], "
              "['Sprawdzasz, ile procent wynosi 37 z 148 w trzech różnych zestawach danych.', 'Kalkulator lub arkusz kalkulacyjny.']]")
tools78 = [
    bank_choice('Aplikacja bankowa podaje, że po roku lokata 1 000 zł przy oprocentowaniu 4% da 1 400 zł zysku. Co powinieneś zrobić?',
                [('Sprawdzić wynik w pamięci: 4% z 1 000 zł to 40 zł, więc 1 400 zł zysku to pomyłka.', True), ('Uwierzyć aplikacji.', False),
                 ('Wpisać dane jeszcze raz i znów uwierzyć.', False), ('Zaokrąglić wynik do tysięcy.', False)],
                [('idea', 'Szacowanie w pamięci pozwala szybko wychwycić błąd narzędzia lub błąd wpisanych danych.')]),
    bank_choice('W arkuszu kalkulacyjnym chcesz obliczyć 23% VAT dla 200 cen. Co ułatwi pracę?',
                [('Wpisać wzór w pierwszej komórce i przeciągnąć go w dół.', True), ('Liczyć każdą cenę osobno na kalkulatorze i przepisywać.', False),
                 ('Obliczyć tylko pierwszą cenę, resztę zgadnąć.', False), ('Pomnożyć wszystkie ceny przez 23.', False)],
                [('idea', 'Arkusz powtarza ten sam wzór dla wielu danych. Pamiętaj: 23% to mnożenie przez 0,23.')]),
    bank_choice('Kalkulator pokazuje √50 ≈ 7,0711. Jak zaokrąglisz tę wartość do części dziesiątych?',
                [('7,1', True), ('7,0', False), ('7,2', False), ('7,07', False)],
                [('idea', 'Patrzymy na cyfrę setnych: 7 ≥ 5, więc zwiększamy cyfrę dziesiątych: 7,0 → 7,1.')]),
    bank_choice('Chcesz zaplanować budżet i porównać trzy oferty subskrypcji z różnymi opłatami za rok. Co zrobisz?',
                [('Zapiszesz dane w tabeli, obliczysz roczny koszt każdej oferty i porównasz wyniki.', True), ('Wybierzesz najtańszą miesięczną opłatę, nie sprawdzając reszty.', False),
                 ('Wybierzesz ofertę z najdłuższą nazwą.', False), ('Wybierzesz losowo.', False)],
                [('idea', 'Porównuj całkowity koszt w tym samym okresie, uwzględniając opłaty jednorazowe.')]),
    bank_choice('Który wynik jest sensowny dla działania 4,8 · 3,9 (bez dokładnego liczenia)?',
                [('około 19', True), ('około 1,9', False), ('około 190', False), ('około 8,7', False)],
                [('idea', '4,8 ≈ 5, 3,9 ≈ 4, więc iloczyn jest bliski 20.')]),
]
bank_skill('vh-calculator', S, 'Kalkulator i aplikacje obliczeniowe', ['VII-VIII.1.12', 'VII-VIII.5.1.c'], tools78, levels=['Mądre użycie narzędzi'], tags=('thinking', 'calculator-allowed'), area=A1,
           intro='Kalkulator i arkusz kalkulacyjny przyspieszają rachunki, ale to ty ustawiasz dane i oceniasz, czy wynik jest sensowny.')

# ============================================================================ ścieżka
un = Unit(S, 'vh-u1', 'Procenty', 'Jakim procentem jest liczba, procent liczby, liczba z procentu, zmiany cen i finanse.', 'percent', area=A1)
un.learn('vh-percent-what').learn('vh-percent-of').learn('vh-percent-number').learn('vh-price-change').learn('vh-interest')
un.checkpoint(['vh-percent-what', 'vh-percent-of', 'vh-percent-number', 'vh-price-change', 'vh-interest'])

un = Unit(S, 'vh-u2', 'Potęgi', 'Potęgi o wykładnikach naturalnych i całkowitych, działania na potęgach i notacja wykładnicza.', 'power', area=A1)
un.learn('vh-power-calc').learn('vh-power-decimal').learn('vh-power-negative').learn('vh-power-laws').learn('vh-sci-exponent').learn('vh-sci-compare')
un.checkpoint(['vh-power-calc', 'vh-power-negative', 'vh-power-laws', 'vh-sci-exponent', 'vh-sci-compare'])

un = Unit(S, 'vh-u3', 'Pierwiastki', 'Pierwiastki kwadratowe i sześcienne, szacowanie i działania.', 'root', area=A1)
un.learn('vh-sqrt-exact').learn('vh-sqrt-between').learn('vh-sqrt-approx').learn('vh-root-factor').learn('vh-root-bring-in').learn('vh-root-multiply')
un.checkpoint(['vh-sqrt-exact', 'vh-sqrt-between', 'vh-root-factor', 'vh-root-bring-in', 'vh-root-multiply'])

un = Unit(S, 'vh-u4', 'Proporcje, zliczanie i narzędzia', 'Proporcjonalność, podział proporcjonalny, reguła mnożenia i mądre użycie kalkulatora.', 'ratio', area=A1)
un.learn('vh-direct-prop').learn('vh-prop-divide').learn('vh-count-pairs').learn('vh-calculator', levels=[1], tasks=5)
un.checkpoint(['vh-direct-prop', 'vh-prop-divide', 'vh-count-pairs'])
