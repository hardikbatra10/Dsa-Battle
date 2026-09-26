"""Two Pointers problems."""

def _solve_remove_duplicates(lines):
    nums = list(map(int, lines[0].split()))
    out = []
    for n in nums:
        if not out or out[-1] != n:
            out.append(n)
    return " ".join(map(str, out))


def _solve_container_water(lines):
    heights = list(map(int, lines[0].split()))
    l, r = 0, len(heights) - 1
    best = 0
    while l < r:
        best = max(best, min(heights[l], heights[r]) * (r - l))
        if heights[l] < heights[r]:
            l += 1
        else:
            r -= 1
    return str(best)


def _solve_three_sum(lines):
    nums = sorted(map(int, lines[0].split()))
    n = len(nums)
    res = []
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s == 0:
                res.append((nums[i], nums[l], nums[r]))
                while l < r and nums[l] == nums[l + 1]:
                    l += 1
                while l < r and nums[r] == nums[r - 1]:
                    r -= 1
                l += 1
                r -= 1
            elif s < 0:
                l += 1
            else:
                r -= 1
    return "\n".join(" ".join(map(str, t)) for t in res)

def _solve_move_zeroes(lines):
    nums = list(map(int, lines[0].split()))
    out = [x for x in nums if x != 0]
    out.extend([0] * (len(nums) - len(out)))
    return " ".join(map(str, out))


def _solve_reverse_vowels(lines):
    s = list(lines[0])
    vowels = set("aeiouAEIOU")
    i, j = 0, len(s) - 1
    while i < j:
        if s[i] not in vowels:
            i += 1
        elif s[j] not in vowels:
            j -= 1
        else:
            s[i], s[j] = s[j], s[i]
            i += 1
            j -= 1
    return "".join(s)


def _solve_sorted_squares(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    out = [0] * n
    i, j = 0, n - 1
    for k in range(n - 1, -1, -1):
        if abs(nums[i]) > abs(nums[j]):
            out[k] = nums[i] * nums[i]
            i += 1
        else:
            out[k] = nums[j] * nums[j]
            j -= 1
    return " ".join(map(str, out))


def _solve_remove_element(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    return " ".join(str(x) for x in nums if x != target)


def _solve_valid_palindrome_ii(lines):
    s = lines[0]

    def ok(lo, hi):
        while lo < hi:
            if s[lo] != s[hi]:
                return False
            lo += 1
            hi -= 1
        return True

    i, j = 0, len(s) - 1
    while i < j:
        if s[i] != s[j]:
            return "true" if ok(i + 1, j) or ok(i, j - 1) else "false"
        i += 1
        j -= 1
    return "true"


def _solve_sort_colors(lines):
    nums = list(map(int, lines[0].split()))
    low, mid, high = 0, 0, len(nums) - 1
    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 2:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
        else:
            mid += 1
    return " ".join(map(str, nums))


def _solve_three_sum_closest(lines):
    nums = sorted(map(int, lines[0].split()))
    target = int(lines[1])
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            total = nums[i] + nums[lo] + nums[hi]
            if abs(total - target) < abs(best - target):
                best = total
            if total == target:
                return str(total)
            if total < target:
                lo += 1
            else:
                hi -= 1
    return str(best)


def _solve_longest_mountain(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    best = 0
    i = 1
    while i < n - 1:
        if nums[i - 1] < nums[i] > nums[i + 1]:
            lo = i - 1
            while lo > 0 and nums[lo - 1] < nums[lo]:
                lo -= 1
            hi = i + 1
            while hi < n - 1 and nums[hi] > nums[hi + 1]:
                hi += 1
            best = max(best, hi - lo + 1)
            i = hi
        else:
            i += 1
    return str(best)


def _solve_boats_to_save_people(lines):
    people = sorted(map(int, lines[0].split()))
    limit = int(lines[1])
    i, j = 0, len(people) - 1
    boats = 0
    while i <= j:
        if people[i] + people[j] <= limit:
            i += 1
        j -= 1
        boats += 1
    return str(boats)


def _solve_four_sum(lines):
    nums = sorted(map(int, lines[0].split()))
    target = int(lines[1])
    n = len(nums)
    out = []
    for i in range(n - 3):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            lo, hi = j + 1, n - 1
            while lo < hi:
                total = nums[i] + nums[j] + nums[lo] + nums[hi]
                if total == target:
                    out.append((nums[i], nums[j], nums[lo], nums[hi]))
                    while lo < hi and nums[lo] == nums[lo + 1]:
                        lo += 1
                    while lo < hi and nums[hi] == nums[hi - 1]:
                        hi -= 1
                    lo += 1
                    hi -= 1
                elif total < target:
                    lo += 1
                else:
                    hi -= 1
    return "\n".join(" ".join(map(str, q)) for q in sorted(out))


def _solve_subarrays_k_distinct(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])

    def at_most(limit):
        from collections import defaultdict
        count = defaultdict(int)
        left = 0
        total = 0
        for right, v in enumerate(nums):
            count[v] += 1
            while len(count) > limit:
                count[nums[left]] -= 1
                if count[nums[left]] == 0:
                    del count[nums[left]]
                left += 1
            total += right - left + 1
        return total

    return str(at_most(k) - at_most(k - 1))

def _solve_merge_sorted_array(lines):
    a = list(map(int, lines[0].split())) if lines[0].strip() else []
    b = list(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []
    out = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            out.append(a[i])
            i += 1
        else:
            out.append(b[j])
            j += 1
    out.extend(a[i:])
    out.extend(b[j:])
    return " ".join(map(str, out))


def _solve_two_sum_sorted(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        total = nums[lo] + nums[hi]
        if total == target:
            return f"{lo + 1} {hi + 1}"
        if total < target:
            lo += 1
        else:
            hi -= 1
    return "-1 -1"


def _solve_is_subsequence_count(lines):
    s = lines[0]
    t = lines[1] if len(lines) > 1 else ""
    i = 0
    for c in t:
        if i < len(s) and s[i] == c:
            i += 1
    return str(i)


def _solve_reverse_string_words_count(lines):
    s = lines[0]
    lo, hi = 0, len(s) - 1
    count = 0
    while lo < hi:
        if s[lo] == s[hi]:
            count += 1
        lo += 1
        hi -= 1
    return str(count)


def _solve_sort_array_by_parity(lines):
    nums = list(map(int, lines[0].split()))
    return " ".join(map(str, [v for v in nums if v % 2 == 0]
                        + [v for v in nums if v % 2 != 0]))


def _solve_backspace_two_pointer(lines):
    def build(text):
        out = []
        for c in text:
            if c == "#":
                if out:
                    out.pop()
            else:
                out.append(c)
        return "".join(out)

    return build(lines[0])


def _solve_interval_intersections(lines):
    k = int(lines[0])
    first = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    m = int(lines[1 + k])
    second = [tuple(map(int, lines[2 + k + i].split())) for i in range(m)]
    out = []
    i = j = 0
    while i < k and j < m:
        lo = max(first[i][0], second[j][0])
        hi = min(first[i][1], second[j][1])
        if lo <= hi:
            out.append((lo, hi))
        if first[i][1] < second[j][1]:
            i += 1
        else:
            j += 1
    return "\n".join(f"{a} {b}" for a, b in out)


def _solve_partition_array_into_disjoint(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    suffix_min = [0] * n
    suffix_min[n - 1] = nums[n - 1]
    for i in range(n - 2, -1, -1):
        suffix_min[i] = min(nums[i], suffix_min[i + 1])
    running_max = nums[0]
    for i in range(n - 1):
        running_max = max(running_max, nums[i])
        if running_max <= suffix_min[i + 1]:
            return str(i + 1)
    return str(n)


def _solve_shortest_unsorted_subarray(lines):
    nums = list(map(int, lines[0].split()))
    ordered = sorted(nums)
    lo = 0
    while lo < len(nums) and nums[lo] == ordered[lo]:
        lo += 1
    if lo == len(nums):
        return "0"
    hi = len(nums) - 1
    while nums[hi] == ordered[hi]:
        hi -= 1
    return str(hi - lo + 1)


def _solve_max_consecutive_ones_iii(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    left = 0
    zeros = 0
    best = 0
    for right, v in enumerate(nums):
        if v == 0:
            zeros += 1
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1
        best = max(best, right - left + 1)
    return str(best)


def _solve_count_pairs_below_target(lines):
    nums = sorted(map(int, lines[0].split()))
    target = int(lines[1])
    lo, hi = 0, len(nums) - 1
    count = 0
    while lo < hi:
        if nums[lo] + nums[hi] < target:
            count += hi - lo
            lo += 1
        else:
            hi -= 1
    return str(count)


def _solve_rearrange_by_sign(lines):
    nums = list(map(int, lines[0].split()))
    positives = [v for v in nums if v > 0]
    negatives = [v for v in nums if v < 0]
    out = []
    for i in range(len(positives)):
        out.append(positives[i])
        out.append(negatives[i])
    return " ".join(map(str, out))


def _solve_minimum_size_pairs(lines):
    nums = sorted(map(int, lines[0].split()))
    lo, hi = 0, len(nums) - 1
    best = None
    while lo < hi:
        total = nums[lo] + nums[hi]
        best = total if best is None else max(best, total)
        lo += 1
        hi -= 1
    return str(best)


def _solve_trapping_two_pointer(lines):
    heights = list(map(int, lines[0].split()))
    lo, hi = 0, len(heights) - 1
    left_max = right_max = 0
    total = 0
    while lo < hi:
        if heights[lo] < heights[hi]:
            left_max = max(left_max, heights[lo])
            total += left_max - heights[lo]
            lo += 1
        else:
            right_max = max(right_max, heights[hi])
            total += right_max - heights[hi]
            hi -= 1
    return str(total)


def _solve_smallest_range_pair(lines):
    a = sorted(map(int, lines[0].split()))
    b = sorted(map(int, lines[1].split()))
    i = j = 0
    best = None
    while i < len(a) and j < len(b):
        gap = abs(a[i] - b[j])
        if best is None or gap < best:
            best = gap
        if a[i] < b[j]:
            i += 1
        else:
            j += 1
    return str(best)


def _solve_longest_word_in_dictionary(lines):
    s = lines[0]
    n = int(lines[1])
    words = [lines[2 + i] for i in range(n)]
    best = ""
    for w in words:
        i = 0
        for c in s:
            if i < len(w) and w[i] == c:
                i += 1
        if i == len(w):
            if len(w) > len(best) or (len(w) == len(best) and w < best):
                best = w
    return best


def _solve_three_sum_smaller(lines):
    nums = sorted(map(int, lines[0].split()))
    target = int(lines[1])
    n = len(nums)
    count = 0
    for i in range(n - 2):
        lo, hi = i + 1, n - 1
        while lo < hi:
            if nums[i] + nums[lo] + nums[hi] < target:
                count += hi - lo
                lo += 1
            else:
                hi -= 1
    return str(count)


def _solve_max_distance_two_arrays(lines):
    a = list(map(int, lines[0].split()))
    b = list(map(int, lines[1].split()))
    i = j = 0
    best = 0
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            best = max(best, j - i)
            j += 1
        else:
            i += 1
    return str(best)


def _solve_minimum_window_subsequence(lines):
    text = lines[0]
    want = lines[1]
    n = len(text)
    best_start, best_len = -1, 0
    start_at = 0
    while start_at < n:
        # Walk forward matching `want` greedily, then walk back from that
        # end to pull the left edge in as far as it will go.
        j = 0
        k = start_at
        while k < n:
            if text[k] == want[j]:
                j += 1
                if j == len(want):
                    break
            k += 1
        if j < len(want):
            break
        end = k
        j = len(want) - 1
        while j >= 0:
            if text[k] == want[j]:
                j -= 1
            k -= 1
        left = k + 1
        if best_start < 0 or end - left + 1 < best_len:
            best_start, best_len = left, end - left + 1
        start_at = left + 1
    if best_start < 0:
        return "-1"
    return text[best_start:best_start + best_len]


PROBLEMS = [
{
        "title": "Remove Duplicates from Sorted Array",
        "topic": "two_pointers",
        "difficulty": "easy",
        "description": "Given a sorted array, remove duplicates in-place so each element appears once, and return the resulting array.",
        "example_input": "0 0 1 1 1 2 2 3 3 4",
        "constraints": "Input format: one line, sorted space-separated integers (may contain duplicates). Output format: the deduplicated array, space-separated.",
        "solve": _solve_remove_duplicates,
        "sample_inputs": ["0 0 1 1 1 2 2 3 3 4", "2 2 3 4 4"],
        "hidden_inputs": [
            "1",
            "1 1",     # every element is a duplicate
            "1 2",     # no duplicates
            "1 1 2",
            "1 1 1 1",
            "1 2 3",
            "-1 0 1",  # negatives
            "-3 -3 -1 0 0 1",
            "5 5 5 5 5 5 5 5 5 5",
            "0 0 0 1 1 2 3 3 3 3",
        ],
    },
{
        "title": "Container With Most Water",
        "topic": "two_pointers",
        "difficulty": "medium",
        "description": "Given an array of heights, choose two lines that together with the x-axis form a container holding the most water. Return that max area.",
        "example_input": "1 8 6 2 5 4 8 3 7",
        "constraints": "Input format: one line of space-separated non-negative heights. Output format: a single integer.",
        "solve": _solve_container_water,
        "sample_inputs": ["1 8 6 2 5 4 8 3 7", "3 9 3 4 7"],
        "hidden_inputs": [
            "0 0",        # zero heights
            "1 1",
            "1 2",
            "2 1",
            "1 2 1",
            "5 5 5 5 5",  # flat, so width decides
            "1 0 0 0 1",  # tallest pair is also the widest pair
            "1 2 3 4 5",
            "4 3 2 1 4",
            "100 1 100",
            "2 3 4 5 18 17 6",
        ],
    },
{
        "title": "3Sum",
        "topic": "two_pointers",
        "difficulty": "hard",
        "description": "Given an integer array, return all unique triplets that sum to zero. Each triplet's values should be printed ascending; triplets should be printed in ascending lexicographic order, one per line. If none exist, print nothing.",
        "example_input": "-1 0 1 2 -1 -4",
        "constraints": "Input format: one line of space-separated integers. Output format: one triplet per line, space-separated, ascending order; empty output if none.",
        "solve": _solve_three_sum,
        "sample_inputs": ["-1 0 1 2 -1 -4", "-2 -1 0 1 3"],
        "hidden_inputs": [
            "0 0",      # fewer than three elements
            "5",
            "1 2 3",    # no triplet sums to zero
            "0 0 0",
            "0 1 1",
            "-1 -1 2",
            "1 -1 0",
            "0 0 0 0",  # duplicate triplet must be emitted once
            "-2 0 1 1 2",
            "3 0 -2 -1 1 2",
            "-1 0 1 2 -1 -4 -2 -3 3 0 4",
            "-4 -2 -2 -2 0 1 2 2 2 3 3 4 4 6 6",
        ],
    },
{
        "title": "Move Zeroes",
        "topic": "two_pointers",
        "difficulty": "easy",
        "description": "Shift every zero to the end of the list while keeping the other values in their original relative order.",
        "example_input": "0 1 0 3 12",
        "constraints": "Input format: one line of space-separated integers. Output format: the rearranged values, space-separated.",
        "solve": _solve_move_zeroes,
        "sample_inputs": ["0 1 0 3 12", "0"],
        "hidden_inputs": [
            "1",                    # nothing to move
            "0 0",                  # every value is a zero
            "1 2",                  # no zeroes at all
            "0 1",
            "1 0",                  # already in place
            "0 0 1",
            "1 0 0",
            "-1 0 -2 0 3",          # negatives keep their order
            "0 0 0 1 2 3",
            "1 2 0 3 0 4 0",
        ],
    },
{
        "title": "Reverse Vowels of a String",
        "topic": "two_pointers",
        "difficulty": "easy",
        "description": "Reverse the order in which the vowels appear in the string, leaving every other character exactly where it is. Both upper and lower case vowels count.",
        "example_input": "IceCreAm",
        "constraints": "Input format: one line containing the string. Output format: the resulting string.",
        "solve": _solve_reverse_vowels,
        "sample_inputs": ["IceCreAm", "leetcode"],
        "hidden_inputs": [
            "a",                    # one vowel, nothing to swap
            "b",                    # no vowels at all
            "ab",
            "ae",                   # two vowels swap
            "aa",                   # identical vowels, no visible change
            "aA",                   # case travels with the vowel
            "bcd",
            "hello",
            "rhythm",               # a word with no vowels
            "aeiouAEIOU",
        ],
    },
{
        "title": "Squares of a Sorted Array",
        "topic": "two_pointers",
        "difficulty": "easy",
        "description": "Given a list of integers already in non-decreasing order, return their squares in non-decreasing order.",
        "example_input": "-4 -1 0 3 10",
        "constraints": "Input format: one line of space-separated integers in non-decreasing order. Output format: the sorted squares, space-separated.",
        "solve": _solve_sorted_squares,
        "sample_inputs": ["-4 -1 0 3 10", "-7 -3 2 3 11"],
        "hidden_inputs": [
            "0",                    # a single zero
            "5",                    # a single positive
            "-5",                   # a single negative
            "-1 1",                 # equal squares
            "-2 -1",                # all negative, order reverses
            "1 2",                  # all positive, order kept
            "-3 0 3",
            "-1 0 1",
            "-5 -4 -3 -2 -1",
            "-2 -2 0 2 2",          # duplicates on both sides of zero
        ],
    },
{
        "title": "Remove Element",
        "topic": "two_pointers",
        "difficulty": "easy",
        "description": "Delete every occurrence of the given value from the list, keeping the remaining values in their original order.",
        "example_input": "3 2 2 3\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is the value to remove. Output format: the remaining values, space-separated (empty if none remain).",
        "solve": _solve_remove_element,
        "sample_inputs": ["3 2 2 3\n3", "0 1 2 2 3 0 4 2\n2"],
        "hidden_inputs": [
            "1\n1",                 # the list empties
            "1\n2",                 # nothing matches
            "1 1\n1",
            "1 2\n1",               # the first value goes
            "1 2\n2",               # the last value goes
            "2 1 2\n2",             # both ends go
            "0 0 0\n0",
            "-1 -1 0\n-1",          # negatives
            "1 2 3 4 5\n3",
            "4 4 4 1 4\n4",
        ],
    },
{
        "title": "Valid Palindrome II",
        "topic": "two_pointers",
        "difficulty": "easy",
        "description": "Decide whether the string can be made to read the same forwards and backwards by deleting at most one character.",
        "example_input": "aba",
        "constraints": "Input format: one line containing the lowercase string. Output format: \"true\" or \"false\".",
        "solve": _solve_valid_palindrome_ii,
        "sample_inputs": ["aba", "abca"],
        "hidden_inputs": [
            "a",                    # already a palindrome
            "ab",                   # deleting either letter works
            "aa",
            "abc",                  # one deletion is not enough
            "abccba",               # already a palindrome, no deletion needed
            "abcd",
            "deeee",                # the odd letter is at the very start
            "eeeed",                # and at the very end
            "cbbcc",
            "abcdefdba",            # two mismatches, impossible
        ],
    },
{
        "title": "Sort Colors",
        "topic": "two_pointers",
        "difficulty": "medium",
        "description": "The list holds only the values 0, 1 and 2. Arrange them in non-decreasing order in a single pass.",
        "example_input": "2 0 2 1 1 0",
        "constraints": "Input format: one line of space-separated values, each 0, 1 or 2. Output format: the sorted values, space-separated.",
        "solve": _solve_sort_colors,
        "sample_inputs": ["2 0 2 1 1 0", "2 0 1"],
        "hidden_inputs": [
            "0",                    # a single value
            "2",
            "1 0",                  # one swap
            "2 0",
            "0 1 2",                # already sorted
            "2 1 0",                # fully reversed
            "0 0 0",                # one colour only
            "2 2 2",
            "1 1 0 0 2 2",
            "2 0 2 0 2 0 1",
        ],
    },
{
        "title": "3Sum Closest",
        "topic": "two_pointers",
        "difficulty": "medium",
        "description": "Choose three values from the list whose total comes closest to the target, and return that total. Exactly one total is closest.",
        "example_input": "-1 2 1 -4\n1",
        "constraints": "Input format: line 1 is the space-separated integers (at least three), line 2 is the target. Output format: a single integer.",
        "solve": _solve_three_sum_closest,
        "sample_inputs": ["-1 2 1 -4\n1", "0 0 0\n1"],
        "hidden_inputs": [
            "1 2 3\n6",             # an exact hit
            "1 2 3\n0",             # the target is far below
            "1 2 3\n100",           # far above
            "0 0 0\n0",
            "-1 -1 -1\n-3",
            "-3 -2 -5 3 -4\n-1",
            "1 1 1 1\n3",           # duplicates everywhere
            "4 0 5 -5 3 3 0 -4 -5\n-2",
            "-100 -98 -2 -1\n-101",
            "1 2 4 8 16 32\n21",
        ],
    },
{
        "title": "Longest Mountain in Array",
        "topic": "two_pointers",
        "difficulty": "medium",
        "description": "A mountain is a run of at least three values that rises strictly to a single peak and then falls strictly away from it. Return the length of the longest mountain, or 0 if there is none.",
        "example_input": "2 1 4 7 3 2 5",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_longest_mountain,
        "sample_inputs": ["2 1 4 7 3 2 5", "2 2 2"],
        "hidden_inputs": [
            "1",                    # too short for a mountain
            "1 2",
            "1 2 3",                # rising only, no descent
            "3 2 1",                # falling only
            "1 2 1",                # the smallest mountain
            "1 1 1",                # flat, no strict rise
            "1 2 2 1",              # the plateau breaks the peak
            "0 1 0 1 0",            # two separate mountains
            "1 3 5 4 2 0",          # one mountain spanning everything
            "2 3 3 2 0 2",
        ],
    },
{
        "title": "Boats to Save People",
        "topic": "two_pointers",
        "difficulty": "medium",
        "description": "Every boat carries at most two people and can hold a limited total weight. Return the fewest boats needed to carry everybody.",
        "example_input": "1 2\n3",
        "constraints": "Input format: line 1 is the space-separated weights, line 2 is the weight limit; no single person exceeds it. Output format: a single integer.",
        "solve": _solve_boats_to_save_people,
        "sample_inputs": ["1 2\n3", "3 2 2 1\n3"],
        "hidden_inputs": [
            "1\n1",                 # one person, one boat
            "1 1\n2",               # both fit together
            "1 1\n1",               # neither can share
            "2 2\n3",
            "3 5 3 4\n5",           # nobody can share
            "1 2 3\n3",
            "1 1 1 1\n2",           # perfect pairing
            "5 1 4 2 3\n6",         # heaviest pairs with lightest
            "2 2 2 2 2\n4",
            "1 2 2 3\n3",
        ],
    },
{
        "title": "4Sum",
        "topic": "two_pointers",
        "difficulty": "hard",
        "description": "Return every distinct group of four values from the list that adds up to the target. Each group is written in increasing order, and the groups are listed in increasing order.",
        "example_input": "1 0 -1 0 -2 2\n0",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is the target. Output format: one group per line, values space-separated (empty if none).",
        "solve": _solve_four_sum,
        "sample_inputs": ["1 0 -1 0 -2 2\n0", "2 2 2 2 2\n8"],
        "hidden_inputs": [
            "1 2 3\n6",             # fewer than four values, empty output
            "1 2 3 4\n10",          # the only group
            "1 2 3 4\n11",          # just out of reach
            "0 0 0 0\n0",
            "0 0 0 0 0\n0",         # duplicates must not repeat a line
            "1 1 1 1 1\n4",
            "-3 -1 0 2 4 5\n0",
            "-2 -1 0 0 1 2\n0",
            "1 -2 -5 -4 -3 3 3 5\n-11",
            "2 2 2 2 2 2\n8",
        ],
    },
{
        "title": "Subarrays with K Different Integers",
        "topic": "two_pointers",
        "difficulty": "hard",
        "description": "Count the runs of consecutive values that contain exactly k different values between them.",
        "example_input": "1 2 1 2 3\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: a single integer.",
        "solve": _solve_subarrays_k_distinct,
        "sample_inputs": ["1 2 1 2 3\n2", "1 2 1 3 4\n3"],
        "hidden_inputs": [
            "1\n1",                 # a single value
            "1\n2",                 # k exceeds what exists
            "1 1\n1",               # three runs of one value
            "1 2\n1",
            "1 2\n2",
            "1 1 1\n1",
            "1 2 3\n3",             # only the whole list qualifies
            "1 2 3\n1",             # every single element
            "2 2 2 2\n1",
            "1 2 1 2 3 4\n3",
        ],
    },
{
        "title": "Merge Sorted Array",
        "topic": "two_pointers", "difficulty": "easy",
        "description": "Combine two lists that are each already in non-decreasing order into one list that is also in non-decreasing order.",
        "example_input": "1 2 3\n2 5 6",
        "constraints": "Input format: line 1 and line 2 are the two lists in non-decreasing order, either of which may be empty. Output format: the merged list, space-separated.",
        "solve": _solve_merge_sorted_array,
        "sample_inputs": ["1 2 3\n2 5 6", "1\n"],
        "hidden_inputs": [
            "1\n1",                 # equal values
            "1\n2",
            "2\n1",
            "1 2 3\n",              # the second list is empty
            "\n1 2 3",              # the first list is empty
            "1 1 1\n1 1 1",
            "1 2 3\n4 5 6",         # disjoint ranges
            "4 5 6\n1 2 3",
            "-5 -3\n-4 -2",         # negatives
            "1 3 5 7\n2 4 6 8",     # strict interleave
        ],
    },
{
        "title": "Two Sum II - Input Array Is Sorted",
        "topic": "two_pointers", "difficulty": "easy",
        "description": "Given values in non-decreasing order and a target, find the two whose total is the target and return their positions counting from one. Exactly one pair works.",
        "example_input": "2 7 11 15\n9",
        "constraints": "Input format: line 1 is the sorted values, line 2 is the target. Exactly one pair adds up to it. Output format: the two positions, space-separated.",
        "solve": _solve_two_sum_sorted,
        "sample_inputs": ["2 7 11 15\n9", "2 3 4\n6"],
        "hidden_inputs": [
            "1 2\n3",               # the only pair
            "-1 0\n-1",             # negatives
            "1 2 3\n3",             # the pair sits at the front
            "1 2 3\n5",             # and at the back
            "1 2 3 4\n5",
            "0 0 3 4\n0",           # zeroes
            "-3 -1 0 2\n-1",
            "1 3 5 7 9\n12",
            "2 7 11 15\n26",
            "-10 -5 0 5 10\n0",
        ],
    },
{
        "title": "Longest Common Prefix Length of Subsequence",
        "topic": "two_pointers", "difficulty": "easy",
        "description": "Walk through the second text once, matching its letters in order against the first. Return how many letters of the first text get matched.",
        "example_input": "abc\nahbgdc",
        "constraints": "Input format: line 1 is the shorter text, line 2 is the longer, both lowercase. Output format: a single integer.",
        "solve": _solve_is_subsequence_count,
        "sample_inputs": ["abc\nahbgdc", "axc\nahbgdc"],
        "hidden_inputs": [
            "a\na",                 # a full match
            "a\nb",                 # nothing matches
            "ab\nba",               # order matters
            "ab\nab",
            "abc\nab",              # the second text runs out
            "aa\naba",
            "aaa\naa",
            "ace\nabcde",
            "bb\nbabab",
            "xyz\nxxyyzz",
        ],
    },
{
        "title": "Count Matching Mirror Positions",
        "topic": "two_pointers", "difficulty": "easy",
        "description": "Walk inwards from both ends at once and count how many times the two letters being looked at are the same, stopping when the pointers meet.",
        "example_input": "abcba",
        "constraints": "Input format: one line containing the lowercase text. Output format: a single integer.",
        "solve": _solve_reverse_string_words_count,
        "sample_inputs": ["abcba", "abcd"],
        "hidden_inputs": [
            "a",                    # the pointers start together
            "aa",                   # one matching pair
            "ab",
            "aba",                  # the middle letter is never compared
            "abb",
            "abccba",               # every pair matches
            "abcdef",
            "aabbaa",
            "racecar",
            "zzzz",
        ],
    },
{
        "title": "Sort Array By Parity",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "Rearrange the values so that every even one comes before every odd one, keeping the original order within each group.",
        "example_input": "3 1 2 4",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: the rearranged values, space-separated.",
        "solve": _solve_sort_array_by_parity,
        "sample_inputs": ["3 1 2 4", "0"],
        "hidden_inputs": [
            "1",                    # a single odd value
            "2",                    # a single even value
            "1 2",
            "2 1",                  # already in order
            "1 3 5",                # no even values
            "2 4 6",                # no odd values
            "0 1 0 1",
            "1 1 2 2",
            "4 2 5 7",
            "0 0 0 1",
        ],
    },
{
        "title": "Backspace String",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "A hash character means the letter before it was deleted, and a hash with nothing before it does nothing. Return what the text finally reads.",
        "example_input": "ab#c",
        "constraints": "Input format: one line of lowercase letters and hashes. Output format: the resulting text, or an empty line if nothing remains.",
        "solve": _solve_backspace_two_pointer,
        "sample_inputs": ["ab#c", "a##c"],
        "hidden_inputs": [
            "a",                    # nothing is deleted
            "#",                    # a hash with nothing before it
            "a#",                   # the text empties
            "##",
            "ab#",
            "a#b",
            "abc###",               # everything deleted
            "a#b#c",
            "####a",
            "xy#z#w",
        ],
    },
{
        "title": "Interval List Intersections",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "Both lists hold ranges already in increasing order and none overlapping within a list. Report every stretch covered by a range from each list.",
        "example_input": "4\n0 2\n5 10\n13 23\n24 25\n3\n1 5\n8 12\n15 24",
        "constraints": "Input format: line 1 is the size of the first list, then that many lines each \"start end\", then a line with the size of the second list, then that many lines. Output format: one shared stretch per line as \"start end\" (empty if none).",
        "solve": _solve_interval_intersections,
        "sample_inputs": ["4\n0 2\n5 10\n13 23\n24 25\n3\n1 5\n8 12\n15 24", "1\n1 3\n1\n5 9"],
        "hidden_inputs": [
            "1\n1 2\n1\n1 2",       # identical ranges
            "1\n1 2\n1\n3 4",       # no overlap
            "1\n1 2\n1\n2 3",       # they touch at a point
            "1\n1 5\n1\n2 3",       # one contains the other
            "1\n2 3\n1\n1 5",
            "2\n1 2\n5 6\n1\n0 10",
            "2\n1 3\n5 7\n2\n2 4\n6 8",
            "1\n0 0\n1\n0 0",
            "3\n1 2\n3 4\n5 6\n3\n2 3\n4 5\n6 7",
            "2\n1 10\n20 30\n2\n5 15\n25 35",
        ],
    },
{
        "title": "Partition Array into Disjoint Intervals",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "Cut the list into a left part and a right part so that every value on the left is no larger than every value on the right, and both parts hold at least one value. Return the length of the shortest possible left part.",
        "example_input": "5 0 3 8 6",
        "constraints": "Input format: one line of at least two space-separated integers; a valid cut always exists. Output format: a single integer.",
        "solve": _solve_partition_array_into_disjoint,
        "sample_inputs": ["5 0 3 8 6", "1 1 1 0 6 12"],
        "hidden_inputs": [
            "1 2",                  # the shortest possible cut
            "1 1",                  # equal values still cut
            "1 1 1",
            "1 2 3",
            "2 2 3 3",
            "1 0 2",                # the zero forces a longer left part
            "1 0 0 2",
            "0 1 2 3 4",
            "5 5 5 6",
            "1 3 2 4 5",
        ],
    },
{
        "title": "Shortest Unsorted Continuous Subarray",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "Return the length of the shortest stretch which, if sorted on its own, would leave the whole list in non-decreasing order.",
        "example_input": "2 6 4 8 10 9 15",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_shortest_unsorted_subarray,
        "sample_inputs": ["2 6 4 8 10 9 15", "1 2 3 4"],
        "hidden_inputs": [
            "1",                    # already sorted
            "1 1",
            "2 1",                  # the whole list
            "1 2",
            "1 3 2 4",
            "3 2 1",
            "1 1 1 1",
            "1 2 4 3 5",
            "5 4 3 2 1",
            "1 2 3 3 3",
        ],
    },
{
        "title": "Max Consecutive Ones III",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "Given a list of zeroes and ones, you may turn at most k zeroes into ones. Return the length of the longest run of ones obtainable.",
        "example_input": "1 1 1 0 0 0 1 1 1 1 0\n2",
        "constraints": "Input format: line 1 is the space-separated 0 and 1 values, line 2 is k. Output format: a single integer.",
        "solve": _solve_max_consecutive_ones_iii,
        "sample_inputs": ["1 1 1 0 0 0 1 1 1 1 0\n2", "0 0 1 1 0 0 1 1 1 0 1 1 0 0 0 1 1 1 1\n3"],
        "hidden_inputs": [
            "1\n0",                 # already a run of one
            "0\n0",                 # nothing can be flipped
            "0\n1",
            "1 1\n0",
            "0 0\n1",
            "0 0\n2",
            "1 0 1\n1",
            "1 0 1\n0",
            "0 0 0 0\n2",
            "1 1 1 1\n3",           # more budget than zeroes
        ],
    },
{
        "title": "Count Pairs With Sum Below Target",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "Count the pairs of different positions whose two values add up to strictly less than the target.",
        "example_input": "-1 1 2 3 1\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is the target. Output format: a single integer.",
        "solve": _solve_count_pairs_below_target,
        "sample_inputs": ["-1 1 2 3 1\n2", "-6 2 5 -2 -7 -1 3\n-2"],
        "hidden_inputs": [
            "1\n5",                 # a single value, no pair
            "1 1\n3",               # the only pair qualifies
            "1 1\n2",               # equal to the target does not count
            "1 1\n1",
            "0 0\n1",
            "-1 -2\n0",             # negatives
            "1 2 3\n4",
            "1 2 3\n100",           # every pair qualifies
            "1 2 3\n0",             # none does
            "5 5 5 5\n11",
        ],
    },
{
        "title": "Rearrange Array Elements by Sign",
        "topic": "two_pointers", "difficulty": "medium",
        "description": "The list holds equally many positive and negative values. Rearrange it so the signs alternate starting with a positive, keeping the original order within each sign.",
        "example_input": "3 1 -2 -5 2 -4",
        "constraints": "Input format: one line of space-separated non-zero integers, half positive and half negative. Output format: the rearranged values, space-separated.",
        "solve": _solve_rearrange_by_sign,
        "sample_inputs": ["3 1 -2 -5 2 -4", "-1 1"],
        "hidden_inputs": [
            "1 -1",                 # the smallest case
            "-7 7",
            "1 2 -1 -2",
            "-1 -2 1 2",
            "1 -1 2 -2",            # already alternating
            "-1 1 -2 2",
            "5 -5",
            "1 2 3 -1 -2 -3",
            "-3 -2 -1 3 2 1",
            "10 -10 20 -20",
        ],
    },
{
        "title": "Trapping Rain Water with Two Pointers",
        "topic": "two_pointers", "difficulty": "hard",
        "description": "Given bar heights each one unit wide, work out how much water is held between them after rain, walking inwards from both ends.",
        "example_input": "0 1 0 2 1 0 1 3 2 1 2 1",
        "constraints": "Input format: one line of space-separated non-negative heights. Output format: a single integer.",
        "solve": _solve_trapping_two_pointer,
        "sample_inputs": ["0 1 0 2 1 0 1 3 2 1 2 1", "4 2 0 3 2 5"],
        "hidden_inputs": [
            "0",                    # a single bar holds nothing
            "1 2",                  # two bars cannot hold
            "2 1 2",                # the smallest basin
            "3 0 3",
            "1 2 3 4 5",            # increasing, nothing held
            "5 4 3 2 1",            # decreasing
            "0 0 0",
            "5 1 5 1 5",
            "10 0 10",
            "1 0 1 0 1",
        ],
    },
{
        "title": "Minimum Absolute Difference Between Two Arrays",
        "topic": "two_pointers", "difficulty": "hard",
        "description": "Pick one value from each list and return the smallest difference between them, ignoring sign.",
        "example_input": "1 3 15 11 2\n23 127 235 19 8",
        "constraints": "Input format: line 1 and line 2 are the two space-separated lists, both non-empty. Output format: a single integer.",
        "solve": _solve_smallest_range_pair,
        "sample_inputs": ["1 3 15 11 2\n23 127 235 19 8", "1\n1"],
        "hidden_inputs": [
            "1\n2",                 # a difference of one
            "2\n1",
            "0\n0",                 # an exact match
            "5 5\n5 5",
            "1 2\n3 4",
            "1 100\n50 51",         # the closest pair is in the middle
            "-1 -2\n1 2",           # negatives
            "-5 5\n0",
            "1 3 5 7\n2 4 6 8",
            "10 20 30\n11 19 31",
        ],
    },
{
        "title": "Longest Word in Dictionary through Deleting",
        "topic": "two_pointers", "difficulty": "hard",
        "description": "Find the longest word in the list that can be made by deleting letters from the text without reordering the rest. When several are equally long, return the one that comes first alphabetically.",
        "example_input": "abpcplea\n4\nale\napple\nmonkey\nplea",
        "constraints": "Input format: line 1 is the text, line 2 is the number of words, followed by that many lowercase words. Output format: the word, or an empty line if none qualifies.",
        "solve": _solve_longest_word_in_dictionary,
        "sample_inputs": ["abpcplea\n4\nale\napple\nmonkey\nplea", "abpcplea\n2\na\nb"],
        "hidden_inputs": [
            "a\n1\na",              # an exact match
            "a\n1\nb",              # nothing qualifies
            "ab\n2\na\nb",          # a tie broken alphabetically
            "ab\n2\nb\na",          # the input order must not matter
            "ab\n1\nab",
            "ab\n1\nba",            # order matters, so nothing qualifies
            "abc\n3\nab\nac\nbc",
            "aaa\n2\naa\naaa",
            "bab\n2\nba\nab",
            "abpcplea\n3\napple\nplea\nale",
        ],
    },
{
        "title": "3Sum Smaller",
        "topic": "two_pointers", "difficulty": "hard",
        "description": "Count the triples of different positions whose three values add up to strictly less than the target.",
        "example_input": "-2 0 1 3\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is the target. Output format: a single integer.",
        "solve": _solve_three_sum_smaller,
        "sample_inputs": ["-2 0 1 3\n2", "0\n0"],
        "hidden_inputs": [
            "1 2\n10",              # fewer than three values
            "1 1 1\n4",             # the only triple qualifies
            "1 1 1\n3",             # equal to the target does not count
            "0 0 0\n1",
            "-1 -1 -1\n0",          # negatives
            "1 2 3\n7",
            "1 2 3\n6",
            "1 2 3 4\n8",
            "5 5 5 5\n100",         # every triple qualifies
            "5 5 5 5\n1",           # none does
        ],
    },
{
        "title": "Maximum Distance Between a Pair of Values",
        "topic": "two_pointers", "difficulty": "hard",
        "description": "Both lists are in non-increasing order. A pair of positions is valid when the first position is no later than the second and the value in the first list is no larger than the value in the second. Return the greatest gap between such positions, or zero if none is valid.",
        "example_input": "55 30 5 4 2\n100 20 10 10 5",
        "constraints": "Input format: line 1 and line 2 are the two lists in non-increasing order. Output format: a single integer.",
        "solve": _solve_max_distance_two_arrays,
        "sample_inputs": ["55 30 5 4 2\n100 20 10 10 5", "2 2 2\n10 10 1"],
        "hidden_inputs": [
            "1\n1",                 # equal values at the same position
            "2\n1",                 # no valid pair
            "1\n2",
            "2 1\n2 1",
            "5 4\n5 4",
            "5 4 3\n3 2 1",         # nothing further along qualifies
            "1 1 1\n1 1 1",
            "30 29 19 5\n25 25 25 25 25",
            "9 8 7\n10 9 8 7",
            "5 5 5 5\n5",
        ],
    },
{
        "title": "Minimize Maximum Pair Sum in Array",
        "topic": "two_pointers", "difficulty": "hard",
        "description": "Split the values into pairs so that every value is used exactly once. Arrange the pairs so that the largest total of any pair is as small as possible, and return that total.",
        "example_input": "3 5 2 3",
        "constraints": "Input format: one line of an even count of space-separated integers. Output format: a single integer.",
        "solve": _solve_minimum_size_pairs,
        "sample_inputs": ["3 5 2 3", "3 5 4 2 4 6"],
        "hidden_inputs": [
            "1 1",                  # one pair
            "1 2",
            "2 1",                  # order must not matter
            "0 0",
            "1 1 1 1",              # every pairing is identical
            "1 2 3 4",              # ends pair with ends
            "4 3 2 1",
            "-1 -2 -3 -4",          # negatives
            "1 1 100 100",
            "1 5 2 4 3 3",
        ],
    },
{
        "title": "Minimum Window Subsequence",
        "topic": "two_pointers", "difficulty": "hard",
        "description": "Find the shortest run of consecutive letters in the first string that contains the second string as a subsequence, meaning the second string's letters appear inside that run in the same order though not necessarily next to one another. If two runs are equally short, return the one that starts earliest.",
        "example_input": "abcdebdde\nbde",
        "constraints": "Input format: line 1 is the text and line 2 is the pattern, both non-empty strings of lowercase letters. Output format: the shortest qualifying run of letters, or -1 when no run contains the pattern.",
        "solve": _solve_minimum_window_subsequence,
        "sample_inputs": ["abcdebdde\nbde", "abc\nac"],
        "hidden_inputs": [
            "a\na",                  # text and pattern are one letter
            "a\nb",                  # no window at all
            "ab\nba",                # the letters are there but out of order
            "ba\nba",
            "aaa\naa",               # ties go to the earliest start
            "abcabc\ncb",            # the window straddles the repeat
            "abbaba\naba",
            "xyz\nxyz",              # the whole text is the only window
            "aaaaa\na",
            "abcdef\nafd",           # the last letter comes too early
        ],
    },
]
