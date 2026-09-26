"""String problems."""

def _solve_valid_anagram(lines):
    s, t = lines[0], lines[1]
    return "true" if sorted(s) == sorted(t) else "false"


def _solve_longest_substr_no_repeat(lines):
    s = lines[0]
    seen = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in seen and seen[ch] >= left:
            left = seen[ch] + 1
        seen[ch] = right
        best = max(best, right - left + 1)
    return str(best)


def _solve_longest_palindrome(lines):
    s = lines[0]
    if not s:
        return ""
    start, maxlen = 0, 1

    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return l + 1, r - 1

    for i in range(len(s)):
        l1, r1 = expand(i, i)
        if r1 - l1 + 1 > maxlen:
            start, maxlen = l1, r1 - l1 + 1
        l2, r2 = expand(i, i + 1)
        if r2 - l2 + 1 > maxlen:
            start, maxlen = l2, r2 - l2 + 1
    return s[start:start + maxlen]

def _solve_reverse_string(lines):
    return lines[0][::-1]


def _solve_valid_palindrome(lines):
    s = "".join(c.lower() for c in lines[0] if c.isalnum())
    return "true" if s == s[::-1] else "false"


def _solve_longest_common_prefix(lines):
    n = int(lines[0])
    words = [lines[1 + i] for i in range(n)]
    if not words:
        return ""
    prefix = words[0]
    for w in words[1:]:
        while not w.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def _solve_first_unique_char(lines):
    s = lines[0]
    from collections import Counter
    counts = Counter(s)
    for i, c in enumerate(s):
        if counts[c] == 1:
            return str(i)
    return "-1"


def _solve_first_occurrence(lines):
    haystack = lines[0]
    needle = lines[1] if len(lines) > 1 else ""
    if not needle:
        return "0"
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return str(i)
    return "-1"


def _solve_group_anagrams(lines):
    n = int(lines[0])
    words = [lines[1 + i] for i in range(n)]
    groups = {}
    for w in words:
        groups.setdefault("".join(sorted(w)), []).append(w)
    ordered = sorted(sorted(g) for g in groups.values())
    return "\n".join(" ".join(g) for g in ordered)


def _solve_string_compression(lines):
    s = lines[0]
    if not s:
        return ""
    out = []
    run = 1
    for i in range(1, len(s) + 1):
        if i < len(s) and s[i] == s[i - 1]:
            run += 1
        else:
            out.append(s[i - 1] if run == 1 else s[i - 1] + str(run))
            run = 1
    return "".join(out)


def _solve_zigzag_conversion(lines):
    s = lines[0]
    rows = int(lines[1])
    if rows == 1 or rows >= len(s):
        return s
    buckets = [[] for _ in range(rows)]
    r = 0
    step = 1
    for c in s:
        buckets[r].append(c)
        if r == 0:
            step = 1
        elif r == rows - 1:
            step = -1
        r += step
    return "".join("".join(b) for b in buckets)


def _solve_multiply_strings(lines):
    a = lines[0]
    b = lines[1]
    if a == "0" or b == "0":
        return "0"
    result = [0] * (len(a) + len(b))
    for i in range(len(a) - 1, -1, -1):
        for j in range(len(b) - 1, -1, -1):
            result[i + j + 1] += int(a[i]) * int(b[j])
    for k in range(len(result) - 1, 0, -1):
        result[k - 1] += result[k] // 10
        result[k] %= 10
    digits = "".join(map(str, result)).lstrip("0")
    return digits or "0"


def _solve_longest_valid_parentheses(lines):
    s = lines[0]
    stack = [-1]
    best = 0
    for i, c in enumerate(s):
        if c == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                best = max(best, i - stack[-1])
    return str(best)


def _solve_word_break_ii(lines):
    s = lines[0]
    n = int(lines[1])
    words = set(lines[2 + i] for i in range(n))
    memo = {}

    def go(i):
        if i == len(s):
            return [""]
        if i in memo:
            return memo[i]
        out = []
        for j in range(i + 1, len(s) + 1):
            head = s[i:j]
            if head in words:
                for rest in go(j):
                    out.append(head if rest == "" else head + " " + rest)
        memo[i] = out
        return out

    return "\n".join(sorted(go(0)))

def _solve_length_of_last_word(lines):
    parts = lines[0].split()
    return str(len(parts[-1]) if parts else 0)


def _solve_to_lower_case(lines):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in lines[0])


def _solve_reverse_words_iii(lines):
    return " ".join(w[::-1] for w in lines[0].split(" "))


def _solve_detect_capital(lines):
    word = lines[0]
    if word.isupper() or word.islower():
        return "true"
    return "true" if word[0].isupper() and word[1:].islower() else "false"


def _solve_reverse_words(lines):
    return " ".join(reversed(lines[0].split()))


def _solve_count_and_say(lines):
    n = int(lines[0])
    text = "1"
    for _ in range(n - 1):
        out = []
        i = 0
        while i < len(text):
            j = i
            while j < len(text) and text[j] == text[i]:
                j += 1
            out.append(str(j - i))
            out.append(text[i])
            i = j
        text = "".join(out)
    return text


def _solve_longest_palindromic_subsequence(lines):
    s = lines[0]
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return str(dp[0][n - 1]) if n else "0"


def _solve_longest_repeating_substring(lines):
    s = lines[0]
    best = 0
    seen = {}
    for length in range(1, len(s)):
        window = set()
        found = False
        for i in range(len(s) - length + 1):
            piece = s[i:i + length]
            if piece in window:
                found = True
                break
            window.add(piece)
        if found:
            best = length
    return str(best)


def _solve_decode_ways_ii(lines):
    s = lines[0]
    MOD = 10 ** 9 + 7

    def one(ch):
        if ch == "*":
            return 9
        return 0 if ch == "0" else 1

    def two(a, b):
        if a == "*" and b == "*":
            return 15
        if a == "*":
            return 2 if b <= "6" else 1
        if b == "*":
            if a == "1":
                return 9
            if a == "2":
                return 6
            return 0
        value = int(a + b)
        return 1 if 10 <= value <= 26 else 0

    prev2, prev1 = 1, one(s[0])
    for i in range(1, len(s)):
        cur = (prev1 * one(s[i]) + prev2 * two(s[i - 1], s[i])) % MOD
        prev2, prev1 = prev1, cur
    return str(prev1 % MOD)


def _solve_word_pattern(lines):
    pattern = lines[0]
    words = lines[1].split()
    if len(pattern) != len(words):
        return "false"
    forward, backward = {}, {}
    for c, w in zip(pattern, words):
        if forward.setdefault(c, w) != w:
            return "false"
        if backward.setdefault(w, c) != c:
            return "false"
    return "true"


def _solve_isomorphic_strings(lines):
    a = lines[0]
    b = lines[1] if len(lines) > 1 else ""
    if len(a) != len(b):
        return "false"
    forward, backward = {}, {}
    for x, y in zip(a, b):
        if forward.setdefault(x, y) != y:
            return "false"
        if backward.setdefault(y, x) != x:
            return "false"
    return "true"


def _solve_repeated_substring_pattern(lines):
    s = lines[0]
    n = len(s)
    for size in range(1, n // 2 + 1):
        if n % size == 0 and s[:size] * (n // size) == s:
            return "true"
    return "false"


def _solve_reverse_only_letters(lines):
    s = list(lines[0])
    i, j = 0, len(s) - 1
    while i < j:
        if not s[i].isalpha():
            i += 1
        elif not s[j].isalpha():
            j -= 1
        else:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
    return "".join(s)


def _solve_compare_version(lines):
    a = [int(x) for x in lines[0].split(".")]
    b = [int(x) for x in lines[1].split(".")]
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else 0
        y = b[i] if i < len(b) else 0
        if x != y:
            return "1" if x > y else "-1"
    return "0"


def _solve_shortest_palindrome(lines):
    s = lines[0]
    if not s:
        return ""
    combined = s + "#" + s[::-1]
    fail = [0] * len(combined)
    for i in range(1, len(combined)):
        k = fail[i - 1]
        while k and combined[i] != combined[k]:
            k = fail[k - 1]
        if combined[i] == combined[k]:
            k += 1
        fail[i] = k
    return s[fail[-1]:][::-1] + s


def _solve_valid_palindrome_iii(lines):
    s = lines[0]
    k = int(lines[1])
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return "true" if n - dp[0][n - 1] <= k else "false"


def _solve_longest_duplicate_substring(lines):
    # str.count() counts only NON-overlapping occurrences, so it reports
    # "ana" as appearing once in "banana". The statement allows overlap, so
    # this walks the positions itself, longest length first, and returns the
    # repeated stretch whose first appearance comes earliest.
    s = lines[0]
    n = len(s)
    for length in range(n - 1, 0, -1):
        first = {}
        repeated = {}
        for i in range(n - length + 1):
            piece = s[i:i + length]
            if piece in first:
                if piece not in repeated:
                    repeated[piece] = first[piece]
            else:
                first[piece] = i
        if repeated:
            return min(repeated.items(), key=lambda kv: kv[1])[0]
    return ""


def _solve_string_to_integer(lines):
    s = lines[0]
    i = 0
    while i < len(s) and s[i] == " ":
        i += 1
    sign = 1
    if i < len(s) and s[i] in "+-":
        sign = -1 if s[i] == "-" else 1
        i += 1
    value = 0
    while i < len(s) and s[i].isdigit():
        value = value * 10 + int(s[i])
        i += 1
    value *= sign
    return str(max(-2 ** 31, min(2 ** 31 - 1, value)))


def _solve_count_binary_substrings(lines):
    s = lines[0]
    groups = []
    i = 0
    while i < len(s):
        j = i
        while j < len(s) and s[j] == s[i]:
            j += 1
        groups.append(j - i)
        i = j
    return str(sum(min(groups[i], groups[i + 1]) for i in range(len(groups) - 1)))


PROBLEMS = [
{
        "title": "Valid Anagram",
        "topic": "string",
        "difficulty": "easy",
        "description": "Given two strings s and t, determine if t is an anagram of s (uses exactly the same letters, same counts).",
        "example_input": "anagram\nnagaram",
        "constraints": "Input format: line 1 is s, line 2 is t. Output format: \"true\" or \"false\".",
        "solve": _solve_valid_anagram,
        "sample_inputs": ["anagram\nnagaram", "car\nrac"],
        "hidden_inputs": [
            "a\na",
            "a\nb",
            "a\nab",       # different lengths
            "ab\nba",
            "ab\nab",
            "xy\nxx",      # same length, wrong letter counts
            "aacc\nccac",  # same letter set, different multiplicities
            "rat\ncar",
            "aaa\naaa",
            "listen\nsilent",
            "abcdefghij\njihgfedcba",
        ],
    },
{
        "title": "Longest Substring Without Repeating Characters",
        "topic": "string",
        "difficulty": "medium",
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "example_input": "abcabcbb",
        "constraints": "Input format: one line containing s. Output format: a single integer.",
        "solve": _solve_longest_substr_no_repeat,
        "sample_inputs": ["abcabcbb", "abcde"],
        "hidden_inputs": [
            "a",
            "aa",
            "ab",
            "aab",
            "au",
            "abba",     # index must not rewind behind the window start
            "dvdf",     # repeat sits outside the current window
            "bbbbb",
            "pwwkew",
            "tmmzuxt",
            "abcdefg",  # no repeats at all
        ],
    },
{
        "title": "Longest Palindromic Substring",
        "topic": "string",
        "difficulty": "hard",
        "description": "Given a string s, return the longest palindromic substring in s. If there are multiple, return the one found by scanning left to right and expanding around each center first.",
        "example_input": "babad",
        "constraints": "Input format: one line containing s. Output format: the substring itself.",
        "solve": _solve_longest_palindrome,
        "sample_inputs": ["babad", "forgeeksskeegfor"],
        "hidden_inputs": [
            "a",
            "aa",
            "ab",       # no palindrome longer than 1 -> leftmost single char
            "aaa",
            "ccc",
            "cbbd",
            "abcda",    # ties resolved by the leftmost center
            "bananas",
            "racecar",  # whole string is the answer
            "aacabdkacaa",
            "abacdfgdcaba",
        ],
    },
{
        "title": "Reverse String",
        "topic": "string",
        "difficulty": "easy",
        "description": "Return the given string with its characters in the opposite order.",
        "example_input": "hello",
        "constraints": "Input format: one line containing the string. Output format: the reversed string.",
        "solve": _solve_reverse_string,
        "sample_inputs": ["hello", "Hannah"],
        "hidden_inputs": [
            "a",                    # a single character
            "ab",
            "aa",                   # reversal changes nothing
            "aba",                  # a palindrome
            "abcdef",
            "AbCdE",                # case is preserved exactly
            "12345",
            "a1b2c3",
            "racecar",
            "zyxwvutsrqponmlkjihgfedcba",
        ],
    },
{
        "title": "Valid Palindrome",
        "topic": "string",
        "difficulty": "easy",
        "description": "Ignoring every character that is not a letter or digit, and treating upper and lower case as the same, decide whether the string reads the same forwards and backwards.",
        "example_input": "A man, a plan, a canal: Panama",
        "constraints": "Input format: one line containing the string, with no leading or trailing spaces. Output format: \"true\" or \"false\".",
        "solve": _solve_valid_palindrome,
        "sample_inputs": ["A man, a plan, a canal: Panama", "race a car"],
        "hidden_inputs": [
            "a",                    # a single letter
            "ab",
            "aA",                   # case must be folded
            ".,",                   # nothing but punctuation
            "0P",                   # a digit and a letter, not a palindrome
            "1a1",
            "ab@ba",                # punctuation in the middle is skipped
            "No lemon, no melon",
            "Was it a car or a cat I saw?",
            "Almost a palindrome!",
        ],
    },
{
        "title": "Longest Common Prefix",
        "topic": "string",
        "difficulty": "easy",
        "description": "Return the longest string that begins every one of the given words. If there is no such string, return nothing.",
        "example_input": "3\nflower\nflow\nflight",
        "constraints": "Input format: line 1 is the number of words, followed by that many lowercase words. Output format: the common prefix, or an empty line if there is none.",
        "solve": _solve_longest_common_prefix,
        "sample_inputs": ["3\nflower\nflow\nflight", "3\ndog\nracecar\ncar"],
        "hidden_inputs": [
            "1\nalone",             # one word is its own prefix
            "2\na\na",              # identical single letters
            "2\na\nb",              # nothing in common
            "2\nab\nabc",           # one word is a prefix of the other
            "2\nabc\nab",           # the same pair reversed
            "3\naaa\naab\naac",
            "3\nc\nacc\nccc",       # the first letter already differs
            "4\nprefix\nprefer\npremium\nprevent",
            "2\nsame\nsame",
            "5\nab\nab\nab\nab\nac",
        ],
    },
{
        "title": "First Unique Character in a String",
        "topic": "string",
        "difficulty": "easy",
        "description": "Return the position of the first character that appears exactly once in the string, counting from zero, or -1 if every character repeats.",
        "example_input": "leetcode",
        "constraints": "Input format: one line containing the lowercase string. Output format: a single integer.",
        "solve": _solve_first_unique_char,
        "sample_inputs": ["leetcode", "loveleetcode"],
        "hidden_inputs": [
            "a",                    # the only character
            "aa",                   # everything repeats
            "ab",                   # the first character wins
            "aab",                  # the answer is not at index 0
            "aabb",
            "abab",
            "abcabc",               # nothing is unique
            "abcabd",               # the unique one is last
            "zzzzzzzzzy",
            "dddccdbba",            # the unique one sits at the very end
        ],
    },
{
        "title": "Find the Index of the First Occurrence",
        "topic": "string",
        "difficulty": "easy",
        "description": "Return the position at which the second string first appears inside the first, counting from zero, or -1 if it never does.",
        "example_input": "sadbutsad\nsad",
        "constraints": "Input format: line 1 is the haystack, line 2 is the needle, both lowercase and non-empty. Output format: a single integer.",
        "solve": _solve_first_occurrence,
        "sample_inputs": ["sadbutsad\nsad", "leetcode\nleeto"],
        "hidden_inputs": [
            "a\na",                 # the whole string matches
            "a\nb",                 # no match at all
            "ab\nb",                # a match at the end
            "b\nab",                # the needle is longer
            "aaa\naa",              # overlapping matches, take the first
            "abab\nab",
            "abab\nba",             # the match starts at index 1
            "mississippi\nissip",
            "hello\nll",
            "aaaaa\naaaaa",
        ],
    },
{
        "title": "Group Anagrams",
        "topic": "string",
        "difficulty": "medium",
        "description": "Collect the given words into groups, where two words belong together when one is a rearrangement of the other. Sort the words within each group, then list the groups in order.",
        "example_input": "6\neat\ntea\ntan\nate\nnat\nbat",
        "constraints": "Input format: line 1 is the number of words, followed by that many lowercase words. Output format: one group per line, words space-separated.",
        "solve": _solve_group_anagrams,
        "sample_inputs": ["6\neat\ntea\ntan\nate\nnat\nbat", "3\nabc\nbca\nxyz"],
        "hidden_inputs": [
            "1\na",                 # a single word
            "2\na\na",              # identical words group together
            "2\na\nb",              # two groups of one
            "2\nab\nba",
            "3\nab\nba\nab",        # a repeat inside one group
            "3\naab\naba\nbaa",     # all three are rearrangements
            "4\nabc\ncba\nxyz\nzyx",
            "4\na\nb\nc\nd",        # nothing groups
            "5\ncat\ntac\nact\ndog\ngod",
            "3\naa\naaa\na",        # different lengths never group
        ],
    },
{
        "title": "String Compression",
        "topic": "string",
        "difficulty": "medium",
        "description": "Replace each run of the same repeated character by that character followed by the length of the run. A run of length one is written as just the character.",
        "example_input": "aabcccccaaa",
        "constraints": "Input format: one line containing the lowercase string. Output format: the compressed string.",
        "solve": _solve_string_compression,
        "sample_inputs": ["aabcccccaaa", "abc"],
        "hidden_inputs": [
            "a",                    # a single character, no count
            "aa",                   # the shortest run that gets a count
            "ab",                   # two runs of one
            "aaa",
            "aaaaaaaaaa",           # a two-digit count
            "aaaaaaaaaaaa",
            "aabb",
            "abab",                 # alternating, nothing compresses
            "aabbaa",               # the same letter in two separate runs
            "zzzzyyyxxw",
        ],
    },
{
        "title": "Zigzag Conversion",
        "topic": "string",
        "difficulty": "medium",
        "description": "Write the string downwards and diagonally across the given number of rows, turning at the top and bottom, then read it off one row at a time from the top.",
        "example_input": "PAYPALISHIRING\n3",
        "constraints": "Input format: line 1 is the string, line 2 is the number of rows. Output format: the converted string.",
        "solve": _solve_zigzag_conversion,
        "sample_inputs": ["PAYPALISHIRING\n3", "PAYPALISHIRING\n4"],
        "hidden_inputs": [
            "A\n1",                 # a single row leaves it unchanged
            "A\n5",                 # more rows than characters
            "AB\n1",
            "AB\n2",                # one character per row
            "ABC\n2",
            "ABCD\n2",
            "ABCD\n3",
            "ABCDE\n4",             # the turn happens once
            "AB\n5",                # rows far exceed the length
            "ABCDEFGHIJ\n3",
        ],
    },
{
        "title": "Multiply Strings",
        "topic": "string",
        "difficulty": "medium",
        "description": "Two non-negative whole numbers are given as strings of digits. Return their product, also as a string of digits, without using any built-in big-number conversion.",
        "example_input": "123\n456",
        "constraints": "Input format: line 1 and line 2 are the two numbers, each without leading zeros unless the number is zero itself. Output format: the product, without leading zeros.",
        "solve": _solve_multiply_strings,
        "sample_inputs": ["123\n456", "2\n3"],
        "hidden_inputs": [
            "0\n0",                 # zero times zero
            "0\n123",               # zero on the left
            "123\n0",               # zero on the right
            "1\n1",
            "1\n999",               # multiplying by one
            "9\n9",                 # a single carry
            "99\n99",
            "999999\n999999",       # well past 32-bit
            "123456789\n987654321", # past 64-bit too
            "100\n100",             # trailing zeros in the product
        ],
    },
{
        "title": "Longest Valid Parentheses",
        "topic": "string",
        "difficulty": "hard",
        "description": "Given a string of opening and closing brackets, return the length of the longest run of consecutive characters that forms a properly matched sequence.",
        "example_input": ")()())",
        "constraints": "Input format: one line containing only the characters ( and ). Output format: a single integer.",
        "solve": _solve_longest_valid_parentheses,
        "sample_inputs": [")()())", "(()"],
        "hidden_inputs": [
            "(",                    # nothing can match
            ")",
            "()",                   # the whole string matches
            ")(",                   # the right characters, the wrong order
            "(()())",               # nesting and sequencing together
            "())",
            "()()",                 # two runs joined into one
            "(())",                 # nesting counts as one run
            "()(()",                # the longer run is not the first
            "((((((((((",           # all openers, nothing valid
        ],
    },
{
        "title": "Word Break II",
        "topic": "string",
        "difficulty": "hard",
        "description": "Split the string into a sentence of words, every one of which appears in the given dictionary, adding single spaces between them. List every sentence that can be formed, in alphabetical order.",
        "example_input": "catsanddog\n5\ncat\ncats\nand\nsand\ndog",
        "constraints": "Input format: line 1 is the string, line 2 is the dictionary size, followed by that many lowercase words. Output format: one sentence per line (empty if none can be formed).",
        "solve": _solve_word_break_ii,
        "sample_inputs": ["catsanddog\n5\ncat\ncats\nand\nsand\ndog", "pineapplepenapple\n5\napple\npen\napplepen\npine\npineapple"],
        "hidden_inputs": [
            "a\n1\na",              # the whole string is one word
            "a\n1\nb",              # nothing matches, empty output
            "ab\n2\na\nb",          # one sentence of two words
            "ab\n1\nab",
            "aa\n1\na",             # one sentence, the word used twice
            "aaa\n2\na\naa",        # several splittings
            "aaaa\n2\na\naa",
            "catsandog\n5\ncats\ndog\nsand\nand\ncat",   # no valid split exists
            "abcd\n4\na\nabc\nb\ncd",
            "abab\n2\na\nab",       # a dead end must not be reported
        ],
    },
{
        "title": "Length of Last Word",
        "topic": "string", "difficulty": "easy",
        "description": "Return the number of letters in the last word of the given text, where words are separated by single spaces.",
        "example_input": "Hello World",
        "constraints": "Input format: one line of words separated by single spaces, with none at either end. Output format: a single integer.",
        "solve": _solve_length_of_last_word,
        "sample_inputs": ["Hello World", "luffy is still joyboy"],
        "hidden_inputs": [
            "a",                    # a single letter
            "ab",
            "a b",                  # the last word is one letter
            "ab cd",
            "a bb ccc",             # the last word is longest
            "ccc bb a",             # and shortest
            "hello",
            "one two three four",
            "day",
            "the quick brown fox jumps",
        ],
    },
{
        "title": "To Lower Case",
        "topic": "string", "difficulty": "easy",
        "description": "Return the text with every capital letter replaced by its small form, leaving everything else as it is.",
        "example_input": "Hello",
        "constraints": "Input format: one line of text with no spaces at either end. Output format: the converted text.",
        "solve": _solve_to_lower_case,
        "sample_inputs": ["Hello", "LOVELY"],
        "hidden_inputs": [
            "a",                    # already small
            "A",
            "aA",
            "Aa",
            "abc",
            "ABC",
            "AbCdE",
            "1a2B3c",               # digits are untouched
            "Hello,World!",         # punctuation is untouched
            "ZYXWVUTSRQ",
        ],
    },
{
        "title": "Reverse Words in a String III",
        "topic": "string", "difficulty": "easy",
        "description": "Reverse the letters of every word while leaving the words themselves in their original order.",
        "example_input": "Let's take LeetCode contest",
        "constraints": "Input format: one line of words separated by single spaces, with none at either end. Output format: the resulting text.",
        "solve": _solve_reverse_words_iii,
        "sample_inputs": ["Let's take LeetCode contest", "Mr Ding"],
        "hidden_inputs": [
            "a",                    # one letter, unchanged
            "ab",
            "aa",                   # reversal is invisible
            "ab cd",
            "abc def ghi",
            "racecar level",        # palindromic words
            "a b c",
            "hello world",
            "one",
            "The quick brown fox",
        ],
    },
{
        "title": "Detect Capital",
        "topic": "string", "difficulty": "easy",
        "description": "Capital letters are used properly when the whole word is capitals, the whole word is small, or only the first letter is capital. Decide whether the given word uses them properly.",
        "example_input": "USA",
        "constraints": "Input format: one line containing a single word of letters. Output format: \"true\" or \"false\".",
        "solve": _solve_detect_capital,
        "sample_inputs": ["USA", "FlaG"],
        "hidden_inputs": [
            "a",                    # a single small letter
            "A",                    # a single capital
            "ab",
            "AB",
            "Ab",
            "aB",                   # a capital in the wrong place
            "ABc",
            "aBC",
            "Google",
            "leetcode",
        ],
    },
{
        "title": "Reverse Words in a String",
        "topic": "string", "difficulty": "medium",
        "description": "Return the words in the opposite order, separated by single spaces, with any extra spacing removed.",
        "example_input": "the sky is blue",
        "constraints": "Input format: one line of words separated by one or more spaces, with none at either end. Output format: the reordered text.",
        "solve": _solve_reverse_words,
        "sample_inputs": ["the sky is blue", "a good   example"],
        "hidden_inputs": [
            "a",                    # a single word
            "a b",
            "b a",
            "a  b",                 # extra spacing collapses
            "a   b   c",
            "one two three",
            "hello world",
            "x y z w",
            "the  quick  brown",
            "single",
        ],
    },
{
        "title": "Count and Say",
        "topic": "string", "difficulty": "medium",
        "description": "The first term is 1, and each later term is produced by reading the term before it aloud as runs of repeated digits, writing the length then the digit for each run. Return the nth term.",
        "example_input": "4",
        "constraints": "Input format: one line containing n (at least 1). Output format: the nth term.",
        "solve": _solve_count_and_say,
        "sample_inputs": ["4", "1"],
        "hidden_inputs": [
            "2",
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
        "title": "Longest Palindromic Subsequence",
        "topic": "string", "difficulty": "medium",
        "description": "Return the length of the longest sequence of letters that can be picked out of the text, keeping their order, which reads the same forwards and backwards.",
        "example_input": "bbbab",
        "constraints": "Input format: one line containing the lowercase text. Output format: a single integer.",
        "solve": _solve_longest_palindromic_subsequence,
        "sample_inputs": ["bbbab", "cbbd"],
        "hidden_inputs": [
            "a",                    # a single letter
            "ab",                   # no pair matches
            "aa",
            "aba",
            "abc",
            "aaaa",
            "abcba",                # the whole text
            "abcde",
            "agbdba",
            "character",
        ],
    },
{
        "title": "Longest Repeating Substring",
        "topic": "string", "difficulty": "medium",
        "description": "Return the length of the longest stretch of letters that appears more than once in the text, where the two appearances may overlap. Return zero if none does.",
        "example_input": "abcd",
        "constraints": "Input format: one line containing the lowercase text. Output format: a single integer.",
        "solve": _solve_longest_repeating_substring,
        "sample_inputs": ["abcd", "abbaba"],
        "hidden_inputs": [
            "a",                    # nothing can repeat
            "aa",                   # a single letter repeats
            "ab",
            "aaa",                  # overlapping appearances count
            "abab",
            "abcabc",
            "aabcaabdaab",
            "abcdefg",
            "zzzzz",
            "banana",
        ],
    },
{
        "title": "Decode Ways II",
        "topic": "string", "difficulty": "medium",
        "description": "A message of digits was encoded by mapping A to 1 through Z to 26, and a star stands for any digit from 1 to 9. Count the letter strings the message could decode to, modulo 1000000007. A group may not have a leading zero.",
        "example_input": "*",
        "constraints": "Input format: one line of digits and stars. Output format: a single integer, the count modulo 1000000007.",
        "solve": _solve_decode_ways_ii,
        "sample_inputs": ["*", "1*"],
        "hidden_inputs": [
            "0",                    # a lone zero decodes to nothing
            "1",
            "**",
            "*0",
            "0*",
            "12",
            "1*1",
            "2*",
            "***",
            "*1*1*0",
        ],
    },
{
        "title": "Word Pattern",
        "topic": "string", "difficulty": "medium",
        "description": "Decide whether the words match the pattern, meaning each pattern letter always stands for the same word and each word is always stood for by the same letter.",
        "example_input": "abba\ndog cat cat dog",
        "constraints": "Input format: line 1 is the pattern of small letters, line 2 is the words separated by single spaces. Output format: \"true\" or \"false\".",
        "solve": _solve_word_pattern,
        "sample_inputs": ["abba\ndog cat cat dog", "abba\ndog cat cat fish"],
        "hidden_inputs": [
            "a\ndog",               # a single pairing
            "a\ndog cat",           # the lengths differ
            "ab\ndog",
            "aa\ndog dog",
            "aa\ndog cat",          # one letter, two words
            "ab\ndog dog",          # two letters, one word
            "ab\ndog cat",
            "abba\ndog dog dog dog",
            "aaaa\ndog cat cat dog",
            "abc\ndog cat fish",
        ],
    },
{
        "title": "Isomorphic Strings",
        "topic": "string", "difficulty": "medium",
        "description": "Decide whether the letters of the first text can be replaced to give the second, with each letter always becoming the same letter and no two letters becoming the same one.",
        "example_input": "egg\nadd",
        "constraints": "Input format: line 1 and line 2 are the two lowercase texts. Output format: \"true\" or \"false\".",
        "solve": _solve_isomorphic_strings,
        "sample_inputs": ["egg\nadd", "foo\nbar"],
        "hidden_inputs": [
            "a\na",                 # identical
            "a\nb",
            "ab\nab",
            "ab\nba",
            "ab\naa",               # two letters would collide
            "aa\nab",               # one letter cannot split
            "abc\nxyz",
            "paper\ntitle",
            "badc\nbaba",
            "ab\nabc",              # the lengths differ
        ],
    },
{
        "title": "Repeated Substring Pattern",
        "topic": "string", "difficulty": "medium",
        "description": "Decide whether the text can be built by writing out some shorter stretch of it two or more times in a row.",
        "example_input": "abab",
        "constraints": "Input format: one line containing the lowercase text. Output format: \"true\" or \"false\".",
        "solve": _solve_repeated_substring_pattern,
        "sample_inputs": ["abab", "aba"],
        "hidden_inputs": [
            "a",                    # nothing shorter to repeat
            "aa",                   # the shortest true case
            "ab",
            "aaa",
            "abc",
            "abcabc",
            "abcabcabc",
            "abac",
            "abaababaab",
            "bb",
        ],
    },
{
        "title": "Reverse Only Letters",
        "topic": "string", "difficulty": "hard",
        "description": "Reverse the order of the letters while leaving every other character exactly where it is.",
        "example_input": "ab-cd",
        "constraints": "Input format: one line of text with no spaces at either end. Output format: the resulting text.",
        "solve": _solve_reverse_only_letters,
        "sample_inputs": ["ab-cd", "a-bC-dEf-ghIj"],
        "hidden_inputs": [
            "a",                    # nothing to swap
            "-",                    # no letters at all
            "ab",
            "a-b",
            "-a-",
            "ab-",
            "-ab",
            "a1b2c3",
            "Test1ng-Leet=code-Q!",
            "---",
        ],
    },
{
        "title": "Compare Version Numbers",
        "topic": "string", "difficulty": "hard",
        "description": "Version numbers are written as parts separated by dots, and missing parts count as zero. Return 1 if the first is larger, -1 if the second is, and 0 if they are equal.",
        "example_input": "1.2\n1.10",
        "constraints": "Input format: line 1 and line 2 are the two version numbers. Output format: 1, -1 or 0.",
        "solve": _solve_compare_version,
        "sample_inputs": ["1.2\n1.10", "1.01\n1.001"],
        "hidden_inputs": [
            "1\n1",                 # equal
            "1\n2",
            "2\n1",
            "1.0\n1",               # a missing part counts as zero
            "1\n1.0",
            "1.0.0\n1",
            "0\n0",
            "1.0.1\n1",
            "7.5.2.4\n7.5.3",
            "01\n1",                # leading zeros do not matter
        ],
    },
{
        "title": "Shortest Palindrome",
        "topic": "string", "difficulty": "hard",
        "description": "Add as few letters as possible to the front of the text so that it reads the same forwards and backwards, and return the result.",
        "example_input": "aacecaaa",
        "constraints": "Input format: one line containing the lowercase text. Output format: the resulting text.",
        "solve": _solve_shortest_palindrome,
        "sample_inputs": ["aacecaaa", "abcd"],
        "hidden_inputs": [
            "a",                    # already a palindrome
            "aa",
            "ab",
            "ba",
            "aba",
            "abb",
            "aabba",
            "abcba",                # nothing to add
            "aaaa",
            "abbacd",
        ],
    },
{
        "title": "Valid Palindrome III",
        "topic": "string", "difficulty": "hard",
        "description": "Decide whether the text can be made to read the same forwards and backwards by deleting at most k of its letters.",
        "example_input": "abcdeca\n2",
        "constraints": "Input format: line 1 is the lowercase text, line 2 is k. Output format: \"true\" or \"false\".",
        "solve": _solve_valid_palindrome_iii,
        "sample_inputs": ["abcdeca\n2", "abbababa\n1"],
        "hidden_inputs": [
            "a\n0",                 # already a palindrome
            "ab\n0",
            "ab\n1",                # one deletion suffices
            "abc\n1",
            "abc\n2",
            "abcd\n1",
            "aabb\n2",
            "racecar\n0",
            "abcdef\n3",
            "aaaa\n0",
        ],
    },
{
        "title": "Longest Duplicate Substring",
        "topic": "string", "difficulty": "hard",
        "description": "Return the longest stretch of letters that appears at least twice in the text, where the appearances may overlap. When several are equally long, return the one that comes first in the text; return nothing if none does.",
        "example_input": "banana",
        "constraints": "Input format: one line containing the lowercase text. Output format: the stretch, or an empty line if none exists.",
        "solve": _solve_longest_duplicate_substring,
        "sample_inputs": ["banana", "abcd"],
        "hidden_inputs": [
            "a",                    # nothing repeats
            "aa",
            "ab",
            "aaa",                  # overlapping appearances count
            "abab",
            "abcabc",
            "zxcvzxcv",
            "aabcaabdaab",
            "nnpxouomcofdjuvtwyaaa",
            "bbbbb",
        ],
    },
{
        "title": "String to Integer",
        "topic": "string", "difficulty": "hard",
        "description": "Read a number from the front of the text: skip any leading spaces, take an optional plus or minus sign, then take digits until a non-digit or the end. Return the value, clamped to the signed 32-bit range, or zero if no digits were found.",
        "example_input": "42",
        "constraints": "Input format: one line of text with no spaces at either end. Output format: a single integer.",
        "solve": _solve_string_to_integer,
        "sample_inputs": ["42", "4193 with words"],
        "hidden_inputs": [
            "0",                    # a plain zero
            "-1",
            "+1",                   # a leading plus
            "words and 987",        # no digits at the front
            "00000012",             # leading zeros
            "3.14",                 # reading stops at the dot
            "+-12",                 # two signs, so nothing is read
            "2147483648",           # clamped to the maximum
            "-2147483649",          # clamped to the minimum
            "-91283472332",
        ],
    },
{
        "title": "Count Binary Substrings",
        "topic": "string", "difficulty": "hard",
        "description": "Count the stretches of the binary text that hold the same number of zeroes as ones, with all the zeroes together and all the ones together. Stretches that occur more than once are counted each time.",
        "example_input": "00110011",
        "constraints": "Input format: one line made only of the characters 0 and 1. Output format: a single integer.",
        "solve": _solve_count_binary_substrings,
        "sample_inputs": ["00110011", "10101"],
        "hidden_inputs": [
            "0",                    # nothing qualifies
            "01",                   # the smallest qualifying stretch
            "10",
            "00",                   # no ones at all
            "11",
            "001",
            "0011",
            "000111",
            "0110",
            "00011100",
        ],
    },
]
