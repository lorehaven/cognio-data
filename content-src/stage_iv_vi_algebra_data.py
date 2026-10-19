"""Stage IV-VI: Algebra (area 3) and Data (area 5).
Objectives: IV-VI.3.1-3.5, IV-VI.5.1-5.4."""
from dsl import *

S = 'IV-VI'
A3 = 'IV-VI.3'
A5 = 'IV-VI.5'
FIN = ('finance', 'no-calculator')

# ============================================================================ algebra (3.1-3.5)
skill('n46-alg-expression', S, 'Wyrażenie algebraiczne z treści zadania', ['IV-VI.3.1'],
      [lvl('Jedno działanie', pmin=0, pmax=3), lvl('Dwa działania', pmin=4, pmax=7)],
      [('lt', "choice(['x', 'a', 'n', 'm'])"), ('k', 'randint(2, 9)'), ('p', 'randint(pmin, pmax)'),
       ('texts', "['Kasia ma ' + lt + ' lat. Jej siostra jest o ' + pln(k, ['rok', 'lata', 'lat']) + ' starsza. Jakie wyrażenie opisuje wiek siostry?', "
                 "'Jeden zeszyt kosztuje ' + lt + ' zł. Jakie wyrażenie opisuje koszt ' + str(k) + ' zeszytów?', "
                 "'W pudełku było ' + lt + ' cukierków. Ola zjadła ' + pln(k, ['cukierek', 'cukierki', 'cukierków']) + '. Jakie wyrażenie opisuje liczbę cukierków, które zostały?', "
                 "'Tata miał ' + lt + ' zł i podzielił je po równo między ' + pln(k, ['osobę', 'osoby', 'osób']) + '. Jakie wyrażenie opisuje, ile złotych dostała każda osoba?', "
                 "'Bilet do kina kosztuje ' + lt + ' zł. Kupiono ' + str(k) + ' biletów i zapłacono banknotem 100 zł. Jakie wyrażenie opisuje resztę?', "
                 "'Ola ma ' + lt + ' zł, a Ania ma o ' + str(k) + ' zł więcej. Jakie wyrażenie opisuje, ile mają razem?', "
                 "'Prostokąt ma szerokość ' + lt + ' cm, a długość o ' + str(k) + ' cm większą. Jakie wyrażenie opisuje obwód prostokąta?', "
                 "'Zeszyt kosztuje ' + lt + ' zł, a długopis o ' + str(k) + ' zł mniej. Jakie wyrażenie opisuje koszt zeszytu i długopisu razem?']"),
       ('opts', "[[lt + ' + ' + str(k), lt + ' − ' + str(k), str(k) + ' · ' + lt, lt + ' : ' + str(k)], "
                "[str(k) + ' · ' + lt, lt + ' + ' + str(k), lt + ' : ' + str(k), lt + ' − ' + str(k)], "
                "[lt + ' − ' + str(k), lt + ' + ' + str(k), str(k) + ' − ' + lt, str(k) + ' · ' + lt], "
                "[lt + ' : ' + str(k), lt + ' − ' + str(k), str(k) + ' · ' + lt, str(k) + ' : ' + lt], "
                "['100 − ' + str(k) + ' · ' + lt, str(k) + ' · ' + lt + ' − 100', '100 − ' + lt, '(100 − ' + str(k) + ') · ' + lt], "
                "[lt + ' + (' + lt + ' + ' + str(k) + ')', lt + ' + ' + str(k), lt + ' · (' + lt + ' + ' + str(k) + ')', '2 · ' + lt + ' − ' + str(k)], "
                "['2 · (' + lt + ' + ' + lt + ' + ' + str(k) + ')', lt + ' + ' + lt + ' + ' + str(k), '2 · ' + lt + ' + ' + str(k), lt + ' · (' + lt + ' + ' + str(k) + ')'], "
                "[lt + ' + (' + lt + ' − ' + str(k) + ')', lt + ' + ' + lt + ' + ' + str(k), '2 · ' + lt + ' + ' + str(k), lt + ' · (' + lt + ' − ' + str(k) + ')']]")],
      choice('@{texts[p]}', 'opts[p][0]', ['opts[p][1]', 'opts[p][2]', 'opts[p][3]'],
             [('idea', 'Zapisz, co się dzieje z niewiadomą: dodajemy, odejmujemy, mnożymy czy dzielimy? Litera zastępuje liczbę, której nie znamy.'),
              ('conclude', 'Poprawne wyrażenie: @{opts[p][0]}.')]),
      min_distinct=40, area=A3,
      intro='Litery w matematyce zastępują liczby. Wyrażenie algebraiczne to zapis działań na liczbach i literach, np. $x + 3$ (liczba x zwiększona o 3) albo $5 \\cdot x$ (pięć razy x).')

skill('n46-alg-evaluate', S, 'Wartość wyrażenia algebraicznego', ['IV-VI.3.2'],
      [lvl('Jedna zmienna, jedno działanie', fmin=0, fmax=1), lvl('Nawiasy i kwadrat', fmin=2, fmax=3), lvl('Dwie zmienne', fmin=4, fmax=5)],
      [('f', 'randint(fmin, fmax)'), ('a', 'randint(2, 9)'), ('b', 'randint(1, 12)'), ('c', 'randint(2, 9)'), ('x', 'randint(2, 9)'), ('y', 'randint(2, 9)'),
       ('exprs', "['$' + str(a) + 'x + ' + str(b) + '$', '$' + str(a) + 'x - ' + str(b) + '$', '$' + str(a) + '(x + ' + str(b) + ')$', '$x^2 + ' + str(b) + '$', "
                 "'$' + str(a) + 'x + ' + str(c) + 'y$', '$' + str(a) + 'xy - ' + str(b) + '$']"),
       ('vals', '[a * x + b, a * x - b, a * (x + b), x * x + b, a * x + c * y, a * x * y - b]'),
       ('g1', "'$x = ' + str(x) + '$'"), ('g2', "'$x = ' + str(x) + '$ i $y = ' + str(y) + '$'"), ('given', '[g1, g1, g1, g1, g2, g2]'),
       ('v', 'vals[f]')],
      number('Oblicz wartość wyrażenia @{exprs[f]} dla @{given[f]}.', 'v',
             [('idea', 'Podstaw liczbę w miejsce litery i wykonaj działania we właściwej kolejności.'),
              ('conclude', 'Wartość wyrażenia: @{v}.')],
             errors=[('concat', Int('a * 10 + x if f == 0 else v'), 'Zapis 3x oznacza 3 · x, a nie liczbę „3x” (trzydzieści kilka).', 'f == 0')]),
      constraints=['f != 1 or a * x > b', 'f != 5 or a * x * y > b'], selfCheck=['v > 0'], min_distinct=40, area=A3, prereq=['n46-alg-expression'])

FORMULAS_NOTE = 'wzory z literami'
skill('n46-alg-formula', S, 'Obliczanie ze wzoru', ['IV-VI.3.3'],
      [lvl('Pole i obwód prostokąta, droga', fmin=0, fmax=2), lvl('Trójkąt i prostopadłościan', fmin=3, fmax=4), lvl('Trapez', fmin=5, fmax=5)],
      [('f', 'randint(fmin, fmax)'), ('a', 'randint(2, 12)'), ('b', 'randint(2, 12)'), ('c', 'randint(2, 6)'),
       ('names', "['pole prostokąta', 'obwód prostokąta', 'drogę przebytą ruchem jednostajnym', 'pole trójkąta', 'objętość prostopadłościanu', 'pole trapezu']"),
       ('forms', "['P = a \\\\cdot b', 'O = 2a + 2b', 's = v \\\\cdot t', 'P = \\\\frac{1}{2} \\\\cdot a \\\\cdot h', 'V = a \\\\cdot b \\\\cdot c', 'P = \\\\frac{1}{2} \\\\cdot (a + b) \\\\cdot h']"),
       ('given', "['a = ' + str(a) + ', b = ' + str(b), 'a = ' + str(a) + ', b = ' + str(b), 'v = ' + str(a) + ', t = ' + str(b), 'a = ' + str(2 * a) + ', h = ' + str(b), "
                 "'a = ' + str(a) + ', b = ' + str(b) + ', c = ' + str(c), 'a = ' + str(a) + ', b = ' + str(b) + ', h = ' + str(2 * c)]"),
       ('vals', '[a * b, 2 * a + 2 * b, a * b, a * b, a * b * c, (a + b) * c]'),
       ('v', 'vals[f]')],
      number('Oblicz @{names[f]} ze wzoru $@{forms[f]}$ dla @{given[f]}.', 'v',
             [('idea', 'Podstaw podane liczby w miejsce liter i oblicz.'), ('conclude', 'Wynik: @{v}.')]),
      selfCheck=['denom(v) == 1'], min_distinct=40, area=A3, prereq=['n46-alg-evaluate'],
      intro='Wzór to zapis zależności między wielkościami za pomocą liter, np. pole prostokąta $P = a \\cdot b$. Aby obliczyć wartość, podstawiamy liczby w miejsce liter.')

skill('n46-alg-equation-build', S, 'Ułóż równanie do zadania', ['IV-VI.3.4'],
      [lvl('Jedno działanie', pmin=0, pmax=3), lvl('Dwa działania', pmin=4, pmax=7)],
      [('k', 'randint(2, 9)'), ('n', 'randint(2, 9)'), ('xv', 'randint(2, 12)'), ('p', 'randint(pmin, pmax)'),
       ('m', '[xv + k, xv * k, xv - k, xv // k, xv * k + n, 2 * xv + n, 2 * (xv - k), 2 * xv + k][p]'),
       ('texts', "['Pomyślałem liczbę, dodałem do niej ' + str(k) + ' i otrzymałem ' + str(m) + '.', "
                 "'Pomyślałem liczbę, pomnożyłem ją przez ' + str(k) + ' i otrzymałem ' + str(m) + '.', "
                 "'Pomyślałem liczbę, odjąłem od niej ' + str(k) + ' i otrzymałem ' + str(m) + '.', "
                 "'Pomyślałem liczbę, podzieliłem ją przez ' + str(k) + ' i otrzymałem ' + str(xv // k) + '.', "
                 "'Pomyślałem liczbę, pomnożyłem ją przez ' + str(k) + ', dodałem ' + str(n) + ' i otrzymałem ' + str(m) + '.', "
                 "'Do podwojonej liczby dodałem ' + str(n) + ' i otrzymałem ' + str(m) + '.', "
                 "'Od pewnej liczby odjąłem ' + str(k) + ', wynik podwoiłem i otrzymałem ' + str(m) + '.', "
                 "'Ola ma x zł, a Ania ma o ' + str(k) + ' zł więcej. Razem mają ' + str(m) + ' zł.']"),
       ('good', "['x + ' + str(k) + ' = ' + str(m), str(k) + ' · x = ' + str(m), 'x − ' + str(k) + ' = ' + str(m), 'x : ' + str(k) + ' = ' + str(xv // k), "
                "str(k) + ' · x + ' + str(n) + ' = ' + str(m), '2 · x + ' + str(n) + ' = ' + str(m), '(x − ' + str(k) + ') · 2 = ' + str(m), 'x + (x + ' + str(k) + ') = ' + str(m)]"),
       ('w1', "['x − ' + str(k) + ' = ' + str(m), 'x + ' + str(k) + ' = ' + str(m), 'x + ' + str(k) + ' = ' + str(m), 'x · ' + str(k) + ' = ' + str(xv // k), "
              "str(k) + ' · (x + ' + str(n) + ') = ' + str(m), 'x + 2 + ' + str(n) + ' = ' + str(m), 'x − ' + str(k) + ' · 2 = ' + str(m), 'x + ' + str(k) + ' = ' + str(m)]"),
       ('w2', "[str(k) + ' · x = ' + str(m), 'x : ' + str(k) + ' = ' + str(m), str(k) + ' − x = ' + str(m), 'x + ' + str(k) + ' = ' + str(xv // k), "
              "'x + ' + str(k) + ' + ' + str(n) + ' = ' + str(m), '2 + x + ' + str(n) + ' = ' + str(m), '2 · x − ' + str(k) + ' = ' + str(m), '2 · x + ' + str(k) + ' = ' + str(m)]"),
       ('w3', "['x : ' + str(k) + ' = ' + str(m), str(k) + ' − x = ' + str(m), 'x : ' + str(k) + ' = ' + str(m), str(k) + ' : x = ' + str(xv // k), "
              "str(k) + ' · x − ' + str(n) + ' = ' + str(m), '2 · (x + ' + str(n) + ') = ' + str(m), 'x · 2 − ' + str(k) + ' = ' + str(m), 'x · (x + ' + str(k) + ') = ' + str(m)]")],
      choice('@{texts[p]} Które równanie opisuje tę sytuację, jeśli x oznacza niewiadomą?', 'good[p]', ['w1[p]', 'w2[p]', 'w3[p]'],
             [('idea', 'Zapisz każde zdanie jako działanie na niewiadomej x. Szukany wynik stoi po prawej stronie znaku równości.'), ('conclude', 'Równanie: @{good[p]}.')]),
      constraints=['p != 3 or xv % k == 0', 'p != 3 or xv // k >= 2', 'p != 6 or xv > k', 'p != 2 or xv > k', 'len(uniq([good[p], w1[p], w2[p], w3[p]])) == 4'],
      min_distinct=40, area=A3, prereq=['n46-alg-expression'])

skill('n46-alg-solve', S, 'Rozwiązywanie prostych równań', ['IV-VI.3.5'],
      [lvl('Dodawanie i odejmowanie', fmin=0, fmax=1), lvl('Mnożenie i dzielenie', fmin=2, fmax=3), lvl('Dwa działania', fmin=4, fmax=6)],
      [('f', 'randint(fmin, fmax)'), ('xv', 'randint(2, 20)'), ('a', 'randint(2, 9)'), ('b', 'randint(2, 15)'),
       ('eqs', "['x + ' + str(b) + ' = ' + str(xv + b), 'x − ' + str(b) + ' = ' + str(xv - b), str(a) + 'x = ' + str(a * xv), 'x : ' + str(a) + ' = ' + str(xv), "
               "str(a) + 'x + ' + str(b) + ' = ' + str(a * xv + b), '(x + ' + str(b) + ') : ' + str(a) + ' = ' + str(xv), str(a * xv + b) + ' − x = ' + str(a * xv + b - xv)]"),
       ('hints', "['Odejmij ' + str(b) + ' od obu stron.', 'Dodaj ' + str(b) + ' do obu stron.', 'Podziel obie strony przez ' + str(a) + '.', 'Pomnóż obie strony przez ' + str(a) + '.', "
                 "'Najpierw odejmij ' + str(b) + ', potem podziel przez ' + str(a) + '.', 'Najpierw pomnóż przez ' + str(a) + ', potem odejmij ' + str(b) + '.', 'Odejmij od ' + str(a * xv + b) + ' prawą stronę.']")],
      number('Rozwiąż równanie: $@{eqs[f]}$', 'xv',
             [('idea', '@{hints[f]}'), ('conclude', 'x = @{xv}. Sprawdzenie: podstaw @{xv} do równania.')]),
      constraints=['f != 3 or xv * a < 200'], selfCheck=['xv >= 2'], min_distinct=40, area=A3, prereq=['n46-alg-equation-build'],
      intro='Aby rozwiązać równanie, odwracamy działania. Jeśli do x dodano 5, odejmujemy 5; jeśli x pomnożono przez 3, dzielimy przez 3. To, co robimy z jedną stroną równania, robimy też z drugą.')

# ============================================================================ dane (5.1-5.4)
DAYS3 = "['poniedziałek', 'wtorek', 'środa']"
FRUIT = "[['jabłka', 'jabłek'], ['banany', 'bananów'], ['gruszki', 'gruszek'], ['śliwki', 'śliwek'], ['pomarańcze', 'pomarańczy']]"
skill('n46-table-read', S, 'Odczytaj dane z tabeli', ['IV-VI.5.1'],
      [lvl('Suma w wierszu', ask=0, hi=30), lvl('Różnica największej i najmniejszej', ask=1, hi=60), lvl('Największa wartość', ask=2, hi=99)],
      [('fr', 'shuffle(' + FRUIT + ')'), ('v', 'sample(5, hi, 9)'), ('i', 'randint(0, 2)'),
       ('rows', '[[fr[0][0], v[0], v[1], v[2]], [fr[1][0], v[3], v[4], v[5]], [fr[2][0], v[6], v[7], v[8]]]'),
       ('row', 'rows[i]'), ('gen', 'fr[i][1]'), ('nums', 'take(drop(row, 1), 3)'),
       ('txt', "('Ile kilogramów ' + gen + ' sprzedano w sumie we wszystkie trzy dni?') if ask == 0 else "
               "(('O ile kilogramów więcej ' + gen + ' sprzedano w dniu o największej sprzedaży niż w dniu o najmniejszej?') if ask == 1 else "
               "('Ile kilogramów ' + gen + ' sprzedano w dniu, w którym sprzedaż była największa?'))"),
       ('ans', 'sum(nums) if ask == 0 else (max(nums) - min(nums) if ask == 1 else max(nums))')],
      number('Tabela pokazuje sprzedaż owoców (w kg) w sklepie osiedlowym. @{txt}', 'ans',
             [('idea', 'Znajdź w tabeli właściwy wiersz (rodzaj owoców) i odczytaj liczby z kolumn kolejnych dni.'), ('conclude', 'Odpowiedź: @{ans}.')],
             media=[{'type': 'table', 'kind': 'table', 'essential': True, 'alt': 'Tabela: sprzedaż owoców w trzy dni (kg).',
                     'params': {'headers': ['Owoc', 'poniedziałek', 'wtorek', 'środa'], 'rows': E('rows')}}]),
      min_distinct=40, area=A5)

skill('n46-bar-chart', S, 'Odczytaj dane z diagramu słupkowego', ['IV-VI.5.1'],
      [lvl('Odczyt jednego słupka', ask=0), lvl('Różnica i suma', ask=1)],
      [('cats', "choice([['kot', 'pies', 'chomik', 'rybki', 'papuga'], ['piłka nożna', 'koszykówka', 'pływanie', 'tenis', 'siatkówka'], ['czerwony', 'niebieski', 'zielony', 'żółty', 'fioletowy']])"),
       ('topic', "choice(['Ulubione zwierzęta uczniów klasy 4a', 'Ulubione sporty uczniów klasy 4b', 'Ulubione kolory uczniów klasy 4c'])"),
       ('vs', 'sample(2, 20, 5)'), ('i', 'randint(0, 4)'), ('j', 'randint(0, 4)'),
       ('txt', "('Ilu uczniów wybrało odpowiedź „' + cats[i] + '”?') if ask == 0 else "
               "('O ile więcej uczniów wybrało odpowiedź „' + cats[i] + '” niż „' + cats[j] + '”?')"),
       ('ans', 'vs[i] if ask == 0 else vs[i] - vs[j]')],
      number('Diagram słupkowy przedstawia wyniki ankiety. @{txt}', 'ans',
             [('idea', 'Znajdź słupek podpisany odpowiednią odpowiedzią i odczytaj jego wysokość na osi pionowej.'), ('conclude', 'Odpowiedź: @{ans}.')],
             media=[{'type': 'chart', 'kind': 'bar', 'essential': True, 'alt': 'Diagram słupkowy: @{topic}.',
                     'params': {'title': E('topic'), 'labels': E('cats'), 'values': E('vs')}}]),
      constraints=['ask == 0 or vs[i] > vs[j]'], min_distinct=40, area=A5)

skill('n46-line-chart', S, 'Odczytaj dane z wykresu liniowego', ['IV-VI.5.1'],
      [lvl('Odczyt wartości', ask=0), lvl('Największa wartość', ask=1), lvl('Zmiana między godzinami', ask=2)],
      [('t0', 'randint(6, 14)'), ('d', 'sample(-3, 5, 6)'),
       ('ys', '[t0, t0 + d[0], t0 + d[0] + d[1], t0 + d[0] + d[1] + d[2], t0 + d[0] + d[1] + d[2] + d[3], t0 + d[0] + d[1] + d[2] + d[3] + d[4]]'),
       ('hours', '[6, 8, 10, 12, 14, 16]'), ('i', 'randint(0, 4)'), ('j', 'randint(i + 1, 5)'),
       ('txt', "('Jaka była temperatura o godzinie ' + str(hours[i]) + ':00?') if ask == 0 else "
               "(('Jaka była największa temperatura zmierzona tego dnia?') if ask == 1 else "
               "('O ile stopni zmieniła się temperatura między godziną ' + str(hours[i]) + ':00 a ' + str(hours[j]) + ':00? Podaj wynik bez znaku.'))"),
       ('ans', 'ys[i] if ask == 0 else (max(ys) if ask == 1 else abs(ys[j] - ys[i]))')],
      number('Wykres pokazuje temperaturę powietrza (w °C) mierzoną co 2 godziny. @{txt}', 'ans',
             [('idea', 'Znajdź na osi poziomej godzinę, a potem odczytaj wartość punktu na osi pionowej.'), ('conclude', 'Odpowiedź: @{ans}.')],
             media=[{'type': 'chart', 'kind': 'line', 'essential': True, 'alt': 'Wykres liniowy temperatury w ciągu dnia.',
                     'params': {'x': E('hours'), 'y': E('ys'), 'xLabel': 'godzina', 'yLabel': '°C'}}]),
      constraints=['min(ys) >= 0', 'max(ys) <= 30', 'ask != 2 or ys[i] != ys[j]'], min_distinct=40, area=A5)

skill('n46-receipt', S, 'Paragon sklepowy', ['IV-VI.5.1', 'IV-VI.2.13'],
      [lvl('Suma do zapłaty', ask=0), lvl('Reszta z banknotu', ask=1)],
      [('names', "shuffle(['mleko', 'chleb', 'masło', 'ser', 'jogurt', 'jajka', 'makaron', 'sok'])"),
       ('q', 'sample(1, 5, 3)'), ('pr', '[randint(2, 12) * 50 / 100 + 1, randint(2, 12) * 50 / 100 + 1, randint(2, 12) * 50 / 100 + 1]'),
       ('vals', '[q[0] * pr[0], q[1] * pr[1], q[2] * pr[2]]'), ('total', 'sum(vals)'), ('bill', 'choice([50, 100, 200])'),
       ('rows', "[[names[0], q[0], fmt(pr[0], 2), fmt(vals[0], 2)], [names[1], q[1], fmt(pr[1], 2), fmt(vals[1], 2)], [names[2], q[2], fmt(pr[2], 2), fmt(vals[2], 2)]]"),
       ('ans', 'total if ask == 0 else bill - total')],
      quantity('Na paragonie zapisano zakupy. @{(\'Ile złotych wynosi suma do zapłaty?\' if ask == 0 else \'Klient zapłacił banknotem \' + str(bill) + \' zł. Ile reszty powinien otrzymać?\')}',
               'ans', 'zł',
               [('idea', 'Dodaj wartości wszystkich pozycji z ostatniej kolumny.'), ('compute', 'Suma: @{total|dec:2} zł.@{(\' Reszta: \' + str(bill) + \' − \' + fmt(total, 2) + \' = \' + fmt(bill - total, 2) + \' zł.\' if ask == 1 else \'\')}')],
               decimals=2,
               media=[{'type': 'table', 'kind': 'table', 'essential': True, 'alt': 'Paragon z trzema pozycjami.',
                       'params': {'headers': ['Towar', 'Ilość', 'Cena (zł)', 'Wartość (zł)'], 'rows': E('rows')}}]),
      constraints=['len(uniq(pr)) == 3', 'bill > total'], tags=FIN, min_distinct=40, area=A5, prereq=['n46-total-cost'])

skill('n46-survey-tally', S, 'Wyniki ankiety', ['IV-VI.5.2'],
      [lvl('Policz odpowiedzi')],
      [('pool', "choice([['kot', 'pies', 'rybki'], ['lody', 'ciastka', 'owoce'], ['rower', 'hulajnoga', 'rolki']])"),
       ('c', 'sample(3, 9, 3)'), ('answers', 'shuffle(repeat(pool[0], c[0]) + repeat(pool[1], c[1]) + repeat(pool[2], c[2]))'),
       ('i', 'randint(0, 2)'), ('n', 'c[0] + c[1] + c[2]')],
      number('W ankiecie zapytano uczniów o ulubioną odpowiedź. Zebrano takie odpowiedzi: @{join(answers, ", ")}. Ile osób wybrało odpowiedź „@{pool[i]}”?', 'c[i]',
             [('idea', 'Policz odpowiedzi jedna po drugiej (możesz stawiać kreski) i zapisz wynik w tabeli.'), ('conclude', '„@{pool[i]}”: @{c[i]}. Wszystkich odpowiedzi: @{n}.')]),
      min_distinct=40, area=A5)

skill('n46-mean', S, 'Średnia arytmetyczna', ['IV-VI.5.3'],
      [lvl('Średnia całkowita', k=3, frac=0), lvl('Średnia z ułamkiem', k=4, frac=1), lvl('Brakujący składnik', k=4, frac=2)],
      [('m', 'randint(3, 12)'), ('vs', 'sample(1, 14, 4)'),
       ('nums', 'take(vs, k - 1) + [k * m - sum(take(vs, k - 1))] if frac != 1 else take(vs, k)'),
       ('s', 'sum(nums)'), ('avg', 's / k'),
       ('ctx', "choice(['Ala przeczytała w kolejnych dniach tyle stron', 'W kolejnych dniach zmierzono temperatury (w °C)', 'Franek zrobił w kolejnych dniach tyle tysięcy kroków'])"),
       ('given', 'take(nums, k - 1)'), ('miss', 'nums[k - 1]'),
       ('txt', "(ctx + ': ' + join(nums, ', ') + '. Jaka jest średnia arytmetyczna tych liczb?') if frac < 2 else "
               "('Średnia arytmetyczna czterech liczb wynosi ' + str(m) + '. Trzy z nich to: ' + join(given, ', ') + '. Jaka jest czwarta liczba?')"),
       ('ans', 'avg if frac < 2 else miss')],
      decimal('@{txt}', 'ans',
              [('idea', "@{('Średnia to suma liczb podzielona przez ich liczbę.' if frac < 2 else 'Suma wszystkich liczb to średnia razy liczba składników. Odejmij sumę znanych liczb.')}"),
               ('compute', "@{(fmt(s) + ' : ' + str(k) + ' = ' + fmt(avg) if frac < 2 else str(k) + ' · ' + str(m) + ' − ' + str(sum(given)) + ' = ' + str(miss))}")],
              errors=[('forgot_divide', Dec('s'), 'Średnia to suma podzielona przez liczbę składników.', 'frac < 2')]),
      constraints=['frac != 1 or (s % k != 0 and denom(avg) in divisors(100))', 'frac == 1 or s % k == 0', 'min(nums) >= 1', 'len(uniq(nums)) == len(nums)'],
      min_distinct=40, area=A5)

skill('n46-expenses-average', S, 'Średnie wydatki', ['IV-VI.5.4'],
      [lvl('Średnia z czterech miesięcy', mo=4), lvl('Średnia z sześciu miesięcy', mo=6)],
      [('what', "choice(['telefon', 'bilety autobusowe', 'zakupy spożywcze', 'prąd'])"),
       ('base', 'randint(8, 30) * 5'), ('ds', 'sample(-6, 6, mo)'),
       ('xs', '[base + 5 * ds[0], base + 5 * ds[1], base + 5 * ds[2], base + 5 * ds[3]] if mo == 4 else [base + 5 * ds[0], base + 5 * ds[1], base + 5 * ds[2], base + 5 * ds[3], base + 5 * ds[4], base + 5 * ds[5]]'),
       ('avg', 'sum(xs) / mo')],
      quantity('Rodzina Kowalskich przez @{mo|pl:[\'miesiąc\', \'miesiące\', \'miesięcy\']} wydawała na @{what} kolejno: @{join(xs, ", ")} zł. Jakie były średnie miesięczne wydatki na ten cel?', 'avg', 'zł',
               [('idea', 'Dodaj wydatki ze wszystkich miesięcy i podziel przez liczbę miesięcy.'), ('compute', '@{sum(xs)} : @{mo} = @{avg|dec}')], decimals=2),
      constraints=['denom(avg) in divisors(100)'], tags=FIN, min_distinct=40, area=A5, prereq=['n46-mean'])

skill('n46-expenses-decision', S, 'Czy budżet wystarczy?', ['IV-VI.5.4'],
      [lvl('Porównaj średnią z budżetem')],
      [('base', 'randint(10, 30) * 10'), ('ds', 'sample(-5, 5, 4)'), ('xs', '[base + 10 * ds[0], base + 10 * ds[1], base + 10 * ds[2], base + 10 * ds[3]]'),
       ('avg', 'sum(xs) / 4'), ('budget', 'avg + choice([-30, -20, -10, 10, 20, 30])')],
      choice_text('Przez cztery miesiące wydano na rachunki kolejno: @{join(xs, ", ")} zł. Co miesiąc odkładamy na rachunki @{budget|money}. Czy ta kwota wystarcza, żeby pokryć wydatki w przeciętnym miesiącu?',
                  [('Tak, wystarcza', 'budget >= avg'), ('Nie, nie wystarcza', 'budget < avg')], None,
                  [('idea', 'Oblicz średnie miesięczne wydatki i porównaj z kwotą, którą odkładamy.'), ('compute', 'Średnio: @{sum(xs)} : 4 = @{avg|money}; odkładamy @{budget|money}.')], fixed_order=True),
      constraints=['denom(avg) in divisors(100)', 'budget > 0'], tags=FIN, min_distinct=40, area=A5, prereq=['n46-expenses-average'])

skill('n46-plan-compare', S, 'Który abonament się opłaca?', ['IV-VI.5.4', 'IV-VI.1.35'],
      [lvl('Porównanie na 12 miesięcy')],
      [('a', 'randint(3, 9) * 10'), ('b', 'a - 10 * randint(1, 2)'), ('f', 'randint(2, 12) * 10'), ('months', 'choice([6, 12, 24])'),
       ('costA', 'a * months'), ('costB', 'f + b * months')],
      choice_text('Abonament A kosztuje @{a} zł miesięcznie. Abonament B kosztuje @{b} zł miesięcznie, ale trzeba jednorazowo zapłacić @{f} zł za aktywację. Który abonament jest tańszy w ciągu @{months} miesięcy?',
                  [('Abonament A', 'costA < costB'), ('Abonament B', 'costB < costA'), ('Kosztują tyle samo', 'costA == costB')], None,
                  [('idea', 'Policz łączny koszt każdego abonamentu w całym okresie.'),
                   ('compute', 'A: @{a} · @{months} = @{costA} zł. B: @{f} + @{b} · @{months} = @{costB} zł.')], fixed_order=True),
      constraints=['costA != costB'], tags=FIN, min_distinct=40, area=A5, prereq=['n46-expenses-decision'])

# ============================================================================ ścieżka
un = Unit(S, 'n46-u20', 'Litery zamiast liczb', 'Wyrażenia algebraiczne, wzory i równania.', 'algebra', area=A3)
un.learn('n46-alg-expression').learn('n46-alg-evaluate').learn('n46-alg-formula').review('Powtórka: wyrażenia i wzory', ['n46-alg-expression', 'n46-alg-evaluate', 'n46-alg-formula'])
un.learn('n46-alg-equation-build').learn('n46-alg-solve')
un.checkpoint(['n46-alg-expression', 'n46-alg-evaluate', 'n46-alg-formula', 'n46-alg-equation-build', 'n46-alg-solve'])

un = Unit(S, 'n46-u21', 'Dane i statystyka', 'Tabele, diagramy, wykresy, ankiety, średnia i wydatki.', 'chart', area=A5)
un.learn('n46-table-read').learn('n46-bar-chart').learn('n46-line-chart').learn('n46-receipt')
un.review('Powtórka: odczyt danych', ['n46-table-read', 'n46-bar-chart', 'n46-line-chart', 'n46-receipt'])
un.learn('n46-survey-tally').learn('n46-mean').learn('n46-expenses-average').learn('n46-expenses-decision').learn('n46-plan-compare')
un.checkpoint(['n46-table-read', 'n46-bar-chart', 'n46-line-chart', 'n46-survey-tally', 'n46-mean', 'n46-expenses-average'])
