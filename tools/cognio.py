#!/usr/bin/env python3
"""Reference implementation + tooling for the course pack format (docs/02-course-format.md).

Commands (run with `python3 -I tools/cognio.py ...` from the project root):
  lint  <packdir>                      validate schemas + references + generator smoke tests + llm-spec examples
  gen   <packdir> <generator> <level> <seed>     print one generated task
  vectors <packdir> <out.json>         write conformance vectors (generator, level, seed -> task) for an engine port
  sample <packdir> <skill|all> [n]       print generated tasks for human review
  coverage <packdir>                   which official objectives have skills (per stage / area)
  scenes <packdir> <out.json>          media -> scene conformance cases for a renderer port
  quest <packdir> <id> [seed]          print one generated quest (story + steps + answers)
  fit   <packdir>                      lower lesson sizes to what the task sources can supply
  pack  <packdir> <out.cognio>       write file hashes into course.json and zip the pack

Every engine port (the app\'s Dart engine) MUST reproduce `vectors` bit-for-bit; this file is the executable specification
of the DSL (PRNG, expression language, filters).
"""
import ast, hashlib, json, math, pathlib, re, sys, zipfile
from fractions import Fraction
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import render as figures

MASK = (1 << 64) - 1
NBSP = ' '
MAX_TRIES = 1000


# ----------------------------------------------------------------------------- Polish numerals
_ONES = ['zero', 'jeden', 'dwa', 'trzy', 'cztery', 'pięć', 'sześć', 'siedem', 'osiem', 'dziewięć', 'dziesięć',
         'jedenaście', 'dwanaście', 'trzynaście', 'czternaście', 'piętnaście', 'szesnaście', 'siedemnaście',
         'osiemnaście', 'dziewiętnaście']
_TENS = ['', '', 'dwadzieścia', 'trzydzieści', 'czterdzieści', 'pięćdziesiąt', 'sześćdziesiąt', 'siedemdziesiąt',
         'osiemdziesiąt', 'dziewięćdziesiąt']
_HUNDREDS = ['', 'sto', 'dwieście', 'trzysta', 'czterysta', 'pięćset', 'sześćset', 'siedemset', 'osiemset', 'dziewięćset']
_GROUPS = [('', '', ''), ('tysiąc', 'tysiące', 'tysięcy'), ('milion', 'miliony', 'milionów'),
           ('miliard', 'miliardy', 'miliardów')]


def _words_below_1000(n):
    parts = []
    if n >= 100:
        parts.append(_HUNDREDS[n // 100])
        n %= 100
    if n >= 20:
        parts.append(_TENS[n // 10])
        n %= 10
        if n:
            parts.append(_ONES[n])
    elif n:
        parts.append(_ONES[n])
    return ' '.join(parts)


def words_pl(n: int) -> str:
    """Polish cardinal numeral, nominative (0 .. 999 999 999 999). 1000 -> 'tysiąc', 1 000 000 -> 'milion'."""
    if n == 0:
        return 'zero'
    groups, out = [], []
    while n:
        groups.append(n % 1000)
        n //= 1000
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        if g == 0:
            continue
        if i == 0:
            out.append(_words_below_1000(g))
        elif g == 1:
            out.append(_GROUPS[i][0])
        else:
            out.append(_words_below_1000(g) + ' ' + pl_form(g, _GROUPS[i]))
    return ' '.join(out)


# ----------------------------------------------------------------------------- PRNG (SplitMix64)
class Rng:
    def __init__(self, seed: int):
        self.s = seed & MASK

    def next(self) -> int:
        self.s = (self.s + 0x9E3779B97F4A7C15) & MASK
        z = self.s
        z = ((z ^ (z >> 30)) * 0xBF58476D1CE4E5B9) & MASK
        z = ((z ^ (z >> 27)) * 0x94D049BB133111EB) & MASK
        return z ^ (z >> 31)


# ----------------------------------------------------------------------------- expression language
class DslError(Exception):
    pass


def _num(x):
    if isinstance(x, bool) or not isinstance(x, (int, Fraction)):
        raise DslError(f'number expected, got {x!r}')
    return Fraction(x)


def idstr(x):
    """Canonical string of a value: used for option ids, sequence/set members and str()."""
    if isinstance(x, str):
        return x
    if isinstance(x, Fraction) and x.denominator != 1:
        try:
            return dec_plain(x)
        except DslError:
            return f'{x.numerator}/{x.denominator}'
    return str(int(x)) if not isinstance(x, bool) else str(x).lower()


def _norm(x):
    """Integers stay ints (Fractions with denominator 1 collapse)."""
    if isinstance(x, Fraction) and x.denominator == 1:
        return int(x)
    return x


def _isint(x):
    return isinstance(x, int) and not isinstance(x, bool)


class Evaluator:
    FUNCS = {}

    def __init__(self, rng=None):
        self.rng = rng

    def eval(self, src, env):
        try:
            tree = ast.parse(src.strip(), mode='eval')
        except SyntaxError as e:
            raise DslError(f'syntax error in {src!r}: {e}')
        return self._ev(tree.body, env)

    def _ev(self, n, env):
        t = type(n)
        if t is ast.Constant:
            v = n.value
            if isinstance(v, bool) or isinstance(v, str):
                return v
            if isinstance(v, int):
                return v
            if isinstance(v, float):
                return _norm(Fraction(repr(v)))
            raise DslError(f'constant {v!r} not allowed')
        if t is ast.Name:
            if n.id in env:
                return env[n.id]
            if n.id in ('True', 'False', 'true', 'false'):
                return n.id in ('True', 'true')
            raise DslError(f'unknown name {n.id}')
        if t is ast.List:
            return [self._ev(e, env) for e in n.elts]
        if t is ast.Subscript:
            seq = self._ev(n.value, env)
            idx = self._ev(n.slice, env)
            if not _isint(idx):
                raise DslError('index must be int')
            return seq[idx]
        if t is ast.UnaryOp:
            v = self._ev(n.operand, env)
            if isinstance(n.op, ast.USub):
                return _norm(-_num(v))
            if isinstance(n.op, ast.UAdd):
                return _norm(_num(v))
            if isinstance(n.op, ast.Not):
                return not v
            raise DslError('unary operator not allowed')
        if t is ast.BinOp:
            a = self._ev(n.left, env)
            b = self._ev(n.right, env)
            op = n.op
            if isinstance(op, ast.Add):
                if isinstance(a, str) and isinstance(b, str):
                    return a + b
                if isinstance(a, list) and isinstance(b, list):
                    return a + b
                return _norm(_num(a) + _num(b))
            if isinstance(op, ast.Sub):
                return _norm(_num(a) - _num(b))
            if isinstance(op, ast.Mult):
                return _norm(_num(a) * _num(b))
            if isinstance(op, ast.Div):
                if _num(b) == 0:
                    raise DslError('division by zero')
                return _norm(_num(a) / _num(b))
            if isinstance(op, (ast.FloorDiv, ast.Mod)):
                if not (_isint(a) and _isint(b)) or b == 0:
                    raise DslError('// and % need integers (non-zero divisor)')
                return a // b if isinstance(op, ast.FloorDiv) else a % b
            raise DslError('binary operator not allowed (use pow(a, n) for powers)')
        if t is ast.BoolOp:
            if isinstance(n.op, ast.And):
                for v in n.values:
                    if not self._ev(v, env):
                        return False
                return True
            for v in n.values:
                if self._ev(v, env):
                    return True
            return False
        if t is ast.Compare:
            left = self._ev(n.left, env)
            for op, comp in zip(n.ops, n.comparators):
                right = self._ev(comp, env)
                if isinstance(op, ast.In):
                    ok = left in right
                elif isinstance(op, ast.NotIn):
                    ok = left not in right
                else:
                    f = {ast.Eq: lambda x, y: x == y, ast.NotEq: lambda x, y: x != y, ast.Lt: lambda x, y: x < y,
                         ast.LtE: lambda x, y: x <= y, ast.Gt: lambda x, y: x > y, ast.GtE: lambda x, y: x >= y}[type(op)]
                    ok = f(left, right)
                if not ok:
                    return False
                left = right
            return True
        if t is ast.IfExp:
            return self._ev(n.body, env) if self._ev(n.test, env) else self._ev(n.orelse, env)
        if t is ast.Call:
            if not isinstance(n.func, ast.Name) or n.keywords:
                raise DslError('only plain function calls allowed')
            return self._call(n.func.id, [self._ev(a, env) for a in n.args])
        raise DslError(f'syntax element {t.__name__} not allowed')

    def _call(self, name, a):
        if name == 'randint':
            lo, hi = a
            if not (_isint(lo) and _isint(hi)) or hi < lo:
                raise DslError('randint(lo, hi) needs ints, lo <= hi')
            return lo + self.rng.next() % (hi - lo + 1)
        if name == 'choice':
            (seq,) = a
            return seq[self.rng.next() % len(seq)]
        if name == 'gcd':
            return math.gcd(int(a[0]), int(a[1]))
        if name == 'lcm':
            return math.lcm(int(a[0]), int(a[1]))
        if name == 'floor':
            return math.floor(_num(a[0]))
        if name == 'ceil':
            return math.ceil(_num(a[0]))
        if name == 'abs':
            return _norm(abs(_num(a[0])))
        if name == 'min':
            return min(a[0]) if len(a) == 1 and isinstance(a[0], list) else min(a)
        if name == 'max':
            return max(a[0]) if len(a) == 1 and isinstance(a[0], list) else max(a)
        if name == 'pow':
            base, e = a
            if not _isint(e) or abs(e) > 64:
                raise DslError('pow exponent must be an int, |e| <= 64')
            return _norm(_num(base) ** e)
        if name == 'round':       # round half up to k decimal places
            x, k = _num(a[0]), a[1]
            scale = Fraction(10) ** k
            return _norm(Fraction(math.floor(x * scale + Fraction(1, 2))) / scale)
        if name == 'len':
            return len(a[0])
        return self._call11(name, a)

    # ---- DSL 1.1 (additive) ------------------------------------------------------------------
    def _call11(self, name, a):
        def lst(x):
            if not isinstance(x, list):
                raise DslError(f'{name}: list expected')
            return x
        if name == 'sample':                      # k distinct ints from [lo, hi], in draw order
            lo, hi, k = a
            n = hi - lo + 1
            if not all(map(_isint, a)) or k > n or k < 0:
                raise DslError('sample(lo, hi, k): ints, k <= hi-lo+1')
            out = []
            while len(out) < k:
                x = lo + self.rng.next() % n
                if x not in out:
                    out.append(x)
            return out
        if name == 'shuffle':                     # Fisher-Yates, descending
            xs = list(lst(a[0]))
            for i in range(len(xs) - 1, 0, -1):
                j = self.rng.next() % (i + 1)
                xs[i], xs[j] = xs[j], xs[i]
            return xs
        if name == 'sorted':
            return sorted(lst(a[0]))
        if name == 'reverse':
            return list(reversed(lst(a[0])))
        if name == 'sum':
            return _norm(sum((_num(x) for x in lst(a[0])), Fraction(0)))
        if name == 'product':
            r = Fraction(1)
            for x in lst(a[0]):
                r *= _num(x)
            return _norm(r)
        if name == 'range':
            lo, hi = a
            if not (_isint(lo) and _isint(hi)) or hi - lo > 1000:
                raise DslError('range(lo, hi): ints, at most 1000 elements')
            return list(range(lo, hi))
        if name == 'digits':
            n = a[0]
            if not _isint(n) or n < 0:
                raise DslError('digits(n): n >= 0 int')
            return [int(c) for c in str(n)]
        if name == 'is_prime':
            n = a[0]
            return _isint(n) and n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))
        if name == 'factorize':
            n, out, d = a[0], [], 2
            if not _isint(n) or n < 2:
                raise DslError('factorize(n): n >= 2 int')
            while d * d <= n:
                while n % d == 0:
                    out.append(d)
                    n //= d
                d += 1
            return out + ([n] if n > 1 else [])
        if name == 'divisors':
            n = a[0]
            if not _isint(n) or n < 1:
                raise DslError('divisors(n): n >= 1 int')
            return [d for d in range(1, n + 1) if n % d == 0]
        if name == 'roman':
            n = a[0]
            if not _isint(n) or not 1 <= n <= 3999:
                raise DslError('roman(n): 1..3999')
            out = ''
            for v, r in ((1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'),
                         (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')):
                while n >= v:
                    out += r
                    n -= v
            return out
        if name == 'isqrt':
            return math.isqrt(a[0])
        if name == 'icbrt':
            n = a[0]
            r = round(n ** (1 / 3))
            while r ** 3 > n:
                r -= 1
            while (r + 1) ** 3 <= n:
                r += 1
            return r
        if name == 'numer':
            return Fraction(a[0]).numerator
        if name == 'denom':
            return Fraction(a[0]).denominator
        if name == 'sign':
            x = _num(a[0])
            return (x > 0) - (x < 0)
        if name == 'count':
            return lst(a[0]).count(a[1])
        if name == 'index':
            return lst(a[0]).index(a[1])
        if name == 'mean':
            xs = [_num(x) for x in lst(a[0])]
            return _norm(sum(xs, Fraction(0)) / len(xs))
        if name == 'median':
            xs = sorted(_num(x) for x in lst(a[0]))
            m = len(xs) // 2
            return _norm(xs[m] if len(xs) % 2 else (xs[m - 1] + xs[m]) / 2)
        if name == 'take':
            return lst(a[0])[:a[1]]
        if name == 'drop':
            return lst(a[0])[a[1]:]
        if name == 'str':
            return idstr(a[0])
        if name == 'cap':
            return a[0][:1].upper() + a[0][1:]
        if name == 'hhmm':                        # minutes since midnight -> "H:MM" (mod 24 h)
            t = int(a[0]) % 1440
            return f'{t // 60}:{t % 60:02d}'
        if name in ('pln', 'plw'):                # "5 jabłek" / "jabłek": Polish plural agreement as a string
            n, forms = a
            return (fmt_value(n, 'dec', None, False) + ' ' if name == 'pln' else '') + pl_form(n, forms)
        if name == 'fmt':                         # number as text: decimal comma, NBSP groups, optional fixed places
            return fmt_value(a[0], 'dec', a[1] if len(a) > 1 else None, False)
        if name == 'expand':                      # truncated decimal expansion with comma; '…' if it does not terminate
            x, k = _num(a[0]), a[1]
            neg = x < 0
            x = abs(x)
            ip = int(x)
            frac, digs = x - ip, ''
            for _ in range(k):
                frac *= 10
                d = int(frac)
                digs += str(d)
                frac -= d
            text = f'{ip},{digs}' if k else str(ip)
            text = ('\u2212' if neg else '') + text
            return text + ('\u2026' if frac != 0 else '')
        if name == 'poly':                        # polynomial text: poly([2, -1, 5], ['x', 'y', '']) -> "2x − y + 5"
            cs, vs = lst(a[0]), lst(a[1])
            out = ''
            for c, v in zip(cs, vs):
                if c == 0:
                    continue
                mag = str(abs(c)) if v == '' else ('' if abs(c) == 1 else str(abs(c))) + v
                out += (('\u2212' if c < 0 else '') + mag) if not out else (' \u2212 ' if c < 0 else ' + ') + mag
            return out or '0'
        if name in ('sqrt_dec', 'cbrt_dec'):      # root of a non-negative integer, rounded half up to k decimal places
            n, k = a
            if not (_isint(n) and _isint(k) and n >= 0 and 0 <= k <= 6):
                raise DslError(name + '(n, k): n >= 0 int, 0 <= k <= 6')
            deg = 2 if name == 'sqrt_dec' else 3
            target = n * 10 ** (deg * k)
            r = math.isqrt(target) if deg == 2 else round(target ** (1 / 3))
            if deg == 3:
                while r ** 3 > target:
                    r -= 1
                while (r + 1) ** 3 <= target:
                    r += 1
            # round half up: compare (r + 1/2)^deg with target exactly
            if (2 * r + 1) ** deg <= 2 ** deg * target:
                r += 1
            return _norm(Fraction(r, 10 ** k))
        if name == 'par':                         # negative numbers in parentheses: (−3)
            return fmt_value(a[0], 'par', None, False)
        if name == 'repeat':
            if not _isint(a[1]) or not 0 <= a[1] <= 1000:
                raise DslError('repeat(x, n): 0 <= n <= 1000')
            return [a[0]] * a[1]
        if name == 'join':
            return str(a[1]).join(idstr(x) for x in lst(a[0]))
        if name == 'setat':
            xs = list(lst(a[0]))
            xs[a[1]] = a[2]
            return xs
        if name == 'uniq':
            out = []
            for x in lst(a[0]):
                if x not in out:
                    out.append(x)
            return out
        if name == 'words':
            n = a[0]
            if not _isint(n) or not 0 <= n < 10 ** 12:
                raise DslError('words(n): 0 <= n < 10^12')
            return words_pl(n)
        if name == 'rev_digits':
            return int(str(a[0])[::-1])
        if name == 'is_square':
            return _isint(a[0]) and a[0] >= 0 and math.isqrt(a[0]) ** 2 == a[0]
        raise DslError(f'unknown function {name}')


# ----------------------------------------------------------------------------- formatting
def dec_plain(x: Fraction, places=None) -> str:
    """Exact decimal string with a DOT. places=None -> minimal digits (must terminate)."""
    x = Fraction(x)
    if places is None:
        # minimal power of ten that clears the denominator
        k = 0
        while (x * 10 ** k).denominator != 1:
            k += 1
            if k > 12:
                raise DslError('value has no finite decimal expansion')
        places = k
    scaled = x * 10 ** places
    if scaled.denominator != 1:   # fixed places -> round half up
        scaled = Fraction(math.floor(scaled + Fraction(1, 2)))
    s = int(scaled)
    neg = s < 0
    s = abs(s)
    digits = str(s).rjust(places + 1, '0')
    out = digits[:-places] + '.' + digits[-places:] if places else digits
    return ('-' if neg else '') + out


def thousands(s: str) -> str:
    neg = s.startswith('-')
    s = s.lstrip('-')
    ip, _, fp = s.partition('.')
    ip = f'{int(ip):,}'.replace(',', NBSP) if len(ip) > 4 else ip   # 4-digit numbers are not grouped (PL convention)
    return ('-' if neg else '') + ip + ('.' + fp if fp else '')


def pl_form(n, forms):
    if isinstance(n, Fraction) or not _isint(n):
        return forms[1]                      # non-integers: genitive singular (≈ "few" form), e.g. 2,5 kg
    n = abs(n)
    if n == 1:
        return forms[0]
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return forms[1]
    return forms[2]


LIST_SEP = {None: ', ', 'and': None, 'or': None, 'semi': '; ', 'space': ' ', 'cdot': ' \\cdot ' , 'plus': ' + ', 'colon': ' : '}


def _minus(s, in_math):
    """Typographic minus in running text; LaTeX makes its own inside $...$."""
    return s if in_math or not s.startswith('-') else '\u2212' + s[1:]


def fmt_value(v, flt, arg, in_math):
    comma = '{,}' if in_math else ','
    if isinstance(v, list) and flt != 'list':
        raise DslError('a list needs the |list filter')
    if flt in (None, 'dec', 'par'):
        if isinstance(v, str):
            return v
        s = _minus(thousands(dec_plain(_num(v), None if arg is None else int(arg))).replace('.', comma), in_math)
        return f'({s})' if flt == 'par' and _num(v) < 0 else s
    if flt == 'int':
        return _minus(thousands(str(int(v))), in_math)
    if flt == 'money':
        return _minus(thousands(dec_plain(_num(v), 2)).replace('.', comma), in_math) + NBSP + 'zł'
    if flt == 'frac':
        f = Fraction(v)
        return str(f.numerator) if f.denominator == 1 else f'\\frac{{{f.numerator}}}{{{f.denominator}}}'
    if flt == 'mixed':
        f = Fraction(v)
        w, r = divmod(f.numerator, f.denominator) if f >= 0 else (0, 0)
        if f < 0 or r == 0 or w == 0:
            return fmt_value(f, 'frac', None, in_math)
        return f'{w}\\frac{{{r}}}{{{f.denominator}}}'
    if flt == 'list':
        sep, _, ef = (arg or '').partition(':')       # |list:SEP[:ELEMENT_FILTER], e.g. list:semi:frac
        arg = sep or None
        if ef:
            items = [fmt_value(x, ef, None, in_math) for x in v]
            if ef in ('frac', 'mixed') and not in_math:
                items = ['$' + i + '$' for i in items]
        else:
            items = [fmt_value(x, 'par' if arg == 'plus' else None, None, in_math) for x in v]
        if arg in ('and', 'or'):
            word = ' i ' if arg == 'and' else ' lub '
            return ', '.join(items[:-1]) + word + items[-1] if len(items) > 1 else items[0]
        return LIST_SEP[arg].join(items)
    raise DslError(f'unknown filter {flt}')


INTERP = re.compile(r'@\{(.*?)\}', re.S)


def render(template: str, env, ev: Evaluator) -> str:
    out, last, math_ctx = [], 0, False
    for m in INTERP.finditer(template):
        seg = template[last:m.start()]
        math_ctx ^= (seg.replace('\\$', '').count('$') % 2 == 1)
        out.append(seg)
        body = m.group(1)
        expr, flt, arg = body, None, None
        if '|' in body:
            expr, f = body.rsplit('|', 1)
            flt, _, arg = f.strip().partition(':')
            arg = arg or None
        if flt in ('dec', 'par') and arg is not None and not arg.lstrip('-').isdigit():
            arg = str(ev.eval(arg, env))             # places given as an expression, e.g. |dec:k
        if flt == 'pl':
            v = ev.eval(expr, env)
            forms = ev.eval(arg, env)
            out.append(fmt_value(v, 'dec', None, math_ctx) + ' ' + pl_form(v, forms))
        else:
            out.append(fmt_value(ev.eval(expr, env), flt, arg, math_ctx))
        last = m.end()
    out.append(template[last:])
    return ''.join(out)


# ----------------------------------------------------------------------------- value compilation
def _strict_int(v):
    if isinstance(v, bool) or not isinstance(v, (int, Fraction)) or Fraction(v).denominator != 1:
        raise DslError(f'integer expected, got {v!r}')
    return int(v)


def to_value(spec, env, ev):
    """Resolve {"$expr": ...} leaves; normalise numbers to canonical strings."""
    if isinstance(spec, dict):
        if set(spec) == {'$expr'}:
            return ev.eval(spec['$expr'], env)
        out = {k: to_value(v, env, ev) for k, v in spec.items()}
        t = out.get('type')
        if t == 'int':
            out['value'] = str(_strict_int(out['value']))
        elif t == 'decimal':
            out['value'] = dec_plain(_num(out['value']))
        elif t == 'rational':
            out['num'], out['den'] = str(_strict_int(out['num'])), str(_strict_int(out['den']))
        elif t == 'quantity' and not isinstance(out['value'], str):
            out['value'] = dec_plain(_num(out['value']))
        elif t == 'choice':
            out['value'] = str(out['value'])
        elif t == 'mixed':
            out['whole'], out['num'], out['den'] = (str(_strict_int(out[k])) for k in ('whole', 'num', 'den'))
        elif t in ('sequence', 'set'):
            out['value'] = [idstr(x) for x in out['value']]
        elif t == 'point':
            out['x'], out['y'] = str(_strict_int(out['x'])), str(_strict_int(out['y']))
        return out
    if isinstance(spec, list):
        return [to_value(x, env, ev) for x in spec]
    return spec


def resolve(spec, env, ev):
    """Generic resolution for `input` / `media`: {"$expr": ..} leaves are evaluated, strings are templates."""
    if isinstance(spec, dict):
        if set(spec) == {'$expr'}:
            return _plain(ev.eval(spec['$expr'], env))
        return {k: resolve(v, env, ev) for k, v in spec.items()}
    if isinstance(spec, list):
        return [resolve(x, env, ev) for x in spec]
    if isinstance(spec, str):
        return render(spec, env, ev) if '@{' in spec else spec
    return spec


def _plain(v):
    """Expression results -> JSON-able: numbers become exact strings (ints stay ints), lists recurse."""
    if isinstance(v, list):
        return [_plain(x) for x in v]
    if isinstance(v, bool) or isinstance(v, (int, str)):
        return v
    if isinstance(v, Fraction):
        return dec_plain(v) if v.denominator != 1 else int(v)
    return v


# ----------------------------------------------------------------------------- generators
def generate(gen: dict, skill_id: str, level: int, seed: int) -> dict:
    return generate_env(gen, skill_id, level, seed)[0]


def draw_vars(spec: dict, ev, base: dict) -> dict:
    """Evaluate spec['vars'] top to bottom, redrawing the whole list until spec['constraints'] hold (generators and quests)."""
    for _ in range(MAX_TRIES):
        env = dict(base)
        rejected = False
        for v in spec.get('vars', []):
            env[v['name']] = ev.eval(v['expr'], env)
            if v.get('require') and not env[v['name']]:    # early rejection: later vars may be undefined for this draw
                rejected = True
                break
        if not rejected and all(ev.eval(c, env) for c in spec.get('constraints', [])):
            return env
    raise DslError(f'constraints not satisfiable in {MAX_TRIES} tries')


def generate_quest(q: dict, skill_id: str, seed: int):
    """One quest instance: shared variables, then every step compiled as an ordinary task.  Returns (quest, env, ev)."""
    ev = Evaluator(Rng(seed))
    env = draw_vars(q, ev, {})
    steps = []
    for i, st in enumerate(q['steps'], 1):
        steps.append(compile_task(st, env, ev, {'id': f'{skill_id}/{q["id"]}/{seed}/{i}', 'skill': skill_id, 'level': 1,
                                                 'provenance': {'source': 'generator', 'generator': q['id'], 'seed': str(seed)}}))
    quest = {'id': f'{skill_id}/{q["id"]}/{seed}', 'skill': skill_id, 'kind': 'quest', 'title': q['title']['pl'], 'intro': render(q['intro'], env, ev), 'steps': steps}
    if q.get('media'):
        quest['media'] = resolve([{k: v for k, v in m.items() if k != 'when'} for m in q['media'] if 'when' not in m or ev.eval(m['when'], env)], env, ev)
    if q.get('outro'):
        quest['outro'] = render(q['outro'], env, ev)
    return quest, env, ev


def generate_env(gen: dict, skill_id: str, level: int, seed: int):
    """Like generate(), but also returns (env, evaluator) so the linter can evaluate selfCheck expressions."""
    lv = next((l for l in gen['levels'] if l['level'] == level), None)
    if lv is None:
        raise DslError(f'generator {gen["id"]} has no level {level}')
    ev = Evaluator(Rng(seed))
    env = {}
    for k, expr in lv.get('vars', {}).items():
        if 'randint' in expr or 'choice' in expr:
            raise DslError('random calls are not allowed in level vars')
        env[k] = ev.eval(expr, env)
    env = draw_vars(gen, ev, env)
    task = compile_task(gen['task'], env, ev, {
        'id': f'{skill_id}/{gen["id"]}/{level}/{seed}', 'skill': skill_id, 'level': level,
        'provenance': {'source': 'generator', 'generator': gen['id'], 'seed': str(seed)}})
    return task, env, ev


def compile_task(t: dict, env, ev, head: dict) -> dict:
    task = dict(head)
    task['kind'] = t['kind']
    task['prompt'] = render(t['prompt'], env, ev)
    if 'input' in t:
        task['input'] = resolve(t['input'], env, ev)
    if 'media' in t:
        media = [{k: v for k, v in m.items() if k != 'when'} for m in t['media'] if 'when' not in m or ev.eval(m['when'], env)]
        if media:
            task['media'] = resolve(media, env, ev)
    if 'options' in t:
        task['options'] = []
        for o in t['options']:
            opt = {'id': o['id'], 'text': render(o['text'], env, ev)}
            if 'correct' in o:
                opt['correct'] = bool(ev.eval(o['correct'], env))
            task['options'].append(opt)
    task['answer'] = to_value(t['answer'], env, ev)
    if t.get('equivalent'):
        task['equivalent'] = [{'answer': to_value(e['answer'], env, ev), 'verdict': e['verdict'],
                               **({'feedbackKey': e['feedbackKey']} if 'feedbackKey' in e else {})} for e in t['equivalent']]
    rules = []
    for r in t.get('errorRules', []):
        if 'when' in r and not ev.eval(r['when'], env):
            continue
        try:
            a = to_value(r['answer'], env, ev)
        except (DslError, ZeroDivisionError):
            continue                     # the buggy procedure has no representable result for this task
        if a == task['answer']:
            continue                     # a bug that gives the right answer here is not a bug
        rules.append({'id': r['id'], 'answer': a, 'feedback': render(r['feedback'], env, ev)})
    if rules:
        task['errorRules'] = rules
    task['steps'] = [{k: (render(v, env, ev) if k == 'text' else v) for k, v in s.items()} for s in t['steps']]
    if t.get('tags'):
        task['tags'] = t['tags']
    return task


# ----------------------------------------------------------------------------- LLM output verification
NUM = re.compile(r'^-?\d+(\.\d+)?$')


def verify_llm_output(spec: dict, skill_id: str, level: int, out: dict, index: int = 0):
    """Return (task, errors). The model's own numbers are inputs; the answer is recomputed here."""
    errs = []
    try:
        params = {}
        for k, v in out['params'].items():
            params[k] = _norm(Fraction(v)) if isinstance(v, str) and NUM.match(v) else v
        env = dict(params, level=level)
        ev = Evaluator()
        for v in spec['verifier'].get('vars', []):
            env[v['name']] = ev.eval(v['expr'], env)
        for c in spec['verifier'].get('constraints', []):
            if not ev.eval(c, env):
                errs.append(f'constraint failed: {c}')
        story = out['story']
        for name in spec['verifier'].get('mustAppearInText', []):
            val = params[name]
            cands = {fmt_value(val, 'dec', None, False)}
            if not _isint(val):
                cands.add(dec_plain(_num(val), 2).replace('.', ','))
            if not any(re.search(r'(?<![\d,])' + re.escape(c) + r'(?![\d,]|\d)', story) for c in cands):
                errs.append(f'{name}={val} not found in story (tried {sorted(cands)})')
        if errs:
            return None, errs
        env_t = dict(env, story=story)
        tt = spec['taskTemplate']
        task = {'id': f'{skill_id}/{spec["id"]}/{level}/{index}', 'skill': skill_id, 'level': level,
                'kind': tt['kind'], 'prompt': story}
        if 'input' in tt:
            task['input'] = tt['input']
        task['answer'] = to_value(spec['verifier']['answer'], env, ev)
        task['steps'] = [{'id': f's{i}', 'text': render(s, env_t, ev)} for i, s in enumerate(spec['verifier']['steps'], 1)]
        if 'estimatedSeconds' in tt:
            task['estimatedSeconds'] = tt['estimatedSeconds']
        if tt.get('tags'):
            task['tags'] = tt['tags']
        task['provenance'] = {'source': 'bank-llm', 'specId': spec['id'], 'verifiedBy': 'solver'}
        return task, []
    except (DslError, KeyError, ValueError, ZeroDivisionError) as e:
        return None, [f'{type(e).__name__}: {e}']


# ----------------------------------------------------------------------------- lint / pack
def load(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8'))


def schema_registry(root):
    from referencing import Registry, Resource
    reg = Registry()
    for f in (root / 'schemas').glob('*.schema.json'):
        s = json.loads(f.read_text(encoding='utf-8'))
        reg = reg.with_resource(s['$id'], Resource.from_contents(s))
        reg = reg.with_resource(f.name, Resource.from_contents(s))
    return reg


def validator(root, name):
    import jsonschema
    s = load(root / 'schemas' / f'{name}.schema.json')
    reg = schema_registry(root)
    return jsonschema.Draft202012Validator(s, registry=reg, format_checker=None)


SEEDS = 200
SUPPLY = {}          # (skill id, level) -> distinct tasks seen in SEEDS seeds; filled by lint_generator / measure_supply
MIN_SUPPLY = 8       # a level that cannot yield 8 different tasks cannot carry even the smallest lesson (4 tasks, no repeats on replay)


def task_problems(t: dict) -> list[str]:
    """Structural / semantic checks every compiled task must pass (generated or from a bank)."""
    bad = []
    blob = json.dumps(t, ensure_ascii=False)
    if '@{' in blob or 'None' in blob or 'nan' in t['prompt'].lower().split():
        bad.append('unresolved template / None in task')
    if re.search(r'\d\.\d', t['prompt'].replace('\\ldots', '')) and 'http' not in t['prompt']:
        bad.append('decimal point instead of comma in prompt')
    if '  ' in t['prompt']:
        bad.append('double space in prompt')
    k, ans, opts = t['kind'], t['answer'], t.get('options', [])
    ids = [o['id'] for o in opts]
    if k in ('multiple-choice', 'multi-select', 'find-the-mistake'):
        if len(set(ids)) != len(ids) or len({o['text'] for o in opts}) != len(opts):
            bad.append('duplicate option ids or texts')
        if k == 'multiple-choice':
            good = [o['id'] for o in opts if o.get('correct')]
            if len(good) != 1 or ans.get('value') != good[0]:
                bad.append(f'choice answer {ans.get("value")} != correct options {good}')
        elif k == 'multi-select':
            good = sorted(o['id'] for o in opts if o.get('correct'))
            if sorted(ans.get('value', [])) != good or not good:
                bad.append('multi-select answer != correct options')
        elif ans.get('value') not in ids:
            bad.append('find-the-mistake answer is not an option')
    if k == 'order-items':
        items = [i['id'] for i in t.get('input', {}).get('items', [])]
        if sorted(ans.get('value', [])) != sorted(items) or len(set(items)) != len(items):
            bad.append('order-items answer is not a permutation of the items')
    if not t.get('steps'):
        bad.append('no steps')
    return bad


def lint_generator(g, ref, sid, lv, errors, notes, schema_check):
    prompts, tag = set(), f'{ref} L{lv}'
    lvspec = next((l for l in g['levels'] if l['level'] == lv), {})
    need = lvspec.get('minDistinct', g.get('minDistinct', 12))
    for seed in range(1, SEEDS + 1):
        try:
            t, env, ev = generate_env(g, sid, lv, seed)
            for chk in g.get('selfCheck', []):
                if not ev.eval(chk, env):
                    raise DslError(f'selfCheck failed: {chk}')
        except (DslError, KeyError, ValueError, ZeroDivisionError, IndexError, TypeError) as e:
            errors.append(f'{tag} seed {seed}: {type(e).__name__}: {e}')
            return
        for prob in task_problems(t):
            errors.append(f'{tag} seed {seed}: {prob}: {t["prompt"][:80]!r}')
            return
        if seed <= 3:
            schema_check(t, f'{tag} seed {seed}')
        for m in t.get('media', []):
            try:
                bad = figures.problems(figures.scene(m))
            except (KeyError, ValueError, TypeError, IndexError, ZeroDivisionError) as e:
                bad = [f'{type(e).__name__}: {e}']
            if bad:
                errors.append(f'{tag} seed {seed}: media {m["kind"]}: {bad[0]}')
                return
        prompts.add(t['prompt'] + json.dumps(t.get('media', ''), sort_keys=True) + json.dumps(t.get('input', ''), sort_keys=True)
                    + json.dumps([o['text'] for o in t.get('options', [])]))
    SUPPLY[(sid, lv)] = len(prompts)
    if len(prompts) < need:
        errors.append(f'{tag}: only {len(prompts)} distinct tasks in {SEEDS} seeds (minDistinct {need})')
    notes.append(f'{tag}: {SEEDS} seeds OK, {len(prompts)} distinct')


def lint_quest(q, ref, sid, errors, notes, schema_check):
    seen, tag = set(), ref
    for seed in range(1, 101):
        try:
            quest, env, ev = generate_quest(q, sid, seed)
            for chk in q.get('selfCheck', []):
                if not ev.eval(chk, env):
                    raise DslError(f'selfCheck failed: {chk}')
        except (DslError, KeyError, ValueError, ZeroDivisionError, IndexError, TypeError) as e:
            errors.append(f'{tag} seed {seed}: {type(e).__name__}: {e}')
            return
        if '@{' in json.dumps(quest, ensure_ascii=False) or 'None' in quest['intro']:
            errors.append(f'{tag} seed {seed}: unresolved template in the story')
            return
        for i, t in enumerate(quest['steps'], 1):
            for prob in task_problems(t):
                errors.append(f'{tag} seed {seed} step {i}: {prob}')
                return
            if seed <= 3:
                schema_check(t, f'{tag} seed {seed} step {i}')
        for m in quest.get('media', []) + [m for t in quest['steps'] for m in t.get('media', [])]:
            try:
                bad = figures.problems(figures.scene(m))
            except (KeyError, ValueError, TypeError, IndexError, ZeroDivisionError) as e:
                bad = [f'{type(e).__name__}: {e}']
            if bad:
                errors.append(f'{tag} seed {seed}: media {m["kind"]}: {bad[0]}')
                return
        seen.add(quest['intro'] + ''.join(t['prompt'] for t in quest['steps']) + json.dumps(quest.get('media', ''), sort_keys=True))
    SUPPLY[(sid, 1)] = len(seen)
    if len(seen) < q.get('minDistinct', 20):
        errors.append(f'{tag}: only {len(seen)} distinct quests in 100 seeds (minDistinct {q.get("minDistinct", 20)})')
    notes.append(f'{tag}: 100 seeds OK, {len(seen)} distinct')


def lint(pack: pathlib.Path):
    root = pathlib.Path(__file__).resolve().parent.parent
    errors, notes = [], []
    cur = load(pack / 'curriculum.json')
    objective_ids = {o['id'] for st in cur['stages'] for a in st['areas'] for o in a['objectives']}
    objective_ids |= {p['id'] for st in cur['stages'] for a in st['areas'] for o in a['objectives'] for p in o['parts']}
    area_ids = {a['id'] for st in cur['stages'] for a in st['areas']}
    vs = {n: validator(root, n) for n in ('skill', 'generator', 'task', 'llm-spec', 'course', 'path', 'quest')}

    def check(v, doc, where):
        for e in sorted(v.iter_errors(doc), key=lambda e: list(e.path)):
            errors.append(f'{where}: {"/".join(map(str, e.path))}: {e.message[:200]}')

    man = load(pack / 'course.json')
    check(vs['course'], man, 'course.json')
    listed = {x for st in man.get('stages', []) for x in st['skills']}
    on_disk = {str(f.relative_to(pack)) for f in (pack / 'skills').rglob('*.json')}
    for x in sorted(listed ^ on_disk):
        errors.append(f'course.json: skill file {x} is not listed in stages / not on disk')
    for f in man.get('files', []):
        fp = pack / f['path']
        if not fp.exists() or hashlib.sha256(fp.read_bytes()).hexdigest() != f['sha256']:
            errors.append(f'course.json: hash mismatch or missing file {f["path"]} (run `pack`)')

    skills = {}
    for sf in sorted((pack / 'skills').rglob('*.json')):
        s = load(sf)
        check(vs['skill'], s, sf.relative_to(pack))
        skills[s['id']] = (sf, s)
    for sid, (sf, s) in skills.items():
        w = str(sf.relative_to(pack))
        for o in s['objectives']:
            if o not in objective_ids:
                errors.append(f'{w}: unknown objective {o}')
        if s.get('area') and s['area'] not in area_ids:
            errors.append(f'{w}: unknown area {s["area"]}')
        for p in s.get('prerequisites', []):
            if p not in skills:
                errors.append(f'{w}: unknown prerequisite {p}')
        levels = {l['level'] for l in s['levels']}
        for src in s['taskSources']:
            ref = pack / src['ref']
            if not ref.exists():
                errors.append(f'{w}: missing file {src["ref"]}')
                continue
            if src['type'] == 'generator':
                g = load(ref)
                check(vs['generator'], g, src['ref'])
                for lv in src['levels']:
                    if lv not in levels:
                        errors.append(f'{w}: generator level {lv} not declared in skill levels')
                    lint_generator(g, src['ref'], sid, lv, errors, notes, lambda t, where: check(vs['task'], t, where))
            elif src['type'] == 'quest':
                q = load(ref)
                check(vs['quest'], q, src['ref'])
                lint_quest(q, src['ref'], sid, errors, notes, lambda t, where: check(vs['task'], t, where))
            elif src['type'] == 'bank':
                n = 0
                for i, line in enumerate(ref.read_text(encoding='utf-8').splitlines(), 1):
                    t = json.loads(line)
                    check(vs['task'], t, f'{src["ref"]}:{i}')
                    if t['skill'] != sid:
                        errors.append(f'{src["ref"]}:{i}: skill mismatch')
                    pv = t['provenance']
                    if pv['source'] == 'bank-llm' and pv.get('verifiedBy', 'none') == 'none':
                        errors.append(f'{src["ref"]}:{i}: LLM-written task without verification')
                    for prob in task_problems(t):
                        errors.append(f'{src["ref"]}:{i}: {prob}')
                    n += 1
                notes.append(f'{src["ref"]}: {n} tasks OK')
            elif src['type'] == 'llm':
                spec = load(ref)
                check(vs['llm-spec'], spec, src['ref'])
                if spec['skill'] != sid:
                    errors.append(f'{src["ref"]}: skill mismatch')
                for k, ex in enumerate(spec.get('examples', [])):
                    for lv in (1, 2):
                        task, errs = verify_llm_output(spec, sid, lv, ex, k)
                        if task:
                            check(vs['task'], task, f'{src["ref"]} example {k} L{lv}')
                        notes.append(f'{src["ref"]} example {k} at L{lv}: ' + ('verified -> ' + task['answer']['value'] + ' ' + task['answer'].get('unit', '') if task else 'rejected (' + '; '.join(errs) + ')'))
    lint_paths(pack, man, skills, errors, notes, lambda d, where: check(vs['path'], d, where))
    return errors, notes


def skill_level_supply(pack, skill) -> dict:
    """level -> number of distinct tasks known to exist (None = unbounded: generators / llm)."""
    supply = {}
    for src in skill['taskSources']:
        if src['type'] == 'generator':
            for lv in src['levels']:
                supply[lv] = None
        elif src['type'] == 'quest':
            supply[1] = None
        elif src['type'] == 'bank':
            f = pack / src['ref']
            if f.exists():
                for line in f.read_text(encoding='utf-8').splitlines():
                    lv = json.loads(line)['level']
                    if supply.get(lv, 0) is not None:
                        supply[lv] = supply.get(lv, 0) + 1
        else:
            for l in skill['levels']:
                supply[l['level']] = None
    return supply


def measure_supply(pack: pathlib.Path):
    """Fill SUPPLY for every generator level (same distinctness notion as the lint)."""
    for gf in sorted((pack / 'generators').glob('*.json')):
        g = load(gf)
        for L in g['levels']:
            seen = set()
            for seed in range(1, SEEDS + 1):
                try:
                    t = generate(g, g['id'], L['level'], seed)
                except (DslError, KeyError, ValueError, ZeroDivisionError, IndexError, TypeError):
                    continue
                seen.add(t['prompt'] + json.dumps(t.get('media', ''), sort_keys=True) + json.dumps(t.get('input', ''), sort_keys=True)
                         + json.dumps([o['text'] for o in t.get('options', [])]))
            SUPPLY[(g['id'], L['level'])] = len(seen)


def fit_paths(pack: pathlib.Path):
    """Lower a lesson's `tasks` to what its sources can supply without repeating a task: generator levels give
    `distinct // 2` (a replay still sees mostly new tasks), banks give all their tasks.  Never below 4 (schema)."""
    measure_supply(pack)
    skills = {}
    for sf in (pack / 'skills').rglob('*.json'):
        sk = load(sf)
        skills[sk['id']] = sk
    changed = 0
    for pf in sorted((pack / 'paths').glob('*.json')):
        path = load(pf)
        for unit in path['units']:
            for lesson in unit['lessons']:
                items = [(lesson['skill'], lv) for lv in lesson['levels']] if 'skill' in lesson else [(m['skill'], m.get('level', 1)) for m in lesson['mix']]
                allowed = []
                for sid, lv in items:
                    sup = skill_level_supply(pack, skills[sid]).get(lv)
                    cap = sup if sup is not None else SUPPLY.get((sid, lv), 10 ** 6) // 2
                    allowed.append(cap)
                cap = min(allowed)
                if lesson['kind'] == 'quest':
                    continue
                if 'mix' in lesson:
                    cap *= len(lesson['mix'])
                new = max(4, min(lesson.get('tasks', 10), cap))
                if new != lesson.get('tasks', 10):
                    lesson['tasks'] = new
                    changed += 1
        pf.write_text(json.dumps(path, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'fit: lowered the task count of {changed} lessons')


def lint_paths(pack, man, skills, errors, notes, schema_check):
    used = set()
    for st in man.get('stages', []):
        if not st['skills'] and not st.get('path'):
            continue
        pf = st.get('path')
        if not pf or not (pack / pf).exists():
            errors.append(f'course.json: stage {st["id"]} has skills but no path file')
            continue
        path = load(pack / pf)
        schema_check(path, pf)
        if path['stage'] != st['id']:
            errors.append(f'{pf}: stage {path["stage"]} != {st["id"]}')
        seen, order = {}, []
        n_lessons = 0
        for ui, unit in enumerate(path['units']):
            for lesson in unit['lessons']:
                n_lessons += 1
                lid, where = lesson['id'], f'{pf}:{lesson["id"]}'
                if lid in seen:
                    errors.append(f'{where}: duplicate lesson id')
                for r in lesson.get('requires', []):
                    if r not in seen:
                        errors.append(f'{where}: requires {r}, which is not an earlier lesson')
                if not order and lesson.get('requires'):
                    errors.append(f'{where}: the first lesson of a stage must be open (no requires)')
                items = [{'skill': lesson['skill'], 'level': lv} for lv in lesson['levels']] if 'skill' in lesson else None
                if ('skill' in lesson) == ('mix' in lesson):
                    errors.append(f'{where}: exactly one of skill / mix')
                    continue
                if lesson['kind'] in ('learn', 'practice') and 'skill' not in lesson:
                    errors.append(f'{where}: {lesson["kind"]} lessons train one skill')
                if lesson['kind'] in ('review', 'checkpoint') and 'mix' not in lesson:
                    errors.append(f'{where}: {lesson["kind"]} lessons mix skills')
                items = items or [{'skill': m['skill'], 'level': m.get('level', 1)} for m in lesson['mix']]
                for it in items:
                    sk = skills.get(it['skill'])
                    if not sk:
                        errors.append(f'{where}: unknown skill {it["skill"]}')
                        continue
                    sk = sk[1]
                    if sk['stage'] != path['stage']:
                        errors.append(f'{where}: skill {it["skill"]} belongs to stage {sk["stage"]}')
                    used.add(it['skill'])
                    if lesson['kind'] == 'learn' and not sk.get('tutor', {}).get('intro'):
                        errors.append(f'{where}: learn lesson of {it["skill"]} needs tutor.intro (shown before the first task)')
                    supply = skill_level_supply(pack, sk)
                    if it['level'] not in supply:
                        errors.append(f'{where}: skill {it["skill"]} has no tasks at level {it["level"]}')
                    elif supply[it['level']] is not None and supply[it['level']] < lesson.get('tasks', 10):
                        errors.append(f'{where}: only {supply[it["level"]]} bank tasks at level {it["level"]} for a {lesson.get("tasks", 10)}-task lesson')
                    elif supply[it['level']] is None and lesson['kind'] != 'quest':
                        got = SUPPLY.get((it['skill'], it['level']))
                        share = lesson.get('tasks', 10) if 'skill' in lesson else -(-lesson.get('tasks', 10) // len(lesson['mix']))
                        if got is not None and (got < MIN_SUPPLY or got < 2 * share):
                            errors.append(f'{where}: {it["skill"]} L{it["level"]} yields only {got} distinct tasks, too few for {share} tasks per lesson (need >= {max(MIN_SUPPLY, 2 * share)}); '
                                          'widen the generator or run `cognio.py fit`')
                seen[lid] = unit['id']
                order.append(lid)
        notes.append(f'{pf}: {len(path["units"])} units, {n_lessons} lessons, entry={path["entry"]}')
    for sid, (sf, sk) in skills.items():
        if sid not in used:
            errors.append(f'{sf.relative_to(pack)}: skill {sid} is not in any lesson (unreachable)')


def pack_cmd(pack: pathlib.Path, out: pathlib.Path):
    man_path = pack / 'course.json'
    man = load(man_path)
    files = []
    for f in sorted(pack.rglob('*')):
        if f.is_file() and f.name != 'course.json' and not f.name.endswith('.cognio'):
            b = f.read_bytes()
            files.append({'path': str(f.relative_to(pack)), 'sha256': hashlib.sha256(b).hexdigest(), 'size': len(b)})
    man['files'] = files
    man_path.write_text(json.dumps(man, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.write(man_path, 'course.json')
        for f in files:
            z.write(pack / f['path'], f['path'])
    print(f'{out}: {len(files)} files')


def main(argv):
    if len(argv) < 3:
        print(__doc__)
        return 2
    cmd, pack = argv[1], pathlib.Path(argv[2])
    if cmd == 'lint':
        errs, notes = lint(pack)
        for n in notes:
            print('ok  ', n)
        for e in errs:
            print('FAIL', e)
        print(f'{len(errs)} error(s)')
        return 1 if errs else 0
    if cmd == 'gen':
        gen = load(pack / 'generators' / f'{argv[3]}.json')
        print(json.dumps(generate(gen, argv[3], int(argv[4]), int(argv[5])), ensure_ascii=False, indent=1))
        return 0
    if cmd == 'vectors':
        vec = []
        for gf in sorted((pack / 'generators').glob('*.json')):
            g = load(gf)
            for lv in g['levels']:
                for seed in (1, 2, 3, 42, 2026, 18446744073709551615):
                    vec.append({'generator': g['id'], 'level': lv['level'], 'seed': str(seed),
                                'task': generate(g, g['id'], lv['level'], seed)})
        pathlib.Path(argv[3]).write_text(json.dumps({'prng': 'splitmix64', 'vectors': vec}, ensure_ascii=False, indent=1), encoding='utf-8')
        print(f'{len(vec)} vectors')
        return 0
    if cmd == 'sample':       # sample <pack> <skill|all> [n=2]  - human-readable review of generated tasks
        n = int(argv[4]) if len(argv) > 4 else 2
        for sf in sorted((pack / 'skills').rglob('*.json')):
            sk = load(sf)
            if argv[3] not in ('all', sk['id']):
                continue
            for src in sk['taskSources']:
                if src['type'] != 'generator':
                    continue
                g = load(pack / src['ref'])
                for lv in src['levels']:
                    for seed in range(7, 7 + n):
                        t = generate(g, sk['id'], lv, seed * 13)
                        print(f"[{sk['id']} L{lv}] {t['prompt']}")
                        if t.get('options'):
                            print('    ' + ' | '.join(('*' if o.get('correct') else ' ') + o['text'] for o in t['options']))
                        if t.get('input', {}).get('items'):
                            print('    items: ' + ', '.join(i['text'] for i in t['input']['items']))
                        print(f"    => {json.dumps(t['answer'], ensure_ascii=False)}   | " + ' / '.join(x['text'] for x in t['steps'])[:170])
                        for r in t.get('errorRules', []):
                            print(f"       bug {r['id']}: {json.dumps(r['answer'], ensure_ascii=False)}")
        return 0
    if cmd == 'coverage':
        cur = load(pack / 'curriculum.json')
        used = {o.rsplit('.', 1)[0] if re.search(r'\.[a-z]$', o) and o.count('.') == 3 else o
                for sf in (pack / 'skills').rglob('*.json') for o in load(sf)['objectives']}
        used |= {o for sf in (pack / 'skills').rglob('*.json') for o in load(sf)['objectives']}
        for st in cur['stages']:
            tot = sum(len(a['objectives']) for a in st['areas'])
            cov = sum(1 for a in st['areas'] for o in a['objectives'] if o['id'] in used or any(p['id'] in used for p in o['parts']))
            print(f"{st['id']:9} {cov:3}/{tot:<3} objectives have a skill")
            for a in st['areas']:
                n = sum(1 for o in a['objectives'] if o['id'] in used or any(p['id'] in used for p in o['parts']))
                print(f"   {a['id']:10} {a['name']:28} {n}/{len(a['objectives'])}")
        return 0
    if cmd == 'scenes':      # scenes <pack> <out.json>  - media -> scene conformance cases for a renderer port
        cases, seen = [], set()

        def add(where, m):
            key = json.dumps(m, sort_keys=True, ensure_ascii=False)
            if key not in seen:
                seen.add(key)
                cases.append({'where': where, 'media': m, 'scene': figures.scene(m)})
        for gf in sorted((pack / 'generators').glob('*.json')):
            g = load(gf)
            for lv in g['levels']:
                for seed in (1, 2, 3):
                    for m in generate(g, g['id'], lv['level'], seed).get('media', []):
                        add(f"{g['id']} L{lv['level']} seed {seed}", m)
        for qf in sorted((pack / 'quests').glob('*.json')):
            q = load(qf)
            for seed in (1, 2):
                quest, _, _ = generate_quest(q, q['id'], seed)
                for m in quest.get('media', []) + [m for t in quest['steps'] for m in t.get('media', [])]:
                    add(f"{q['id']} seed {seed}", m)
        for i, m in enumerate(json.loads((pathlib.Path(__file__).resolve().parent.parent / 'tests/conformance/media-extra.json').read_text(encoding='utf-8'))):
            add(f'media-extra #{i}', m)
        pathlib.Path(argv[3]).write_text(json.dumps({'note': 'media -> scene, generated by tools/cognio.py scenes', 'cases': cases}, ensure_ascii=False), encoding='utf-8')
        print(f'{len(cases)} scenes')
        return 0
    if cmd == 'quest':       # quest <pack> <id> [seed=1]  - print one quest instance
        q = load(pack / 'quests' / f'{argv[3]}.json')
        quest, _, _ = generate_quest(q, argv[3], int(argv[4]) if len(argv) > 4 else 1)
        print(f"== {quest['title']}\n{quest['intro']}")
        for m in quest.get('media', []):
            print('   [media]', m['kind'], json.dumps(m['params'], ensure_ascii=False)[:200])
        for i, t in enumerate(quest['steps'], 1):
            print(f"{i}. {t['prompt']}")
            if t.get('options'):
                print('    ' + ' | '.join(('*' if o.get('correct') else ' ') + o['text'] for o in t['options']))
            print(f"    => {json.dumps(t['answer'], ensure_ascii=False)}   | " + ' / '.join(x['text'] for x in t['steps'])[:150])
        print(quest.get('outro', ''))
        return 0
    if cmd == 'fit':
        fit_paths(pack)
        return 0
    if cmd == 'pack':
        pack_cmd(pack, pathlib.Path(argv[3]))
        return 0
    print(__doc__)
    return 2


if __name__ == '__main__':
    sys.exit(main(sys.argv))
