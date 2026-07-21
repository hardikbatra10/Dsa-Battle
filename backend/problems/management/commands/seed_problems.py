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
