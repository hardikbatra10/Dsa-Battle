"""Sliding Window problems."""

def _solve_max_avg_subarray(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    avg = best / k
    if avg == int(avg):
        return str(int(avg))
    return f"{avg:.5f}"


def _solve_longest_k_distinct(lines):
    s = lines[0]
    k = int(lines[1])
    if k == 0:
        return "0"
    from collections import defaultdict
    count = defaultdict(int)
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while len(count) > k:
            count[s[left]] -= 1
            if count[s[left]] == 0:
                del count[s[left]]
            left += 1
        best = max(best, right - left + 1)
    return str(best)


def _solve_min_window_substring(lines):
    s = lines[0]
    t = lines[1]
    from collections import Counter
    if not t or not s:
        return ""
    need = Counter(t)
    missing = len(t)
    left = start = end = 0
    for right, ch in enumerate(s, 1):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        if missing == 0:
            while left < right and need[s[left]] < 0:
                need[s[left]] += 1
                left += 1
            if end == 0 or right - left < end - start:
                start, end = left, right
    return s[start:end]

def _solve_contains_duplicate_ii(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    seen = {}
    for i, n in enumerate(nums):
        if n in seen and i - seen[n] <= k:
            return "true"
        seen[n] = i
    return "false"


def _solve_char_replacement(lines):
    s = lines[0]
    k = int(lines[1])
    from collections import defaultdict
    count = defaultdict(int)
    left = 0
    best = 0
    most = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        most = max(most, count[ch])
        while (right - left + 1) - most > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return str(best)


def _solve_min_size_subarray_sum(lines):
    target = int(lines[0])
    nums = list(map(int, lines[1].split()))
    left = 0
    total = 0
    best = len(nums) + 1
    for right, n in enumerate(nums):
        total += n
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return str(best if best <= len(nums) else 0)


def _solve_permutation_in_string(lines):
    s1 = lines[0]
    s2 = lines[1]
    if len(s1) > len(s2):
        return "false"
    from collections import Counter
    need = Counter(s1)
    window = Counter(s2[:len(s1)])
    if window == need:
        return "true"
    for i in range(len(s1), len(s2)):
        window[s2[i]] += 1
        out = s2[i - len(s1)]
        window[out] -= 1
        if window[out] == 0:
            del window[out]
        if window == need:
            return "true"
    return "false"


def _solve_k_closest_elements(lines):
    arr = list(map(int, lines[0].split()))
    k = int(lines[1])
    x = int(lines[2])
    lo, hi = 0, len(arr) - k
    while lo < hi:
        mid = (lo + hi) // 2
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid
    return " ".join(map(str, arr[lo:lo + k]))


def _solve_sliding_window_maximum(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import deque
    dq = deque()
    out = []
    for i, n in enumerate(nums):
        while dq and nums[dq[-1]] <= n:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            out.append(str(nums[dq[0]]))
    return " ".join(out)


def _solve_repeated_dna(lines):
    s = lines[0]
    seen = set()
    repeated = []
    for i in range(len(s) - 9):
        chunk = s[i:i + 10]
        if chunk in seen and chunk not in repeated:
            repeated.append(chunk)
        seen.add(chunk)
    return " ".join(repeated)


def _solve_longest_substr_k_repeating(lines):
    s = lines[0]
    k = int(lines[1])

    def helper(sub):
        if not sub:
            return 0
        from collections import Counter
        counts = Counter(sub)
        for ch, c in counts.items():
            if c < k:
                return max(helper(part) for part in sub.split(ch))
        return len(sub)

    return str(helper(s))


def _solve_max_sum_distinct_k(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import defaultdict
    count = defaultdict(int)
    total = 0
    best = 0
    for i, n in enumerate(nums):
        count[n] += 1
        total += n
        if i >= k:
            out = nums[i - k]
            count[out] -= 1
            total -= out
            if count[out] == 0:
                del count[out]
        if i >= k - 1 and len(count) == k:
            best = max(best, total)
    return str(best)


def _solve_max_subarray_sum_equals_k(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    first = {0: -1}
    prefix = 0
    best = 0
    for i, n in enumerate(nums):
        prefix += n
        if prefix - k in first:
            best = max(best, i - first[prefix - k])
        if prefix not in first:
            first[prefix] = i
    return str(best)


def _solve_min_ops_reduce_to_zero(lines):
    nums = list(map(int, lines[0].split()))
    x = int(lines[1])
    target = sum(nums) - x
    if target < 0:
        return "-1"
    if target == 0:
        return str(len(nums))
    left = 0
    total = 0
    best = -1
    for right, n in enumerate(nums):
        total += n
        while total > target and left <= right:
            total -= nums[left]
            left += 1
        if total == target:
            best = max(best, right - left + 1)
    return str(len(nums) - best) if best != -1 else "-1"


def _solve_substrings_all_three(lines):
    s = lines[0]
    last = {"a": -1, "b": -1, "c": -1}
    total = 0
    for i, ch in enumerate(s):
        last[ch] = i
        total += min(last["a"], last["b"], last["c"]) + 1
    return str(total)


def _solve_sliding_subarray_beauty(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    x = int(lines[2])
    counts = [0] * 101          # values are in [-50, 50]
    out = []
    for i, n in enumerate(nums):
        counts[n + 50] += 1
        if i >= k:
            counts[nums[i - k] + 50] -= 1
        if i >= k - 1:
            seen = 0
            beauty = 0
            for v in range(0, 50):      # only negatives can be beautiful
                seen += counts[v]
                if seen >= x:
                    beauty = v - 50
                    break
            out.append(str(beauty))
    return " ".join(out)


def _solve_max_points_from_cards(lines):
    cards = list(map(int, lines[0].split()))
    k = int(lines[1])
    n = len(cards)
    if k >= n:
        return str(sum(cards))
    window = n - k
    cur = sum(cards[:window])
    smallest = cur
    for i in range(window, n):
        cur += cards[i] - cards[i - window]
        smallest = min(smallest, cur)
    return str(sum(cards) - smallest)


def _solve_subarrays_avg_threshold(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    threshold = int(lines[2])
    need = k * threshold
    total = sum(nums[:k])
    count = 1 if total >= need else 0
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]
        if total >= need:
            count += 1
    return str(count)


def _solve_all_binary_codes(lines):
    s = lines[0]
    k = int(lines[1])
    if len(s) < k:
        return "false"
    seen = set()
    for i in range(len(s) - k + 1):
        seen.add(s[i:i + k])
    return "true" if len(seen) == (1 << k) else "false"


def _solve_find_all_anagrams(lines):
    s = lines[0]
    p = lines[1]
    if len(p) > len(s):
        return ""
    from collections import Counter
    need = Counter(p)
    window = Counter(s[:len(p)])
    out = []
    if window == need:
        out.append(0)
    for i in range(len(p), len(s)):
        window[s[i]] += 1
        gone = s[i - len(p)]
        window[gone] -= 1
        if window[gone] == 0:
            del window[gone]
        if window == need:
            out.append(i - len(p) + 1)
    return " ".join(map(str, out))


def _solve_substrings_size_three(lines):
    s = lines[0]
    count = 0
    for i in range(len(s) - 2):
        if len(set(s[i:i + 3])) == 3:
            count += 1
    return str(count)


def _solve_good_cyclic_rotations(lines):
    s = lines[0]
    n = len(s)
    count = 0
    for r in range(n):
        rot = s[r:] + s[:r]
        if all(rot[i] != rot[i + 1] for i in range(n - 1)) and (n == 1 or rot[0] != rot[-1]):
            count += 1
    return str(count)


def _solve_count_good_subarrays(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import defaultdict
    count = defaultdict(int)
    pairs = 0
    left = 0
    total = 0
    for right, n in enumerate(nums):
        pairs += count[n]
        count[n] += 1
        while pairs >= k:
            count[nums[left]] -= 1
            pairs -= count[nums[left]]
            left += 1
        total += left
    return str(total)


def _solve_longest_semi_repetitive(lines):
    s = lines[0]
    left = 0
    doubles = 0
    best = 1 if s else 0
    for right in range(1, len(s)):
        if s[right] == s[right - 1]:
            doubles += 1
        while doubles > 1:
            left += 1
            if s[left] == s[left - 1]:
                doubles -= 1
        best = max(best, right - left + 1)
    return str(best)

def _solve_max_vowels_substring(lines):
    s = lines[0]
    k = int(lines[1])
    vowels = set("aeiou")
    cur = sum(1 for c in s[:k] if c in vowels)
    best = cur
    for i in range(k, len(s)):
        cur += (1 if s[i] in vowels else 0) - (1 if s[i - k] in vowels else 0)
        best = max(best, cur)
    return str(best)


def _solve_k_beauty(lines):
    num = lines[0]
    k = int(lines[1])
    value = int(num)
    count = 0
    for i in range(len(num) - k + 1):
        piece = int(num[i:i + k])
        if piece != 0 and value % piece == 0:
            count += 1
    return str(count)


def _solve_defuse_the_bomb(lines):
    code = list(map(int, lines[0].split()))
    k = int(lines[1])
    n = len(code)
    if k == 0:
        return " ".join("0" for _ in range(n))
    out = []
    for i in range(n):
        total = 0
        if k > 0:
            for j in range(1, k + 1):
                total += code[(i + j) % n]
        else:
            for j in range(1, -k + 1):
                total += code[(i - j) % n]
        out.append(str(total))
    return " ".join(out)


def _solve_min_recolors(lines):
    blocks = lines[0]
    k = int(lines[1])
    cur = sum(1 for c in blocks[:k] if c == "W")
    best = cur
    for i in range(k, len(blocks)):
        cur += (1 if blocks[i] == "W" else 0) - (1 if blocks[i - k] == "W" else 0)
        best = min(best, cur)
    return str(best)


def _solve_longest_harmonious(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = Counter(nums)
    best = 0
    for v in counts:
        if v + 1 in counts:
            best = max(best, counts[v] + counts[v + 1])
    return str(best)


def _solve_grumpy_bookstore(lines):
    customers = list(map(int, lines[0].split()))
    grumpy = list(map(int, lines[1].split()))
    minutes = int(lines[2])
    base = sum(c for c, g in zip(customers, grumpy) if g == 0)
    gain = sum(customers[i] for i in range(min(minutes, len(customers)))
               if grumpy[i] == 1)
    best = gain
    for i in range(minutes, len(customers)):
        if grumpy[i] == 1:
            gain += customers[i]
        if grumpy[i - minutes] == 1:
            gain -= customers[i - minutes]
        best = max(best, gain)
    return str(base + best)


def _solve_count_subarrays_fixed_bounds(lines):
    nums = list(map(int, lines[0].split()))
    lo, hi = map(int, lines[1].split())
    total = 0
    last_bad = -1
    last_lo = -1
    last_hi = -1
    for i, v in enumerate(nums):
        if v < lo or v > hi:
            last_bad = i
        if v == lo:
            last_lo = i
        if v == hi:
            last_hi = i
        total += max(0, min(last_lo, last_hi) - last_bad)
    return str(total)


def _solve_max_robots_budget(lines):
    charge = list(map(int, lines[0].split()))
    running = list(map(int, lines[1].split()))
    budget = int(lines[2])
    from collections import deque
    dq = deque()
    left = 0
    total = 0
    best = 0
    for right, c in enumerate(charge):
        total += running[right]
        while dq and charge[dq[-1]] <= c:
            dq.pop()
        dq.append(right)
        while dq and charge[dq[0]] + (right - left + 1) * total > budget:
            total -= running[left]
            if dq[0] == left:
                dq.popleft()
            left += 1
        best = max(best, right - left + 1)
    return str(best)


def _solve_constrained_subsequence_sum(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import deque
    dq = deque()
    dp = [0] * len(nums)
    for i, v in enumerate(nums):
        while dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = v + (dp[dq[0]] if dq and dp[dq[0]] > 0 else 0)
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
    return str(max(dp))


def _solve_longest_subarray_abs_limit(lines):
    nums = list(map(int, lines[0].split()))
    limit = int(lines[1])
    from collections import deque
    maxq = deque()
    minq = deque()
    left = 0
    best = 0
    for right, v in enumerate(nums):
        while maxq and nums[maxq[-1]] <= v:
            maxq.pop()
        maxq.append(right)
        while minq and nums[minq[-1]] >= v:
            minq.pop()
        minq.append(right)
        while nums[maxq[0]] - nums[minq[0]] > limit:
            if maxq[0] == left:
                maxq.popleft()
            if minq[0] == left:
                minq.popleft()
            left += 1
        best = max(best, right - left + 1)
    return str(best)


def _solve_jump_game_vi(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import deque
    dq = deque([0])
    dp = [0] * len(nums)
    dp[0] = nums[0]
    for i in range(1, len(nums)):
        while dq and dq[0] < i - k:
            dq.popleft()
        dp[i] = nums[i] + dp[dq[0]]
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)
    return str(dp[-1])


PROBLEMS = [
{
        "title": "Maximum Average Subarray",
        "topic": "sliding_window",
        "difficulty": "easy",
        "description": "Given an array and an integer k, find the maximum average value of any contiguous subarray of length k.",
        "example_input": "4 4 4 4\n2",
        "constraints": "Input format: line 1 is the space-separated array, line 2 is k. Output format: the max average.",
        "solve": _solve_max_avg_subarray,
        "sample_inputs": ["4 4 4 4\n2", "3 8 1 9\n2"],
        "hidden_inputs": [
            "5\n1",          # single element, window of one
            "-5 -5\n1",
            "1 2\n2",        # window covers the whole array
            "0 0 0\n1",
            "5 5\n2",
            "1 2 3 4 5\n1",  # window of one, so the maximum element
            "1 2 3 4 5\n5",  # window equals the array
            "2 2 2 6\n2",
            "-1 -2 -3\n2",   # all negative, fractional average
            "1 12 -5 -6 50 3\n4",
            "100000 100000\n2",
        ],
    },
{
        "title": "Longest Substring with At Most K Distinct Characters",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a string s and an integer k, find the length of the longest substring that contains at most k distinct characters.",
        "example_input": "eceba\n2",
        "constraints": "Input format: line 1 is s, line 2 is k. Output format: a single integer.",
        "solve": _solve_longest_k_distinct,
        "sample_inputs": ["eceba\n2", "aabbcc\n2"],
        "hidden_inputs": [
            "a\n0",       # k = 0 admits nothing
            "ab\n0",
            "a\n1",
            "ab\n1",
            "aa\n1",
            "aaaa\n2",    # fewer distinct chars than k
            "abc\n5",     # k exceeds the alphabet present
            "aabbcc\n1",
            "aabbcc\n3",  # k covers everything
            "abcabcabc\n2",
            "abaccc\n2",
            "abcadcacacaca\n3",
        ],
    },
{
        "title": "Minimum Window Substring",
        "topic": "sliding_window",
        "difficulty": "hard",
        "description": "Given strings s and t, return the smallest substring of s that contains every character of t (with the same multiplicity). Return an empty string if no such substring exists.",
        "example_input": "ADOBECODEBANC\nABC",
        "constraints": "Input format: line 1 is s, line 2 is t. Output format: the minimum window substring, or an empty line if none.",
        "solve": _solve_min_window_substring,
        "sample_inputs": ["ADOBECODEBANC\nABC", "aa\na"],
        "hidden_inputs": [
            "a\na",                 # s equals t
            "a\naa",                # t needs more copies than s has
            "ab\na",
            "ab\nb",
            "aa\naa",
            "abcdef\nxyz",          # no character of t occurs in s
            "bba\nab",              # window must shrink from the left
            "ABC\nCBA",             # t is a permutation of s
            "aaaaaaaaaa\naaa",      # many equally short windows
            "ADOBECODEBANC\nABBC",  # duplicate letter in t raises the requirement
            "cabwefgewcwaefgcf\ncae",
        ],
    },
{
        "title": "Contains Duplicate II",
        "topic": "sliding_window",
        "difficulty": "easy",
        "description": "Given an array of integers and an integer k, decide whether there are two distinct indices i and j such that the values are equal and the gap between the indices is at most k.",
        "example_input": "1 2 3 1\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: \"true\" or \"false\".",
        "solve": _solve_contains_duplicate_ii,
        "sample_inputs": ["1 2 3 1\n3", "1 2 3 1 2 3\n2"],
        "hidden_inputs": [
            "1\n1",                 # single element, nothing to pair
            "1 1\n0",               # k of zero can never match
            "1 1\n1",               # adjacent duplicates
            "1 2 1\n1",             # duplicate exists but too far apart
            "1 2 1\n2",             # same array, k now reaches
            "1 2 3 4\n10",          # no duplicates at all
            "5 5 5 5\n1",
            "0 0\n1",               # zeros
            "-1 -1\n1",             # negatives
            "1 0 1 1\n1",           # the nearest pair is what counts
            "99 99\n2",
        ],
    },
{
        "title": "Longest Repeating Character Replacement",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a string of uppercase letters, you may change at most k characters to any other uppercase letter. Return the length of the longest substring that can be made to contain a single repeated letter.",
        "example_input": "ABAB\n2",
        "constraints": "Input format: line 1 is the string, line 2 is k. Output format: a single integer.",
        "solve": _solve_char_replacement,
        "sample_inputs": ["ABAB\n2", "AABABBA\n1"],
        "hidden_inputs": [
            "A\n0",                 # single character, no budget
            "A\n5",                 # budget larger than the string
            "AB\n0",                # no change allowed
            "AB\n1",                # one change unifies both
            "AAAA\n0",              # already uniform
            "AAAA\n2",
            "ABCDE\n0",
            "ABCDE\n2",
            "ABBB\n2",
            "AABBCC\n2",
            "ABAA\n0",              # best run ignores the budget entirely
        ],
    },
{
        "title": "Minimum Size Subarray Sum",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a target and an array of positive integers, return the length of the shortest contiguous subarray whose sum is at least target. Return 0 if no such subarray exists.",
        "example_input": "7\n2 3 1 2 4 3",
        "constraints": "Input format: line 1 is the target, line 2 is the space-separated positive integers. Output format: a single integer.",
        "solve": _solve_min_size_subarray_sum,
        "sample_inputs": ["7\n2 3 1 2 4 3", "11\n1 1 1 1 1 1 1 1"],
        "hidden_inputs": [
            "1\n1",                 # single element meets the target
            "2\n1",                 # single element falls short
            "4\n1 4 4",             # one element alone suffices
            "11\n1 2 3",            # whole array falls short
            "6\n1 2 3",             # whole array is exactly enough
            "5\n1 1 1 1 1",
            "3\n1 1 1 1 1",
            "15\n1 2 3 4 5",        # entire array needed
            "9\n2 3 1 2 4 3",       # target just above the sample's
            "100\n1 1 1",
            "8\n5 1 3 5 10 7 4 9 2 8",
        ],
    },
{
        "title": "Permutation in String",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given two strings s1 and s2, decide whether s2 contains a substring that is a permutation of s1.",
        "example_input": "ab\neidbaooo",
        "constraints": "Input format: line 1 is s1, line 2 is s2 (both lowercase). Output format: \"true\" or \"false\".",
        "solve": _solve_permutation_in_string,
        "sample_inputs": ["ab\neidbaooo", "ab\neidboaoo"],
        "hidden_inputs": [
            "a\na",                 # identical single characters
            "a\nb",
            "ab\na",                # s1 longer than s2
            "ab\nab",               # exact match
            "ab\nba",               # reversed is still a permutation
            "abc\ncba",
            "aa\naa",
            "aa\naba",              # letters present but never adjacent
            "adc\ndcda",
            "hello\nooolleoooleh",
            "abc\nbbbca",
        ],
    },
{
        "title": "Find K Closest Elements",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a sorted array, an integer k and a value x, return the k elements closest to x in ascending order. When two elements are equally close, the smaller one is preferred.",
        "example_input": "1 2 3 4 5\n4\n3",
        "constraints": "Input format: line 1 is the sorted array, line 2 is k, line 3 is x. Output format: the k chosen elements, space-separated ascending.",
        "solve": _solve_k_closest_elements,
        "sample_inputs": ["1 2 3 4 5\n4\n3", "1 2 3 4 5\n4\n-1"],
        "hidden_inputs": [
            "1\n1\n1",              # single element
            "1 2\n1\n1",
            "1 2\n2\n1",            # k equals the array length
            "1 3\n1\n2",            # exact tie, the smaller wins
            "1 2 3 4 5\n1\n3",
            "1 2 3 4 5\n5\n3",      # everything is chosen
            "1 2 3 4 5\n2\n100",    # x beyond the right end
            "1 2 3 4 5\n2\n-100",   # x beyond the left end
            "0 0 1 2 3 3 4 7 7 8\n3\n5",
            "1 1 1 10 10 10\n1\n9",
            "1 5 9 13\n2\n7",       # tie resolved between two gaps
        ],
    },
{
        "title": "Sliding Window Maximum",
        "topic": "sliding_window",
        "difficulty": "hard",
        "description": "Given an array and a window size k, slide the window one position at a time from left to right and report the maximum value inside the window at each stop.",
        "example_input": "1 3 -1 -3 5 3 6 7\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k (1 <= k <= array length). Output format: one maximum per window position, space-separated.",
        "solve": _solve_sliding_window_maximum,
        "sample_inputs": ["1 3 -1 -3 5 3 6 7\n3", "9 11\n2"],
        "hidden_inputs": [
            "1\n1",                 # single element window
            "1 2 3\n1",             # window of one echoes the array
            "1 2 3\n3",             # window covers everything
            "3 3 3 3\n2",           # all equal
            "1 2 3 4 5\n2",         # increasing, max is the right edge
            "5 4 3 2 1\n2",         # decreasing, max is the left edge
            "-1 -2 -3\n2",          # negatives
            "-7 -8 7 5 7 1 6 0\n4",
            "1 3 1 2 0 5\n3",
            "7 2 4\n2",
            "1 -1\n1",
        ],
    },
{
        "title": "Repeated DNA Sequences",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a DNA string made of the letters A, C, G and T, return every 10-letter substring that occurs more than once, listed in the order their repetition is first detected.",
        "example_input": "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT",
        "constraints": "Input format: one line containing the DNA string. Output format: the repeated 10-letter substrings, space-separated (empty if none).",
        "solve": _solve_repeated_dna,
        "sample_inputs": ["AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT", "AAAAAAAAAAAAA"],
        "hidden_inputs": [
            "A",                        # far shorter than 10
            "AAAAAAAAA",                # exactly one short of 10
            "AAAAAAAAAA",               # exactly 10, cannot repeat
            "AAAAAAAAAAA",              # 11 letters, first repeat
            "ACGTACGTAC",               # 10 distinct-ish, no repeat
            "ACGTACGTACGTACGTACGT",
            "AAAAAAAAAAAA",
            "GAGAGAGAGAGAGA",
            "AAAAACCCCCAAAAACCCCCC",
            "TTTTTCCCCCTTTTTCCCCCGGGGG",
        ],
    },
{
        "title": "Longest Substring with At Least K Repeating Characters",
        "topic": "sliding_window",
        "difficulty": "hard",
        "description": "Given a string s and an integer k, return the length of the longest substring in which every distinct character appears at least k times.",
        "example_input": "aaabb\n3",
        "constraints": "Input format: line 1 is s (lowercase), line 2 is k. Output format: a single integer.",
        "solve": _solve_longest_substr_k_repeating,
        "sample_inputs": ["aaabb\n3", "ababbc\n2"],
        "hidden_inputs": [
            "a\n1",                 # single character meets k
            "a\n2",                 # single character falls short
            "aa\n2",
            "ab\n2",                # neither letter can reach k
            "aaa\n1",
            "aaabbb\n3",            # the whole string qualifies
            "bbaaacbd\n3",
            "abcdedghijklmnopqrstuvwxyz\n2",   # nothing repeats enough
            "aaabbbccc\n3",
            "weitong\n2",
            "aaaaaaaaaaaabbbbbbbbbb\n11",
        ],
    },
{
        "title": "Maximum Sum of Distinct Subarrays With Length K",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Return the largest possible sum of a contiguous subarray of length exactly k in which every element is distinct. Return 0 if no such subarray exists.",
        "example_input": "1 5 4 2 9 9 9\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: a single integer.",
        "solve": _solve_max_sum_distinct_k,
        "sample_inputs": ["1 5 4 2 9 9 9\n3", "4 4 4\n3"],
        "hidden_inputs": [
            "1\n1",                 # single element
            "1 1\n1",               # window of one is always distinct
            "1 1\n2",               # no distinct window of two
            "1 2\n2",
            "9 9 9 9\n2",           # every window repeats
            "1 2 3 4 5\n5",         # the whole array is distinct
            "1 2 3 4 5\n1",
            "5 5 1 2 3\n3",
            "-1 -2 -3\n2",          # negatives, best sum is least negative
            "1 2 1 2 1 2\n2",
            "1 5 4 2 9 9 9\n4",
        ],
    },
{
        "title": "Maximum Size Subarray Sum Equals K",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given an array of integers, which may be negative, return the length of the longest contiguous subarray whose sum is exactly k. Return 0 if there is none.",
        "example_input": "1 -1 5 -2 3\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: a single integer.",
        "solve": _solve_max_subarray_sum_equals_k,
        "sample_inputs": ["1 -1 5 -2 3\n3", "-2 -1 2 1\n1"],
        "hidden_inputs": [
            "1\n1",                 # single element matches
            "1\n2",                 # single element does not
            "0\n0",                 # a zero-sum single element
            "0 0 0\n0",             # whole array sums to zero
            "1 -1\n0",              # positives and negatives cancel
            "1 2 3\n6",             # entire array
            "1 2 3\n7",             # unreachable
            "-1 -1 -1\n-2",
            "1 0 -1\n0",            # longest wins over earliest
            "1 -1 5 -2 3\n4",       # the answer sits in the middle
            "5 -3 2 1 -4 6\n3",
        ],
    },
{
        "title": "Minimum Operations to Reduce X to Zero",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Each operation removes either the leftmost or the rightmost element of the array and subtracts its value from x. Return the fewest operations that reduce x to exactly zero, or -1 if it cannot be done.",
        "example_input": "1 1 4 2 3\n5",
        "constraints": "Input format: line 1 is the space-separated positive integers, line 2 is x. Output format: a single integer, or -1.",
        "solve": _solve_min_ops_reduce_to_zero,
        "sample_inputs": ["1 1 4 2 3\n5", "5 6 7 8 9\n4"],
        "hidden_inputs": [
            "1\n1",                 # one element, exactly x
            "1\n2",                 # x exceeds the total
            "1 1\n2",               # both elements needed
            "1 2 3\n6",             # the whole array
            "1 2 3\n7",             # impossible
            "5 2 3 1 1\n5",         # one element from the left
            "3 2 20 1 1 3\n10",     # taken from both ends
            "1 1 1 1\n2",
            "2 2 2\n3",             # never lands exactly on x
            "1 1 4 2 3\n10",
            "8 9 4 5 3\n29",        # requires every element
        ],
    },
{
        "title": "Number of Substrings Containing All Three Characters",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a string made only of the characters a, b and c, count how many of its substrings contain at least one of each.",
        "example_input": "abcabc",
        "constraints": "Input format: one line containing the string. Output format: a single integer.",
        "solve": _solve_substrings_all_three,
        "sample_inputs": ["abcabc", "aaacb"],
        "hidden_inputs": [
            "a",                    # too short
            "ab",                   # missing a letter entirely
            "abc",                  # exactly one qualifying substring
            "aaa",                  # only one distinct letter
            "cba",
            "abcc",
            "ccba",
            "aaabbbccc",
            "abababab",             # never contains a c
            "cabcabcabc",
            "aabbcc",
        ],
    },
{
        "title": "Sliding Subarray Beauty",
        "topic": "sliding_window",
        "difficulty": "hard",
        "description": "For each contiguous window of size k, its beauty is the x-th smallest value in the window if that value is negative, and 0 otherwise. Report the beauty of every window from left to right.",
        "example_input": "1 -1 -3 -2 3\n3\n2",
        "constraints": "Input format: line 1 is the space-separated integers (each between -50 and 50), line 2 is k, line 3 is x (1 <= x <= k). Output format: one beauty per window, space-separated.",
        "solve": _solve_sliding_subarray_beauty,
        "sample_inputs": ["1 -1 -3 -2 3\n3\n2", "-1 -2 -3 -4 -5\n2\n2"],
        "hidden_inputs": [
            "-1\n1\n1",             # single negative element
            "1\n1\n1",              # single positive gives 0
            "0\n1\n1",              # zero is not negative
            "1 2 3\n2\n1",          # no negatives anywhere
            "-1 -1\n2\n1",
            "-1 -1\n2\n2",          # x reaches the second smallest
            "-50 50\n2\n1",         # the extremes of the allowed range
            "1 -1 -3 -2 3\n3\n1",
            "-3 1 2 -3 0 -3\n2\n1",
            "-1 -2 -3 -4 -5\n5\n3",
            "5 -3 -2 0 4 -1\n3\n2",
        ],
    },
{
        "title": "Maximum Points You Can Obtain from Cards",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Cards lie in a row. You take exactly k cards, each time from either the far left or the far right end. Return the largest total you can collect.",
        "example_input": "1 2 3 4 5 6 1\n3",
        "constraints": "Input format: line 1 is the space-separated card values, line 2 is k (1 <= k <= number of cards). Output format: a single integer.",
        "solve": _solve_max_points_from_cards,
        "sample_inputs": ["1 2 3 4 5 6 1\n3", "2 2 2\n2"],
        "hidden_inputs": [
            "5\n1",                 # a single card
            "1 2\n1",               # pick the better end
            "1 2\n2",               # both cards taken
            "9 7 7 9 7 7 9\n7",     # every card taken
            "1 1 1 1\n2",
            "1 79 80 1 1 1 200 1\n3",   # best answer wraps around the ends
            "100 40 17 9 73 75\n3",
            "1 2 3 4 5\n1",
            "5 4 3 2 1\n1",
            "1 1000 1\n2",          # the big card is unreachable in two picks
            "11 49 100 20 86 29 72\n4",
        ],
    },
{
        "title": "Number of Sub-arrays of Size K With Average at Least Threshold",
        "topic": "sliding_window",
        "difficulty": "easy",
        "description": "Count how many contiguous subarrays of length exactly k have an average greater than or equal to the given threshold.",
        "example_input": "2 2 2 2 5 5 5 8\n3\n4",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k, line 3 is the threshold. Output format: a single integer.",
        "solve": _solve_subarrays_avg_threshold,
        "sample_inputs": ["2 2 2 2 5 5 5 8\n3\n4", "11 13 17 23 29 31 7 5 2 3\n3\n5"],
        "hidden_inputs": [
            "5\n1\n5",              # exactly on the threshold
            "5\n1\n6",              # just below
            "4\n1\n4",
            "1 1 1\n3\n1",          # one window, exactly at threshold
            "1 1 1\n1\n2",          # nothing qualifies
            "10 10 10\n1\n10",      # every window qualifies
            "0 0 0\n2\n0",          # zeros against a zero threshold
            "-1 -1 -1\n2\n-1",      # negatives
            "4 4 4 4\n2\n4",
            "1 2 3 4 5\n2\n3",
            "9 9 9 1 1 1\n3\n5",
        ],
    },
{
        "title": "Check If a String Contains All Binary Codes of Size K",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a binary string s and an integer k, decide whether every possible binary string of length k appears somewhere in s as a substring.",
        "example_input": "00110110\n2",
        "constraints": "Input format: line 1 is the binary string, line 2 is k. Output format: \"true\" or \"false\".",
        "solve": _solve_all_binary_codes,
        "sample_inputs": ["00110110\n2", "0110\n2"],
        "hidden_inputs": [
            "0\n1",                 # missing the code "1"
            "01\n1",                # both length-1 codes present
            "1\n2",                 # string shorter than k
            "0000\n1",              # only zeros
            "00\n2",                # only one of four codes
            "0011\n2",              # missing "10"
            "00110\n2",             # all four present
            "1111\n2",
            "0000000001011100\n4",
            "010101\n3",
            "00110110\n3",          # too short to hold all eight codes
        ],
    },
{
        "title": "Find All Anagrams in a String",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given strings s and p, return the starting index of every substring of s that is an anagram of p, in increasing order.",
        "example_input": "cbaebabacd\nabc",
        "constraints": "Input format: line 1 is s, line 2 is p (both lowercase). Output format: the starting indices, space-separated (empty if none).",
        "solve": _solve_find_all_anagrams,
        "sample_inputs": ["cbaebabacd\nabc", "abab\nab"],
        "hidden_inputs": [
            "a\na",                 # match at index 0
            "a\nb",                 # no match
            "a\nab",                # p longer than s
            "aa\na",                # overlapping single-letter matches
            "aaa\naa",              # overlapping windows both match
            "ab\nba",
            "abc\ncba",
            "baa\naa",
            "aaaaaaaaaa\naaaaaaaaaa",   # the whole string
            "cbaebabacd\nabcd",     # p longer than any anagram present
            "abacbabc\nabc",
        ],
    },
{
        "title": "Substrings of Size Three with Distinct Characters",
        "topic": "sliding_window",
        "difficulty": "easy",
        "description": "Count the substrings of length exactly three in which all three characters are different. Substrings that occur more than once are counted each time.",
        "example_input": "xyzzaz",
        "constraints": "Input format: one line containing the string (lowercase). Output format: a single integer.",
        "solve": _solve_substrings_size_three,
        "sample_inputs": ["xyzzaz", "aababcabc"],
        "hidden_inputs": [
            "a",                    # shorter than three
            "ab",
            "abc",                  # exactly one good substring
            "aaa",                  # all identical
            "aab",
            "aba",                  # first and last repeat
            "abcabc",
            "aaaaaa",
            "abcdef",               # every window qualifies
            "zzzabc",               # a dead run followed by a good one
            "abababab",
        ],
    },
{
        "title": "Count Good Cyclic Rotations",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "A cyclic rotation is good when no two characters that sit next to each other in the rotated string are equal, treating the string as a straight line rather than a circle. Count how many of the rotations are good.",
        "example_input": "abab",
        "constraints": "Input format: one line containing the string (lowercase). Output format: a single integer.",
        "solve": _solve_good_cyclic_rotations,
        "sample_inputs": ["abab", "aaa"],
        "hidden_inputs": [
            "a",                    # a single character is trivially good
            "aa",                   # no rotation can separate them
            "ab",                   # both rotations are good
            "aab",
            "abc",                  # every rotation is good
            "aabb",
            "abba",
            "abcabc",
            "aaab",
            "ababab",
            "xyzxyz",
        ],
    },
{
        "title": "Count the Number of Good Subarrays",
        "topic": "sliding_window",
        "difficulty": "hard",
        "description": "A subarray is good when it contains at least k pairs of indices holding equal values. Count how many contiguous subarrays are good.",
        "example_input": "1 1 1 1 1\n10",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: a single integer.",
        "solve": _solve_count_good_subarrays,
        "sample_inputs": ["1 1 1 1 1\n10", "3 1 4 3 2 2 4\n2"],
        "hidden_inputs": [
            "1\n1",                 # a single element has no pairs
            "1 1\n1",               # exactly one pair
            "1 1\n2",               # not enough pairs anywhere
            "1 2 3\n1",             # no equal values at all
            "1 1 1\n1",
            "1 1 1\n3",             # the whole array is the only good one
            "2 2 2 2\n2",
            "1 2 1 2 1\n2",
            "5 5 5 5 5\n1",
            "1 1 1 1 1\n11",        # k just beyond the maximum
            "7 7 7 7 7 7\n15",      # k equals the total pair count
        ],
    },
{
        "title": "Find the Longest Semi-Repetitive Substring",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "A string of digits is semi-repetitive when at most one pair of adjacent characters is equal. Return the length of the longest semi-repetitive substring.",
        "example_input": "52233",
        "constraints": "Input format: one line containing the digit string. Output format: a single integer.",
        "solve": _solve_longest_semi_repetitive,
        "sample_inputs": ["52233", "1111111"],
        "hidden_inputs": [
            "5",                    # single digit
            "11",                   # exactly one adjacent pair
            "12",                   # no adjacent pair
            "111",                  # two pairs, only one allowed
            "1111",
            "5494",                 # already semi-repetitive throughout
            "0010",
            "1223456",
            "1223334",              # the second run forces a cut
            "0000000",
            "12345678",             # no repeats at all
        ],
    },
{
        "title": "Maximum Number of Vowels in a Substring of Given Length",
        "topic": "sliding_window", "difficulty": "easy",
        "description": "Return the greatest number of vowels that any run of exactly k consecutive letters can contain.",
        "example_input": "abciiidef\n3",
        "constraints": "Input format: line 1 is the lowercase string, line 2 is k (1 <= k <= length). Output format: a single integer.",
        "solve": _solve_max_vowels_substring,
        "sample_inputs": ["abciiidef\n3", "aeiou\n2"],
        "hidden_inputs": [
            "a\n1",                 # one vowel
            "b\n1",                 # no vowels
            "ab\n1",
            "ab\n2",
            "leetcode\n3",
            "rhythms\n4",           # no vowels anywhere
            "aeiou\n5",             # every letter is a vowel
            "tryhard\n4",
            "aaaaa\n1",
            "weallloveleetcode\n7",
        ],
    },
{
        "title": "Find the K-Beauty of a Number",
        "topic": "sliding_window", "difficulty": "easy",
        "description": "Take every run of exactly k consecutive digits of the number. Count how many of those runs, read as numbers, divide the original exactly. Runs equal to zero never count.",
        "example_input": "240\n2",
        "constraints": "Input format: line 1 is the number written out in digits, line 2 is k. Output format: a single integer.",
        "solve": _solve_k_beauty,
        "sample_inputs": ["240\n2", "430043\n2"],
        "hidden_inputs": [
            "1\n1",                 # the whole number divides itself
            "5\n1",
            "10\n1",                # a run of zero never counts
            "11\n1",
            "20\n2",                # the run is the whole number
            "100\n1",
            "1111\n2",
            "123456\n3",            # nothing divides
            "600\n1",
            "240\n1",
        ],
    },
{
        "title": "Defuse the Bomb",
        "topic": "sliding_window", "difficulty": "easy",
        "description": "The numbers are arranged in a circle. For each position, replace it by the total of the next k numbers clockwise when k is positive, the total of the previous k when k is negative, and zero when k is zero.",
        "example_input": "5 7 1 4\n3",
        "constraints": "Input format: line 1 is the space-separated numbers, line 2 is k. Output format: the replacement numbers, space-separated.",
        "solve": _solve_defuse_the_bomb,
        "sample_inputs": ["5 7 1 4\n3", "1 2 3 4\n0"],
        "hidden_inputs": [
            "1\n0",                 # k of zero blanks everything
            "1 2\n0",
            "1 2\n1",               # the circle wraps immediately
            "1 2\n-1",              # counting backwards
            "2 4 9 3\n-2",
            "1 2 3 4\n4",           # k equal to the length
            "1 2 3 4\n-4",
            "5 5 5\n1",
            "0 0 0\n2",
            "1 2 3 4 5\n2",
        ],
    },
{
        "title": "Minimum Recolors to Get K Consecutive Black Blocks",
        "topic": "sliding_window", "difficulty": "easy",
        "description": "Blocks are coloured white or black. Return the fewest white blocks that must be repainted black so that some run of exactly k consecutive blocks is entirely black.",
        "example_input": "WBBWWBBWBW\n7",
        "constraints": "Input format: line 1 is the block string using W and B, line 2 is k (1 <= k <= length). Output format: a single integer.",
        "solve": _solve_min_recolors,
        "sample_inputs": ["WBBWWBBWBW\n7", "WBWBBBW\n2"],
        "hidden_inputs": [
            "B\n1",                 # already black
            "W\n1",                 # one repaint
            "WB\n1",
            "WW\n2",                # both must change
            "BB\n2",                # neither does
            "WBW\n2",
            "BWB\n3",
            "WWWWW\n5",
            "BBBBB\n3",
            "WBBWWBBWBW\n3",
        ],
    },
{
        "title": "Longest Harmonious Subsequence",
        "topic": "sliding_window", "difficulty": "easy",
        "description": "A harmonious group is one where the largest and smallest values differ by exactly one. Return the size of the largest such group that can be picked out of the list, ignoring order.",
        "example_input": "1 3 2 2 5 2 3 7",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_longest_harmonious,
        "sample_inputs": ["1 3 2 2 5 2 3 7", "1 2 3 4"],
        "hidden_inputs": [
            "1",                    # nothing can pair
            "1 1",                  # equal values differ by zero, not one
            "1 2",
            "2 1",
            "1 3",                  # a gap of two
            "1 1 1 1",
            "1 1 2 2 2",
            "-1 0",                 # negatives
            "5 5 5 6",
            "1 2 2 3 3 3 4 4 4 4",
        ],
    },
{
        "title": "Grumpy Bookstore Owner",
        "topic": "sliding_window", "difficulty": "easy",
        "description": "Customers arrive one minute at a time, and are only satisfied if the owner is not grumpy. The owner may stop being grumpy for one stretch of exactly the given number of minutes. Return the greatest number of satisfied customers possible.",
        "example_input": "1 0 1 2 1 1 7 5\n0 1 0 1 0 1 0 1\n3",
        "constraints": "Input format: line 1 is the customers per minute, line 2 is 1 for a grumpy minute and 0 otherwise, line 3 is the stretch length. Output format: a single integer.",
        "solve": _solve_grumpy_bookstore,
        "sample_inputs": ["1 0 1 2 1 1 7 5\n0 1 0 1 0 1 0 1\n3", "1\n0\n1"],
        "hidden_inputs": [
            "1\n1\n1",              # the one grumpy minute is fixed
            "5\n0\n1",              # never grumpy
            "1 2\n1 1\n1",          # only one minute can be fixed
            "1 2\n1 1\n2",          # both can
            "1 2\n0 0\n2",
            "4 10 10\n1 1 0\n2",
            "0 0 0\n1 1 1\n2",      # no customers to save
            "2 6 6 9\n0 0 1 1\n1",
            "1 1 1 1 1\n1 0 1 0 1\n2",
            "10 1 7\n0 0 0\n1",
        ],
    },
{
        "title": "Count Subarrays With Fixed Bounds",
        "topic": "sliding_window", "difficulty": "hard",
        "description": "Count the runs of consecutive values whose smallest value is exactly the given lower bound and whose largest is exactly the given upper bound.",
        "example_input": "1 3 5 2 7 5\n1 5",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 holds the lower and upper bounds. Output format: a single integer.",
        "solve": _solve_count_subarrays_fixed_bounds,
        "sample_inputs": ["1 3 5 2 7 5\n1 5", "1 1 1 1\n1 1"],
        "hidden_inputs": [
            "1\n1 1",               # the single value matches both bounds
            "1\n1 2",               # the upper bound never appears
            "2\n1 2",               # the lower bound never appears
            "1 2\n1 2",
            "2 1\n1 2",             # order must not matter
            "1 3\n1 3",
            "1 9 2\n1 2",           # a value outside the bounds splits the run
            "1 2 1 2\n1 2",
            "5 5 5\n5 5",
            "1 2 3 1 2 3\n1 3",
        ],
    },
{
        "title": "Maximum Number of Robots Within Budget",
        "topic": "sliding_window", "difficulty": "hard",
        "description": "Running a consecutive stretch of robots costs the largest charging cost among them plus the number of robots times the total of their running costs. Return the longest stretch whose cost stays within the budget.",
        "example_input": "3 6 1 3 4\n2 1 3 4 5\n25",
        "constraints": "Input format: line 1 is the charging costs, line 2 is the running costs, line 3 is the budget. Output format: a single integer.",
        "solve": _solve_max_robots_budget,
        "sample_inputs": ["3 6 1 3 4\n2 1 3 4 5\n25", "11 12 19\n10 8 7\n19"],
        "hidden_inputs": [
            "1\n1\n2",              # one robot exactly affordable
            "1\n1\n1",              # one robot just too dear
            "5\n1\n5",
            "1 1\n1 1\n3",          # both robots fit
            "1 1\n1 1\n2",          # only one does
            "1 1 1\n1 1 1\n4",
            "10 10 10\n1 1 1\n11",
            "3 6 1 3 4\n2 1 3 4 5\n7",
            "1 2 3 4 5\n5 4 3 2 1\n100",    # the whole row fits
            "50 50 50\n50 50 50\n1",        # nothing fits
        ],
    },
{
        "title": "Constrained Subsequence Sum",
        "topic": "sliding_window", "difficulty": "hard",
        "description": "Pick a non-empty group of values keeping their original order, with the rule that no two chosen positions may be more than k apart. Return the greatest total possible.",
        "example_input": "10 2 -10 5 20\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k (k >= 1). Output format: a single integer.",
        "solve": _solve_constrained_subsequence_sum,
        "sample_inputs": ["10 2 -10 5 20\n2", "-1 -2 -3\n1"],
        "hidden_inputs": [
            "5\n1",                 # a single value
            "-5\n1",                # a single negative value
            "1 2\n1",
            "-1 2\n1",              # the negative is skipped
            "2 -1\n1",
            "-5 -2 -3\n2",          # all negative, take the least bad
            "10 -2 -10 -5 20\n2",
            "1 2 3 4 5\n1",         # every value is taken
            "0 0 0\n2",
            "-8269 3217 -4023 -4138 -683 6455 -3621 9242 4015 -3790\n5",
        ],
    },
{
        "title": "Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit",
        "topic": "sliding_window", "difficulty": "hard",
        "description": "Return the length of the longest run of consecutive values in which the largest and smallest differ by no more than the given limit.",
        "example_input": "8 2 4 7\n4",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is the limit. Output format: a single integer.",
        "solve": _solve_longest_subarray_abs_limit,
        "sample_inputs": ["8 2 4 7\n4", "10 1 2 4 7 2\n5"],
        "hidden_inputs": [
            "1\n0",                 # a single value always qualifies
            "1 1\n0",               # equal values differ by nothing
            "1 2\n0",               # a limit of zero splits them
            "1 2\n1",
            "5 5 5 5\n0",
            "1 5 9\n3",             # no pair fits
            "4 2 2 2 4 4 2 2\n0",
            "4 2 2 2 4 4 2 2\n2",
            "-1 -2 -3\n1",          # negatives
            "1 2 3 4 5 6 7 8\n3",
        ],
    },
{
        "title": "Jump Game VI",
        "topic": "sliding_window", "difficulty": "hard",
        "description": "Start at the first position and move forward by anywhere from one to k places at a time until reaching the last position, collecting the value at every position you land on including the first and last. Return the greatest total possible.",
        "example_input": "1 -1 -2 4 -7 3\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k (k >= 1). Output format: a single integer.",
        "solve": _solve_jump_game_vi,
        "sample_inputs": ["1 -1 -2 4 -7 3\n2", "10 -5 -2 4 0 3\n3"],
        "hidden_inputs": [
            "5\n1",                 # start and finish are the same place
            "-5\n1",
            "1 2\n1",               # every position must be visited
            "1 -2\n1",              # the negative cannot be avoided
            "1 -2 3\n2",            # k of two skips the negative
            "1 -2 3\n1",
            "1 -5 -20 4 -1 3 -6 -3\n2",
            "0 0 0 0\n2",
            "-1 -1 -1\n2",          # all negative
            "1 2 3 4 5\n4",         # one jump straight to the end
        ],
    },
]
