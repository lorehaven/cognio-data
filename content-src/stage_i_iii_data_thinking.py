"""Stage I-III (edukacja wczesnoszkolna): area 4 (Dane) and area 5 (Myślenie matematyczne).  Objectives: I-III.4.a-4.c, 5.a-5.h."""
from dsl import *

S = 'I-III'
A4 = 'I-III.4'
A5 = 'I-III.5'
FIN = ('finance', 'no-calculator')
PERSONS = "[['Ola', 'a'], ['Kasia', 'a'], ['Ania', 'a'], ['Tomek', ''], ['Marek', ''], ['Kuba', '']]"
ITEMS = ("[['jabłko', 'jabłka', 'jabłek'], ['ciastko', 'ciastka', 'ciastek'], ['naklejka', 'naklejki', 'naklejek'], ['kredka', 'kredki', 'kredek'], "
         "['klocek', 'klocki', 'klocków'], ['cukierek', 'cukierki', 'cukierków']]")

# ============================================================================ dane (4.a - 4.c)
skill('ew-table-read', S, 'Odczytaj dane z tabeli', ['I-III.4.a'],
      [lvl('Jedna wartość', ask=0), lvl('Suma w wierszu', ask=1), lvl('Różnica dwóch wartości', ask=2)],
      [('fr', "shuffle([['jabłka', 'jabłek'], ['banany', 'bananów'], ['gruszki', 'gruszek'], ['śliwki', 'śliwek']])"), ('v', 'sample(2, 20, 6)'), ('i', 'randint(0, 1)'),
       ('j', 'randint(0, 2)'), ('j2', 'randint(0, 2)'),
       ('rows', '[[fr[0][0], v[0], v[1], v[2]], [fr[1][0], v[3], v[4], v[5]]]'), ('gen', 'fr[i][1]'), ('nums', 'take(drop(rows[i], 1), 3)'),
       ('days', "['w poniedziałek', 'we wtorek', 'w środę']"),
       ('txt', "('Ile kilogramów ' + gen + ' sprzedano ' + days[j] + '?') if ask == 0 else "
               "(('Ile kilogramów ' + gen + ' sprzedano w sumie w te trzy dni?') if ask == 1 else "
               "('O ile kilogramów więcej ' + gen + ' sprzedano ' + days[j] + ' niż ' + days[j2] + '?'))"),
       ('ans', 'nums[j] if ask == 0 else (sum(nums) if ask == 1 else nums[j] - nums[j2])')],
      number('Tabela pokazuje, ile kilogramów owoców sprzedano w sklepie. @{txt}', 'ans',
             [('idea', 'Znajdź w tabeli wiersz z owocami i kolumnę z dniem.'), ('conclude', 'Odpowiedź: @{ans}.')],
             media=[{'type': 'table', 'kind': 'table', 'essential': True, 'alt': 'Tabela sprzedaży owoców w trzy dni (kg).',
                     'params': {'headers': ['Owoc', 'poniedziałek', 'wtorek', 'środa'], 'rows': E('rows')}}]),
      constraints=['ask != 2 or (j != j2 and nums[j] > nums[j2])'], min_distinct=30, area=A4)

skill('ew-bar-chart', S, 'Odczytaj dane z diagramu słupkowego', ['I-III.4.a'],
      [lvl('Odczyt słupka', ask=0), lvl('Który słupek jest najwyższy?', ask=1), lvl('Różnica słupków', ask=2)],
      [('cats', "choice([['kot', 'pies', 'rybki', 'papuga'], ['lody', 'ciastka', 'owoce', 'czekolada'], ['rower', 'hulajnoga', 'rolki', 'deskorolka']])"),
       ('vs', 'sample(2, 15, 4)'), ('i', 'randint(0, 3)'), ('j', 'randint(0, 3)'),
       ('txt', "('Ile osób wybrało odpowiedź „' + cats[i] + '”?') if ask == 0 else "
               "(('Ile osób wybrało odpowiedź, którą wybrano najczęściej?') if ask == 1 else "
               "('O ile więcej osób wybrało „' + cats[i] + '” niż „' + cats[j] + '”?'))"),
       ('ans', 'vs[i] if ask == 0 else (max(vs) if ask == 1 else vs[i] - vs[j])')],
      number('Diagram słupkowy pokazuje wyniki ankiety w klasie. @{txt}', 'ans',
             [('idea', 'Znajdź słupek podpisany odpowiednią odpowiedzią i odczytaj jego wysokość.'), ('conclude', 'Odpowiedź: @{ans}.')],
             media=[{'type': 'chart', 'kind': 'bar', 'essential': True, 'alt': 'Diagram słupkowy z wynikami ankiety.', 'params': {'labels': E('cats'), 'values': E('vs')}}]),
      constraints=['ask != 2 or vs[i] > vs[j]'], min_distinct=30, area=A4)

skill('ew-price-list', S, 'Cennik', ['I-III.4.b', 'I-III.5.a'],
      [lvl('Ile kosztują oba?', ask=0), lvl('O ile różnią się ceny?', ask=1), lvl('Reszta z 20 zł', ask=2)],
      [('names', "shuffle(['bułka', 'sok', 'jogurt', 'ciastko', 'banan', 'woda', 'kanapka'])"), ('pr', 'sample(1, 9, 4)'),
       ('rows', '[[names[0], pr[0]], [names[1], pr[1]], [names[2], pr[2]], [names[3], pr[3]]]'), ('a', 'randint(0, 3)'), ('b', 'randint(0, 3)'),
       ('pair', "names[a] + ' i ' + names[b]"),
       ('txt', "('Ile zapłacisz za dwa produkty z cennika: ' + pair + '?') if ask == 0 else "
               "(('O ile złotych różnią się ceny produktów: ' + pair + '?') if ask == 1 else "
               "('Kupujesz dwa produkty z cennika: ' + pair + ', i płacisz banknotem 20 zł. Ile reszty dostaniesz?'))"),
       ('ans', 'pr[a] + pr[b] if ask == 0 else (abs(pr[b] - pr[a]) if ask == 1 else 20 - pr[a] - pr[b])')],
      quantity('Przeczytaj cennik w szkolnym sklepiku. @{txt}', 'ans', 'zł',
               [('idea', "@{('Dodaj ceny obu produktów.' if ask == 0 else ('Od większej ceny odejmij mniejszą.' if ask == 1 else 'Dodaj ceny, a potem odejmij od 20 zł.'))}"), ('conclude', 'Odpowiedź: @{ans} zł.')],
               media=[{'type': 'table', 'kind': 'table', 'essential': True, 'alt': 'Cennik w sklepiku szkolnym.', 'params': {'headers': ['Towar', 'Cena (zł)'], 'rows': E('rows')}}]),
      constraints=['a != b', 'ask != 1 or pr[b] != pr[a]'], tags=FIN, min_distinct=30, area=A4)

skill('ew-compare-sources', S, 'Gdzie taniej?', ['I-III.4.b'],
      [lvl('Dwa sklepy')],
      [('item', "choice(['zeszyt', 'długopis', 'plecak', 'piórnik', 'piłka'])"), ('p1', 'randint(3, 30)'), ('p2', 'randint(3, 30)')],
      number('W sklepie A cena towaru „@{item}” wynosi @{p1} zł, a w sklepie B – @{p2} zł. O ile złotych taniej kupisz w tańszym sklepie?', 'abs(p1 - p2)',
             [('idea', 'Porównaj dwie ceny i odejmij mniejszą od większej.'), ('compute', '@{max(p1, p2)} − @{min(p1, p2)} = @{abs(p1 - p2)}')]),
      constraints=['p1 != p2'], tags=FIN, min_distinct=30, area=A4)

skill('ew-tally', S, 'Zapisz wyniki w tabeli', ['I-III.4.c'],
      [lvl('Dwie odpowiedzi', k=2), lvl('Trzy odpowiedzi', k=3)],
      [('pool', "choice([['kot', 'pies', 'rybki'], ['lody', 'ciastka', 'owoce'], ['rower', 'hulajnoga', 'rolki'], ['czerwony', 'niebieski', 'zielony']])"),
       ('c', 'sample(2, 9, 3)'), ('answers', 'shuffle(repeat(pool[0], c[0]) + repeat(pool[1], c[1]) + (repeat(pool[2], c[2]) if k == 3 else []))'), ('i', 'randint(0, k - 1)')],
      number('Uczniowie wybierali ulubioną odpowiedź: @{join(answers, ", ")}. Przepisz wyniki do tabeli. Ile osób wybrało „@{pool[i]}”?', 'c[i]',
             [('idea', 'Policz odpowiedzi jedna po drugiej i stawiaj kreski w tabeli.'), ('conclude', '„@{pool[i]}”: @{c[i]}.')]),
      min_distinct=30, area=A4)

# ============================================================================ myślenie: teksty, zadania (5.a - 5.d)
skill('ew-read-timetable', S, 'Rozkład jazdy', ['I-III.5.a'],
      [lvl('Najbliższy odjazd')],
      [('t0', 'randint(6, 16) * 60 + randint(0, 3) * 15'), ('d1', 'randint(2, 5) * 10'), ('d2', 'randint(2, 5) * 10'), ('d3', 'randint(2, 5) * 10'),
       ('deps', '[t0, t0 + d1, t0 + d1 + d2, t0 + d1 + d2 + d3]'), ('k', 'randint(0, 2)'), ('now', 'deps[k] + randint(1, deps[k + 1] - deps[k] - 1)'), ('nxt', 'deps[k + 1]'),
       ('rows', '[[hhmm(deps[0])], [hhmm(deps[1])], [hhmm(deps[2])], [hhmm(deps[3])]]')],
      task('time-input', 'W tabeli podano godziny odjazdów autobusu. Jest godzina @{hhmm(now)}. O której odjedzie najbliższy autobus?', Time('hhmm(nxt)'),
           [('idea', 'Znajdź pierwszy odjazd, który jest później niż teraz.'), ('conclude', 'Najbliższy autobus odjedzie o @{hhmm(nxt)}.')],
           media=[{'type': 'table', 'kind': 'table', 'essential': True, 'alt': 'Rozkład jazdy: cztery odjazdy.', 'params': {'headers': ['Odjazdy'], 'rows': E('rows')}}]),
      min_distinct=30, area=A5, prereq=['ew-clock-read'])

skill('ew-wait-minutes', S, 'Ile minut czekać?', ['I-III.5.a'],
      [lvl('Czas oczekiwania')],
      [('t0', 'randint(6, 16) * 60 + randint(0, 3) * 15'), ('d1', 'randint(2, 5) * 10'), ('d2', 'randint(2, 5) * 10'), ('d3', 'randint(2, 5) * 10'),
       ('deps', '[t0, t0 + d1, t0 + d1 + d2, t0 + d1 + d2 + d3]'), ('k', 'randint(0, 2)'), ('now', 'deps[k] + randint(1, deps[k + 1] - deps[k] - 1)'), ('nxt', 'deps[k + 1]'),
       ('rows', '[[hhmm(deps[0])], [hhmm(deps[1])], [hhmm(deps[2])], [hhmm(deps[3])]]')],
      number('W tabeli podano godziny odjazdów autobusu. Jest godzina @{hhmm(now)}. Ile minut trzeba czekać na najbliższy autobus?', 'nxt - now',
             [('idea', 'Znajdź najbliższy odjazd i policz, ile minut dzieli go od teraz.'), ('compute', '@{hhmm(now)} → @{hhmm(nxt)}: @{nxt - now} min.')],
             media=[{'type': 'table', 'kind': 'table', 'essential': True, 'alt': 'Rozkład jazdy: cztery odjazdy.', 'params': {'headers': ['Odjazdy'], 'rows': E('rows')}}]),
      min_distinct=30, area=A5, prereq=['ew-read-timetable'])

skill('ew-recipe', S, 'Przepis kulinarny', ['I-III.5.a', 'I-III.5.c'],
      [lvl('Dwa razy więcej', md=20, f=2), lvl('Trzy razy więcej lub dwa razy mniej', md=20, f=3)],
      [('rec', "choice([[['naleśnik', 'naleśniki', 'naleśników'], 'mąki', 'g', 25], [['naleśnik', 'naleśniki', 'naleśników'], 'mleka', 'ml', 50], "
               "[['babeczka', 'babeczki', 'babeczek'], 'cukru', 'g', 10], [['babeczka', 'babeczki', 'babeczek'], 'masła', 'g', 20], "
               "[['porcja kisielu', 'porcje kisielu', 'porcji kisielu'], 'wody', 'ml', 100], [['kanapka', 'kanapki', 'kanapek'], 'szynki', 'g', 15], "
               "[['gofr', 'gofry', 'gofrów'], 'mąki', 'g', 30], [['placek', 'placki', 'placków'], 'jabłek', 'g', 40], "
               "[['kubek kakao', 'kubki kakao', 'kubków kakao'], 'mleka', 'ml', 200], [['szklanka kompotu', 'szklanki kompotu', 'szklanek kompotu'], 'wody', 'ml', 150]])"),
       ('base', 'choice([2, 4, 6])'), ('half', 'randint(0, 1) == 1 if f == 3 else False'), ('target', 'base // 2 if half else base * f'), ('per', 'rec[3]'),
       ('amount', 'per * target'),
       ('txt', "'Przepis na ' + pln(base, rec[0]) + ': ' + str(per * base) + ' ' + rec[2] + ' ' + rec[1] + '. Ile ' + rec[2] + ' ' + rec[1] + ' potrzeba na ' + pln(target, rec[0]) + '?'")],
      number('@{txt}', 'amount',
             [('idea', "@{('Liczby składników zmieniają się tyle razy, ile razy zmienia się liczba porcji.' if not half else 'Porcji jest dwa razy mniej, więc składników też dwa razy mniej.')}"),
              ('compute', "@{(str(per * base) + ' · ' + str(f) + ' = ' + str(amount) if not half else str(per * base) + ' : 2 = ' + str(amount))}")]),
      constraints=['target != base'], tags=('no-calculator',), area=A5)

skill('ew-calendar-week', S, 'Dni tygodnia', ['I-III.5.a'],
      [lvl('Za kilka dni', md=30, back=0), lvl('Kilka dni temu', md=30, back=1)],
      [('days', "['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']"), ('t', 'randint(0, 6)'), ('n', 'randint(2, 6)'),
       ('r', '(t - n) % 7 if back == 1 else (t + n) % 7'),
       ('txt', "('Dziś jest ' + days[t] + '. Jaki dzień tygodnia będzie za ' + pln(n, ['dzień', 'dni', 'dni']) + '?') if back == 0 else "
               "('Dziś jest ' + days[t] + '. Jaki dzień tygodnia był ' + pln(n, ['dzień', 'dni', 'dni']) + ' temu?')")],
      choice('@{txt}', 'days[r]', ['days[(r + 1) % 7]', 'days[(r + 2) % 7]', 'days[(r + 6) % 7]'],
             [('idea', 'Tydzień ma 7 dni: poniedziałek, wtorek, środa, czwartek, piątek, sobota, niedziela. Przesuwaj się po jednym dniu.'), ('conclude', 'Odpowiedź: @{days[r]}.')]),
      min_distinct=40, area=A5)

skill('ew-wp-add-sub', S, 'Zadania tekstowe: dodawanie i odejmowanie', ['I-III.5.b', 'I-III.5.c'],
      [lvl('Do 20', hi=20, kmin=0, kmax=2), lvl('Do 100', hi=100, kmin=0, kmax=2), lvl('Do 1000', hi=1000, kmin=0, kmax=2)],
      [('p', 'choice(' + PERSONS + ')'), ('q', 'choice(' + PERSONS + ')'), ('it', 'choice(' + ITEMS + ')'), ('k', 'randint(kmin, kmax)'),
       ('a', 'randint(hi // 4, hi // 2) // (1 if hi < 100 else 10) * (1 if hi < 100 else 10)'), ('b', 'randint(hi // 10 + 1, hi // 4) // (1 if hi < 100 else 10) * (1 if hi < 100 else 10)'),
       ('txt', "(p[0] + ' miał' + p[1] + ' ' + pln(a, it) + '. ' + p[0] + ' dostał' + p[1] + ' jeszcze ' + pln(b, it) + '. Ile ' + it[2] + ' ma teraz ' + p[0] + '?') if k == 0 else "
               "((p[0] + ' miał' + p[1] + ' ' + pln(a, it) + '. ' + p[0] + ' oddał' + p[1] + ' ' + pln(b, it) + '. Ile ' + it[2] + ' zostało?') if k == 1 else "
               "(p[0] + ' ma ' + pln(a + b, it) + ', a ' + q[0] + ' ma ' + pln(a, it) + '. O ile ' + it[2] + ' więcej ma ' + p[0] + '?'))"),
       ('ans', 'a + b if k == 0 else (a - b if k == 1 else b)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Dostał(a) jeszcze – więc dodajemy.' if k == 0 else ('Oddał(a) – więc odejmujemy.' if k == 1 else 'Porównujemy: odejmujemy mniejszą liczbę od większej.'))}"),
              ('conclude', "@{(str(a) + ' + ' + str(b) + ' = ' + str(a + b) if k == 0 else (str(a) + ' − ' + str(b) + ' = ' + str(a - b) if k == 1 else str(a + b) + ' − ' + str(a) + ' = ' + str(b)))}")]),
      constraints=['a > b', 'b > 0', 'p[0] != q[0]', 'k != 0 or a + b <= hi'], min_distinct=40, area=A5, prereq=['ew-add', 'ew-sub'])

skill('ew-wp-mul-div', S, 'Zadania tekstowe: mnożenie i dzielenie', ['I-III.5.b', 'I-III.5.c'],
      [lvl('Po równo w grupach', k=0), lvl('Dzielenie po równo', k=1), lvl('Ile razy więcej?', k=2)],
      [('it', 'choice(' + ITEMS + ')'), ('p', 'choice(' + PERSONS + ')'), ('q', 'choice(' + PERSONS + ')'), ('a', 'randint(2, 9)'), ('b', 'randint(2, 9)'),
       ('txt', "('Kupiono ' + pln(a, ['paczkę', 'paczki', 'paczek']) + ' po ' + pln(b, it) + '. Ile ' + it[2] + ' kupiono razem?') if k == 0 else "
               "(('Rozdzielono po równo ' + pln(a * b, it) + ' między ' + pln(a, ['osobę', 'osoby', 'osób']) + '. Ile ' + it[2] + ' dostała każda osoba?') if k == 1 else "
               "(p[0] + ' ma ' + pln(a * b, it) + ', a ' + q[0] + ' ma ' + pln(b, it) + '. Ile razy więcej ' + it[2] + ' ma ' + p[0] + '?'))"),
       ('ans', 'a * b if k == 0 else (b if k == 1 else a)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Mamy kilka takich samych grup – mnożymy.' if k == 0 else ('Dzielimy po równo – dzielimy.' if k == 1 else 'Pytanie „ile razy więcej” – dzielimy większą liczbę przez mniejszą.'))}"),
              ('conclude', "@{(str(a) + ' · ' + str(b) + ' = ' + str(a * b) if k == 0 else (str(a * b) + ' : ' + str(a) + ' = ' + str(b) if k == 1 else str(a * b) + ' : ' + str(b) + ' = ' + str(a)))}")]),
      constraints=['p[0] != q[0]', 'a != b'], min_distinct=30, area=A5, prereq=['ew-mul-table', 'ew-div-table'])

skill('ew-wp-two-step', S, 'Zadania tekstowe: dwa kroki', ['I-III.5.b', 'I-III.5.c'],
      [lvl('Zakupy i reszta', f=0), lvl('Dwie grupy', f=1)],
      [('p', 'choice(' + PERSONS + ')'), ('th', "choice([['zeszyt', 'zeszyty', 'zeszytów'], ['długopis', 'długopisy', 'długopisów'], ['pierniczek', 'pierniczki', 'pierniczków']])"),
       ('n', 'randint(2, 5)'), ('u', 'randint(2, 6)'), ('m', 'randint(2, 5)'), ('v', 'randint(2, 6)'), ('money', 'n * u + randint(3, 9)'),
       ('kr', "['kredka', 'kredki', 'kredek']"),
       ('txt', "(p[0] + ' miał' + p[1] + ' ' + str(money) + ' zł. Kupił' + p[1] + ' ' + pln(n, th) + ' po ' + str(u) + ' zł. Ile złotych zostało?') if f == 0 else "
               "('W jednym pudełku jest ' + pln(u, kr) + ', a w drugim ' + pln(v, kr) + '. Mamy ' + pln(n, ['pudełko', 'pudełka', 'pudełek']) + ' pierwszego rodzaju i ' + pln(m, ['pudełko', 'pudełka', 'pudełek']) + ' drugiego. Ile kredek mamy razem?')"),
       ('ans', 'money - n * u if f == 0 else n * u + m * v')],
      number('@{txt}', 'ans',
             [('idea', "@{('Najpierw policz, ile kosztowały zakupy, potem odejmij od pieniędzy.' if f == 0 else 'Policz osobno kredki z każdego rodzaju pudełek, potem dodaj.')}"),
              ('conclude', "@{(str(money) + ' − ' + str(n * u) + ' = ' + str(money - n * u) if f == 0 else str(n * u) + ' + ' + str(m * v) + ' = ' + str(n * u + m * v))}")]),
      constraints=['f != 0 or money > n * u'], tags=FIN, min_distinct=40, area=A5, prereq=['ew-wp-mul-div'])

skill('ew-puzzle-heads-legs', S, 'Kury i króliki', ['I-III.5.b'],
      [lvl('Głowy i nogi')],
      [('c', 'randint(2, 8)'), ('r', 'randint(2, 8)'), ('heads', 'c + r'), ('legs', '2 * c + 4 * r')],
      number('Na podwórku są kury (każda ma 2 nogi) i króliki (każdy ma 4 nogi). Razem jest @{heads} głów i @{legs} nóg. Ile jest kur?', 'c',
             [('idea', 'Spróbuj różnych liczb kur i królików (możesz narysować tabelkę). Sprawdzaj, czy liczba nóg się zgadza.'), ('conclude', 'Kur: @{c}, królików: @{r}. Nóg: @{2 * c} + @{4 * r} = @{legs}.')]),
      constraints=['c != r'], min_distinct=30, area=A5)

# ============================================================================ regularności, klasyfikacje, gry (5.e - 5.h)
skill('ew-sequence', S, 'Ciąg liczb: co będzie dalej?', ['I-III.5.f'],
      [lvl('Dodajemy to samo', kind=0), lvl('Odejmujemy to samo', kind=1), lvl('Podwajamy lub potrajamy', md=20, kind=2), lvl('Dodajemy coraz więcej', kind=3)],
      [('st', 'randint(2, 9)'), ('s0', 'randint(30, 60) if kind == 1 else (randint(1, 25) if kind == 2 else randint(1, 10))'), ('inc', 'randint(1, 3)'), ('mm', 'choice([2, 2, 3])'),
       ('seq', '[s0, s0 + st, s0 + 2 * st, s0 + 3 * st, s0 + 4 * st] if kind == 0 else ([s0, s0 - st, s0 - 2 * st, s0 - 3 * st, s0 - 4 * st] if kind == 1 else '
               '([s0, s0 * mm, s0 * mm * mm, s0 * pow(mm, 3), s0 * pow(mm, 4)] if kind == 2 else [s0, s0 + inc, s0 + 3 * inc, s0 + 6 * inc, s0 + 10 * inc]))'),
       ('shown', 'take(seq, 4)'), ('nxt', 'seq[4]')],
      number('Jaka liczba będzie następna? @{shown|list}, ___', 'nxt',
             [('idea', "@{('Dodajemy ciągle tę samą liczbę.' if kind == 0 else ('Odejmujemy ciągle tę samą liczbę.' if kind == 1 else ('Każda liczba jest ' + str(mm) + ' razy większa od poprzedniej.' if kind == 2 else 'Dodajemy coraz więcej: 1, 2, 3, 4… razy to samo.')))}"),
              ('conclude', 'Następna liczba: @{nxt}.')]),
      constraints=['kind != 2 or s0 * pow(mm, 4) <= 400', 'kind != 1 or seq[4] > 0'], min_distinct=20, area=A5)

skill('ew-rhythm', S, 'Rytm i powtarzający się wzór', ['I-III.5.f'],
      [lvl('Wzór z dwóch elementów', k=2), lvl('Wzór z trzech elementów', k=3), lvl('Wzór z czterech elementów', k=4)],
      [('syms', "shuffle(['A', 'B', 'C', 'D', 'E'])"), ('pat', 'take(syms, k)'),
       ('shown', '[pat[0], pat[1 % k], pat[2 % k], pat[3 % k], pat[4 % k], pat[5 % k], pat[6 % k]]'), ('nxt', 'pat[7 % k]'), ('idx', 'index(syms, nxt)')],
      choice('Jaki znak będzie następny w ciągu: @{join(shown, " ")} ___ ?', 'nxt', ['syms[(idx + 1) % 5]', 'syms[(idx + 2) % 5]', 'syms[(idx + 3) % 5]'],
             [('idea', 'Znajdź powtarzający się fragment: @{join(pat, " ")}. Potem sprawdź, który znak jest na kolejnym miejscu.'), ('conclude', 'Następny znak: @{nxt}.')]),
      min_distinct=20, area=A5)

ODD_GROUPS = ("[['jabłko', 'gruszka', 'śliwka', 'banan', 'truskawka'], ['marchewka', 'ogórek', 'pomidor', 'cebula', 'ziemniak'], ['kot', 'pies', 'chomik', 'królik', 'papuga'], "
              "['sosna', 'dąb', 'brzoza', 'świerk', 'buk'], ['linijka', 'ołówek', 'gumka', 'temperówka', 'cyrkiel'], ['młotek', 'śrubokręt', 'piła', 'wiertarka', 'obcęgi']]")
skill('ew-odd-one-out', S, 'Co nie pasuje?', ['I-III.5.g'],
      [lvl('Znajdź intruza')],
      [('groups', ODD_GROUPS), ('g1', 'randint(0, 5)'), ('g2', '(g1 + randint(1, 5)) % 6'), ('a', 'shuffle(groups[g1])'), ('b', 'groups[g2]'), ('odd', 'choice(b)')],
      choice('Który wyraz nie pasuje do pozostałych: @{a[0]}, @{a[1]}, @{a[2]}, …', 'odd', ['a[0]', 'a[1]', 'a[2]'],
             [('idea', 'Zastanów się, co łączy trzy wyrazy. Ten, który nie pasuje, należy do innej grupy.'), ('conclude', 'Intruz: @{odd}.')]),
      min_distinct=40, area=A5)

skill('ew-odd-one-out-num', S, 'Liczba, która nie pasuje', ['I-III.5.g'],
      [lvl('Parzyste i nieparzyste', mode=0), lvl('Wielokrotności', mode=1)],
      [('d', 'choice([5, 3, 10]) if mode == 1 else 2'), ('base', 'sample(1, 9, 4)'),
       ('good', '[d * base[0], d * base[1], d * base[2]]'), ('bad', 'd * base[3] + (1 if d == 2 else randint(1, d - 1))'), ('all', 'shuffle(good + [bad])')],
      choice('Trzy z czterech liczb: @{all|list} mają wspólną cechę. Która liczba nie pasuje do pozostałych?', 'bad', ['good[0]', 'good[1]', 'good[2]'],
             [('idea', "Sprawdź, co mają wspólnego trzy liczby: @{('wszystkie są parzyste' if d == 2 else 'wszystkie dzielą się przez ' + str(d))}."), ('conclude', 'Niepasująca liczba: @{bad}.')]),
      constraints=['bad % d != 0'], min_distinct=20, area=A5)

skill('ew-classify-criterion', S, 'Co łączy te liczby?', ['I-III.5.g'],
      [lvl('Nazwij wspólną cechę')],
      [('c', 'randint(0, 3)'), ('s', 'sample(1, 12, 4)'),
       ('xs', '[2 * s[0], 2 * s[1], 2 * s[2], 2 * s[3]] if c == 0 else ([2 * s[0] + 1, 2 * s[1] + 1, 2 * s[2] + 1, 2 * s[3] + 1] if c == 1 else '
              '([5 * s[0], 5 * s[1], 5 * s[2], 5 * s[3]] if c == 2 else [3 * s[0], 3 * s[1], 3 * s[2], 3 * s[3]]))'),
       ('r2', 'xs[0] % 2 + xs[1] % 2 + xs[2] % 2 + xs[3] % 2'), ('r3', 'xs[0] % 3 + xs[1] % 3 + xs[2] % 3 + xs[3] % 3'), ('r5', 'xs[0] % 5 + xs[1] % 5 + xs[2] % 5 + xs[3] % 5'),
       ('fits', '(1 if r2 == 0 else 0) + (1 if r2 == 4 else 0) + (1 if r5 == 0 else 0) + (1 if r3 == 0 else 0)'),
       ('names', "['parzyste', 'nieparzyste', 'podzielne przez 5', 'podzielne przez 3']")],
      choice('Co łączy wszystkie liczby: @{xs|list}? Wszystkie są …', 'names[c]', ['names[(c + 1) % 4]', 'names[(c + 2) % 4]', 'names[(c + 3) % 4]'],
             [('idea', 'Sprawdź każdą cechę po kolei: czy pasuje do wszystkich czterech liczb?'), ('conclude', 'Wszystkie są @{names[c]}.')]),
      constraints=['fits == 1'], min_distinct=30, area=A5)

skill('ew-nim', S, 'Gra: kto zabierze ostatni patyczek?', ['I-III.5.e'],
      [lvl('Można wziąć 1 lub 2', k=2), lvl('Można wziąć 1, 2 lub 3', k=3)],
      [('n', 'randint(6, 20)'), ('first', 'n % (k + 1)')],
      number('W grze są @{n} patyczków. Gracze na zmianę zabierają od 1 do @{k} patyczków. Wygrywa ten, kto zabierze ostatni patyczek. Ty zaczynasz. Ile patyczków zabierzesz na początku, żeby wygrać?', 'first',
             [('idea', 'Doprowadź do sytuacji, w której zostanie liczba patyczków podzielna przez @{k + 1}: wtedy rywal nie może wygrać.'),
              ('conclude', 'Zabierasz @{first}, zostaje @{n - first}. Potem odpowiadasz tak, aby razem z rywalem zabrać zawsze @{k + 1}.')]),
      constraints=['first != 0'], min_distinct=10, area=A5)

skill('ew-saving', S, 'Oszczędzanie kieszonkowego', ['I-III.5.h', 'I-III.2.h'],
      [lvl('Po ilu tygodniach?', mode=0), lvl('Ile uzbieram?', mode=1), lvl('Ile brakuje?', mode=2)],
      [('week', 'choice([2, 3, 4, 5, 10])'), ('have', 'randint(1, 3) * week'), ('weeks', 'randint(2, 9)'), ('goal', 'have + weeks * week'),
       ('txt', "('Franek ma ' + str(have) + ' zł i chce uzbierać ' + str(goal) + ' zł. Co tydzień odkłada ' + str(week) + ' zł. Po ilu tygodniach uzbiera tyle pieniędzy?') if mode == 0 else "
               "(('Ola ma ' + str(have) + ' zł. Co tydzień odkłada ' + str(week) + ' zł. Ile złotych będzie miała po ' + pln(weeks, ['tygodniu', 'tygodniach', 'tygodniach']) + '?') if mode == 1 else "
               "('Maja chce kupić grę za ' + str(goal) + ' zł. Ma już ' + str(have) + ' zł. Ile złotych jeszcze jej brakuje?'))"),
       ('ans', 'weeks if mode == 0 else (goal if mode == 1 else goal - have)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Podziel to, co jeszcze trzeba uzbierać, przez kwotę odkładaną co tydzień.' if mode == 0 else ('Dodaj odłożone pieniądze do tego, co już masz.' if mode == 1 else 'Odejmij to, co masz, od ceny.'))}"), ('conclude', 'Odpowiedź: @{ans}.')]),
      tags=FIN, min_distinct=30, area=A5, prereq=['ew-shopping'])

# ============================================================================ banki
bank_tasks = [
    bank_find_mistake('Ola obliczała 15 + 7. Zobacz jej kroki. W którym kroku jest błąd?',
                      ['15 + 5 = 20.', 'Do dodania zostało jeszcze 3.', '20 + 3 = 23.', 'Wynik: 23.'], 2,
                      [('check', '7 − 5 = 2, więc do dodania zostały jeszcze 2. Poprawny wynik to 22.')]),
    bank_find_mistake('Kuba obliczał 30 − 12. W którym kroku jest błąd?',
                      ['30 − 10 = 20.', '20 − 2 = 18.', 'Wynik: 18.'], None,
                      [('check', 'Sprawdzamy: 18 + 12 = 30. Nie ma błędu.')]),
    bank_find_mistake('Maja obliczała 6 · 4. W którym kroku jest błąd?',
                      ['Mnożenie to dodawanie jednakowych liczb.', '6 · 4 to 4 razy po 6.', '6 + 6 + 6 = 18.', 'Wynik: 18.'], 3,
                      [('check', 'Dodać trzeba cztery szóstki: 6 + 6 + 6 + 6 = 24.')]),
    bank_find_mistake('Franek dzielił 20 : 4. W którym kroku jest błąd?',
                      ['Szukam liczby, która razy 4 da 20.', '4 · 5 = 20.', 'Zatem 20 : 4 = 5.'], None,
                      [('check', '5 · 4 = 20. Nie ma błędu.')]),
    bank_find_mistake('Zosia odczytała z zegara: „Kwadrans po trzeciej to 3:45”. W którym kroku jest błąd?',
                      ['Kwadrans to 15 minut.', 'Po trzeciej znaczy: po godzinie 3:00.', '3:00 + 15 minut = 3:45.', 'Wynik: 3:45.'], 3,
                      [('check', '3:00 + 15 minut = 3:15.')]),
    bank_find_mistake('Adam zamieniał 2 m na centymetry. W którym kroku jest błąd?',
                      ['1 m = 100 cm.', '2 m to dwa razy po 100 cm.', '2 · 100 = 20.', 'Wynik: 2 m = 20 cm.'], 3,
                      [('check', '2 · 100 = 200, więc 2 m = 200 cm.')]),
    bank_find_mistake('Ewa zapisała cenę 3 zł 5 gr jako 3,50 zł. W którym kroku jest błąd?',
                      ['1 zł = 100 gr.', 'Grosze piszemy po przecinku jako dwie cyfry.', '5 gr to 05, więc 3 zł 5 gr = 3,50 zł.', 'Wynik: 3,50 zł.'], 3,
                      [('check', '3 zł 5 gr = 3,05 zł. Zapis 3,50 zł to 3 zł 50 gr.')]),
    bank_find_mistake('Piotr zapisał: „Liczba 47 jest parzysta, bo ma cyfrę 4”. W którym kroku jest błąd?',
                      ['Liczba parzysta kończy się cyfrą 0, 2, 4, 6 lub 8.', 'Liczba 47 ma cyfry 4 i 7.', 'Cyfra 4 jest parzysta.', 'Zatem 47 jest parzysta.'], 3,
                      [('check', 'Liczy się ostatnia cyfra. 47 kończy się cyfrą 7, więc jest nieparzysta.')]),
    bank_find_mistake('Leon obliczał 25 + 38. W którym kroku jest błąd?',
                      ['25 + 30 = 55.', '55 + 8 = 63.', 'Wynik: 63.'], None,
                      [('check', '63 − 38 = 25. Nie ma błędu.')]),
    bank_find_mistake('Hania obliczała temperaturę: było 3 °C, spadło o 5 stopni. W którym kroku jest błąd?',
                      ['Temperatura spadła, więc odejmujemy.', '3 − 5 = 2.', 'Wynik: 2 °C.'], 2,
                      [('check', '3 − 5 = −2. Temperatura wynosi −2 °C, czyli poniżej zera.')]),
    bank_find_mistake('Staś liczył połowę z 18. W którym kroku jest błąd?',
                      ['Połowa to dzielenie przez 2.', '18 : 2 = 8.', 'Wynik: połowa z 18 to 8.'], 2,
                      [('check', '18 : 2 = 9, bo 9 + 9 = 18.')]),
    bank_find_mistake('Julia mówi: „Prostokąt ma 3 boki”. W którym kroku jest błąd?',
                      ['Trójkąt ma 3 boki.', 'Prostokąt ma cztery kąty proste.', 'Zatem prostokąt ma 3 boki.'], 3,
                      [('check', 'Prostokąt ma 4 boki, bo ma 4 kąty (i 4 wierzchołki).')]),
]
assert 15 + 7 == 22 and 30 - 12 == 18 and 6 * 4 == 24 and 25 + 38 == 63 and 3 - 5 == -2 and 18 // 2 == 9
bank_skill('ew-find-mistake', S, 'Detektyw błędów', ['I-III.5.d', 'I-III.5.c'], bank_tasks, levels=['Znajdź błąd w rozwiązaniu'], tags=('thinking',), area=A5,
           intro='Czasem rozwiązanie ma błąd. Czytaj po kolei każdy krok i sprawdzaj go. Możesz też sprawdzić wynik działaniem odwrotnym.')

game_tasks = [
    bank_choice('W grze „Kółko i krzyżyk” na planszy 3 × 3 gracz stawia swój znak na pierwszym ruchu. Które pole daje najwięcej możliwości ułożenia trzech znaków w linii?',
                [('Pole w środku planszy', True), ('Pole w rogu', False), ('Pole na środku boku', False), ('Każde pole jest tak samo dobre', False)],
                [('idea', 'Przez środek planszy przechodzi najwięcej linii: 4 (dwie przekątne, jedna pozioma i jedna pionowa).')]),
    bank_choice('Gra: dwoje graczy na zmianę dokłada monetę na stół. Moneta nie może leżeć na innej. Przegrywa ten, kto nie może dołożyć. Co warto zrobić na początku?',
                [('Położyć monetę dokładnie na środku stołu i potem odpowiadać symetrycznie.', True), ('Położyć monetę na brzegu.', False), ('Położyć kilka monet w jednym miejscu.', False), ('Poczekać, aż rywal zacznie.', False)],
                [('idea', 'Strategia symetrii: po ruchu rywala zawsze możesz ułożyć swoją monetę „po przeciwnej stronie” środka.')]),
    bank_choice('W grze w kości rzucasz jedną kostką. Które liczby wypadają równie często?',
                [('Wszystkie liczby od 1 do 6 mają taką samą szansę.', True), ('Szóstka wypada najrzadziej.', False), ('Jedynka wypada najczęściej.', False), ('Liczby parzyste wypadają częściej.', False)],
                [('idea', 'Uczciwa kostka ma 6 jednakowych ścian, więc każda ma taką samą szansę.')]),
    bank_choice('W grze w domino układamy kostki tak, żeby sąsiednie pola miały tyle samo oczek. Po polu z 3 oczkami możesz położyć kostkę, która ma po jednej stronie:',
                [('3 oczka', True), ('4 oczka', False), ('0 oczek', False), ('6 oczek', False)],
                [('idea', 'Sąsiadujące końce muszą mieć tyle samo oczek.')]),
    bank_choice('Gra: na stole leży 5 zapałek. Gracze na zmianę zabierają 1 albo 2 zapałki. Wygrywa ten, kto zabierze ostatnią. Zaczynasz. Ile zapałek warto zabrać?',
                [('2 zapałki (zostaną 3 – rywal nie może wygrać)', True), ('1 zapałkę', False), ('Nie ma znaczenia', False), ('Żadnej – trzeba zabrać co najmniej 3', False)],
                [('idea', 'Zostaw rywalowi liczbę zapałek podzielną przez 3, a potem zawsze dobieraj tak, by razem zabrać 3.')]),
    bank_choice('W szachownicy 8 × 8 pola mają na przemian kolor biały i czarny. Ile jest białych pól?',
                [('32', True), ('16', False), ('64', False), ('24', False)],
                [('idea', 'Pól jest 64, a kolory na przemian: połowa z 64 to 32.')]),
]
bank_skill('ew-games', S, 'Gry i strategie', ['I-III.5.e'], game_tasks, levels=['Pomyśl jak gracz'], tags=('thinking',), area=A5,
           intro='W grach planszowych i kościanych pomaga myślenie z wyprzedzeniem: co zrobi rywal po moim ruchu? Szukamy ruchu, który daje większą szansę wygranej.')

# ============================================================================ ścieżka
un = Unit(S, 'ew-u9', 'Dane i tabele', 'Czytamy tabele, diagramy i cenniki.', 'chart', area=A4)
un.learn('ew-table-read').learn('ew-bar-chart').learn('ew-price-list').learn('ew-compare-sources').learn('ew-tally')
un.checkpoint(['ew-table-read', 'ew-bar-chart', 'ew-price-list', 'ew-compare-sources', 'ew-tally'])

un = Unit(S, 'ew-u10', 'Zadania z życia', 'Rozkład jazdy, przepisy, kalendarz i zadania tekstowe.', 'book', area=A5)
un.learn('ew-read-timetable').learn('ew-wait-minutes').learn('ew-recipe').learn('ew-calendar-week')
un.review('Powtórka: czytamy teksty z liczbami', ['ew-read-timetable', 'ew-wait-minutes', 'ew-recipe', 'ew-calendar-week'])
un.learn('ew-wp-add-sub').learn('ew-wp-mul-div').learn('ew-wp-two-step').learn('ew-puzzle-heads-legs')
un.checkpoint(['ew-read-timetable', 'ew-recipe', 'ew-wp-add-sub', 'ew-wp-mul-div', 'ew-wp-two-step'])

un = Unit(S, 'ew-u11', 'Myślenie matematyczne', 'Rytmy, ciągi, klasyfikowanie, gry i szukanie błędów.', 'brain', area=A5)
un.learn('ew-sequence').learn('ew-rhythm').learn('ew-odd-one-out').learn('ew-odd-one-out-num').learn('ew-classify-criterion')
un.learn('ew-nim').learn('ew-games', levels=[1], tasks=5).learn('ew-saving').learn('ew-find-mistake', levels=[1], tasks=6)
un.checkpoint(['ew-sequence', 'ew-rhythm', 'ew-odd-one-out', 'ew-odd-one-out-num', 'ew-nim'])
