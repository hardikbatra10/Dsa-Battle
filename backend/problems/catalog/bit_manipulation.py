"""Bit Manipulation problems."""

def _solve_single_number(lines):
    nums = list(map(int, lines[0].split()))
    result = 0
    for n in nums:
        result ^= n
    return str(result)


def _solve_counting_bits(lines):
    n = int(lines[0])
    return " ".join(str(bin(i).count("1")) for i in range(n + 1))


def _solve_max_xor(lines):
    nums = list(map(int, lines[0].split()))
    best = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            best = max(best, nums[i] ^ nums[j])
    return str(best)

def _solve_number_of_one_bits(lines):
    return str(bin(int(lines[0])).count("1"))


def _solve_hamming_distance(lines):
    x, y = map(int, lines[0].split())
    return str(bin(x ^ y).count("1"))


def _solve_power_of_two(lines):
    n = int(lines[0])
    return "true" if n > 0 and n & (n - 1) == 0 else "false"


def _solve_missing_number(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    return str(n * (n + 1) // 2 - sum(nums))


def _solve_reverse_bits(lines):
    n = int(lines[0])
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return str(result)


def _solve_single_number_ii(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = Counter(nums)
    return str(next(v for v, c in counts.items() if c == 1))


def _solve_bitwise_and_range(lines):
    left, right = map(int, lines[0].split())
    shift = 0
    while left < right:
        left >>= 1
        right >>= 1
        shift += 1
    return str(left << shift)


def _solve_sum_two_integers(lines):
    a, b = map(int, lines[0].split())
    return str(a + b)


def _solve_gray_code(lines):
    n = int(lines[0])
    return " ".join(str(i ^ (i >> 1)) for i in range(1 << n))


def _solve_single_number_iii(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = Counter(nums)
    return " ".join(str(v) for v in sorted(v for v, c in counts.items() if c == 1))


def _solve_min_k_bit_flips(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    n = len(nums)
    diff = [0] * (n + 1)
    current = 0
    flips = 0
    for i in range(n):
        current ^= diff[i]
        if (nums[i] ^ current) == 0:
            if i + k > n:
                return "-1"
            flips += 1
            current ^= 1
            diff[i + k] ^= 1
    return str(flips)

def _solve_add_binary(lines):
    a = lines[0]
    b = lines[1] if len(lines) > 1 else "0"
    return bin(int(a, 2) + int(b, 2))[2:]


def _solve_number_complement(lines):
    n = int(lines[0])
    if n == 0:
        return "1"
    mask = (1 << n.bit_length()) - 1
    return str(n ^ mask)


def _solve_alternating_bits(lines):
    n = int(lines[0])
    x = n ^ (n >> 1)
    return "true" if x & (x + 1) == 0 else "false"


def _solve_power_of_four(lines):
    n = int(lines[0])
    if n <= 0 or n & (n - 1):
        return "false"
    return "true" if (n - 1) % 3 == 0 else "false"


def _solve_total_hamming_distance(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    total = 0
    for bit in range(32):
        ones = sum(1 for v in nums if v >> bit & 1)
        total += ones * (n - ones)
    return str(total)


def _solve_max_product_word_lengths(lines):
    count = int(lines[0])
    words = [lines[1 + i] for i in range(count)]
    masks = []
    for w in words:
        m = 0
        for c in w:
            m |= 1 << (ord(c) - 97)
        masks.append(m)
    best = 0
    for i in range(count):
        for j in range(i + 1, count):
            if masks[i] & masks[j] == 0:
                best = max(best, len(words[i]) * len(words[j]))
    return str(best)


def _solve_utf8_validation(lines):
    data = list(map(int, lines[0].split()))
    i = 0
    while i < len(data):
        first = data[i] & 255
        if first >> 7 == 0:
            length = 1
        elif first >> 5 == 0b110:
            length = 2
        elif first >> 4 == 0b1110:
            length = 3
        elif first >> 3 == 0b11110:
            length = 4
        else:
            return "false"
        if i + length > len(data):
            return "false"
        for j in range(i + 1, i + length):
            if (data[j] & 255) >> 6 != 0b10:
                return "false"
        i += length
    return "true"


def _solve_divide_two_integers(lines):
    a, b = map(int, lines[0].split())
    negative = (a < 0) != (b < 0)
    a, b = abs(a), abs(b)
    quotient = 0
    for shift in range(31, -1, -1):
        if (b << shift) <= a:
            a -= b << shift
            quotient += 1 << shift
    if negative:
        quotient = -quotient
    quotient = max(-2 ** 31, min(2 ** 31 - 1, quotient))
    return str(quotient)


def _solve_xor_queries(lines):
    nums = list(map(int, lines[0].split()))
    q = int(lines[1])
    prefix = [0]
    for v in nums:
        prefix.append(prefix[-1] ^ v)
    out = []
    for i in range(q):
        l, r = map(int, lines[2 + i].split())
        out.append(str(prefix[r + 1] ^ prefix[l]))
    return " ".join(out)


def _solve_decode_xored_array(lines):
    encoded = list(map(int, lines[0].split()))
    first = int(lines[1])
    out = [first]
    for v in encoded:
        out.append(out[-1] ^ v)
    return " ".join(map(str, out))


def _solve_min_flips_or(lines):
    a, b, c = map(int, lines[0].split())
    flips = 0
    for bit in range(32):
        x, y, z = a >> bit & 1, b >> bit & 1, c >> bit & 1
        if z == 0:
            flips += x + y
        elif x == 0 and y == 0:
            flips += 1
    return str(flips)


def _solve_count_equal_xor_triplets(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    prefix = [0]
    for v in nums:
        prefix.append(prefix[-1] ^ v)
    count = 0
    for i in range(n):
        for k in range(i + 1, n):
            if prefix[i] == prefix[k + 1]:
                count += k - i
    return str(count)


def _solve_max_xor_with_limit(lines):
    nums = sorted(map(int, lines[0].split()))
    q = int(lines[1])
    out = []
    for i in range(q):
        x, m = map(int, lines[2 + i].split())
        best = -1
        for v in nums:
            if v <= m:
                best = max(best, v ^ x)
        out.append(str(best))
    return " ".join(out)


def _solve_shortest_path_all_nodes(lines):
    n, m = map(int, lines[0].split())
    adj = [[] for _ in range(n)]
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        adj[a].append(b)
        adj[b].append(a)
    full = (1 << n) - 1
    if n == 1:
        return "0"
    frontier = [(v, 1 << v) for v in range(n)]
    seen = set(frontier)
    steps = 0
    while frontier:
        nxt = []
        for v, mask in frontier:
            if mask == full:
                return str(steps)
            for w in adj[v]:
                state = (w, mask | (1 << w))
                if state not in seen:
                    seen.add(state)
                    nxt.append(state)
        frontier = nxt
        steps += 1
    return "-1"


def _solve_smallest_sufficient_team(lines):
    ns = int(lines[0])
    skills = lines[1].split()
    np_ = int(lines[2])
    index = {s: i for i, s in enumerate(skills)}
    people = []
    for i in range(np_):
        parts = lines[3 + i].split()
        mask = 0
        for s in parts[1:]:
            mask |= 1 << index[s]
        people.append(mask)
    full = (1 << ns) - 1
    best = None
    for combo in range(1 << np_):
        mask = 0
        team = []
        for i in range(np_):
            if combo >> i & 1:
                mask |= people[i]
                team.append(i)
        if mask == full:
            if best is None or (len(team), team) < (len(best), best):
                best = team
    return " ".join(map(str, best)) if best else ""


def _solve_ways_to_wear_hats(lines):
    n = int(lines[0])
    lists = [list(map(int, lines[1 + i].split()))[1:] for i in range(n)]
    MOD = 10 ** 9 + 7
    by_hat = {}
    for person, hats in enumerate(lists):
        for h in hats:
            by_hat.setdefault(h, []).append(person)
    full = (1 << n) - 1
    dp = [0] * (1 << n)
    dp[0] = 1
    for h in sorted(by_hat):
        nxt = dp[:]
        for mask in range(1 << n):
            if dp[mask] == 0:
                continue
            for person in by_hat[h]:
                if not (mask >> person & 1):
                    nxt[mask | (1 << person)] = (nxt[mask | (1 << person)] + dp[mask]) % MOD
        dp = nxt
    return str(dp[full] % MOD)


def _solve_shortest_superstring(lines):
    n = int(lines[0])
    words = [lines[1 + i] for i in range(n)]
    words = [w for i, w in enumerate(words)
             if not any(w in other and i != j for j, other in enumerate(words)
                        if len(other) > len(w) or (len(other) == len(w) and j < i))]
    n = len(words)

    def overlap(a, b):
        for k in range(min(len(a), len(b)), 0, -1):
            if a.endswith(b[:k]):
                return k
        return 0

    from itertools import permutations
    best = None
    for p in permutations(range(n)):
        s = words[p[0]]
        for i in range(1, n):
            k = overlap(s, words[p[i]])
            s += words[p[i]][k:]
        if best is None or (len(s), s) < (len(best), best):
            best = s
    return best if best is not None else ""


def _solve_max_students_exam(lines):
    m, n = map(int, lines[0].split())
    rows = [lines[1 + i].split() for i in range(m)]
    valid_rows = []
    for r in rows:
        free = 0
        for j, c in enumerate(r):
            if c == ".":
                free |= 1 << j
        valid_rows.append(free)
    prev = {0: 0}
    for free in valid_rows:
        cur = {}
        for mask in range(1 << n):
            if mask & ~free:
                continue
            if mask & (mask << 1):
                continue
            count = bin(mask).count("1")
            for pmask, pbest in prev.items():
                if mask & (pmask << 1) or mask & (pmask >> 1):
                    continue
                cur[mask] = max(cur.get(mask, -1), pbest + count)
        prev = cur if cur else {0: max(prev.values())}
    return str(max(prev.values()))


def _solve_min_xor_sum(lines):
    a = list(map(int, lines[0].split()))
    b = list(map(int, lines[1].split()))
    n = len(a)
    INF = float("inf")
    dp = [INF] * (1 << n)
    dp[0] = 0
    for mask in range(1 << n):
        if dp[mask] == INF:
            continue
        i = bin(mask).count("1")
        if i == n:
            continue
        for j in range(n):
            if not (mask >> j & 1):
                nm = mask | (1 << j)
                dp[nm] = min(dp[nm], dp[mask] + (a[i] ^ b[j]))
    return str(dp[(1 << n) - 1])


PROBLEMS = [
{
        "title": "Single Number",
        "topic": "bit_manipulation",
        "difficulty": "easy",
        "description": "Given a non-empty array where every element appears twice except for one, find that single element.",
        "example_input": "4 1 2 1 2",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_single_number,
        "sample_inputs": ["4 1 2 1 2", "9 3 9"],
        "hidden_inputs": [
            "1",          # the lone element is the answer
            "0",
            "-1",
            "0 1 1",      # the answer is zero
            "2 2 1",
            "3 1 1 2 2",  # single element first
            "1 2 1 2 5",  # single element last
            "1 1 2 2 3",
            "-1 -1 -2",   # negative answer
            "7 3 5 3 5",
            "1000000 1 1",
        ],
    },
{
        "title": "Counting Bits",
        "topic": "bit_manipulation",
        "difficulty": "medium",
        "description": "Given an integer n, return an array of length n+1 where the value at index i is the number of 1's in the binary representation of i.",
        "example_input": "5",
        "constraints": "Input format: one line containing n. Output format: space-separated counts for i = 0..n.",
        "solve": _solve_counting_bits,
        "sample_inputs": ["5", "4"],
        "hidden_inputs": [
            "0",  # just i = 0
            "1",
            "2",
            "3",
            "7",  # last index before a new bit length
            "8",  # first index of a new bit length
            "15",
            "16",
            "31",
            "32",
            "100",
        ],
    },
{
        "title": "Maximum XOR of Two Numbers in an Array",
        "topic": "bit_manipulation",
        "difficulty": "hard",
        "description": "Given an array of integers (at least two elements), find the maximum XOR of any two elements.",
        "example_input": "3 10 5 25 2 8",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_max_xor,
        "sample_inputs": ["3 10 5 25 2 8", "4 6 7"],
        "hidden_inputs": [
            "0 0",           # minimum size, answer zero
            "1 1",           # identical values xor to zero
            "0 1",
            "8 1",
            "2 4",
            "5 5 5",         # every pair is identical
            "8 10 2",
            "1 3 5 7 9",
            "1 2 3 4 5 6 7",
            "2147483647 0",  # 32-bit maximum
            "14 70 53 83 49 91 36 80 92 51 66 70",
        ],
    },
{
        "title": "Number of 1 Bits",
        "topic": "bit_manipulation",
        "difficulty": "easy",
        "description": "Return how many bits are set to one in the binary form of a non-negative integer.",
        "example_input": "11",
        "constraints": "Input format: one line containing the integer (at least 0). Output format: a single integer.",
        "solve": _solve_number_of_one_bits,
        "sample_inputs": ["11", "128"],
        "hidden_inputs": [
            "0",                    # no bits set
            "1",
            "2",
            "3",                    # two adjacent bits
            "7",                    # three adjacent bits
            "8",                    # a single high bit
            "15",
            "16",
            "255",                  # a full byte
            "4294967293",           # 32 bits with one zero among them
        ],
    },
{
        "title": "Hamming Distance",
        "topic": "bit_manipulation",
        "difficulty": "easy",
        "description": "Return how many bit positions hold different values between two non-negative integers.",
        "example_input": "1 4",
        "constraints": "Input format: one line holding the two integers. Output format: a single integer.",
        "solve": _solve_hamming_distance,
        "sample_inputs": ["1 4", "3 1"],
        "hidden_inputs": [
            "0 0",                  # identical, distance zero
            "1 1",
            "0 1",                  # a single differing bit
            "1 0",                  # order must not matter
            "0 255",                # every bit of a byte differs
            "255 255",
            "5 5",
            "7 8",                  # no bits in common
            "1024 1",
            "4294967295 0",         # all 32 bits differ
        ],
    },
{
        "title": "Power of Two",
        "topic": "bit_manipulation",
        "difficulty": "easy",
        "description": "Decide whether an integer can be written as two raised to some whole power of zero or more.",
        "example_input": "16",
        "constraints": "Input format: one line containing the integer, which may be negative. Output format: \"true\" or \"false\".",
        "solve": _solve_power_of_two,
        "sample_inputs": ["16", "3"],
        "hidden_inputs": [
            "1",                    # two to the zero
            "0",                    # zero is not a power
            "-1",                   # negatives never are
            "-16",                  # even a negative power of two
            "2",
            "4",
            "6",                    # even but not a power
            "1023",                 # one below a power
            "1024",
            "1073741824",           # the largest inside 32-bit
        ],
    },
{
        "title": "Missing Number",
        "topic": "bit_manipulation",
        "difficulty": "easy",
        "description": "A list holds every whole number from zero up to n except one, each appearing once. Return the number that is missing.",
        "example_input": "3 0 1",
        "constraints": "Input format: one line of space-separated distinct integers drawn from 0 to n with exactly one absent. Output format: a single integer.",
        "solve": _solve_missing_number,
        "sample_inputs": ["3 0 1", "9 6 4 2 3 5 7 0 1"],
        "hidden_inputs": [
            "0",                    # only zero present, one is missing
            "1",                    # only one present, zero is missing
            "0 1",                  # the last number is missing
            "1 2",                  # the first is missing
            "0 2",                  # one from the middle
            "2 0 1",
            "0 1 2 3 4",
            "1 2 3 4 5",
            "5 4 3 2 1",            # reversed order
            "0 1 2 3 4 5 6 7 8 10",
        ],
    },
{
        "title": "Reverse Bits",
        "topic": "bit_manipulation",
        "difficulty": "easy",
        "description": "Treating the input as a 32-bit unsigned number, reverse the order of its bits and return the resulting value.",
        "example_input": "43261596",
        "constraints": "Input format: one line containing the integer, between 0 and 4294967295. Output format: a single integer.",
        "solve": _solve_reverse_bits,
        "sample_inputs": ["43261596", "1"],
        "hidden_inputs": [
            "0",                    # reverses to itself
            "2",
            "4294967295",           # every bit set, reverses to itself
            "2147483648",           # the top bit becomes the bottom
            "3",
            "1073741824",
            "65535",                # the low half set
            "4294901760",           # the high half set
            "16",
            "4294967294",
        ],
    },
{
        "title": "Single Number II",
        "topic": "bit_manipulation",
        "difficulty": "medium",
        "description": "Every value in the list appears exactly three times except one, which appears once. Return that value.",
        "example_input": "2 2 3 2",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_single_number_ii,
        "sample_inputs": ["2 2 3 2", "0 1 0 1 0 1 99"],
        "hidden_inputs": [
            "5",                    # the lone value stands alone
            "0",
            "1 1 1 2",              # the single value is last
            "2 1 1 1",              # and first
            "1 2 1 1",              # and in the middle
            "0 0 0 -2",             # a negative answer
            "-2 -2 -2 -1",
            "7 7 7 8 8 8 9",
            "30000 500 100 30000 100 30000 100",
            "-4 -4 -4 100",
        ],
    },
{
        "title": "Bitwise AND of Numbers Range",
        "topic": "bit_manipulation",
        "difficulty": "medium",
        "description": "Return the result of combining every whole number from left to right inclusive with the bitwise AND operation.",
        "example_input": "5 7",
        "constraints": "Input format: one line holding left and right, with left no greater than right. Output format: a single integer.",
        "solve": _solve_bitwise_and_range,
        "sample_inputs": ["5 7", "0 0"],
        "hidden_inputs": [
            "1 1",                  # a single number
            "0 1",                  # crossing zero clears everything
            "1 2",
            "2 3",                  # adjacent numbers sharing a prefix
            "4 7",                  # a full power-of-two block
            "7 8",                  # crossing a power of two
            "8 15",
            "5 6",
            "1 2147483647",         # the widest possible range
            "1000 1010",
        ],
    },
{
        "title": "Sum of Two Integers",
        "topic": "bit_manipulation",
        "difficulty": "medium",
        "description": "Return the sum of two integers without using the addition or subtraction operators.",
        "example_input": "1 2",
        "constraints": "Input format: one line holding the two integers, which may be negative. Output format: a single integer.",
        "solve": _solve_sum_two_integers,
        "sample_inputs": ["1 2", "2 3"],
        "hidden_inputs": [
            "0 0",                  # nothing to carry
            "0 5",
            "5 0",
            "-1 1",                 # opposite signs cancel
            "1 -1",
            "-2 -3",                # both negative
            "-1 -1",
            "7 9",                  # a carry that ripples
            "-1000 -1000",
            "2147483647 -2147483648",   # the two 32-bit extremes
        ],
    },
{
        "title": "Gray Code",
        "topic": "bit_manipulation",
        "difficulty": "medium",
        "description": "List every number that can be written with n bits, arranged so that consecutive entries differ in exactly one bit, the first entry is zero, and the last also differs from the first in exactly one bit. Return the standard such arrangement, where each entry is the position combined with itself shifted right once.",
        "example_input": "2",
        "constraints": "Input format: one line containing n (n >= 0). Output format: the sequence, space-separated.",
        "solve": _solve_gray_code,
        "sample_inputs": ["2", "1"],
        "hidden_inputs": [
            "0",                    # a single entry, zero
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",                   # 1024 entries, as large as stays readable
            "11",
        ],
    },
{
        "title": "Single Number III",
        "topic": "bit_manipulation",
        "difficulty": "hard",
        "description": "Every value in the list appears exactly twice except two, which appear once each. Return those two values in increasing order.",
        "example_input": "1 2 1 3 2 5",
        "constraints": "Input format: one line of space-separated integers. Output format: the two values, space-separated ascending.",
        "solve": _solve_single_number_iii,
        "sample_inputs": ["1 2 1 3 2 5", "1 0"],
        "hidden_inputs": [
            "0 1",                  # the whole list is the answer
            "1 2",
            "-1 0",                 # a negative and a zero
            "-1 -2",                # both negative
            "1 1 2 3",              # the pair sits first
            "2 3 1 1",              # and last
            "1 2 1 3",
            "0 0 1 2",
            "5 5 7 7 9 11",
            "-1 -1 -2 -3",
        ],
    },
{
        "title": "Minimum Number of K Consecutive Bit Flips",
        "topic": "bit_manipulation",
        "difficulty": "hard",
        "description": "One move flips every bit in a run of exactly k consecutive positions. Return the fewest moves that turn every bit into a one, or -1 if it cannot be done.",
        "example_input": "0 1 0\n1",
        "constraints": "Input format: line 1 is the space-separated bits, each 0 or 1, line 2 is k. Output format: a single integer, or -1.",
        "solve": _solve_min_k_bit_flips,
        "sample_inputs": ["0 1 0\n1", "1 1 0\n2"],
        "hidden_inputs": [
            "1\n1",                 # already done
            "0\n1",                 # one flip
            "1 1\n1",
            "0 0\n1",               # two separate flips
            "0 0\n2",               # one flip covers both
            "0 1\n2",               # impossible, the run is fixed
            "1 1 1\n3",
            "0 0 0\n3",
            "0 0 0 1 0 1 1 0\n3",
            "1 0 1 0 1\n2",         # runs out of room at the end
        ],
    },
{
        "title": "Add Binary",
        "topic": "bit_manipulation", "difficulty": "easy",
        "description": "Add two numbers written in binary and return the total, also in binary, without leading zeros.",
        "example_input": "11\n1",
        "constraints": "Input format: line 1 and line 2 are the two binary strings without leading zeros. Output format: the sum in binary.",
        "solve": _solve_add_binary,
        "sample_inputs": ["11\n1", "1010\n1011"],
        "hidden_inputs": [
            "0\n0",                 # zero plus zero
            "0\n1",
            "1\n0",
            "1\n1",                 # a carry out of one bit
            "11\n11",
            "111\n1",               # a carry that ripples all the way
            "1111\n1111",
            "1\n1111",              # very different lengths
            "10101\n1010",
            "100000000\n1",
        ],
    },
{
        "title": "Number Complement",
        "topic": "bit_manipulation", "difficulty": "easy",
        "description": "Flip every bit of a positive number, counting only the bits from its highest set bit downwards, and return the result.",
        "example_input": "5",
        "constraints": "Input format: one line containing a non-negative integer. Output format: a single integer.",
        "solve": _solve_number_complement,
        "sample_inputs": ["5", "1"],
        "hidden_inputs": [
            "0",                    # zero complements to one
            "2",
            "3",                    # every bit set, so zero
            "4",
            "7",
            "8",
            "10",
            "15",
            "16",
            "2147483647",           # 31 bits all set
        ],
    },
{
        "title": "Binary Number with Alternating Bits",
        "topic": "bit_manipulation", "difficulty": "easy",
        "description": "Decide whether a positive number's binary form never has two equal bits next to each other.",
        "example_input": "5",
        "constraints": "Input format: one line containing a positive integer. Output format: \"true\" or \"false\".",
        "solve": _solve_alternating_bits,
        "sample_inputs": ["5", "7"],
        "hidden_inputs": [
            "1",                    # a single bit
            "2",
            "3",                    # two equal bits together
            "4",
            "6",
            "10",
            "11",
            "21",
            "170",
            "1431655765",           # alternating across 31 bits
        ],
    },
{
        "title": "Power of Four",
        "topic": "bit_manipulation", "difficulty": "easy",
        "description": "Decide whether an integer can be written as four raised to some whole power of zero or more.",
        "example_input": "16",
        "constraints": "Input format: one line containing the integer, which may be negative. Output format: \"true\" or \"false\".",
        "solve": _solve_power_of_four,
        "sample_inputs": ["16", "5"],
        "hidden_inputs": [
            "1",                    # four to the zero
            "0",
            "-4",                   # negatives never qualify
            "2",                    # a power of two but not of four
            "4",
            "8",
            "64",
            "256",
            "1073741824",           # the largest inside 32-bit
            "536870912",            # a power of two, not of four
        ],
    },
{
        "title": "Total Hamming Distance",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "Add up, over every pair of values in the list, the number of bit positions at which the two differ.",
        "example_input": "4 14 2",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: a single integer.",
        "solve": _solve_total_hamming_distance,
        "sample_inputs": ["4 14 2", "4 14 4"],
        "hidden_inputs": [
            "1",                    # no pair exists
            "0 0",                  # identical values
            "0 1",
            "1 1 1",
            "0 1 2 3",
            "7 7 7 7",
            "1 2 4 8",              # no two share a bit
            "255 0",
            "1023 1023 0",
            "5 9 13",
        ],
    },
{
        "title": "Maximum Product of Word Lengths",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "Find two words that share no letter at all, and return the largest product of their lengths. Return zero if no such pair exists.",
        "example_input": "6\nabcw\nbaz\nfoo\nbar\nxtfn\nabcdef",
        "constraints": "Input format: line 1 is the number of words, followed by that many lowercase words. Output format: a single integer.",
        "solve": _solve_max_product_word_lengths,
        "sample_inputs": ["6\nabcw\nbaz\nfoo\nbar\nxtfn\nabcdef", "4\na\nab\nabc\nd"],
        "hidden_inputs": [
            "1\na",                 # no pair at all
            "2\na\na",              # the pair shares its only letter
            "2\na\nb",
            "2\nab\ncd",
            "2\nabc\ncde",          # they share c
            "3\na\nbb\nccc",
            "3\naa\nbb\nab",
            "4\na\nb\nc\nd",
            "3\nabcdefghijklmnopqrstuvwxyz\na\nb",
            "5\neae\nea\naaf\nbda\nfcf",
        ],
    },
{
        "title": "UTF-8 Validation",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "Each value gives the low eight bits of one byte. A character is one byte starting with a zero bit, or two to four bytes where the first starts with that many ones then a zero and every later byte starts with one then zero. Decide whether the whole sequence is a valid encoding.",
        "example_input": "197 130 1",
        "constraints": "Input format: one line of space-separated integers. Output format: \"true\" or \"false\".",
        "solve": _solve_utf8_validation,
        "sample_inputs": ["197 130 1", "235 140 4"],
        "hidden_inputs": [
            "0",                    # a single plain byte
            "127",                  # the largest one-byte value
            "128",                  # a continuation byte with nothing before it
            "255",                  # five leading ones is never valid
            "192 128",              # a valid two-byte character
            "192",                  # the continuation byte is missing
            "224 128 128",          # a valid three-byte character
            "224 128",              # one byte short
            "240 128 128 128",      # a valid four-byte character
            "145",                  # a lone continuation byte
        ],
    },
{
        "title": "Divide Two Integers",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "Divide one integer by another without using multiplication, division or the remainder operator. The result discards any fraction, rounding towards zero, and is clamped to the signed 32-bit range.",
        "example_input": "10 3",
        "constraints": "Input format: one line holding the dividend and the divisor, the divisor never zero. Output format: a single integer.",
        "solve": _solve_divide_two_integers,
        "sample_inputs": ["10 3", "7 -3"],
        "hidden_inputs": [
            "0 1",                  # zero divided by anything
            "1 1",
            "1 2",                  # rounds towards zero
            "-1 2",
            "-7 2",                 # towards zero, not down
            "7 -2",
            "-7 -2",                # two negatives
            "2147483647 1",         # the 32-bit maximum
            "-2147483648 -1",       # overflows and is clamped
            "-2147483648 1",
        ],
    },
{
        "title": "XOR Queries of a Subarray",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "For each query giving a first and last position, combine every value in that stretch with the exclusive-or operation and report the result.",
        "example_input": "1 3 4 8\n4\n0 1\n1 2\n0 3\n3 3",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is the number of queries, followed by that many lines each \"first last\" counting from zero. Output format: one answer per query, space-separated.",
        "solve": _solve_xor_queries,
        "sample_inputs": ["1 3 4 8\n4\n0 1\n1 2\n0 3\n3 3", "4 8 2 10\n4\n2 3\n1 3\n0 0\n0 3"],
        "hidden_inputs": [
            "1\n1\n0 0",            # a single value
            "0\n1\n0 0",
            "1 1\n1\n0 1",          # equal values cancel
            "1 2\n1\n0 1",
            "5 5 5\n1\n0 2",
            "1 2 3\n3\n0 0\n1 1\n2 2",
            "1 2 3\n1\n0 2",
            "0 0 0\n1\n0 2",
            "7 3 5 1\n2\n0 3\n1 2",
            "1 2 4 8 16\n3\n0 4\n2 4\n4 4",
        ],
    },
{
        "title": "Decode XORed Array",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "Each value given is the exclusive-or of two neighbouring values of the original list. Given also the first original value, rebuild the whole list.",
        "example_input": "1 2 3\n1",
        "constraints": "Input format: line 1 is the space-separated encoded values, line 2 is the first original value. Output format: the original list, space-separated.",
        "solve": _solve_decode_xored_array,
        "sample_inputs": ["1 2 3\n1", "6 2 7 3\n4"],
        "hidden_inputs": [
            "0\n0",                 # two zeroes
            "0\n5",                 # a repeated value
            "1\n0",
            "1\n1",
            "5\n0",
            "0 0 0\n7",             # every value the same
            "1 1 1\n0",
            "2 4 8\n1",
            "255 255\n255",
            "1 2 4 8 16\n0",
        ],
    },
{
        "title": "Minimum Flips to Make a OR b Equal to c",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "Flipping a single bit of the first or second number counts as one move. Return the fewest moves needed so that combining the two with the or operation gives the third number.",
        "example_input": "2 6 5",
        "constraints": "Input format: one line holding the three non-negative integers. Output format: a single integer.",
        "solve": _solve_min_flips_or,
        "sample_inputs": ["2 6 5", "4 2 7"],
        "hidden_inputs": [
            "0 0 0",                # already correct
            "1 1 1",
            "0 0 1",                # one bit must be turned on
            "1 0 0",                # one bit must be turned off
            "1 1 0",                # both must be turned off
            "1 2 3",
            "3 3 0",
            "7 0 7",
            "8 3 5",
            "255 255 0",
        ],
    },
{
        "title": "Count Triplets That Can Form Two Arrays of Equal XOR",
        "topic": "bit_manipulation", "difficulty": "medium",
        "description": "Count the triples of positions, the first no later than the second and the second no later than the last, where combining the values before the second position gives the same exclusive-or as combining those from it onwards.",
        "example_input": "2 3 1 6 7",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: a single integer.",
        "solve": _solve_count_equal_xor_triplets,
        "sample_inputs": ["2 3 1 6 7", "1 1 1 1 1"],
        "hidden_inputs": [
            "1",                    # too short for a triple
            "1 1",                  # equal values give one triple
            "1 2",                  # unequal values give none
            "0 0",
            "0 0 0",
            "1 2 3",
            "2 3 1",
            "1 3 5 7 9",
            "7 11 12 9 5 2 7 17 22",
            "0 1 0 1",
        ],
    },
{
        "title": "Maximum XOR With an Element From Array",
        "topic": "bit_manipulation", "difficulty": "hard",
        "description": "For each query giving a value and a limit, combine the value with the best element of the list that does not exceed the limit, using the exclusive-or operation, and report the largest result, or -1 if no element qualifies.",
        "example_input": "0 1 2 3 4\n3\n3 1\n1 3\n5 6",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is the number of queries, followed by that many lines each \"value limit\". Output format: one answer per query, space-separated.",
        "solve": _solve_max_xor_with_limit,
        "sample_inputs": ["0 1 2 3 4\n3\n3 1\n1 3\n5 6", "5 2 4 6 6 3\n3\n12 4\n8 1\n6 3"],
        "hidden_inputs": [
            "1\n1\n0 1",            # one element, within the limit
            "1\n1\n0 0",            # the only element exceeds the limit
            "0\n1\n0 0",
            "1 2\n1\n0 1",
            "1 2\n1\n0 2",
            "5 5 5\n1\n0 5",        # duplicates
            "1 2 4 8\n2\n15 8\n15 1",
            "0 1 2 3\n1\n0 3",
            "7\n2\n7 7\n7 6",
            "1 3 5 7 9\n3\n2 5\n2 9\n2 0",
        ],
    },
{
        "title": "Shortest Path Visiting All Nodes",
        "topic": "bit_manipulation", "difficulty": "hard",
        "description": "Starting wherever you like and free to revisit nodes and edges, return the fewest edge steps needed to visit every node of a connected graph at least once.",
        "example_input": "4 3\n0 1\n0 2\n0 3",
        "constraints": "Input format: line 1 is \"n m\", followed by m lines each \"a b\" describing an undirected edge; the graph is connected. Output format: a single integer.",
        "solve": _solve_shortest_path_all_nodes,
        "sample_inputs": ["4 3\n0 1\n0 2\n0 3", "4 4\n1 0\n1 1\n1 2\n1 3"],
        "hidden_inputs": [
            "1 0",                  # one node, already visited
            "2 1\n0 1",             # one step
            "3 2\n0 1\n1 2",        # a path
            "3 3\n0 1\n1 2\n2 0",   # a triangle
            "4 3\n0 1\n1 2\n2 3",   # a longer path
            "4 4\n0 1\n1 2\n2 3\n3 0",
            "5 4\n0 1\n0 2\n0 3\n0 4",      # a star forces backtracking
            "5 4\n0 1\n1 2\n2 3\n3 4",
            "6 5\n0 1\n0 2\n0 3\n0 4\n0 5",
            "4 5\n0 1\n1 2\n2 3\n0 2\n1 3",
        ],
    },
{
        "title": "Smallest Sufficient Team",
        "topic": "bit_manipulation", "difficulty": "hard",
        "description": "Pick the fewest people whose skills together cover every required skill. When several teams are equally small, return the one that comes first when the member numbers are compared in order.",
        "example_input": "3\njava nodejs reactjs\n3\n1 java\n2 nodejs reactjs\n2 java reactjs",
        "constraints": "Input format: line 1 is the number of required skills, line 2 lists them, line 3 is the number of people, followed by one line per person holding a count then that person's skills. A sufficient team always exists. Output format: the chosen people's numbers counting from zero, space-separated ascending.",
        "solve": _solve_smallest_sufficient_team,
        "sample_inputs": [
            "3\njava nodejs reactjs\n3\n1 java\n2 nodejs reactjs\n2 java reactjs",
            "2\na b\n2\n1 a\n1 b",
        ],
        "hidden_inputs": [
            "1\na\n1\n1 a",                 # one person covers everything
            "1\na\n2\n1 a\n1 a",            # a tie broken by the lower number
            "2\na b\n1\n2 a b",
            "2\na b\n3\n1 a\n1 b\n2 a b",   # one person beats two
            "3\na b c\n3\n1 a\n1 b\n1 c",   # everyone is needed
            "3\na b c\n4\n2 a b\n2 b c\n1 c\n1 a",
            "2\na b\n4\n1 a\n1 a\n1 b\n1 b",
            "4\na b c d\n2\n2 a b\n2 c d",
            "3\na b c\n2\n3 a b c\n1 a",
            "4\na b c d\n4\n1 a\n2 a b\n2 c d\n1 d",
        ],
    },
{
        "title": "Number of Ways to Wear Different Hats to Each Other",
        "topic": "bit_manipulation", "difficulty": "hard",
        "description": "Each person will wear exactly one hat from their own list, and no two people may wear the same hat. Count the ways this can be arranged, modulo 1000000007.",
        "example_input": "2\n2 3 4\n2 4 5",
        "constraints": "Input format: line 1 is the number of people, followed by one line per person holding a count then that person's hat numbers. Output format: a single integer, the count modulo 1000000007.",
        "solve": _solve_ways_to_wear_hats,
        "sample_inputs": ["2\n2 3 4\n2 4 5", "2\n1 1\n1 1"],
        "hidden_inputs": [
            "1\n1 1",               # one person, one hat
            "1\n3 1 2 3",           # one person, three choices
            "2\n1 1\n1 2",          # exactly one arrangement
            "2\n2 1 2\n2 1 2",      # two arrangements
            "2\n2 1 2\n1 1",
            "3\n1 1\n1 2\n1 3",
            "3\n2 1 2\n2 1 2\n2 1 2",   # three people, two hats, impossible
            "2\n3 1 2 3\n3 1 2 3",
            "3\n3 1 2 3\n3 1 2 3\n3 1 2 3",
            "4\n1 1\n1 2\n1 3\n1 4",
        ],
    },
{
        "title": "Find the Shortest Superstring",
        "topic": "bit_manipulation", "difficulty": "hard",
        "description": "Build the shortest string that contains every one of the given words somewhere inside it. When several are equally short, return the one that comes first alphabetically.",
        "example_input": "2\nalex\nloves",
        "constraints": "Input format: line 1 is the number of words, followed by that many lowercase words, none of which contains another. Output format: the string.",
        "solve": _solve_shortest_superstring,
        "sample_inputs": ["2\nalex\nloves", "3\ncatg\nctaagt\ngcta"],
        "hidden_inputs": [
            "1\nabc",               # one word is its own superstring
            "2\nab\nba",            # they overlap either way round
            "2\nab\ncd",            # no overlap at all
            "2\nabc\nbcd",
            "2\nbcd\nabc",          # order in the input must not matter
            "3\na\nb\nc",
            "3\nab\nbc\ncd",
            "3\nabc\ncde\nefg",
            "4\nab\nbc\ncd\nde",
            "3\ngat\ntag\natg",
        ],
    },
{
        "title": "Maximum Students Taking Exam",
        "topic": "bit_manipulation", "difficulty": "hard",
        "description": "Seats marked with a dot are usable and those marked with a hash are broken. A student can copy from the seats immediately left, right, upper left and upper right, so no two seated students may sit in any of those relations. Return the greatest number that can be seated.",
        "example_input": "3 4\n# . # #\n. . . .\n# . # #",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated seats, each a dot or a hash. Output format: a single integer.",
        "solve": _solve_max_students_exam,
        "sample_inputs": ["3 4\n# . # #\n. . . .\n# . # #", "3 3\n. #\n# #\n. #"[:0] or "3 3\n. # .\n# # #\n. # ."],
        "hidden_inputs": [
            "1 1\n.",               # one usable seat
            "1 1\n#",               # none usable
            "1 2\n. .",             # neighbours cannot both be used
            "1 3\n. . .",
            "2 1\n.\n.",            # directly above is allowed
            "2 2\n. .\n. .",
            "2 2\n# #\n# #",
            "2 3\n. . .\n. . .",
            "3 3\n. . .\n. . .\n. . .",
            "4 2\n. .\n. .\n. .\n. .",
        ],
    },
{
        "title": "Minimum XOR Sum of Two Arrays",
        "topic": "bit_manipulation", "difficulty": "hard",
        "description": "Pair every value of the first list with a different value of the second, combine each pair with the exclusive-or operation, and add the results. Return the smallest total possible.",
        "example_input": "1 2\n2 3",
        "constraints": "Input format: line 1 and line 2 are the two space-separated lists, both the same length. Output format: a single integer.",
        "solve": _solve_min_xor_sum,
        "sample_inputs": ["1 2\n2 3", "1 0 3\n5 3 4"],
        "hidden_inputs": [
            "0\n0",                 # one pair, no difference
            "1\n1",
            "0\n1",
            "1 1\n1 1",             # every pairing is identical
            "0 0\n0 0",
            "1 2\n1 2",             # the obvious pairing is best
            "1 2\n2 1",             # the crossed pairing is best
            "3 5\n5 3",
            "7 0 3\n3 0 7",
            "1 2 4 8\n8 4 2 1",
        ],
    },
]
