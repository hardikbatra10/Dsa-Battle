"""Dp problems."""

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

def _grid(lines, rows, start=1):
    return [list(map(int, lines[start + i].split())) for i in range(rows)]


def _solve_predict_winner(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = nums[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(nums[i] - dp[i + 1][j], nums[j] - dp[i][j - 1])
    return "true" if dp[0][n - 1] >= 0 else "false"


def _solve_interleaving_string(lines):
    s1 = lines[0]
    s2 = lines[1]
    s3 = lines[2] if len(lines) > 2 else ""
    if len(s1) + len(s2) != len(s3):
        return "false"
    dp = [[False] * (len(s2) + 1) for _ in range(len(s1) + 1)]
    dp[0][0] = True
    for i in range(len(s1) + 1):
        for j in range(len(s2) + 1):
            if i and dp[i - 1][j] and s1[i - 1] == s3[i + j - 1]:
                dp[i][j] = True
            if j and dp[i][j - 1] and s2[j - 1] == s3[i + j - 1]:
                dp[i][j] = True
    return "true" if dp[len(s1)][len(s2)] else "false"


def _solve_unique_paths(lines):
    m, n = map(int, lines[0].split())
    dp = [1] * n
    for _ in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j - 1]
    return str(dp[n - 1])


def _solve_perfect_squares(lines):
    n = int(lines[0])
    dp = [0] + [float("inf")] * n
    for i in range(1, n + 1):
        j = 1
        while j * j <= i:
            dp[i] = min(dp[i], dp[i - j * j] + 1)
            j += 1
    return str(dp[n])


def _solve_decode_ways(lines):
    s = lines[0]
    if not s or s[0] == "0":
        return "0"
    prev, cur = 1, 1
    for i in range(1, len(s)):
        nxt = 0
        if s[i] != "0":
            nxt += cur
        if 10 <= int(s[i - 1:i + 1]) <= 26:
            nxt += prev
        prev, cur = cur, nxt
    return str(cur)


def _solve_count_good_strings(lines):
    low, high, zero, one = map(int, lines[0].split())
    MOD = 10 ** 9 + 7
    dp = [0] * (high + 1)
    dp[0] = 1
    total = 0
    for i in range(1, high + 1):
        if i >= zero:
            dp[i] = (dp[i] + dp[i - zero]) % MOD
        if i >= one:
            dp[i] = (dp[i] + dp[i - one]) % MOD
        if i >= low:
            total = (total + dp[i]) % MOD
    return str(total)


def _solve_min_cost_tickets(lines):
    days = list(map(int, lines[0].split()))
    c1, c7, c30 = map(int, lines[1].split())
    wanted = set(days)
    last = days[-1]
    dp = [0] * (last + 1)
    for i in range(1, last + 1):
        if i not in wanted:
            dp[i] = dp[i - 1]
        else:
            dp[i] = min(dp[i - 1] + c1,
                        dp[max(0, i - 7)] + c7,
                        dp[max(0, i - 30)] + c30)
    return str(dp[last])


def _solve_min_coins_fruits(lines):
    prices = list(map(int, lines[0].split()))
    n = len(prices)
    INF = float("inf")
    dp = [INF] * (n + 2)
    dp[n + 1] = 0
    for i in range(n, 0, -1):
        best = INF
        for j in range(i + 1, min(n, 2 * i) + 2):
            best = min(best, dp[j])
        dp[i] = prices[i - 1] + best
    return str(dp[1])


def _solve_mystic_dungeon(lines):
    energy = list(map(int, lines[0].split()))
    k = int(lines[1])
    n = len(energy)
    dp = [0] * n
    best = float("-inf")
    for i in range(n - 1, -1, -1):
        dp[i] = energy[i] + (dp[i + k] if i + k < n else 0)
        best = max(best, dp[i])
    return str(best)


def _solve_max_jumps(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    n = len(nums)
    NEG = float("-inf")
    dp = [NEG] * n
    dp[0] = 0
    for j in range(1, n):
        for i in range(j):
            if dp[i] != NEG and abs(nums[j] - nums[i]) <= target:
                dp[j] = max(dp[j], dp[i] + 1)
    return str(dp[n - 1]) if dp[n - 1] != NEG else "-1"


def _solve_min_falling_path(lines):
    n = int(lines[0])
    grid = _grid(lines, n)
    for i in range(1, n):
        for j in range(n):
            best = grid[i - 1][j]
            if j > 0:
                best = min(best, grid[i - 1][j - 1])
            if j < n - 1:
                best = min(best, grid[i - 1][j + 1])
            grid[i][j] += best
    return str(min(grid[n - 1]))


def _solve_paint_house(lines):
    n = int(lines[0])
    if n == 0:
        return "0"
    costs = _grid(lines, n)
    dp = costs[0][:]
    for i in range(1, n):
        dp = [costs[i][0] + min(dp[1], dp[2]),
              costs[i][1] + min(dp[0], dp[2]),
              costs[i][2] + min(dp[0], dp[1])]
    return str(min(dp))


def _solve_min_falling_path_ii(lines):
    n = int(lines[0])
    grid = _grid(lines, n)
    dp = grid[0][:]
    for i in range(1, n):
        nxt = []
        for j in range(n):
            best = min(dp[c] for c in range(n) if c != j)
            nxt.append(grid[i][j] + best)
        dp = nxt
    return str(min(dp))


def _solve_knight_dialer(lines):
    n = int(lines[0])
    MOD = 10 ** 9 + 7
    moves = {0: [4, 6], 1: [6, 8], 2: [7, 9], 3: [4, 8], 4: [3, 9, 0],
             5: [], 6: [1, 7, 0], 7: [2, 6], 8: [1, 3], 9: [2, 4]}
    dp = [1] * 10
    for _ in range(n - 1):
        nxt = [0] * 10
        for d in range(10):
            for m in moves[d]:
                nxt[m] = (nxt[m] + dp[d]) % MOD
        dp = nxt
    return str(sum(dp) % MOD)


def _solve_max_moves_grid(lines):
    m, n = map(int, lines[0].split())
    grid = _grid(lines, m)
    dp = [[0] * n for _ in range(m)]
    best = 0
    for j in range(1, n):
        for i in range(m):
            for di in (-1, 0, 1):
                pi = i + di
                if 0 <= pi < m and grid[pi][j - 1] < grid[i][j]:
                    if j - 1 == 0 or dp[pi][j - 1] > 0:
                        dp[i][j] = max(dp[i][j], dp[pi][j - 1] + 1)
            best = max(best, dp[i][j])
    return str(best)


def _solve_increasing_paths_grid(lines):
    m, n = map(int, lines[0].split())
    grid = _grid(lines, m)
    MOD = 10 ** 9 + 7
    memo = {}

    def go(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        total = 1
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > grid[i][j]:
                total = (total + go(ni, nj)) % MOD
        memo[(i, j)] = total
        return total

    return str(sum(go(i, j) for i in range(m) for j in range(n)) % MOD)


def _solve_longest_increasing_path(lines):
    m, n = map(int, lines[0].split())
    grid = _grid(lines, m)
    memo = {}

    def go(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        best = 1
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] > grid[i][j]:
                best = max(best, 1 + go(ni, nj))
        memo[(i, j)] = best
        return best

    return str(max(go(i, j) for i in range(m) for j in range(n)))


def _solve_maximal_square(lines):
    m, n = map(int, lines[0].split())
    grid = _grid(lines, m)
    dp = [[0] * n for _ in range(m)]
    best = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                if i == 0 or j == 0:
                    dp[i][j] = 1
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                best = max(best, dp[i][j])
    return str(best * best)


def _solve_bomb_enemy(lines):
    m, n = map(int, lines[0].split())
    grid = [lines[1 + i].split() for i in range(m)]
    best = 0
    row_hits = 0
    col_hits = [0] * n
    for i in range(m):
        for j in range(n):
            if j == 0 or grid[i][j - 1] == "W":
                row_hits = 0
                for k in range(j, n):
                    if grid[i][k] == "W":
                        break
                    if grid[i][k] == "E":
                        row_hits += 1
            if i == 0 or grid[i - 1][j] == "W":
                col_hits[j] = 0
                for k in range(i, m):
                    if grid[k][j] == "W":
                        break
                    if grid[k][j] == "E":
                        col_hits[j] += 1
            if grid[i][j] == "0":
                best = max(best, row_hits + col_hits[j])
    return str(best)


def _solve_delete_and_earn(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = Counter(nums)
    top = max(nums)
    dp = [0] * (top + 1)
    dp[1] = counts.get(1, 0)
    for v in range(2, top + 1):
        dp[v] = max(dp[v - 1], dp[v - 2] + v * counts.get(v, 0))
    return str(dp[top])

def _solve_min_cost_climbing_stairs(lines):
    cost = list(map(int, lines[0].split()))
    a, b = 0, 0
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return str(b)


def _solve_fibonacci(lines):
    n = int(lines[0])
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return str(a)


def _solve_tribonacci(lines):
    n = int(lines[0])
    a, b, c = 0, 1, 1
    if n == 0:
        return "0"
    if n <= 2:
        return "1"
    for _ in range(3, n + 1):
        a, b, c = b, c, a + b + c
    return str(c)


def _solve_is_subsequence(lines):
    s = lines[0]
    t = lines[1] if len(lines) > 1 else ""
    i = 0
    for c in t:
        if i < len(s) and s[i] == c:
            i += 1
    return "true" if i == len(s) else "false"


def _solve_house_robber(lines):
    nums = list(map(int, lines[0].split()))
    take, skip = 0, 0
    for v in nums:
        take, skip = skip + v, max(skip, take)
    return str(max(take, skip))


def _solve_partition_equal_subset(lines):
    nums = list(map(int, lines[0].split()))
    total = sum(nums)
    if total % 2:
        return "false"
    target = total // 2
    reachable = 1
    for v in nums:
        reachable |= reachable << v
    return "true" if (reachable >> target) & 1 else "false"


def _solve_edit_distance(lines):
    a = lines[0]
    b = lines[1] if len(lines) > 1 else ""
    prev = list(range(len(b) + 1))
    for i in range(1, len(a) + 1):
        cur = [i] + [0] * len(b)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
        prev = cur
    return str(prev[len(b)])


def _solve_burst_balloons(lines):
    nums = [1] + list(map(int, lines[0].split())) + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for lo in range(0, n - length):
            hi = lo + length
            for k in range(lo + 1, hi):
                dp[lo][hi] = max(dp[lo][hi],
                                 dp[lo][k] + nums[lo] * nums[k] * nums[hi] + dp[k][hi])
    return str(dp[0][n - 1])


def _solve_regex_matching(lines):
    s = lines[0]
    p = lines[1] if len(lines) > 1 else ""
    memo = {}

    def go(i, j):
        if (i, j) in memo:
            return memo[(i, j)]
        if j == len(p):
            result = i == len(s)
        else:
            first = i < len(s) and p[j] in (s[i], ".")
            if j + 1 < len(p) and p[j + 1] == "*":
                result = go(i, j + 2) or (first and go(i + 1, j))
            else:
                result = first and go(i + 1, j + 1)
        memo[(i, j)] = result
        return result

    return "true" if go(0, 0) else "false"


def _solve_distinct_subsequences(lines):
    s = lines[0]
    t = lines[1] if len(lines) > 1 else ""
    dp = [1] + [0] * len(t)
    for c in s:
        for j in range(len(t), 0, -1):
            if t[j - 1] == c:
                dp[j] += dp[j - 1]
    return str(dp[len(t)])


PROBLEMS = [
{
        "title": "Longest Increasing Subsequence",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Given an integer array nums, return the length of the longest strictly increasing subsequence.",
        "example_input": "10 9 2 5 3 7 101 18",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_lis,
        "sample_inputs": ["10 9 2 5 3 7 101 18", "3 10 2 1 20"],
        "hidden_inputs": [
            "1",
            "10",
            "7 7 7 7",    # all equal -> strictly increasing means 1
            "5 4 3 2 1",  # strictly decreasing
            "1 2 3 4 5",  # already increasing
            "2 2 2 1 3",
            "-1 -2 -3 0",
            "0 1 0 3 2 3",
            "4 10 4 3 8 9",
            "1 3 6 7 9 4 10 5 6",
        ],
    },
{
        "title": "Climbing Stairs",
        "topic": "dp",
        "difficulty": "easy",
        "description": "You are climbing a staircase with n steps. Each time you can climb 1 or 2 steps. Return the number of distinct ways to reach the top.",
        "example_input": "5",
        "constraints": "Input format: one line containing n. Output format: a single integer.",
        "solve": _solve_climbing_stairs,
        "sample_inputs": ["5", "7"],
        "hidden_inputs": [
            "1",
            "2",
            "3",
            "4",
            "10",
            "20",
            "30",
            "45",  # largest n whose answer still fits in signed 32-bit
        ],
    },
{
        "title": "Coin Change",
        "topic": "dp",
        "difficulty": "hard",
        "description": "Given an array of coin denominations and a target amount, return the fewest number of coins needed to make up that amount, or -1 if it can't be made.",
        "example_input": "1 2 5\n11",
        "constraints": "Input format: line 1 is space-separated coin denominations, line 2 is the target amount. Output format: a single integer.",
        "solve": _solve_coin_change,
        "sample_inputs": ["1 2 5\n11", "2 3 5\n9"],
        "hidden_inputs": [
            "1\n0",    # amount 0 needs no coins
            "2\n0",
            "1\n1",
            "5\n3",    # single coin larger than the amount
            "2\n3",    # unreachable odd amount
            "3 7\n5",
            "7 11\n14",
            "2 5 10 1\n27",
            "1\n100",  # answer equals the amount
            "1 2 5\n100",
            "186 419 83 408\n6249",
        ],
    },
{
        "title": "Unique Paths",
        "topic": "dp",
        "difficulty": "easy",
        "description": "A robot starts in the top-left cell of an m by n grid and may only move right or down. Return how many distinct paths reach the bottom-right cell.",
        "example_input": "3 7",
        "constraints": "Input format: one line containing m and n. Output format: a single integer.",
        "solve": _solve_unique_paths,
        "sample_inputs": ["3 7", "3 2"],
        "hidden_inputs": [
            "1 1",                  # already at the destination
            "1 5",                  # a single row, one path
            "5 1",                  # a single column
            "2 2",
            "2 3",
            "3 3",
            "4 4",
            "7 3",                  # the transpose of the sample
            "10 10",
            "16 16",                # large enough to need real counting
        ],
    },
{
        "title": "Perfect Squares",
        "topic": "dp",
        "difficulty": "easy",
        "description": "Return the fewest perfect squares that sum to n. A perfect square is the product of an integer with itself.",
        "example_input": "12",
        "constraints": "Input format: one line containing n (n >= 0). Output format: a single integer.",
        "solve": _solve_perfect_squares,
        "sample_inputs": ["12", "13"],
        "hidden_inputs": [
            "0",                    # nothing is needed
            "1",                    # already a perfect square
            "2",                    # 1 + 1
            "3",
            "4",
            "7",                    # needs the maximum of four squares
            "9",
            "28",
            "48",
            "100",
        ],
    },
{
        "title": "Paint House",
        "topic": "dp",
        "difficulty": "easy",
        "description": "Each house must be painted red, blue or green, and no two neighbouring houses may share a colour. Given each house's cost for each colour, return the smallest total cost.",
        "example_input": "3\n17 2 17\n16 16 5\n14 3 19",
        "constraints": "Input format: line 1 is the number of houses n, followed by n lines each holding the three costs. Output format: a single integer.",
        "solve": _solve_paint_house,
        "sample_inputs": ["3\n17 2 17\n16 16 5\n14 3 19", "2\n1 2 3\n3 2 1"],
        "hidden_inputs": [
            "0",                    # no houses at all
            "1\n5 3 8",             # one house takes its cheapest colour
            "1\n7 7 7",             # all colours cost the same
            "2\n1 1 1\n1 1 1",
            "2\n1 100 100\n1 100 100",   # the cheap colour cannot repeat
            "3\n1 1 1\n1 1 1\n1 1 1",
            "3\n0 0 0\n0 0 0\n0 0 0",    # zero costs
            "4\n1 5 3\n2 9 4\n3 1 5\n9 2 1",
            "5\n8 1 3\n2 7 4\n6 2 9\n1 8 5\n4 3 7",
            "2\n100 1 1\n1 1 100",
        ],
    },
{
        "title": "Minimum Falling Path Sum",
        "topic": "dp",
        "difficulty": "easy",
        "description": "Starting anywhere in the first row of a square grid, fall to the bottom by moving each step to the cell directly below or diagonally below-left or below-right. Return the smallest possible total of the visited cells.",
        "example_input": "3\n2 1 3\n6 5 4\n7 8 9",
        "constraints": "Input format: line 1 is n, followed by n lines each holding n integers. Output format: a single integer.",
        "solve": _solve_min_falling_path,
        "sample_inputs": ["3\n2 1 3\n6 5 4\n7 8 9", "2\n-19 57\n-40 -5"],
        "hidden_inputs": [
            "1\n5",                 # a single cell
            "1\n-5",                # a single negative cell
            "2\n1 2\n3 4",
            "2\n1 1\n1 1",          # all equal
            "3\n1 1 1\n1 1 1\n1 1 1",
            "3\n0 0 0\n0 0 0\n0 0 0",
            "3\n-1 -2 -3\n-4 -5 -6\n-7 -8 -9",   # all negative
            "3\n100 1 100\n100 1 100\n100 1 100",  # a cheap central column
            "4\n1 9 9 9\n9 1 9 9\n9 9 1 9\n9 9 9 1",   # the diagonal is cheapest
            "4\n5 3 8 1\n2 7 4 9\n6 1 3 2\n8 4 7 5",
        ],
    },
{
        "title": "Delete and Earn",
        "topic": "dp",
        "difficulty": "easy",
        "description": "Pick a value from the array and earn it once for every copy present, but doing so deletes every copy of that value minus one and that value plus one. Return the largest total that can be earned.",
        "example_input": "3 4 2",
        "constraints": "Input format: one line of space-separated positive integers. Output format: a single integer.",
        "solve": _solve_delete_and_earn,
        "sample_inputs": ["3 4 2", "2 2 3 3 3 4"],
        "hidden_inputs": [
            "1",                    # a single value
            "5",
            "1 1 1",                # repeats of one value all count
            "1 2",                  # neighbours, only one survives
            "2 1",
            "1 3",                  # not neighbours, take both
            "1 1 1 2 4 5 5",
            "3 3 3 4 2",
            "1 2 3 4 5 6 7 8 9 10",
            "10 10 10 9 9 8",
        ],
    },
{
        "title": "Decode Ways",
        "topic": "dp",
        "difficulty": "medium",
        "description": "A message of digits was encoded by mapping A to 1 through Z to 26. Count how many different letter strings the digit string could decode to. A group may not have a leading zero.",
        "example_input": "226",
        "constraints": "Input format: one line containing the digit string. Output format: a single integer.",
        "solve": _solve_decode_ways,
        "sample_inputs": ["226", "12"],
        "hidden_inputs": [
            "0",                    # a lone zero decodes to nothing
            "1",                    # a single digit
            "06",                   # leading zero kills it
            "10",                   # only the pair works
            "27",                   # the pair exceeds 26
            "100",                  # a zero that cannot be paired
            "101",
            "110",
            "1111",
            "2626",
        ],
    },
{
        "title": "Count Ways To Build Good Strings",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Build a binary string by repeatedly appending either zero copies of '0' a fixed number of times or '1' a fixed number of times. Count the strings whose length lies between low and high inclusive, modulo 1000000007.",
        "example_input": "3 3 1 1",
        "constraints": "Input format: one line holding low, high, zero and one. Output format: a single integer, the count modulo 1000000007.",
        "solve": _solve_count_good_strings,
        "sample_inputs": ["3 3 1 1", "2 3 1 2"],
        "hidden_inputs": [
            "1 1 1 1",              # two strings of length one
            "1 1 2 2",              # no string of length one can be built
            "1 2 2 2",
            "1 5 1 1",              # every length is reachable
            "2 2 1 2",
            "4 4 2 2",
            "1 10 3 5",
            "5 5 5 5",
            "1 20 1 2",
            "10 15 4 6",
        ],
    },
{
        "title": "Minimum Cost For Tickets",
        "topic": "dp",
        "difficulty": "medium",
        "description": "You have a list of the days you plan to travel. A ticket covers one day, seven consecutive days or thirty consecutive days, at three given prices. Return the least you can spend to cover every travel day.",
        "example_input": "1 4 6 7 8 20\n2 7 15",
        "constraints": "Input format: line 1 is the ascending travel days, line 2 is the one-day, seven-day and thirty-day prices. Output format: a single integer.",
        "solve": _solve_min_cost_tickets,
        "sample_inputs": ["1 4 6 7 8 20\n2 7 15", "1 2 3 4 5 6 7 8 9 10 30 31\n2 7 15"],
        "hidden_inputs": [
            "1\n2 7 15",            # a single travel day
            "1\n10 3 1",            # the thirty-day pass is cheapest outright
            "1 2\n2 7 15",
            "1 7\n2 7 15",          # exactly a week apart
            "1 8\n2 7 15",          # one day too far for a single week pass
            "1 2 3 4 5 6 7\n2 7 15",     # a week pass exactly pays off
            "1 2 3 4 5 6 7 8\n2 7 15",
            "1 30\n2 7 15",
            "1 4 6 7 8 20\n7 2 15",      # a week pass cheaper than a day pass
            "2 4 6 8 10 12 14 16 18 20\n2 7 15",
        ],
    },
{
        "title": "Minimum Number of Coins for Fruits",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Fruits are numbered from one. Paying for fruit i entitles you to take the next i fruits for free, though you may still choose to pay for any of them to extend the offer. Return the fewest coins needed to acquire every fruit.",
        "example_input": "3 1 2",
        "constraints": "Input format: one line of space-separated prices, where position i holds the price of fruit i (counting from one). Output format: a single integer.",
        "solve": _solve_min_coins_fruits,
        "sample_inputs": ["3 1 2", "1 10 1 1"],
        "hidden_inputs": [
            "5",                    # one fruit must be paid for
            "1 1",                  # the first purchase covers the second
            "5 1",                  # still cheaper to take the free one
            "1 5 5",
            "2 2 2",
            "1 1 1 1",
            "3 1 2 5 1",
            "26 18 6 12 49 15",
            "1 100 1 100 1",        # paying again beats a long free run
            "10 9 8 7 6 5",
        ],
    },
{
        "title": "Taking Maximum Energy From the Mystic Dungeon",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Starting at any position, you absorb that position's energy and are teleported k places forward, repeating until you would leave the line. Return the greatest total energy obtainable.",
        "example_input": "5 2 -10 -5 1\n3",
        "constraints": "Input format: line 1 is the space-separated energy values, line 2 is k. Output format: a single integer.",
        "solve": _solve_mystic_dungeon,
        "sample_inputs": ["5 2 -10 -5 1\n3", "-2 -3 -1\n2"],
        "hidden_inputs": [
            "5\n1",                 # a single position
            "-5\n1",                # a single negative position
            "1 2 3\n3",             # k skips straight off the end
            "1 2 3\n1",             # k of one chains everything
            "-1 -2 -3\n1",          # all negative, take the least bad
            "0 0 0\n2",
            "1 -1 1 -1 1\n2",
            "10 -5 10 -5 10\n2",
            "-1 5 -1 5 -1\n2",
            "3 1 4 1 5 9 2 6\n3",
        ],
    },
{
        "title": "Maximum Number of Jumps to Reach the Last Index",
        "topic": "dp",
        "difficulty": "medium",
        "description": "From index i you may jump forward to any index j where the difference between the two values is at most target in absolute terms. Starting at the first index, return the largest number of jumps that reaches the last index, or -1 if it cannot be reached.",
        "example_input": "1 3 6 4 1 2\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is target. Output format: a single integer, or -1.",
        "solve": _solve_max_jumps,
        "sample_inputs": ["1 3 6 4 1 2\n2", "1 3 6 4 1 2\n3"],
        "hidden_inputs": [
            "1\n0",                 # already at the last index
            "1 2\n0",               # the gap is too wide
            "1 1\n0",               # equal values allow a zero-target jump
            "1 2\n1",
            "1 3 6 4 1 2\n0",       # unreachable, so -1
            "0 0 0 0\n0",           # every hop is legal, take them all
            "1 2 3 4 5\n1",
            "1 5 2 6 3\n4",
            "-1 -2 -3\n1",          # negatives
            "5 1 5 1 5\n4",
        ],
    },
{
        "title": "Minimum Falling Path Sum II",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Fall from the top row of a square grid to the bottom, taking exactly one cell per row, with the rule that no two cells chosen in consecutive rows may share a column. Return the smallest possible total.",
        "example_input": "3\n1 2 3\n4 5 6\n7 8 9",
        "constraints": "Input format: line 1 is n, followed by n lines each holding n integers. Output format: a single integer.",
        "solve": _solve_min_falling_path_ii,
        "sample_inputs": ["3\n1 2 3\n4 5 6\n7 8 9", "2\n7 6\n1 3"],
        "hidden_inputs": [
            "1\n7",                 # one row, one column, no constraint
            "2\n1 2\n3 4",
            "2\n1 1\n1 1",
            "3\n1 1 1\n1 1 1\n1 1 1",
            "3\n0 0 0\n0 0 0\n0 0 0",
            "3\n1 100 100\n1 100 100\n1 100 100",   # the cheap column cannot repeat
            "3\n-1 -2 -3\n-4 -5 -6\n-7 -8 -9",
            "4\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 16",
            "4\n5 9 2 7\n3 8 4 1\n6 2 9 5\n7 4 1 8",
            "3\n7 1 2\n3 9 4\n5 6 8",
        ],
    },
{
        "title": "Knight Dialer",
        "topic": "dp",
        "difficulty": "medium",
        "description": "A chess knight stands on a telephone keypad and makes jumps in the usual L shape, never leaving the pad. Starting from any digit, count the distinct numbers of exactly n digits it can dial, modulo 1000000007.",
        "example_input": "3",
        "constraints": "Input format: one line containing n (n >= 1). Output format: a single integer, the count modulo 1000000007.",
        "solve": _solve_knight_dialer,
        "sample_inputs": ["3", "2"],
        "hidden_inputs": [
            "1",                    # every digit is reachable on its own
            "4",
            "5",
            "6",
            "10",
            "20",
            "50",
            "100",                  # large enough that the modulus bites
            "161",
            "3131",                 # stresses the iteration count
        ],
    },
{
        "title": "Maximum Number of Moves in a Grid",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Starting from any cell in the first column, you may move to the cell to the right, right-and-up or right-and-down, provided the destination holds a strictly larger value. Return the greatest number of moves possible.",
        "example_input": "3 4\n2 4 3 5\n5 4 9 3\n3 4 2 11",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of integers. Output format: a single integer.",
        "solve": _solve_max_moves_grid,
        "sample_inputs": ["3 4\n2 4 3 5\n5 4 9 3\n3 4 2 11", "3 3\n3 2 4\n2 1 9\n1 1 7"],
        "hidden_inputs": [
            "1 1\n5",               # nowhere to move
            "1 2\n1 2",             # a single move right
            "1 2\n2 1",             # not strictly larger, no move
            "2 2\n1 2\n3 4",
            "2 2\n1 1\n1 1",        # all equal, no move is legal
            "3 1\n1\n2\n3",         # a single column
            "2 3\n1 2 3\n4 5 6",
            "3 3\n1 2 3\n4 5 6\n7 8 9",
            "3 3\n9 8 7\n6 5 4\n3 2 1",   # decreasing, no move
            "4 4\n1 5 2 9\n3 1 8 4\n7 2 6 1\n2 9 3 5",
        ],
    },
{
        "title": "Maximal Square",
        "topic": "dp",
        "difficulty": "medium",
        "description": "Given a grid of zeroes and ones, find the largest square made entirely of ones and return its area.",
        "example_input": "4 5\n1 0 1 0 0\n1 0 1 1 1\n1 1 1 1 1\n1 0 0 1 0",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of 0 and 1 values. Output format: a single integer, the area.",
        "solve": _solve_maximal_square,
        "sample_inputs": ["4 5\n1 0 1 0 0\n1 0 1 1 1\n1 1 1 1 1\n1 0 0 1 0", "2 2\n0 1\n1 0"],
        "hidden_inputs": [
            "1 1\n0",               # no ones at all
            "1 1\n1",               # a single one
            "1 4\n1 1 1 1",         # a single row can only hold a 1x1 square
            "4 1\n1\n1\n1\n1",      # a single column
            "2 2\n1 1\n1 1",
            "3 3\n0 0 0\n0 0 0\n0 0 0",
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 3\n1 1 0\n1 1 0\n0 0 1",
            "4 4\n1 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 1",
            "4 5\n0 1 1 0 1\n1 1 0 1 0\n0 1 1 1 0\n1 1 1 1 0",
        ],
    },
{
        "title": "Predict the Winner",
        "topic": "dp",
        "difficulty": "hard",
        "description": "Two players alternate taking a number from either end of the array, both playing to maximise their own total. Decide whether the player who moves first ends up with at least as much as the other.",
        "example_input": "1 5 2",
        "constraints": "Input format: one line of space-separated integers. Output format: \"true\" or \"false\".",
        "solve": _solve_predict_winner,
        "sample_inputs": ["1 5 2", "1 5 233 7"],
        "hidden_inputs": [
            "1",                    # the first player takes everything
            "0",
            "1 2",                  # the first player takes the larger end
            "2 1",
            "1 1",                  # a tie still counts as a win
            "1 2 3",
            "1 5 2 4 6",
            "0 0 0 0",
            "-1 -2 -3",             # negatives
            "2 4 55 6 8",
        ],
    },
{
        "title": "Interleaving String",
        "topic": "dp",
        "difficulty": "hard",
        "description": "Decide whether the third string can be formed by interleaving the first two, keeping the characters of each in their original order.",
        "example_input": "aabcc\ndbbca\naadbbcbcac",
        "constraints": "Input format: line 1 is s1, line 2 is s2, line 3 is s3. Output format: \"true\" or \"false\".",
        "solve": _solve_interleaving_string,
        "sample_inputs": ["aabcc\ndbbca\naadbbcbcac", "aabcc\ndbbca\naadbbbaccc"],
        "hidden_inputs": [
            "a\nb\nab",             # the smallest true case
            "a\nb\nba",             # order may be swapped between strings
            "a\nb\naa",             # a character that is not available
            "a\nb\nabc",            # lengths do not add up
            "ab\ncd\nacbd",
            "ab\ncd\nabdc",
            "aa\naa\naaaa",         # identical strings
            "abc\nabc\naabbcc",
            "abc\ndef\nadbecf",
            "aabc\nabad\naabadabc",
        ],
    },
{
        "title": "Number of Increasing Paths in a Grid",
        "topic": "dp",
        "difficulty": "hard",
        "description": "Count the strictly increasing paths in a grid, moving only between cells that share an edge. A single cell counts as a path. Report the total modulo 1000000007.",
        "example_input": "2 2\n1 1\n3 4",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of integers. Output format: a single integer, the count modulo 1000000007.",
        "solve": _solve_increasing_paths_grid,
        "sample_inputs": ["2 2\n1 1\n3 4", "1 2\n1 2"],
        "hidden_inputs": [
            "1 1\n5",               # one cell, one path
            "1 2\n2 1",
            "1 3\n1 2 3",           # a strictly increasing row
            "2 2\n1 1\n1 1",        # all equal, only the single cells count
            "2 2\n1 2\n3 4",
            "3 1\n3\n2\n1",         # a single decreasing column
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 3\n1 2 3\n4 5 6\n7 8 9",
            "3 3\n9 8 7\n6 5 4\n3 2 1",
            "3 4\n1 2 3 4\n2 3 4 5\n3 4 5 6",
        ],
    },
{
        "title": "Longest Increasing Path in a Matrix",
        "topic": "dp",
        "difficulty": "hard",
        "description": "Return the length of the longest strictly increasing path in a grid, moving only between cells that share an edge. Diagonal moves and wrapping are not allowed.",
        "example_input": "3 3\n9 9 4\n6 6 8\n2 1 1",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of integers. Output format: a single integer.",
        "solve": _solve_longest_increasing_path,
        "sample_inputs": ["3 3\n9 9 4\n6 6 8\n2 1 1", "3 3\n3 4 5\n3 2 6\n2 2 1"],
        "hidden_inputs": [
            "1 1\n1",               # a single cell is a path of length one
            "1 2\n1 2",
            "1 2\n2 1",
            "2 2\n1 1\n1 1",        # all equal, nothing increases
            "2 2\n1 2\n4 3",
            "1 5\n1 2 3 4 5",       # a single increasing row
            "5 1\n5\n4\n3\n2\n1",   # a single decreasing column
            "3 3\n1 2 3\n6 5 4\n7 8 9",   # a snake through the whole grid
            "3 3\n7 8 9\n6 1 2\n5 4 3",
            "4 4\n1 2 3 4\n12 13 14 5\n11 16 15 6\n10 9 8 7",
        ],
    },
{
        "title": "Bomb Enemy",
        "topic": "dp",
        "difficulty": "hard",
        "description": "A grid holds walls marked W, enemies marked E and empty cells marked 0. Placing one bomb in an empty cell kills every enemy in the same row and column until a wall blocks it. Return the most enemies a single bomb can kill.",
        "example_input": "3 4\n0 E 0 0\n E 0 W E\n0 E 0 0",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated cells, each 0, E or W. Output format: a single integer.",
        "solve": _solve_bomb_enemy,
        "sample_inputs": ["3 4\n0 E 0 0\nE 0 W E\n0 E 0 0", "1 3\n0 E 0"],
        "hidden_inputs": [
            "1 1\n0",               # nowhere to place a useful bomb
            "1 1\nE",               # no empty cell at all
            "1 1\nW",
            "1 2\n0 E",             # one enemy in the row
            "2 1\n0\nE",            # one enemy in the column
            "1 3\n0 W E",           # the wall blocks the enemy
            "2 2\nE E\nE 0",
            "3 3\nE E E\nE 0 E\nE E E",   # the centre reaches four enemies
            "3 3\nW W W\nW 0 W\nW W W",   # walls seal the bomb in
            "2 3\n0 E E\nW E 0",
        ],
    },
{
        "title": "Min Cost Climbing Stairs",
        "topic": "dp", "difficulty": "easy",
        "description": "Each step charges a fee when you stand on it. You may start on either the first or the second step, and each move goes up one or two steps. Return the least you can pay to get past the top step.",
        "example_input": "10 15 20",
        "constraints": "Input format: one line of space-separated non-negative fees. Output format: a single integer.",
        "solve": _solve_min_cost_climbing_stairs,
        "sample_inputs": ["10 15 20", "1 100 1 1 1 100 1 1 100 1"],
        "hidden_inputs": [
            "1 1",                  # start on either, pay nothing more
            "0 0",
            "5 1",                  # start on the cheaper step
            "1 5",
            "1 2 3",
            "0 0 0 0",
            "10 1 1 10",
            "1 1 1 1 1",
            "100 1 1 1 100",
            "5 5 5 5 5 5",
        ],
    },
{
        "title": "Fibonacci Number",
        "topic": "dp", "difficulty": "easy",
        "description": "The sequence starts at zero then one, and every later value is the sum of the two before it. Return the value at the given position, counting from zero.",
        "example_input": "4",
        "constraints": "Input format: one line containing the position (at least 0). Output format: a single integer.",
        "solve": _solve_fibonacci,
        "sample_inputs": ["4", "2"],
        "hidden_inputs": [
            "0",                    # the first value
            "1",
            "3",
            "5",
            "10",
            "20",
            "30",
            "45",                   # the largest that fits in signed 32-bit
            "50",
            "70",
        ],
    },
{
        "title": "N-th Tribonacci Number",
        "topic": "dp", "difficulty": "easy",
        "description": "The sequence starts zero, one, one, and every later value is the sum of the three before it. Return the value at the given position, counting from zero.",
        "example_input": "4",
        "constraints": "Input format: one line containing the position (at least 0). Output format: a single integer.",
        "solve": _solve_tribonacci,
        "sample_inputs": ["4", "25"],
        "hidden_inputs": [
            "0",                    # the three seed values
            "1",
            "2",
            "3",                    # the first computed value
            "5",
            "10",
            "20",
            "30",
            "37",                   # the largest that fits in signed 32-bit
            "40",
        ],
    },
{
        "title": "Is Subsequence",
        "topic": "dp", "difficulty": "easy",
        "description": "Decide whether the first string can be obtained from the second by deleting some of its characters without reordering the rest.",
        "example_input": "abc\nahbgdc",
        "constraints": "Input format: line 1 is the candidate, line 2 is the longer string, both lowercase. Output format: \"true\" or \"false\".",
        "solve": _solve_is_subsequence,
        "sample_inputs": ["abc\nahbgdc", "axc\nahbgdc"],
        "hidden_inputs": [
            "a\na",                 # identical
            "a\nb",
            "a\nba",                # a match at the end
            "ab\nba",               # the right letters, the wrong order
            "ab\nab",
            "abc\nab",              # the candidate is longer
            "aa\naba",
            "aaa\naa",
            "ace\nabcde",
            "bb\nbabab",
        ],
    },
{
        "title": "House Robber",
        "topic": "dp", "difficulty": "medium",
        "description": "Houses stand in a row, each holding some money, but two houses next to each other cannot both be emptied. Return the largest sum that can be taken.",
        "example_input": "1 2 3 1",
        "constraints": "Input format: one line of space-separated non-negative amounts. Output format: a single integer.",
        "solve": _solve_house_robber,
        "sample_inputs": ["1 2 3 1", "2 7 9 3 1"],
        "hidden_inputs": [
            "5",                    # a single house
            "0",
            "1 2",                  # take the richer one
            "2 1",
            "1 1 1",                # the two ends beat the middle
            "0 0 0",
            "2 1 1 2",
            "5 1 1 5",
            "100 1 1 100 1",
            "1 2 3 4 5 6 7 8 9",
        ],
    },
{
        "title": "Partition Equal Subset Sum",
        "topic": "dp", "difficulty": "medium",
        "description": "Decide whether the values can be split into two groups adding up to the same total.",
        "example_input": "1 5 11 5",
        "constraints": "Input format: one line of space-separated positive integers. Output format: \"true\" or \"false\".",
        "solve": _solve_partition_equal_subset,
        "sample_inputs": ["1 5 11 5", "1 2 3 5"],
        "hidden_inputs": [
            "1",                    # one value cannot be split
            "2",
            "1 1",                  # the smallest true case
            "1 2",                  # an odd total is hopeless
            "2 2 2",                # an even total that still cannot split
            "1 1 1 1",
            "3 3 3 4 5",
            "1 2 5",
            "100 100",
            "1 2 3 4 5 6 7",
        ],
    },
{
        "title": "Edit Distance",
        "topic": "dp", "difficulty": "hard",
        "description": "Return the fewest single-character insertions, deletions or replacements needed to turn the first string into the second.",
        "example_input": "horse\nros",
        "constraints": "Input format: line 1 and line 2 are the two lowercase strings. Output format: a single integer.",
        "solve": _solve_edit_distance,
        "sample_inputs": ["horse\nros", "intention\nexecution"],
        "hidden_inputs": [
            "a\na",                 # already equal
            "a\nb",                 # one replacement
            "a\nab",                # one insertion
            "ab\na",                # one deletion
            "ab\nba",               # two edits, not one
            "abc\nabc",
            "abc\ndef",             # everything replaced
            "kitten\nsitting",
            "sunday\nsaturday",
            "aaaa\naa",
        ],
    },
{
        "title": "Burst Balloons",
        "topic": "dp", "difficulty": "hard",
        "description": "Bursting a balloon earns its value multiplied by the values of the balloons still standing on either side, treating anything past the ends as one. Burst them all in the best order and return the greatest total.",
        "example_input": "3 1 5 8",
        "constraints": "Input format: one line of space-separated non-negative values. Output format: a single integer.",
        "solve": _solve_burst_balloons,
        "sample_inputs": ["3 1 5 8", "1 5"],
        "hidden_inputs": [
            "1",                    # one balloon
            "0",                    # a zero-valued balloon
            "1 1",
            "2 3",                  # order changes the total
            "3 2",
            "0 0 0",
            "1 2 3",
            "5 1 5",                # the middle should go first
            "9 76 64 21",
            "1 2 3 4 5",
        ],
    },
{
        "title": "Regular Expression Matching",
        "topic": "dp", "difficulty": "hard",
        "description": "Decide whether a pattern matches the whole string, where a dot stands for any single character and a star means the item before it may repeat any number of times, including none.",
        "example_input": "aa\na*",
        "constraints": "Input format: line 1 is the lowercase string, line 2 is the pattern of lowercase letters, dots and stars. Output format: \"true\" or \"false\".",
        "solve": _solve_regex_matching,
        "sample_inputs": ["aa\na*", "ab\n.*"],
        "hidden_inputs": [
            "a\na",                 # a plain match
            "a\nb",
            "a\n.",                 # a dot matches anything
            "a\na*",
            "a\nb*a",               # a star matching nothing
            "aa\na",                # the pattern must cover the whole string
            "aaa\na*a",
            "mississippi\nmis*is*p*.",
            "ab\n.*c",
            "aab\nc*a*b",
        ],
    },
{
        "title": "Distinct Subsequences",
        "topic": "dp", "difficulty": "hard",
        "description": "Count the different ways the second string can be formed by deleting characters from the first without reordering what remains.",
        "example_input": "rabbbit\nrabbit",
        "constraints": "Input format: line 1 is the source string, line 2 is the target, both lowercase. Output format: a single integer.",
        "solve": _solve_distinct_subsequences,
        "sample_inputs": ["rabbbit\nrabbit", "babgbag\nbag"],
        "hidden_inputs": [
            "a\na",                 # exactly one way
            "a\nb",                 # no way at all
            "aa\na",                # two positions give two ways
            "aaa\na",
            "aaa\naa",
            "ab\nab",
            "ab\nba",               # order matters
            "abc\nabc",
            "aaaa\naa",
            "bbbbb\nbb",
        ],
    },
]
