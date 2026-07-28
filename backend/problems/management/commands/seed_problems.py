"""
Seeds/repairs the Problem + TestCase catalog so every topic x difficulty
combination has at least one usable problem, and every problem has both
sample (is_sample=True) and hidden (is_sample=False) test cases.

Expected outputs are never typed in by hand: each problem defines a small
Python reference solution, and this command actually executes it against
each raw input to compute the correct expected_output. That's the only way
to be confident the seeded test data is right.

Safe to re-run: existing problems are matched by title and only the fields
this command owns are updated; test cases for a problem are fully replaced
each run so there's never stale/duplicate data.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from problems.models import Problem, TestCase
from users.models import User


# ---------------------------------------------------------------------------
# Small binary tree helper shared by the tree problems below. Trees are
# encoded on stdin as one line of space-separated level-order values, with
# "null" marking a missing child (e.g. "1 null 2 3").
# ---------------------------------------------------------------------------
class _Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def _build_tree(tokens):
    if not tokens or tokens[0] == "null":
        return None
    root = _Node(int(tokens[0]))
    queue = [root]
    i = 1
    while queue and i < len(tokens):
        node = queue.pop(0)
        if i < len(tokens):
            if tokens[i] != "null":
                node.left = _Node(int(tokens[i]))
                queue.append(node.left)
            i += 1
        if i < len(tokens):
            if tokens[i] != "null":
                node.right = _Node(int(tokens[i]))
                queue.append(node.right)
            i += 1
    return root


# ---------------------------------------------------------------------------
# Small singly-linked-list helper shared by the linked-list problems below.
# Lists are encoded on stdin as one line of space-separated values.
# ---------------------------------------------------------------------------
class _LNode:
    def __init__(self, val):
        self.val = val
        self.next = None


def _build_linked_list(tokens):
    head = None
    tail = None
    for t in tokens:
        node = _LNode(int(t))
        if head is None:
            head = node
            tail = node
        else:
            tail.next = node
            tail = node
    return head


def _linked_list_to_str(head):
    vals = []
    while head:
        vals.append(str(head.val))
        head = head.next
    return " ".join(vals)


# ---------------------------------------------------------------------------
# Reference solutions. Each takes the raw stdin split into lines and returns
# the exact expected stdout string.
# ---------------------------------------------------------------------------
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


def _solve_binary_tree_inorder(lines):
    root = _build_tree(lines[0].split())
    out = []

    def inorder(node):
        if not node:
            return
        inorder(node.left)
        out.append(str(node.val))
        inorder(node.right)

    inorder(root)
    return " ".join(out)


def _solve_max_depth(lines):
    root = _build_tree(lines[0].split())

    def depth(node):
        if not node:
            return 0
        return 1 + max(depth(node.left), depth(node.right))

    return str(depth(root))


def _solve_diameter(lines):
    root = _build_tree(lines[0].split())
    best = [0]

    def depth(node):
        if not node:
            return 0
        l = depth(node.left)
        r = depth(node.right)
        best[0] = max(best[0], l + r)
        return 1 + max(l, r)

    depth(root)
    return str(best[0])


def _solve_number_of_islands(lines):
    rows, cols = map(int, lines[0].split())
    grid = [list(map(int, lines[1 + i].split())) for i in range(rows)]
    visited = [[False] * cols for _ in range(rows)]
    count = 0

    def dfs(r, c):
        stack = [(r, c)]
        visited[r][c] = True
        while stack:
            cr, cc = stack.pop()
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = cr + dr, cc + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and not visited[nr][nc]
                    and grid[nr][nc] == 1
                ):
                    visited[nr][nc] = True
                    stack.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                count += 1
                dfs(r, c)
    return str(count)


def _solve_find_path_exists(lines):
    n, m, src, dst = map(int, lines[0].split())
    adj = [[] for _ in range(n)]
    for i in range(m):
        u, v = map(int, lines[1 + i].split())
        adj[u].append(v)
        adj[v].append(u)
    visited = [False] * n
    stack = [src]
    visited[src] = True
    while stack:
        node = stack.pop()
        if node == dst:
            return "true"
        for nb in adj[node]:
            if not visited[nb]:
                visited[nb] = True
                stack.append(nb)
    return "true" if src == dst else "false"


def _solve_course_schedule(lines):
    n, m = map(int, lines[0].split())
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        adj[b].append(a)
        indeg[a] += 1
    queue = [i for i in range(n) if indeg[i] == 0]
    visited_count = 0
    while queue:
        node = queue.pop()
        visited_count += 1
        for nb in adj[node]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                queue.append(nb)
    return "true" if visited_count == n else "false"


def _solve_lis(lines):
    nums = list(map(int, lines[0].split()))
    if not nums:
        return "0"
    tails = []
    for n in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < n:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(n)
        else:
            tails[lo] = n
    return str(len(tails))


def _solve_climbing_stairs(lines):
    n = int(lines[0])
    if n <= 2:
        return str(max(n, 1))
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return str(b)


def _solve_coin_change(lines):
    coins = list(map(int, lines[0].split()))
    amount = int(lines[1])
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return str(dp[amount] if dp[amount] != INF else -1)


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


def _solve_reverse_linked_list(lines):
    head = _build_linked_list(lines[0].split())
    prev = None
    while head:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return _linked_list_to_str(prev)


def _solve_merge_two_lists(lines):
    a = _build_linked_list(lines[0].split())
    b = _build_linked_list(lines[1].split())
    dummy = _LNode(0)
    tail = dummy
    while a and b:
        if a.val <= b.val:
            tail.next = a
            a = a.next
        else:
            tail.next = b
            b = b.next
        tail = tail.next
    tail.next = a or b
    return _linked_list_to_str(dummy.next)


def _solve_linked_list_cycle(lines):
    vals = list(map(int, lines[0].split()))
    pos = int(lines[1])
    nodes = [_LNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos != -1 and nodes:
        nodes[-1].next = nodes[pos]
    if not nodes:
        return "false"
    slow = fast = nodes[0]
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return "true"
    return "false"


def _solve_next_greater_element(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] < nums[i]:
            res[stack.pop()] = nums[i]
        stack.append(i)
    return " ".join(map(str, res))


def _solve_min_stack(lines):
    q = int(lines[0])
    stack = []
    mins = []
    outputs = []
    for i in range(1, q + 1):
        parts = lines[i].split()
        if parts[0] == "push":
            v = int(parts[1])
            stack.append(v)
            mins.append(v if not mins else min(v, mins[-1]))
        elif parts[0] == "pop":
            stack.pop()
            mins.pop()
        elif parts[0] == "getMin":
            outputs.append(str(mins[-1]))
    return " ".join(outputs)


def _solve_largest_rectangle(lines):
    heights = list(map(int, lines[0].split()))
    stack = []
    max_area = 0
    extended = heights + [0]
    for i, h in enumerate(extended):
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)
    return str(max_area)


def _solve_kth_largest(lines):
    k = int(lines[0])
    nums = list(map(int, lines[1].split()))
    return str(sorted(nums, reverse=True)[k - 1])


def _solve_top_k_frequent(lines):
    k = int(lines[0])
    nums = list(map(int, lines[1].split()))
    from collections import Counter
    counts = Counter(nums)
    first_occurrence = {}
    for i, n in enumerate(nums):
        if n not in first_occurrence:
            first_occurrence[n] = i
    items = sorted(counts.items(), key=lambda x: (-x[1], first_occurrence[x[0]]))
    return " ".join(str(x[0]) for x in items[:k])


def _solve_merge_k_lists(lines):
    k = int(lines[0])
    merged = []
    for i in range(1, k + 1):
        merged.extend(map(int, lines[i].split()))
    merged.sort()
    return " ".join(map(str, merged))


def _solve_jump_game(lines):
    nums = list(map(int, lines[0].split()))
    reach = 0
    for i, n in enumerate(nums):
        if i > reach:
            return "false"
        reach = max(reach, i + n)
    return "true"


def _solve_gas_station(lines):
    gas = list(map(int, lines[0].split()))
    cost = list(map(int, lines[1].split()))
    total = sum(gas) - sum(cost)
    if total < 0:
        return "-1"
    tank = 0
    start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:
            start = i + 1
            tank = 0
    return str(start)


def _solve_candy(lines):
    ratings = list(map(int, lines[0].split()))
    n = len(ratings)
    candies = [1] * n
    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            candies[i] = candies[i - 1] + 1
    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            candies[i] = max(candies[i], candies[i + 1] + 1)
    return str(sum(candies))


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


def _solve_binary_search(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return str(mid)
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return "-1"


def _solve_search_rotated(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return str(mid)
        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return "-1"


def _solve_median_two_arrays(lines):
    a = list(map(int, lines[0].split())) if lines[0].strip() else []
    b = list(map(int, lines[1].split())) if lines[1].strip() else []
    merged = sorted(a + b)
    n = len(merged)
    if n % 2 == 1:
        return str(merged[n // 2])
    median = (merged[n // 2 - 1] + merged[n // 2]) / 2
    if median == int(median):
        return str(int(median))
    return f"{median:.1f}"


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


def _solve_remove_duplicates(lines):
    nums = list(map(int, lines[0].split()))
    out = []
    for n in nums:
        if not out or out[-1] != n:
            out.append(n)
    return " ".join(map(str, out))


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


PROBLEMS = [
    {
        "title": "Two Sum",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given an integer target and an array of integers nums, return the 0-indexed positions of the two numbers that add up to target. Exactly one valid pair exists.",
        "example_input": "9\n2 7 11 15",
        "constraints": "Input format: line 1 is the target, line 2 is the space-separated array. Output format: the two 0-indexed positions, space-separated.",
        "solve": _solve_two_sum,
        "sample_inputs": ["9\n2 7 11 15"],
        "hidden_inputs": ["6\n3 2 4", "7\n3 4", "10\n1 2 3 7"],
    },
    {
        "title": "Two Sum II",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given an array of n integers and a target, find two numbers whose sum equals target and return their 0-indexed positions.",
        "example_input": "4\n2 7 11 15\n9",
        "constraints": "Input format: line 1 is n, line 2 is the space-separated array, line 3 is the target. Output format: the two 0-indexed positions, space-separated.",
        "solve": _solve_two_sum_ii,
        "sample_inputs": ["4\n2 7 11 15\n9"],
        "hidden_inputs": ["3\n1 2 3\n5", "5\n0 4 3 0 8\n0"],
    },
    {
        "title": "Valid Parentheses",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid: every open bracket must be closed by the same type of bracket, in the correct order.",
        "example_input": "()[]{}",
        "constraints": "Input format: one line containing the string. Output format: \"true\" or \"false\" (lowercase).",
        "solve": _solve_valid_parentheses,
        "sample_inputs": ["()[]{}"],
        "hidden_inputs": ["(]", "([)]", "{[]}"],
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "topic": "array",
        "difficulty": "easy",
        "description": "Given an array of stock prices where prices[i] is the price on day i, return the maximum profit from buying on one day and selling on a later day. Return 0 if no profit is possible.",
        "example_input": "7 1 5 3 6 4",
        "constraints": "Input format: one line of space-separated prices. Output format: a single integer, the max profit.",
        "solve": _solve_best_time_to_sell_stock,
        "sample_inputs": ["7 1 5 3 6 4"],
        "hidden_inputs": ["7 6 4 3 1", "2 4 1 7"],
    },
    {
        "title": "Maximum Subarray",
        "topic": "array",
        "difficulty": "medium",
        "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) with the largest sum, and return that sum.",
        "example_input": "-2 1 -3 4 -1 2 1 -5 4",
        "constraints": "Input format: one line of space-separated integers (may be negative). Output format: a single integer, the max subarray sum.",
        "solve": _solve_max_subarray,
        "sample_inputs": ["-2 1 -3 4 -1 2 1 -5 4"],
        "hidden_inputs": ["1", "-1 -2 -3"],
    },
    {
        "title": "Trapping Rain Water",
        "topic": "array",
        "difficulty": "hard",
        "description": "Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.",
        "example_input": "0 1 0 2 1 0 1 3 2 1 2 1",
        "constraints": "Input format: one line of space-separated non-negative heights. Output format: a single integer, total trapped water.",
        "solve": _solve_trapping_rain_water,
        "sample_inputs": ["0 1 0 2 1 0 1 3 2 1 2 1"],
        "hidden_inputs": ["4 2 0 3 2 5", "0 0 0"],
    },
    {
        "title": "Binary Tree Inorder Traversal",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
        "example_input": "1 null 2 3",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: space-separated inorder values.",
        "solve": _solve_binary_tree_inorder,
        "sample_inputs": ["1 null 2 3"],
        "hidden_inputs": ["5 3 8 1 4 7 9", "10 5 15 2 7 12 20"],
    },
    {
        "title": "Maximum Depth of Binary Tree",
        "topic": "trees",
        "difficulty": "easy",
        "description": "Given the root of a binary tree, return its maximum depth (the number of nodes along the longest path from the root to a leaf).",
        "example_input": "3 9 20 null null 15 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_max_depth,
        "sample_inputs": ["3 9 20 null null 15 7"],
        "hidden_inputs": ["1", "null"],
    },
    {
        "title": "Diameter of Binary Tree",
        "topic": "trees",
        "difficulty": "hard",
        "description": "Given the root of a binary tree, return the length (in edges) of the diameter of the tree: the longest path between any two nodes, which may or may not pass through the root.",
        "example_input": "1 2 3 4 5",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_diameter,
        "sample_inputs": ["1 2 3 4 5"],
        "hidden_inputs": ["1 2", "1"],
    },
    {
        "title": "Number of Islands",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Given an m x n 2D binary grid representing a map of '1' (land) and '0' (water), return the number of islands (land cells connected horizontally or vertically).",
        "example_input": "4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0",
        "constraints": "Input format: line 1 is \"rows cols\", followed by `rows` lines of `cols` space-separated 0/1 values. Output format: a single integer.",
        "solve": _solve_number_of_islands,
        "sample_inputs": ["4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0"],
        "hidden_inputs": ["3 3\n1 1 0\n1 0 0\n0 0 1", "2 2\n0 0\n0 0"],
    },
    {
        "title": "Find if Path Exists in Graph",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "Given an undirected graph with n nodes (0-indexed) and a list of edges, determine if there is a valid path from a source node to a destination node.",
        "example_input": "3 2 0 2\n0 1\n1 2",
        "constraints": "Input format: line 1 is \"n m source destination\", followed by `m` lines each \"u v\" describing an edge. Output format: \"true\" or \"false\".",
        "solve": _solve_find_path_exists,
        "sample_inputs": ["3 2 0 2\n0 1\n1 2"],
        "hidden_inputs": ["4 2 0 3\n0 1\n2 3", "1 0 0 0"],
    },
    {
        "title": "Course Schedule",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "There are n courses (0-indexed) and a list of prerequisite pairs [a, b] meaning course b must be taken before course a. Return whether it's possible to finish all courses.",
        "example_input": "2 1\n1 0",
        "constraints": "Input format: line 1 is \"n m\", followed by `m` lines each \"a b\" meaning b is a prerequisite of a. Output format: \"true\" or \"false\".",
        "solve": _solve_course_schedule,
        "sample_inputs": ["2 1\n1 0"],
        "hidden_inputs": ["2 2\n1 0\n0 1", "4 3\n1 0\n2 1\n3 2"],
    },
    {
        "title": "Longest Increasing Subsequence",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "example_input": "10 9 2 5 3 7 101 18",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_lis,
        "sample_inputs": ["10 9 2 5 3 7 101 18"],
        "hidden_inputs": ["0 1 0 3 2 3", "7 7 7 7"],
    },
    {
        "title": "Climbing Stairs",
        "topic": "dp",
        "difficulty": "easy",
        "description": "You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. Return the number of distinct ways to reach the top.",
        "example_input": "5",
        "constraints": "Input format: one line containing n. Output format: a single integer.",
        "solve": _solve_climbing_stairs,
        "sample_inputs": ["5"],
        "hidden_inputs": ["2", "1"],
    },
    {
        "title": "Coin Change",
        "topic": "dp",
        "difficulty": "hard",
        "description": "Given an array of coin denominations and a target amount, return the fewest number of coins needed to make up that amount, or -1 if it can't be made.",
        "example_input": "1 2 5\n11",
        "constraints": "Input format: line 1 is space-separated coin denominations, line 2 is the target amount. Output format: a single integer.",
        "solve": _solve_coin_change,
        "sample_inputs": ["1 2 5\n11"],
        "hidden_inputs": ["2\n3", "1\n0"],
    },

    # --- string ---
    {
        "title": "Valid Anagram",
        "topic": "string",
        "difficulty": "easy",
        "description": "Given two strings s and t, determine if t is an anagram of s (uses exactly the same letters, same counts).",
        "example_input": "anagram\nnagaram",
        "constraints": "Input format: line 1 is s, line 2 is t. Output format: \"true\" or \"false\".",
        "solve": _solve_valid_anagram,
        "sample_inputs": ["anagram\nnagaram"],
        "hidden_inputs": ["rat\ncar", "a\nab"],
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "topic": "string",
        "difficulty": "medium",
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "example_input": "abcabcbb",
        "constraints": "Input format: one line containing s. Output format: a single integer.",
        "solve": _solve_longest_substr_no_repeat,
        "sample_inputs": ["abcabcbb"],
        "hidden_inputs": ["bbbbb", "pwwkew"],
    },
    {
        "title": "Longest Palindromic Substring",
        "topic": "string",
        "difficulty": "hard",
        "description": "Given a string s, return the longest palindromic substring in s. If there are multiple, return the one found by scanning left to right and expanding around each center first.",
        "example_input": "babad",
        "constraints": "Input format: one line containing s. Output format: the substring itself.",
        "solve": _solve_longest_palindrome,
        "sample_inputs": ["babad"],
        "hidden_inputs": ["cbbd", "a"],
    },

    # --- linked_list ---
    {
        "title": "Reverse Linked List",
        "topic": "linked_list",
        "difficulty": "easy",
        "description": "Given the head of a singly linked list, reverse the list and return the reversed list.",
        "example_input": "1 2 3 4 5",
        "constraints": "Input format: one line, space-separated list values head-to-tail. Output format: space-separated reversed values.",
        "solve": _solve_reverse_linked_list,
        "sample_inputs": ["1 2 3 4 5"],
        "hidden_inputs": ["1 2", "1"],
    },
    {
        "title": "Merge Two Sorted Lists",
        "topic": "linked_list",
        "difficulty": "medium",
        "description": "Given the heads of two sorted linked lists, merge them into one sorted list and return its head.",
        "example_input": "1 2 4\n1 3 4",
        "constraints": "Input format: line 1 and line 2 are the two sorted lists, space-separated. Output format: the merged sorted list, space-separated.",
        "solve": _solve_merge_two_lists,
        "sample_inputs": ["1 2 4\n1 3 4"],
        "hidden_inputs": ["5\n1 2 4", "1 3\n2"],
    },
    {
        "title": "Linked List Cycle",
        "topic": "linked_list",
        "difficulty": "hard",
        "description": "Given the head of a linked list and the index (0-based) the tail connects back to (-1 if it doesn't), determine if the list has a cycle.",
        "example_input": "3 2 0 -4\n1",
        "constraints": "Input format: line 1 is the space-separated node values, line 2 is the 0-indexed position the tail connects to (-1 for no cycle). Output format: \"true\" or \"false\".",
        "solve": _solve_linked_list_cycle,
        "sample_inputs": ["3 2 0 -4\n1"],
        "hidden_inputs": ["1 2\n0", "1\n-1"],
    },

    # --- stack_queue ---
    {
        "title": "Next Greater Element",
        "topic": "stack_queue",
        "difficulty": "easy",
        "description": "Given an array nums, for each element find the next element to its right that is greater than it. If none exists, use -1.",
        "example_input": "2 1 2 4 3",
        "constraints": "Input format: one line of space-separated integers. Output format: space-separated results, one per input element.",
        "solve": _solve_next_greater_element,
        "sample_inputs": ["2 1 2 4 3"],
        "hidden_inputs": ["1 2 3 4", "4 3 2 1"],
    },
    {
        "title": "Min Stack Operations",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "Simulate a stack that supports push(x), pop() and getMin() (returns the current minimum). Given a sequence of operations, output the result of every getMin call, in order.",
        "example_input": "5\npush 5\npush 3\ngetMin\npop\ngetMin",
        "constraints": "Input format: line 1 is the operation count Q, followed by Q lines each \"push x\", \"pop\", or \"getMin\". Output format: space-separated results of every getMin call.",
        "solve": _solve_min_stack,
        "sample_inputs": ["5\npush 5\npush 3\ngetMin\npop\ngetMin"],
        "hidden_inputs": [
            "4\npush 10\npush 20\ngetMin\ngetMin",
            "6\npush -2\npush 0\npush -3\ngetMin\npop\ngetMin",
        ],
    },
    {
        "title": "Largest Rectangle in Histogram",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Given an array of bar heights of width 1 each, find the area of the largest rectangle that can be formed within the histogram.",
        "example_input": "2 1 5 6 2 3",
        "constraints": "Input format: one line of space-separated non-negative heights. Output format: a single integer.",
        "solve": _solve_largest_rectangle,
        "sample_inputs": ["2 1 5 6 2 3"],
        "hidden_inputs": ["2 4", "1 1 1 1"],
    },

    # --- heap ---
    {
        "title": "Kth Largest Element in an Array",
        "topic": "heap",
        "difficulty": "easy",
        "description": "Given an integer array nums and an integer k, return the kth largest element (not the kth distinct element).",
        "example_input": "2\n3 2 1 5 6 4",
        "constraints": "Input format: line 1 is k, line 2 is the space-separated array. Output format: a single integer.",
        "solve": _solve_kth_largest,
        "sample_inputs": ["2\n3 2 1 5 6 4"],
        "hidden_inputs": ["4\n3 2 3 1 2 4 5 5 6", "1\n7 6 5 4"],
    },
    {
        "title": "Top K Frequent Elements",
        "topic": "heap",
        "difficulty": "medium",
        "description": "Given an integer array nums and an integer k, return the k most frequent elements, ordered by frequency (descending), ties broken by which value appeared first in the input.",
        "example_input": "2\n1 1 1 2 2 3",
        "constraints": "Input format: line 1 is k, line 2 is the space-separated array. Output format: space-separated top-k elements.",
        "solve": _solve_top_k_frequent,
        "sample_inputs": ["2\n1 1 1 2 2 3"],
        "hidden_inputs": ["1\n1", "3\n4 4 4 6 6 2 2 2 2"],
    },
    {
        "title": "Merge K Sorted Lists",
        "topic": "heap",
        "difficulty": "hard",
        "description": "Given k sorted arrays, merge them into one fully sorted array.",
        "example_input": "3\n1 4 5\n1 3 4\n2 6",
        "constraints": "Input format: line 1 is k, followed by k lines each a sorted space-separated array. Output format: the merged sorted array, space-separated.",
        "solve": _solve_merge_k_lists,
        "sample_inputs": ["3\n1 4 5\n1 3 4\n2 6"],
        "hidden_inputs": ["2\n1 2 3\n4 5 6", "1\n1"],
    },

    # --- greedy ---
    {
        "title": "Jump Game",
        "topic": "greedy",
        "difficulty": "easy",
        "description": "Given an array where each element is the maximum jump length from that position, determine if you can reach the last index starting from index 0.",
        "example_input": "2 3 1 1 4",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: \"true\" or \"false\".",
        "solve": _solve_jump_game,
        "sample_inputs": ["2 3 1 1 4"],
        "hidden_inputs": ["3 2 1 0 4", "0"],
    },
    {
        "title": "Gas Station",
        "topic": "greedy",
        "difficulty": "medium",
        "description": "There are n gas stations in a circuit; gas[i] is the fuel available at station i and cost[i] is the fuel needed to travel from station i to i+1. Return the starting station index that lets you complete the circuit, or -1 if impossible.",
        "example_input": "1 2 3 4 5\n3 4 5 1 2",
        "constraints": "Input format: line 1 is the space-separated gas array, line 2 is the space-separated cost array. Output format: a single integer.",
        "solve": _solve_gas_station,
        "sample_inputs": ["1 2 3 4 5\n3 4 5 1 2"],
        "hidden_inputs": ["2 3 4\n3 4 3", "5 1 2 3 4\n4 4 1 5 1"],
    },
    {
        "title": "Candy",
        "topic": "greedy",
        "difficulty": "hard",
        "description": "Each child is given a rating. Every child must get at least 1 candy, and a child with a higher rating than a neighbor must get more candy than that neighbor. Return the minimum total candies needed.",
        "example_input": "1 0 2",
        "constraints": "Input format: one line of space-separated ratings. Output format: a single integer.",
        "solve": _solve_candy,
        "sample_inputs": ["1 0 2"],
        "hidden_inputs": ["1 2 2", "1 3 4 5 2"],
    },

    # --- backtracking ---
    {
        "title": "Subsets",
        "topic": "backtracking",
        "difficulty": "easy",
        "description": "Given an array of distinct integers, return all non-empty subsets, one per line: first all subsets of size 1 in input order, then all of size 2, and so on.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line of space-separated distinct integers. Output format: one subset per line, space-separated values, ordered by increasing size.",
        "solve": _solve_subsets,
        "sample_inputs": ["1 2 3"],
        "hidden_inputs": ["1 2", "5"],
    },
    {
        "title": "Permutations",
        "topic": "backtracking",
        "difficulty": "medium",
        "description": "Given an array of distinct integers, return all possible permutations, one per line, in the standard lexicographic order relative to the input.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line of space-separated distinct integers. Output format: one permutation per line, space-separated values.",
        "solve": _solve_permutations,
        "sample_inputs": ["1 2 3"],
        "hidden_inputs": ["1 2", "1"],
    },
    {
        "title": "N-Queens Count",
        "topic": "backtracking",
        "difficulty": "hard",
        "description": "Given an integer n, return the number of distinct ways to place n queens on an n x n chessboard so that no two queens attack each other.",
        "example_input": "4",
        "constraints": "Input format: one line containing n. Output format: a single integer.",
        "solve": _solve_n_queens_count,
        "sample_inputs": ["4"],
        "hidden_inputs": ["1", "8"],
    },

    # --- binary_search ---
    {
        "title": "Binary Search",
        "topic": "binary_search",
        "difficulty": "easy",
        "description": "Given a sorted array of distinct integers and a target, return the index of target, or -1 if it isn't present.",
        "example_input": "-1 0 3 5 9 12\n9",
        "constraints": "Input format: line 1 is the sorted array, line 2 is the target. Output format: a single integer.",
        "solve": _solve_binary_search,
        "sample_inputs": ["-1 0 3 5 9 12\n9"],
        "hidden_inputs": ["-1 0 3 5 9 12\n2", "5\n5"],
    },
    {
        "title": "Search in Rotated Sorted Array",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Given a sorted array of distinct integers rotated at an unknown pivot, and a target, return its index, or -1 if not present.",
        "example_input": "4 5 6 7 0 1 2\n0",
        "constraints": "Input format: line 1 is the rotated array, line 2 is the target. Output format: a single integer.",
        "solve": _solve_search_rotated,
        "sample_inputs": ["4 5 6 7 0 1 2\n0"],
        "hidden_inputs": ["4 5 6 7 0 1 2\n3", "1\n0"],
    },
    {
        "title": "Median of Two Sorted Arrays",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Given two sorted arrays, return the median of the combined dataset. Print it as an integer if it's a whole number, otherwise with exactly one decimal place.",
        "example_input": "1 3\n2",
        "constraints": "Input format: line 1 and line 2 are the two sorted arrays, space-separated. Output format: the median, formatted as described above.",
        "solve": _solve_median_two_arrays,
        "sample_inputs": ["1 3\n2"],
        "hidden_inputs": ["1 2\n3 4", "0 0\n0 0"],
    },

    # --- two_pointers ---
    {
        "title": "Remove Duplicates from Sorted Array",
        "topic": "two_pointers",
        "difficulty": "easy",
        "description": "Given a sorted array, remove duplicates in-place so each element appears once, and return the resulting array.",
        "example_input": "0 0 1 1 1 2 2 3 3 4",
        "constraints": "Input format: one line, sorted space-separated integers (may contain duplicates). Output format: the deduplicated array, space-separated.",
        "solve": _solve_remove_duplicates,
        "sample_inputs": ["0 0 1 1 1 2 2 3 3 4"],
        "hidden_inputs": ["1 1 2", "1"],
    },
    {
        "title": "Container With Most Water",
        "topic": "two_pointers",
        "difficulty": "medium",
        "description": "Given an array of heights, choose two lines that together with the x-axis form a container holding the most water. Return that max area.",
        "example_input": "1 8 6 2 5 4 8 3 7",
        "constraints": "Input format: one line of space-separated non-negative heights. Output format: a single integer.",
        "solve": _solve_container_water,
        "sample_inputs": ["1 8 6 2 5 4 8 3 7"],
        "hidden_inputs": ["1 1", "4 3 2 1 4"],
    },
    {
        "title": "3Sum",
        "topic": "two_pointers",
        "difficulty": "hard",
        "description": "Given an integer array, return all unique triplets that sum to zero. Each triplet's values should be printed ascending; triplets should be printed in ascending lexicographic order, one per line. If none exist, print nothing.",
        "example_input": "-1 0 1 2 -1 -4",
        "constraints": "Input format: one line of space-separated integers. Output format: one triplet per line, space-separated, ascending order; empty output if none.",
        "solve": _solve_three_sum,
        "sample_inputs": ["-1 0 1 2 -1 -4"],
        "hidden_inputs": ["0 1 1", "0 0 0"],
    },

    # --- sliding_window ---
    {
        "title": "Maximum Average Subarray",
        "topic": "sliding_window",
        "difficulty": "easy",
        "description": "Given an array and an integer k, find the maximum average value of any contiguous subarray of length k.",
        "example_input": "4 4 4 4\n2",
        "constraints": "Input format: line 1 is the space-separated array, line 2 is k. Output format: the max average.",
        "solve": _solve_max_avg_subarray,
        "sample_inputs": ["4 4 4 4\n2"],
        "hidden_inputs": ["2 2 2 6\n2", "5 5\n2"],
    },
    {
        "title": "Longest Substring with At Most K Distinct Characters",
        "topic": "sliding_window",
        "difficulty": "medium",
        "description": "Given a string s and an integer k, find the length of the longest substring that contains at most k distinct characters.",
        "example_input": "eceba\n2",
        "constraints": "Input format: line 1 is s, line 2 is k. Output format: a single integer.",
        "solve": _solve_longest_k_distinct,
        "sample_inputs": ["eceba\n2"],
        "hidden_inputs": ["aa\n1", "abcadcacacaca\n3"],
    },
    {
        "title": "Minimum Window Substring",
        "topic": "sliding_window",
        "difficulty": "hard",
        "description": "Given strings s and t, return the smallest substring of s that contains every character of t (with the same multiplicity). Return an empty string if no such substring exists.",
        "example_input": "ADOBECODEBANC\nABC",
        "constraints": "Input format: line 1 is s, line 2 is t. Output format: the minimum window substring, or an empty line if none.",
        "solve": _solve_min_window_substring,
        "sample_inputs": ["ADOBECODEBANC\nABC"],
        "hidden_inputs": ["a\na", "a\naa"],
    },

    # --- bit_manipulation ---
    {
        "title": "Single Number",
        "topic": "bit_manipulation",
        "difficulty": "easy",
        "description": "Given a non-empty array where every element appears twice except for one, find that single element.",
        "example_input": "4 1 2 1 2",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_single_number,
        "sample_inputs": ["4 1 2 1 2"],
        "hidden_inputs": ["2 2 1", "1"],
    },
    {
        "title": "Counting Bits",
        "topic": "bit_manipulation",
        "difficulty": "medium",
        "description": "Given an integer n, return an array of length n+1 where the value at index i is the number of 1's in the binary representation of i.",
        "example_input": "5",
        "constraints": "Input format: one line containing n. Output format: space-separated counts for i = 0..n.",
        "solve": _solve_counting_bits,
        "sample_inputs": ["5"],
        "hidden_inputs": ["2", "0"],
    },
    {
        "title": "Maximum XOR of Two Numbers in an Array",
        "topic": "bit_manipulation",
        "difficulty": "hard",
        "description": "Given an array of integers (at least two elements), find the maximum XOR of any two elements.",
        "example_input": "3 10 5 25 2 8",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_max_xor,
        "sample_inputs": ["3 10 5 25 2 8"],
        "hidden_inputs": ["2 4", "8 10 2"],
    },

    # --- math ---
    {
        "title": "Reverse Integer",
        "topic": "math",
        "difficulty": "easy",
        "description": "Given a signed 32-bit integer x, return x with its digits reversed. If reversing causes it to go outside the signed 32-bit range, return 0.",
        "example_input": "123",
        "constraints": "Input format: one line containing the integer. Output format: a single integer.",
        "solve": _solve_reverse_integer,
        "sample_inputs": ["123"],
        "hidden_inputs": ["-123", "120"],
    },
    {
        "title": "Pow(x, n)",
        "topic": "math",
        "difficulty": "medium",
        "description": "Given an integer x and a non-negative integer n, compute x raised to the power n.",
        "example_input": "2\n10",
        "constraints": "Input format: line 1 is x, line 2 is n (n >= 0). Output format: a single integer.",
        "solve": _solve_pow,
        "sample_inputs": ["2\n10"],
        "hidden_inputs": ["3\n0", "5\n3"],
    },
    {
        "title": "Integer to Roman",
        "topic": "math",
        "difficulty": "hard",
        "description": "Given an integer in the range 1 to 3999, convert it to a Roman numeral.",
        "example_input": "1994",
        "constraints": "Input format: one line containing the integer. Output format: the Roman numeral string.",
        "solve": _solve_int_to_roman,
        "sample_inputs": ["1994"],
        "hidden_inputs": ["58", "3"],
    },
]


class Command(BaseCommand):
    help = "Seeds/repairs problems and their sample + hidden test cases."

    def handle(self, *args, **options):
        owner = User.objects.filter(is_superuser=True).order_by("id").first()
        if owner is None:
            self.stderr.write(self.style.ERROR(
                "No superuser exists to own seeded problems. Create one first: "
                "python manage.py createsuperuser"
            ))
            return

        with transaction.atomic():
            for spec in PROBLEMS:
                solve = spec["solve"]
                example_output = solve(spec["example_input"].split("\n"))

                problem, _ = Problem.objects.update_or_create(
                    title=spec["title"],
                    defaults={
                        "topic": spec["topic"],
                        "difficulty": spec["difficulty"],
                        "description": spec["description"],
                        "example_input": spec["example_input"],
                        "example_output": example_output,
                        "constraints": spec["constraints"],
                        "created_by": owner,
                    },
                )

                problem.test_cases.all().delete()

                test_cases = []
                for raw_input in spec["sample_inputs"]:
                    expected = solve(raw_input.split("\n"))
                    test_cases.append(TestCase(
                        problem=problem,
                        input_data=raw_input,
                        expected_output=expected,
                        is_sample=True,
                    ))
                for raw_input in spec["hidden_inputs"]:
                    expected = solve(raw_input.split("\n"))
                    test_cases.append(TestCase(
                        problem=problem,
                        input_data=raw_input,
                        expected_output=expected,
                        is_sample=False,
                    ))
                TestCase.objects.bulk_create(test_cases)

                self.stdout.write(self.style.SUCCESS(
                    f"{problem.title} ({problem.topic}/{problem.difficulty}): "
                    f"{len(spec['sample_inputs'])} sample + {len(spec['hidden_inputs'])} hidden test cases"
                ))

        self.stdout.write(self.style.SUCCESS(f"Done. {len(PROBLEMS)} problems seeded."))
