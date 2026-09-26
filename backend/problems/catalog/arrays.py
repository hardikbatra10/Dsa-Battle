"""Array problems."""

def _solve_two_sum(lines):
    target = int(lines[0])
    nums = list(map(int, lines[1].split()))
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return f"{seen[target - n]} {i}"
        seen[n] = i
    return ""


def _solve_two_sum_ii(lines):
    n = int(lines[0])
    nums = list(map(int, lines[1].split()))
    target = int(lines[2])
    for i in range(n):
        for j in range(i + 1, n):
            if nums[i] + nums[j] == target:
                return f"{i} {j}"
    return ""


def _solve_valid_parentheses(lines):
    s = lines[0]
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != pairs[ch]:
                return "false"
    return "true" if not stack else "false"


def _solve_best_time_to_sell_stock(lines):
    prices = list(map(int, lines[0].split()))
    min_price = float("inf")
    max_profit = 0
    for p in prices:
        min_price = min(min_price, p)
        max_profit = max(max_profit, p - min_price)
    return str(max_profit)


def _solve_max_subarray(lines):
    nums = list(map(int, lines[0].split()))
    best = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        best = max(best, cur)
    return str(best)


def _solve_trapping_rain_water(lines):
    heights = list(map(int, lines[0].split()))
    if not heights:
        return "0"
    n = len(heights)
    left_max = [0] * n
    right_max = [0] * n
    left_max[0] = heights[0]
    for i in range(1, n):
        left_max[i] = max(left_max[i - 1], heights[i])
    right_max[n - 1] = heights[n - 1]
    for i in range(n - 2, -1, -1):
        right_max[i] = max(right_max[i + 1], heights[i])
    total = sum(min(left_max[i], right_max[i]) - heights[i] for i in range(n))
    return str(total)

def _solve_running_sum(lines):
    nums = list(map(int, lines[0].split()))
    out = []
    total = 0
    for v in nums:
        total += v
        out.append(str(total))
    return " ".join(out)


def _solve_majority_element(lines):
    nums = list(map(int, lines[0].split()))
    count = 0
    candidate = None
    for v in nums:
        if count == 0:
            candidate = v
        count += 1 if v == candidate else -1
    return str(candidate)


def _solve_contains_duplicate(lines):
    nums = lines[0].split()
    return "true" if len(set(nums)) != len(nums) else "false"


def _solve_find_pivot_index(lines):
    nums = list(map(int, lines[0].split()))
    total = sum(nums)
    left = 0
    for i, v in enumerate(nums):
        if left == total - left - v:
            return str(i)
        left += v
    return "-1"


def _solve_product_except_self(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    out = [1] * n
    prefix = 1
    for i in range(n):
        out[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix
        suffix *= nums[i]
    return " ".join(map(str, out))


def _solve_rotate_array(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1]) % len(nums)
    if k == 0:
        return " ".join(map(str, nums))
    return " ".join(map(str, nums[-k:] + nums[:-k]))


def _solve_find_all_duplicates(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = Counter(nums)
    return " ".join(str(v) for v in sorted(v for v, c in counts.items() if c == 2))


def _solve_subarray_sum_equals_k(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import defaultdict
    seen = defaultdict(int)
    seen[0] = 1
    total = 0
    count = 0
    for v in nums:
        total += v
        count += seen[total - k]
        seen[total] += 1
    return str(count)


def _solve_spiral_matrix(lines):
    m, n = map(int, lines[0].split())
    grid = [list(map(int, lines[1 + i].split())) for i in range(m)]
    out = []
    top, bottom, left, right = 0, m - 1, 0, n - 1
    while top <= bottom and left <= right:
        for j in range(left, right + 1):
            out.append(grid[top][j])
        top += 1
        for i in range(top, bottom + 1):
            out.append(grid[i][right])
        right -= 1
        if top <= bottom:
            for j in range(right, left - 1, -1):
                out.append(grid[bottom][j])
            bottom -= 1
        if left <= right:
            for i in range(bottom, top - 1, -1):
                out.append(grid[i][left])
            left += 1
    return " ".join(map(str, out))


def _solve_first_missing_positive(lines):
    nums = set(map(int, lines[0].split()))
    i = 1
    while i in nums:
        i += 1
    return str(i)


def _solve_longest_consecutive(lines):
    nums = set(map(int, lines[0].split()))
    best = 0
    for v in nums:
        if v - 1 not in nums:
            length = 1
            cur = v
            while cur + 1 in nums:
                cur += 1
                length += 1
            best = max(best, length)
    return str(best)

def _solve_smaller_than_current(lines):
    nums = list(map(int, lines[0].split()))
    return " ".join(str(sum(1 for y in nums if y < x)) for x in nums)


def _solve_richest_customer(lines):
    m, n = map(int, lines[0].split())
    return str(max(sum(map(int, lines[1 + i].split())) for i in range(m)))


def _solve_set_matrix_zeroes(lines):
    m, n = map(int, lines[0].split())
    grid = [list(map(int, lines[1 + i].split())) for i in range(m)]
    rows = {i for i in range(m) if 0 in grid[i]}
    cols = {j for j in range(n) if any(grid[i][j] == 0 for i in range(m))}
    out = []
    for i in range(m):
        out.append(" ".join(
            "0" if i in rows or j in cols else str(grid[i][j])
            for j in range(n)))
    return "\n".join(out)


def _solve_rotate_image(lines):
    n = int(lines[0].split()[0])
    grid = [list(map(int, lines[1 + i].split())) for i in range(n)]
    out = []
    for j in range(n):
        out.append(" ".join(str(grid[n - 1 - i][j]) for i in range(n)))
    return "\n".join(out)


def _solve_merge_intervals(lines):
    k = int(lines[0])
    ivs = sorted(tuple(map(int, lines[1 + i].split())) for i in range(k))
    out = []
    for s, e in ivs:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return "\n".join(f"{s} {e}" for s, e in out)


def _solve_insert_interval(lines):
    k = int(lines[0])
    ivs = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    ns, ne = map(int, lines[1 + k].split())
    out = []
    i = 0
    while i < k and ivs[i][1] < ns:
        out.append(list(ivs[i]))
        i += 1
    merged = [ns, ne]
    while i < k and ivs[i][0] <= merged[1]:
        merged[0] = min(merged[0], ivs[i][0])
        merged[1] = max(merged[1], ivs[i][1])
        i += 1
    out.append(merged)
    while i < k:
        out.append(list(ivs[i]))
        i += 1
    return "\n".join(f"{s} {e}" for s, e in out)


def _solve_find_duplicate_number(lines):
    nums = list(map(int, lines[0].split()))
    slow = fast = nums[0]
    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return str(slow)


def _solve_maximum_product_subarray(lines):
    nums = list(map(int, lines[0].split()))
    best = hi = lo = nums[0]
    for v in nums[1:]:
        candidates = (v, hi * v, lo * v)
        hi = max(candidates)
        lo = min(candidates)
        best = max(best, hi)
    return str(best)


def _solve_increasing_triplet(lines):
    nums = list(map(int, lines[0].split()))
    first = second = float("inf")
    for v in nums:
        if v <= first:
            first = v
        elif v <= second:
            second = v
        else:
            return "true"
    return "false"


def _solve_summary_ranges(lines):
    nums = list(map(int, lines[0].split()))
    out = []
    i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}")
        i = j + 1
    return " ".join(out)


def _solve_max_points_on_line(lines):
    k = int(lines[0])
    pts = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    if k <= 2:
        return str(k)
    best = 1
    for i in range(k):
        slopes = {}
        for j in range(k):
            if i == j:
                continue
            dx = pts[j][0] - pts[i][0]
            dy = pts[j][1] - pts[i][1]
            g = _gcd(abs(dx), abs(dy)) or 1
            dx //= g
            dy //= g
            if dx < 0 or (dx == 0 and dy < 0):
                dx, dy = -dx, -dy
            slopes[(dx, dy)] = slopes.get((dx, dy), 0) + 1
            best = max(best, slopes[(dx, dy)] + 1)
    return str(best)


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _solve_stock_iii(lines):
    prices = list(map(int, lines[0].split()))
    buy1 = buy2 = float("-inf")
    sell1 = sell2 = 0
    for p in prices:
        buy1 = max(buy1, -p)
        sell1 = max(sell1, buy1 + p)
        buy2 = max(buy2, sell1 - p)
        sell2 = max(sell2, buy2 + p)
    return str(sell2)


def _solve_stock_iv(lines):
    k = int(lines[0])
    prices = list(map(int, lines[1].split()))
    if k == 0 or not prices:
        return "0"
    k = min(k, len(prices) // 2) or 1
    buy = [float("-inf")] * (k + 1)
    sell = [0] * (k + 1)
    for p in prices:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - p)
            sell[t] = max(sell[t], buy[t] + p)
    return str(sell[k])


def _solve_count_smaller_after_self(lines):
    nums = list(map(int, lines[0].split()))
    out = []
    for i, v in enumerate(nums):
        out.append(str(sum(1 for w in nums[i + 1:] if w < v)))
    return " ".join(out)


def _solve_reverse_pairs(lines):
    nums = list(map(int, lines[0].split()))
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] > 2 * nums[j]:
                count += 1
    return str(count)


def _solve_russian_doll_envelopes(lines):
    k = int(lines[0])
    env = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    env.sort(key=lambda e: (e[0], -e[1]))
    import bisect
    tails = []
    for _, h in env:
        i = bisect.bisect_left(tails, h)
        if i == len(tails):
            tails.append(h)
        else:
            tails[i] = h
    return str(len(tails))


def _solve_maximum_gap(lines):
    nums = sorted(map(int, lines[0].split()))
    if len(nums) < 2:
        return "0"
    return str(max(nums[i + 1] - nums[i] for i in range(len(nums) - 1)))


PROBLEMS = [
{
        "title": "Two Sum",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given an integer target and an array of integers nums, return the 0-indexed positions of the two numbers that add up to target. Exactly one valid pair exists.",
        "example_input": "9\n2 7 11 15",
        "constraints": "Input format: line 1 is the target, line 2 is the space-separated array. Output format: the two 0-indexed positions, space-separated.",
        "solve": _solve_two_sum,
        "sample_inputs": ["9\n2 7 11 15", "13\n5 8 2"],
        "hidden_inputs": [
            "6\n3 3",                                         # the pair is two equal values
            "0\n0 0",                                         # zero target, zero values
            "3\n1 2 9 8",                                     # pair at the very start
            "7\n3 4",                                         # minimum array size
            "6\n3 2 4",
            "8\n4 1 2 7",                                     # 4+4 would hit target but 4 appears once - no reuse
            "10\n1 2 3 7",
            "-8\n-3 -5 1",                                    # negative target and values
            "1\n-1000000 2 1000001",
            "11\n1 4 5 8 7",                                  # pair buried in the middle
            "17\n8 1 2 3 4 5 9",                              # pair spans first and last index
            "2000000000\n1000000000 5 999999999 1000000000",  # 32-bit sized values
        ],
    },
{
        "title": "Two Sum II",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given an array of n integers and a target, find two numbers whose sum equals target and return their 0-indexed positions.",
        "example_input": "4\n2 7 11 15\n9",
        "constraints": "Input format: line 1 is n, line 2 is the space-separated array, line 3 is the target. Output format: the two 0-indexed positions, space-separated.",
        "solve": _solve_two_sum_ii,
        "sample_inputs": ["4\n2 7 11 15\n9", "3\n10 20 30\n50"],
        "hidden_inputs": [
            "2\n1 2\n3",           # minimum n
            "2\n-5 -5\n-10",       # both negative, equal values
            "3\n1 2 3\n5",
            "4\n0 0 5 7\n0",       # zero target, exactly one valid pair
            "5\n0 4 3 0 8\n0",
            "5\n-3 4 3 90 -1\n0",  # pair sums to zero via opposite signs
            "6\n1 2 3 4 5 6\n11",  # answer is the final pair
            "3\n1000000 999999 1\n1999999",
        ],
    },
{
        "title": "Valid Parentheses",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid: every open bracket must be closed by the same type of bracket, in the correct order.",
        "example_input": "()[]{}",
        "constraints": "Input format: one line containing the string. Output format: \"true\" or \"false\" (lowercase).",
        "solve": _solve_valid_parentheses,
        "sample_inputs": ["()[]{}", "([]{})"],
        "hidden_inputs": [
            "(",               # lone opener
            ")",               # lone closer
            "]",
            "(]",
            "([)]",
            "{[]}",
            "(()",             # unclosed opener remains on the stack
            "())",             # closer with an empty stack
            ")()(",            # balanced counts, wrong order
            "{[}]",
            "()()()",          # repeated siblings
            "([{}])",
            "((((((()))))))",  # deep nesting
        ],
    },
{
        "title": "Best Time to Buy and Sell Stock",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given an array of stock prices where prices[i] is the price on day i, return the maximum profit from buying on one day and selling on a later day. Return 0 if no profit is possible.",
        "example_input": "7 1 5 3 6 4",
        "constraints": "Input format: one line of space-separated prices. Output format: a single integer, the max profit.",
        "solve": _solve_best_time_to_sell_stock,
        "sample_inputs": ["7 1 5 3 6 4", "2 4 1"],
        "hidden_inputs": [
            "1",          # single day, no transaction possible
            "2 1",        # only a loss available
            "1 2",
            "5 5 5 5",    # flat prices
            "7 6 4 3 1",
            "1 2 3 4 5",  # monotonically rising
            "5 4 3 2 1",  # monotonically falling
            "2 4 1 7",
            "3 2 6 5 0 3",
            "2 1 4 9 0",  # global min is last and unusable
            "1 1000000000",
        ],
    },
{
        "title": "Maximum Subarray",
        "topic": "array",
        "difficulty": "medium",
        "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) with the largest sum, and return that sum.",
        "example_input": "-2 1 -3 4 -1 2 1 -5 4",
        "constraints": "Input format: one line of space-separated integers (may be negative). Output format: a single integer, the max subarray sum.",
        "solve": _solve_max_subarray,
        "sample_inputs": ["-2 1 -3 4 -1 2 1 -5 4", "1 2 3 -2 5"],
        "hidden_inputs": [
            "1",
            "-5",              # single negative element
            "0",
            "-1 -2 -3",
            "-3 -2 -5 -1 -4",  # all negative, answer is the least negative
            "0 0 0",
            "1 -1 1 -1 1",
            "2 -1 2 -1 2",
            "5 4 -1 7 8",
            "-1 5 -2 6 -10 4",
            "1000000 -1 1000000",
        ],
    },
{
        "title": "Trapping Rain Water",
        "topic": "array",
        "difficulty": "hard",
        "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "example_input": "0 1 0 2 1 0 1 3 2 1 2 1",
        "constraints": "Input format: one line of space-separated non-negative heights. Output format: a single integer, total trapped water.",
        "solve": _solve_trapping_rain_water,
        "sample_inputs": ["0 1 0 2 1 0 1 3 2 1 2 1", "3 0 2 0 4"],
        "hidden_inputs": [
            "0",          # single bar traps nothing
            "1 2",        # two bars cannot trap
            "0 0 0",
            "2 1 2",      # smallest real basin
            "3 0 3",
            "1 2 3 4 5",  # strictly increasing traps nothing
            "5 4 3 2 1",  # strictly decreasing traps nothing
            "1 0 1 0 1",
            "5 1 5 1 5",
            "10 0 10",
            "4 2 0 3 2 5",
        ],
    },
{
        "title": "Running Sum of 1d Array",
        "topic": "array",
        "difficulty": "easy",
        "description": "Return a list in which each position holds the total of every value up to and including that position.",
        "example_input": "1 2 3 4",
        "constraints": "Input format: one line of space-separated integers. Output format: the running totals, space-separated.",
        "solve": _solve_running_sum,
        "sample_inputs": ["1 2 3 4", "1 1 1 1 1"],
        "hidden_inputs": [
            "5",                    # a single value
            "0",
            "-5",                   # a negative value
            "1 -1",                 # the total returns to zero
            "0 0 0",
            "-1 -2 -3",             # totals fall away
            "3 1 2 10 1",
            "1 2 3 4 5 6 7 8 9 10",
            "100 -50 25 -12",
            "1000000 1000000 1000000",
        ],
    },
{
        "title": "Majority Element",
        "topic": "array",
        "difficulty": "easy",
        "description": "One value appears more than half the time in the list. Return that value.",
        "example_input": "3 2 3",
        "constraints": "Input format: one line of space-separated integers, where one value is guaranteed to occupy more than half the positions. Output format: a single integer.",
        "solve": _solve_majority_element,
        "sample_inputs": ["3 2 3", "2 2 1 1 1 2 2"],
        "hidden_inputs": [
            "1",                    # a single value is its own majority
            "1 1",
            "1 1 2",                # just over half
            "2 1 1",                # the majority is not at the front
            "1 2 1",                # nor contiguous
            "0 0 0",
            "-1 -1 -1 2 3",         # a negative majority
            "5 5 5 5 5",
            "6 5 5",
            "1 1 1 1 2 2 3",
        ],
    },
{
        "title": "Contains Duplicate",
        "topic": "array",
        "difficulty": "easy",
        "description": "Decide whether any value appears more than once in the list.",
        "example_input": "1 2 3 1",
        "constraints": "Input format: one line of space-separated integers. Output format: \"true\" or \"false\".",
        "solve": _solve_contains_duplicate,
        "sample_inputs": ["1 2 3 1", "1 2 3 4"],
        "hidden_inputs": [
            "1",                    # nothing can repeat
            "1 1",                  # the smallest repeat
            "1 2",
            "0 0",
            "-1 -1",                # negatives repeat too
            "-1 1",
            "1 2 3 4 5",
            "1 2 3 4 1",            # the repeat spans the whole list
            "5 5 5 5",
            "1 1 2 3 3 4 4 4",
        ],
    },
{
        "title": "Find Pivot Index",
        "topic": "array",
        "difficulty": "easy",
        "description": "Find the leftmost position where everything strictly to its left adds up to the same total as everything strictly to its right. Return that position, or -1 if there is none.",
        "example_input": "1 7 3 6 5 6",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_find_pivot_index,
        "sample_inputs": ["1 7 3 6 5 6", "1 2 3"],
        "hidden_inputs": [
            "0",                    # both sides are empty, so index 0
            "5",                    # a single value still pivots
            "0 0",                  # the leftmost of two valid answers
            "1 0",
            "0 1",
            "2 1 -1",               # the pivot sits at the end
            "-1 -1 -1 0 1 1",
            "1 2 3 4 5",            # no pivot exists
            "1 1 1 1",
            "-1 -1 0 1 1",
        ],
    },
{
        "title": "Product of Array Except Self",
        "topic": "array",
        "difficulty": "medium",
        "description": "For each position, return the product of every other value in the list, without performing any division.",
        "example_input": "1 2 3 4",
        "constraints": "Input format: one line of space-separated integers. Output format: the products, space-separated.",
        "solve": _solve_product_except_self,
        "sample_inputs": ["1 2 3 4", "-1 1 0 -3 3"],
        "hidden_inputs": [
            "5",                    # one value, an empty product of 1
            "2 3",                  # each is the other
            "0 0",                  # two zeroes make everything zero
            "0 5",                  # a single zero
            "1 1 1",
            "-1 -2 -3",             # sign handling
            "1 0 3",
            "2 2 2 2",
            "1 2 3 4 5 6",
            "10 -10 1 -1",
        ],
    },
{
        "title": "Rotate Array",
        "topic": "array",
        "difficulty": "medium",
        "description": "Shift every value k places towards the end, wrapping the ones that fall off back round to the front.",
        "example_input": "1 2 3 4 5 6 7\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k (k >= 0). Output format: the rotated values, space-separated.",
        "solve": _solve_rotate_array,
        "sample_inputs": ["1 2 3 4 5 6 7\n3", "-1 -100 3 99\n2"],
        "hidden_inputs": [
            "1\n0",                 # nothing to do
            "1\n5",                 # a single value rotates onto itself
            "1 2\n1",
            "1 2\n2",               # a full turn restores the order
            "1 2 3\n3",             # k equal to the length
            "1 2 3\n4",             # k just past the length
            "1 2 3\n100",           # k far beyond the length
            "1 2 3 4\n2",           # exactly half
            "5 5 5\n1",             # duplicate values
            "1 2 3 4 5\n4",
        ],
    },
{
        "title": "Find All Duplicates in an Array",
        "topic": "array",
        "difficulty": "medium",
        "description": "The list holds values between one and its own length, each appearing either once or twice. Return the values that appear twice, in increasing order.",
        "example_input": "4 3 2 7 8 2 3 1",
        "constraints": "Input format: one line of space-separated integers between 1 and the list's length. Output format: the repeated values ascending, space-separated (empty if none).",
        "solve": _solve_find_all_duplicates,
        "sample_inputs": ["4 3 2 7 8 2 3 1", "1 1 2"],
        "hidden_inputs": [
            "1",                    # nothing can repeat
            "1 2",                  # no repeats
            "2 2",                  # both positions hold the same value
            "1 2 3",
            "2 1 2",                # the repeat is not adjacent
            "1 1 2 2",              # two separate repeats
            "3 1 3",                # the repeat is the largest allowed value
            "4 4 3 3 2 2 1 1",      # every value repeats
            "1 2 3 4 5 6",
            "5 4 6 7 9 3 10 9 5 6",
        ],
    },
{
        "title": "Subarray Sum Equals K",
        "topic": "array",
        "difficulty": "medium",
        "description": "Count the runs of consecutive values that add up to exactly k. Values may be negative.",
        "example_input": "1 1 1\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: a single integer.",
        "solve": _solve_subarray_sum_equals_k,
        "sample_inputs": ["1 1 1\n2", "1 2 3\n3"],
        "hidden_inputs": [
            "1\n1",                 # the single value matches
            "1\n2",                 # no run matches
            "0\n0",                 # a zero-valued run
            "0 0\n0",               # three separate runs sum to zero
            "1 -1\n0",              # positives and negatives cancel
            "-1 -1 1\n0",
            "1 2 3\n6",             # the whole list
            "3 4 7 2 -3 1 4 2\n7",
            "1 1 1 1 1\n3",
            "-1 -1 -1\n-2",         # negative target
        ],
    },
{
        "title": "Spiral Matrix",
        "topic": "array",
        "difficulty": "medium",
        "description": "Read every value of a grid in a spiral: along the top row, down the right side, back along the bottom, up the left side, then inwards and round again.",
        "example_input": "3 3\n1 2 3\n4 5 6\n7 8 9",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of integers. Output format: the values in spiral order, space-separated.",
        "solve": _solve_spiral_matrix,
        "sample_inputs": ["3 3\n1 2 3\n4 5 6\n7 8 9", "3 4\n1 2 3 4\n5 6 7 8\n9 10 11 12"],
        "hidden_inputs": [
            "1 1\n7",               # a single cell
            "1 4\n1 2 3 4",         # a single row, no turn
            "4 1\n1\n2\n3\n4",      # a single column
            "2 2\n1 2\n3 4",
            "2 3\n1 2 3\n4 5 6",
            "3 2\n1 2\n3 4\n5 6",
            "4 4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16",
            "5 1\n1\n2\n3\n4\n5",
            "2 4\n1 2 3 4\n5 6 7 8",
            "3 3\n-1 -2 -3\n-4 -5 -6\n-7 -8 -9",
        ],
    },
{
        "title": "First Missing Positive",
        "topic": "array",
        "difficulty": "hard",
        "description": "Return the smallest whole number greater than zero that does not appear in the list.",
        "example_input": "3 4 -1 1",
        "constraints": "Input format: one line of space-separated integers, which may be negative or repeated. Output format: a single integer.",
        "solve": _solve_first_missing_positive,
        "sample_inputs": ["3 4 -1 1", "7 8 9 11 12"],
        "hidden_inputs": [
            "1",                    # one is present, so two is missing
            "2",                    # one is missing outright
            "0",                    # zero does not count
            "-1",                   # negatives do not count
            "1 2",                  # the answer is just past the end
            "2 1",                  # order must not matter
            "1 1",                  # a repeat does not fill the gap
            "1 2 3 4 5",
            "-1 -2 -3",
            "1 2 0 4 5",            # the gap sits in the middle
        ],
    },
{
        "title": "Longest Consecutive Sequence",
        "topic": "array",
        "difficulty": "hard",
        "description": "Return the length of the longest run of whole numbers that follow one another, ignoring the order they appear in and counting repeats only once.",
        "example_input": "100 4 200 1 3 2",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_longest_consecutive,
        "sample_inputs": ["100 4 200 1 3 2", "0 3 7 2 5 8 4 6 0 1"],
        "hidden_inputs": [
            "1",                    # a run of one
            "1 1",                  # repeats collapse
            "1 2",
            "2 1",                  # order must not matter
            "1 3",                  # a gap breaks the run
            "5 5 5 5",
            "-1 0 1",               # a run crossing zero
            "-3 -2 -1",             # entirely negative
            "1 2 3 10 11 12 13",    # the longer run comes second
            "9 1 4 7 3 2 6 5 8",
        ],
    },
{
        "title": "How Many Numbers Are Smaller Than the Current Number",
        "topic": "array", "difficulty": "easy",
        "description": "For each value, count how many other values in the list are strictly smaller than it.",
        "example_input": "8 1 2 2 3",
        "constraints": "Input format: one line of space-separated integers. Output format: one count per value, space-separated.",
        "solve": _solve_smaller_than_current,
        "sample_inputs": ["8 1 2 2 3", "6 5 4 8"],
        "hidden_inputs": [
            "1",                    # nothing is smaller
            "1 1",                  # equal values do not count
            "1 2",
            "2 1",
            "5 5 5 5",
            "1 2 3 4",
            "4 3 2 1",
            "-1 -2 -3",             # negatives
            "0 0 1",
            "7 7 7 7 7 7 7 7",
        ],
    },
{
        "title": "Richest Customer Wealth",
        "topic": "array", "difficulty": "easy",
        "description": "Each row records one customer's holdings across several accounts. Return the largest total held by any single customer.",
        "example_input": "2 3\n1 2 3\n3 2 1",
        "constraints": "Input format: line 1 is \"customers accounts\", followed by that many lines of non-negative amounts. Output format: a single integer.",
        "solve": _solve_richest_customer,
        "sample_inputs": ["2 3\n1 2 3\n3 2 1", "3 2\n1 5\n7 3\n3 5"],
        "hidden_inputs": [
            "1 1\n0",               # a single empty account
            "1 1\n5",
            "1 3\n1 2 3",           # one customer
            "3 1\n1\n2\n3",         # one account each
            "2 2\n0 0\n0 0",
            "2 2\n1 1\n1 1",        # a tie
            "2 3\n1 1 1\n2 2 2",
            "3 3\n2 8 7\n7 1 3\n1 9 5",
            "2 4\n1 2 3 4\n4 3 2 1",
            "4 2\n9 0\n0 9\n5 5\n1 1",
        ],
    },
{
        "title": "Set Matrix Zeroes",
        "topic": "array", "difficulty": "medium",
        "description": "Wherever the grid holds a zero, set every value in that row and that column to zero, and return the result.",
        "example_input": "3 3\n1 1 1\n1 0 1\n1 1 1",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of integers. Output format: the resulting grid in the same layout.",
        "solve": _solve_set_matrix_zeroes,
        "sample_inputs": ["3 3\n1 1 1\n1 0 1\n1 1 1", "3 4\n0 1 2 0\n3 4 5 2\n1 3 1 5"],
        "hidden_inputs": [
            "1 1\n1",               # nothing to clear
            "1 1\n0",
            "1 3\n1 0 1",           # a single row
            "3 1\n1\n0\n1",         # a single column
            "2 2\n1 1\n1 1",
            "2 2\n0 1\n1 1",
            "2 2\n0 0\n0 0",
            "2 3\n1 2 3\n4 0 6",
            "3 3\n0 1 1\n1 1 1\n1 1 0",     # two zeroes clear most of it
            "3 3\n1 2 3\n4 5 6\n7 8 9",
        ],
    },
{
        "title": "Rotate Image",
        "topic": "array", "difficulty": "medium",
        "description": "Turn a square grid a quarter turn clockwise and return the result.",
        "example_input": "3 3\n1 2 3\n4 5 6\n7 8 9",
        "constraints": "Input format: line 1 is \"n n\", followed by n lines of n integers. Output format: the rotated grid in the same layout.",
        "solve": _solve_rotate_image,
        "sample_inputs": ["3 3\n1 2 3\n4 5 6\n7 8 9", "2 2\n1 2\n3 4"],
        "hidden_inputs": [
            "1 1\n1",               # a single cell is unchanged
            "1 1\n0",
            "2 2\n1 1\n1 1",        # symmetric, the turn is invisible
            "2 2\n1 2\n2 1",
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 3\n1 0 0\n0 0 0\n0 0 0",     # a corner travels
            "3 3\n-1 -2 -3\n-4 -5 -6\n-7 -8 -9",
            "4 4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16",
            "4 4\n5 1 9 11\n2 4 8 10\n13 3 6 7\n15 14 12 16",
            "3 3\n0 0 1\n0 0 0\n0 0 0",
        ],
    },
{
        "title": "Merge Intervals",
        "topic": "array", "difficulty": "medium",
        "description": "Combine every group of overlapping or touching ranges into a single range, and list the results in increasing order.",
        "example_input": "4\n1 3\n2 6\n8 10\n15 18",
        "constraints": "Input format: line 1 is the number of ranges, followed by that many lines each \"start end\". Output format: one range per line as \"start end\".",
        "solve": _solve_merge_intervals,
        "sample_inputs": ["4\n1 3\n2 6\n8 10\n15 18", "2\n1 4\n4 5"],
        "hidden_inputs": [
            "1\n1 2",               # nothing to merge
            "2\n1 2\n3 4",          # disjoint, kept apart
            "2\n1 2\n2 3",          # touching, merged
            "2\n1 5\n2 3",          # one contains the other
            "2\n3 4\n1 2",          # given out of order
            "3\n1 4\n0 4\n3 5",
            "3\n1 2\n1 2\n1 2",     # identical ranges
            "4\n1 10\n2 3\n4 5\n6 7",
            "4\n5 6\n3 4\n1 2\n7 8",
            "5\n1 3\n2 4\n3 5\n6 8\n7 9",
        ],
    },
{
        "title": "Insert Interval",
        "topic": "array", "difficulty": "medium",
        "description": "Given ranges already sorted and not overlapping, add one more range and combine anything that now overlaps. Return the result in increasing order.",
        "example_input": "2\n1 3\n6 9\n2 5",
        "constraints": "Input format: line 1 is the number of existing ranges, followed by that many lines each \"start end\" in increasing order, then a final line holding the new range. Output format: one range per line as \"start end\".",
        "solve": _solve_insert_interval,
        "sample_inputs": ["2\n1 3\n6 9\n2 5", "5\n1 2\n3 5\n6 7\n8 10\n12 16\n4 8"],
        "hidden_inputs": [
            "0\n1 2",               # the new range is the only one
            "1\n1 2\n3 4",          # added after
            "1\n3 4\n1 2",          # added before
            "1\n1 5\n2 3",          # swallowed by an existing range
            "1\n2 3\n1 5",          # swallows an existing range
            "1\n1 2\n2 3",          # touching, merged
            "2\n1 2\n5 6\n3 4",     # slotted into the gap
            "3\n1 2\n4 5\n7 8\n3 6",
            "3\n1 2\n3 4\n5 6\n0 7", # swallows everything
            "2\n1 3\n6 9\n10 12",
        ],
    },
{
        "title": "Find the Duplicate Number",
        "topic": "array", "difficulty": "medium",
        "description": "A list of n plus one values, each between one and n, holds exactly one value more than once. Return that value.",
        "example_input": "1 3 4 2 2",
        "constraints": "Input format: one line of space-separated integers between 1 and one less than the count, with exactly one repeated. Output format: a single integer.",
        "solve": _solve_find_duplicate_number,
        "sample_inputs": ["1 3 4 2 2", "3 1 3 4 2"],
        "hidden_inputs": [
            "1 1",                  # the smallest possible case
            "1 1 1",                # the same value three times
            "2 2 2 2",
            "1 2 2",
            "2 1 2",                # the repeat is not adjacent
            "2 2 1",
            "1 3 2 3",
            "3 3 3 3 3",
            "1 2 3 4 4",
            "4 3 1 4 2",
        ],
    },
{
        "title": "Maximum Product Subarray",
        "topic": "array", "difficulty": "medium",
        "description": "Return the largest product obtainable from any run of consecutive values.",
        "example_input": "2 3 -2 4",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_maximum_product_subarray,
        "sample_inputs": ["2 3 -2 4", "-2 0 -1"],
        "hidden_inputs": [
            "2",                    # a single value
            "-2",                   # a single negative value
            "0",
            "-2 -3",                # two negatives multiply to a positive
            "-2 3",
            "0 2",                  # a zero resets the run
            "-1 -2 -3",             # an odd count of negatives
            "-1 -2 -3 -4",          # an even count
            "2 -5 -2 -4 3",
            "0 -3 1 -2 0 4",
        ],
    },
{
        "title": "Increasing Triplet Subsequence",
        "topic": "array", "difficulty": "medium",
        "description": "Decide whether three positions exist, in order, whose values strictly increase.",
        "example_input": "1 2 3 4 5",
        "constraints": "Input format: one line of space-separated integers. Output format: \"true\" or \"false\".",
        "solve": _solve_increasing_triplet,
        "sample_inputs": ["1 2 3 4 5", "5 4 3 2 1"],
        "hidden_inputs": [
            "1",                    # too short
            "1 2",
            "1 2 3",                # exactly enough
            "3 2 1",
            "1 1 1",                # equal values do not increase
            "1 1 2 2 3",
            "2 1 5 0 4 6",          # the triplet is not contiguous
            "5 1 5 5 2 5 4",
            "20 100 10 12 5 13",
            "-5 -4 -3",             # negatives
        ],
    },
{
        "title": "Summary Ranges",
        "topic": "array", "difficulty": "medium",
        "description": "Given values in increasing order with no repeats, gather every run of consecutive whole numbers into a single entry written as first arrow last, leaving lone values as they are.",
        "example_input": "0 1 2 4 5 7",
        "constraints": "Input format: one line of space-separated increasing distinct integers. Output format: the entries space-separated, each a single value or \"first->last\".",
        "solve": _solve_summary_ranges,
        "sample_inputs": ["0 1 2 4 5 7", "0 2 3 4 6 8 9"],
        "hidden_inputs": [
            "0",                    # a lone value
            "-1",
            "0 1",                  # the shortest run
            "0 2",                  # not consecutive
            "0 1 2",
            "1 3 5 7",              # no runs at all
            "1 2 3 4 5",            # one run covering everything
            "-3 -2 -1 1 2",         # a run crossing zero
            "-5 -4 0 1 2 9",
            "0 1 2 3 5 6 8",
        ],
    },
{
        "title": "Max Points on a Line",
        "topic": "array", "difficulty": "hard",
        "description": "Return the largest number of the given points that lie on a single straight line.",
        "example_input": "3\n1 1\n2 2\n3 3",
        "constraints": "Input format: line 1 is the number of points, followed by that many lines each \"x y\", all points distinct. Output format: a single integer.",
        "solve": _solve_max_points_on_line,
        "sample_inputs": ["3\n1 1\n2 2\n3 3", "6\n1 1\n3 2\n5 3\n4 1\n2 3\n1 4"],
        "hidden_inputs": [
            "1\n0 0",               # a single point
            "2\n0 0\n1 1",          # two points always share a line
            "3\n0 0\n1 1\n2 3",     # only two are collinear
            "3\n0 0\n0 1\n0 2",     # a vertical line
            "3\n0 0\n1 0\n2 0",     # a horizontal line
            "4\n0 0\n1 1\n2 2\n3 3",
            "4\n0 0\n1 1\n0 1\n1 0",
            "5\n0 0\n1 1\n2 2\n3 4\n4 5",
            "4\n-1 -1\n0 0\n1 1\n2 2",      # negatives
            "5\n1 1\n2 2\n3 3\n1 2\n2 4",
        ],
    },
{
        "title": "Best Time to Buy and Sell Stock III",
        "topic": "array", "difficulty": "hard",
        "description": "You may complete at most two buy-and-sell pairs, and must sell before buying again. Return the largest total profit.",
        "example_input": "3 3 5 0 0 3 1 4",
        "constraints": "Input format: one line of space-separated prices. Output format: a single integer.",
        "solve": _solve_stock_iii,
        "sample_inputs": ["3 3 5 0 0 3 1 4", "1 2 3 4 5"],
        "hidden_inputs": [
            "1",                    # no trade possible
            "2 1",                  # only a loss
            "1 2",                  # one trade
            "7 6 4 3 1",            # falling every day
            "1 2 3 4 5 6",          # one trade captures everything
            "1 5 1 5",              # two trades beat one
            "5 1 5 1 5",
            "1 2 4 2 5 7 2 4 9 0",
            "0 0 0 0",
            "6 1 3 2 4 7",
        ],
    },
{
        "title": "Best Time to Buy and Sell Stock IV",
        "topic": "array", "difficulty": "hard",
        "description": "You may complete at most k buy-and-sell pairs, and must sell before buying again. Return the largest total profit.",
        "example_input": "2\n2 4 1",
        "constraints": "Input format: line 1 is k (k >= 0), line 2 is the space-separated prices. Output format: a single integer.",
        "solve": _solve_stock_iv,
        "sample_inputs": ["2\n2 4 1", "2\n3 2 6 5 0 3"],
        "hidden_inputs": [
            "0\n1 2 3",             # no trades allowed
            "1\n1",                 # a single day
            "1\n1 2",
            "1\n2 1",
            "1\n1 5 1 5",           # only one trade allowed
            "2\n1 5 1 5",           # both trades taken
            "5\n1 5 1 5",           # more trades allowed than useful
            "100\n1 2 3 4 5",
            "2\n5 4 3 2 1",         # nothing to gain
            "3\n1 2 4 2 5 7 2 4 9 0",
        ],
    },
{
        "title": "Count of Smaller Numbers After Self",
        "topic": "array", "difficulty": "hard",
        "description": "For each position, count how many values to its right are strictly smaller than it.",
        "example_input": "5 2 6 1",
        "constraints": "Input format: one line of space-separated integers. Output format: one count per position, space-separated.",
        "solve": _solve_count_smaller_after_self,
        "sample_inputs": ["5 2 6 1", "-1 -1"],
        "hidden_inputs": [
            "1",                    # nothing to the right
            "1 2",                  # nothing smaller follows
            "2 1",
            "1 1",                  # equal values do not count
            "3 3 3",
            "1 2 3 4",
            "4 3 2 1",              # every value dominates the rest
            "-1 0 1",               # negatives
            "5 5 1 5 1",
            "2 0 1",
        ],
    },
{
        "title": "Reverse Pairs",
        "topic": "array", "difficulty": "hard",
        "description": "Count the pairs of positions, the first before the second, where the earlier value is more than twice the later one.",
        "example_input": "1 3 2 3 1",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_reverse_pairs,
        "sample_inputs": ["1 3 2 3 1", "2 4 3 5 1"],
        "hidden_inputs": [
            "1",                    # no pair exists
            "1 1",
            "3 1",                  # exactly one pair
            "2 1",                  # twice is not more than twice
            "1 3",
            "0 0",                  # zeroes
            "-1 -1",
            "5 4 3 2 1",
            "1 2 3 4 5",
            "-5 -3 -1 0 1",         # negatives
        ],
    },
{
        "title": "Russian Doll Envelopes",
        "topic": "array", "difficulty": "hard",
        "description": "One envelope fits inside another only when both its width and its height are strictly smaller. Return the largest number that can be nested one inside the next.",
        "example_input": "4\n5 4\n6 4\n6 7\n2 3",
        "constraints": "Input format: line 1 is the number of envelopes, followed by that many lines each \"width height\". Output format: a single integer.",
        "solve": _solve_russian_doll_envelopes,
        "sample_inputs": ["4\n5 4\n6 4\n6 7\n2 3", "3\n1 1\n1 1\n1 1"],
        "hidden_inputs": [
            "1\n1 1",               # a single envelope
            "2\n1 1\n2 2",          # one fits inside the other
            "2\n1 2\n2 1",          # neither fits
            "2\n1 1\n1 2",          # equal widths never nest
            "2\n1 1\n2 1",          # equal heights never nest
            "3\n1 1\n2 2\n3 3",
            "3\n3 3\n2 2\n1 1",     # given in reverse
            "4\n1 1\n2 2\n2 3\n3 4",
            "5\n4 5\n4 6\n6 7\n2 3\n1 1",
            "4\n2 100\n3 200\n4 300\n5 500",
        ],
    },
{
        "title": "Maximum Gap",
        "topic": "array", "difficulty": "hard",
        "description": "Sort the values in increasing order and return the largest difference between two neighbouring values, or zero if there are fewer than two values.",
        "example_input": "3 6 9 1",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: a single integer.",
        "solve": _solve_maximum_gap,
        "sample_inputs": ["3 6 9 1", "10"],
        "hidden_inputs": [
            "0",                    # a single value, gap of zero
            "1 1",                  # equal values
            "1 2",                  # the smallest real gap
            "1 100",
            "1 1 1 1",
            "1 2 3 4 5",            # every gap identical
            "1 10 100 1000",        # the gaps grow
            "0 0 0 1",
            "5 4 3 2 1",            # given in reverse
            "1 3 100 4 2",
        ],
    },
]
