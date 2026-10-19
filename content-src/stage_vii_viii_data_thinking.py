"""Stage VII-VIII, areas 4 (Dane i zdarzenia losowe) and 5 (Myślenie matematyczne).  Objectives: VII-VIII.4.1 - 4.6, 5.1 - 5.3."""
from dsl import *

S = 'VII-VIII'
A4 = 'VII-VIII.4'
A5 = 'VII-VIII.5'

# ============================================================================ źródła danych i ich prezentacja (4.1, 4.2)
SOURCES = [
    bank_choice('Chcesz sprawdzić, ile średnio kosztuje 1 kg jabłek w Polsce. Które źródło danych jest najbardziej wiarygodne?',
                [('Oficjalne dane urzędu statystycznego (GUS) z podaną metodą zbierania danych.', True), ('Anonimowy wpis na forum internetowym.', False),
                 ('Reklama jednego ze sklepów.', False), ('Cena, którą zapamiętał jeden znajomy.', False)],
                [('idea', 'Wiarygodne dane mają znane źródło, opisaną metodę i dotyczą dużej, dobrze dobranej próby.')]),
    bank_choice('W szkole zapytano o ulubiony sport tylko uczniów, którzy czekali przed salą gimnastyczną na trening piłki nożnej. Czy wynik ankiety opisuje całą szkołę?',
                [('Nie – ankietowani nie reprezentują wszystkich uczniów.', True), ('Tak – ankieta była przecież prawdziwa.', False),
                 ('Tak, jeśli ankietowanych było więcej niż 5.', False), ('Tak, bo piłka nożna jest najpopularniejsza.', False)],
                [('idea', 'Próba powinna reprezentować całą grupę. Wybieranie tylko miłośników jednego sportu zniekształca wynik.')]),
    bank_choice('Masz 30 wypełnionych ankiet z odpowiedziami „tak” i „nie”. Co zrobisz najpierw, aby je przeanalizować?',
                [('Uporządkuję odpowiedzi w tabeli i policzę, ile jest każdej z nich.', True), ('Wybiorę pierwszą ankietę jako wynik.', False),
                 ('Wyrzucę połowę ankiet.', False), ('Dodam do tabeli dane zmyślone dla porównania.', False)],
                [('idea', 'Dane trzeba najpierw uporządkować, np. w tabeli częstości, a dopiero potem wyciągać wnioski.')]),
    bank_choice('W zestawie wzrostów uczniów klasy (w cm) są liczby: 148, 152, 150, 1500, 155. Co zrobisz z wartością 1500?',
                [('Sprawdzę, czy to nie błąd zapisu (np. miało być 150) i poprawię lub pominę.', True), ('Uwzględnię ją bez zastrzeżeń.', False),
                 ('Usunę wszystkie pozostałe wartości.', False), ('Zamienię ją na 0.', False)],
                [('idea', 'Wartość odstająca może być błędem. Najpierw ją sprawdzamy, a nie ślepo liczymy.')]),
    bank_choice('Chcesz poznać aktualną stopę inflacji w Polsce. Do jakiego źródła zajrzysz?',
                [('Do komunikatu Głównego Urzędu Statystycznego lub Narodowego Banku Polskiego.', True), ('Do filmiku bez źródeł.', False),
                 ('Do plotek na komunikatorze.', False), ('Do reklamy banku.', False)],
                [('idea', 'Wskaźniki makroekonomiczne publikują oficjalne instytucje; sprawdzamy datę i metodę.')]),
    bank_choice('Sondaż: „3 z 5 zapytanych osób woli herbatę”. Co jest największym problemem tego wniosku?',
                [('Próba jest bardzo mała (5 osób) – wniosek jest niepewny.', True), ('Herbata jest mniej popularna niż kawa.', False),
                 ('Wynik nie może być ułamkiem.', False), ('Nie ma żadnego problemu.', False)],
                [('idea', 'Im mniejsza próba, tym mniej wiarygodne wnioski o całej grupie.')]),
]
bank_skill('vh-data-sources', S, 'Źródła i wiarygodność danych', ['VII-VIII.4.1'], SOURCES, levels=['Wiarygodne dane'], tags=('thinking',), area=A4,
           intro='Zanim wyciągniesz wniosek z danych, sprawdź, skąd pochodzą, kto je zebrał, ile ich jest i czy próba jest reprezentatywna.')

CHARTS = [
    bank_choice('Chcesz pokazać, jak zmieniała się temperatura w ciągu doby. Który sposób przedstawienia będzie najlepszy?',
                [('Wykres liniowy.', True), ('Diagram kołowy.', False), ('Pojedyncza liczba – średnia.', False), ('Wykres słupkowy z kolorami dla każdego dnia tygodnia.', False)],
                [('idea', 'Zmianę w czasie najlepiej pokazuje wykres liniowy.')]),
    bank_choice('Chcesz porównać liczbę uczniów w pięciu klasach. Co wybierzesz?',
                [('Diagram słupkowy – słupki łatwo porównać.', True), ('Wykres liniowy łączący klasy.', False), ('Opis słowny bez liczb.', False), ('Diagram kołowy z 20 częściami.', False)],
                [('idea', 'Porównywanie wartości w różnych kategoriach: diagram słupkowy.')]),
    bank_choice('Chcesz pokazać, jaką część miesięcznego budżetu rodziny stanowią czynsz, jedzenie, transport i rozrywka. Co wybierzesz?',
                [('Diagram kołowy – przedstawia części całości.', True), ('Wykres liniowy.', False), ('Tabelę z jedną kolumną.', False), ('Wyłącznie średnią.', False)],
                [('idea', 'Diagram kołowy pokazuje, jaką część całości stanowi każda kategoria.')]),
    bank_choice('Masz 500 pomiarów i chcesz szybko policzyć średnią oraz narysować wykres. Co ułatwi pracę?',
                [('Arkusz kalkulacyjny z wbudowanymi wzorami i wykresami.', True), ('Liczenie na kartce wszystkich pomiarów.', False), ('Policzenie tylko pierwszych dwóch pomiarów.', False), ('Wybranie losowej liczby.', False)],
                [('idea', 'Przy dużej liczbie danych korzystamy z aplikacji obliczeniowych (arkusza), ale wyniki weryfikujemy.')]),
    bank_choice('Wykonałeś 60 rzutów kostką. Jak najlepiej pokazać, ile razy wypadła każda liczba oczek?',
                [('Tabela częstości i diagram słupkowy.', True), ('Jedna liczba – suma oczek.', False), ('Wykres liniowy łączący liczby oczek.', False), ('Opisowo, bez liczb.', False)],
                [('idea', 'Kategorie (liczby oczek) i ich liczności pokazuje diagram słupkowy.')]),
    bank_choice('Cena paliwa była notowana co miesiąc przez rok. Który wykres pokaże trend?',
                [('Wykres liniowy cen w kolejnych miesiącach.', True), ('Diagram kołowy z miesiącami.', False), ('Pojedynczy słupek z najwyższą ceną.', False), ('Tabela bez liczb.', False)],
                [('idea', 'Trend – zmiana w czasie – widać na wykresie liniowym.')]),
]
bank_skill('vh-chart-choice', S, 'Jak przedstawić dane?', ['VII-VIII.4.2'], CHARTS, levels=['Dobór wykresu'], tags=('thinking',), area=A4, prereq=['vh-data-sources'],
           intro='Dane można pokazać w tabeli, na diagramie słupkowym, kołowym lub na wykresie liniowym. Wybierz taki sposób, który pomaga odpowiedzieć na pytanie.')

# ============================================================================ wykresy zależności (4.3)
skill('vh-graph-distance', S, 'Wykres drogi w czasie', ['VII-VIII.4.3'],
      [lvl('Odczyt drogi', ask=0), lvl('Prędkość w jednej godzinie', ask=1), lvl('Droga w dwóch godzinach', ask=2), lvl('Średnia prędkość', ask=3)],
      [('v1', 'randint(6, 24)'), ('v2', 'choice([0, 6, 12, 18, 24])'), ('v3', 'randint(6, 24)'), ('v4', 'randint(6, 24)'),
       ('ys', '[0, v1, v1 + v2, v1 + v2 + v3, v1 + v2 + v3 + v4]'), ('hours', '[0, 1, 2, 3, 4]'),
       ('i', 'randint(1, 4)'), ('j', 'randint(1, 4)'),
       ('txt', "('Ile kilometrów przejechał rowerzysta po ' + str(i) + ' godzinach jazdy?') if ask == 0 else "
               "(('Z jaką prędkością (w km/h) jechał rowerzysta w ' + str(j) + '. godzinie?') if ask == 1 else "
               "(('Ile kilometrów przejechał rowerzysta w drugiej i trzeciej godzinie razem?') if ask == 2 else "
               "('Jaka była średnia prędkość (w km/h) rowerzysty na całej 4-godzinnej trasie?')))"),
       ('ans', 'ys[i] if ask == 0 else (ys[j] - ys[j - 1] if ask == 1 else (ys[3] - ys[1] if ask == 2 else ys[4] // 4))'),
       ('u', "'km' if ask == 0 or ask == 2 else 'km/h'")],
      quantity('Wykres pokazuje drogę przebytą przez rowerzystę w ciągu 4 godzin. @{txt}', 'ans', 'u',
               [('idea', "@{('Odczytaj wartość na osi pionowej dla danej godziny.' if ask == 0 else ('Prędkość w jednej godzinie to przyrost drogi w tej godzinie.' if ask == 1 else ('Odejmij odczytane drogi po 3 i po 1 godzinie.' if ask == 2 else 'Średnia prędkość = cała droga : cały czas.')))}"),
                ('conclude', 'Odpowiedź: @{ans} @{u}.')], unit_expr=True,
               media=[{'type': 'chart', 'kind': 'line', 'essential': True, 'alt': 'Wykres liniowy: droga rowerzysty w kolejnych godzinach.',
                       'params': {'x': E('hours'), 'y': E('ys'), 'xLabel': 'czas (h)', 'yLabel': 'droga (km)'}}]),
      constraints=['ask != 3 or (ys[4] % 4 == 0)', 'ask != 1 or ys[j] != ys[j - 1] or v2 == 0', 'ys[4] <= 90'], min_distinct=30, area=A4, prereq=['n46-line-chart'])

skill('vh-graph-change', S, 'Zmiany cen i wynagrodzeń w czasie', ['VII-VIII.4.3'],
      [lvl('Różnica wartości', ask=0), lvl('O ile procent wzrosło?', ask=1), lvl('O ile procent zmalało?', ask=2)],
      [('years', '[2019, 2020, 2021, 2022, 2023, 2024]'), ('i', 'randint(0, 3)'), ('j', 'randint(i + 1, 5)'),
       ('base', '20 * randint(10, 25)'), ('p', 'choice([5, 10, 20, 25, 50])'),
       ('vi', 'base'), ('vj', 'base + base * p // 100 if ask < 2 else base - base * p // 100'),
       ('o', 'sample(200, 500, 6)'),
       ('vals', 'setat(setat(o, i, vi), j, vj)'),
       ('txt', "('O ile złotych zmienił się koszt koszyka zakupów między rokiem ' + str(years[i]) + ' a ' + str(years[j]) + '? Podaj wynik bez znaku.') if ask == 0 else "
               "(('O ile procent wzrósł koszt koszyka zakupów między rokiem ' + str(years[i]) + ' a ' + str(years[j]) + '?') if ask == 1 else "
               "('O ile procent zmalał koszt koszyka zakupów między rokiem ' + str(years[i]) + ' a ' + str(years[j]) + '?'))"),
       ('ans', 'abs(vj - vi) if ask == 0 else p'), ('u', "'zł' if ask == 0 else '%'")],
      quantity('Wykres pokazuje roczny koszt koszyka zakupów (w zł). @{txt}', 'ans', 'u',
               [('idea', "@{('Odczytaj obie wartości i odejmij mniejszą od większej.' if ask == 0 else 'Oblicz różnicę wartości i podziel ją przez wartość początkową (z roku wcześniejszego). Wynik zamień na procent.')}"),
                ('compute', 'Wartość w roku @{years[i]}: @{vi} zł, w roku @{years[j]}: @{vj} zł.')], unit_expr=True,
               media=[{'type': 'chart', 'kind': 'line', 'essential': True, 'alt': 'Wykres liniowy: koszt koszyka zakupów w latach 2019–2024.',
                       'params': {'x': E('years'), 'y': E('vals'), 'xLabel': 'rok', 'yLabel': 'koszt (zł)'}}]),
      constraints=['len(uniq(vals)) == 6', 'vi >= 200 and vj >= 200', 'min(vals) >= 150 and max(vals) <= 800'], min_distinct=40, area=A4, prereq=['vh-percent-what', 'vh-graph-distance'])

# ============================================================================ średnia i mediana (4.4)
skill('vh-mean-exact', S, 'Średnia arytmetyczna zestawu danych', ['VII-VIII.4.4'],
      [lvl('Punkty ze sprawdzianów', n=5), lvl('Wydatki tygodniowe', n=6)],
      [('m', 'randint(20, 60)'), ('rest', 'sample(m - 12, m + 12, n - 1)'), ('last', 'm * n - sum(rest)'), ('vs', 'rest + [last]'),
       ('what', "'Wyniki z ' + str(n) + ' sprawdzianów (w punktach): ' if n == 5 else 'Wydatki Oli w ostatnich ' + str(n) + ' dniach (w zł): '")],
      number('@{what}@{join(vs, ", ")}. Oblicz średnią arytmetyczną tych liczb.', 'm',
             [('idea', 'Średnia arytmetyczna = suma wszystkich liczb : liczba liczb.'), ('compute', '@{join(vs, " + ")} = @{sum(vs)}; @{sum(vs)} : @{n} = @{m}')]),
      constraints=['last >= 5 and last <= 90', 'last not in rest'], selfCheck=['sum(vs) == m * n'], min_distinct=40, area=A4, prereq=['n46-mean'])

skill('vh-median', S, 'Mediana zestawu danych', ['VII-VIII.4.4'],
      [lvl('Nieparzysta liczba danych', n=5), lvl('Parzysta liczba danych', n=6), lvl('Siedem lub osiem danych', n=7)],
      [('k', 'n if n != 7 else choice([7, 8])'), ('vs', 'sample(1, 60, k)'), ('s', 'sorted(vs)'),
       ('med', 's[k // 2] if k % 2 == 1 else (s[k // 2 - 1] + s[k // 2]) / 2')],
      decimal('Dane: @{join(vs, ", ")}. Oblicz medianę tych liczb.', 'med',
              [('idea', 'Mediana to środkowa liczba po uporządkowaniu danych od najmniejszej do największej. Przy parzystej liczbie danych – średnia dwóch środkowych.'),
               ('compute', 'Po uporządkowaniu: @{join(s, ", ")}. Mediana: @{med|dec}.')]),
      min_distinct=40, area=A4, prereq=['vh-mean-exact'])

skill('vh-mean-outlier', S, 'Średnia czy mediana? Zarobki w firmie', ['VII-VIII.4.4', 'VII-VIII.4.5'],
      [lvl('Jedna wysoka pensja')],
      [('base', '500 * randint(6, 9)'), ('d', 'sample(0, 6, 4)'), ('ws', '[base + 100 * d[0], base + 100 * d[1], base + 100 * d[2], base + 100 * d[3]]'),
       ('boss', '1000 * randint(15, 30)'), ('all', 'ws + [boss]'),
       ('mn', 'sum(all) / 5'), ('md', 'sorted(all)[2]')],
      choice_text('W małej firmie pięć osób zarabia miesięcznie (w zł): @{join(all, ", ")}. Pracownicy chcą poinformować nowego kandydata, ile zwykle zarabia się w firmie. Która miara lepiej opisuje typową pensję?',
                  [('Mediana (@{md} zł), bo nie zależy od jednej bardzo wysokiej pensji.', 'md < mn'), ('Średnia arytmetyczna (@{mn|dec} zł).', 'md > mn'),
                   ('Obie opisują typową pensję tak samo dobrze.', 'md == mn'), ('Najwyższa pensja (@{boss} zł).', 'boss < 0')], None,
                  [('idea', 'Jedna wyjątkowo wysoka wartość zawyża średnią, a mediana pozostaje w środku zestawu.'),
                   ('compute', 'Średnia: @{sum(all)} : 5 = @{mn|dec} zł. Mediana: @{md} zł.')], fixed_order=True),
      constraints=['md < mn', 'len(uniq(ws)) == 4'], min_distinct=30, area=A4, prereq=['vh-median'])

skill('vh-mean-missing', S, 'Średnia po dodaniu nowej wartości', ['VII-VIII.4.4', 'VII-VIII.4.5'],
      [lvl('Brakujący wynik', mode=0), lvl('Średnia wzrosła lub zmalała', mode=1)],
      [('n', 'randint(3, 7)'), ('m', 'randint(10, 40)'), ('dd', 'choice([-3, -2, -1, 1, 2, 3])'), ('m2', 'm + dd'),
       ('new', 'm + dd * (n + 1)'),
       ('txt', "('Średnia z ' + str(n) + ' wyników testów Ani wynosi ' + str(m) + ' pkt. Po kolejnym teście średnia z ' + str(n + 1) + ' wyników wynosi ' + str(m2) + ' pkt. Ile punktów Ania zdobyła w ostatnim teście?') if mode == 0 else "
               "('Średnia z ' + str(n) + ' kartkówek Kuby wynosi ' + str(m) + ' pkt. Ile punktów musi zdobyć z następnej kartkówki, aby średnia z ' + str(n + 1) + ' kartkówek wyniosła ' + str(m2) + ' pkt?')")],
      number('@{txt}', 'new',
             [('idea', 'Suma wyników = średnia · liczba wyników. Porównaj sumę po dodaniu nowej wartości z sumą wcześniejszą.'),
              ('compute', 'Nowa suma: @{m2} · @{n + 1} = @{m2 * (n + 1)}; stara suma: @{m} · @{n} = @{m * n}; różnica: @{new}.')]),
      constraints=['new >= 0 and new <= 100'], selfCheck=['(m * n + new) == m2 * (n + 1)'], min_distinct=40, area=A4, prereq=['vh-mean-exact'])

# ============================================================================ krytyczna interpretacja danych (4.5)
CRIT = [
    bank_choice('Na wykresie słupkowym oś pionowa zaczyna się od 90, a słupki mają wysokości 92 i 94. Słupek „B” wygląda na dwa razy wyższy od „A”. Jaki wniosek jest poprawny?',
                [('Różnica jest niewielka; wrażenie wywołuje ucięta oś.', True), ('Wartość B jest dwa razy większa od A.', False), ('Wykres jest zawsze wiarygodny.', False), ('Nie da się odczytać liczb z wykresu.', False)],
                [('idea', 'Zawsze patrz, od jakiej wartości zaczyna się oś. Ucięta oś wyolbrzymia różnice.')]),
    bank_choice('Latem rośnie sprzedaż lodów i liczba utonięć. Czy to oznacza, że lody powodują utonięcia?',
                [('Nie – oba zjawiska zależą od trzeciego czynnika: letniej pogody.', True), ('Tak – widać to na wykresie.', False), ('Tak, jeśli korelacja jest silna.', False), ('Nie da się nic powiedzieć o żadnych zależnościach.', False)],
                [('idea', 'Współwystępowanie dwóch zjawisk nie dowodzi, że jedno powoduje drugie.')]),
    bank_choice('Średnia pensja w firmie wynosi 8000 zł. Czy na tej podstawie można stwierdzić, że większość pracowników zarabia około 8000 zł?',
                [('Nie – kilka bardzo wysokich pensji może zawyżać średnią.', True), ('Tak – średnia zawsze opisuje typową pensję.', False), ('Tak, bo średnia to środek zestawu.', False), ('Nie – średnia nie może być większa od 5000.', False)],
                [('idea', 'Średnia jest wrażliwa na wartości odstające. Warto sprawdzić też medianę i rozrzut.')]),
    bank_choice('Cena towaru wzrosła o 50%, a następnie spadła o 50% (nowej ceny). Czy cena wróciła do pierwotnej?',
                [('Nie – jest niższa: 100 → 150 → 75.', True), ('Tak – 50% w górę i 50% w dół znoszą się.', False), ('Tak, ale tylko dla cen całkowitych.', False), ('Jest wyższa niż na początku.', False)],
                [('idea', 'Procenty liczymy od różnych podstaw: pierwszy raz od ceny początkowej, drugi raz od ceny po podwyżce.')]),
    bank_choice('Reklama: „9 na 10 dentystów poleca naszą pastę”. Co powinno cię zastanowić?',
                [('Ilu dentystów zapytano i jak ich wybrano.', True), ('Nic – wynik jest jednoznaczny.', False), ('Liczba 9 jest nieparzysta.', False), ('Kolor opakowania pasty.', False)],
                [('idea', 'Ważne są: wielkość próby, sposób doboru i dokładne sformułowanie pytania.')]),
    bank_choice('Bank reklamuje kredyt: „rata tylko 99 zł miesięcznie!” bez podania okresu i dodatkowych opłat. Co sprawdzisz przed decyzją?',
                [('Całkowity koszt kredytu: liczbę rat, prowizje i dodatkowe opłaty.', True), ('Tylko wysokość raty.', False), ('Tylko kolor logo banku.', False), ('Nic – niska rata oznacza niski koszt.', False)],
                [('idea', 'Niska rata może oznaczać bardzo długi okres spłaty i wysoki koszt całkowity.')]),
    bank_choice('Inflacja w ciągu roku wyniosła 5%, a twoje kieszonkowe wzrosło o 3%. Co z tego wynika?',
                [('Możesz kupić trochę mniej niż rok temu – realna wartość kieszonkowego spadła.', True), ('Możesz kupić więcej, bo kieszonkowe wzrosło.', False), ('Nic się nie zmieniło.', False), ('Ceny spadły o 2%.', False)],
                [('idea', 'Jeśli ceny rosną szybciej niż dochód, siła nabywcza maleje.')]),
    bank_choice('W badaniu 10 osób odpowiedziało, że lubi nowy napój, a 8 z nich dostało go za darmo przed pytaniem. Jaki wniosek jest bezpieczny?',
                [('Wynik może być obciążony: darmowy napój mógł wpłynąć na opinię i próba jest mała.', True), ('Nowy napój lubi 100% Polaków.', False), ('Napój jest najlepszy na rynku.', False), ('Opinia nie ma znaczenia.', False)],
                [('idea', 'Krytycznie oceniaj, kto pytał, kogo i w jakich warunkach.')]),
]
bank_skill('vh-data-critical', S, 'Krytyczna interpretacja danych', ['VII-VIII.4.5'], CRIT, levels=['Czy ten wniosek wynika z danych?'], tags=('thinking',), area=A4, prereq=['vh-mean-outlier'],
           intro='Pytaj: skąd są dane, ile ich jest, jak zaczyna się oś wykresu i czy wniosek rzeczywiście z nich wynika. Korelacja nie oznacza przyczyny.')

# ============================================================================ prawdopodobieństwo (4.6)
skill('vh-prob-balls', S, 'Losowanie kuli z worka', ['VII-VIII.4.6'],
      [lvl('Jeden kolor', mode=0), lvl('Kula nie jest tego koloru', mode=1), lvl('Jeden z dwóch kolorów', mode=2)],
      [('r', 'randint(1, 8)'), ('b', 'randint(1, 8)'), ('g', 'randint(1, 8)'), ('tot', 'r + b + g'),
       ('c', 'randint(0, 2)'), ('c2', '(c + 1) % 3'),
       ('cnt', '[r, b, g]'), ('col', "['czerwona', 'niebieska', 'zielona']"), ('colg', "['czerwonych', 'niebieskich', 'zielonych']"),
       ('k', 'cnt[c] if mode == 0 else (tot - cnt[c] if mode == 1 else cnt[c] + cnt[c2])'),
       ('sol', 'k / tot'),
       ('txt', "('W worku są kule: czerwone (' + str(r) + '), niebieskie (' + str(b) + ') i zielone (' + str(g) + '). Losujemy jedną kulę. Jakie jest prawdopodobieństwo, że będzie ona ' + col[c] + '?') if mode == 0 else "
               "(('W worku są kule: czerwone (' + str(r) + '), niebieskie (' + str(b) + ') i zielone (' + str(g) + '). Losujemy jedną kulę. Jakie jest prawdopodobieństwo, że NIE będzie ona ' + col[c] + '?') if mode == 1 else "
               "('W worku są kule: czerwone (' + str(r) + '), niebieskie (' + str(b) + ') i zielone (' + str(g) + '). Losujemy jedną kulę. Jakie jest prawdopodobieństwo, że będzie ona ' + col[c] + ' lub ' + col[c2] + '?'))")],
      fraction('@{txt} Podaj wynik jako ułamek nieskracalny.', 'numer(sol)', 'denom(sol)',
               [('idea', 'Prawdopodobieństwo = liczba kul sprzyjających : liczba wszystkich kul.'), ('compute', '@{k} z @{tot}, czyli $@{sol|frac}$')]),
      constraints=['denom(sol) != 1', 'tot <= 20'], min_distinct=40, area=A4, prereq=['n46-frac-simplify'],
      intro='Gdy wszystkie wyniki są jednakowo możliwe, prawdopodobieństwo zdarzenia to liczba wyników sprzyjających podzielona przez liczbę wszystkich wyników.')

skill('vh-prob-dice', S, 'Rzut kostką', ['VII-VIII.4.6'],
      [lvl('Jedna kostka', mode=0)],
      [('t', 'randint(2, 5)'), ('e', 'randint(0, 5)'),
       ('evs', "['większa niż ' + str(t), 'mniejsza niż ' + str(t), 'parzysta', 'podzielna przez 3', 'liczbą pierwszą', 'nieparzysta i większa niż 1']"),
       ('cnt', '[6 - t, t - 1, 3, 2, 3, 2]'),
       ('sol', 'cnt[e] / 6'),
       ('txt', "('Rzucamy raz symetryczną sześcienną kostką do gry. Jakie jest prawdopodobieństwo, że liczba oczek jest ' + evs[e] + '?') if e < 4 else "
               "(('Rzucamy raz symetryczną sześcienną kostką do gry. Jakie jest prawdopodobieństwo, że liczba oczek jest liczbą pierwszą?') if e == 4 else "
               "('Rzucamy raz symetryczną sześcienną kostką do gry. Jakie jest prawdopodobieństwo, że liczba oczek jest nieparzysta i większa niż 1?'))")],
      fraction('@{txt} Podaj wynik jako ułamek nieskracalny.', 'numer(sol)', 'denom(sol)',
               [('idea', 'Wypisz wyniki sprzyjające i podziel ich liczbę przez 6.'), ('compute', '@{cnt[e]} z 6, czyli $@{sol|frac}$')]),
      constraints=['denom(sol) != 1'], min_distinct=12, area=A4, prereq=['vh-prob-balls'])

skill('vh-prob-two', S, 'Dwa rzuty: monety i kostki', ['VII-VIII.4.6'],
      [lvl('Dwie monety', md=8, mode=0), lvl('Trzy monety', md=9, mode=1), lvl('Suma oczek dwóch kostek', md=20, mode=2), lvl('Inne zdarzenia dla dwóch kostek', md=10, mode=3)],
      [('s', 'randint(3, 11)'), ('rel', 'randint(0, 2)'), ('e', 'randint(0, 8)'), ('e3', 'randint(0, 9)'), ('e2', 'randint(0, 11)'),
       ('c2t', "['wypadną dwa orły', 'wypadną dwie reszki', 'wypadnie dokładnie jeden orzeł', 'wypadnie co najmniej jeden orzeł', 'wypadnie co najmniej jedna reszka', "
               "'w obu rzutach wypadnie ten sam wynik', 'w rzutach wypadną różne wyniki', 'w pierwszym rzucie wypadnie orzeł', 'w pierwszym rzucie wypadnie orzeł, a w drugim reszka']"),
       ('c2n', '[1, 1, 2, 3, 3, 2, 2, 2, 1]'),
       ('c3t', "['wypadną trzy orły', 'wypadną trzy reszki', 'wypadną dokładnie dwa orły', 'wypadnie dokładnie jeden orzeł', 'wypadnie co najmniej jeden orzeł', 'wypadną co najmniej dwa orły', "
               "'we wszystkich rzutach wypadnie ten sam wynik', 'wypadnie więcej orłów niż reszek', 'w pierwszym rzucie wypadnie orzeł', 'wypadną dokładnie dwie reszki']"),
       ('c3n', '[1, 1, 3, 3, 7, 4, 2, 4, 4, 3]'),
       ('dt', "['na obu kostkach wypadnie ta sama liczba oczek', 'iloczyn liczb oczek będzie parzysty', 'suma oczek będzie co najmniej 10', 'na co najmniej jednej kostce wypadnie szóstka', "
              "'suma oczek będzie parzysta', 'suma oczek będzie mniejsza niż 6', 'iloczyn liczb oczek będzie nieparzysty', 'suma oczek będzie liczbą pierwszą', "
              "'na pierwszej kostce wypadnie więcej oczek niż na drugiej', 'suma oczek będzie podzielna przez 3', 'na żadnej kostce nie wypadnie szóstka', 'na co najmniej jednej kostce wypadnie parzysta liczba oczek']"),
       ('dn', '[6, 27, 6, 11, 18, 10, 9, 15, 15, 12, 25, 27]'),
       ('wq', '6 - abs(s - 7) if rel == 0 else ((13 - s) * (14 - s) // 2 if (rel == 1 and s >= 7) else (36 - (s - 2) * (s - 1) // 2 if rel == 1 else ((s - 1) * s // 2 if s <= 7 else 36 - (12 - s) * (13 - s) // 2)))'),
       ('rt', "['wyniesie ' + str(s), 'wyniesie co najmniej ' + str(s), 'wyniesie co najwyżej ' + str(s)][rel]"),
       ('ways', 'c2n[e] if mode == 0 else (c3n[e3] if mode == 1 else (wq if mode == 2 else dn[e2]))'), ('all', '4 if mode == 0 else (8 if mode == 1 else 36)'),
       ('sol', 'ways / all'),
       ('txt', "('Rzucamy dwa razy symetryczną monetą. Jakie jest prawdopodobieństwo, że ' + c2t[e] + '?') if mode == 0 else "
               "(('Rzucamy trzy razy symetryczną monetą. Jakie jest prawdopodobieństwo, że ' + c3t[e3] + '?') if mode == 1 else "
               "(('Rzucamy jednocześnie dwiema symetrycznymi sześciennymi kostkami do gry. Jakie jest prawdopodobieństwo, że suma oczek ' + rt + '?') if mode == 2 else "
               "('Rzucamy jednocześnie dwiema symetrycznymi sześciennymi kostkami do gry. Jakie jest prawdopodobieństwo, że ' + dt[e2] + '?')))")],
      fraction('@{txt} Podaj wynik jako ułamek nieskracalny.', 'numer(sol)', 'denom(sol)',
               [('idea', "@{('Wszystkich wyników jest 4: OO, OR, RO, RR.' if mode == 0 else ('Wszystkich wyników jest 8 (2 · 2 · 2). Wypisz wyniki sprzyjające.' if mode == 1 else 'Wszystkich wyników jest 36 (6 · 6). Wypisz wyniki sprzyjające.'))}"),
                ('compute', '@{ways} z @{all}, czyli $@{sol|frac}$')]),
      constraints=['denom(sol) != 1', 'ways > 0'], selfCheck=['mode != 2 or (wq >= 1 and wq <= 35)'], area=A4, prereq=['vh-prob-dice'])

skill('vh-prob-reverse', S, 'Ile kul jest w worku?', ['VII-VIII.4.6'],
      [lvl('Znamy prawdopodobieństwo', mode=0), lvl('Ile kul dołożyć?', mode=1)],
      [('den', 'choice([3, 4, 5, 6, 8])'), ('num', 'randint(1, den - 1)'), ('mult', 'randint(2, 6)'),
       ('r', 'randint(5, 15)'), ('b', 'randint(2, r - 2)'),
       ('tot', 'den * mult'),
       ('txt', "('W worku są kule czerwone i niebieskie, razem ' + str(tot) + ' kul. Prawdopodobieństwo wylosowania kuli czerwonej wynosi ' + str(num) + '/' + str(den) + '. Ile jest kul czerwonych?') if mode == 0 else "
               "('W worku są kule czerwone (' + str(r) + ') i niebieskie (' + str(b) + '). Ile kul niebieskich trzeba dołożyć, aby prawdopodobieństwo wylosowania kuli czerwonej wynosiło 1/2?')"),
       ('ans', 'num * mult if mode == 0 else r - b')],
      number('@{txt}', 'ans',
             [('idea', "@{('Liczba kul czerwonych = prawdopodobieństwo · liczba wszystkich kul.' if mode == 0 else 'Prawdopodobieństwo 1/2 oznacza, że kul czerwonych jest tyle samo co niebieskich.')}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['gcd(num, den) == 1', 'mode == 0 or r > b'], min_distinct=30, area=A4, prereq=['vh-prob-balls'])

skill('vh-prob-frequency', S, 'Doświadczenia losowe: częstość', ['VII-VIII.4.6'],
      [lvl('Częstość względna')],
      [('n', 'choice([20, 25, 40, 50, 100, 200])'), ('k', 'randint(2, n - 2)'), ('what', "choice(['orzeł w rzutach monetą', 'szóstka w rzutach kostką', 'trafienie do kosza w rzutach koszykarza'])"), ('f', 'k / n')],
      decimal('W @{n} powtórzeniach doświadczenia (@{what}) zdarzenie zaszło @{k} razy. Oblicz częstość względną tego zdarzenia (jako liczbę dziesiętną).', 'f',
              [('idea', 'Częstość względna = liczba zajść zdarzenia : liczba wszystkich prób.'), ('compute', '@{k} : @{n} = @{f|dec}')]),
      constraints=['k * 2 != n'], min_distinct=40, area=A4, prereq=['vh-prob-balls'])

skill('vh-prob-expected', S, 'Ile razy można się spodziewać zdarzenia?', ['VII-VIII.4.6'],
      [lvl('Spodziewana liczba zajść')],
      [('den', 'choice([2, 3, 4, 5, 6, 10])'), ('num', 'randint(1, den - 1)'), ('trials', 'den * randint(5, 30)'),
       ('what', "choice(['wylosowania wygranego kuponu', 'trafienia do celu', 'wyrzucenia pożądanego wyniku'])")],
      number('Prawdopodobieństwo @{what} w jednej próbie wynosi $\\frac{@{num}}{@{den}}$. Ile razy zdarzenie to zajdzie średnio w @{trials} niezależnych próbach?', 'trials * num // den',
             [('idea', 'Spodziewana liczba zajść = prawdopodobieństwo · liczba prób.'), ('compute', '@{num}/@{den} · @{trials} = @{trials * num // den}')]),
      constraints=['gcd(num, den) == 1'], min_distinct=40, area=A4, prereq=['vh-prob-frequency'])

# ============================================================================ myślenie matematyczne (5.1 - 5.3)
skill('vh-think-structure', S, 'Zapisz związki między danymi', ['VII-VIII.5.1.a'],
      [lvl('Wiek: tabelka', mode=0), lvl('Głowy i nogi', mode=1)],
      [('x', 'randint(5, 25)'), ('dd', 'randint(2, 9)'), ('k', 'randint(5, 15)'),
       ('ch', 'randint(5, 25)'), ('rb', 'randint(5, 25)'),
       ('txt', "('Ola jest o ' + str(dd) + ' lat starsza od Kuby. Za ' + str(k) + ' lat suma ich wieków wyniesie ' + str(2 * x + dd + 2 * k) + '. Ile lat ma teraz Kuba?') if mode == 0 else "
               "('Na podwórku są kury i króliki. Liczba wszystkich głów wynosi ' + str(ch + rb) + ', a liczba wszystkich nóg ' + str(2 * ch + 4 * rb) + '. Ile jest królików?')"),
       ('ans', 'x if mode == 0 else rb')],
      number('@{txt}', 'ans',
             [('idea', "@{('Zrób tabelkę: wiek Kuby x, wiek Oli x + ' + str(dd) + '; za ' + str(k) + ' lat każde jest starsze o ' + str(k) + '. Zapisz sumę jako równanie.' if mode == 0 else 'Gdyby wszystkie zwierzęta były kurami, na każdą głowę przypadałyby 2 nogi. Każdy królik ma o 2 nogi więcej, więc różnica nóg i podwojonej liczby głów to 2 · liczba królików.')}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      constraints=['mode != 1 or ch != rb'], min_distinct=40, area=A5, prereq=['vh-eq-word'])

skill('vh-think-clever', S, 'Rachunek sprytnym sposobem', ['VII-VIII.5.1.b'],
      [lvl('Mnożenie przez 25 i 4', mode=0), lvl('Mnożenie przez 125 i 8', mode=1), lvl('Mnożenie przez 99', mode=2)],
      [('x', 'randint(11, 99)'), ('big', 'randint(12, 40)'),
       ('txt', "'Oblicz sprytnie: 4 · ' + str(x) + ' · 25' if mode == 0 else ('Oblicz sprytnie: 125 · ' + str(big) + ' · 8' if mode == 1 else 'Oblicz sprytnie: 99 · ' + str(x))"),
       ('ans', '100 * x if mode == 0 else (1000 * big if mode == 1 else 99 * x)')],
      number('@{txt}', 'ans',
             [('idea', "@{('4 · 25 = 100, więc pomnóż najpierw te czynniki.' if mode == 0 else ('125 · 8 = 1000.' if mode == 1 else '99 = 100 − 1, więc 99 · x = 100x − x.'))}"),
              ('conclude', 'Wynik: @{ans}.')]),
      min_distinct=25, area=A5, prereq=['vh-think-structure'])

skill('vh-justify-right', S, 'Czy trójkąt jest prostokątny? Uzasadnij', ['VII-VIII.5.2.a', 'VII-VIII.5.3.a'],
      [lvl('Twierdzenie odwrotne do Pitagorasa')],
      [('t', 'choice([[3, 4, 5], [5, 12, 13], [8, 15, 17], [7, 24, 25]])'), ('k', 'randint(1, 3)'), ('yes', 'randint(0, 1) == 1'), ('bump', 'choice([1, 2])'),
       ('a', 't[0] * k'), ('b', 't[1] * k'), ('c', 't[2] * k if yes else t[2] * k + bump'),
       ('good', "'Tak: ' + str(a) + '² + ' + str(b) + '² = ' + str(c) + '² (' + str(a * a + b * b) + ' = ' + str(c * c) + ').' if yes else 'Nie: ' + str(a) + '² + ' + str(b) + '² = ' + str(a * a + b * b) + ', a ' + str(c) + '² = ' + str(c * c) + ' – to różne liczby.'"),
       ('w1', "'Tak, bo suma dwóch boków jest większa od trzeciego.' if not yes else 'Nie, bo ' + str(a) + ' + ' + str(b) + ' > ' + str(c) + '.'"),
       ('w2', "'Tak, bo wszystkie boki są liczbami całkowitymi.' if not yes else 'Nie, bo żaden bok nie jest dwa razy dłuższy od innego.'"),
       ('w3', "'Tak, bo ' + str(a) + ' + ' + str(b) + ' = ' + str(a + b) + ' jest bliskie ' + str(c) + '.' if not yes else 'Nie, bo trójkąt prostokątny musi być równoramienny.'")],
      choice('Trójkąt ma boki długości @{a}, @{b} i @{c}. Czy jest on prostokątny? Wybierz poprawne uzasadnienie.', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Sprawdź, czy kwadrat najdłuższego boku jest równy sumie kwadratów dwóch pozostałych. To twierdzenie odwrotne do twierdzenia Pitagorasa.'), ('conclude', '@{good}')]),
      constraints=['yes or (a * a + b * b != c * c)', 'len(uniq([good, w1, w2, w3])) == 4'], min_distinct=20, area=A5, prereq=['vh-pyth-basic'])

skill('vh-think-generalise', S, 'Uogólnianie: wzór na n-ty element', ['VII-VIII.5.3.c'],
      [lvl('Sumy liczb', mode=0), lvl('Ciąg arytmetyczny', mode=1), lvl('Wzory z zapałek', mode=2)],
      [('n', 'randint(8, 30)'), ('a', 'randint(1, 9)'), ('d', 'randint(2, 9)'), ('sh', 'randint(0, 1)'),
       ('txt', "('Suma pierwszych ' + str(n) + ' kolejnych liczb nieparzystych (1 + 3 + 5 + …) jest równa kwadratowi pewnej liczby. Ile wynosi ta suma?') if mode == 0 and sh == 0 else "
               "(('Ile wynosi suma wszystkich liczb naturalnych od 1 do ' + str(n) + '?') if mode == 0 else "
               "(('W ciągu ' + str(a) + ', ' + str(a + d) + ', ' + str(a + 2 * d) + ', ' + str(a + 3 * d) + ', … każdy następny wyraz jest większy o ' + str(d) + '. Ile wynosi ' + str(n) + '. wyraz tego ciągu?') if mode == 1 else "
               "('Z zapałek układamy w rzędzie trójkąty: jeden trójkąt wymaga 3 zapałek, dwa trójkąty 5 zapałek, trzy trójkąty 7 zapałek itd. Ile zapałek potrzeba na ' + str(n) + ' trójkątów?')))"),
       ('ans', '(n * n if sh == 0 else n * (n + 1) // 2) if mode == 0 else (a + (n - 1) * d if mode == 1 else 2 * n + 1)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Szukaj wzoru: 1 = 1², 1 + 3 = 2², 1 + 3 + 5 = 3². Suma n pierwszych nieparzystych to n².' if mode == 0 and sh == 0 else ('Sparuj pierwszą liczbę z ostatnią, drugą z przedostatnią: każda para daje n + 1. Par jest n : 2.' if mode == 0 else ('n-ty wyraz to pierwszy wyraz plus (n − 1) · różnica.' if mode == 1 else 'Pierwszy trójkąt: 3 zapałki, każdy następny dodaje 2 zapałki: 3 + 2(n − 1) = 2n + 1.')))}"),
              ('conclude', 'Odpowiedź: @{ans}.')]),
      min_distinct=20, area=A5, prereq=['vh-alg-evaluate'])

skill('vh-counterexample', S, 'Kontrprzykład do twierdzenia', ['VII-VIII.5.3.d'],
      [lvl('Znajdź przykład, który obala twierdzenie')],
      [('s', 'randint(0, 3)'), ('k', 'randint(2, 6)'), ('pi', 'randint(0, 3)'), ('wi', 'randint(0, 2)'),
       ('stm', "['Kwadrat każdej liczby jest większy od tej liczby.', 'Suma dwóch liczb pierwszych jest liczbą pierwszą.', 'Każda liczba podzielna przez 4 jest podzielna przez 8.', 'Pierwiastek kwadratowy z każdej liczby dodatniej jest mniejszy od tej liczby.']"),
       ('good', "['1/' + str(k), ['3 i 5', '5 i 7', '7 i 11', '3 i 7'][pi], str(4 * (2 * k + 1)), '1/' + str(k * k)][s]"),
       ('w1', "[str(k + 1), '2 i 3', str(8 * k), str(k * k)][s]"),
       ('w2', "[str(k * k), '2 i 5', str(16 * k), str(4 * k)][s]"),
       ('w3', "[str(k + 5), '2 i 11', str(8 * k + 8), str(k + 3)][s]")],
      choice('Kasia twierdzi: „@{stm[s]}” Który przykład pokazuje, że Kasia się myli?', 'good', ['w1', 'w2', 'w3'],
             [('idea', 'Kontrprzykład to konkretny przypadek, który spełnia założenie twierdzenia, ale nie spełnia jego tezy.'),
              ('conclude', 'Kontrprzykład: @{good}.')]),
      constraints=['len(uniq([good, w1, w2, w3])) == 4'], min_distinct=15, area=A5, prereq=['vh-justify-right'])

CONVERSE = [
    bank_choice('Twierdzenie: „Jeśli liczba jest podzielna przez 6, to jest podzielna przez 3.” Które zdanie jest twierdzeniem odwrotnym?',
                [('Jeśli liczba jest podzielna przez 3, to jest podzielna przez 6.', True), ('Jeśli liczba nie jest podzielna przez 6, to nie jest podzielna przez 3.', False),
                 ('Jeśli liczba jest podzielna przez 6, to nie jest podzielna przez 3.', False), ('Liczba podzielna przez 3 jest nieparzysta.', False)],
                [('idea', 'W twierdzeniu odwrotnym zamieniamy miejscami założenie i tezę.')]),
    bank_choice('Czy twierdzenie odwrotne do „Jeśli liczba jest podzielna przez 6, to jest podzielna przez 3” jest prawdziwe?',
                [('Nie – np. 9 jest podzielna przez 3, ale nie przez 6.', True), ('Tak – zawsze, gdy twierdzenie jest prawdziwe, jego odwrotne też.', False),
                 ('Tak – bo 6 jest wielokrotnością 3.', False), ('Nie da się tego sprawdzić.', False)],
                [('idea', 'Twierdzenie prawdziwe nie musi mieć prawdziwego twierdzenia odwrotnego. Jeden przykład to pokazuje.')]),
    bank_choice('Twierdzenie: „Jeśli czworokąt jest kwadratem, to ma wszystkie boki równe.” Czy twierdzenie odwrotne jest prawdziwe?',
                [('Nie – romb ma wszystkie boki równe i nie musi być kwadratem.', True), ('Tak – kwadrat jest jedynym takim czworokątem.', False),
                 ('Tak – bo boki są równe.', False), ('Tak, ale tylko w układzie współrzędnych.', False)],
                [('idea', 'Szukamy figury, która spełnia tezę, a nie spełnia założenia.')]),
    bank_choice('Twierdzenie Pitagorasa: „Jeśli trójkąt jest prostokątny, to a² + b² = c².” Które zdanie jest twierdzeniem odwrotnym?',
                [('Jeśli w trójkącie a² + b² = c², to trójkąt jest prostokątny.', True), ('Jeśli trójkąt nie jest prostokątny, to a² + b² = c².', False),
                 ('Jeśli trójkąt jest prostokątny, to a² + b² ≠ c².', False), ('W każdym trójkącie a² + b² = c².', False)],
                [('idea', 'Zamień miejscami założenie i tezę. Twierdzenie odwrotne do Pitagorasa również jest prawdziwe.')]),
    bank_choice('Twierdzenie: „Jeśli n jest liczbą parzystą, to n² jest liczbą parzystą.” Które zdanie jest twierdzeniem odwrotnym?',
                [('Jeśli n² jest liczbą parzystą, to n jest liczbą parzystą.', True), ('Jeśli n jest nieparzysta, to n² jest nieparzysta.', False),
                 ('Jeśli n jest parzysta, to n² jest nieparzysta.', False), ('Jeśli n² jest nieparzysta, to n jest parzysta.', False)],
                [('idea', 'Założenie i teza zamieniają się miejscami.')]),
    bank_choice('Zdanie „Jeśli pada deszcz, to ulica jest mokra” jest prawdziwe. Czy z tego wynika, że zdanie „Jeśli ulica jest mokra, to pada deszcz” też jest prawdziwe?',
                [('Nie – ulica może być mokra z innego powodu, np. po myciu.', True), ('Tak – oba zdania znaczą to samo.', False),
                 ('Tak – gdy ulica jest mokra, zawsze pada.', False), ('Tak, jeśli jest zima.', False)],
                [('idea', 'Twierdzenie i twierdzenie odwrotne to dwa różne zdania; jedno może być prawdziwe, a drugie fałszywe.')]),
]
bank_skill('vh-converse', S, 'Twierdzenie i twierdzenie odwrotne', ['VII-VIII.5.3.a'], CONVERSE, levels=['Twierdzenie odwrotne'], tags=('thinking',), area=A5, prereq=['vh-justify-right'],
           intro='Twierdzenie „jeśli A, to B” ma twierdzenie odwrotne „jeśli B, to A”. Prawdziwość jednego nie gwarantuje prawdziwości drugiego.')

INDIRECT = [
    bank_choice('Chcemy wykazać nie wprost, że nie istnieje największa liczba naturalna. Od czego zaczniemy?',
                [('Założymy, że taka największa liczba N istnieje, i znajdziemy sprzeczność (N + 1 jest większa).', True), ('Wypiszemy wszystkie liczby naturalne.', False),
                 ('Założymy, że N + 1 jest mniejsza od N.', False), ('Sprawdzimy kilka przykładów.', False)],
                [('idea', 'Dowód nie wprost: zakładamy zaprzeczenie tezy i dochodzimy do sprzeczności.')]),
    bank_choice('Chcemy uzasadnić nie wprost: „Jeśli n² jest nieparzyste, to n jest nieparzyste”. Co założymy?',
                [('Że n jest parzyste, i pokażemy, że wtedy n² byłoby parzyste (sprzeczność).', True), ('Że n² jest parzyste.', False),
                 ('Że n jest nieparzyste i n² parzyste.', False), ('Nic nie zakładamy.', False)],
                [('idea', 'Zaprzeczamy tezie: „n nie jest nieparzyste”, czyli n jest parzyste.')]),
    bank_choice('Wykaż, że w trójkącie nie ma dwóch kątów rozwartych. Które rozumowanie jest poprawne?',
                [('Gdyby były dwa kąty rozwarte, ich suma byłaby większa od 180°, a suma kątów trójkąta to 180° – sprzeczność.', True),
                 ('Narysowałem trójkąt z jednym kątem rozwartym, więc dwa nie mogą istnieć.', False),
                 ('Kąty rozwarte są duże, więc nie mieszczą się w trójkącie.', False), ('Trójkąty mają zawsze kąty ostre.', False)],
                [('idea', 'Zakładamy przeciwieństwo tezy i pokazujemy sprzeczność z własnością o sumie kątów.')]),
    bank_choice('Chcemy uzasadnić, że równanie x + 1 = x nie ma rozwiązania. Które rozumowanie nie wprost jest poprawne?',
                [('Załóżmy, że x jest rozwiązaniem. Odejmując x od obu stron, dostajemy 1 = 0 – sprzeczność.', True), ('Sprawdzę x = 1, x = 2 i x = 3; żadna nie pasuje, więc nie ma rozwiązania.', False),
                 ('Równanie ma rozwiązanie, bo x + 1 jest większe od x.', False), ('Przenoszę x na prawą stronę i zmieniam znak na 1 = x.', False)],
                [('idea', 'Zakładamy, że teza (brak rozwiązania) jest fałszywa, i prowadzi to do sprzeczności 1 = 0.')]),
    bank_choice('Wszystkie 5 kul, które wyjęto z pudełka, było czerwonych lub niebieskich, a wiemy, że w pudełku jest co najmniej 6 kul i żadna nie jest zielona. Chcemy uzasadnić, że wśród wyjętych są co najmniej 3 kule jednego koloru. Jak?',
                [('Gdyby każdego koloru było najwyżej 2, kul byłoby najwyżej 4 – sprzeczność z 5 wyjętymi.', True), ('Wystarczy jedna próba losowania.', False),
                 ('Zielone kule nie istnieją, więc teza jest oczywista.', False), ('Nie da się tego uzasadnić.', False)],
                [('idea', 'Zaprzeczamy tezie („każdego koloru najwyżej 2”) i pokazujemy sprzeczność.')]),
]
bank_skill('vh-indirect', S, 'Rozumowanie nie wprost', ['VII-VIII.5.3.b'], INDIRECT, levels=['Dowód nie wprost'], tags=('thinking',), area=A5, prereq=['vh-converse'],
           intro='W rozumowaniu nie wprost zakładamy, że teza jest fałszywa, i pokazujemy, że prowadzi to do sprzeczności.')

MINARG = [
    bank_choice('Chcesz uzasadnić, że przekątne rombu są prostopadłe. Który zestaw argumentów jest wystarczający i bez zbędnych elementów?',
                [('Romb ma wszystkie boki równe, więc jest deltoidem, a przekątne deltoidu są prostopadłe.', True), ('Romb jest ładny i symetryczny.', False),
                 ('Narysowałem jeden romb i przekątne wyglądają na prostopadłe.', False), ('Romb ma cztery boki, a cztery to liczba parzysta.', False)],
                [('idea', 'Dobre uzasadnienie odwołuje się tylko do potrzebnych własności figury.')]),
    bank_choice('Wykaż, że suma dwóch kolejnych liczb nieparzystych jest podzielna przez 4. Które uzasadnienie jest najkrótsze i poprawne?',
                [('Liczby to 2k − 1 i 2k + 1, ich suma to 4k.', True), ('3 + 5 = 8, 5 + 7 = 12, 7 + 9 = 16 – działa.', False),
                 ('Liczby nieparzyste są zawsze podzielne przez 4.', False), ('Suma dwóch liczb jest zawsze parzysta, więc wystarczy.', False)],
                [('idea', 'Zapis ogólny (z literą) pokazuje związek dla wszystkich takich par, a sprawdzenie kilku przykładów – nie.')]),
    bank_choice('Uzasadniasz, że liczba 4 · 7 · 11 jest podzielna przez 14. Które sformułowanie zawiera tylko potrzebne argumenty?',
                [('Liczba zawiera czynnik 7 i czynnik 4, który jest podzielny przez 2, więc dzieli się przez 2 · 7 = 14.', True), ('Liczba jest duża i jest iloczynem trzech liczb.', False),
                 ('Obliczyłem iloczyn i dzielę go długo przez 14.', False), ('Liczba 11 jest pierwsza.', False)],
                [('idea', 'Wystarczy wskazać czynniki 2 i 7 – reszta danych (11) jest niepotrzebna.')]),
    bank_choice('Uzasadniasz, że pole trójkąta o podstawie 10 cm i wysokości 6 cm wynosi 30 cm². Który zapis jest wystarczający?',
                [('P = ½ · 10 · 6 = 30 cm².', True), ('Trójkąt jest mały, a 30 to ładna liczba.', False), ('10 + 6 = 16, więc pole wynosi 16 cm².', False), ('Pole to obwód podzielony przez 2.', False)],
                [('idea', 'Zastosuj właściwy wzór i krótko zapisz obliczenia.')]),
]
bank_skill('vh-minimal-argument', S, 'Uzasadnienie bez zbędnych argumentów', ['VII-VIII.5.2.b'], MINARG, levels=['Krótkie uzasadnienie'], tags=('thinking',), area=A5, prereq=['vh-justify-right'],
           intro='Dobre uzasadnienie zawiera tylko niezbędne kroki. Sprawdzenie kilku przykładów nie jest dowodem – potrzebny jest argument ogólny.')

CONCLUSIONS = [
    bank_choice('W klasie 4 z 20 uczniów ma psa. Który wniosek wynika z tej informacji?',
                [('20% uczniów w tej klasie ma psa.', True), ('Większość uczniów w Polsce ma psa.', False), ('Każdy uczeń ma kota.', False), ('Pies jest najlepszym zwierzęciem.', False)],
                [('idea', 'Wniosek może dotyczyć tylko tej grupy, której dotyczą dane.')]),
    bank_choice('Wiemy, że wszystkie kwadraty są prostokątami i że figura F jest kwadratem. Co wynika?',
                [('Figura F jest prostokątem.', True), ('Figura F ma boki długości 4.', False), ('Każdy prostokąt jest kwadratem.', False), ('Figura F ma pole 16.', False)],
                [('idea', 'Z faktu „każdy A jest B” i „F jest A” wynika „F jest B”.')]),
    bank_choice('Pole prostokąta wynosi 24 cm², a jeden bok 4 cm. Co wynika z tych danych?',
                [('Drugi bok ma 6 cm.', True), ('Obwód wynosi 24 cm.', False), ('Prostokąt jest kwadratem.', False), ('Drugi bok ma 20 cm.', False)],
                [('idea', 'Z pola P = a · b i znanej wartości a wynika b = P : a.')]),
    bank_choice('W sklepie cena butów wzrosła o 20%, a potem spadła o 20%. Który wniosek jest poprawny?',
                [('Końcowa cena jest niższa od początkowej.', True), ('Końcowa cena jest taka sama jak początkowa.', False), ('Końcowa cena jest wyższa.', False), ('Nie da się nic stwierdzić.', False)],
                [('idea', 'Po wzroście o 20% cena to 1,2 ceny początkowej; 80% z niej to 0,96 ceny początkowej.')]),
    bank_choice('Z kosza wylosowano 5 jabłek i wszystkie były dojrzałe. Który wniosek jest uzasadniony?',
                [('Wszystkie wylosowane jabłka były dojrzałe.', True), ('Wszystkie jabłka w koszu są dojrzałe.', False), ('W koszu nie ma niedojrzałych jabłek.', False), ('Kosz zawiera dokładnie 5 jabłek.', False)],
                [('idea', 'Z próby nie wynika pewność o całej grupie.')]),
]
bank_skill('vh-conclusions', S, 'Wnioski z rozumowania', ['VII-VIII.5.2.c'], CONCLUSIONS, levels=['Co wynika z danych?'], tags=('thinking',), area=A5, prereq=['vh-minimal-argument'],
           intro='Wniosek musi wynikać z podanych informacji. Uważaj na przejście od próbki do całej grupy.')

SIMILAR = [
    bank_choice('Zadanie 1: dwa pociągi jadą naprzeciw siebie z prędkościami 60 km/h i 80 km/h. Zadanie 2: dwie pompy napełniają basen z wydajnością 60 l/min i 80 l/min. Co mają wspólnego?',
                [('W obu dodajemy tempa pracy lub ruchu (prędkości lub wydajności).', True), ('Nic – dotyczą różnych dziedzin.', False), ('Oba można rozwiązać tylko rysunkiem.', False), ('W obu trzeba pomnożyć 60 · 80.', False)],
                [('idea', 'Różne konteksty mogą mieć tę samą strukturę matematyczną: tempo · czas = ilość.')]),
    bank_choice('Zadanie 1: „Oblicz 15% z 80”. Zadanie 2: „Z 80 zł zapłacono 15% podatku. Ile to zł?” Jaka jest relacja między nimi?',
                [('To to samo zadanie opisane innymi słowami.', True), ('Zupełnie różne zadania.', False), ('Pierwsze jest trudniejsze.', False), ('Drugie nie ma rozwiązania.', False)],
                [('idea', 'Szukaj wspólnej metody: procent liczby = liczba · procent.')]),
    bank_choice('Znasz metodę liczenia pola prostokąta (długość · szerokość). Zadanie o pokryciu podłogi płytkami przypomina, że:',
                [('liczymy pole podłogi i dzielimy przez pole jednej płytki.', True), ('płytki trzeba zawsze kupować parzystą liczbę.', False), ('pole nie ma tu znaczenia.', False), ('płytek jest tyle co metrów.', False)],
                [('idea', 'Znajoma metoda (pole figury) przenosi się na nowe zadanie.')]),
    bank_choice('Rozwiązałeś równanie 3x + 5 = 20. Które z poniższych zadań rozwiążesz podobnie?',
                [('„Kuba kupił 3 zeszyty i długopis za 5 zł. Razem zapłacił 20 zł. Ile kosztuje zeszyt?”', True), ('„Ile jest 20 : 5?”', False), ('„Oblicz pole trójkąta.”', False), ('„Który kąt jest rozwarty?”', False)],
                [('idea', 'Obie sytuacje prowadzą do równania pierwszego stopnia z jedną niewiadomą.')]),
    bank_choice('Droga = prędkość · czas, praca = wydajność · czas. Co jest wspólną ideą?',
                [('Wielkość całkowita jest iloczynem tempa i czasu.', True), ('Obie wielkości są zawsze równe.', False), ('Czas jest zawsze mniejszy od tempa.', False), ('Nie ma nic wspólnego.', False)],
                [('idea', 'Dostrzeganie podobieństw między metodami ułatwia rozwiązywanie nowych zadań.')]),
]
bank_skill('vh-similar-methods', S, 'Podobne zadania, ta sama metoda', ['VII-VIII.5.1.d'], SIMILAR, levels=['Wspólna metoda'], tags=('thinking',), area=A5, prereq=['vh-think-structure'],
           intro='Różne zadania często mają tę samą strukturę. Gdy ją dostrzeżesz, możesz użyć znanej metody.')

SIMPLIFY = [
    bank_choice('Rozwiązanie: 25 · 36 · 4 = (25 · 4) · 36 = 100 · 36 = 3600. Co o nim można powiedzieć?',
                [('Jest uproszczone dzięki zamianie kolejności i grupowaniu czynników.', True), ('Jest błędne, bo zmieniono kolejność.', False), ('Jest długie i można je tylko wydłużyć.', False), ('Nie ma związku z mnożeniem.', False)],
                [('idea', 'Zmiana kolejności mnożenia nie zmienia wyniku. Wybieramy parę, która daje okrągłą liczbę.')]),
    bank_choice('Kuba rozwiązał zadanie na 10 linijek, a Ola na 3 i otrzymali ten sam wynik. Co zrobisz po analizie obu rozwiązań?',
                [('Sprawdzę, czy krótszy sposób jest poprawny, i użyję go w podobnych zadaniach.', True), ('Zawsze wybiorę dłuższy sposób.', False), ('Pominę rozwiązanie Oli.', False), ('Uznam, że wynik jest zły, bo różnią się długością.', False)],
                [('idea', 'Po rozwiązaniu warto zastanowić się, czy da się je uprościć.')]),
    bank_choice('Chcesz policzyć 99 · 47. Który zapis jest najprostszy?',
                [('100 · 47 − 47 = 4700 − 47 = 4653', True), ('99 · 40 + 99 · 7 = 3960 + 693', False), ('99 · 47 = 99 · 50 − 99 · 3', False), ('47 · 99 = 47 · 9 · 11', False)],
                [('idea', 'Zapis 99 = 100 − 1 prowadzi do najkrótszych obliczeń w pamięci.')]),
    bank_choice('Rozwiązujesz równanie 2(x + 3) = 14. Które pierwsze działanie jest najprostsze?',
                [('Podzielić obie strony przez 2: x + 3 = 7.', True), ('Opuścić nawias: 2x + 6 = 14 i dalej.', False), ('Zgadywać x.', False), ('Pomnożyć obie strony przez x.', False)],
                [('idea', 'Dzielenie przez 2 od razu daje prostsze równanie.')]),
]
bank_skill('vh-simplify-solution', S, 'Czy da się prościej?', ['VII-VIII.5.1.b'], SIMPLIFY, levels=['Prostsze rozwiązanie'], tags=('thinking',), area=A5, prereq=['vh-think-clever'],
           intro='Po rozwiązaniu zadania spytaj: czy to samo można zrobić krócej? Często wystarczy zmienić kolejność lub zastosować znaną sztuczkę.')

# ============================================================================ ścieżka
un = Unit(S, 'vh-u13', 'Dane i wykresy', 'Wiarygodne źródła, dobór wykresu, odczyt wykresów drogi i cen oraz krytyczna interpretacja.', 'chart', area=A4)
un.learn('vh-data-sources', tasks=5).learn('vh-chart-choice', tasks=5).learn('vh-graph-distance').learn('vh-graph-change').learn('vh-data-critical', tasks=6)
un.checkpoint(['vh-graph-distance', 'vh-graph-change'])

un = Unit(S, 'vh-u14', 'Średnia i mediana', 'Średnia arytmetyczna, mediana i wybór miary do opisu danych.', 'average', area=A4)
un.learn('vh-mean-exact').learn('vh-median').learn('vh-mean-outlier').learn('vh-mean-missing')
un.checkpoint(['vh-mean-exact', 'vh-median', 'vh-mean-outlier', 'vh-mean-missing'])

un = Unit(S, 'vh-u15', 'Prawdopodobieństwo', 'Losowanie kul, rzuty monetą i kostką, częstość i spodziewana liczba zajść.', 'dice', area=A4)
un.learn('vh-prob-balls').learn('vh-prob-dice').learn('vh-prob-two').learn('vh-prob-reverse').learn('vh-prob-frequency').learn('vh-prob-expected')
un.checkpoint(['vh-prob-balls', 'vh-prob-dice', 'vh-prob-two', 'vh-prob-reverse', 'vh-prob-expected'])

un = Unit(S, 'vh-u16', 'Myślenie matematyczne', 'Zapisywanie związków, upraszczanie, uzasadnianie, twierdzenie odwrotne, kontrprzykłady i dowód nie wprost.', 'brain', area=A5)
un.learn('vh-think-structure').learn('vh-think-clever').learn('vh-simplify-solution', tasks=4).learn('vh-similar-methods', tasks=5).learn('vh-justify-right')
un.learn('vh-think-generalise').learn('vh-counterexample').learn('vh-converse', tasks=6).learn('vh-indirect', tasks=5).learn('vh-minimal-argument', tasks=4).learn('vh-conclusions', tasks=5)
un.checkpoint(['vh-think-structure', 'vh-justify-right', 'vh-think-generalise', 'vh-counterexample'])
