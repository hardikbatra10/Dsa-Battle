"""Backtracking problems."""

def _solve_subsets(lines):
    from itertools import combinations
    nums = list(map(int, lines[0].split()))
    out = []
    for r in range(1, len(nums) + 1):
        for combo in combinations(nums, r):
            out.append(" ".join(map(str, combo)))
    return "\n".join(out)


def _solve_permutations(lines):
    from itertools import permutations
    nums = list(map(int, lines[0].split()))
    return "\n".join(" ".join(map(str, p)) for p in permutations(nums))


def _solve_n_queens_count(lines):
    n = int(lines[0])
    count = [0]
    cols, diag1, diag2 = set(), set(), set()

    def backtrack(row):
        if row == n:
            count[0] += 1
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

    backtrack(0)
    return str(count[0])

def _solve_combinations(lines):
    n, k = map(int, lines[0].split())
    from itertools import combinations
    return "\n".join(" ".join(map(str, c))
                     for c in combinations(range(1, n + 1), k))


def _solve_letter_case_permutation(lines):
    s = lines[0]
    results = [""]
    for ch in s:
        if ch.isalpha():
            results = [r + c for r in results for c in (ch.lower(), ch.upper())]
        else:
            results = [r + ch for r in results]
    return "\n".join(sorted(results))


def _solve_generate_parentheses(lines):
    n = int(lines[0])
    out = []

    def go(cur, opened, closed):
        if len(cur) == 2 * n:
            out.append(cur)
            return
        if opened < n:
            go(cur + "(", opened + 1, closed)
        if closed < opened:
            go(cur + ")", opened, closed + 1)

    go("", 0, 0)
    return "\n".join(sorted(out))


def _solve_subsets_with_duplicates(lines):
    nums = sorted(map(int, lines[0].split()))
    from itertools import combinations
    seen = set()
    for r in range(1, len(nums) + 1):
        for c in combinations(nums, r):
            seen.add(c)
    ordered = sorted(seen, key=lambda t: (len(t), t))
    return "\n".join(" ".join(map(str, t)) for t in ordered)


def _solve_letter_combinations(lines):
    digits = lines[0]
    if not digits:
        return ""
    mapping = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
               "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}
    results = [""]
    for d in digits:
        results = [r + c for r in results for c in mapping[d]]
    return "\n".join(results)


def _solve_combination_sum(lines):
    cands = sorted(set(map(int, lines[0].split())))
    target = int(lines[1])
    out = []

    def go(start, remain, cur):
        if remain == 0:
            out.append(list(cur))
            return
        for i in range(start, len(cands)):
            if cands[i] <= remain:
                cur.append(cands[i])
                go(i, remain - cands[i], cur)
                cur.pop()

    go(0, target, [])
    out.sort()
    return "\n".join(" ".join(map(str, c)) for c in out)


def _solve_combination_sum_ii(lines):
    cands = sorted(map(int, lines[0].split()))
    target = int(lines[1])
    out = set()

    def go(start, remain, cur):
        if remain == 0:
            out.add(tuple(cur))
            return
        for i in range(start, len(cands)):
            if cands[i] > remain:
                break
            cur.append(cands[i])
            go(i + 1, remain - cands[i], cur)
            cur.pop()

    go(0, target, [])
    return "\n".join(" ".join(map(str, c)) for c in sorted(out))


def _solve_permutations_with_duplicates(lines):
    nums = sorted(map(int, lines[0].split()))
    from itertools import permutations
    return "\n".join(" ".join(map(str, p)) for p in sorted(set(permutations(nums))))


def _solve_palindrome_partitioning(lines):
    s = lines[0]
    out = []

    def go(i, cur):
        if i == len(s):
            out.append(" ".join(cur))
            return
        for j in range(i + 1, len(s) + 1):
            part = s[i:j]
            if part == part[::-1]:
                cur.append(part)
                go(j, cur)
                cur.pop()

    go(0, [])
    return "\n".join(sorted(out))


def _solve_word_search(lines):
    m, n = map(int, lines[0].split())
    grid = [lines[1 + i].split() for i in range(m)]
    word = lines[1 + m]

    def go(i, j, k, used):
        if k == len(word):
            return True
        if not (0 <= i < m and 0 <= j < n):
            return False
        if (i, j) in used or grid[i][j] != word[k]:
            return False
        used.add((i, j))
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if go(i + di, j + dj, k + 1, used):
                used.discard((i, j))
                return True
        used.discard((i, j))
        return False

    for i in range(m):
        for j in range(n):
            if go(i, j, 0, set()):
                return "true"
    return "false"


def _solve_n_queens_solutions(lines):
    n = int(lines[0])
    out = []
    cols, diag1, diag2 = set(), set(), set()
    placement = []

    def go(row):
        if row == n:
            out.append(list(placement))
            return
        for c in range(n):
            if c in cols or (row - c) in diag1 or (row + c) in diag2:
                continue
            cols.add(c)
            diag1.add(row - c)
            diag2.add(row + c)
            placement.append(c)
            go(row + 1)
            placement.pop()
            cols.discard(c)
            diag1.discard(row - c)
            diag2.discard(row + c)

    go(0)
    return "\n".join(" ".join(map(str, p)) for p in out)

def _solve_binary_watch(lines):
    n = int(lines[0])
    out = []
    for h in range(12):
        for m in range(60):
            if bin(h).count("1") + bin(m).count("1") == n:
                out.append("%d:%02d" % (h, m))
    return " ".join(out)


def _solve_count_vowel_strings(lines):
    n = int(lines[0])
    counts = [1] * 5
    for _ in range(n - 1):
        for i in range(3, -1, -1):
            counts[i] += counts[i + 1]
    return str(sum(counts))


def _solve_combination_sum_iii(lines):
    k, n = map(int, lines[0].split())
    from itertools import combinations
    out = []
    for combo in combinations(range(1, 10), k):
        if sum(combo) == n:
            out.append(" ".join(map(str, combo)))
    return "\n".join(out)


def _solve_count_unique_digit_numbers(lines):
    n = int(lines[0])
    if n == 0:
        return "1"
    total = 10
    product = 9
    for i in range(2, min(n, 10) + 1):
        product *= (11 - i)
        total += product
    return str(total)


def _solve_letter_tile_possibilities(lines):
    tiles = lines[0]
    seen = set()

    def go(prefix, remaining):
        if prefix:
            seen.add(prefix)
        for i in range(len(remaining)):
            go(prefix + remaining[i], remaining[:i] + remaining[i + 1:])

    go("", tiles)
    return str(len(seen))


def _solve_restore_ip_addresses(lines):
    s = lines[0]
    out = []

    def go(start, parts):
        if len(parts) == 4:
            if start == len(s):
                out.append(".".join(parts))
            return
        for size in range(1, 4):
            if start + size > len(s):
                break
            piece = s[start:start + size]
            if (piece[0] == "0" and size > 1) or int(piece) > 255:
                continue
            go(start + size, parts + [piece])

    go(0, [])
    return "\n".join(sorted(out))


def _solve_beautiful_arrangement(lines):
    n = int(lines[0])
    used = [False] * (n + 1)
    count = [0]

    def go(pos):
        if pos > n:
            count[0] += 1
            return
        for v in range(1, n + 1):
            if not used[v] and (v % pos == 0 or pos % v == 0):
                used[v] = True
                go(pos + 1)
                used[v] = False

    go(1)
    return str(count[0])


def _solve_partition_k_equal_subsets(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    total = sum(nums)
    if total % k:
        return "false"
    target = total // k
    nums.sort(reverse=True)
    if nums[0] > target:
        return "false"
    buckets = [0] * k

    def go(i):
        if i == len(nums):
            return True
        seen = set()
        for b in range(k):
            if buckets[b] in seen or buckets[b] + nums[i] > target:
                continue
            seen.add(buckets[b])
            buckets[b] += nums[i]
            if go(i + 1):
                return True
            buckets[b] -= nums[i]
        return False

    return "true" if go(0) else "false"


def _solve_matchsticks_to_square(lines):
    nums = list(map(int, lines[0].split()))
    total = sum(nums)
    if total % 4:
        return "false"
    side = total // 4
    nums.sort(reverse=True)
    if nums[0] > side:
        return "false"
    sides = [0] * 4

    def go(i):
        if i == len(nums):
            return True
        seen = set()
        for b in range(4):
            if sides[b] in seen or sides[b] + nums[i] > side:
                continue
            seen.add(sides[b])
            sides[b] += nums[i]
            if go(i + 1):
                return True
            sides[b] -= nums[i]
        return False

    return "true" if go(0) else "false"


def _solve_split_descending(lines):
    s = lines[0]

    def go(start, prev):
        if start == len(s):
            return True
        for end in range(start + 1, len(s) + 1):
            value = int(s[start:end])
            if prev is None or value == prev - 1:
                if go(end, value):
                    return True
        return False

    for end in range(1, len(s)):
        if go(end, int(s[:end])):
            return "true"
    return "false"


def _solve_max_unique_concat(lines):
    n = int(lines[0])
    words = [lines[1 + i] for i in range(n)]
    best = [0]

    def go(i, used):
        best[0] = max(best[0], len(used))
        for j in range(i, n):
            w = set(words[j])
            if len(w) == len(words[j]) and not (w & used):
                go(j + 1, used | w)

    go(0, set())
    return str(best[0])


def _solve_find_unique_binary_string(lines):
    n = int(lines[0])
    given = {lines[1 + i] for i in range(n)}
    for i in range(1 << n):
        cand = format(i, "0" + str(n) + "b")
        if cand not in given:
            return cand
    return ""


def _solve_sudoku_solver(lines):
    grid = [list(lines[i]) for i in range(9)]

    def ok(r, c, ch):
        for i in range(9):
            if grid[r][i] == ch or grid[i][c] == ch:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if grid[i][j] == ch:
                    return False
        return True

    def go():
        for r in range(9):
            for c in range(9):
                if grid[r][c] == "0":
                    for ch in "123456789":
                        if ok(r, c, ch):
                            grid[r][c] = ch
                            if go():
                                return True
                            grid[r][c] = "0"
                    return False
        return True

    go()
    return "\n".join("".join(row) for row in grid)


def _solve_word_search_ii(lines):
    m, n = map(int, lines[0].split())
    grid = [lines[1 + i].split() for i in range(m)]
    count = int(lines[1 + m])
    words = [lines[2 + m + i] for i in range(count)]
    found = []

    def can(word):
        def go(i, j, k, used):
            if k == len(word):
                return True
            if not (0 <= i < m and 0 <= j < n) or (i, j) in used:
                return False
            if grid[i][j] != word[k]:
                return False
            used.add((i, j))
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if go(i + di, j + dj, k + 1, used):
                    used.discard((i, j))
                    return True
            used.discard((i, j))
            return False

        return any(go(i, j, 0, set()) for i in range(m) for j in range(n))

    for w in words:
        if can(w):
            found.append(w)
    return " ".join(sorted(found))


def _solve_expression_add_operators(lines):
    num = lines[0]
    target = int(lines[1])
    out = []

    def go(pos, expr, value, last):
        if pos == len(num):
            if value == target:
                out.append(expr)
            return
        for end in range(pos + 1, len(num) + 1):
            piece = num[pos:end]
            if len(piece) > 1 and piece[0] == "0":
                break
            v = int(piece)
            if pos == 0:
                go(end, piece, v, v)
            else:
                go(end, expr + "+" + piece, value + v, v)
                go(end, expr + "-" + piece, value - v, -v)
                go(end, expr + "*" + piece, value - last + last * v, last * v)

    go(0, "", 0, 0)
    return "\n".join(sorted(out))


def _solve_remove_invalid_parentheses(lines):
    s = lines[0]

    def valid(t):
        bal = 0
        for c in t:
            if c == "(":
                bal += 1
            elif c == ")":
                bal -= 1
                if bal < 0:
                    return False
        return bal == 0

    level = {s}
    while level:
        good = sorted(t for t in level if valid(t))
        if good:
            return "\n".join(good)
        nxt = set()
        for t in level:
            for i in range(len(t)):
                if t[i] in "()":
                    nxt.add(t[:i] + t[i + 1:])
        level = nxt
    return ""


def _solve_permutation_sequence(lines):
    n, k = map(int, lines[0].split())
    import math
    digits = [str(i) for i in range(1, n + 1)]
    k -= 1
    out = []
    for i in range(n, 0, -1):
        f = math.factorial(i - 1)
        idx = k // f
        k %= f
        out.append(digits.pop(idx))
    return "".join(out)


def _solve_squareful_arrays(lines):
    nums = list(map(int, lines[0].split()))
    from itertools import permutations

    def square(x):
        r = int(x ** 0.5)
        while r * r < x:
            r += 1
        return r * r == x

    seen = set()
    for p in permutations(nums):
        if all(square(p[i] + p[i + 1]) for i in range(len(p) - 1)):
            seen.add(p)
    return str(len(seen))


def _solve_max_score_words(lines):
    n = int(lines[0])
    words = [lines[1 + i] for i in range(n)]
    letters = lines[1 + n].split()
    score = list(map(int, lines[2 + n].split()))
    from collections import Counter
    have = Counter(letters)
    best = [0]

    def go(i, pool, total):
        best[0] = max(best[0], total)
        for j in range(i, n):
            need = Counter(words[j])
            if all(pool[c] >= need[c] for c in need):
                gained = sum(score[ord(c) - 97] * need[c] for c in need)
                left = pool.copy()
                for c in need:
                    left[c] -= need[c]
                go(j + 1, left, total + gained)

    go(0, have, 0)
    return str(best[0])


PROBLEMS = [
{
        "title": "Subsets",
        "topic": "backtracking",
        "difficulty": "easy",
        "description": "Given an array of distinct integers, return all non-empty subsets, one per line: first all subsets of size 1 in input order, then all of size 2, and so on.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line of space-separated distinct integers. Output format: one subset per line, space-separated values, ordered by increasing size.",
        "solve": _solve_subsets,
        "sample_inputs": ["1 2 3", "4 5"],
        "hidden_inputs": [
            "5",      # single element
            "1",
            "1 2",
            "-1 -2",  # negative values
            "3 1 2",  # output follows input order, not sorted order
            "0 5 10",
            "1 2 3 4",
            "1 2 3 4 5",
            "7 8 9 10 11 12",
        ],
    },
{
        "title": "Permutations",
        "topic": "backtracking",
        "difficulty": "medium",
        "description": "Given an array of distinct integers, return all possible permutations, one per line, in the standard lexicographic order relative to the input.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line of space-separated distinct integers. Output format: one permutation per line, space-separated values.",
        "solve": _solve_permutations,
        "sample_inputs": ["1 2 3", "7 8"],
        "hidden_inputs": [
            "1",    # single element
            "1 2",
            "2 1",  # order is relative to the input
            "3 2 1",
            "-1 0 1",
            "1 2 3 4",
            "10 20 30",   # multi-digit values must not be split
            "5 6 7 8 9",
        ],
    },
{
        "title": "N-Queens Count",
        "topic": "backtracking",
        "difficulty": "hard",
        "description": "Given an integer n, return the number of distinct ways to place n queens on an n x n chessboard so that no two queens attack each other.",
        "example_input": "4",
        "constraints": "Input format: one line containing n. Output format: a single integer.",
        "solve": _solve_n_queens_count,
        "sample_inputs": ["4", "10"],
        "hidden_inputs": [
            "1",  # trivially one placement
            "2",  # no solution exists
            "3",  # no solution exists
            "5",
            "6",
            "7",
            "8",
            "9",
        ],
    },
{
        "title": "Combinations",
        "topic": "backtracking",
        "difficulty": "easy",
        "description": "Given two integers n and k, list every way of choosing k different numbers from 1 through n. Each choice is written in increasing order, and the choices themselves are listed in increasing order.",
        "example_input": "4 2",
        "constraints": "Input format: one line holding n and k (1 <= k <= n). Output format: one choice per line, values space-separated.",
        "solve": _solve_combinations,
        "sample_inputs": ["4 2", "3 3"],
        "hidden_inputs": [
            "1 1",                  # the only choice
            "2 1",                  # every single element
            "2 2",                  # the whole range
            "3 1",
            "3 2",
            "4 1",
            "4 4",                  # k equals n, one line
            "5 2",
            "5 3",
            "6 3",
        ],
    },
{
        "title": "Letter Case Permutation",
        "topic": "backtracking",
        "difficulty": "easy",
        "description": "Given a string of letters and digits, produce every string obtainable by changing the case of any of its letters. Digits are left alone. List the results in alphabetical order.",
        "example_input": "a1b2",
        "constraints": "Input format: one line containing the string. Output format: one string per line, alphabetically ordered.",
        "solve": _solve_letter_case_permutation,
        "sample_inputs": ["a1b2", "3z4"],
        "hidden_inputs": [
            "a",                    # a single letter
            "A",                    # already uppercase
            "1",                    # digits only, one result
            "12345",
            "ab",
            "aA",                   # the same letter in both cases
            "a1",
            "1a2",
            "abc",
            "z9y",
        ],
    },
{
        "title": "Generate Parentheses",
        "topic": "backtracking",
        "difficulty": "easy",
        "description": "Given n, list every string of n opening and n closing brackets in which each closing bracket is matched by an earlier opening one. List the strings in alphabetical order.",
        "example_input": "3",
        "constraints": "Input format: one line containing n (n >= 0). Output format: one string per line, alphabetically ordered; n = 0 produces no output.",
        "solve": _solve_generate_parentheses,
        "sample_inputs": ["3", "1"],
        "hidden_inputs": [
            "0",                    # nothing to build, empty output
            "2",                    # two arrangements
            "4",
            "5",
            "6",
            "7",
            "8",                    # 1430 arrangements; n=9 would put 92KB of
                                    # expected output into failure_detail and
                                    # straight onto the contest page
        ],
    },
{
        "title": "Subsets With Duplicates",
        "topic": "backtracking",
        "difficulty": "easy",
        "description": "Given a list of integers that may repeat, list every distinct non-empty subset. Each subset is written in increasing order; subsets are listed by size, and by value within a size.",
        "example_input": "1 2 2",
        "constraints": "Input format: one line of space-separated integers. Output format: one subset per line, values space-separated.",
        "solve": _solve_subsets_with_duplicates,
        "sample_inputs": ["1 2 2", "4 4 4 1 4"],
        "hidden_inputs": [
            "1",                    # a single element
            "1 1",                  # both copies give one subset each size
            "1 2",                  # no duplicates at all
            "2 1",                  # order in the input must not matter
            "0 0 0",
            "1 1 2 2",
            "-1 -1 0",              # negatives
            "5 5 5 5",
            "1 2 3",
            "3 2 1 2",
        ],
    },
{
        "title": "Letter Combinations of a Phone Number",
        "topic": "backtracking",
        "difficulty": "easy",
        "description": "On a telephone keypad 2 spells abc, 3 def, 4 ghi, 5 jkl, 6 mno, 7 pqrs, 8 tuv and 9 wxyz. Given a string of those digits, list every letter string it could spell, in alphabetical order.",
        "example_input": "23",
        "constraints": "Input format: one line of digits, each between 2 and 9. Output format: one string per line, alphabetically ordered.",
        "solve": _solve_letter_combinations,
        "sample_inputs": ["23", "2"],
        "hidden_inputs": [
            "9",                    # a four-letter key
            "7",                    # the other four-letter key
            "22",
            "29",
            "79",                   # sixteen results
            "234",
            "789",
            "222",
            "999",
            "2345",
        ],
    },
{
        "title": "Combination Sum",
        "topic": "backtracking",
        "difficulty": "medium",
        "description": "Given a list of distinct positive integers and a target, list every way of adding them up to the target. A number may be used any number of times. Each combination is written in increasing order, and combinations are listed in increasing order.",
        "example_input": "2 3 6 7\n7",
        "constraints": "Input format: line 1 is the space-separated distinct positive integers, line 2 is the target. Output format: one combination per line, values space-separated (empty if none).",
        "solve": _solve_combination_sum,
        "sample_inputs": ["2 3 6 7\n7", "2 3 5\n8"],
        "hidden_inputs": [
            "1\n1",                 # a single way
            "1\n3",                 # repetition of one value
            "2\n3",                 # unreachable, empty output
            "5\n5",
            "3 5\n8",
            "2 4\n6",
            "7 3 2\n18",
            "2 3 6 7\n1",           # target below every candidate
            "2 3 6 7\n6",
            "4 2 8\n8",
        ],
    },
{
        "title": "Combination Sum II",
        "topic": "backtracking",
        "difficulty": "medium",
        "description": "Given a list of positive integers that may repeat and a target, list every distinct way of adding them up to the target, using each listed number at most once. Each combination is written in increasing order, and combinations are listed in increasing order.",
        "example_input": "10 1 2 7 6 1 5\n8",
        "constraints": "Input format: line 1 is the space-separated positive integers, line 2 is the target. Output format: one combination per line, values space-separated (empty if none).",
        "solve": _solve_combination_sum_ii,
        "sample_inputs": ["10 1 2 7 6 1 5\n8", "2 5 2 1 2\n5"],
        "hidden_inputs": [
            "1\n1",                 # the single element matches
            "1\n2",                 # cannot reuse it, empty output
            "1 1\n2",               # two copies make the target
            "2 2 2\n4",             # duplicates must not repeat a line
            "3\n3",
            "1 2 3\n6",             # the whole list
            "1 2 3\n7",             # just out of reach
            "4 4 4 4\n8",
            "1 1 1 1\n2",
            "2 3 4 5\n7",
        ],
    },
{
        "title": "Permutations With Duplicates",
        "topic": "backtracking",
        "difficulty": "medium",
        "description": "Given a list of integers that may repeat, list every distinct ordering of them, in increasing order as sequences.",
        "example_input": "1 1 2",
        "constraints": "Input format: one line of space-separated integers. Output format: one ordering per line, values space-separated.",
        "solve": _solve_permutations_with_duplicates,
        "sample_inputs": ["1 1 2", "1 2 3"],
        "hidden_inputs": [
            "1",                    # one ordering
            "1 1",                  # identical values give one ordering
            "2 1",                  # output is sorted regardless of input order
            "0 0 0",
            "1 1 1 1",
            "1 2 2",
            "-1 0 1",               # negatives
            "3 3 1 1",
            "1 2 3 4",
            "2 2 1 1",
        ],
    },
{
        "title": "Palindrome Partitioning",
        "topic": "backtracking",
        "difficulty": "medium",
        "description": "Split a string into consecutive pieces so that every piece reads the same forwards and backwards. List every possible splitting, in alphabetical order when each splitting is written as its pieces separated by spaces.",
        "example_input": "aab",
        "constraints": "Input format: one line containing the string (lowercase). Output format: one splitting per line, pieces space-separated.",
        "solve": _solve_palindrome_partitioning,
        "sample_inputs": ["aab", "a"],
        "hidden_inputs": [
            "ab",                   # only the single-letter split works
            "aa",                   # two splittings
            "aaa",
            "aba",                  # the whole string is a palindrome
            "abc",                  # nothing longer than one letter
            "abba",
            "aabb",
            "racecar",
            "abcba",
            "aaaa",                 # the most splittings for its length
        ],
    },
{
        "title": "Word Search",
        "topic": "backtracking",
        "difficulty": "hard",
        "description": "Decide whether a word can be spelled out in a grid of letters by stepping between cells that share an edge, never using the same cell twice.",
        "example_input": "3 4\nA B C E\nS F C S\nA D E E\nABCCED",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated letters, then a final line holding the word. Output format: \"true\" or \"false\".",
        "solve": _solve_word_search,
        "sample_inputs": ["3 4\nA B C E\nS F C S\nA D E E\nABCCED", "3 4\nA B C E\nS F C S\nA D E E\nABCB"],
        "hidden_inputs": [
            "1 1\nA\nA",            # the whole grid is the word
            "1 1\nA\nB",            # the letter is wrong
            "1 1\nA\nAA",           # a cell cannot be reused
            "1 2\nA B\nAB",
            "1 2\nA B\nBA",         # the path may run right to left
            "2 2\nA B\nC D\nABDC",  # a path that turns
            "2 2\nA A\nA A\nAAAA",  # every cell used exactly once
            "2 2\nA A\nA A\nAAAAA", # one letter too many
            "3 3\nA B C\nD E F\nG H I\nAEI",   # diagonals are not allowed
            "3 4\nA B C E\nS F C S\nA D E E\nSEE",
        ],
    },
{
        "title": "N-Queens Solutions",
        "topic": "backtracking",
        "difficulty": "hard",
        "description": "Place n queens on an n by n board so that no two share a row, a column or a diagonal. List every arrangement by giving, for each row from the top, the column its queen occupies. Arrangements are listed in increasing order as sequences.",
        "example_input": "4",
        "constraints": "Input format: one line containing n. Output format: one arrangement per line as n space-separated column numbers counting from zero (empty if none exist).",
        "solve": _solve_n_queens_solutions,
        "sample_inputs": ["4", "1"],
        "hidden_inputs": [
            "2",                    # no arrangement exists
            "3",                    # likewise
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",                   # 724 arrangements, as large as stays sane
        ],
    },
{
        "title": "Binary Watch",
        "topic": "backtracking", "difficulty": "easy",
        "description": "A watch shows the hour with four lamps and the minute with six. Given how many lamps are lit in total, list every time it could be showing, hours from 0 to 11 and minutes written with two digits, in increasing order of time.",
        "example_input": "1",
        "constraints": "Input format: one line containing the number of lit lamps (0 to 10). Output format: the times space-separated as \"h:mm\" (empty if none).",
        "solve": _solve_binary_watch,
        "sample_inputs": ["1", "9"],
        "hidden_inputs": [
            "0",                    # only midnight
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "10",                   # no time has ten lamps lit
        ],
    },
{
        "title": "Count Sorted Vowel Strings",
        "topic": "backtracking", "difficulty": "easy",
        "description": "Count the strings of the given length made only of vowels in which the letters never go backwards alphabetically.",
        "example_input": "2",
        "constraints": "Input format: one line containing the length (at least 1). Output format: a single integer.",
        "solve": _solve_count_vowel_strings,
        "sample_inputs": ["2", "33"],
        "hidden_inputs": [
            "1",                    # the five vowels themselves
            "3",
            "4",
            "5",
            "10",
            "15",
            "20",
            "25",
            "40",
            "50",
        ],
    },
{
        "title": "Combination Sum III",
        "topic": "backtracking", "difficulty": "easy",
        "description": "Find every way of choosing exactly k different digits from 1 to 9 that add up to n. Write each choice in increasing order, and list the choices in increasing order.",
        "example_input": "3 7",
        "constraints": "Input format: one line holding k and n. Output format: one choice per line, digits space-separated (empty if none).",
        "solve": _solve_combination_sum_iii,
        "sample_inputs": ["3 7", "3 9"],
        "hidden_inputs": [
            "1 1",                  # a single digit
            "1 9",
            "1 10",                 # no single digit reaches ten
            "2 3",
            "2 18",                 # impossible for two digits
            "3 15",
            "4 1",                  # far too small
            "9 45",                 # every digit, the only way
            "9 44",                 # one short, impossible
            "2 5",
        ],
    },
{
        "title": "Count Numbers with Unique Digits",
        "topic": "backtracking", "difficulty": "easy",
        "description": "Count the whole numbers from zero up to but not including ten raised to the power n whose digits are all different.",
        "example_input": "2",
        "constraints": "Input format: one line containing n (0 to 10). Output format: a single integer.",
        "solve": _solve_count_unique_digit_numbers,
        "sample_inputs": ["2", "0"],
        "hidden_inputs": [
            "1",                    # the ten single digits
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",                   # beyond this nothing new can be added
            "11",
        ],
    },
{
        "title": "Letter Tile Possibilities",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Given tiles each printed with one letter, count the different non-empty sequences that can be spelled by laying some of them in a row. Tiles printed with the same letter cannot be told apart.",
        "example_input": "AAB",
        "constraints": "Input format: one line of capital letters. Output format: a single integer.",
        "solve": _solve_letter_tile_possibilities,
        "sample_inputs": ["AAB", "AAABBC"],
        "hidden_inputs": [
            "A",                    # one tile
            "AA",                   # identical tiles
            "AB",
            "AAA",
            "ABC",
            "AABB",
            "ABCD",
            "AAAA",
            "AABC",
            "V",
        ],
    },
{
        "title": "Restore IP Addresses",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Insert three dots into a string of digits so that it reads as four numbers, each between 0 and 255, none written with a leading zero unless it is zero itself. List every possibility in increasing order.",
        "example_input": "25525511135",
        "constraints": "Input format: one line of digits. Output format: one address per line (empty if none).",
        "solve": _solve_restore_ip_addresses,
        "sample_inputs": ["25525511135", "0000"],
        "hidden_inputs": [
            "1",                    # far too short
            "111",
            "1111",                 # exactly one way
            "0101",
            "1234",
            "12345",
            "255255255255",
            "010010",
            "101023",
            "99999999999999",       # far too long
        ],
    },
{
        "title": "Beautiful Arrangement",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Count the ways to arrange the numbers 1 to n in a row so that at every position, either the number divides its position or the position divides the number, counting positions from one.",
        "example_input": "2",
        "constraints": "Input format: one line containing n (1 to 12). Output format: a single integer.",
        "solve": _solve_beautiful_arrangement,
        "sample_inputs": ["2", "1"],
        "hidden_inputs": [
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "10",
            "11",
            "12",
        ],
    },
{
        "title": "Partition to K Equal Sum Subsets",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Decide whether the values can be split into exactly k groups that all add up to the same total.",
        "example_input": "4 3 2 3 5 2 1\n4",
        "constraints": "Input format: line 1 is the space-separated positive integers, line 2 is k. Output format: \"true\" or \"false\".",
        "solve": _solve_partition_k_equal_subsets,
        "sample_inputs": ["4 3 2 3 5 2 1\n4", "1 2 3 4\n3"],
        "hidden_inputs": [
            "1\n1",                 # one group holding everything
            "1 1\n2",
            "1 2\n2",               # the totals cannot match
            "2 2 2 2\n4",
            "2 2 2 2\n2",
            "1 1 1 1\n3",           # the total does not divide by three
            "4 4 4 4 4 4\n3",
            "1 1 1 1 2 2 2 2\n4",
            "10 10 10 7 7 7 7 7 7 6 6 6\n3",
            "3 3 3 3 3\n5",
        ],
    },
{
        "title": "Matchsticks to Square",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Decide whether every matchstick can be used, unbroken, to form the four sides of a square.",
        "example_input": "1 1 2 2 2",
        "constraints": "Input format: one line of space-separated positive lengths. Output format: \"true\" or \"false\".",
        "solve": _solve_matchsticks_to_square,
        "sample_inputs": ["1 1 2 2 2", "3 3 3 3 4"],
        "hidden_inputs": [
            "1",                    # too few sticks
            "1 1 1 1",              # one per side
            "1 1 1 2",              # the total does not divide by four
            "2 2 2 2",
            "1 1 2 2 2 2 4",
            "5 5 5 5 4 4 4 4 3 3 3 3",
            "1 1 1 1 1 1 1 1",
            "4 4 4 4 4",            # one stick too many
            "10 6 5 5 5 3 3 3 2 2 2 2",
            "1 2 3 4",
        ],
    },
{
        "title": "Splitting a String Into Descending Consecutive Values",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Decide whether a string of digits can be cut into two or more pieces whose values, read in order, each fall exactly one below the piece before. Leading zeroes inside a piece are allowed.",
        "example_input": "1234",
        "constraints": "Input format: one line of digits. Output format: \"true\" or \"false\".",
        "solve": _solve_split_descending,
        "sample_inputs": ["1234", "050043"],
        "hidden_inputs": [
            "1",                    # cannot be cut at all
            "10",                   # one then zero
            "21",
            "12",                   # rising, not falling
            "11",                   # equal, not falling
            "321",
            "9876543210",
            "010",                  # leading zeroes are allowed
            "1234567890",
            "99998",
        ],
    },
{
        "title": "Maximum Length of a Concatenated String with Unique Characters",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Join together some of the given strings, keeping their order, so that no letter is used twice in the result. Return the greatest possible length.",
        "example_input": "3\nun\niq\nue",
        "constraints": "Input format: line 1 is the number of strings, followed by that many lowercase strings. Output format: a single integer.",
        "solve": _solve_max_unique_concat,
        "sample_inputs": ["3\nun\niq\nue", "3\ncha\nr\nact"],
        "hidden_inputs": [
            "1\na",                 # a single string
            "1\naa",                # its own letters clash, so nothing
            "2\na\na",              # the two clash with each other
            "2\na\nb",
            "2\nab\nba",            # same letters, cannot combine
            "3\na\nb\nc",
            "4\nab\ncd\nef\ngh",
            "2\nabcdefghijklmnopqrstuvwxyz\na",
            "3\naa\nbb\ncc",        # every string clashes with itself
            "4\nabc\nbcd\ncde\ndef",
        ],
    },
{
        "title": "Find Unique Binary String",
        "topic": "backtracking", "difficulty": "medium",
        "description": "Given several different binary strings, all of the same length as the number of strings, return the smallest binary string of that length which is not among them.",
        "example_input": "3\n011\n101\n110",
        "constraints": "Input format: line 1 is the number of strings, followed by that many binary strings of that same length. Output format: the missing string.",
        "solve": _solve_find_unique_binary_string,
        "sample_inputs": ["3\n011\n101\n110", "2\n00\n01"],
        "hidden_inputs": [
            "1\n0",                 # only one string of length one is used
            "1\n1",
            "2\n01\n10",
            "2\n10\n11",
            "2\n11\n10",
            "3\n000\n001\n010",
            "3\n111\n110\n101",
            "3\n100\n010\n001",
            "4\n0000\n0001\n0010\n0011",
            "4\n1111\n1110\n1101\n1100",
        ],
    },
{
        "title": "Sudoku Solver",
        "topic": "backtracking", "difficulty": "hard",
        "description": "Fill every empty square of a nine by nine puzzle so that each row, each column and each of the nine smaller three by three boxes holds the digits one to nine exactly once. Exactly one solution exists.",
        "example_input": "530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079",
        "constraints": "Input format: nine lines of nine characters each, using 0 for an empty square. Output format: the completed puzzle in the same layout.",
        "solve": _solve_sudoku_solver,
        "sample_inputs": [
            "530070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079",
            "123456780\n456780123\n780123456\n234567801\n567801234\n801234567\n345678012\n678012345\n012345678",
        ],
        "hidden_inputs": [
            "123456789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "023456789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "003456789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "000456789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "000056789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "000000789\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "000000000\n456789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "000000000\n000789123\n789123456\n214365897\n365897214\n897214365\n531642978\n642978531\n978531642",
            "534678912\n672195348\n198342567\n859761423\n426853791\n713924856\n961537284\n287419635\n345286179",
            "500070000\n600195000\n098000060\n800060003\n400803001\n700020006\n060000280\n000419005\n000080079",
        ],
    },
{
        "title": "Word Search II",
        "topic": "backtracking", "difficulty": "hard",
        "description": "Given a grid of letters and a list of words, report which of the words can be spelled by stepping between cells that share an edge, never using the same cell twice within one word. List them in alphabetical order.",
        "example_input": "4 4\no a a n\ne t a e\ni h k r\ni f l v\n4\noath\npea\neat\nrain",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated letters, then a line holding the word count, then that many words. Output format: the words found, space-separated (empty if none).",
        "solve": _solve_word_search_ii,
        "sample_inputs": [
            "4 4\no a a n\ne t a e\ni h k r\ni f l v\n4\noath\npea\neat\nrain",
            "2 2\na b\nc d\n1\nabcd",
        ],
        "hidden_inputs": [
            "1 1\na\n1\na",                     # the whole grid is the word
            "1 1\na\n1\nb",                     # not present
            "1 1\na\n1\naa",                    # a cell cannot be reused
            "1 2\na b\n2\nab\nba",              # both directions work
            "2 2\na a\na a\n1\naaaa",           # every cell used once
            "2 2\na a\na a\n1\naaaaa",          # one letter too many
            "2 2\na b\nc d\n3\nab\nac\nbd",
            "3 3\na b c\nd e f\ng h i\n2\nabc\naei",   # diagonals are not allowed
            "2 3\nc a t\nd o g\n3\ncat\ndog\ncod",
            "2 2\na b\nc d\n2\nzz\nyy",         # nothing is found
        ],
    },
{
        "title": "Expression Add Operators",
        "topic": "backtracking", "difficulty": "hard",
        "description": "Insert plus, minus and times signs between the digits of a string, without reordering them, so that the expression works out to the target. Multiplication binds tighter than addition and subtraction, and no number may be written with a leading zero. List every expression in increasing order.",
        "example_input": "123\n6",
        "constraints": "Input format: line 1 is the digit string, line 2 is the target. Output format: one expression per line (empty if none).",
        "solve": _solve_expression_add_operators,
        "sample_inputs": ["123\n6", "232\n8"],
        "hidden_inputs": [
            "1\n1",                 # the digit alone
            "1\n2",                 # no expression works
            "0\n0",
            "12\n3",
            "12\n12",               # the digits joined
            "105\n5",               # a leading zero blocks some splits
            "00\n0",
            "123\n7",
            "2147\n2",
            "34562374\n9191",       # no expression reaches it
        ],
    },
{
        "title": "Remove Invalid Parentheses",
        "topic": "backtracking", "difficulty": "hard",
        "description": "Delete as few brackets as possible so that the string becomes properly matched. List every distinct result achievable with that fewest number of deletions, in increasing order.",
        "example_input": "()())()",
        "constraints": "Input format: one line containing brackets and lowercase letters. Output format: one result per line.",
        "solve": _solve_remove_invalid_parentheses,
        "sample_inputs": ["()())()", "(a)())()"],
        "hidden_inputs": [
            "",                     # nothing to do
            "a",                    # no brackets at all
            "(",                    # one deletion
            ")",
            "()",                   # already valid
            ")(",                   # both must go
            "(((",
            "()()",
            "n",
            "(a(b(c)d)",
        ],
    },
{
        "title": "Permutation Sequence",
        "topic": "backtracking", "difficulty": "hard",
        "description": "Write out every arrangement of the digits 1 to n in increasing order and return the kth of them.",
        "example_input": "3 3",
        "constraints": "Input format: one line holding n and k, where k is at most n factorial. Output format: the arrangement as a string of digits.",
        "solve": _solve_permutation_sequence,
        "sample_inputs": ["3 3", "4 9"],
        "hidden_inputs": [
            "1 1",                  # the only arrangement
            "2 1",                  # the first
            "2 2",                  # the last
            "3 1",
            "3 6",
            "4 1",
            "4 24",
            "5 60",
            "6 720",
            "9 362880",             # the very last of nine digits
        ],
    },
{
        "title": "Number of Squareful Arrays",
        "topic": "backtracking", "difficulty": "hard",
        "description": "Count the different arrangements of the values in which every pair of neighbours adds up to a perfect square. Arrangements that read identically count once.",
        "example_input": "1 17 8",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: a single integer.",
        "solve": _solve_squareful_arrays,
        "sample_inputs": ["1 17 8", "2 2 2"],
        "hidden_inputs": [
            "1",                    # a single value is trivially fine
            "0",
            "0 0",                  # zero plus zero is a square
            "1 3",                  # four is a square
            "1 2",                  # three is not
            "2 2",
            "1 8 17",
            "0 1 3",
            "4 5 11 20",
            "1 1 1 1",
        ],
    },
{
        "title": "Maximum Score Words Formed by Letters",
        "topic": "backtracking", "difficulty": "hard",
        "description": "Choose some of the words so that the letters available are enough to spell all of them together. Each letter carries a score, and a word scores the total of its letters. Return the greatest score obtainable.",
        "example_input": "4\ndog\ncat\ndad\ngood\nd o g o a t i i g\n1 0 9 5 0 0 3 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0",
        "constraints": "Input format: line 1 is the number of words, followed by that many lowercase words, then a line of the available letters space-separated, then a line of twenty-six scores for a through z. Output format: a single integer.",
        "solve": _solve_max_score_words,
        "sample_inputs": [
            "4\ndog\ncat\ndad\ngood\nd o g o a t i i g\n1 0 9 5 0 0 3 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0",
            "3\nxxxz\nax\nbx\nz a b x x x z\n4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5",
        ],
        "hidden_inputs": [
            "1\na\na\n1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "1\na\nb\n1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "1\naa\na\n1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "1\naa\na a\n1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "2\na\nb\na b\n1 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "2\na\na\na\n5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "2\nab\nba\na b\n1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "1\nabc\na b c\n0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "3\na\nb\nc\na b c\n1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0",
            "2\nleet\ncode\nl e e t c o d e\n0 0 1 1 1 0 0 0 0 0 0 1 0 0 1 0 0 0 0 1 0 0 0 0 0 0",
        ],
    },
]
