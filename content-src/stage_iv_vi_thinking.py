"""Stage IV-VI, area 6 (Myślenie matematyczne) and word problems.
Objectives: IV-VI.6.1-6.3, 1.38 (calculator), 2.14 (digital tools)."""
from dsl import *

S = 'IV-VI'
A6 = 'IV-VI.6'
FIN = ('finance', 'no-calculator')
PERSONS = "[['Ola', 'a'], ['Kasia', 'a'], ['Ania', 'a'], ['Tomek', ''], ['Marek', ''], ['Kuba', '']]"
THINGS = ("[['zeszyt', 'zeszyty', 'zeszytów'], ['długopis', 'długopisy', 'długopisów'], ['kredka', 'kredki', 'kredek'], "
          "['gumka', 'gumki', 'gumek'], ['linijka', 'linijki', 'linijek'], ['teczka', 'teczki', 'teczek']]")

# ============================================================================ zadania tekstowe (6.1)
skill('n46-wp-shopping', S, 'Zakupy: zadania tekstowe', ['IV-VI.6.1.a', 'IV-VI.6.1.b', 'IV-VI.1.9'],
      [lvl('Dwa towary: razem', mode=0), lvl('Reszta z banknotu', mode=1), lvl('Trzy towary', mode=2)],
      [('p', 'choice(' + PERSONS + ')'), ('th', 'shuffle(' + THINGS + ')'), ('a', 'randint(2, 8)'), ('b', 'randint(2, 6)'), ('c', 'randint(2, 5)'),
       ('u1', 'randint(2, 9)'), ('u2', 'randint(2, 9)'), ('u3', 'randint(2, 9)'),
       ('cost', 'a * u1 + b * u2 + (c * u3 if mode == 2 else 0)'), ('bill', 'choice([50, 100])'),
       ('first', "p[0] + ' kupił' + p[1] + ' ' + pln(a, th[0]) + ' po ' + str(u1) + ' zł i ' + pln(b, th[1]) + ' po ' + str(u2) + ' zł'"),
       ('txt', "first + (' oraz ' + pln(c, th[2]) + ' po ' + str(u3) + ' zł' if mode == 2 else '') + ('. Zapłacił' + p[1] + ' banknotem ' + str(bill) + ' zł. Ile reszty otrzymał' + p[1] + '?' if mode == 1 else '. Ile zapłacił' + p[1] + ' za wszystkie zakupy?')"),
       ('ans', 'cost if mode != 1 else bill - cost')],
      number('@{txt}', 'ans',
             [('idea', 'Policz osobno koszt każdego towaru (liczba sztuk razy cena), potem dodaj koszty@{(\' i odejmij od banknotu\' if mode == 1 else \'\')}.'),
              ('compute', "@{(str(a) + ' · ' + str(u1) + ' + ' + str(b) + ' · ' + str(u2) + (' + ' + str(c) + ' · ' + str(u3) if mode == 2 else '') + ' = ' + str(cost) + ' zł' + ((', reszta: ' + str(bill) + ' − ' + str(cost) + ' = ' + str(bill - cost) + ' zł') if mode == 1 else ''))}")],
             errors=[('answer_cost', Int('cost'), 'To jest koszt zakupów. Zadanie pyta o resztę z banknotu.', 'mode == 1')]),
      constraints=['mode != 1 or bill > cost', 'len(uniq([th[0][0], th[1][0], th[2][0]])) == 3'], tags=FIN, min_distinct=40, area=A6, prereq=['n46-total-cost'],
      intro='Przy zadaniach tekstowych najpierw zapisz, co wiesz i o co pytają. Potem zaplanuj kroki: co policzysz najpierw, a co potem. Na końcu sprawdź, czy wynik jest sensowny.')

skill('n46-wp-sum-difference', S, 'Suma i różnica, suma i iloraz', ['IV-VI.6.1.a', 'IV-VI.6.1.b'],
      [lvl('Suma i różnica', mode=0), lvl('Suma i „ile razy więcej”', mode=1)],
      [('p', 'choice(' + PERSONS + ')'), ('q', 'choice(' + PERSONS + ')'), ('th', "choice([['naklejka', 'naklejki', 'naklejek'], ['kartka', 'kartki', 'kartek'], ['moneta', 'monety', 'monet'], ['książka', 'książki', 'książek']])"),
       ('small', 'randint(5, 40)'), ('d', 'randint(2, 12)'), ('k', 'randint(2, 5)'),
       ('big', 'small + d if mode == 0 else small * k'), ('total', 'small + big'),
       ('txt', "(p[0] + ' ma o ' + pln(d, th) + ' więcej niż ' + q[0] + '. Razem mają ' + pln(total, th) + '. Ile ' + th[2] + ' ma ' + q[0] + '?') if mode == 0 else "
               "(p[0] + ' ma ' + str(k) + ' razy więcej ' + th[2] + ' niż ' + q[0] + '. Razem mają ' + pln(total, th) + '. Ile ' + th[2] + ' ma ' + q[0] + '?')")],
      number('@{txt}', 'small',
             [('idea', "@{('Gdyby oboje mieli tyle samo co mniejsza liczba, razem mieliby o różnicę mniej. Odejmij różnicę od sumy i podziel na dwie równe części.' if mode == 0 else 'Narysuj odcinki: mniejsza liczba to 1 część, większa to ' + str(k) + ' części. Razem ' + str(k + 1) + ' części.')}"),
              ('compute', "@{(str(total) + ' − ' + str(d) + ' = ' + str(total - d) + '; ' + str(total - d) + ' : 2 = ' + str(small) if mode == 0 else str(total) + ' : ' + str(k + 1) + ' = ' + str(small))}")]),
      constraints=['p[0] != q[0]', 'mode != 0 or (total - d) % 2 == 0'], min_distinct=40, area=A6, prereq=['n46-wp-shopping'])

skill('n46-wp-reverse', S, 'Działania odwrotne: jaką liczbę pomyślałem?', ['IV-VI.6.1.b', 'IV-VI.6.3.b'],
      [lvl('Dwa działania', ops=2), lvl('Trzy działania', ops=3)],
      [('x', 'randint(2, 12)'), ('a', 'randint(2, 6)'), ('b', 'randint(2, 15)'), ('c', 'randint(2, 5)'),
       ('r1', 'x * a'), ('r2', 'r1 + b'), ('r3', 'r2 * c'),
       ('txt', "'Pomyślałem liczbę, pomnożyłem ją przez ' + str(a) + ', dodałem ' + str(b) + (', wynik pomnożyłem przez ' + str(c) if ops == 3 else '') + ' i otrzymałem ' + str(r2 if ops == 2 else r3) + '. Jaką liczbę pomyślałem?'")],
      number('@{txt}', 'x',
             [('idea', 'Cofamy działania od końca: odwrotnością mnożenia jest dzielenie, a dodawania – odejmowanie.'),
              ('compute', "@{((str(r3) + ' : ' + str(c) + ' = ' + str(r2) + '; ') if ops == 3 else '') + str(r2) + ' − ' + str(b) + ' = ' + str(r1) + '; ' + str(r1) + ' : ' + str(a) + ' = ' + str(x)}")]),
      selfCheck=['(x * a + b) * (c if ops == 3 else 1) == (r2 if ops == 2 else r3)'], min_distinct=40, area=A6, prereq=['n46-alg-solve'])

skill('n46-wp-proportion', S, 'Rozumowanie proporcjonalne', ['IV-VI.6.3.d'],
      [lvl('Cena i liczba sztuk', ctx=0), lvl('Droga i czas', ctx=1), lvl('Przepis dla większej liczby osób', ctx=2)],
      [('k', 'randint(2, 6)'), ('u', 'randint(2, 12)'), ('n', 'randint(k + 1, 15)'), ('total', 'k * u'), ('ans', 'n * u'),
       ('txt', "('Za ' + pln(k, ['zeszyt', 'zeszyty', 'zeszytów']) + ' zapłacono ' + str(total) + ' zł. Ile złotych kosztuje ' + pln(n, ['zeszyt', 'zeszyty', 'zeszytów']) + ' w tej samej cenie?') if ctx == 0 else "
               "(('Rowerzysta w ciągu ' + pln(k, ['godziny', 'godzin', 'godzin']) + ' przejeżdża ' + str(total) + ' km. Ile kilometrów przejedzie w ciągu ' + pln(n, ['godziny', 'godzin', 'godzin']) + ' jadąc tak samo szybko?') if ctx == 1 else "
               "('Do ciasta dla ' + pln(k, ['osoby', 'osób', 'osób']) + ' potrzeba ' + str(total * 10) + ' g mąki. Ile gramów mąki potrzeba na takie samo ciasto dla ' + pln(n, ['osoby', 'osób', 'osób']) + '?'))"),
       ('res', 'ans if ctx < 2 else ans * 10')],
      number('@{txt}', 'res',
             [('idea', 'Najpierw policz, ile przypada na jedną sztukę (godzinę, osobę): podziel. Potem pomnóż przez żądaną liczbę.'),
              ('compute', "@{(str(total if ctx < 2 else total * 10) + ' : ' + str(k) + ' = ' + str(u if ctx < 2 else u * 10) + '; ' + str(u if ctx < 2 else u * 10) + ' · ' + str(n) + ' = ' + str(res))}")],
             errors=[('add_difference', Int('total + (n - k) * (1 if ctx < 2 else 10)'), 'Gdy liczba sztuk rośnie, wynik rośnie proporcjonalnie (mnożymy), a nie o tyle samo.', 'total + (n - k) * (1 if ctx < 2 else 10) != res')]),
      constraints=['n != k'], min_distinct=40, area=A6, prereq=['n46-wp-shopping'])

skill('n46-sense-check', S, 'Czy wynik jest sensowny?', ['IV-VI.6.1.c', 'IV-VI.1.37'],
      [lvl('Zakupy: przecinek w złym miejscu')],
      [('it', "choice([['ziemniaków', 'kg'], ['jabłek', 'kg'], ['wędliny', 'kg'], ['pomidorów', 'kg']])"), ('qty', 'randint(2, 9)'), ('price', 'randint(8, 40) * 10 / 100'),
       ('res', 'qty * price')],
      choice('Marek kupił @{qty} kg @{it[0]} po @{price|money} za kilogram. Zanim policzył dokładnie, chciał ocenić, ile mniej więcej zapłaci. Który wynik jest sensowny?',
             "fmt(res, 2) + ' zł'", ["fmt(res / 10, 2) + ' zł'", "fmt(res * 10, 2) + ' zł'", "fmt(res / 100, 2) + ' zł'"],
             [('idea', 'Oszacuj: zaokrąglij ilość i cenę. @{qty} kg po około @{round(price, 0)|int} zł to około @{qty * round(price, 0)|int} zł.'),
              ('conclude', 'Dokładnie: @{qty} · @{price|dec:2} = @{res|dec:2} zł.')]),
      constraints=['denom(res) in divisors(100)', 'res >= 5', 'price != round(price, 0)'], tags=FIN, min_distinct=30, area=A6, prereq=['n46-estimate-product'])

# ============================================================================ rozumowania (6.3)
skill('n46-examples', S, 'Liczba spełniająca warunki', ['IV-VI.6.3.a'],
      [lvl('Dwa warunki')],
      [('d1', 'choice([2, 3, 4, 5, 9])'), ('d2', 'choice([3, 4, 5, 6, 7])'), ('lim', 'randint(2, 8) * 10'), ('l', 'lcm(d1, d2)'),
       ('m', 'lim // l + randint(1, 2)'), ('good', 'l * m'),
       ('w1', 'd1 * (randint(lim // d1 + 1, lim // d1 + 6))'), ('w2', 'd2 * (randint(lim // d2 + 1, lim // d2 + 6))'), ('w3', 'l * (lim // l)')],
      choice('Którą liczbę można wpisać? Szukamy liczby większej od @{lim}, podzielnej przez @{d1} i przez @{d2}.', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Sprawdź po kolei wszystkie warunki. Liczba musi spełniać każdy z nich.'),
              ('conclude', '@{good} : @{d1} = @{good // d1}, @{good} : @{d2} = @{good // d2}, a @{good} > @{lim}.')]),
      constraints=['d1 != d2', 'w1 % d2 != 0', 'w2 % d1 != 0', 'w3 <= lim', 'w3 > 0', 'good > lim', 'good % d1 == 0', 'good % d2 == 0'],
      selfCheck=['w1 > lim', 'w2 > lim'], min_distinct=40, area=A6)

skill('n46-counterexample', S, 'Kontrprzykład', ['IV-VI.6.3.a'],
      [lvl('Obal twierdzenie', md=15)],
      [('s', 'randint(0, 3)'), ('k', 'randint(1, 8)'),
       ('stmts', "['Każda liczba podzielna przez 3 jest nieparzysta.', 'Każda liczba parzysta jest podzielna przez 4.', 'Każda liczba pierwsza jest nieparzysta.', 'Każda liczba podzielna przez 6 jest podzielna przez 12.']"),
       ('good', '[6 * k, 4 * k + 2, 2, 6 * (2 * k - 1)][s]'),
       ('w1', '[3 * (2 * k + 1), 4 * k, 3, 12 * k][s]'), ('w2', '[4 * k + 1, 2 * (2 * k + 1) + 1, 5, 6 * k + 1][s]'), ('w3', '[2 * (3 * k + 1) + 1, 8 * k, 7, 12 * k + 12][s]')],
      choice('Kuba twierdzi: „@{stmts[s]}”. Który przykład pokazuje, że Kuba się myli?', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Kontrprzykład to liczba, która spełnia założenie twierdzenia, ale nie spełnia jego wniosku.'),
              ('conclude', 'Liczba @{good} jest kontrprzykładem.')]),
      constraints=['len(uniq([good, w1, w2, w3])) == 4'],
      selfCheck=['s != 0 or (good % 3 == 0 and good % 2 == 0)', 's != 1 or (good % 2 == 0 and good % 4 != 0)', 's != 2 or (is_prime(good) and good % 2 == 0)', 's != 3 or (good % 6 == 0 and good % 12 != 0)',
                 's != 0 or (w1 % 3 == 0 and w1 % 2 == 1)', 's != 1 or w1 % 4 == 0', 's != 2 or (is_prime(w1) and w1 % 2 == 1)', 's != 3 or w1 % 12 == 0'],
      min_distinct=20, area=A6, prereq=['n46-examples'])

skill('n46-sum-product', S, 'Metoda prób i poprawek', ['IV-VI.6.3.b'],
      [lvl('Dwie liczby: suma i iloczyn', md=40, mode=0), lvl('Cyfry liczby dwucyfrowej', md=25, mode=1)],
      [('a', 'randint(2, 12)'), ('b', 'randint(a + 1, 15)'), ('c', 'randint(1, 8)'), ('d', 'randint(c + 1, 9)'),
       ('txt', "('Dwie liczby naturalne mają sumę ' + str(a + b) + ' i iloczyn ' + str(a * b) + '. Jaka jest większa z tych liczb?') if mode == 0 else "
               "('Cyfry pewnej liczby dwucyfrowej mają sumę ' + str(c + d) + ' i iloczyn ' + str(c * d) + '. Jaka jest największa liczba dwucyfrowa o takich cyfrach?')"),
       ('ans', 'b if mode == 0 else 10 * d + c')],
      number('@{txt}', 'ans',
             [('idea', 'Wypisuj pary liczb o danej sumie i sprawdzaj ich iloczyn. Poprawiaj próbę, aż iloczyn się zgodzi.'),
              ('compute', "@{(str(a) + ' + ' + str(b) + ' = ' + str(a + b) + ' i ' + str(a) + ' · ' + str(b) + ' = ' + str(a * b) if mode == 0 else 'Cyfry: ' + str(c) + ' i ' + str(d) + '; największa liczba: ' + str(10 * d + c))}")]),
      constraints=['mode != 1 or c * d != 0'], selfCheck=['mode != 0 or ans * (a + b - ans) == a * b'], min_distinct=40, area=A6, prereq=['n46-wp-sum-difference'])

skill('n46-count-cases', S, 'Rozważ wszystkie przypadki', ['IV-VI.6.3.c'],
      [lvl('Zestawy ubrań', md=20, mode=0), lvl('Liczby z podanych cyfr', md=30, mode=1), lvl('Mecze w turnieju', md=10, mode=2)],
      [('n', 'randint(2, 6)'), ('m', 'randint(2, 6)'), ('t', 'randint(3, 12)'), ('dg', 'sample(1, 9, 3)'),
       ('txt', "('Mam ' + pln(n, ['koszulkę', 'koszulki', 'koszulek']) + ' i ' + pln(m, ['spodnie', 'spodnie', 'spodni']) + '. Ile różnych zestawów (koszulka i spodnie) mogę ułożyć?') if mode == 0 else "
               "(('Ile różnych liczb trzycyfrowych można zapisać za pomocą cyfr ' + str(dg[0]) + ', ' + str(dg[1]) + ' i ' + str(dg[2]) + ', jeśli w każdej liczbie każda cyfra występuje dokładnie raz?') if mode == 1 else "
               "('W turnieju gra ' + str(t) + ' drużyn. Każda drużyna rozgrywa dokładnie jeden mecz z każdą inną. Ile meczów odbędzie się w turnieju?'))"),
       ('ans', 'n * m if mode == 0 else (6 if mode == 1 else t * (t - 1) // 2)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Do każdej koszulki możesz dobrać każde spodnie: policz przypadki dla jednej koszulki i pomnóż.' if mode == 0 else ('Wypisz wszystkie liczby systematycznie: najpierw te zaczynające się od najmniejszej cyfry, potem od kolejnej.' if mode == 1 else 'Każda drużyna gra z t − 1 rywalami, ale każdy mecz policzyliśmy dwa razy.'))}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      area=A6, prereq=['n46-wp-sum-difference'])

skill('n46-justify', S, 'Które uzasadnienie jest poprawne?', ['IV-VI.6.2', 'IV-VI.6.1.c'],
      [lvl('Podzielność')],
      [('d', 'choice([6, 12, 15, 18])'), ('k', 'randint(3, 15)'), ('n', 'd * k'),
       ('good', "str(n) + ' = ' + str(d) + ' · ' + str(k) + ', więc dzieli się przez ' + str(d)"),
       ('w1', "'Liczba ' + str(n) + ' jest parzysta, więc dzieli się przez ' + str(d)"),
       ('w2', "'Ostatnia cyfra liczby ' + str(n) + ' to ' + str(n % 10) + ', więc dzieli się przez ' + str(d)"),
       ('w3', "'Suma cyfr liczby ' + str(n) + ' wynosi ' + str(sum(digits(n))) + ', więc dzieli się przez ' + str(d)")],
      choice('Ola twierdzi, że liczba @{n} jest podzielna przez @{d}. Które uzasadnienie jest w pełni poprawne?', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Poprawne uzasadnienie musi wynikać z definicji lub z kompletnej cechy podzielności – jedna cecha częściowa nie wystarcza.'),
              ('conclude', 'Najpewniejsze jest wskazanie takiej liczby całkowitej k, że @{n} = @{d} · k.')]),
      constraints=['n % 2 == 0', 'len(uniq([good, w1, w2, w3])) == 4'], min_distinct=30, area=A6, prereq=['n46-divisible-pick'])

# ============================================================================ narzędzia: kalkulator i aplikacje (1.38, 2.14)
CALC_YES = ("['Dodajesz 15 różnych cen z paragonów z kilku sklepów, aby sprawdzić miesięczne wydatki.', 'Obliczasz 12,5% z 1 847 zł, żeby poznać wysokość podatku.', "
            "'Porównujesz ceny jednostkowe sześciu różnych opakowań w sklepie internetowym.', 'Liczysz średnią z 20 pomiarów temperatury z całego miesiąca.', "
            "'Zamieniasz dziesięć odległości z mapy na kilometry w skali 1 : 75 000.']")
CALC_NO = ("['Obliczasz 6 · 7, żeby sprawdzić tabliczkę mnożenia.', 'Dodajesz 25 + 15 w pamięci.', 'Ćwiczysz pisemne dzielenie 756 : 6 w zeszycie.', "
           "'Liczysz połowę z 40.', 'Porównujesz, czy 0,5 jest większe niż 0,05.']")
skill('n46-calculator-use', S, 'Kiedy użyć kalkulatora?', ['IV-VI.1.38', 'IV-VI.6.1.c'],
      [lvl('Wybierz sytuację')],
      [('yes', 'shuffle(' + CALC_YES + ')'), ('no', 'shuffle(' + CALC_NO + ')')],
      choice('W której sytuacji kalkulator naprawdę się przyda, bo rachunki są długie, a liczy się wynik, a nie sam trening rachowania?', 'yes[0]', ['no[0]', 'no[1]', 'no[2]'],
             [('idea', 'Kalkulator pomaga, gdy liczb jest dużo albo są duże. Nie używamy go, gdy ćwiczymy rachunki lub gdy łatwo policzyć w pamięci.'),
              ('conclude', 'Warto użyć kalkulatora, gdy: @{yes[0]}')]),
      min_distinct=5, area=A6)

# ============================================================================ banki: znajdź błąd, narzędzia cyfrowe
def _sub_lines(a, b):
    assert a - b > 0
    return a - b

tasks = []
tasks.append(bank_find_mistake('Ola odejmowała pisemnie 503 − 178. W którym kroku jest błąd?',
    ['Jedności: 3 − 8 nie da się, więc pożyczam z dziesiątek.',
     'W 503 nie ma dziesiątek, więc pożyczam ze setek: 5 setek to 4 setki i 10 dziesiątek; 1 dziesiątkę oddaję jednościom.',
     'Jedności: 13 − 8 = 5. Dziesiątki: 9 − 7 = 2. Setki: 4 − 1 = 3.', 'Wynik: 325.'], None,
    [('check', 'Sprawdzamy odwrotnym działaniem: 325 + 178 = 503. Zgadza się, więc nie ma błędu.')]))
assert 503 - 178 == 325
tasks.append(bank_find_mistake('Zosia odejmowała pisemnie 5 203 − 1 748. W którym kroku jest błąd?',
    ['Jedności: 3 − 8 nie da się. W 5 203 nie ma dziesiątek, więc pożyczam ze setek: 2 setki to 1 setka i 10 dziesiątek; 1 dziesiątkę oddaję jednościom.',
     'Jedności: 13 − 8 = 5. Dziesiątki: 9 − 4 = 4.',
     'Setki: 1 − 7 nie da się, więc pożyczam z tysięcy: 5 tysięcy to 4 tysiące i 10 setek, czyli mamy 11 setek. Setki: 11 − 7 = 4.', 'Tysiące: 4 − 1 = 3. Wynik: 3 445.'], 2,
    [('check', 'Sprawdzenie: 3 445 + 1 748 = 5 193, a miało być 5 203.'), ('conclude', 'Dziesiątki: 9 − 4 = 5, a nie 4. Poprawny wynik to 3 455.')]))
assert 5203 - 1748 == 3455 and 3445 + 1748 == 5193
tasks.append(bank_find_mistake('Franek dodawał ułamki ⅓ + ¼. W którym kroku jest błąd?',
    ['Wspólny mianownik liczb 3 i 4 to 12.', 'Rozszerzam: ⅓ = 4/12, ¼ = 3/12.', 'Dodaję liczniki i mianowniki: (4 + 3)/(12 + 12) = 7/24.', 'Wynik: 7/24.'], 3,
    [('conclude', 'Przy dodawaniu ułamków o tym samym mianowniku dodajemy tylko liczniki: 4/12 + 3/12 = 7/12.')]))
tasks.append(bank_find_mistake('Maja obliczała 0,3 · 0,4. W którym kroku jest błąd?',
    ['Mnożę bez przecinków: 3 · 4 = 12.', 'W czynnikach razem jest jedno miejsce po przecinku.', 'Zatem w wyniku odliczam jedno miejsce: 1,2.', 'Wynik: 1,2.'], 2,
    [('conclude', 'Każdy czynnik ma jedno miejsce po przecinku, więc razem są dwa. Wynik to 0,12.')]))
tasks.append(bank_find_mistake('Kuba obliczał 25% z 80. W którym kroku jest błąd?',
    ['25% to jedna czwarta całości.', '80 : 4 = 20.', 'Zatem 25% z 80 to 20.', 'Odpowiedź: 20.'], None,
    [('check', 'Sprawdzenie: 20 · 4 = 80, a 20 to jedna czwarta z 80. Nie ma błędu.')]))
tasks.append(bank_find_mistake('Ania obliczała pole trójkąta o podstawie 6 cm i wysokości 4 cm. W którym kroku jest błąd?',
    ['Pole trójkąta liczymy ze wzoru P = a · h.', 'Podstawiam: P = 6 · 4.', 'P = 24.', 'Odpowiedź: 24 cm².'], 1,
    [('conclude', 'Pole trójkąta to połowa iloczynu podstawy i wysokości: P = ½ · 6 · 4 = 12 cm².')]))
tasks.append(bank_find_mistake('Tomek zamieniał 3,5 km na metry. W którym kroku jest błąd?',
    ['1 km = 1000 m.', 'Zamieniamy większą jednostkę na mniejszą, więc mnożymy.', '3,5 · 1000 = 350.', 'Odpowiedź: 3,5 km = 350 m.'], 3,
    [('conclude', '3,5 · 1000 = 3500, więc 3,5 km = 3500 m.')]))
tasks.append(bank_find_mistake('Ola obliczała 5 + 3 · 4. W którym kroku jest błąd?',
    ['Wykonuję działania po kolei od lewej.', '5 + 3 = 8.', '8 · 4 = 32.', 'Wynik: 32.'], 1,
    [('conclude', 'Mnożenie wykonujemy przed dodawaniem: 3 · 4 = 12, a 5 + 12 = 17.')]))
tasks.append(bank_find_mistake('Marek obliczał średnią liczb 4, 6 i 8. W którym kroku jest błąd?',
    ['Dodaję liczby: 4 + 6 + 8 = 18.', 'Średnia to suma podzielona przez liczbę składników.', 'Składniki są trzy, więc dzielę przez 3.', 'Wynik: 18 : 3 = 6.'], None,
    [('check', 'Średnia 6 leży między najmniejszą (4) a największą (8) liczbą. Nie ma błędu.')]))
assert 4 + 6 + 8 == 18 and 18 / 3 == 6
tasks.append(bank_find_mistake('Kasia obliczała trzeci kąt trójkąta, w którym dwa kąty mają 50° i 60°. W którym kroku jest błąd?',
    ['50° + 60° = 110°.', 'Suma kątów w trójkącie wynosi 360°.', '360° − 110° = 250°.', 'Trzeci kąt ma 250°.'], 2,
    [('conclude', 'Suma kątów w trójkącie to 180°. Trzeci kąt ma 180° − 110° = 70°.')]))
tasks.append(bank_find_mistake('Piotr zapisał: „51 jest liczbą pierwszą, bo nie dzieli się przez 2, 5 ani 10”. W którym kroku jest błąd?',
    ['51 nie jest parzysta, więc nie dzieli się przez 2.', '51 nie kończy się cyfrą 0 ani 5, więc nie dzieli się przez 5 ani 10.', 'Skoro nie dzieli się przez te liczby, to jest pierwsza.', 'Odpowiedź: 51 jest pierwsza.'], 3,
    [('conclude', 'Trzeba sprawdzić też inne dzielniki. Suma cyfr 5 + 1 = 6 dzieli się przez 3, więc 51 = 3 · 17.')]))
assert 3 * 17 == 51
tasks.append(bank_find_mistake('Ewa obliczała obwód prostokąta o bokach 5 cm i 3 cm. W którym kroku jest błąd?',
    ['Obwód to suma długości wszystkich boków.', 'Prostokąt ma dwa boki po 5 cm i dwa po 3 cm.', 'Obwód = 5 · 3 = 15.', 'Odpowiedź: 15 cm.'], 3,
    [('conclude', 'Obwód to 5 + 5 + 3 + 3 = 16 cm. Iloczyn boków to pole, a nie obwód.')]))
tasks.append(bank_find_mistake('Adam dzielił z resztą 47 przez 6. W którym kroku jest błąd?',
    ['6 · 7 = 42, a 6 · 8 = 48 jest już za dużo.', 'Zatem iloraz niepełny to 7.', 'Reszta: 47 − 42 = 5.', 'Zapis: 47 = 6 · 7 + 5.'], None,
    [('check', 'Reszta 5 jest mniejsza od dzielnika 6, a 6 · 7 + 5 = 47. Nie ma błędu.')]))
assert 6 * 7 + 5 == 47
tasks.append(bank_find_mistake('Zuzia porównywała ułamki ¾ i ⅝. W którym kroku jest błąd?',
    ['Sprowadzam do wspólnego mianownika 8: ¾ = 6/8.', '⅝ zostaje bez zmian.', 'Porównuję liczniki: 6 < 5.', 'Zatem ¾ < ⅝.'], 3,
    [('conclude', '6 jest większe od 5, więc ¾ > ⅝.')]))
tasks.append(bank_find_mistake('Leon policzył, że trzy zeszyty po 2,50 zł kosztują razem 6 zł. W którym kroku jest błąd?',
    ['Cena jednego zeszytu: 2,50 zł.', 'Liczba zeszytów: 3.', 'Koszt: 3 · 2,50 zł.', '3 · 2,50 = 6,00, więc koszt to 6 zł.'], 4,
    [('conclude', '3 · 2,50 = 7,50 zł.')]))
assert 3 * 2.5 == 7.5
bank_skill('n46-find-mistake', S, 'Detektyw błędów', ['IV-VI.6.1.c', 'IV-VI.6.2', 'IV-VI.1.9'], tasks,
           levels=['Znajdź błąd w rozwiązaniu'], tags=('thinking',), area=A6,
           intro='Czasem rozwiązanie wygląda dobrze, ale ma ukryty błąd. Czytaj krok po kroku i sprawdzaj każdy z nich. Możesz też sprawdzić wynik działaniem odwrotnym lub oszacować, czy jest sensowny.')

tools = [
  bank_choice('Chcesz szybko zamienić 7,5 km na metry i kilka razy sprawdzić inne odległości. Co zrobisz?',
              [('Użyję konwertera jednostek w aplikacji, a potem sprawdzę, czy wynik jest sensowny (metrów jest więcej niż kilometrów).', True),
               ('Wpiszę liczby do aplikacji i przepiszę wynik bez sprawdzania.', False),
               ('Poproszę kolegę, żeby powiedział wynik z głowy.', False),
               ('Zgadnę wynik.', False)],
              [('idea', 'Narzędzie przyspiesza liczenie, ale wynik trzeba samemu ocenić.')]),
  bank_choice('Aplikacja pokazuje, że 250 ml to 25 l. Co powinieneś zrobić?',
              [('Zauważyć, że szklanka ma około 250 ml, a nie 25 l – wynik jest nieprawdopodobny, więc sprawdzić dane i jednostki.', True),
               ('Zaufać aplikacji, bo komputer się nie myli.', False),
               ('Zapisać wynik, bo jest ładną liczbą.', False),
               ('Pomnożyć wynik jeszcze raz przez 10.', False)],
              [('idea', 'Zawsze oceniaj sensowność wyniku, nawet gdy liczy aplikacja.')]),
  bank_choice('Pomierzyłeś długość pokoju i otrzymałeś 4,2 m, a szerokość 350 cm. Chcesz obliczyć pole w arkuszu kalkulacyjnym. Co jest ważne?',
              [('Wpisać obie wartości w tej samej jednostce, np. 4,2 m i 3,5 m, i dopiero pomnożyć.', True),
               ('Wpisać 4,2 i 350 i pomnożyć.', False),
               ('Wpisać 420 i 3,5 i pomnożyć.', False),
               ('Dodać wymiary zamiast mnożyć.', False)],
              [('idea', 'Przed obliczeniami ujednolić jednostki: 350 cm = 3,5 m. Pole: 4,2 · 3,5 = 14,7 m².')]),
  bank_choice('Chcesz obliczyć średnią ze stu pomiarów temperatury zapisanych w tabeli. Które narzędzie będzie najwygodniejsze?',
              [('Arkusz kalkulacyjny z funkcją średniej.', True), ('Sama kartka i długopis.', False), ('Zegarek.', False), ('Linijka.', False)],
              [('idea', 'Przy dużej liczbie danych arkusz kalkulacyjny oszczędza czas i zmniejsza ryzyko pomyłek.')]),
  bank_choice('Chcesz sprawdzić, ile minut to 3,5 godziny. Aplikacja podaje 350 minut. Jak sprawdzisz, czy wynik jest sensowny?',
              [('3,5 h to 3 h i pół godziny: 3 · 60 + 30 = 210 min, więc 350 min to zły wynik.', True),
               ('Wynik jest dobry, bo 350 zawiera cyfry 3,5.', False),
               ('Wynik jest dobry, bo aplikacja jest pewna.', False),
               ('Wynik trzeba pomnożyć przez 2.', False)],
              [('idea', 'Prosty rachunek w pamięci pozwala szybko wychwycić błąd narzędzia lub błąd przy wpisywaniu danych.')]),
  bank_choice('Aby zaplanować budżet wycieczki klasowej, zbierasz oferty cenowe kilku firm i porównujesz je. Co ułatwi pracę?',
              [('Zapisanie ofert w tabeli (np. w arkuszu) z kolumnami: cena, liczba osób, cena na osobę.', True),
               ('Zapamiętanie ofert w głowie.', False), ('Wybranie najtańszej ceny bez sprawdzania, co obejmuje.', False), ('Wybranie najdroższej oferty.', False)],
              [('idea', 'Porównuj ceny w tej samej jednostce, np. cenie na osobę.')]),
]
bank_skill('n46-digital-tools', S, 'Narzędzia cyfrowe i pomiary', ['IV-VI.2.14', 'IV-VI.6.1.c'], tools,
           levels=['Wybierz mądrze narzędzie'], tags=('thinking',), area=A6,
           intro='Aplikacje, kalkulator i arkusz kalkulacyjny przyspieszają pracę, ale to ty decydujesz, jakie dane wpisać i czy wynik ma sens.')

# ============================================================================ ścieżka
un = Unit(S, 'n46-u28', 'Zadania tekstowe', 'Planujemy rozwiązanie w krokach, rysujemy i sprawdzamy sensowność wyniku.', 'book', area=A6)
un.learn('n46-wp-shopping').learn('n46-wp-sum-difference').learn('n46-wp-reverse').learn('n46-wp-proportion').learn('n46-sense-check')
un.review('Powtórka: zadania tekstowe', ['n46-wp-shopping', 'n46-wp-sum-difference', 'n46-wp-reverse', 'n46-wp-proportion'])
un.checkpoint(['n46-wp-shopping', 'n46-wp-sum-difference', 'n46-wp-reverse', 'n46-wp-proportion', 'n46-sense-check'])

un = Unit(S, 'n46-u29', 'Myślenie matematyczne', 'Przykłady i kontrprzykłady, próby i poprawki, wszystkie przypadki i uzasadnianie.', 'brain', area=A6)
un.learn('n46-examples').learn('n46-counterexample').learn('n46-sum-product').learn('n46-count-cases').learn('n46-justify')
un.learn('n46-find-mistake', levels=[1], tasks=8).learn('n46-calculator-use').learn('n46-digital-tools', levels=[1], tasks=5)
un.checkpoint(['n46-examples', 'n46-counterexample', 'n46-sum-product', 'n46-count-cases', 'n46-justify'])
