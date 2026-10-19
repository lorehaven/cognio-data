"""Stage IV-VI, area 2 (Miary): units, time, calendar, scale, speed, reading instruments.
Objectives: IV-VI.2.1-2.12.  Unit conversions are built by a factory so every pair of units is covered uniformly."""
from dsl import *

S = 'IV-VI'
A2 = 'IV-VI.2'


def conv_skill(id, title, objectives, names, factors, levels, intro, prereq=()):
    """Unit conversion. names: display units; factors: DSL numbers in a common base unit.
    levels: [(label, pairs[[from, to], ...], lo, hi, decimals)]"""
    lv = [lvl(label, pairs=str(pairs), lo=lo, hi=hi, dec=dec) for label, pairs, lo, hi, dec in levels]
    skill(id, S, title, objectives, lv,
          [('N', str(names)), ('F', '[' + ', '.join(factors) + ']'), ('pair', 'choice(pairs)'), ('i', 'pair[0]'), ('j', 'pair[1]'),
           ('x', 'randint(lo, hi) / pow(10, dec)'), ('v', 'x * F[i] / F[j]'), ('ratio', 'F[i] / F[j]')],
          quantity('Zamień @{x|dec} @{N[i]} na @{N[j]}.', 'v', 'N[j]',
                   [('idea', "@{('W jednym ' + N[i] + ' mieści się ' + fmt(ratio) + ' ' + N[j] + ', więc mnożymy.' if ratio >= 1 else 'W jednym ' + N[j] + ' mieści się ' + fmt(1 / ratio) + ' ' + N[i] + ', więc dzielimy.')}"),
                    ('compute', "@{(fmt(x) + ' · ' + fmt(ratio) + ' = ' + fmt(v) if ratio >= 1 else fmt(x) + ' : ' + fmt(1 / ratio) + ' = ' + fmt(v))}")],
                   unit_expr=True,
                   errors=[('wrong_direction', Qty('x * F[j] / F[i]', 'N[j]', True), 'Sprawdź kierunek: z większej jednostki na mniejszą mnożymy, z mniejszej na większą dzielimy.', 'x * F[j] / F[i] != v and denom(x * F[j] / F[i]) in divisors(100000)')]),
          constraints=['denom(v) in divisors(10000)', 'v != x', 'x > 0'], selfCheck=['v * F[j] == x * F[i]'], min_distinct=30,
          area=A2, intro=intro, prereq=list(prereq), tags=('no-calculator',))


# ============================================================================ jednostki długości, masy, pojemności, pola
conv_skill('n46-len-units', 'Jednostki długości', ['IV-VI.2.2', 'IV-VI.2.1'],
           ['mm', 'cm', 'dm', 'm', 'km'], ['1', '10', '100', '1000', '1000000'],
           [('m i cm, cm i mm', [[3, 1], [1, 3], [1, 0], [0, 1]], 2, 90, 0),
            ('km i m, dm', [[4, 3], [3, 4], [3, 2], [2, 3]], 2, 90, 0),
            ('Ułamki dziesiętne', [[3, 1], [1, 3], [4, 3], [3, 4], [1, 0], [0, 1], [3, 2], [2, 3]], 11, 999, 1)],
           'Jednostki długości: 1 km = 1000 m, 1 m = 10 dm = 100 cm = 1000 mm, 1 dm = 10 cm, 1 cm = 10 mm. Z większej jednostki na mniejszą mnożymy, z mniejszej na większą dzielimy.')

conv_skill('n46-mass-units', 'Jednostki masy', ['IV-VI.2.7'],
           ['g', 'dag', 'kg', 't'], ['1', '10', '1000', '1000000'],
           [('kg i g', [[2, 0], [0, 2]], 2, 90, 0), ('dag i tony', [[2, 1], [1, 2], [3, 2], [2, 3]], 2, 90, 0),
            ('Ułamki dziesiętne', [[2, 0], [0, 2], [2, 1], [1, 2], [3, 2], [2, 3]], 11, 999, 1)],
           'Jednostki masy: 1 kg = 100 dag = 1000 g, 1 dag = 10 g, 1 t = 1000 kg.')

conv_skill('n46-capacity-units', 'Jednostki objętości i pojemności', ['IV-VI.2.5', 'IV-VI.2.6'],
           ['ml', 'l', 'cm³', 'dm³', 'm³'], ['1', '1000', '1', '1000', '1000000'],
           [('l i ml', [[1, 0], [0, 1]], 2, 90, 0), ('Litry, dm³ i cm³', [[1, 3], [3, 1], [0, 2], [2, 0], [3, 2], [2, 3]], 2, 90, 0),
            ('m³ i dm³', [[4, 3], [3, 4], [4, 1], [1, 4]], 2, 90, 1)],
           'Pojemność i objętość: 1 l = 1000 ml = 1 dm³, 1 ml = 1 cm³, 1 m³ = 1000 dm³ = 1000 l.', prereq=['n46-len-units'])

conv_skill('n46-area-units', 'Jednostki pola', ['IV-VI.2.4', 'IV-VI.2.6'],
           ['mm²', 'cm²', 'dm²', 'm²', 'a', 'ha', 'km²'], ['1 / 1000000', '1 / 10000', '1 / 100', '1', '100', '10000', '1000000'],
           [('cm² i dm², m²', [[1, 2], [2, 1], [2, 3], [3, 2]], 2, 90, 0), ('a, ha i m²', [[4, 3], [3, 4], [5, 3], [3, 5], [5, 4], [4, 5]], 2, 90, 0),
            ('km², ha, mm²', [[6, 5], [5, 6], [1, 0], [0, 1], [3, 1], [1, 3]], 2, 90, 0)],
           'Jednostki pola: 1 m² = 100 dm² = 10 000 cm², 1 a = 100 m², 1 ha = 100 a = 10 000 m², 1 km² = 100 ha. Przeliczając pola, mnożymy lub dzielimy przez 100, 10 000…', prereq=['n46-len-units'])

# czas: godziny, minuty, sekundy
skill('n46-time-units', S, 'Jednostki czasu', ['IV-VI.2.9'],
      [lvl('Na mniejsze jednostki', ms='[0, 2]'), lvl('Na większe jednostki', ms='[1, 3]'), lvl('Wszystkie przeliczenia', ms='[0, 1, 2, 3]')],
      [('md', 'choice(ms)'),
       ('x', '[randint(2, 12), 15 * randint(2, 24), randint(2, 30), 15 * randint(2, 40)][md]'),
       ('names', "[['h', 'min'], ['min', 'h'], ['min', 's'], ['s', 'min']]"),
       ('v', '[x * 60, x / 60, x * 60, x / 60][md]'), ('from_u', 'names[md][0]'), ('to_u', 'names[md][1]')],
      quantity('Zamień @{x|dec} @{from_u} na @{to_u}.', 'v', 'to_u',
               [('idea', '1 h = 60 min, 1 min = 60 s. Na mniejszą jednostkę mnożymy przez 60, na większą dzielimy przez 60.'),
                ('compute', "@{(fmt(x) + ' · 60 = ' + fmt(v) if md == 0 or md == 2 else fmt(x) + ' : 60 = ' + fmt(v))}")], unit_expr=True,
               errors=[('wrong_direction', Qty('x / 60 if md == 0 or md == 2 else x * 60', 'to_u', True), 'Sprawdź kierunek: na mniejszą jednostkę mnożymy, na większą dzielimy.',
                        'denom(x / 60 if md == 0 or md == 2 else x * 60) in divisors(1000)')]),
      constraints=['denom(v) in divisors(100)'], selfCheck=['md in [1, 3] or v / 60 == x'], min_distinct=30, area=A2,
      intro='Czas: 1 godzina = 60 minut, 1 minuta = 60 sekund, 1 godzina = 3600 sekund. Pół godziny to 30 minut, kwadrans to 15 minut.')

# ============================================================================ zegar i kalendarz
skill('n46-clock-end', S, 'O której godzinie?', ['IV-VI.2.9'],
      [lvl('W obrębie godziny', dmax=55, hmax=0), lvl('Przez pełną godzinę', dmax=180, hmax=0), lvl('Godziny i minuty', dmax=420, hmax=1)],
      [('start', 'randint(60, 1200) // 5 * 5'), ('dur', 'randint(10, dmax) // 5 * 5'), ('end', 'start + dur'),
       ('c', "choice([['Film zaczyna się o ', ' i trwa ', 'O której się skończy?'], ['Pociąg odjeżdża o ', ', a podróż trwa ', 'O której pociąg dojedzie na miejsce?'], ['Mecz rozpoczyna się o ', ' i trwa ', 'O której się zakończy?']])"),
       ('dtxt', "(str(dur // 60) + ' h ' + str(dur % 60) + ' min') if hmax == 1 and dur >= 60 and dur % 60 != 0 else (str(dur) + ' min')")],
      task('time-input', '@{c[0]}@{hhmm(start)}@{c[1]}@{dtxt}. @{c[2]}', Time('hhmm(end)'),
           [('idea', 'Dodaj czas trwania do godziny rozpoczęcia. Pamiętaj, że 60 minut to 1 godzina.'),
            ('compute', '@{hhmm(start)} + @{dur} min = @{hhmm(end)}')],
           errors=[('decimal_minutes', Time('hhmm(start + dur // 60 * 100 + dur % 60)'), 'Godzina ma 60 minut, a nie 100.', 'dur >= 60 and start + dur // 60 * 100 + dur % 60 < 1440')]),
      constraints=['dur >= 10', 'hmax == 0 or dur >= 60', 'dmax >= 100 or (start % 60) + dur < 60', 'dmax != 180 or (start % 60) + dur >= 60', 'end < 1440'], selfCheck=['end - start == dur'], min_distinct=40, area=A2, prereq=['n46-time-units'])

skill('n46-clock-start', S, 'Kiedy wyjść z domu?', ['IV-VI.2.9'],
      [lvl('Krótkie podróże', dmax=55), lvl('Dłuższe podróże', dmax=240)],
      [('arrive', 'randint(480, 1260) // 5 * 5'), ('dur', 'randint(10, dmax) // 5 * 5'), ('leave', 'arrive - dur'),
       ('c', "choice(['Musimy być na dworcu o ', 'Zajęcia zaczynają się o ', 'Wizyta u lekarza jest o '])")],
      task('time-input', '@{c}@{hhmm(arrive)}. Droga zajmuje @{dur} min. O której najpóźniej trzeba wyjść z domu?', Time('hhmm(leave)'),
           [('idea', 'Odejmij czas drogi od godziny przyjazdu.'), ('compute', '@{hhmm(arrive)} − @{dur} min = @{hhmm(leave)}')]),
      constraints=['dur >= 10'], selfCheck=['leave + dur == arrive'], min_distinct=40, area=A2, prereq=['n46-clock-end'])

skill('n46-clock-duration', S, 'Ile to trwało?', ['IV-VI.2.9'],
      [lvl('W obrębie godziny', dmax=55), lvl('Przez pełną godzinę', dmax=180), lvl('Kilka godzin', dmax=420)],
      [('start', 'randint(360, 1100) // 5 * 5'), ('dur', 'randint(10, dmax) // 5 * 5'), ('end', 'start + dur'),
       ('c', "choice([['Lekcja rozpoczęła się o ', ' i skończyła o ', 'Ile minut trwała lekcja?'], ['Wycieczka wyruszyła o ', ', a wróciła o ', 'Ile minut trwała wycieczka?'], ['Turniej zaczął się o ', ' i zakończył o ', 'Ile minut trwał turniej?']])")],
      number('@{c[0]}@{hhmm(start)}@{c[1]}@{hhmm(end)}. @{c[2]}', 'dur',
             [('idea', 'Policz, ile minut mija od jednej godziny do drugiej: najpierw do pełnej godziny, potem dalej.'),
              ('compute', 'Od @{hhmm(start)} do @{hhmm(end)} jest @{dur} min (@{dur // 60} h @{dur % 60} min).')],
             errors=[('subtract_clock', Int('abs(end // 60 * 100 + end % 60 - (start // 60 * 100 + start % 60))'), 'Godzina ma 60 minut – nie odejmuj godzin jak zwykłych liczb.', 'start // 60 != end // 60')]),
      constraints=['dur >= 10', 'dmax > 55 or (start % 60) + dur < 60'], min_distinct=40, area=A2, prereq=['n46-time-units'])

skill('n46-calendar-weeks', S, 'Dni, tygodnie i miesiące', ['IV-VI.2.8'],
      [lvl('Tygodnie i dni', mode=0), lvl('Dni na tygodnie', mode=1), lvl('Lata i miesiące', mode=2)],
      [('w', 'randint(2, 12)'), ('d', 'randint(1, 6)'), ('total', 'randint(15, 200)'), ('y', 'randint(1, 12)'), ('mo', 'randint(1, 11)'),
       ('txt', "('Wakacje trwają ' + pln(w, ['tydzień', 'tygodnie', 'tygodni']) + ' i ' + pln(d, ['dzień', 'dni', 'dni']) + '. Ile dni trwają wakacje?') if mode == 0 else "
               "(('Ile pełnych tygodni mieści się w ' + pln(total, ['dniu', 'dniach', 'dniach']) + '?') if mode == 1 else "
               "('Kuba ma ' + pln(y, ['rok', 'lata', 'lat']) + ' i ' + pln(mo, ['miesiąc', 'miesiące', 'miesięcy']) + '. Ile to miesięcy?'))"),
       ('ans', 'w * 7 + d if mode == 0 else (total // 7 if mode == 1 else y * 12 + mo)')],
      number('@{txt}', 'ans',
             [('idea', "@{('Tydzień ma 7 dni.' if mode < 2 else 'Rok ma 12 miesięcy.')}"), ('compute', "@{(str(w) + ' · 7 + ' + str(d) + ' = ' + str(ans) if mode == 0 else (str(total) + ' : 7 = ' + str(total // 7) + ' r ' + str(total % 7) if mode == 1 else str(y) + ' · 12 + ' + str(mo) + ' = ' + str(ans)))}")]),
      constraints=['mode != 1 or total % 7 != 0'], min_distinct=40, area=A2)

skill('n46-calendar-weekday', S, 'Jaki to będzie dzień tygodnia?', ['IV-VI.2.8'],
      [lvl('Za kilka dni', dmax=20), lvl('Za wiele dni', dmax=200)],
      [('days', "['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela']"), ('t', 'randint(0, 6)'),
       ('n', 'randint(8, dmax)'), ('r', '(t + n) % 7')],
      choice('Dziś jest @{days[t]}. Jaki dzień tygodnia będzie za @{n|pl:[\'dzień\', \'dni\', \'dni\']}?', 'days[r]',
             ['days[(r + 1) % 7]', 'days[(r + 2) % 7]', 'days[(r + 6) % 7]'],
             [('idea', 'Dni tygodnia powtarzają się co 7. Policz resztę z dzielenia liczby dni przez 7.'),
              ('compute', '@{n} : 7 daje resztę @{n % 7}, więc przesuwamy się o @{n % 7|pl:[\'dzień\', \'dni\', \'dni\']} od dnia „@{days[t]}”.')]),
      constraints=['n % 7 != 0'], min_distinct=40, area=A2, prereq=['n46-calendar-weeks'])

# ============================================================================ zapis dwumianowany i dziesiętny (2.10)
skill('n46-compound-to-decimal', S, 'Wyrażenia dwumianowane na ułamki dziesiętne', ['IV-VI.2.10'],
      [lvl('Metry i centymetry, złote i grosze', ps="[['m', 'cm', 100], ['zł', 'gr', 100]]"),
       lvl('Kilogramy i dekagramy, grami', ps="[['kg', 'dag', 100], ['kg', 'g', 1000]]"),
       lvl('Kilometry, litry, tony', ps="[['km', 'm', 1000], ['l', 'ml', 1000], ['t', 'kg', 1000]]")],
      [('pp', 'choice(ps)'), ('big', 'pp[0]'), ('small', 'pp[1]'), ('r', 'pp[2]'), ('a', 'randint(1, 20)'), ('b', 'randint(1, r - 1)'), ('x', 'a + b / r')],
      decimal('Uzupełnij: @{a} @{big} @{b} @{small} = ? @{big}', 'x',
              [('idea', '1 @{small} to $\\frac{1}{@{r}}$ @{big}, więc @{b} @{small} to @{b / r|dec} @{big}.'), ('compute', '@{a} + @{b / r|dec} = @{x|dec}')],
              errors=[('wrong_places', Dec('a + b / (r * 10)'), 'Sprawdź, ile jednostek mniejszych mieści się w większej: 100 – dwa miejsca po przecinku, 1000 – trzy.')]),
      selfCheck=['(x - a) * r == b'], min_distinct=40, area=A2, prereq=['n46-dec-to-fraction'])

skill('n46-decimal-to-compound', S, 'Ułamki dziesiętne na wyrażenia dwumianowane', ['IV-VI.2.10'],
      [lvl('Metry i centymetry, złote i grosze', ps="[['m', 'cm', 100], ['zł', 'gr', 100]]"),
       lvl('Kilogramy, kilometry, litry', ps="[['kg', 'dag', 100], ['kg', 'g', 1000], ['km', 'm', 1000], ['l', 'ml', 1000]]")],
      [('pp', 'choice(ps)'), ('big', 'pp[0]'), ('small', 'pp[1]'), ('r', 'pp[2]'), ('a', 'randint(1, 20)'), ('b', 'randint(1, r - 1)'), ('x', 'a + b / r')],
      number('Uzupełnij: @{x|dec} @{big} = @{a} @{big} ? @{small}', 'b',
             [('idea', 'Część całkowita to @{a} @{big}. Część po przecinku zamieniamy na @{small}: @{x - a|dec} · @{r} = @{b}.'), ('conclude', '@{x|dec} @{big} = @{a} @{big} @{b} @{small}')]),
      constraints=['b % 10 != 0 or r == 1000'], selfCheck=['(x - a) * r == b'], min_distinct=40, area=A2, prereq=['n46-compound-to-decimal'])

# ============================================================================ skala (2.11)
skill('n46-scale-real', S, 'Skala: odległość w rzeczywistości', ['IV-VI.2.11'],
      [lvl('Plany i modele (skale do 1:1000)', ss='[10, 20, 50, 100, 200, 500, 1000]', un=0), lvl('Mapy (skale od 1:10 000)', ss='[10000, 20000, 25000, 50000, 100000]', un=1)],
      [('sc', 'choice(ss)'), ('cm', 'randint(2, 30)'), ('real', 'cm * sc'),
       ('ans', 'real / 100 if un == 0 else real / 100000'), ('u', "'m' if un == 0 else 'km'")],
      quantity('Skala planu wynosi 1 : @{sc|int}. Odcinek na planie ma długość @{cm} cm. Jaka jest rzeczywista długość tego odcinka w @{(\'metrach\' if un == 0 else \'kilometrach\')}?',
               'ans', 'u',
               [('idea', 'Skala 1 : @{sc|int} oznacza, że 1 cm na planie to @{sc|int} cm w rzeczywistości.'),
                ('compute', "@{cm} · @{sc|int} cm = @{real|int} cm = @{fmt(ans)} @{u}")], unit_expr=True,
               errors=[('wrong_conversion', Qty('real / 10 if un == 0 else real / 1000', 'u', True), 'Sprawdź przeliczenie jednostek: 1 m = 100 cm, 1 km = 100 000 cm.')]),
      constraints=['denom(ans) in divisors(1000)'], selfCheck=['ans * (100 if un == 0 else 100000) == real'], min_distinct=40, area=A2, prereq=['n46-len-units'])

skill('n46-scale-map', S, 'Skala: odległość na mapie', ['IV-VI.2.11'],
      [lvl('Plany i modele', ss='[10, 20, 50, 100, 200, 500, 1000]', un=0), lvl('Mapy', ss='[10000, 20000, 25000, 50000, 100000]', un=1)],
      [('sc', 'choice(ss)'), ('k', 'randint(2, 30)'), ('map_cm', 'k'), ('real', 'map_cm * sc'),
       ('rtxt', "fmt(real / 100) + ' m' if un == 0 else fmt(real / 100000) + ' km'")],
      number('Skala wynosi 1 : @{sc|int}. Rzeczywista odległość to @{rtxt}. Ile centymetrów ma ta odległość na rysunku?', 'map_cm',
             [('idea', 'Zamień rzeczywistą odległość na centymetry i podziel przez @{sc|int}.'), ('compute', '@{real|int} cm : @{sc|int} = @{map_cm} cm')]),
      constraints=['denom(real / 100) in divisors(100)', 'denom(real / 100000) in divisors(1000000)'], min_distinct=40, area=A2, prereq=['n46-scale-real'])

# ============================================================================ prędkość, droga, czas (2.12)
CTX = "choice(['Pociąg', 'Rowerzysta', 'Samochód', 'Autobus'])"
skill('n46-speed-distance', S, 'Droga: s = v · t', ['IV-VI.2.12'],
      [lvl('Pełne godziny', mode=0), lvl('Połowy godziny', mode=1), lvl('Czas w minutach', mode=2)],
      [('who', CTX), ('v', '10 * randint(2, 9)'), ('tm', '30 * randint(1, 8) if mode == 1 else (randint(1, 6) * 60 if mode == 0 else 15 * randint(1, 16))'),
       ('h', 'tm / 60'), ('s', 'v * h'),
       ('ttxt', "(str(tm // 60) + ' h') if tm % 60 == 0 else (str(tm) + ' min')")],
      quantity('@{who} jechał ze stałą prędkością @{v} km/h przez @{ttxt}. Jaką drogę przebył?', 's', 'km',
               [('idea', 'Droga = prędkość · czas. Czas musi być w godzinach, bo prędkość jest w km/h.'), ('compute', '@{tm} min = @{h|dec} h; @{v} · @{h|dec} = @{s|dec} km')],
               errors=[('minutes_as_hours', Qty('v * tm', 'km'), 'Prędkość jest w km/h, więc czas zamień na godziny.', 'mode == 2')]),
      constraints=['denom(s) in divisors(100)', 'tm >= 15'], selfCheck=['s / v * 60 == tm'], min_distinct=15, area=A2, prereq=['n46-time-units'])

skill('n46-speed-velocity', S, 'Prędkość: v = s : t', ['IV-VI.2.12'],
      [lvl('Pełne godziny', mode=0), lvl('Czas w minutach', mode=1)],
      [('who', CTX), ('v', '5 * randint(3, 20)'), ('tm', 'randint(1, 6) * 60 if mode == 0 else 30 * randint(1, 10)'), ('h', 'tm / 60'), ('s', 'v * h'),
       ('ttxt', "(str(tm // 60) + ' h') if tm % 60 == 0 else (str(tm) + ' min')")],
      quantity('@{who} przebył @{s|dec} km w czasie @{ttxt}. Jaka była jego średnia prędkość w km/h?', 'v', 'km/h',
               [('idea', 'Prędkość = droga : czas (w godzinach).'), ('compute', '@{s|dec} : @{h|dec} = @{v}')],
               errors=[('multiply', Qty('s * h', 'km/h'), 'Prędkość to droga podzielona przez czas, a nie pomnożona.', 's * h != v')]),
      constraints=['denom(s) in divisors(100)'], selfCheck=['v * h == s'], min_distinct=15, area=A2, prereq=['n46-speed-distance'])

skill('n46-speed-time', S, 'Czas: t = s : v', ['IV-VI.2.12'],
      [lvl('Wynik w godzinach', un=0), lvl('Wynik w minutach', un=1)],
      [('who', CTX), ('v', '10 * randint(2, 12)'), ('hh', 'randint(1, 8) if un == 0 else 15 * randint(1, 12) / 60'), ('s', 'v * hh'),
       ('ans', 'hh if un == 0 else hh * 60'), ('u', "'h' if un == 0 else 'min'")],
      quantity('@{who} jedzie ze stałą prędkością @{v} km/h. Ile czasu zajmie mu przejechanie @{s|dec} km? Podaj wynik w @{(\'godzinach\' if un == 0 else \'minutach\')}.', 'ans', 'u',
               [('idea', 'Czas = droga : prędkość.'), ('compute', "@{s|dec} : @{v} = @{hh|dec} h@{(' = ' + fmt(hh * 60) + ' min' if un == 1 else '')}")], unit_expr=True),
      constraints=['denom(s) in divisors(100)'], selfCheck=['v * hh == s'], min_distinct=15, area=A2, prereq=['n46-speed-distance'])

skill('n46-speed-units', S, 'm/s i km/h', ['IV-VI.2.12'],
      [lvl('Z m/s na km/h', rev=0), lvl('Z km/h na m/s', rev=1)],
      [('ms', 'randint(2, 30)'), ('kmh', 'ms * 36 / 10'), ('k9', '9 * randint(1, 16)'), ('ms2', 'k9 * 10 / 36'),
       ('ans', 'kmh if rev == 0 else ms2'), ('u', "'km/h' if rev == 0 else 'm/s'")],
      quantity('@{(fmt(ms) + \' m/s\' if rev == 0 else fmt(k9) + \' km/h\')} to ile @{(\'km/h\' if rev == 0 else \'m/s\')}?', 'ans', 'u',
               [('idea', '1 m/s = 3,6 km/h. W ciągu godziny (3600 s) przejeżdżamy 3600 razy więcej metrów, a 1 km to 1000 m.'),
                ('compute', "@{(fmt(ms) + ' · 3,6 = ' + fmt(kmh) if rev == 0 else fmt(k9) + ' : 3,6 = ' + fmt(ms2))}")], unit_expr=True),
      constraints=['denom(ans) in divisors(100)'], min_distinct=15, area=A2, prereq=['n46-speed-distance'])

# ============================================================================ szacowanie i wybór jednostki (2.1, 2.7)
UNIT_FACTS = ("[['Długość ołówka to około 17', 'cm', ['m', 'km', 'mm']], ['Wysokość drzwi to około 2', 'm', ['cm', 'km', 'mm']], "
              "['Odległość z Warszawy do Gdańska to około 340', 'km', ['m', 'cm', 'mm']], ['Grubość monety to około 2', 'mm', ['m', 'km', 'dm']], "
              "['Długość boiska piłkarskiego to około 100', 'm', ['cm', 'km', 'mm']], ['Masa dorosłego człowieka to około 70', 'kg', ['g', 't', 'dag']], "
              "['Masa tabliczki czekolady to około 100', 'g', ['kg', 't', 'mm']], ['Masa samochodu osobowego to około 1,5', 't', ['g', 'dag', 'mm']], "
              "['Pojemność szklanki to około 250', 'ml', ['l', 'm³', 'dm³']], ['Pojemność wanny to około 150', 'l', ['ml', 'm³', 'cm³']], "
              "['Lekcja w szkole trwa 45', 'min', ['s', 'h', 'dni']], ['Wysokość bloku mieszkalnego to około 30', 'm', ['cm', 'km', 'mm']], "
              "['Szerokość kartki A4 to około 21', 'cm', ['mm', 'm', 'km']], ['Prędkość samochodu w mieście to około 50', 'km/h', ['m/s', 'km/s', 'cm/h']]]")
skill('n46-choose-unit', S, 'Jaka jednostka pasuje?', ['IV-VI.2.1', 'IV-VI.2.7', 'IV-VI.6.1.c'],
      [lvl('Wybierz jednostkę')],
      [('f', f'choice({UNIT_FACTS})')],
      choice('@{f[0]} … Którą jednostkę należy wpisać w miejsce kropek?', 'f[1]', ['f[2][0]', 'f[2][1]', 'f[2][2]'],
             [('idea', 'Wyobraź sobie ten przedmiot lub odległość i porównaj z tym, co znasz: kartka ma ok. 30 cm, litr mleka waży ok. 1 kg.'),
              ('conclude', '@{f[0]} @{f[1]}.')]),
      min_distinct=14, area=A2, prereq=['n46-len-units', 'n46-mass-units'])

# ============================================================================ odczyt przyrządów (2.1, 2.3) - rysunki
skill('n46-ruler-read', S, 'Odczytaj długość z linijki', ['IV-VI.2.1'],
      [lvl('Pełne centymetry od zera', mode=0), lvl('Z dokładnością do milimetra', mode=1), lvl('Odcinek nie zaczyna się od zera', mode=2)],
      [('start', 'randint(1, 6) if mode == 2 else 0'), ('mm', 'randint(2, 14) * 10 if mode == 0 else randint(21, 149)'), ('len', 'mm / 10')],
      decimal('Jaką długość ma odcinek zaznaczony na rysunku? Podaj wynik w centymetrach.', 'len',
              [('idea', 'Odczytaj początek i koniec odcinka na linijce, a potem odejmij. Jedna kreska to 1 mm = 0,1 cm.'), ('compute', 'Długość: @{len|dec} cm.')],
              media=[{'type': 'figure', 'kind': 'ruler', 'essential': True, 'alt': 'Linijka z odcinkiem o początku w @{start} cm.',
                      'params': {'startMm': E('start * 10'), 'lengthMm': E('mm'), 'unit': 'cm'}}]),
      constraints=['mode != 2 or start * 10 + mm <= 200'], min_distinct=8, area=A2)

skill('n46-protractor-read', S, 'Odczytaj miarę kąta', ['IV-VI.2.3'],
      [lvl('Pełne dziesiątki stopni', mode=0), lvl('Dowolna liczba stopni', mode=1)],
      [('deg', 'randint(1, 17) * 10 if mode == 0 else randint(5, 175)'), ('flip', 'randint(0, 1)')],
      number('Ile stopni ma kąt narysowany na rysunku?', 'deg',
             [('idea', 'Ustaw środek kątomierza w wierzchołku kąta, a jedno ramię na zerze. Odczytaj wartość tam, gdzie leży drugie ramię (pilnuj właściwej skali).'),
              ('conclude', 'Kąt ma @{deg}°.')],
             media=[{'type': 'figure', 'kind': 'protractor', 'essential': True, 'alt': 'Kąt narysowany obok kątomierza.',
                     'params': {'degrees': E('deg'), 'mirrored': E('flip')}}],
             errors=[('wrong_scale', Int('180 - deg'), 'Kątomierz ma dwie skale. Zacznij od zera na tym ramieniu, które leży na linii podstawy.', 'deg != 90')]),
      min_distinct=17, area=A2)

# ============================================================================ ścieżka
un = Unit(S, 'n46-u17', 'Jednostki miar', 'Długość, masa, pojemność i pole: przeliczamy jednostki.', 'ruler', area=A2)
un.learn('n46-len-units').learn('n46-mass-units').learn('n46-capacity-units').learn('n46-area-units')
un.review('Powtórka: jednostki', ['n46-len-units', 'n46-mass-units', 'n46-capacity-units', 'n46-area-units'])
un.learn('n46-compound-to-decimal').learn('n46-decimal-to-compound').learn('n46-choose-unit')
un.checkpoint(['n46-len-units', 'n46-mass-units', 'n46-capacity-units', 'n46-area-units', 'n46-compound-to-decimal', 'n46-decimal-to-compound'])

un = Unit(S, 'n46-u18', 'Czas i kalendarz', 'Godziny, minuty, dni, tygodnie i miesiące.', 'clock', area=A2)
un.learn('n46-time-units').learn('n46-clock-end').learn('n46-clock-start').learn('n46-clock-duration')
un.learn('n46-calendar-weeks').learn('n46-calendar-weekday')
un.checkpoint(['n46-time-units', 'n46-clock-end', 'n46-clock-start', 'n46-clock-duration', 'n46-calendar-weeks', 'n46-calendar-weekday'])

un = Unit(S, 'n46-u19', 'Skala, prędkość i pomiary', 'Plany i mapy, droga, prędkość, czas oraz odczyty z przyrządów.', 'map', area=A2)
un.learn('n46-scale-real').learn('n46-scale-map').learn('n46-speed-distance').learn('n46-speed-velocity').learn('n46-speed-time').learn('n46-speed-units')
un.learn('n46-ruler-read').learn('n46-protractor-read')
un.checkpoint(['n46-scale-real', 'n46-scale-map', 'n46-speed-distance', 'n46-speed-velocity', 'n46-speed-time', 'n46-speed-units'])
