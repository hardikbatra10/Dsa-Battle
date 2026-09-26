"""Math problems."""

def _solve_reverse_integer(lines):
    x = int(lines[0])
    sign = -1 if x < 0 else 1
    reversed_num = sign * int(str(abs(x))[::-1])
    if reversed_num < -2**31 or reversed_num > 2**31 - 1:
        return "0"
    return str(reversed_num)


def _solve_pow(lines):
    x = int(lines[0])
    n = int(lines[1])
    return str(x ** n)


def _solve_int_to_roman(lines):
    num = int(lines[0])
    vals = [
        (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
        (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
        (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
    ]
    res = []
    for v, sym in vals:
        while num >= v:
            res.append(sym)
            num -= v
    return "".join(res)

def _solve_palindrome_number(lines):
    x = int(lines[0])
    if x < 0:
        return "false"
    s = str(x)
    return "true" if s == s[::-1] else "false"


def _solve_fizz_buzz(lines):
    n = int(lines[0])
    out = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            out.append("FizzBuzz")
        elif i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        else:
            out.append(str(i))
    return "\n".join(out)


def _solve_happy_number(lines):
    n = int(lines[0])
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(c) ** 2 for c in str(n))
    return "true" if n == 1 else "false"


def _solve_excel_column_title(lines):
    n = int(lines[0])
    out = []
    while n > 0:
        n, rem = divmod(n - 1, 26)
        out.append(chr(ord("A") + rem))
    return "".join(reversed(out))


def _solve_plus_one(lines):
    digits = list(map(int, lines[0].split()))
    i = len(digits) - 1
    while i >= 0:
        if digits[i] < 9:
            digits[i] += 1
            return " ".join(map(str, digits))
        digits[i] = 0
        i -= 1
    return " ".join(map(str, [1] + digits))


def _solve_count_primes(lines):
    n = int(lines[0])
    if n < 3:
        return "0"
    sieve = [True] * n
    sieve[0] = sieve[1] = False
    i = 2
    while i * i < n:
        if sieve[i]:
            for j in range(i * i, n, i):
                sieve[j] = False
        i += 1
    return str(sum(sieve))


def _solve_roman_to_integer(lines):
    s = lines[0]
    vals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    for i, c in enumerate(s):
        if i + 1 < len(s) and vals[c] < vals[s[i + 1]]:
            total -= vals[c]
        else:
            total += vals[c]
    return str(total)


def _solve_integer_sqrt(lines):
    x = int(lines[0])
    lo, hi = 0, x
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            lo = mid + 1
        else:
            hi = mid - 1
    return str(hi)


def _solve_factorial_trailing_zeroes(lines):
    n = int(lines[0])
    count = 0
    power = 5
    while power <= n:
        count += n // power
        power *= 5
    return str(count)


def _solve_fraction_to_decimal(lines):
    num = int(lines[0])
    den = int(lines[1])
    if num == 0:
        return "0"
    sign = "-" if (num < 0) != (den < 0) else ""
    num, den = abs(num), abs(den)
    whole, rem = divmod(num, den)
    if rem == 0:
        return sign + str(whole)
    seen = {}
    frac = []
    while rem and rem not in seen:
        seen[rem] = len(frac)
        rem *= 10
        digit, rem = divmod(rem, den)
        frac.append(str(digit))
    if rem:
        idx = seen[rem]
        frac.insert(idx, "(")
        frac.append(")")
    return sign + str(whole) + "." + "".join(frac)


def _solve_basic_calculator(lines):
    s = lines[0]
    total = 0
    sign = 1
    num = 0
    stack = []
    for c in s:
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in "+-":
            total += sign * num
            num = 0
            sign = 1 if c == "+" else -1
        elif c == "(":
            stack.append(total)
            stack.append(sign)
            total = 0
            sign = 1
        elif c == ")":
            total += sign * num
            num = 0
            total *= stack.pop()
            total += stack.pop()
            sign = 1
    return str(total + sign * num)

def _solve_add_digits(lines):
    n = int(lines[0])
    while n >= 10:
        n = sum(int(c) for c in str(n))
    return str(n)


def _solve_ugly_number(lines):
    n = int(lines[0])
    if n <= 0:
        return "false"
    for p in (2, 3, 5):
        while n % p == 0:
            n //= p
    return "true" if n == 1 else "false"


def _solve_excel_column_number(lines):
    title = lines[0]
    total = 0
    for c in title:
        total = total * 26 + (ord(c) - 64)
    return str(total)


def _solve_self_dividing_numbers(lines):
    left, right = map(int, lines[0].split())
    out = []
    for v in range(left, right + 1):
        digits = str(v)
        if "0" in digits:
            continue
        if all(v % int(d) == 0 for d in digits):
            out.append(str(v))
    return " ".join(out)


def _solve_ugly_number_ii(lines):
    n = int(lines[0])
    ugly = [1]
    i2 = i3 = i5 = 0
    while len(ugly) < n:
        nxt = min(ugly[i2] * 2, ugly[i3] * 3, ugly[i5] * 5)
        ugly.append(nxt)
        if nxt == ugly[i2] * 2:
            i2 += 1
        if nxt == ugly[i3] * 3:
            i3 += 1
        if nxt == ugly[i5] * 5:
            i5 += 1
    return str(ugly[n - 1])


def _solve_rotate_function(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    total = sum(nums)
    current = sum(i * v for i, v in enumerate(nums))
    best = current
    for k in range(1, n):
        current += total - n * nums[n - k]
        best = max(best, current)
    return str(best)


def _solve_nth_digit(lines):
    n = int(lines[0])
    length = 1
    count = 9
    start = 1
    while n > length * count:
        n -= length * count
        length += 1
        count *= 10
        start *= 10
    number = start + (n - 1) // length
    return str(number)[(n - 1) % length]


def _solve_bulb_switcher(lines):
    n = int(lines[0])
    root = 0
    while (root + 1) * (root + 1) <= n:
        root += 1
    return str(root)


def _solve_super_pow(lines):
    a = int(lines[0])
    b = [int(c) for c in lines[1].split()]
    result = 1
    for digit in b:
        result = pow(result, 10, 1337) * pow(a, digit, 1337) % 1337
    return str(result)


def _solve_integer_break(lines):
    n = int(lines[0])
    dp = [0] * (n + 1)
    for i in range(2, n + 1):
        for j in range(1, i):
            dp[i] = max(dp[i], j * (i - j), j * dp[i - j])
    return str(dp[n])


def _solve_number_of_digit_one(lines):
    n = int(lines[0])
    count = 0
    power = 1
    while power <= n:
        high = n // (power * 10)
        current = (n // power) % 10
        low = n % power
        if current == 0:
            count += high * power
        elif current == 1:
            count += high * power + low + 1
        else:
            count += (high + 1) * power
        power *= 10
    return str(count)


def _solve_simplified_fractions(lines):
    n = int(lines[0])

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    out = []
    for den in range(2, n + 1):
        for num in range(1, den):
            if gcd(num, den) == 1:
                out.append((num, den))
    out.sort()
    return " ".join(f"{a}/{b}" for a, b in out)


def _solve_super_ugly_number(lines):
    n = int(lines[0])
    primes = list(map(int, lines[1].split()))
    ugly = [1]
    idx = [0] * len(primes)
    while len(ugly) < n:
        candidates = [ugly[idx[i]] * primes[i] for i in range(len(primes))]
        nxt = min(candidates)
        ugly.append(nxt)
        for i in range(len(primes)):
            if candidates[i] == nxt:
                idx[i] += 1
    return str(ugly[n - 1])


def _solve_reach_a_number(lines):
    target = abs(int(lines[0]))
    step = 0
    total = 0
    while total < target or (total - target) % 2:
        step += 1
        total += step
    return str(step)


def _solve_count_of_range_sum(lines):
    nums = list(map(int, lines[0].split()))
    lower, upper = map(int, lines[1].split())
    prefix = [0]
    for v in nums:
        prefix.append(prefix[-1] + v)
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums) + 1):
            if lower <= prefix[j] - prefix[i] <= upper:
                count += 1
    return str(count)


def _solve_nth_magical_number(lines):
    n, a, b = map(int, lines[0].split())
    MOD = 10 ** 9 + 7

    def gcd(x, y):
        while y:
            x, y = y, x % y
        return x

    lcm = a // gcd(a, b) * b
    lo, hi = 1, n * min(a, b)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid // a + mid // b - mid // lcm >= n:
            hi = mid
        else:
            lo = mid + 1
    return str(lo % MOD)


def _solve_preimage_factorial_zeroes(lines):
    k = int(lines[0])

    def zeroes(x):
        total = 0
        power = 5
        while power <= x:
            total += x // power
            power *= 5
        return total

    lo, hi = 0, 5 * (k + 1)
    while lo < hi:
        mid = (lo + hi) // 2
        if zeroes(mid) >= k:
            hi = mid
        else:
            lo = mid + 1
    return "5" if zeroes(lo) == k else "0"


def _solve_smallest_good_base(lines):
    n = int(lines[0])
    for length in range(len(bin(n)) - 2, 1, -1):
        base = int(n ** (1.0 / (length - 1)))
        for candidate in (base, base + 1):
            if candidate < 2:
                continue
            total = 0
            for _ in range(length):
                total = total * candidate + 1
            if total == n:
                return str(candidate)
    return str(n - 1)


def _solve_consecutive_numbers_sum(lines):
    n = int(lines[0])
    count = 0
    k = 1
    while k * (k + 1) // 2 <= n:
        rest = n - k * (k + 1) // 2
        if rest % k == 0:
            count += 1
        k += 1
    return str(count)


PROBLEMS = [
{
        "title": "Reverse Integer",
        "topic": "math",
        "difficulty": "easy",
        "description": "Given a signed 32-bit integer x, return x with its digits reversed. If reversing causes it to go outside the signed 32-bit range, return 0.",
        "example_input": "123",
        "constraints": "Input format: one line containing the integer. Output format: a single integer.",
        "solve": _solve_reverse_integer,
        "sample_inputs": ["123", "1200"],
        "hidden_inputs": [
            "0",
            "1",
            "-1",
            "10",           # trailing zero disappears
            "-10",
            "100",
            "120",
            "-120",         # negative with a trailing zero
            "-123",
            "1463847412",   # reverses to exactly 2147483641, just inside range
            "1534236469",   # overflows, so 0
            "2147483647",   # 32-bit max, overflows when reversed
            "-2147483648",  # 32-bit min, overflows when reversed
        ],
    },
{
        "title": "Pow(x, n)",
        "topic": "math",
        "difficulty": "medium",
        "description": "Given an integer x and a non-negative integer n, compute x raised to the power n.",
        "example_input": "2\n10",
        "constraints": "Input format: line 1 is x, line 2 is n (n >= 0). Output format: a single integer.",
        "solve": _solve_pow,
        "sample_inputs": ["2\n10", "3\n4"],
        "hidden_inputs": [
            "0\n0",      # zero to the zero is 1
            "1\n0",
            "2\n0",
            "3\n0",
            "10\n0",
            "0\n5",      # zero base
            "1\n1000",   # one base, large exponent
            "-1\n999",   # odd exponent keeps the sign
            "-1\n1000",  # even exponent drops the sign
            "-2\n3",
            "-2\n10",
            "5\n3",
            "2\n30",     # largest power of two inside signed 32-bit
        ],
    },
{
        "title": "Integer to Roman",
        "topic": "math",
        "difficulty": "hard",
        "description": "Given an integer in the range 1 to 3999, convert it to a Roman numeral.",
        "example_input": "1994",
        "constraints": "Input format: one line containing the integer. Output format: the Roman numeral string.",
        "solve": _solve_int_to_roman,
        "sample_inputs": ["1994", "2718"],
        "hidden_inputs": [
            "1",     # smallest input
            "3",
            "4",     # subtractive form
            "9",
            "14",
            "40",
            "44",
            "58",
            "90",
            "400",
            "900",
            "1000",
            "2024",
            "3888",  # longest numeral in the valid range
            "3999",  # largest input
        ],
    },
{
        "title": "Palindrome Number",
        "topic": "math",
        "difficulty": "easy",
        "description": "Decide whether an integer reads the same forwards and backwards. Negative numbers never do, because of the minus sign.",
        "example_input": "121",
        "constraints": "Input format: one line containing the integer. Output format: \"true\" or \"false\".",
        "solve": _solve_palindrome_number,
        "sample_inputs": ["121", "-121"],
        "hidden_inputs": [
            "0",                    # zero reads the same
            "1",                    # any single digit
            "9",
            "-1",                   # the minus sign spoils it
            "10",                   # a trailing zero cannot be a leading one
            "11",
            "12",
            "1221",                 # even length
            "12321",                # odd length
            "1000000001",
        ],
    },
{
        "title": "Fizz Buzz",
        "topic": "math",
        "difficulty": "easy",
        "description": "Count from one up to n, one entry per line. Write Fizz in place of any multiple of three, Buzz in place of any multiple of five, and FizzBuzz where a number is a multiple of both.",
        "example_input": "15",
        "constraints": "Input format: one line containing n (n >= 1). Output format: n lines.",
        "solve": _solve_fizz_buzz,
        "sample_inputs": ["15", "3"],
        "hidden_inputs": [
            "1",                    # before any rule applies
            "2",
            "4",
            "5",                    # the first Buzz
            "6",
            "9",
            "10",
            "14",                   # stops one short of FizzBuzz
            "16",                   # one past it
            "30",                   # two FizzBuzz entries
        ],
    },
{
        "title": "Happy Number",
        "topic": "math",
        "difficulty": "easy",
        "description": "Repeatedly replace a number by the sum of the squares of its digits. A number is happy if this eventually reaches one; otherwise it falls into a loop that never does. Decide whether the given number is happy.",
        "example_input": "19",
        "constraints": "Input format: one line containing a positive integer. Output format: \"true\" or \"false\".",
        "solve": _solve_happy_number,
        "sample_inputs": ["19", "2"],
        "hidden_inputs": [
            "1",                    # already there
            "7",                    # a longer happy chain
            "10",
            "4",                    # the head of the unhappy cycle
            "3",
            "13",
            "23",
            "68",
            "100",
            "986543210",            # a large starting point
        ],
    },
{
        "title": "Excel Sheet Column Title",
        "topic": "math",
        "difficulty": "easy",
        "description": "Columns in a spreadsheet are labelled A to Z, then AA to AZ, then BA onwards. Given a column's position counting from one, return its label.",
        "example_input": "28",
        "constraints": "Input format: one line containing the position (at least 1). Output format: the column label in capitals.",
        "solve": _solve_excel_column_title,
        "sample_inputs": ["28", "1"],
        "hidden_inputs": [
            "2",
            "25",
            "26",                   # the last single letter
            "27",                   # the first pair
            "52",                   # the end of the AZ run
            "53",
            "676",                  # the last two-letter label
            "702",
            "703",                  # the first three-letter label
            "2147483647",           # the 32-bit maximum
        ],
    },
{
        "title": "Plus One",
        "topic": "math",
        "difficulty": "easy",
        "description": "A number is given as its digits, most significant first. Add one to it and return the digits of the result.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line of space-separated digits with no leading zeros unless the number is zero itself. Output format: the resulting digits, space-separated.",
        "solve": _solve_plus_one,
        "sample_inputs": ["1 2 3", "4 3 2 1"],
        "hidden_inputs": [
            "0",                    # zero becomes one
            "1",
            "8",
            "9",                    # a new digit appears
            "1 9",                  # one carry
            "9 9",                  # two carries and a new digit
            "9 9 9",
            "1 0 0",
            "2 9 9 9",              # the carry stops partway
            "9 8 7 6 5 4 3 2 1 0",
        ],
    },
{
        "title": "Count Primes",
        "topic": "math",
        "difficulty": "medium",
        "description": "Count the prime numbers strictly below n. A prime has exactly two distinct whole divisors, one and itself.",
        "example_input": "10",
        "constraints": "Input format: one line containing n (n >= 0). Output format: a single integer.",
        "solve": _solve_count_primes,
        "sample_inputs": ["10", "0"],
        "hidden_inputs": [
            "1",                    # nothing below one
            "2",                    # two itself is excluded
            "3",                    # only two counts
            "4",
            "5",
            "11",                   # the bound is itself prime
            "12",
            "100",
            "1000",
            "100000",               # large enough to need a sieve
        ],
    },
{
        "title": "Roman to Integer",
        "topic": "math",
        "difficulty": "medium",
        "description": "Convert a Roman numeral to an ordinary number. A smaller symbol placed before a larger one is subtracted rather than added.",
        "example_input": "MCMXCIV",
        "constraints": "Input format: one line containing a valid Roman numeral between 1 and 3999. Output format: a single integer.",
        "solve": _solve_roman_to_integer,
        "sample_inputs": ["MCMXCIV", "LVIII"],
        "hidden_inputs": [
            "I",                    # the smallest numeral
            "III",
            "IV",                   # the first subtractive form
            "IX",
            "XL",
            "XC",
            "CD",
            "CM",
            "MMXXIV",
            "MMMCMXCIX",            # the largest valid numeral
        ],
    },
{
        "title": "Integer Square Root",
        "topic": "math",
        "difficulty": "medium",
        "description": "Return the whole part of the square root of a non-negative integer, without using any built-in square-root function.",
        "example_input": "8",
        "constraints": "Input format: one line containing the integer (at least 0). Output format: a single integer.",
        "solve": _solve_integer_sqrt,
        "sample_inputs": ["8", "4"],
        "hidden_inputs": [
            "0",                    # the root of zero
            "1",
            "2",                    # rounds down to one
            "3",
            "9",                    # an exact square
            "15",                   # one below a square
            "16",
            "17",                   # one above a square
            "2147395600",           # an exact square near the 32-bit limit
            "2147483647",           # the 32-bit maximum itself
        ],
    },
{
        "title": "Factorial Trailing Zeroes",
        "topic": "math",
        "difficulty": "medium",
        "description": "Return how many zeroes sit at the end of the product of every whole number from one up to n.",
        "example_input": "5",
        "constraints": "Input format: one line containing n (n >= 0). Output format: a single integer.",
        "solve": _solve_factorial_trailing_zeroes,
        "sample_inputs": ["5", "3"],
        "hidden_inputs": [
            "0",                    # an empty product
            "1",
            "4",                    # just below the first zero
            "9",
            "10",                   # two zeroes
            "24",                   # just below a jump
            "25",                   # 25 contributes two fives at once
            "26",
            "100",
            "1000",
        ],
    },
{
        "title": "Fraction to Recurring Decimal",
        "topic": "math",
        "difficulty": "hard",
        "description": "Write a fraction as a decimal. If the digits after the point eventually repeat forever, enclose the repeating part in brackets.",
        "example_input": "4\n333",
        "constraints": "Input format: line 1 is the numerator, line 2 is the denominator, which is never zero. Output format: the decimal, with any repeating run in brackets.",
        "solve": _solve_fraction_to_decimal,
        "sample_inputs": ["4\n333", "1\n2"],
        "hidden_inputs": [
            "0\n5",                 # zero has no sign and no point
            "1\n1",                 # a whole number
            "4\n2",                 # divides exactly
            "1\n3",                 # repeats from the first digit
            "2\n3",
            "1\n6",                 # one fixed digit, then a repeat
            "1\n7",                 # a six-digit repeating run
            "-1\n2",                # a negative numerator
            "1\n-2",                # a negative denominator
            "-50\n8",               # negative and terminating
        ],
    },
{
        "title": "Basic Calculator",
        "topic": "math",
        "difficulty": "hard",
        "description": "Work out the value of an expression made of whole numbers, addition, subtraction, brackets and spaces. A minus sign may also be used to negate whatever follows it.",
        "example_input": "(1+(4+5+2)-3)+(6+8)",
        "constraints": "Input format: one line containing the expression, with no leading or trailing spaces. Output format: a single integer.",
        "solve": _solve_basic_calculator,
        "sample_inputs": ["(1+(4+5+2)-3)+(6+8)", "1 + 1"],
        "hidden_inputs": [
            "0",                    # a lone number
            "42",
            "1+1",                  # no spaces at all
            "2-1",
            "1-2",                  # a negative result
            "-1+2",                 # a leading minus
            "(1)",                  # redundant brackets
            "((3))",
            "2-(5-6)",              # a minus applied to a bracket
            " 2-1 + 2".strip(),
            "(7)-(0)+(4)",
        ],
    },
{
        "title": "Add Digits",
        "topic": "math", "difficulty": "easy",
        "description": "Repeatedly replace a number by the total of its digits until only one digit is left, and return that digit.",
        "example_input": "38",
        "constraints": "Input format: one line containing a non-negative integer. Output format: a single digit.",
        "solve": _solve_add_digits,
        "sample_inputs": ["38", "0"],
        "hidden_inputs": [
            "1",                    # already a single digit
            "9",
            "10",                   # one round
            "19",
            "99",                   # two rounds
            "100",
            "123",
            "999",
            "1000000",
            "2147483647",
        ],
    },
{
        "title": "Ugly Number",
        "topic": "math", "difficulty": "easy",
        "description": "A number is ugly when its only prime divisors are two, three and five. Decide whether the given number is ugly.",
        "example_input": "6",
        "constraints": "Input format: one line containing an integer, which may be zero or negative. Output format: \"true\" or \"false\".",
        "solve": _solve_ugly_number,
        "sample_inputs": ["6", "14"],
        "hidden_inputs": [
            "1",                    # no prime divisors at all
            "0",                    # zero is not ugly
            "-6",                   # negatives never are
            "2",
            "7",                    # a forbidden prime
            "8",
            "30",
            "49",
            "1024",
            "1200",
        ],
    },
{
        "title": "Excel Sheet Column Number",
        "topic": "math", "difficulty": "easy",
        "description": "Columns in a spreadsheet are labelled A to Z, then AA to AZ, then BA onwards. Given a label, return its position counting from one.",
        "example_input": "AB",
        "constraints": "Input format: one line containing the label in capitals. Output format: a single integer.",
        "solve": _solve_excel_column_number,
        "sample_inputs": ["AB", "A"],
        "hidden_inputs": [
            "B",
            "Z",                    # the last single letter
            "AA",                   # the first pair
            "AZ",
            "BA",
            "ZY",
            "ZZ",                   # the last two-letter label
            "AAA",                  # the first three-letter label
            "FXSHRXW",
            "AAB",
        ],
    },
{
        "title": "Self Dividing Numbers",
        "topic": "math", "difficulty": "easy",
        "description": "A number is self dividing when it can be divided exactly by each of its own digits. A number containing a zero never qualifies. List the self dividing numbers in the given range, both ends included.",
        "example_input": "1 22",
        "constraints": "Input format: one line holding the low and high bounds. Output format: the qualifying numbers, space-separated (empty if none).",
        "solve": _solve_self_dividing_numbers,
        "sample_inputs": ["1 22", "47 85"],
        "hidden_inputs": [
            "1 1",                  # a single qualifying number
            "10 10",                # a zero digit disqualifies it
            "1 9",                  # every single digit qualifies
            "11 11",
            "12 12",
            "13 13",                # thirteen is not divisible by three
            "20 30",
            "100 110",
            "128 128",
            "99 101",
        ],
    },
{
        "title": "Ugly Number II",
        "topic": "math", "difficulty": "medium",
        "description": "Ugly numbers have no prime divisors other than two, three and five, and one counts as ugly. Return the nth ugly number, counting from one.",
        "example_input": "10",
        "constraints": "Input format: one line containing n (at least 1). Output format: a single integer.",
        "solve": _solve_ugly_number_ii,
        "sample_inputs": ["10", "1"],
        "hidden_inputs": [
            "2",
            "3",
            "4",
            "5",
            "7",                    # the first gap in the sequence
            "11",
            "20",
            "50",
            "100",
            "150",
        ],
    },
{
        "title": "Rotate Function",
        "topic": "math", "difficulty": "medium",
        "description": "For each way of rotating the list, add up every value multiplied by its position counting from zero. Return the largest such total.",
        "example_input": "4 3 2 6",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_rotate_function,
        "sample_inputs": ["4 3 2 6", "100"],
        "hidden_inputs": [
            "1",                    # one rotation only
            "0",
            "1 2",
            "2 1",
            "1 1 1",                # every rotation identical
            "0 0 0",
            "-1 -2 -3",             # negatives
            "1 2 3 4",
            "4 3 2 1",
            "1 100 1 1",
        ],
    },
{
        "title": "Nth Digit",
        "topic": "math", "difficulty": "medium",
        "description": "Write out the whole numbers one after another as a single endless run of digits. Return the digit at the given position, counting from one.",
        "example_input": "11",
        "constraints": "Input format: one line containing the position (at least 1). Output format: a single digit.",
        "solve": _solve_nth_digit,
        "sample_inputs": ["11", "3"],
        "hidden_inputs": [
            "1",                    # the very first digit
            "9",                    # the last single-digit number
            "10",                   # the first digit of ten
            "12",
            "15",
            "189",                  # the last two-digit number
            "190",                  # the first three-digit number
            "1000",
            "2889",
            "100000",
        ],
    },
{
        "title": "Bulb Switcher",
        "topic": "math", "difficulty": "medium",
        "description": "Bulbs numbered from one all start off. On round i every bulb whose number divides by i is flipped, for rounds one through n. Return how many bulbs are on at the end.",
        "example_input": "3",
        "constraints": "Input format: one line containing n (at least 0). Output format: a single integer.",
        "solve": _solve_bulb_switcher,
        "sample_inputs": ["3", "0"],
        "hidden_inputs": [
            "1",                    # one bulb, switched on once
            "2",
            "4",                    # the second square
            "5",
            "8",
            "9",
            "10",
            "99",
            "100",
            "1000000",
        ],
    },
{
        "title": "Super Pow",
        "topic": "math", "difficulty": "medium",
        "description": "Raise a number to a power whose digits are given one per entry, and return the result after dividing by 1337 and keeping the remainder.",
        "example_input": "2\n3",
        "constraints": "Input format: line 1 is the base, line 2 is the space-separated digits of the exponent. Output format: a single integer.",
        "solve": _solve_super_pow,
        "sample_inputs": ["2\n3", "2\n1 0"],
        "hidden_inputs": [
            "1\n0",                 # one to any power
            "2\n0",                 # anything to the zero
            "1\n9 9",
            "2\n1",
            "3\n2",
            "2\n4",
            "2\n1 1",
            "2147483647\n2 0 0",
            "7\n1 2 3",
            "1337\n1",              # the base equals the modulus
        ],
    },
{
        "title": "Integer Break",
        "topic": "math", "difficulty": "medium",
        "description": "Split a number into at least two whole parts that add up to it, and return the largest product those parts can have.",
        "example_input": "10",
        "constraints": "Input format: one line containing n (at least 2). Output format: a single integer.",
        "solve": _solve_integer_break,
        "sample_inputs": ["10", "2"],
        "hidden_inputs": [
            "3",                    # one and two
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "11",
            "20",
            "58",
        ],
    },
{
        "title": "Number of Digit One",
        "topic": "math", "difficulty": "medium",
        "description": "Count how many times the digit one appears altogether when every whole number from one up to n is written out.",
        "example_input": "13",
        "constraints": "Input format: one line containing n (at least 0). Output format: a single integer.",
        "solve": _solve_number_of_digit_one,
        "sample_inputs": ["13", "0"],
        "hidden_inputs": [
            "1",                    # just the one
            "2",
            "9",
            "10",
            "11",                   # eleven contributes two
            "12",
            "20",
            "100",
            "1000",
            "99999",
        ],
    },
{
        "title": "Simplified Fractions",
        "topic": "math", "difficulty": "medium",
        "description": "List every fraction strictly between zero and one whose bottom number is at most n and which cannot be reduced further. Order them by the top number, then by the bottom.",
        "example_input": "4",
        "constraints": "Input format: one line containing n (at least 1). Output format: the fractions as \"top/bottom\", space-separated (empty if none).",
        "solve": _solve_simplified_fractions,
        "sample_inputs": ["4", "2"],
        "hidden_inputs": [
            "1",                    # nothing qualifies
            "3",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "12",
            "15",
        ],
    },
{
        "title": "Super Ugly Number",
        "topic": "math", "difficulty": "hard",
        "description": "A super ugly number has no prime divisors outside the given list, and one counts as super ugly. Return the nth such number, counting from one.",
        "example_input": "12\n2 7 13 19",
        "constraints": "Input format: line 1 is n, line 2 is the space-separated primes. Output format: a single integer.",
        "solve": _solve_super_ugly_number,
        "sample_inputs": ["12\n2 7 13 19", "1\n2 3 5"],
        "hidden_inputs": [
            "2\n2",                 # powers of a single prime
            "5\n2",
            "2\n3",
            "3\n2 3",
            "10\n2 3 5",
            "1\n7",                 # one is always first
            "4\n5",
            "8\n2 3",
            "15\n2 7 13 19",
            "20\n2 3 5 7",
        ],
    },
{
        "title": "Reach a Number",
        "topic": "math", "difficulty": "hard",
        "description": "Starting at zero on a number line, the first move is one step, the second is two steps, and so on, each taken either left or right. Return the fewest moves needed to land exactly on the target.",
        "example_input": "3",
        "constraints": "Input format: one line containing the target, which may be negative. Output format: a single integer.",
        "solve": _solve_reach_a_number,
        "sample_inputs": ["3", "2"],
        "hidden_inputs": [
            "0",                    # already there, no moves
            "1",                    # one move
            "-1",                   # symmetry about zero
            "-2",
            "4",                    # needs an overshoot then a flip
            "5",
            "6",                    # exactly the sum of one to three
            "-6",
            "10",
            "30",
        ],
    },
{
        "title": "Count of Range Sum",
        "topic": "math", "difficulty": "hard",
        "description": "Count the stretches of consecutive values whose total lies between the two given bounds, both included.",
        "example_input": "-2 5 -1\n-2 2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 holds the lower and upper bounds. Output format: a single integer.",
        "solve": _solve_count_of_range_sum,
        "sample_inputs": ["-2 5 -1\n-2 2", "0\n0 0"],
        "hidden_inputs": [
            "1\n1 1",               # the single value is inside
            "1\n2 3",               # it is outside
            "1 2\n1 3",
            "-1 1\n0 0",            # the pair cancels
            "1 1 1\n2 2",
            "-1 -2 -3\n-3 -1",      # negatives
            "0 0 0\n0 0",
            "1 2 3 4\n3 6",
            "-2 5 -1\n-100 100",    # every stretch qualifies
        ],
    },
{
        "title": "Nth Magical Number",
        "topic": "math", "difficulty": "hard",
        "description": "A number is magical when it divides exactly by at least one of two given numbers. Return the nth magical number in increasing order, after dividing by 1000000007 and keeping the remainder.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line holding n, a and b. Output format: a single integer.",
        "solve": _solve_nth_magical_number,
        "sample_inputs": ["1 2 3", "4 2 3"],
        "hidden_inputs": [
            "1 1 1",                # every number is magical
            "5 1 1",
            "1 2 2",                # both divisors are the same
            "3 2 2",
            "2 2 3",
            "3 2 3",
            "5 2 4",                # one divisor divides the other
            "10 3 5",
            "100 4 6",
            "100000 2 3",
        ],
    },
{
        "title": "Preimage Size of Factorial Zeroes Function",
        "topic": "math", "difficulty": "hard",
        "description": "For a whole number x, count the zeroes at the end of the product of every number from one to x. Given a target count, return how many different values of x produce exactly that many zeroes.",
        "example_input": "0",
        "constraints": "Input format: one line containing the target count (at least 0). Output format: a single integer, always 0 or 5.",
        "solve": _solve_preimage_factorial_zeroes,
        "sample_inputs": ["0", "5"],
        "hidden_inputs": [
            "1",                    # reachable
            "2",
            "3",
            "4",
            "6",
            "7",                    # unreachable, the count jumps past it
            "11",
            "12",
            "1000",
            "100000",
        ],
    },
{
        "title": "Smallest Good Base",
        "topic": "math", "difficulty": "hard",
        "description": "A base is good for a number when writing that number in the base gives nothing but ones. Return the smallest good base for the given number.",
        "example_input": "13",
        "constraints": "Input format: one line containing the number, at least 3. Output format: the base as a single integer.",
        "solve": _solve_smallest_good_base,
        "sample_inputs": ["13", "4681"],
        "hidden_inputs": [
            "3",                    # two in base two is 11
            "4",
            "5",
            "7",                    # 111 in base two
            "8",
            "15",                   # 1111 in base two
            "31",
            "40",
            "1000000",
            "470448398",
        ],
    },
{
        "title": "Consecutive Numbers Sum",
        "topic": "math", "difficulty": "hard",
        "description": "Count the ways a number can be written as the total of two or more consecutive positive whole numbers, plus the trivial way of writing it as itself.",
        "example_input": "5",
        "constraints": "Input format: one line containing n (at least 1). Output format: a single integer.",
        "solve": _solve_consecutive_numbers_sum,
        "sample_inputs": ["5", "9"],
        "hidden_inputs": [
            "1",                    # only itself
            "2",                    # a power of two has just one way
            "3",
            "4",
            "8",
            "15",
            "16",
            "45",
            "100",
            "1000",
        ],
    },
]
