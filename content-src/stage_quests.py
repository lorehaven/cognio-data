"""Quests: story-driven multi-step activities realising the 'doświadczenia edukacyjne' of the regulation (stages IV-VI and VII-VIII).

One quest instance draws its variables once; every step is an ordinary task, so the usual checker, hints and error rules apply.
A quest is a skill with one level whose task source is quests/<id>.json; the path lists it as a lesson of kind 'quest'."""
from dsl import *

TABLE = 'table'


def table(alt, headers, rows, essential=True):
    return {'type': 'table', 'kind': 'table', 'essential': essential, 'alt': alt, 'params': {'headers': headers, 'rows': rows}}


S46, S78 = 'IV-VI', 'VII-VIII'

# ============================================================================ IV-VI, experience 0: data about a social / environmental issue
quest('q46-water', S46, 'Misja: ile wody zużywa nasza klasa?', 0,
      "Klasa 4b prowadziła przez tydzień szkolny dziennik zużycia wody w szkolnej łazience (w litrach). Pomóż uczniom opracować dane i sformułować wnioski.",
      [number('Ile litrów wody zużyto @{dp[i]}?', 'vs[i]',
              [('idea', 'Znajdź w tabeli właściwy dzień i odczytaj liczbę z drugiej kolumny.'), ('conclude', 'Odpowiedź: @{vs[i]} l.')]),
       number('Ile litrów wody klasa zużyła w ciągu całego tygodnia szkolnego (5 dni)?', 'sum(vs)',
              [('idea', 'Dodaj zużycie ze wszystkich pięciu dni.'), ('compute', '@{join(vs, " + ")} = @{sum(vs)}')]),
       number('Oblicz średnie dzienne zużycie wody (w litrach).', 'm',
              [('idea', 'Średnia = suma : liczba dni.'), ('compute', '@{sum(vs)} : 5 = @{m}')]),
       number('W ilu dniach zużycie wody było większe od średniej?', 'above',
              [('idea', 'Porównaj zużycie z każdego dnia ze średnią @{m} l.'), ('conclude', 'Odpowiedź: @{above}.')]),
       decimal('Klasa postanowiła zmniejszyć średnie dzienne zużycie wody o 10%. Ile litrów dziennie (średnio) będzie wtedy zużywać?', 'm * 9 / 10',
               [('idea', '10% z @{m} l to @{m / 10|dec} l. Odejmij to od średniej.'), ('conclude', 'Odpowiedź: @{m * 9 / 10|dec} l.')]),
       number('Ile litrów wody klasa zaoszczędzi w ciągu 20 takich tygodni (po 5 dni), jeśli osiągnie ten cel?', '10 * m',
              [('idea', 'Dziennie oszczędza 10% średniej. Pomnóż przez liczbę dni: 20 · 5 = 100.'), ('compute', '@{m / 10|dec} · 100 = @{10 * m}')]),
       choice('Które zdanie jest poprawnym wnioskiem z zebranych danych?', 'g1', ['g2', 'g3', 'g4'],
              [('idea', 'Wniosek może dotyczyć tylko tego, co zmierzono: tego tygodnia w tej klasie.'), ('conclude', '@{g1}')])],
      [('m', 'randint(40, 90)'), ('r4', 'sample(m - 15, m + 15, 4)'), ('last', '5 * m - sum(r4)'), ('vs', 'shuffle(r4 + [last])'),
       ('days', "['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek']"), ('dp', "['w poniedziałek', 'we wtorek', 'w środę', 'w czwartek', 'w piątek']"), ('i', 'randint(0, 4)'),
       ('above', '(1 if vs[0] > m else 0) + (1 if vs[1] > m else 0) + (1 if vs[2] > m else 0) + (1 if vs[3] > m else 0) + (1 if vs[4] > m else 0)'),
       ('g1', "'W badanym tygodniu średnie dzienne zużycie wody w klasie wyniosło ' + str(m) + ' l.'"),
       ('g2', "'W każdym tygodniu roku klasa zużywa dokładnie ' + str(sum(vs)) + ' l wody.'"),
       ('g3', "'Cała szkoła zużywa dziennie ' + str(m) + ' l wody.'"),
       ('g4', "'Zużycie wody rośnie od poniedziałku do piątku.'")],
      outro='Świetna robota! Dzięki zebranym danym klasa wie, ile wody zużywa, i może zaplanować oszczędzanie.',
      media=[table('Tabela: zużycie wody w kolejnych dniach (litry).', ['Dzień', 'Zużycie wody (l)'],
                   E("[[days[0], vs[0]], [days[1], vs[1]], [days[2], vs[2]], [days[3], vs[3]], [days[4], vs[4]]]"))],
      constraints=['last >= m - 25 and last <= m + 25', 'last not in r4', 'len(uniq([vs[0], vs[1], vs[2], vs[3], vs[4]])) == 5', 'above != 0 and above != 5 and not (vs[4] == m)'],
      selfCheck=['sum(vs) == 5 * m'], objectives=['IV-VI.5.2', 'IV-VI.5.3'], area='IV-VI.5', prereq=['n46-mean'],
      desc='Doświadczenie: opracowanie danych z życia, średnia arytmetyczna i wnioski.')

# ============================================================================ IV-VI, experience 1: cost simulation of a class trip
quest('q46-trip', S46, 'Misja: budżet wycieczki klasowej', 1,
      "Klasa liczy @{pln(n, ['osobę', 'osoby', 'osób'])} i planuje wycieczkę do muzeum. Dostała dwie oferty: A i B. Każda obejmuje przejazd autokarem (cena za cały autokar) i bilety wstępu (cena za jednego ucznia). Porównaj koszty i zaproponuj najlepsze rozwiązanie.",
      [quantity('Ile złotych kosztuje cała wycieczka według oferty A?', 'ca', 'zł',
                [('idea', 'Koszt = cena autokaru + liczba uczniów · cena biletu.'), ('compute', '@{ba} + @{n} · @{ta} = @{ca}')], unit_expr=False),
       quantity('Ile złotych kosztuje cała wycieczka według oferty B?', 'cb', 'zł',
                [('idea', 'Koszt = cena autokaru + liczba uczniów · cena biletu.'), ('compute', '@{bb} + @{n} · @{tb} = @{cb}')]),
       quantity('O ile złotych tańsza jest korzystniejsza oferta?', 'abs(ca - cb)', 'zł',
                [('idea', 'Odejmij mniejszą kwotę od większej.'), ('compute', '@{max(ca, cb)} − @{min(ca, cb)} = @{abs(ca - cb)}')]),
       choice_text('Którą ofertę powinna wybrać klasa, jeśli zależy jej na najniższym koszcie?', [('Ofertę A', 'ca < cb'), ('Ofertę B', 'cb < ca')], None,
                   [('idea', 'Wybieramy ofertę, której całkowity koszt jest mniejszy.'), ('conclude', "@{('Oferta A: ' + str(ca) + ' zł.' if ca < cb else 'Oferta B: ' + str(cb) + ' zł.')}")], fixed_order=True),
       number('Koszt wybranej oferty dzielimy po równo między wszystkich uczniów; wpłata każdego ucznia jest zaokrąglona w górę do pełnego złotego. Ile złotych wpłaca każdy uczeń?', 'ceil(best / n)',
              [('idea', 'Podziel koszt przez liczbę uczniów i zaokrąglij wynik w górę, bo nie można zebrać „ułamka” złotego za mało.'), ('compute', '@{best} : @{n} daje @{best // n} i resztę @{best % n}, więc po zaokrągleniu w górę: @{ceil(best / n)} zł')]),
       number('Ile złotych nadwyżki zostanie po zebraniu wpłat?', 'ceil(best / n) * n - best',
              [('idea', 'Nadwyżka = suma wpłat − koszt wycieczki.'), ('compute', '@{ceil(best / n)} · @{n} − @{best} = @{ceil(best / n) * n - best}')])],
      [('n', 'randint(20, 28)'), ('ba', '100 * randint(8, 14)'), ('ta', 'randint(12, 25)'), ('bb', '100 * randint(6, 12)'), ('tb', 'randint(15, 30)'),
       ('ca', 'ba + n * ta'), ('cb', 'bb + n * tb'), ('best', 'min(ca, cb)')],
      outro='Klasa ma gotową propozycję: wybrała tańszą ofertę i wie, ile każdy uczeń ma wpłacić.',
      media=[table('Tabela: dwie oferty wycieczki.', ['Oferta', 'Autokar (zł)', 'Bilet (zł za ucznia)'], E("[['A', ba, ta], ['B', bb, tb]]"))],
      constraints=['ca != cb', 'abs(ca - cb) >= 20'], objectives=['IV-VI.1.35', 'IV-VI.1.34'], area='IV-VI.1', prereq=['n46-offer-compare'], tags=('finance', 'thinking'),
      desc='Doświadczenie: symulacja kosztów przedsięwzięcia i wybór opłacalnego wariantu.')

# ============================================================================ IV-VI, experience 2: plan of a room in a scale
quest('q46-plan', S46, 'Misja: plan sali w skali', 2,
      "Klasa mierzy salę lekcyjną: ma ona @{L} m długości i @{Wd} m szerokości. Uczniowie rysują jej plan w skali 1 : @{s}. Pomóż obliczyć rozmiary planu i przygotować remont podłogi.",
      [quantity('Jaką długość (w centymetrach) ma sala na planie?', 'L * 100 / s', 'cm',
                [('idea', 'Skala 1 : @{s} oznacza, że 1 cm na planie to @{s} cm w rzeczywistości. Zamień @{L} m na centymetry i podziel przez @{s}.'), ('compute', '@{L * 100} : @{s} = @{L * 100 / s|dec}')]),
       quantity('Jaką szerokość (w centymetrach) ma sala na planie?', 'Wd * 100 / s', 'cm',
                [('idea', 'Postępuj tak samo jak z długością.'), ('compute', '@{Wd * 100} : @{s} = @{Wd * 100 / s|dec}')]),
       quantity('Jakie jest rzeczywiste pole podłogi w sali?', 'L * Wd', 'm²',
                [('idea', 'Pole prostokąta = długość · szerokość.'), ('compute', '@{L} · @{Wd} = @{L * Wd}')]),
       quantity('Jakie pole ma prostokąt przedstawiający salę na planie?', 'L * 100 / s * Wd * 100 / s', 'cm²',
                [('idea', 'Pomnóż rozmiary planu z poprzednich kroków.'), ('compute', '@{L * 100 / s|dec} · @{Wd * 100 / s|dec} = @{L * 100 / s * Wd * 100 / s|dec}')]),
       quantity('Wzdłuż wszystkich ścian (oprócz drzwi o szerokości 1 m) klasa chce przybić listwy przypodłogowe. Ile metrów listew potrzeba?', '2 * (L + Wd) - 1', 'm',
                [('idea', 'Obwód sali minus szerokość drzwi.'), ('compute', '2 · (@{L} + @{Wd}) − 1 = @{2 * (L + Wd) - 1}')]),
       number('Podłogę pokryją kwadratowymi płytkami o boku 50 cm, bez przycinania. Ile płytek trzeba kupić?', '(2 * L) * (2 * Wd)',
              [('idea', 'Wzdłuż 1 m mieszczą się 2 płytki. Policz płytki wzdłuż długości i szerokości i pomnóż.'), ('compute', '@{2 * L} · @{2 * Wd} = @{(2 * L) * (2 * Wd)}')])],
      [('L', 'randint(6, 12)'), ('Wd', 'randint(4, 9)'), ('s', 'choice([20, 25, 50, 100])')],
      outro='Plan gotowy! Znasz rozmiary sali na rysunku, jej pole i liczbę płytek potrzebnych do remontu.',
      media=[fig('rect', 'Prostokątny kształt sali z podanymi wymiarami.', essential=False, w=E('L'), h=E('Wd'), unit='m')],
      constraints=['L > Wd + 1'], objectives=['IV-VI.2.9', 'IV-VI.4.14'], area='IV-VI.2', prereq=['n46-scale-map', 'n46-area-rect'],
      desc='Doświadczenie: plan pomieszczenia w wybranej skali na podstawie pomiarów.')

# ============================================================================ IV-VI, experience 3: an everyday interdisciplinary problem
quest('q46-garden', S46, 'Misja: szkolny ogródek warzywny', 3,
      "Szkoła zakłada prostokątny ogródek o wymiarach @{a} m na @{b} m. Warzywa zajmą @{k}/5 jego powierzchni. Ogródek trzeba ogrodzić i obsiać. Oblicz, co potrzeba kupić i ile to będzie kosztowało.",
      [quantity('Ogrodzenie ma obejmować cały obwód ogródka z wyjątkiem furtki o szerokości 3 m. Ile metrów siatki trzeba kupić?', '2 * (a + b) - 3', 'm',
                [('idea', 'Obwód prostokąta to 2 · (a + b). Od obwodu odejmij szerokość furtki.'), ('compute', '2 · (@{a} + @{b}) − 3 = @{2 * (a + b) - 3}')]),
       quantity('Metr siatki kosztuje @{pm} zł. Ile złotych kosztuje cała siatka?', '(2 * (a + b) - 3) * pm', 'zł',
                [('idea', 'Koszt = liczba metrów · cena metra.'), ('compute', '@{2 * (a + b) - 3} · @{pm} = @{(2 * (a + b) - 3) * pm}')]),
       quantity('Jakie pole ma cały ogródek?', 'a * b', 'm²',
                [('idea', 'Pole prostokąta = długość · szerokość.'), ('compute', '@{a} · @{b} = @{a * b}')]),
       quantity('Jakie pole zajmą warzywa?', 'a * b * k / 5', 'm²',
                [('idea', 'Znajdź jedną piątą pola i pomnóż przez @{k}.'), ('compute', '@{a * b} : 5 · @{k} = @{a * b * k / 5}')]),
       quantity('Na każdy metr kwadratowy warzyw trzeba wysiać @{gm} g nasion. Ile gramów nasion trzeba kupić?', 'a * b * k / 5 * gm', 'g',
                [('idea', 'Pole warzyw razy ilość nasion na 1 m².'), ('compute', '@{a * b * k / 5} · @{gm} = @{a * b * k / 5 * gm}')]),
       quantity('Jaki procent powierzchni ogródka zajmują warzywa?', '20 * k', '%',
                [('idea', '$\\frac{1}{5}$ to 20%. Pomnóż przez @{k}.'), ('compute', '@{k} · 20% = @{20 * k}%')])],
      [('a', 'randint(8, 20)'), ('b', 'randint(5, 12)'), ('pm', 'randint(12, 30)'), ('gm', 'randint(3, 9)'), ('k', 'randint(2, 4)')],
      outro='Ogródek jest zaplanowany: wiemy, ile siatki i nasion trzeba kupić oraz jaką część zajmą warzywa.',
      media=[fig('rect', 'Prostokątny ogródek z podanymi wymiarami.', w=E('a'), h=E('b'), unit='m')],
      constraints=['(a * b) % 5 == 0', 'a != b'], objectives=['IV-VI.4.14', 'IV-VI.4.15', 'IV-VI.1.35'], area='IV-VI.4', prereq=['n46-area-rect', 'n46-perimeter-unknown'], tags=('finance', 'thinking'),
      desc='Doświadczenie: rozwiązanie problemu z życia z użyciem obwodu, pola, ułamków i procentów.')

# ============================================================================ VII-VIII, experience 0: architecture described with the language of maths
quest('q78-arch', S78, 'Misja: okno w kształcie łuku', 0,
      "Zabytkowa kamienica ma okno w kształcie prostokąta z półkolem na górze. Szerokość okna wynosi @{w} dm, wysokość prostokątnej części @{h} dm, a półkole ma średnicę równą szerokości okna. Opisz okno językiem matematyki (przyjmij π ≈ 3,14).",
      [number('Jaki promień ma półkole (w decymetrach)?', 'w // 2',
              [('idea', 'Promień to połowa średnicy.'), ('compute', '@{w} : 2 = @{w // 2}')]),
       quantity('Jakie pole ma prostokątna część okna?', 'w * h', 'dm²',
                [('idea', 'Pole prostokąta = szerokość · wysokość.'), ('compute', '@{w} · @{h} = @{w * h}')]),
       quantity('Jakie pole ma półkole?', '314 / 100 * (w // 2) * (w // 2) / 2', 'dm²',
                [('idea', 'Pole półkola to połowa pola koła: $\\frac{1}{2}\\pi r^2$.'), ('compute', '3,14 · @{w // 2}² : 2 = @{314 / 100 * (w // 2) * (w // 2) / 2|dec}')]),
       quantity('Jakie pole ma całe okno?', 'w * h + 314 / 100 * (w // 2) * (w // 2) / 2', 'dm²',
                [('idea', 'Dodaj pole prostokąta i półkola.'), ('compute', '@{w * h} + @{314 / 100 * (w // 2) * (w // 2) / 2|dec} = @{w * h + 314 / 100 * (w // 2) * (w // 2) / 2|dec}')]),
       quantity('Jaką długość ma drewniana rama okna (trzy boki prostokąta i łuk półkola; dolnego boku nie liczymy)?', '2 * h + w + 314 / 100 * (w // 2)', 'dm',
                [('idea', 'Ramę tworzą dwa pionowe boki, bok dolny oraz półokrąg o długości $\\pi r$.'), ('compute', '2 · @{h} + @{w} + 3,14 · @{w // 2} = @{2 * h + w + 314 / 100 * (w // 2)|dec}')]),
       decimal('Ile metrów kwadratowych szkła potrzeba na całe okno? (1 m² = 100 dm²)', '(w * h + 314 / 100 * (w // 2) * (w // 2) / 2) / 100',
               [('idea', 'Zamień pole z dm² na m², dzieląc przez 100.'), ('conclude', 'Odpowiedź: @{(w * h + 314 / 100 * (w // 2) * (w // 2) / 2) / 100|dec} m².')])],
      [('w', '2 * randint(10, 20)'), ('h', 'randint(10, 30)')],
      outro='Okno opisane: znasz jego pole, długość ramy i zapotrzebowanie na szkło.',
      media=[fig('arch', 'Okno: prostokąt z półkolem na górze.', w=E('w'), h=E('h'), labels={'w': E("str(w) + ' dm'"), 'h': E("str(h) + ' dm'"), 'r': 'r'})],
      constraints=['h != w'], objectives=['VII-VIII.3.7', 'VII-VIII.3.8', 'VII-VIII.3.9'], area='VII-VIII.3', prereq=['vh-circle-calc', 'vh-area-decompose'],
      desc='Doświadczenie: opis elementu architektury z obliczeniami pola i długości.')

# ============================================================================ VII-VIII, experience 1: comparing financial products
quest('q78-deposit', S78, 'Misja: która lokata jest lepsza?', 1,
      "Pani Ewa chce założyć na rok lokatę na kwotę @{K} zł. Bank A oferuje oprocentowanie roczne 3%. Bank B oferuje 2,5% oraz jednorazową premię @{bonus} zł. Odsetki są doliczane po roku. Porównaj oferty i doradź pani Ewie.",
      [quantity('Ile złotych odsetek da lokata w banku A po roku?', 'K * 3 / 100', 'zł',
                [('idea', '3% z kwoty lokaty: podziel kwotę przez 100 i pomnóż przez 3.'), ('compute', '@{K} : 100 · 3 = @{K * 3 / 100|dec}')]),
       quantity('Ile złotych zyska pani Ewa w banku B (odsetki i premia)?', 'K * 25 / 1000 + bonus', 'zł',
                [('idea', 'Odsetki to 2,5% kwoty, do tego dochodzi premia.'), ('compute', '@{K * 25 / 1000|dec} + @{bonus} = @{K * 25 / 1000 + bonus|dec}')]),
       quantity('O ile złotych zysk w korzystniejszym banku jest większy?', 'abs(K * 3 / 100 - (K * 25 / 1000 + bonus))', 'zł',
                [('idea', 'Odejmij mniejszy zysk od większego.'), ('conclude', 'Różnica: @{abs(K * 3 / 100 - (K * 25 / 1000 + bonus))|dec} zł.')]),
       choice_text('Którą lokatę powinna wybrać pani Ewa, jeśli zależy jej na największym zysku po roku?', [('Lokatę z banku A', 'K * 3 / 100 > K * 25 / 1000 + bonus'), ('Lokatę z banku B', 'K * 25 / 1000 + bonus > K * 3 / 100')], None,
                   [('idea', 'Wybierz ofertę z większym zyskiem.'), ('conclude', "@{('Bank A: ' if K * 3 / 100 > K * 25 / 1000 + bonus else 'Bank B: ')}@{max(K * 3 / 100, K * 25 / 1000 + bonus)|dec} zł.")], fixed_order=True),
       quantity('Ile złotych będzie miała pani Ewa na koniec roku w korzystniejszym banku (kapitał i zysk)?', 'K + max(K * 3 / 100, K * 25 / 1000 + bonus)', 'zł',
                [('idea', 'Dodaj do kwoty lokaty większy zysk.'), ('conclude', 'Odpowiedź: @{K + max(K * 3 / 100, K * 25 / 1000 + bonus)|dec} zł.')]),
       quantity('Przy jakiej kwocie lokaty oba banki dałyby dokładnie taki sam zysk?', 'bonus * 200', 'zł',
                [('idea', 'Różnica oprocentowania to 3% − 2,5% = 0,5%. Premia musi być równa 0,5% kwoty, czyli kwota to premia : 0,005.'), ('compute', '@{bonus} : 0,005 = @{bonus * 200}')])],
      [('K', '200 * randint(5, 45)'), ('bonus', '10 * randint(1, 6)')],
      outro='Pani Ewa zna już zyski z obu lokat i wie, od jakiej kwoty bank A staje się korzystniejszy.',
      media=[table('Tabela: oferty banków.', ['Bank', 'Oprocentowanie roczne', 'Premia'], E("[['A', '3%', 'brak'], ['B', '2,5%', str(bonus) + ' zł']]"))],
      constraints=['K != bonus * 200'], objectives=['VII-VIII.1.9', 'VII-VIII.4.4'], area='VII-VIII.1', prereq=['vh-interest'], tags=('finance', 'thinking'),
      desc='Doświadczenie: porównanie ofert finansowych z użyciem obliczeń.')

# ============================================================================ VII-VIII, experience 2: a simple strategy game
quest('q78-nim', S78, 'Misja: gra w patyczki', 2,
      "Dwoje graczy na zmianę zabiera z kupki od 1 do 3 patyczków. Wygrywa ten, kto zabierze ostatni patyczek. Na początku w kupce jest @{pln(N, ['patyczek', 'patyczki', 'patyczków'])} i zaczynasz Ty. Znajdź strategię wygrywającą.",
      [number('Ile patyczków powinieneś zabrać w pierwszym ruchu, aby zostawić liczbę podzielną przez 4?', 'N % 4',
              [('idea', 'Dobra pozycja to taka, w której po Twoim ruchu zostaje liczba patyczków podzielna przez 4. Oblicz resztę z dzielenia @{N} przez 4.'), ('compute', '@{N} : 4 daje resztę @{N % 4}')]),
       number('Ile patyczków zostanie po Twoim pierwszym ruchu?', 'N - N % 4',
              [('idea', 'Od liczby początkowej odejmij zabrane patyczki.'), ('compute', '@{N} − @{N % 4} = @{N - N % 4}')]),
       number("Przeciwnik zabiera @{pln(rr, ['patyczek', 'patyczki', 'patyczków'])}. Ile patyczków powinieneś zabrać teraz, aby znów zostawić liczbę podzielną przez 4?", '4 - rr',
              [('idea', 'Razem Wasze dwa ruchy mają zabrać 4 patyczki.'), ('compute', '4 − @{rr} = @{4 - rr}')]),
       number('Ile patyczków zostanie po tym ruchu?', 'N - N % 4 - 4',
              [('idea', 'Po Waszej parze ruchów zniknęły 4 patyczki.'), ('compute', '@{N - N % 4} − 4 = @{N - N % 4 - 4}')]),
       choice_text("Gdyby na początku w kupce było @{pln(N + 4 - N % 4, ['patyczek', 'patyczki', 'patyczków'])} (liczba podzielna przez 4) i zaczynałbyś Ty, kto miałby strategię wygrywającą?",
                   [('Ty (zaczynający)', 'false'), ('Przeciwnik', 'true')], None,
                   [('idea', 'Jeśli liczba patyczków jest podzielna przez 4, każdy Twój ruch przeciwnik uzupełnia do 4.'), ('conclude', 'Strategię wygrywającą ma przeciwnik.')], fixed_order=True)],
      [('N', 'randint(9, 30)'), ('rr', 'randint(1, 3)')],
      outro='Gra rozgryziona: celem jest zawsze zostawić przeciwnikowi liczbę patyczków podzielną przez 4.',
      constraints=['N % 4 != 0'], objectives=['VII-VIII.5.1', 'VII-VIII.5.3'], area='VII-VIII.5', prereq=['vh-think-structure'],
      desc='Doświadczenie: analiza prostej gry strategicznej i strategii wygrywającej.')

# ============================================================================ VII-VIII, experience 3: how presentation influences the interpretation of data
quest('q78-chart', S78, 'Misja: ten sam wykres, dwie historie', 3,
      "Sklep prezentuje sprzedaż w czterech miesiącach (w tys. zł) na dwóch wykresach. Wykres A ma oś zaczynającą się od zera, a wykres B – od @{ymin}. Sprawdź, jak sposób prezentacji wpływa na wrażenie.",
      [number('Ile wynosi sprzedaż w kwietniu (w tys. zł)?', 'apr',
              [('idea', 'Odczytaj ostatni słupek na osi pionowej.'), ('conclude', 'Odpowiedź: @{apr}.')]),
       number('O ile procent wzrosła sprzedaż od stycznia do kwietnia?', 'pct',
              [('idea', 'Różnicę (kwiecień − styczeń) podziel przez wartość styczniową i zamień na procent.'), ('compute', '(@{apr} − @{jan}) : @{jan} = @{pct}%')]),
       number('Na wykresie B słupek kwietniowy jest wyższy od styczniowego (licząc wysokości słupków od początku osi, czyli od @{ymin}) o ile procent?', 'vis',
              [('idea', 'Wysokość słupka na wykresie B to wartość minus @{ymin}. Porównaj wysokości: @{jan - ymin} i @{apr - ymin}.'), ('compute', '(@{apr - ymin} − @{jan - ymin}) : @{jan - ymin} = @{vis}%')]),
       choice_text('Który wykres może wprowadzać odbiorców w błąd co do skali wzrostu?', [('Wykres A (oś od zera)', 'false'), ('Wykres B (oś ucięta)', 'true'), ('Żaden z nich', 'false')], None,
                   [('idea', 'Ucięta oś powiększa wizualnie różnice między słupkami.'), ('conclude', 'Wykres B wygląda na dużo większy wzrost, niż wynika z danych.')], fixed_order=True),
       choice('Które zdanie jest rzetelnym wnioskiem z danych?', 'g1', ['g2', 'g3', 'g4'],
              [('idea', 'Rzetelny wniosek opiera się na liczbach, a nie na wrażeniu z wykresu.'), ('conclude', '@{g1}')])],
      [('pct', '5 * randint(1, 6)'), ('jan', '20 * randint(5, 25)'), ('d2', 'jan * pct // 100'), ('apr', 'jan + d2'),
       ('dd', 'choice([10, 20, 25, 50])'), ('ymin', 'jan - dd'), ('mids', 'sorted([jan + randint(0, d2), jan + randint(0, d2)])'),
       ('vals', '[jan, mids[0], mids[1], apr]'), ('vis', 'd2 * 100 // dd'),
       ('g1', "'Sprzedaż w kwietniu była o ' + str(pct) + '% większa niż w styczniu.'"),
       ('g2', "'Sprzedaż w kwietniu była ' + str(vis) + ' razy większa niż w styczniu.'"),
       ('g3', "'Sprzedaż wzrosła o ' + str(vis) + '%.'"),
       ('g4', "'Sprzedaż prawie się podwoiła.'")],
      outro='Już wiesz: ten sam zestaw danych można pokazać tak, by wzrost wyglądał na mały lub ogromny. Zawsze sprawdzaj oś wykresu!',
      media=[{'type': 'chart', 'kind': 'bar', 'essential': True, 'alt': 'Wykres A: sprzedaż w miesiącach, oś od zera.',
              'params': {'title': 'Wykres A', 'labels': ['sty', 'lut', 'mar', 'kwi'], 'values': E('vals')}},
             {'type': 'chart', 'kind': 'bar', 'essential': True, 'alt': 'Wykres B: te same dane, oś zaczyna się od wartości większej od zera.',
              'params': {'title': 'Wykres B', 'labels': ['sty', 'lut', 'mar', 'kwi'], 'values': E('vals'), 'yMin': E('ymin')}}],
      constraints=['(d2 * 100) % dd == 0', 'd2 >= 5', 'vis != pct', 'vis < 600', 'g2 != g3'], objectives=['VII-VIII.4.2', 'VII-VIII.4.5'], area='VII-VIII.4', prereq=['vh-data-critical'],
      desc='Doświadczenie: wpływ sposobu przedstawiania danych na ich interpretację.')

# ============================================================================ VII-VIII, experience 4: an everyday interdisciplinary problem
quest('q78-ramp', S78, 'Misja: rampa dla rowerów', 4,
      "W parku powstaje rampa dla rowerów. Jej bok ma kształt trójkąta prostokątnego: rampa wznosi się na wysokość @{hh} dm na poziomej odległości @{dd} dm. Szerokość rampy to @{ww} dm. Oblicz, ile materiałów potrzeba.",
      [quantity('Jaką długość ma powierzchnia rampy (przeciwprostokątna trójkąta)?', 'ls', 'dm',
                [('idea', 'Z twierdzenia Pitagorasa: $c^2 = a^2 + b^2$.'), ('compute', '@{hh}² + @{dd}² = @{hh * hh + dd * dd} = @{ls}²')]),
       quantity('Jakie pole ma prostokątna powierzchnia, po której jadą rowery?', 'ls * ww', 'dm²',
                [('idea', 'Pole prostokąta o bokach: długość rampy i jej szerokość.'), ('compute', '@{ls} · @{ww} = @{ls * ww}')]),
       quantity('Jakie pole ma jedna boczna ściana rampy (trójkąt prostokątny)?', 'hh * dd / 2', 'dm²',
                [('idea', 'Pole trójkąta prostokątnego = połowa iloczynu przyprostokątnych.'), ('compute', '@{hh} · @{dd} : 2 = @{hh * dd / 2|dec}')]),
       quantity('Jakie pole mają razem obie boczne ściany i powierzchnia rampy (powierzchnia do pomalowania)?', 'ls * ww + hh * dd', 'dm²',
                [('idea', 'Dodaj pole powierzchni rampy i dwóch trójkątnych ścian bocznych.'), ('compute', '@{ls * ww} + 2 · @{hh * dd / 2|dec} = @{ls * ww + hh * dd}')]),
       number('Jeden litr farby wystarcza na @{cov} dm². Ile litrów (w pełnych litrach) trzeba kupić?', 'ceil((ls * ww + hh * dd) / cov)',
              [('idea', 'Podziel pole do pomalowania przez wydajność farby i zaokrąglij w górę.'), ('compute', '@{ls * ww + hh * dd} : @{cov} ≈ @{(ls * ww + hh * dd) / cov|dec}')]),
       choice_text('Czy trójkąt o bokach @{hh} dm, @{dd} dm i @{ls} dm jest prostokątny?', [('Tak', 'hh * hh + dd * dd == ls * ls'), ('Nie', 'hh * hh + dd * dd != ls * ls')], None,
                   [('idea', 'Sprawdź twierdzenie odwrotne do twierdzenia Pitagorasa.'), ('conclude', '@{hh}² + @{dd}² = @{hh * hh + dd * dd} = @{ls}², więc trójkąt jest prostokątny.')], fixed_order=True)],
      [('tr', 'choice([[5, 12, 13], [8, 15, 17], [7, 24, 25], [3, 4, 5]])'), ('k', 'randint(1, 4)'), ('hh', 'tr[0] * k'), ('dd', 'tr[1] * k'), ('ls', 'tr[2] * k'),
       ('ww', 'randint(8, 15)'), ('cov', 'choice([40, 50, 80, 100])')],
      outro='Rampa zaplanowana: znasz jej długość, powierzchnię do pomalowania i potrzebną ilość farby.',
      media=[fig('right-triangle', 'Boczna ściana rampy: trójkąt prostokątny z zaznaczoną wysokością i odległością poziomą.', a=E('dd'), b=E('hh'),
                 labels={'a': E("str(dd) + ' dm'"), 'b': E("str(hh) + ' dm'"), 'c': '?'})],
      selfCheck=['hh * hh + dd * dd == ls * ls'], objectives=['VII-VIII.3.4', 'VII-VIII.3.9'], area='VII-VIII.3', prereq=['vh-pyth-basic', 'vh-pyth-context'],
      desc='Doświadczenie: problem z życia wymagający twierdzenia Pitagorasa, pól i szacowania zużycia materiałów.')

# ============================================================================ path: the quests close each stage
un = Unit(S46, 'n46-uQ', 'Misje', 'Dłuższe zadania z życia: dane, budżet, plan i ogródek.', 'quest', area=None)
un.quest('q46-water').quest('q46-trip').quest('q46-plan').quest('q46-garden')

un = Unit(S78, 'vh-uQ', 'Misje', 'Dłuższe zadania z życia: architektura, finanse, strategia, dane i rampa.', 'quest', area=None)
un.quest('q78-arch').quest('q78-deposit').quest('q78-nim').quest('q78-chart').quest('q78-ramp')
