"""Stage IV-VI, area 1 (Liczby): percentages and money (moduł ekonomiczno-finansowy).
Objectives: IV-VI.1.33-1.35, 2.13."""
from dsl import *

S = 'IV-VI'
A1 = 'IV-VI.1'
A2 = 'IV-VI.2'
FIN = ('finance', 'no-calculator')

# shop items: [nominative sg, nominative pl (2-4), genitive pl, price range in groszy: low, high]
ITEMS = ("[['zeszyt', 'zeszyty', 'zeszytów', 150, 800], ['długopis', 'długopisy', 'długopisów', 100, 600], "
         "['batonik', 'batoniki', 'batoników', 200, 450], ['bułka', 'bułki', 'bułek', 80, 250], "
         "['pomarańcza', 'pomarańcze', 'pomarańczy', 150, 350], ['naklejka', 'naklejki', 'naklejek', 50, 300], "
         "['bilet', 'bilety', 'biletów', 250, 1500], ['kredka', 'kredki', 'kredek', 100, 400]]")

# ============================================================================ procenty (1.33, 1.34)
skill('n46-percent-fraction', S, '1%, 10%, 25%, 50% i 100% jako ułamek', ['IV-VI.1.33'],
      [lvl('Z procentu na ułamek', md=30, dirn=0), lvl('Z ułamka na procent', md=30, dirn=1)],
      [('i', 'randint(0, 4)'), ('ph', 'randint(0, 2)'), ('sh', 'shuffle([1, 2, 3, 4])'),
       ('pcs', "['100%', '50%', '25%', '10%', '1%']"),
       ('frs', "['$1$', '$\\\\frac{1}{2}$', '$\\\\frac{1}{4}$', '$\\\\frac{1}{10}$', '$\\\\frac{1}{100}$']"),
       ('q', "(['Który ułamek jest równy ' + pcs[i] + ' całości?', 'Zamień ' + pcs[i] + ' na ułamek.', 'Jaką część całości stanowi ' + pcs[i] + '?'][ph]) if dirn == 0 else "
             "(['Ile procent całości stanowi ułamek ' + frs[i] + '?', 'Zamień ułamek ' + frs[i] + ' na procent.', 'Ułamek ' + frs[i] + ' całości to ile procent?'][ph])")],
      choice('@{q}', 'frs[i] if dirn == 0 else pcs[i]',
             ['frs[(i + sh[0]) % 5] if dirn == 0 else pcs[(i + sh[0]) % 5]', 'frs[(i + sh[1]) % 5] if dirn == 0 else pcs[(i + sh[1]) % 5]',
              'frs[(i + sh[2]) % 5] if dirn == 0 else pcs[(i + sh[2]) % 5]'],
             [('idea', 'Procent to jedna setna całości: 1% = $\\frac{1}{100}$. Stąd 50% to połowa, 25% to jedna czwarta, 10% to jedna dziesiąta, a 100% to cała całość.'),
              ('conclude', '@{pcs[i]} = @{frs[i]}')]),
      area=A1,
      intro='Procent to jedna setna całości: 1% = $\\frac{1}{100}$. Dlatego 100% to cała całość, 50% to połowa, 25% to jedna czwarta, a 10% to jedna dziesiąta.')

skill('n46-percent-key', S, 'Procent z liczby: 50%, 25%, 10%, 1%', ['IV-VI.1.33'],
      [lvl('50%, 10% i 100%', ps='[50, 10, 100]'), lvl('Także 25% i 1%', ps='[50, 10, 25, 1, 100]')],
      [('p', 'choice(ps)'), ('step', '100 // gcd(p, 100)'), ('n', 'step * randint(2, 40)'), ('r', 'n * p / 100'),
       ('how', "['całość', 'połowa', 'jedna czwarta', 'jedna dziesiąta', 'jedna setna'][index([100, 50, 25, 10, 1], p)]")],
      number('Ile to jest @{p}% z liczby @{n|int}?', 'r',
             [('idea', '@{p}% to @{how} całości.'), ('compute', '@{n|int} · @{p} : 100 = @{r|int}')],
             errors=[('percent_as_number', Int('p'), 'Procent mówi, jaką częścią liczby jest wynik – to nie jest jeszcze wynik.', 'p != r')]),
      selfCheck=['r * 100 == n * p'], min_distinct=30, area=A1, prereq=['n46-percent-fraction'])

skill('n46-percent-of', S, 'Procent danej wielkości w zadaniach', ['IV-VI.1.34'],
      [lvl('Procenty okrągłe', ps='[10, 20, 50, 25]'), lvl('Dowolne procenty', ps='[5, 10, 15, 20, 25, 30, 40, 50, 60, 75, 80]')],
      [('p', 'choice(ps)'), ('step', '100 // gcd(p, 100)'), ('n', 'step * randint(2, 30)'), ('c', 'randint(0, 3)'),
       ('txts', "['W szkole jest ' + str(n) + ' uczniów. ' + str(p) + '% z nich jeździ do szkoły rowerem. Ilu uczniów jeździ rowerem?', "
                "'Zbiornik o pojemności ' + str(n) + ' litrów jest napełniony w ' + str(p) + '%. Ile litrów wody jest w zbiorniku?', "
                "'Trasa wycieczki ma ' + str(n) + ' km. Uczniowie przeszli już ' + str(p) + '% trasy. Ile kilometrów już przeszli?', "
                "'Sklep przyjął dostawę ' + str(n) + ' kg jabłek. Pierwszego dnia sprzedano ' + str(p) + '% dostawy. Ile kilogramów jabłek sprzedano?']"),
       ('r', 'n * p / 100')],
      number('@{txts[c]}', 'r',
             [('idea', '1% to jedna setna: @{n} : 100 = @{n / 100|dec}. Bierzemy @{p} takich części.'), ('compute', '@{p} · @{n / 100|dec} = @{r|dec}')],
             errors=[('one_percent_only', Int('n // 100'), 'To jest dopiero 1%. Trzeba jeszcze pomnożyć przez liczbę procent.', 'p != 1 and n % 100 == 0')]),
      constraints=['n >= 20', 'denom(r) == 1'], selfCheck=['r * 100 == n * p'], min_distinct=30, area=A1, prereq=['n46-percent-key'])

skill('n46-price-after-discount', S, 'Cena po obniżce', ['IV-VI.1.34', 'IV-VI.1.35'],
      [lvl('Obniżka 10%, 20%, 50%', ps='[10, 20, 50]'), lvl('Różne obniżki', ps='[5, 10, 15, 20, 25, 30, 40, 50]')],
      [('p', 'choice(ps)'), ('price', '20 * randint(2, 30)'), ('disc', 'price * p / 100'), ('r', 'price - disc'),
       ('item', "choice(['Bluza', 'Plecak', 'Rower', 'Zestaw klocków', 'Para butów', 'Gra planszowa'])")],
      quantity('@{item} kosztuje @{price|int} zł. Cena została obniżona o @{p}%. Ile kosztuje po obniżce?', 'r', 'zł',
               [('idea', 'Najpierw policz, ile wynosi obniżka: @{p}% z @{price|int} zł. Potem odejmij ją od ceny.'),
                ('compute', 'Obniżka: @{disc|dec} zł. Cena po obniżce: @{price|int} − @{disc|dec} = @{r|dec} zł.')], decimals=2,
               errors=[('answer_discount', Qty('disc', 'zł'), 'To jest wysokość obniżki, a nie nowa cena.')]),
      selfCheck=['r + disc == price', 'denom(r) in divisors(100)'], min_distinct=30, tags=FIN, area=A1, prereq=['n46-percent-of'])

# ============================================================================ zakupy (1.35, 2.13)
skill('n46-total-cost', S, 'Koszt zakupu kilku sztuk', ['IV-VI.1.35', 'IV-VI.2.13'],
      [lvl('Jeden towar', two=0), lvl('Dwa towary', two=1), lvl('Z resztą z banknotu', two=2)],
      [('items', ITEMS), ('i', 'randint(0, 7)'), ('j', 'randint(0, 7)'), ('it', 'items[i]'), ('jt', 'items[j]'),
       ('n', 'randint(2, 9)'), ('m', 'randint(2, 6)'),
       ('u', 'randint(it[3] // 10, it[4] // 10) * 10 / 100'), ('v', 'randint(jt[3] // 10, jt[4] // 10) * 10 / 100'),
       ('cost', 'n * u if two == 0 else n * u + m * v'), ('bill', 'choice([20, 50, 100])'),
       ('txt', "('Cena: ' + it[0] + ' – ' + fmt(u, 2) + ' zł za sztukę. Ile zapłacimy za ' + pln(n, it) + '?') if two == 0 else "
               "('Cennik: ' + it[0] + ' – ' + fmt(u, 2) + ' zł, ' + jt[0] + ' – ' + fmt(v, 2) + ' zł (za sztukę). ' + "
               "('Ile zapłacimy za ' + pln(n, it) + ' i ' + pln(m, jt) + '?' if two == 1 else "
               "'Kupiono ' + pln(n, it) + ' i ' + pln(m, jt) + ' i zapłacono banknotem ' + str(bill) + ' zł. Ile reszty otrzymano?'))"),
       ('ans', 'cost if two < 2 else bill - cost')],
      quantity('@{txt}', 'ans', 'zł',
               [('idea', 'Mnożymy cenę jednej sztuki przez liczbę sztuk i dodajemy koszty.'),
                ('compute', 'Za zakupy: @{cost|dec:2} zł.'),
                ('conclude', "@{('Reszta: ' + str(bill) + ' − ' + fmt(cost, 2) + ' = ' + fmt(bill - cost, 2) + ' zł.' if two == 2 else 'Do zapłaty: ' + fmt(cost, 2) + ' zł.')}")],
               decimals=2),
      constraints=['i != j', 'two < 2 or bill > cost'], selfCheck=['denom(cost) in divisors(100)'], min_distinct=40, tags=FIN, area=A1, prereq=['n46-dec-mul', 'n46-dec-add'])

skill('n46-unit-price', S, 'Cena jednostkowa i opłacalność', ['IV-VI.1.35'],
      [lvl('Ceny w pełnych 10 gr', gran=10), lvl('Ceny w groszach', gran=1)],
      [('items', ITEMS), ('it', 'choice(items)'), ('n1', 'choice([2, 3, 4, 5, 6, 8, 10, 12])'), ('n2', 'choice([2, 3, 4, 5, 6, 8, 10, 12])'),
       ('u1', 'randint(it[3] // gran, it[4] // gran) * gran / 100'), ('u2', 'randint(it[3] // gran, it[4] // gran) * gran / 100'), ('p1', 'n1 * u1'), ('p2', 'n2 * u2')],
      choice_text('W sklepie sprzedają te same produkty w dwóch ofertach. Oferta A: @{n1|pl:it} za @{p1|money}. Oferta B: @{n2|pl:it} za @{p2|money}. '
                  'Która oferta jest korzystniejsza, jeśli chcemy płacić jak najmniej za jedną sztukę?',
                  [('Oferta A', 'u1 < u2'), ('Oferta B', 'u2 < u1')], None,
                  [('idea', 'Paczki mają różną liczbę sztuk, więc porównujemy cenę jednej sztuki.'),
                   ('compute', 'Oferta A: @{p1|money} : @{n1} = @{u1|money} za sztukę. Oferta B: @{p2|money} : @{n2} = @{u2|money} za sztukę.'),
                   ('conclude', "Taniej wychodzi oferta @{('A' if u1 < u2 else 'B')}.")], fixed_order=True,
                  errors=[('compare_totals', Choice("'a' if p1 < p2 else 'b'"), 'Porównałeś ceny całych paczek, a paczki mają różną liczbę sztuk. Policz, ile kosztuje jedna sztuka.', '(p1 < p2) != (u1 < u2)')]),
      constraints=['n1 != n2', 'u1 != u2'], selfCheck=['p1 / n1 == u1', 'p2 / n2 == u2'], min_distinct=100, tags=FIN, area=A1, prereq=['n46-total-cost'],
      extra_sources=[{'type': 'llm', 'ref': 'authoring/shop-word-problems.llm.json'}],
      intro='Cena jednostkowa to cena jednej sztuki (albo jednego kilograma, litra). Żeby porównać oferty, dzielimy cenę opakowania przez liczbę sztuk.')

skill('n46-offer-compare', S, 'Promocje: co się bardziej opłaca?', ['IV-VI.1.35', 'IV-VI.1.34'],
      [lvl('Trzecia sztuka gratis', pr=0), lvl('Druga sztuka za pół ceny', pr=1), lvl('Obie promocje', pr=2)],
      [('kind', 'randint(0, 1) if pr == 2 else pr'), ('price', 'choice([10, 12, 20, 24, 30, 40, 50])'), ('pct', 'choice([20, 25, 30, 40])'),
       ('nA', '3 if kind == 0 else 2'), ('costA', '2 * price if kind == 0 else price * 3 / 2'), ('costB', 'nA * price * (100 - pct) / 100'),
       ('descA', "'Oferta A: trzecia sztuka gratis (płacisz za dwie).' if kind == 0 else 'Oferta A: druga sztuka za połowę ceny.'"),
       ('qty', "pln(nA, ['sztukę', 'sztuki', 'sztuk'])")],
      choice_text('Jedna sztuka kosztuje @{price} zł. Chcemy kupić @{qty}. @{descA} Oferta B: @{pct}% taniej na każdą sztukę. Która oferta jest korzystniejsza?',
                  [('Oferta A', 'costA < costB'), ('Oferta B', 'costB < costA'), ('Obie kosztują tyle samo', 'costA == costB')], None,
                  [('idea', 'Policz łączny koszt w obu ofertach i porównaj.'),
                   ('compute', 'A: @{costA|dec:2} zł, B: @{costB|dec:2} zł.')], fixed_order=True),
      constraints=['costA != costB', 'denom(costB) in divisors(100)'], min_distinct=15, tags=FIN, area=A1, prereq=['n46-price-after-discount'])

skill('n46-budget', S, 'Kieszonkowe i oszczędzanie', ['IV-VI.2.13'],
      [lvl('Ile zostało?', md=40, mode=0), lvl('Po ilu tygodniach?', md=12, mode=1), lvl('Ile jeszcze tygodni?', md=12, mode=2)],
      [('start', 'choice([20, 30, 40, 50, 60, 80, 100])'), ('a', 'randint(5, 19) * 50 / 100'), ('b', 'randint(5, 19) * 50 / 100'),
       ('goal', 'choice([60, 80, 90, 120, 150, 200])'), ('week', 'choice([5, 10, 15, 20, 30])'), ('have', 'randint(1, 5) * week'),
       ('txt', "('Ola dostała ' + str(start) + ' zł kieszonkowego. Kupiła zeszyt za ' + fmt(a, 2) + ' zł i długopisy za ' + fmt(b, 2) + ' zł. Ile złotych jej zostało?') if mode == 0 else "
               "(('Franek chce kupić grę za ' + str(goal) + ' zł. Co tydzień odkłada ' + str(week) + ' zł. Po ilu tygodniach uzbiera tyle pieniędzy?') if mode == 1 else "
               "('Marta oszczędza na rower za ' + str(goal) + ' zł. Ma już ' + str(have) + ' zł i co tydzień dokłada ' + str(week) + ' zł. Ile tygodni jeszcze musi oszczędzać?'))"),
       ('ans', 'start - a - b if mode == 0 else (goal / week if mode == 1 else (goal - have) / week)')],
      decimal('@{txt}', 'ans',
              [('idea', "@{('Odejmij oba wydatki od kwoty kieszonkowego.' if mode == 0 else 'Podziel to, co jeszcze trzeba uzbierać, przez kwotę odkładaną co tydzień.')}"),
               ('conclude', 'Odpowiedź: @{ans|dec}.')]),
      constraints=['mode != 0 or start > a + b', 'mode != 1 or goal % week == 0', 'mode != 2 or (goal > have and (goal - have) % week == 0)'],
      tags=FIN, area=A2, prereq=['n46-total-cost'])

skill('n46-exchange', S, 'Wymiana walut', ['IV-VI.2.13'],
      [lvl('Euro na złote', rev=0), lvl('Złote na euro', rev=1)],
      [('rate', 'choice([4, 4.25, 4.5, 4.2, 4.3, 5])'), ('eur', 'randint(2, 60)'), ('pln', 'eur * rate'),
       ('txt', "('Kurs wymiany: 1 euro = ' + fmt(rate, 2) + ' zł. Ile złotych kosztuje ' + str(eur) + ' euro?') if rev == 0 else "
               "('Kurs wymiany: 1 euro = ' + fmt(rate, 2) + ' zł. Ile euro kupisz za ' + fmt(pln, 2) + ' zł?')"),
       ('ans', 'pln if rev == 0 else eur')],
      decimal('@{txt}', 'ans',
              [('idea', "@{('Mnożymy liczbę euro przez kurs.' if rev == 0 else 'Dzielimy kwotę w złotych przez kurs.')}"),
               ('compute', "@{(str(eur) + ' · ' + fmt(rate, 2) + ' = ' + fmt(pln, 2) if rev == 0 else fmt(pln, 2) + ' : ' + fmt(rate, 2) + ' = ' + str(eur))}")]),
      selfCheck=['pln == eur * rate'], min_distinct=40, tags=FIN, area=A2, prereq=['n46-dec-mul', 'n46-dec-div-dec'])

# ============================================================================ ścieżka
un = Unit(S, 'n46-u15', 'Procenty', 'Procent jako część całości, procent z liczby i obniżki.', 'percent', area=A1)
un.learn('n46-percent-fraction').learn('n46-percent-key').learn('n46-percent-of').learn('n46-price-after-discount')
un.checkpoint(['n46-percent-fraction', 'n46-percent-key', 'n46-percent-of', 'n46-price-after-discount'])

un = Unit(S, 'n46-u16', 'Zakupy i pieniądze', 'Koszty, promocje, cena jednostkowa, kieszonkowe i kursy walut.', 'wallet', area=A1)
un.learn('n46-total-cost').learn('n46-unit-price').learn('n46-offer-compare').review('Powtórka: zakupy', ['n46-total-cost', 'n46-unit-price', 'n46-offer-compare'])
un.learn('n46-budget').learn('n46-exchange')
un.checkpoint(['n46-total-cost', 'n46-unit-price', 'n46-offer-compare', 'n46-budget', 'n46-exchange'])
