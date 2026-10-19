"""Stage I-III (edukacja wczesnoszkolna): areas 2 (Miary) and 3 (Figury).  Objectives: I-III.2.a-2.j, I-III.3.a-3.f."""
from dsl import *

S = 'I-III'
A2 = 'I-III.2'
A3 = 'I-III.3'
FIN = ('finance', 'no-calculator')


def conv_i3(id, title, objectives, names, factors, levels, intro):
    """Whole-number unit conversion: levels = [(label, pairs, lo, hi)]."""
    lv = [lvl(label, pairs=str(pairs), lo=lo, hi=hi) for label, pairs, lo, hi in levels]
    skill(id, S, title, objectives, lv,
          [('N', str(names)), ('F', '[' + ', '.join(factors) + ']'), ('pair', 'choice(pairs)'), ('i', 'pair[0]'), ('j', 'pair[1]'),
           ('x', 'randint(lo, hi)'), ('v', 'x * F[i] / F[j]'), ('ratio', 'F[i] / F[j]')],
          quantity('Zamień @{x|int} @{N[i]} na @{N[j]}.', 'v', 'N[j]',
                   [('idea', "@{('W jednym ' + N[i] + ' mieści się ' + fmt(ratio) + ' ' + N[j] + ', więc mnożymy.' if ratio >= 1 else 'W jednym ' + N[j] + ' mieści się ' + fmt(1 / ratio) + ' ' + N[i] + ', więc dzielimy.')}"),
                    ('compute', "@{(fmt(x) + ' · ' + fmt(ratio) + ' = ' + fmt(v) if ratio >= 1 else fmt(x) + ' : ' + fmt(1 / ratio) + ' = ' + fmt(v))}")],
                   unit_expr=True),
          constraints=['denom(v) == 1', 'v != x'], selfCheck=['v * F[j] == x * F[i]'], min_distinct=8, area=A2, intro=intro)


# ============================================================================ pomiary: odczyt (2.a, 2.b)
skill('ew-ruler-read', S, 'Odczytaj długość z linijki', ['I-III.2.a'],
      [lvl('Odcinek od zera', mode=0), lvl('Odcinek nie zaczyna się od zera', mode=1)],
      [('start', 'randint(1, 5) if mode == 1 else 0'), ('len', 'randint(2, 12)')],
      number('Ile centymetrów ma odcinek narysowany obok linijki?', 'len',
             [('idea', 'Odczytaj, gdzie odcinek się zaczyna i gdzie kończy. Policz, ile centymetrów jest pomiędzy.'), ('conclude', 'Odcinek ma @{len} cm.')],
             media=[{'type': 'figure', 'kind': 'ruler', 'essential': True, 'alt': 'Linijka z odcinkiem.', 'params': {'startMm': E('start * 10'), 'lengthMm': E('len * 10'), 'unit': 'cm'}}]),
      min_distinct=10, area=A2)

skill('ew-clock-read', S, 'Która godzina?', ['I-III.2.a'],
      [lvl('Pełne godziny', step=60), lvl('Wpół do, kwadrans', step=15), lvl('Co 5 minut', step=5), lvl('Dowolna minuta', step=1)],
      [('h', 'randint(1, 12)'), ('m', 'randint(0, 59 // step) * step'), ('t', 'h * 60 + m')],
      task('time-input', 'Jaką godzinę pokazuje zegar? Wpisz ją w postaci godzina:minuty.', Time('hhmm(t)'),
           [('idea', 'Krótka wskazówka pokazuje godzinę, a długa – minuty. Długa wskazówka na „12” oznacza pełną godzinę, na „6” – 30 minut.'), ('conclude', 'Zegar pokazuje @{hhmm(t)}.')],
           media=[{'type': 'figure', 'kind': 'clock', 'essential': True, 'alt': 'Tarcza zegara ze wskazówkami.', 'params': {'hour': E('h'), 'minute': E('m')}}]),
      min_distinct=12, area=A2)

skill('ew-thermometer-read', S, 'Odczytaj temperaturę', ['I-III.2.b'],
      [lvl('Temperatura dodatnia', lo=0, hi=30), lvl('Także poniżej zera', lo=-15, hi=30)],
      [('tv', 'randint(lo, hi)')],
      number('Ile stopni Celsjusza pokazuje termometr?', 'tv',
             [('idea', 'Znajdź, gdzie kończy się słupek. Poniżej zera temperatura jest ujemna.'), ('conclude', 'Termometr pokazuje @{tv} °C.')],
             media=[{'type': 'figure', 'kind': 'thermometer', 'essential': True, 'alt': 'Termometr ze słupkiem rtęci.', 'params': {'value': E('tv'), 'min': -20, 'max': 40}}]),
      constraints=['tv != 0'], min_distinct=20, area=A2)

skill('ew-temp-diff', S, 'O ile stopni cieplej, o ile zimniej?', ['I-III.2.b'],
      [lvl('Obie temperatury dodatnie', lo=2, hi=30), lvl('Przez 0 °C', lo=-12, hi=12)],
      [('t1', 'randint(lo, hi)'), ('t2', 'randint(lo, hi)'), ('warmer', 't2 > t1')],
      number('Rano termometr pokazywał @{t1} °C, a w południe @{t2} °C. O ile stopni @{(\'zrobiło się cieplej\' if warmer else \'zrobiło się chłodniej\')}?', 'abs(t2 - t1)',
             [('idea', 'Policz, ile stopni dzieli obie temperatury na termometrze. Gdy przechodzisz przez zero, policz osobno część poniżej i powyżej.'), ('compute', 'Różnica: @{abs(t2 - t1)} °C.')],
             errors=[('forgot_zero', Int('abs(abs(t2) - abs(t1))'), 'Gdy jedna temperatura jest poniżej zera, a druga powyżej, stopnie sumujemy.', 't1 * t2 < 0')]),
      constraints=['t1 != t2', 'lo >= 0 or t1 * t2 < 0 or randint(0, 1) == 0'], min_distinct=30, area=A2, prereq=['ew-thermometer-read'])

UNITS_I3 = ("[['Długość ołówka to około 15', 'cm', ['m', 'km', 'mm']], ['Wysokość drzwi to około 2', 'm', ['cm', 'km', 'mm']], ['Odległość z Warszawy do Krakowa to około 300', 'km', ['m', 'cm', 'mm']], "
            "['Grubość monety to około 2', 'mm', ['m', 'km', 'dm']], ['Masa jabłka to około 150', 'g', ['kg', 't', 'dag']], ['Masa dorosłego człowieka to około 70', 'kg', ['g', 't', 'dag']], "
            "['Masa tabliczki czekolady to około 100', 'g', ['kg', 't', 'mm']], ['Pojemność szklanki to około 250', 'ml', ['l', 'm³', 'km']], ['Pojemność wiadra to około 10', 'l', ['ml', 'm³', 'kg']], "
            "['Lekcja w szkole trwa 45', 'minut', ['sekund', 'godzin', 'dób']], ['Przerwa między lekcjami trwa 10', 'minut', ['sekund', 'godzin', 'dób']], ['Doba ma 24', 'godziny', ['minuty', 'sekundy', 'tygodnie']], "
            "['Mrugnięcie okiem trwa około 1', 'sekundę', ['godzinę', 'dobę', 'minutę']], ['Masa ciężarówki to około 10', 't', ['g', 'dag', 'mm']]]")
skill('ew-choose-unit', S, 'Jaka jednostka pasuje?', ['I-III.2.c', 'I-III.2.j'],
      [lvl('Wybierz jednostkę')],
      [('f', 'choice(' + UNITS_I3 + ')')],
      choice('@{f[0]} … Którą jednostkę należy wpisać w miejsce kropek?', 'f[1]', ['f[2][0]', 'f[2][1]', 'f[2][2]'],
             [('idea', 'Wyobraź sobie ten przedmiot lub czas i porównaj z tym, co znasz.'), ('conclude', '@{f[0]} @{f[1]}.')]),
      min_distinct=14, area=A2)

# ============================================================================ pieniądze (2.d, 2.h)
skill('ew-money-coins', S, 'Monety i banknoty', ['I-III.2.d', 'I-III.2.h'],
      [lvl('Złote', gr=0), lvl('Grosze', gr=1)],
      [('a', 'randint(1, 4)'), ('b', 'randint(1, 4)'), ('c', 'randint(1, 5)'),
       ('txt', "('Masz ' + pln(a, ['monetę', 'monety', 'monet']) + ' po 5 zł, ' + pln(b, ['monetę', 'monety', 'monet']) + ' po 2 zł i ' + pln(c, ['monetę', 'monety', 'monet']) + ' po 1 zł. Ile złotych masz?') if gr == 0 else "
               "('Masz ' + pln(a, ['monetę', 'monety', 'monet']) + ' po 50 gr, ' + pln(b, ['monetę', 'monety', 'monet']) + ' po 20 gr i ' + pln(c, ['monetę', 'monety', 'monet']) + ' po 10 gr. Ile groszy masz?')"),
       ('ans', 'a * 5 + b * 2 + c if gr == 0 else a * 50 + b * 20 + c * 10')],
      number('@{txt}', 'ans',
             [('idea', 'Policz osobno każdy rodzaj monet, a potem dodaj.'), ('compute', "@{(str(a) + ' · 5 + ' + str(b) + ' · 2 + ' + str(c) + ' = ' + str(ans) if gr == 0 else str(a) + ' · 50 + ' + str(b) + ' · 20 + ' + str(c) + ' · 10 = ' + str(ans))}")]),
      min_distinct=30, tags=FIN, area=A2,
      intro='Pieniądze w Polsce to złote (zł) i grosze (gr). 1 zł to 100 gr. Mamy monety: 1 gr, 2 gr, 5 gr, 10 gr, 20 gr, 50 gr, 1 zł, 2 zł, 5 zł oraz banknoty.')

skill('ew-money-notation', S, 'Zapis cen z przecinkiem', ['I-III.2.d', 'I-III.2.h'],
      [lvl('Ile groszy ma cena?', mode=0), lvl('Zapisz cenę z przecinkiem', mode=1)],
      [('z', 'randint(1, 20)'), ('g', 'randint(1, 19) * 5'),
       ('txt', "('Cena batonika to ' + fmt(z + g / 100, 2) + ' zł. Ile to groszy?') if mode == 0 else "
               "('Cena soku to ' + str(z) + ' zł ' + str(g) + ' gr. Zapisz tę cenę w złotych z przecinkiem (np. 3,40).')"),
       ('ans', 'z * 100 + g if mode == 0 else z + g / 100')],
      decimal('@{txt}', 'ans',
              [('idea', '1 zł = 100 gr. W zapisie 12,50 zł po przecinku są grosze.'), ('conclude', '@{(str(ans) + \' gr\' if mode == 0 else fmt(ans, 2) + \' zł\')}')]),
      constraints=['g < 100'], min_distinct=30, tags=FIN, area=A2, prereq=['ew-money-coins'])

skill('ew-shopping', S, 'Zakupy i reszta', ['I-III.2.h', 'I-III.5.h'],
      [lvl('Pełne złote', mode=0), lvl('Ceny z groszami', mode=1), lvl('Reszta z banknotu', mode=2)],
      [('names', "shuffle([['zeszyt', 'zeszyt'], ['długopis', 'długopis'], ['gumka', 'gumka'], ['pierniczek', 'pierniczek'], ['sok', 'sok'], ['bułka', 'bułka']])"),
       ('p1', 'randint(2, 12) if mode == 0 else randint(2, 12) * 50 / 100 + 1'), ('p2', 'randint(2, 12) if mode == 0 else randint(2, 12) * 50 / 100 + 1'), ('bill', 'choice([10, 20, 50])'),
       ('cost', 'p1 + p2'),
       ('txt', "('Cena: ' + names[0][0] + ' – ' + fmt(p1, 2 if mode > 0 else 0) + ' zł, ' + names[1][0] + ' – ' + fmt(p2, 2 if mode > 0 else 0) + ' zł. Ile zapłacimy za oba?') if mode < 2 else "
               "('Cena: ' + names[0][0] + ' – ' + fmt(p1, 2) + ' zł, ' + names[1][0] + ' – ' + fmt(p2, 2) + ' zł. Kupiono oba i zapłacono banknotem ' + str(bill) + ' zł. Ile reszty?')"),
       ('ans', 'cost if mode < 2 else bill - cost')],
      quantity('@{txt}', 'ans', 'zł',
               [('idea', "@{('Dodaj ceny obu towarów.' if mode < 2 else 'Dodaj ceny obu towarów, a potem odejmij od banknotu.')}"),
                ('conclude', "@{('Razem: ' + fmt(cost, 2) + ' zł.' if mode < 2 else 'Reszta: ' + str(bill) + ' − ' + fmt(cost, 2) + ' = ' + fmt(bill - cost, 2) + ' zł.')}")], decimals=2),
      constraints=['mode < 2 or bill > cost', 'mode != 0 or p1 != p2'], tags=FIN, min_distinct=40, area=A2, prereq=['ew-money-notation', 'ew-add'])

# ============================================================================ przeliczanie jednostek (2.e, 2.f, 2.g, 2.i)
conv_i3('ew-convert-length', 'Jednostki długości', ['I-III.2.e'], ['mm', 'cm', 'm', 'km'], ['1', '10', '1000', '1000000'],
        [('Centymetry na milimetry', [[1, 0]], 2, 30), ('Metry na centymetry', [[2, 1]], 2, 20), ('Kilometry na metry', [[3, 2]], 2, 20),
         ('W obie strony (okrągłe liczby)', [[1, 0], [2, 1], [3, 2], [0, 1], [1, 2], [2, 3]], 10, 90)],
        'Jednostki długości: 1 cm = 10 mm, 1 m = 100 cm, 1 km = 1000 m. Z większej jednostki na mniejszą mnożymy, z mniejszej na większą dzielimy.')
conv_i3('ew-convert-mass', 'Jednostki masy', ['I-III.2.f'], ['g', 'dag', 'kg'], ['1', '10', '1000'],
        [('Kilogramy na dekagramy', [[2, 1]], 2, 20), ('Kilogramy na gramy', [[2, 0]], 2, 20), ('W obie strony (okrągłe liczby)', [[2, 1], [2, 0], [1, 2], [0, 2]], 10, 90)],
        'Jednostki masy: 1 kg = 100 dag = 1000 g.')
conv_i3('ew-convert-time', 'Jednostki czasu', ['I-III.2.g'], ['s', 'min', 'h'], ['1', '60', '3600'],
        [('Godziny na minuty', [[2, 1]], 2, 10), ('Minuty na sekundy', [[1, 0]], 2, 10), ('W obie strony (okrągłe liczby)', [[2, 1], [1, 0], [1, 2], [0, 1]], 2, 20)],
        'Czas: 1 godzina = 60 minut, 1 minuta = 60 sekund.')

skill('ew-compound', S, 'Wyrażenia dwumianowane', ['I-III.2.i'],
      [lvl('Metry i centymetry', k=0), lvl('Kilogramy i dekagramy lub gramy', k=1), lvl('Godziny i minuty', k=2)],
      [('a', 'randint(1, 9)'), ('b', 'randint(1, 9) * 10 if k < 2 else randint(1, 5) * 10'),
       ('big', "['m', 'kg', 'h'][k]"), ('small', "['cm', 'dag', 'min'][k]"), ('r', '[100, 100, 60][k]'), ('ans', 'a * r + b')],
      quantity('Zamień na jedną jednostkę: @{a} @{big} @{b} @{small} = ? @{small}', 'ans', 'small',
               [('idea', 'Najpierw zamień większą jednostkę na mniejszą: @{a} @{big} = @{a * r} @{small}. Potem dodaj resztę.'), ('compute', '@{a * r} + @{b} = @{ans}')], unit_expr=True),
      min_distinct=30, area=A2, prereq=['ew-convert-length'])

skill('ew-compare-measures', S, 'Co jest dłuższe, cięższe, dłuższe w czasie?', ['I-III.2.j'],
      [lvl('Porównaj wielkości')],
      [('pairs', "[[3, 'm', 250, 'cm', 'm', 3, 250, 'długość'], [2, 'kg', 1500, 'g', 'kg', 2, 1500, 'masa'], [1, 'h', 50, 'min', 'h', 60, 50, 'czas'], [4, 'km', 3500, 'm', 'km', 4000, 3500, 'długość'], "
                 "[1, 'm', 120, 'cm', 'm', 100, 120, 'długość'], [3, 'kg', 2500, 'g', 'kg', 3000, 2500, 'masa'], [2, 'h', 90, 'min', 'h', 120, 90, 'czas'], [5, 'm', 450, 'cm', 'm', 500, 450, 'długość']]"),
       ('p', 'choice(pairs)'), ('v1', 'p[5]'), ('v2', 'p[6]')],
      choice_text('Co jest większe: @{p[0]} @{p[1]} czy @{p[2]} @{p[3]}? (Porównaj, zamieniając na tę samą jednostkę.)',
                  [('@{p[0]} @{p[1]}', 'v1 > v2'), ('@{p[2]} @{p[3]}', 'v2 > v1'), ('Są równe', 'v1 == v2')], None,
                  [('idea', 'Zamień obie wielkości na tę samą mniejszą jednostkę i porównaj liczby.'), ('compute', '@{p[0]} @{p[1]} = @{v1} @{p[3]}, a drugą wielkością jest @{v2} @{p[3]}.')], fixed_order=True),
      min_distinct=8, area=A2, prereq=['ew-convert-length'])

skill('ew-time-add', S, 'O której godzinie?', ['I-III.2.a', 'I-III.2.g'],
      [lvl('Pełne godziny', step=60, dmax=3), lvl('Pół godziny', step=30, dmax=4), lvl('Kwadrans i minuty', step=15, dmax=8)],
      [('start', 'randint(6, 18) * 60 + randint(0, 1) * 30 * (1 if step < 60 else 0)'), ('dur', 'step * randint(1, dmax)'), ('end', 'start + dur'),
       ('c', "choice([['Lekcja zaczyna się o ', ' i trwa ', 'O której się kończy?'], ['Film zaczyna się o ', ' i trwa ', 'O której się skończy?'], ['Wycieczka zaczyna się o ', ' i trwa ', 'O której się zakończy?']])"),
       ('dtxt', "(str(dur // 60) + ' h') if dur % 60 == 0 else (str(dur) + ' min')")],
      task('time-input', '@{c[0]}@{hhmm(start)}@{c[1]}@{dtxt}. @{c[2]}', Time('hhmm(end)'),
           [('idea', 'Dodaj czas trwania do godziny rozpoczęcia. 60 minut to 1 godzina.'), ('compute', '@{hhmm(start)} + @{dtxt} = @{hhmm(end)}')]),
      constraints=['end < 1440'], min_distinct=20, area=A2, prereq=['ew-clock-read'])

# ============================================================================ figury (3.a - 3.f)
SOLIDS3 = "['sześcian', 'prostopadłościan', 'kula', 'walec']"
OBJ3 = ("[['kostka do gry', 'kostka lodu', 'pudełko po klockach w kształcie kostki'], ['pudełko po butach', 'cegła', 'lodówka'], "
        "['piłka', 'globus', 'bombka choinkowa'], ['puszka po kukurydzy', 'rolka papieru', 'bęben']]")
skill('ew-solid-object', S, 'Bryły wokół nas', ['I-III.3.a'],
      [lvl('Jaki kształt ma przedmiot?', mode=0), lvl('Który przedmiot ma dany kształt?', mode=1)],
      [('solids', SOLIDS3), ('objs', OBJ3), ('s', 'randint(0, 3)'), ('o', 'randint(0, 2)'), ('o2', 'randint(0, 2)')],
      choice("@{('Jaki kształt ma ' + objs[s][o] + '?' if mode == 0 else 'Który z przedmiotów ma kształt bryły: ' + solids[s] + '?')}",
             'solids[s] if mode == 0 else objs[s][o]',
             ['solids[(s + 1) % 4] if mode == 0 else objs[(s + 1) % 4][o2]', 'solids[(s + 2) % 4] if mode == 0 else objs[(s + 2) % 4][o2]', 'solids[(s + 3) % 4] if mode == 0 else objs[(s + 3) % 4][o2]'],
             [('idea', 'Sześcian i prostopadłościan mają płaskie ściany; kula jest okrągła ze wszystkich stron; walec ma dwie okrągłe podstawy.'), ('conclude', 'Prawidłowa odpowiedź: @{(solids[s] if mode == 0 else objs[s][o])}.')]),
      min_distinct=12, area=A3,
      intro='Sześcian i prostopadłościan mają płaskie ściany. Kula jest okrągła ze wszystkich stron i nie ma ścian. Walec ma dwie płaskie, okrągłe podstawy i zakrzywioną powierzchnię boczną.')

skill('ew-shape-description', S, 'Jaka to figura?', ['I-III.3.b'],
      [lvl('Poznaj figury płaskie')],
      [('names', "['trójkąt', 'kwadrat', 'prostokąt', 'koło']"),
       ('descs', "[['Ma 3 boki i 3 wierzchołki.', 'Ma trzy kąty.'], ['Ma 4 równe boki i 4 kąty proste.', 'Wszystkie jego boki mają tę samą długość, a kąty są proste.'], "
                 "['Ma 4 kąty proste, a przeciwległe boki mają równe długości.', 'Ma dwa dłuższe i dwa krótsze boki oraz cztery kąty proste.'], "
                 "['Nie ma boków ani wierzchołków.', 'Jest okrągłe, a wszystkie punkty brzegu są tak samo daleko od środka.']]"),
       ('s', 'randint(0, 3)'), ('d', 'randint(0, 1)')],
      choice('Którą figurę opisuje zdanie: „@{descs[s][d]}”?', 'names[s]', ['names[(s + 1) % 4]', 'names[(s + 2) % 4]', 'names[(s + 3) % 4]'],
             [('idea', 'Policz boki i wierzchołki oraz zwróć uwagę na kąty proste.'), ('conclude', 'To @{names[s]}.')]),
      min_distinct=8, area=A3)

skill('ew-shape-count', S, 'Boki, wierzchołki, kąty', ['I-III.3.b'],
      [lvl('Ile boków i wierzchołków?')],
      [('sh', "choice([['trójkąt', 3], ['kwadrat', 4], ['prostokąt', 4], ['czworokąt', 4]])"), ('ask', 'randint(0, 1)')],
      number("Ile @{('boków' if ask == 0 else 'wierzchołków')} ma @{sh[0]}?", 'sh[1]',
             [('idea', 'Policz boki (odcinki) lub wierzchołki (rogi) figury.'), ('conclude', 'Odpowiedź: @{sh[1]}.')]),
      min_distinct=8, area=A3, prereq=['ew-shape-description'])

skill('ew-perimeter', S, 'Obwód trójkąta i prostokąta', ['I-III.3.c'],
      [lvl('Kwadrat i prostokąt', f=0), lvl('Trójkąt', f=1), lvl('Dłuższe boki', f=2)],
      [('a', 'randint(2, 12) if f < 2 else randint(10, 40)'), ('b', 'randint(2, 12) if f < 2 else randint(10, 40)'), ('c', 'randint(abs(a - b) + 1, a + b - 1) if f > 0 else 0'),
       ('sq', 'randint(0, 1) == 1'), ('un', "choice(['cm', 'm'])"),
       ('txt', "('Kwadrat ma bok ' + str(a) + ' ' + un + '. Oblicz jego obwód.') if (f == 0 and sq) else "
               "(('Prostokąt ma boki ' + str(a) + ' ' + un + ' i ' + str(b) + ' ' + un + '. Oblicz jego obwód.') if f == 0 or f == 2 else "
               "('Trójkąt ma boki ' + str(a) + ' ' + un + ', ' + str(b) + ' ' + un + ' i ' + str(c) + ' ' + un + '. Oblicz jego obwód.'))"),
       ('ans', '4 * a if (f == 0 and sq) else (2 * a + 2 * b if f != 1 else a + b + c)')],
      quantity('@{txt}', 'ans', 'un',
               [('idea', 'Obwód to suma długości wszystkich boków.'), ('conclude', 'Obwód: @{ans} @{un}.')], unit_expr=True,
               errors=[('area_instead', Qty('a * b', 'un', True), 'To jest iloczyn boków. Obwód to suma wszystkich boków.', 'f != 1 and not (f == 0 and sq)')]),
      constraints=['f == 1 or a != b'], min_distinct=30, area=A3, prereq=['ew-shape-count', 'ew-add'])

SYM_YES = "['A', 'H', 'I', 'M', 'O', 'T', 'U', 'V', 'W', 'X', 'Y', 'B', 'C', 'D', 'E']"
SYM_NO = "['F', 'G', 'J', 'L', 'P', 'R', 'S', 'Z']"
skill('ew-symmetry-letters', S, 'Które litery mają oś symetrii?', ['I-III.3.d'],
      [lvl('Wskaż literę z osią symetrii')],
      [('yes', 'shuffle(' + SYM_YES + ')'), ('no', 'shuffle(' + SYM_NO + ')')],
      choice('Którą literę (wielką, drukowaną) można złożyć wzdłuż prostej tak, że obie połowy się pokryją?', 'yes[0]', ['no[0]', 'no[1]', 'no[2]'],
             [('idea', 'Oś symetrii to prosta, wzdłuż której można złożyć figurę tak, aby obie części się pokryły.'), ('conclude', 'Litera @{yes[0]} ma oś symetrii.')]),
      min_distinct=15, area=A3,
      intro='Figura ma oś symetrii, jeśli da się ją złożyć wzdłuż prostej tak, że obie połowy dokładnie się pokrywają, jak skrzydła motyla.')

skill('ew-symmetry-count', S, 'Ile osi symetrii?', ['I-III.3.d'],
      [lvl('Figury i przedmioty')],
      [('items', "[['kwadrat', 4], ['prostokąt (niebędący kwadratem)', 2], ['trójkąt równoboczny', 3], ['motyl z rozłożonymi skrzydłami', 1], ['litera H', 2], ['litera T', 1], "
                 "['litera A', 1], ['litera O', 2], ['litera X', 2], ['litera M', 1], ['litera B', 1], ['litera E', 1], ['trójkąt równoramienny (niebędący równobocznym)', 1], "
                 "['romb (niebędący kwadratem)', 2], ['pięcioramienna gwiazda', 5], ['znak plus (+)', 4], ['serce', 1], ['cyfra 8', 1], ['cyfra 0', 2], ['trapez równoramienny', 1]]"),
       ('it', 'choice(items)'), ('ph', 'randint(0, 1)')],
      number("@{('Ile osi symetrii ma ten kształt: ' + it[0] + '?' if ph == 0 else 'Na ile sposobów można złożyć ' + it[0] + ' wzdłuż prostej tak, aby obie części się pokryły?')}", 'it[1]',
             [('idea', 'Spróbuj złożyć kształt na różne sposoby tak, aby obie części się pokryły.'), ('conclude', 'Odpowiedź: @{it[1]}.')]),
      min_distinct=20, area=A3, prereq=['ew-symmetry-letters'])

skill('ew-directions', S, 'Gdzie jest przedmiot?', ['I-III.3.e'],
      [lvl('Lewo, prawo, przed, za')],
      [('ppl', "[['Ola', 'Oli', 'Olą'], ['Ania', 'Ani', 'Anią'], ['Kuba', 'Kuby', 'Kubą'], ['Marek', 'Marka', 'Markiem'], ['Maja', 'Mai', 'Mają'], ['Zosia', 'Zosi', 'Zosią']]"),
       ('i', 'randint(0, 5)'), ('j', 'randint(0, 5)'), ('p1', 'ppl[i]'), ('p2', 'ppl[j]'), ('rel', 'randint(0, 3)'),
       ('phr', "['po lewej stronie ' + p2[1], 'po prawej stronie ' + p2[1], 'przed ' + p2[2], 'za ' + p2[2]]"),
       ('words', "['po lewej stronie', 'po prawej stronie', 'przed', 'za']"), ('inv', "['po prawej stronie', 'po lewej stronie', 'za', 'przed']")],
      choice('@{p1[0]} siedzi @{phr[rel]}. Gdzie siedzi @{p2[0]} względem @{p1[1]}?', 'inv[rel]', ['words[rel]', 'inv[(rel + 2) % 4]', 'words[(rel + 2) % 4]'],
             [('idea', 'Wyobraź sobie, że siedzisz na miejscu drugiej osoby i patrzysz na pierwszą.'), ('conclude', 'Odpowiedź: @{inv[rel]}.')]),
      constraints=['i != j'], min_distinct=20, area=A3)

skill('ew-grid-robot', S, 'Robot na kratkach', ['I-III.3.e', 'I-III.3.f'],
      [lvl('Dwa ruchy', n=2), lvl('Trzy ruchy', n=3)],
      [('x0', 'randint(1, 4)'), ('y0', 'randint(1, 4)'), ('r', 'randint(1, 4)'), ('u', 'randint(1, 4)'), ('l', 'randint(1, 3)'),
       ('d', 'randint(1, 3)'), ('xe', 'x0 + r - (l if n == 3 else 0)'), ('ye', 'y0 + u - (d if n == 3 else 0)'),
       ('moves', "'idzie ' + pln(r, ['kratkę', 'kratki', 'kratek']) + ' w prawo, potem ' + pln(u, ['kratkę', 'kratki', 'kratek']) + ' w górę' + (', potem ' + pln(l, ['kratkę', 'kratki', 'kratek']) + ' w lewo i ' + pln(d, ['kratkę', 'kratki', 'kratek']) + ' w dół' if n == 3 else '')")],
      task('point-input', 'Robot stoi w punkcie (@{x0}, @{y0}). Najpierw podajemy numer kolumny, potem numer wiersza. Robot @{moves}. W którym punkcie stanie?', Pt('xe', 'ye'),
           [('idea', 'W prawo zwiększa pierwszą liczbę, w górę – drugą. W lewo i w dół zmniejszamy.'), ('conclude', 'Robot stanie w punkcie (@{xe}, @{ye}).')]),
      constraints=['xe >= 0', 'ye >= 0', 'n == 2 or (l < x0 + r and d < y0 + u)'], min_distinct=40, area=A3)

LINES_FACTS = ("[['Szyny kolejowe obok siebie', 'równoległe'], ['Ściana i podłoga w pokoju', 'prostopadłe'], ['Wskazówki zegara o godzinie 3:00', 'prostopadłe'], "
               "['Dwie sąsiednie krawędzie kartki papieru', 'prostopadłe'], ['Pasy na przejściu dla pieszych', 'równoległe'], ['Dwie przeciwległe krawędzie stołu', 'równoległe'], "
               "['Pionowy słup i poziomy chodnik', 'prostopadłe'], ['Linie w zeszycie do pisania', 'równoległe']]")
skill('ew-lines-surroundings', S, 'Proste równoległe i prostopadłe wokół nas', ['I-III.3.f'],
      [lvl('Rozpoznaj w otoczeniu')],
      [('f', 'choice(' + LINES_FACTS + ')')],
      choice_text('@{f[0]} to przykład prostych …', [('równoległych', "f[1] == 'równoległe'"), ('prostopadłych', "f[1] == 'prostopadłe'")], None,
                  [('idea', 'Równoległe nigdy się nie przecinają i są wszędzie tak samo oddalone. Prostopadłe przecinają się pod kątem prostym.'), ('conclude', 'To są proste @{f[1]}.')], fixed_order=True),
      min_distinct=8, area=A3)

skill('ew-pion-poziom', S, 'Pion, poziom, skos', ['I-III.3.f'],
      [lvl('Jak ustawiona jest linia?')],
      [('f', "choice([['Maszt z flagą', 'pionowo'], ['Linia horyzontu nad morzem', 'poziomo'], ['Ściana boczna dachu domu', 'skośnie'], ['Rząd cegieł w murze', 'poziomo'], "
               "['Komin wysokiego domu', 'pionowo'], ['Drabina oparta o ścianę', 'skośnie'], ['Deska, na której bąbelek poziomicy jest w środku', 'poziomo'], ['Latarnia uliczna', 'pionowo']])")],
      choice_text('Jak najczęściej ustawiony jest przedmiot: @{f[0]}?', [('pionowo', "f[1] == 'pionowo'"), ('poziomo', "f[1] == 'poziomo'"), ('skośnie', "f[1] == 'skośnie'")], None,
                  [('idea', 'Pion – jak sznurek z ciężarkiem. Poziom – jak woda w kałuży. Skos – coś pomiędzy.'), ('conclude', 'Jest ustawiony @{f[1]}.')], fixed_order=True),
      min_distinct=8, area=A3, prereq=['ew-lines-surroundings'])

# ============================================================================ ścieżka
un = Unit(S, 'ew-u5', 'Mierzymy: długość, temperatura, czas', 'Linijka, termometr i zegar.', 'ruler', area=A2)
un.learn('ew-ruler-read').learn('ew-thermometer-read').learn('ew-temp-diff').learn('ew-clock-read').learn('ew-time-add')
un.review('Powtórka: pomiary', ['ew-ruler-read', 'ew-thermometer-read', 'ew-temp-diff', 'ew-clock-read', 'ew-time-add'])
un.learn('ew-choose-unit')
un.checkpoint(['ew-ruler-read', 'ew-thermometer-read', 'ew-temp-diff', 'ew-clock-read', 'ew-time-add'])

un = Unit(S, 'ew-u6', 'Jednostki miar', 'Zamieniamy centymetry, kilogramy i godziny.', 'scale', area=A2)
un.learn('ew-convert-length').learn('ew-convert-mass').learn('ew-convert-time').learn('ew-compound').learn('ew-compare-measures')
un.checkpoint(['ew-convert-length', 'ew-convert-mass', 'ew-convert-time', 'ew-compound', 'ew-compare-measures'])

un = Unit(S, 'ew-u7', 'Pieniądze', 'Monety, ceny z przecinkiem, zakupy i reszta.', 'wallet', area=A2)
un.learn('ew-money-coins').learn('ew-money-notation').learn('ew-shopping')
un.checkpoint(['ew-money-coins', 'ew-money-notation', 'ew-shopping'])

un = Unit(S, 'ew-u8', 'Bryły i figury', 'Bryły wokół nas, figury płaskie, obwód i symetria.', 'shapes', area=A3)
un.learn('ew-solid-object').learn('ew-shape-description').learn('ew-shape-count').learn('ew-perimeter')
un.review('Powtórka: figury', ['ew-solid-object', 'ew-shape-description', 'ew-shape-count', 'ew-perimeter'])
un.learn('ew-symmetry-letters').learn('ew-symmetry-count').learn('ew-directions').learn('ew-grid-robot').learn('ew-lines-surroundings').learn('ew-pion-poziom')
un.checkpoint(['ew-solid-object', 'ew-shape-description', 'ew-perimeter', 'ew-symmetry-letters', 'ew-directions', 'ew-grid-robot'])
