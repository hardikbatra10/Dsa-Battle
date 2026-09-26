"""Heap problems."""

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

def _solve_last_stone_weight(lines):
    import heapq
    stones = [-int(x) for x in lines[0].split()]
    heapq.heapify(stones)
    while len(stones) > 1:
        a = -heapq.heappop(stones)
        b = -heapq.heappop(stones)
        if a != b:
            heapq.heappush(stones, -(a - b))
    return str(-stones[0]) if stones else "0"


def _solve_relative_ranks(lines):
    scores = list(map(int, lines[0].split()))
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    label = {}
    for rank, i in enumerate(order, start=1):
        if rank == 1:
            label[i] = "Gold"
        elif rank == 2:
            label[i] = "Silver"
        elif rank == 3:
            label[i] = "Bronze"
        else:
            label[i] = str(rank)
    return " ".join(label[i] for i in range(len(scores)))


def _solve_sort_by_frequency(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = Counter(nums)
    ordered = sorted(nums, key=lambda v: (counts[v], -v))
    return " ".join(map(str, ordered))


def _solve_take_gifts(lines):
    import heapq
    gifts = [-int(x) for x in lines[0].split()]
    k = int(lines[1])
    heapq.heapify(gifts)
    for _ in range(k):
        top = -heapq.heappop(gifts)
        heapq.heappush(gifts, -int(top ** 0.5))
    return str(-sum(gifts))


def _solve_k_weakest_rows(lines):
    m, n, k = map(int, lines[0].split())
    rows = []
    for i in range(m):
        row = list(map(int, lines[1 + i].split()))
        rows.append((sum(row), i))
    rows.sort()
    return " ".join(str(i) for _, i in rows[:k])


def _solve_k_closest_points(lines):
    n, k = map(int, lines[0].split())
    pts = []
    for i in range(n):
        x, y = map(int, lines[1 + i].split())
        pts.append((x * x + y * y, x, y))
    pts.sort()
    return "\n".join(f"{x} {y}" for _, x, y in pts[:k])


def _solve_reorganize_string(lines):
    s = lines[0]
    from collections import Counter
    counts = Counter(s)
    n = len(s)
    if max(counts.values()) > (n + 1) // 2:
        return ""
    out = []
    prev = ""
    for i in range(n):
        placed = False
        for c in sorted(counts):
            if counts[c] == 0 or c == prev:
                continue
            counts[c] -= 1
            remaining = n - i - 1
            ok = True
            if remaining > 0:
                if max(counts.values()) > (remaining + 1) // 2:
                    ok = False
                elif counts[c] * 2 - 1 == remaining:
                    # c would have to take the very next slot as well
                    ok = False
            if ok:
                out.append(c)
                prev = c
                placed = True
                break
            counts[c] += 1
        if not placed:
            return ""
    return "".join(out)


def _solve_k_smallest_pairs(lines):
    k = int(lines[0])
    a = list(map(int, lines[1].split()))
    b = list(map(int, lines[2].split()))
    pairs = sorted(((x + y, x, y) for x in a for y in b))
    return "\n".join(f"{x} {y}" for _, x, y in pairs[:k])


def _solve_kth_smallest_matrix(lines):
    n, k = map(int, lines[0].split())
    vals = []
    for i in range(n):
        vals.extend(map(int, lines[1 + i].split()))
    vals.sort()
    return str(vals[k - 1])


def _solve_median_stream(lines):
    q = int(lines[0])
    import bisect
    data = []
    out = []
    for i in range(1, q + 1):
        parts = lines[i].split()
        if parts[0] == "add":
            bisect.insort(data, int(parts[1]))
        else:
            n = len(data)
            if n % 2 == 1:
                med = data[n // 2]
            else:
                med = (data[n // 2 - 1] + data[n // 2]) / 2
            out.append(str(int(med)) if med == int(med) else "%.1f" % med)
    return " ".join(out)


def _solve_smallest_range_k_lists(lines):
    k = int(lines[0])
    lists = [list(map(int, lines[1 + i].split())) for i in range(k)]
    import heapq
    heap = [(lst[0], i, 0) for i, lst in enumerate(lists)]
    heapq.heapify(heap)
    high = max(lst[0] for lst in lists)
    best = None
    while True:
        low, li, idx = heapq.heappop(heap)
        if best is None or (high - low) < (best[1] - best[0]) or \
                ((high - low) == (best[1] - best[0]) and low < best[0]):
            best = (low, high)
        if idx + 1 == len(lists[li]):
            break
        nxt = lists[li][idx + 1]
        high = max(high, nxt)
        heapq.heappush(heap, (nxt, li, idx + 1))
    return f"{best[0]} {best[1]}"

def _solve_kth_largest_stream(lines):
    k = int(lines[0])
    nums = list(map(int, lines[1].split())) if lines[1].strip() else []
    q = int(lines[2])
    import heapq
    heap = nums[:]
    heapq.heapify(heap)
    while len(heap) > k:
        heapq.heappop(heap)
    out = []
    for i in range(q):
        v = int(lines[3 + i])
        heapq.heappush(heap, v)
        if len(heap) > k:
            heapq.heappop(heap)
        out.append(str(heap[0]))
    return " ".join(out)


def _solve_max_product_three(lines):
    nums = sorted(map(int, lines[0].split()))
    return str(max(nums[-1] * nums[-2] * nums[-3], nums[0] * nums[1] * nums[-1]))


def _solve_third_maximum(lines):
    distinct = sorted(set(map(int, lines[0].split())), reverse=True)
    return str(distinct[2] if len(distinct) >= 3 else distinct[0])


def _solve_height_checker(lines):
    heights = list(map(int, lines[0].split()))
    expected = sorted(heights)
    return str(sum(1 for a, b in zip(heights, expected) if a != b))


def _solve_connect_sticks(lines):
    import heapq
    sticks = list(map(int, lines[0].split()))
    heapq.heapify(sticks)
    cost = 0
    while len(sticks) > 1:
        a = heapq.heappop(sticks)
        b = heapq.heappop(sticks)
        cost += a + b
        heapq.heappush(sticks, a + b)
    return str(cost)


def _solve_sort_by_frequency(lines):
    s = lines[0]
    from collections import Counter
    counts = Counter(s)
    order = sorted(counts, key=lambda c: (-counts[c], c))
    return "".join(c * counts[c] for c in order)


def _solve_furthest_building(lines):
    heights = list(map(int, lines[0].split()))
    bricks = int(lines[1])
    ladders = int(lines[2])
    import heapq
    used = []
    for i in range(len(heights) - 1):
        gap = heights[i + 1] - heights[i]
        if gap <= 0:
            continue
        heapq.heappush(used, gap)
        if len(used) > ladders:
            bricks -= heapq.heappop(used)
            if bricks < 0:
                return str(i)
    return str(len(heights) - 1)


def _solve_seat_manager(lines):
    n = int(lines[0])
    q = int(lines[1])
    import heapq
    free = list(range(1, n + 1))
    heapq.heapify(free)
    out = []
    for i in range(2, 2 + q):
        parts = lines[i].split()
        if parts[0] == "reserve":
            out.append(str(heapq.heappop(free)))
        else:
            heapq.heappush(free, int(parts[1]))
    return " ".join(out)


def _solve_max_coins_piles(lines):
    piles = sorted(map(int, lines[0].split()))
    n = len(piles) // 3
    total = 0
    i = len(piles) - 2
    for _ in range(n):
        total += piles[i]
        i -= 2
    return str(total)


def _solve_least_unique_after_k(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import Counter
    counts = sorted(Counter(nums).values())
    removed = 0
    for i, c in enumerate(counts):
        if k >= c:
            k -= c
            removed += 1
        else:
            break
    return str(len(counts) - removed)


def _solve_sort_an_array(lines):
    import heapq
    nums = list(map(int, lines[0].split()))
    heapq.heapify(nums)
    return " ".join(str(heapq.heappop(nums)) for _ in range(len(nums)))


def _solve_top_k_frequent_words(lines):
    k = int(lines[0])
    n = int(lines[1])
    words = [lines[2 + i] for i in range(n)]
    from collections import Counter
    counts = Counter(words)
    order = sorted(counts, key=lambda w: (-counts[w], w))
    return " ".join(order[:k])


def _solve_sliding_window_median(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    import bisect
    window = sorted(nums[:k])
    out = []

    def median():
        if k % 2 == 1:
            m = window[k // 2]
        else:
            m = (window[k // 2 - 1] + window[k // 2]) / 2
        return str(int(m)) if m == int(m) else "%.1f" % m

    out.append(median())
    for i in range(k, len(nums)):
        window.pop(bisect.bisect_left(window, nums[i - k]))
        bisect.insort(window, nums[i])
        out.append(median())
    return " ".join(out)


def _solve_skyline(lines):
    k = int(lines[0])
    buildings = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    import heapq
    events = []
    for left, right, height in buildings:
        events.append((left, -height, right))
        events.append((right, 0, 0))
    events.sort()
    out = []
    live = [(0, float("inf"))]
    for x, negative_height, right in events:
        while live[0][1] <= x:
            heapq.heappop(live)
        if negative_height:
            heapq.heappush(live, (negative_height, right))
        current = -live[0][0]
        if not out or out[-1][1] != current:
            out.append((x, current))
    return "\n".join(f"{x} {h}" for x, h in out)


def _solve_trapping_rain_water_ii(lines):
    m, n = map(int, lines[0].split())
    grid = [list(map(int, lines[1 + i].split())) for i in range(m)]
    if m < 3 or n < 3:
        return "0"
    import heapq
    heap = []
    seen = [[False] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if i in (0, m - 1) or j in (0, n - 1):
                heapq.heappush(heap, (grid[i][j], i, j))
                seen[i][j] = True
    total = 0
    while heap:
        height, i, j = heapq.heappop(heap)
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and not seen[ni][nj]:
                seen[ni][nj] = True
                total += max(0, height - grid[ni][nj])
                heapq.heappush(heap, (max(height, grid[ni][nj]), ni, nj))
    return str(total)


def _solve_max_team_performance(lines):
    n, k = map(int, lines[0].split())
    speed = list(map(int, lines[1].split()))
    efficiency = list(map(int, lines[2].split()))
    import heapq
    MOD = 10 ** 9 + 7
    workers = sorted(zip(efficiency, speed), reverse=True)
    heap = []
    total = 0
    best = 0
    for eff, spd in workers:
        heapq.heappush(heap, spd)
        total += spd
        if len(heap) > k:
            total -= heapq.heappop(heap)
        best = max(best, total * eff)
    return str(best % MOD)


def _solve_max_events_ii(lines):
    k = int(lines[0])
    events = sorted(tuple(map(int, lines[1 + i].split())) for i in range(k))
    limit = int(lines[1 + k])
    import bisect
    starts = [e[0] for e in events]
    from functools import lru_cache

    @lru_cache(None)
    def go(i, left):
        if i >= k or left == 0:
            return 0
        skip = go(i + 1, left)
        nxt = bisect.bisect_right(starts, events[i][1])
        take = events[i][2] + go(nxt, left - 1)
        return max(skip, take)

    return str(go(0, limit))


def _solve_single_threaded_cpu(lines):
    k = int(lines[0])
    tasks = [tuple(map(int, lines[1 + i].split())) + (i,) for i in range(k)]
    tasks.sort()
    import heapq
    heap = []
    out = []
    time = 0
    i = 0
    while i < k or heap:
        if not heap and time < tasks[i][0]:
            time = tasks[i][0]
        while i < k and tasks[i][0] <= time:
            heapq.heappush(heap, (tasks[i][1], tasks[i][2]))
            i += 1
        duration, index = heapq.heappop(heap)
        time += duration
        out.append(str(index))
    return " ".join(out)


def _solve_swim_in_rising_water(lines):
    n = int(lines[0].split()[0])
    grid = [list(map(int, lines[1 + i].split())) for i in range(n)]
    import heapq
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}
    best = 0
    while heap:
        height, i, j = heapq.heappop(heap)
        best = max(best, height)
        if (i, j) == (n - 1, n - 1):
            return str(best)
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and (ni, nj) not in seen:
                seen.add((ni, nj))
                heapq.heappush(heap, (grid[ni][nj], ni, nj))
    return "-1"


PROBLEMS = [
{
        "title": "Kth Largest Element in an Array",
        "topic": "heap",
        "difficulty": "easy",
        "description": "Given an integer array nums and an integer k, return the kth largest element (not the kth distinct element).",
        "example_input": "2\n3 2 1 5 6 4",
        "constraints": "Input format: line 1 is k, line 2 is the space-separated array. Output format: a single integer.",
        "solve": _solve_kth_largest,
        "sample_inputs": ["2\n3 2 1 5 6 4", "3\n7 10 4 3 20 15"],
        "hidden_inputs": [
            "1\n1",          # single element
            "1\n5 5 5",
            "2\n-1 -1",      # negatives with duplicates
            "3\n3 3 3 3 3",  # kth largest, not kth distinct
            "1\n-1 -2 -3",
            "1\n7 6 5 4",
            "5\n1 2 3 4 5",  # k equals the array length, so the minimum
            "4\n3 2 3 1 2 4 5 5 6",
            "6\n10 9 8 7 6 5 4",
        ],
    },
{
        "title": "Top K Frequent Elements",
        "topic": "heap",
        "difficulty": "medium",
        "description": "Given an integer array nums and an integer k, return the k most frequent elements, ordered by frequency (descending), ties broken by which value appeared first in the input.",
        "example_input": "2\n1 1 1 2 2 3",
        "constraints": "Input format: line 1 is k, line 2 is the space-separated array. Output format: space-separated top-k elements.",
        "solve": _solve_top_k_frequent,
        "sample_inputs": ["2\n1 1 1 2 2 3", "2\n3 0 1 0"],
        "hidden_inputs": [
            "1\n1",            # single element
            "1\n-1 -1 -2",
            "1\n2 2 1 1 1",
            "1\n1 1 2 2 3",    # frequency tie broken by first appearance
            "2\n5 5 4 4 3 3",  # every value ties
            "3\n1 2 3",        # all frequencies are 1
            "3\n4 4 4 6 6 2 2 2 2",
            "4\n1 1 1 1 2 2 2 3 3 4",
        ],
    },
{
        "title": "Merge K Sorted Lists",
        "topic": "heap",
        "difficulty": "hard",
        "description": "Given k sorted arrays, merge them into one fully sorted array.",
        "example_input": "3\n1 4 5\n1 3 4\n2 6",
        "constraints": "Input format: line 1 is k, followed by k lines each a sorted space-separated array. Output format: the merged sorted array, space-separated.",
        "solve": _solve_merge_k_lists,
        "sample_inputs": ["3\n1 4 5\n1 3 4\n2 6", "2\n2 4\n1 3 5"],
        "hidden_inputs": [
            "1\n1",                 # a single one-element list
            "2\n1\n1",
            "2\n-5 -5 -5\n-5 -5",   # duplicates across lists
            "3\n1 2 3\n\n4 5",      # one of the lists is empty
            "2\n1 1 1\n1 1 1",
            "2\n1 2 3\n4 5 6",      # disjoint ranges
            "3\n-3 -1\n-2 0\n1 2",  # negatives interleaving
            "4\n1\n2\n3\n4",
            "2\n1 3 5 7 9\n2 4 6 8 10",
            "5\n1\n2\n3\n4\n5",
        ],
    },
{
        "title": "Last Stone Weight",
        "topic": "heap",
        "difficulty": "easy",
        "description": "Repeatedly take the two heaviest stones and smash them together: if they weigh the same both are destroyed, otherwise the lighter is destroyed and the heavier loses that weight. Return the weight of the stone left at the end, or 0 if none remains.",
        "example_input": "2 7 4 1 8 1",
        "constraints": "Input format: one line of space-separated positive weights. Output format: a single integer.",
        "solve": _solve_last_stone_weight,
        "sample_inputs": ["2 7 4 1 8 1", "1"],
        "hidden_inputs": [
            "5",                    # a single stone survives untouched
            "2 2",                  # equal stones annihilate
            "3 1",                  # the difference remains
            "1 3",                  # order of the input must not matter
            "1 1 1",                # two cancel, one survives
            "1 1 1 1",              # everything cancels
            "10 4 2 10",
            "7 6 7 6 9",
            "2 2 2 2 2 2",
            "1 2 4 8 16",           # each smash leaves a smaller stone
        ],
    },
{
        "title": "Relative Ranks",
        "topic": "heap",
        "difficulty": "easy",
        "description": "Athletes are scored, all scores different. The top three receive Gold, Silver and Bronze; everyone else receives their placing as a number. Report the result for each athlete in the order they were given.",
        "example_input": "5 4 3 2 1",
        "constraints": "Input format: one line of space-separated distinct scores. Output format: one entry per athlete in input order, space-separated, each either Gold, Silver, Bronze or a placing number.",
        "solve": _solve_relative_ranks,
        "sample_inputs": ["5 4 3 2 1", "10 3 8 9 4"],
        "hidden_inputs": [
            "1",                    # one athlete takes Gold
            "1 2",                  # only two medals awarded
            "2 1",
            "1 2 3",                # exactly three medals
            "3 2 1",
            "1 2 3 4",              # the fourth gets a number
            "4 3 2 1",
            "-1 -2 -3",             # negative scores still rank
            "100 50 75 25 60",
            "7 1 9 3 5 2",
        ],
    },
{
        "title": "Sort Array by Increasing Frequency",
        "topic": "heap",
        "difficulty": "easy",
        "description": "Rearrange the values so that those occurring less often come first. Values occurring equally often are placed in decreasing order of value.",
        "example_input": "1 1 2 2 2 3",
        "constraints": "Input format: one line of space-separated integers. Output format: the rearranged values, space-separated.",
        "solve": _solve_sort_by_frequency,
        "sample_inputs": ["1 1 2 2 2 3", "2 3 1 3 2"],
        "hidden_inputs": [
            "1",                    # a single value
            "1 1",                  # one group
            "1 2",                  # a tie broken by decreasing value
            "2 1",
            "1 1 2",
            "5 5 5 5",
            "-1 1 -6 4 5 -6 1 4 1",
            "1 2 3 4 5",            # every value ties at one occurrence
            "3 3 2 2 1 1",          # every value ties at two
            "9 9 9 8 8 7",
        ],
    },
{
        "title": "Take Gifts From the Richest Pile",
        "topic": "heap",
        "difficulty": "easy",
        "description": "For a given number of turns, take the largest pile and leave behind only the whole part of its square root. Return how many gifts remain in total afterwards.",
        "example_input": "25 64 9 4 100\n4",
        "constraints": "Input format: line 1 is the space-separated pile sizes, line 2 is the number of turns. Output format: a single integer.",
        "solve": _solve_take_gifts,
        "sample_inputs": ["25 64 9 4 100\n4", "1 1 1 1\n4"],
        "hidden_inputs": [
            "1\n1",                 # the root of one is one
            "4\n1",
            "4\n2",                 # a second turn on the same pile
            "9\n1",
            "0\n3",                 # zero stays zero
            "2\n1",                 # the root is not exact
            "25 64 9 4 100\n1",
            "25 64 9 4 100\n0",     # no turns at all
            "100 100 100\n3",       # each pile reduced once
            "1000000\n5",
        ],
    },
{
        "title": "K Weakest Rows in a Matrix",
        "topic": "heap",
        "difficulty": "easy",
        "description": "Each row of a grid holds soldiers marked 1 before civilians marked 0. A row is weaker than another when it has fewer soldiers, or when it has the same number but sits higher up. Return the indices of the k weakest rows, weakest first.",
        "example_input": "5 5 3\n1 1 0 0 0\n1 1 1 1 0\n1 0 0 0 0\n1 1 0 0 0\n1 1 1 1 1",
        "constraints": "Input format: line 1 is \"rows cols k\", followed by that many rows of space-separated 0 and 1 values. Output format: the row indices, space-separated.",
        "solve": _solve_k_weakest_rows,
        "sample_inputs": ["5 5 3\n1 1 0 0 0\n1 1 1 1 0\n1 0 0 0 0\n1 1 0 0 0\n1 1 1 1 1", "4 4 2\n1 0 0 0\n1 1 1 1\n1 0 0 0\n1 1 0 0"],
        "hidden_inputs": [
            "1 1 1\n0",             # a single empty row
            "1 1 1\n1",
            "2 2 1\n0 0\n1 1",      # the empty row is weakest
            "2 2 2\n1 1\n0 0",
            "2 2 1\n1 0\n1 0",      # a tie broken by position
            "3 3 3\n1 1 1\n1 1 1\n1 1 1",   # every row identical
            "3 3 2\n0 0 0\n0 0 0\n1 1 1",
            "3 2 1\n1 1\n1 0\n0 0",
            "4 4 4\n1 1 1 1\n1 1 1 0\n1 1 0 0\n1 0 0 0",
            "5 3 2\n1 0 0\n1 1 1\n0 0 0\n1 1 0\n1 0 0",
        ],
    },
{
        "title": "K Closest Points to Origin",
        "topic": "heap",
        "difficulty": "medium",
        "description": "Return the k points lying nearest the origin, measured by ordinary straight-line distance. List them closest first, breaking ties by smaller x and then smaller y.",
        "example_input": "2 1\n1 3\n-2 2",
        "constraints": "Input format: line 1 is \"n k\", followed by n lines each \"x y\". Output format: one point per line as \"x y\".",
        "solve": _solve_k_closest_points,
        "sample_inputs": ["2 1\n1 3\n-2 2", "4 2\n3 3\n5 -1\n-2 4\n0 1"],
        "hidden_inputs": [
            "1 1\n0 0",             # the origin itself
            "1 1\n5 5",
            "2 2\n1 0\n0 1",        # a tie broken by x
            "2 1\n1 0\n0 1",
            "3 3\n1 1\n2 2\n3 3",   # every point returned
            "3 1\n-1 0\n1 0\n0 1",  # negatives tie with positives
            "4 2\n1 1\n-1 -1\n2 0\n0 2",
            "4 1\n10 10\n1 1\n5 5\n2 2",
            "5 3\n0 1\n0 2\n0 3\n0 4\n0 5",
            "3 2\n-3 0\n0 -3\n1 1",
        ],
    },
{
        "title": "Reorganize String",
        "topic": "heap",
        "difficulty": "medium",
        "description": "Rearrange the letters of the string so that no two neighbouring letters are the same. If several rearrangements work, return the one that comes first alphabetically. Return nothing if it cannot be done.",
        "example_input": "aab",
        "constraints": "Input format: one line containing the lowercase string. Output format: the rearranged string, or an empty line if impossible.",
        "solve": _solve_reorganize_string,
        "sample_inputs": ["aab", "aaab"],
        "hidden_inputs": [
            "a",                    # a single letter
            "aa",                   # impossible
            "ab",                   # already fine
            "ba",                   # must be reordered to the smaller one
            "aabb",
            "aaabb",                # the tightest feasible case
            "aaaabb",               # one letter too many
            "vvvlo",
            "abbabb",
            "zzyyx",
        ],
    },
{
        "title": "Find K Pairs with Smallest Sums",
        "topic": "heap",
        "difficulty": "medium",
        "description": "Form pairs by taking one value from each of two lists. Return the k pairs with the smallest sums, ordered by sum and then by the first and second value.",
        "example_input": "3\n1 7 11\n2 4 6",
        "constraints": "Input format: line 1 is k, line 2 and line 3 are the two space-separated lists. Output format: one pair per line as \"a b\"; if fewer than k pairs exist, list them all.",
        "solve": _solve_k_smallest_pairs,
        "sample_inputs": ["3\n1 7 11\n2 4 6", "2\n1 1 2\n1 2 3"],
        "hidden_inputs": [
            "1\n1\n1",              # one pair only
            "5\n1\n1",              # k exceeds the number of pairs
            "2\n1 2\n3",            # one list has a single value
            "4\n1 2\n3 4",          # every pair returned
            "1\n1 2\n3 4",
            "3\n1 1 1\n1 1 1",      # every sum identical
            "3\n-1 0 1\n-1 0 1",    # negatives
            "2\n1 7 11\n2 4 6",
            "6\n1 2 3\n4 5 6",
            "3\n0 0\n0 0",
        ],
    },
{
        "title": "Kth Smallest Element in a Sorted Matrix",
        "topic": "heap",
        "difficulty": "medium",
        "description": "Every row and every column of a square grid is in non-decreasing order. Return the kth smallest value in the whole grid, counting repeats separately.",
        "example_input": "3 8\n1 5 9\n10 11 13\n12 13 15",
        "constraints": "Input format: line 1 is \"n k\", followed by n lines each holding n integers. Output format: a single integer.",
        "solve": _solve_kth_smallest_matrix,
        "sample_inputs": ["3 8\n1 5 9\n10 11 13\n12 13 15", "2 2\n1 2\n1 3"],
        "hidden_inputs": [
            "1 1\n5",               # the only value
            "2 1\n1 2\n3 4",        # the smallest
            "2 4\n1 2\n3 4",        # the largest
            "2 2\n1 1\n1 1",        # every value identical
            "2 3\n1 1\n1 1",
            "3 1\n1 2 3\n4 5 6\n7 8 9",
            "3 9\n1 2 3\n4 5 6\n7 8 9",
            "3 5\n1 2 3\n4 5 6\n7 8 9",   # the exact middle
            "3 4\n-5 -4 -3\n-2 -1 0\n1 2 3",   # negatives
            "4 7\n1 3 5 7\n2 4 6 8\n3 5 7 9\n4 6 8 10",
        ],
    },
{
        "title": "Find Median from Data Stream",
        "topic": "heap",
        "difficulty": "hard",
        "description": "Numbers arrive one at a time and the middle value may be asked for at any point. When an even count has arrived the middle is the average of the two central values. Report the answer to every request in order.",
        "example_input": "5\nadd 1\nadd 2\nmedian\nadd 3\nmedian",
        "constraints": "Input format: line 1 is the number of operations, followed by that many lines each \"add x\" or \"median\". Output format: the answers space-separated, each printed as a whole number when exact and otherwise with one decimal place.",
        "solve": _solve_median_stream,
        "sample_inputs": ["5\nadd 1\nadd 2\nmedian\nadd 3\nmedian", "3\nadd 5\nadd 5\nmedian"],
        "hidden_inputs": [
            "2\nadd 1\nmedian",             # a single value
            "1\nadd 1",                     # no request at all, empty output
            "3\nadd 1\nadd 2\nmedian",      # an average ending in .5
            "3\nadd 2\nadd 1\nmedian",      # arrival order must not matter
            "4\nadd 1\nmedian\nadd 3\nmedian",
            "5\nadd -1\nadd -2\nadd -3\nmedian\nmedian",   # negatives, repeated request
            "6\nadd 1\nadd 2\nadd 3\nadd 4\nmedian\nadd 5",
            "7\nadd 5\nadd 1\nadd 3\nmedian\nadd 2\nadd 4\nmedian",
            "5\nadd 0\nadd 0\nmedian\nadd 0\nmedian",
            "8\nadd 6\nadd 10\nadd 2\nmedian\nadd 6\nmedian\nadd 5\nmedian",
        ],
    },
{
        "title": "Smallest Range Covering Elements from K Lists",
        "topic": "heap",
        "difficulty": "hard",
        "description": "Given several lists of numbers, each already in increasing order, find the shortest span of values that contains at least one number from every list. If several spans are equally short, return the one that starts lowest.",
        "example_input": "3\n4 10 15 24 26\n0 9 12 20\n5 18 22 30",
        "constraints": "Input format: line 1 is the number of lists, followed by that many lines each a space-separated increasing list. Output format: the span as \"low high\".",
        "solve": _solve_smallest_range_k_lists,
        "sample_inputs": ["3\n4 10 15 24 26\n0 9 12 20\n5 18 22 30", "3\n1 2 3\n1 2 3\n1 2 3"],
        "hidden_inputs": [
            "1\n1",                 # one list, one value
            "1\n1 2 3",             # one list, the smallest span is a point
            "2\n1\n1",              # both lists share a value
            "2\n1\n2",
            "2\n1 2\n3 4",
            "2\n1 5\n2 6",
            "3\n1 1 1\n1 1 1\n1 1 1",   # everything identical
            "2\n-5 -1\n-3 0",       # negatives
            "3\n10 20 30\n11 21 31\n12 22 32",
            "2\n1 2 3 4 5\n5",      # one list pins the span
        ],
    },
{
        "title": "Kth Largest Element in a Stream",
        "topic": "heap", "difficulty": "easy",
        "description": "Values arrive one at a time on top of a starting list. After each arrival, report the kth largest value seen so far, counting repeats separately.",
        "example_input": "3\n4 5 8 2\n4\n3\n5\n10\n9",
        "constraints": "Input format: line 1 is k, line 2 is the starting values, line 3 is the number of arrivals, followed by that many lines each one value. At least k values exist after the first arrival. Output format: one answer per arrival, space-separated.",
        "solve": _solve_kth_largest_stream,
        "sample_inputs": ["3\n4 5 8 2\n4\n3\n5\n10\n9", "1\n5\n2\n1\n9"],
        "hidden_inputs": [
            "1\n1\n1\n2",            # the largest so far
            "1\n5\n1\n1",
            "2\n1 2\n1\n3",
            "2\n2 2\n2\n2\n2",       # repeats count separately
            "3\n1 2 3\n1\n4",
            "3\n5 5 5\n2\n5\n5",
            "1\n0\n3\n-1\n-2\n-3",   # negatives
            "2\n1 1\n3\n1\n1\n1",
            "4\n1 2 3 4\n2\n5\n0",
            "3\n10 9 8 7 6\n3\n5\n11\n12",
        ],
    },
{
        "title": "Maximum Product of Three Numbers",
        "topic": "heap", "difficulty": "easy",
        "description": "Return the largest product obtainable by multiplying three of the given values together.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line of at least three space-separated integers. Output format: a single integer.",
        "solve": _solve_max_product_three,
        "sample_inputs": ["1 2 3", "-1 -2 -3"],
        "hidden_inputs": [
            "1 2 3 4",
            "0 0 0",                # zeroes
            "-1 -2 3",              # two negatives beat three positives
            "-100 -98 -1 2 3",
            "1 2 3 -4",
            "-4 -3 -2 -1",          # all negative, take the three largest
            "5 5 5 5",
            "0 -1 -2 -3",
            "1 1 1 1 1",
            "-10 -10 1 3 2",
        ],
    },
{
        "title": "Third Maximum Number",
        "topic": "heap", "difficulty": "easy",
        "description": "Return the third largest different value in the list. If fewer than three different values exist, return the largest instead.",
        "example_input": "3 2 1",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_third_maximum,
        "sample_inputs": ["3 2 1", "1 2"],
        "hidden_inputs": [
            "1",                    # only one value
            "1 1",                  # only one different value
            "2 2 3 1",              # repeats do not count separately
            "1 2 3",
            "3 2 1 0",
            "1 1 2",
            "-1 -2 -3",             # negatives
            "5 5 5 5",
            "2 2 3 1 4",
            "1 2 2 5 3 5",
        ],
    },
{
        "title": "Height Checker",
        "topic": "heap", "difficulty": "easy",
        "description": "Compare the row of heights against the same heights arranged in non-decreasing order, and count the positions where the two differ.",
        "example_input": "1 1 4 2 1 3",
        "constraints": "Input format: one line of space-separated positive heights. Output format: a single integer.",
        "solve": _solve_height_checker,
        "sample_inputs": ["1 1 4 2 1 3", "5 1 2 3 4"],
        "hidden_inputs": [
            "1",                    # already in order
            "1 1",
            "2 1",                  # both positions differ
            "1 2",
            "1 1 1 1",
            "1 2 3 4",
            "4 3 2 1",
            "2 1 2 1",
            "5 5 1 1",
            "1 3 2 4 5",
        ],
    },
{
        "title": "Minimum Cost to Connect Sticks",
        "topic": "heap", "difficulty": "medium",
        "description": "Joining two sticks costs the total of their lengths and leaves one stick of that length. Return the least it can cost to join them all into one.",
        "example_input": "2 4 3",
        "constraints": "Input format: one line of space-separated positive lengths. Output format: a single integer.",
        "solve": _solve_connect_sticks,
        "sample_inputs": ["2 4 3", "1 8 3 5"],
        "hidden_inputs": [
            "5",                    # nothing to join
            "1 1",                  # one join
            "1 2",
            "1 1 1",
            "1 1 1 1",
            "5 5 5 5",
            "1 2 3 4",
            "1 100 100",            # joining the small ones first matters
            "10 1 1 1",
            "2 2 3 3",
        ],
    },
{
        "title": "Sort Characters By Frequency",
        "topic": "heap", "difficulty": "medium",
        "description": "Rearrange the string so the letters occurring most often come first, keeping equal letters together. Letters occurring equally often are placed in alphabetical order.",
        "example_input": "tree",
        "constraints": "Input format: one line containing the string of letters. Output format: the rearranged string.",
        "solve": _solve_sort_by_frequency,
        "sample_inputs": ["tree", "cccaaa"],
        "hidden_inputs": [
            "a",                    # a single letter
            "aa",
            "ab",                   # a tie broken alphabetically
            "ba",
            "aab",
            "abb",
            "aabbcc",               # every letter ties
            "Aabb",                 # capitals sort before lower case
            "abcabc",
            "zzyyx",
        ],
    },
{
        "title": "Furthest Building You Can Reach",
        "topic": "heap", "difficulty": "medium",
        "description": "Moving to a taller building costs either a ladder or as many bricks as the height difference; moving to one no taller is free. Starting at the first building, return the furthest position reachable.",
        "example_input": "4 2 7 6 9 14 12\n5\n1",
        "constraints": "Input format: line 1 is the space-separated heights, line 2 is the number of bricks, line 3 is the number of ladders. Output format: a single integer counting from zero.",
        "solve": _solve_furthest_building,
        "sample_inputs": ["4 2 7 6 9 14 12\n5\n1", "4 12 2 7 3 18 20 3 19\n10\n2"],
        "hidden_inputs": [
            "1\n0\n0",              # already at the end
            "1 2\n0\n0",            # cannot climb at all
            "1 2\n1\n0",            # bricks just suffice
            "1 2\n0\n1",            # a ladder instead
            "2 1\n0\n0",            # going down is free
            "1 1 1\n0\n0",
            "1 5 1 5\n4\n0",
            "1 5 1 5\n0\n2",
            "1 2 3 4 5\n10\n0",
            "14 3 19 3\n17\n0",
        ],
    },
{
        "title": "Seat Reservation Manager",
        "topic": "heap", "difficulty": "medium",
        "description": "Seats numbered from one are all free to begin with. Reserving takes the lowest-numbered free seat, and unreserving puts a seat back. Report the seat given out by each reservation.",
        "example_input": "5\n6\nreserve\nreserve\nunreserve 2\nreserve\nreserve\nreserve",
        "constraints": "Input format: line 1 is the number of seats, line 2 is the number of operations, followed by that many lines each \"reserve\" or \"unreserve x\". Output format: one seat number per reservation, space-separated.",
        "solve": _solve_seat_manager,
        "sample_inputs": ["5\n6\nreserve\nreserve\nunreserve 2\nreserve\nreserve\nreserve", "1\n1\nreserve"],
        "hidden_inputs": [
            "1\n2\nreserve\nunreserve 1",       # freed but never retaken
            "1\n3\nreserve\nunreserve 1\nreserve",
            "2\n2\nreserve\nreserve",
            "2\n3\nreserve\nunreserve 1\nreserve",
            "3\n3\nreserve\nreserve\nreserve",
            "3\n5\nreserve\nreserve\nunreserve 1\nreserve\nreserve",
            "5\n1\nreserve",
            "5\n4\nreserve\nreserve\nunreserve 2\nreserve",
            "4\n6\nreserve\nreserve\nreserve\nunreserve 2\nunreserve 1\nreserve",
            "2\n4\nreserve\nunreserve 1\nreserve\nreserve",
        ],
    },
{
        "title": "Maximum Number of Coins You Can Get",
        "topic": "heap", "difficulty": "medium",
        "description": "The piles are split into groups of three. From each group the largest pile goes to one friend, the middle to you and the smallest to another friend. Arrange the groups to collect as much as possible, and return that total.",
        "example_input": "2 4 1 2 7 8",
        "constraints": "Input format: one line of space-separated pile sizes, a multiple of three of them. Output format: a single integer.",
        "solve": _solve_max_coins_piles,
        "sample_inputs": ["2 4 1 2 7 8", "2 4 5"],
        "hidden_inputs": [
            "1 1 1",                # every pile identical
            "1 2 3",                # one group
            "3 2 1",                # order must not matter
            "0 0 0",
            "1 1 1 1 1 1",
            "1 2 3 4 5 6",
            "9 8 7 6 5 1 2 3 4",
            "2 2 2 2 2 2",
            "1 100 1 1 100 1",
            "5 5 5 5 5 5 5 5 5",
        ],
    },
{
        "title": "Least Number of Unique Integers after K Removals",
        "topic": "heap", "difficulty": "medium",
        "description": "Remove exactly k values from the list, chosen however you like, so that as few different values as possible remain. Return how many different values are left.",
        "example_input": "5 5 4\n1",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: a single integer.",
        "solve": _solve_least_unique_after_k,
        "sample_inputs": ["5 5 4\n1", "4 3 1 1 3 3 2\n3"],
        "hidden_inputs": [
            "1\n0",                 # nothing removed
            "1\n1",                 # the only value goes
            "1 2\n1",
            "1 1\n1",               # one copy left, still one value
            "1 1\n2",
            "1 2 3\n0",
            "1 2 3\n3",
            "1 1 2 2 3\n2",
            "5 5 5 1 2\n2",         # removing the rare values first
            "2 4 1 8 3 5 1 3\n3",
        ],
    },
{
        "title": "Sort an Array",
        "topic": "heap", "difficulty": "medium",
        "description": "Arrange the values in non-decreasing order without using any built-in sorting routine.",
        "example_input": "5 2 3 1",
        "constraints": "Input format: one line of space-separated integers. Output format: the sorted values, space-separated.",
        "solve": _solve_sort_an_array,
        "sample_inputs": ["5 2 3 1", "5 1 1 2 0 0"],
        "hidden_inputs": [
            "1",                    # nothing to do
            "2 1",
            "1 2",
            "1 1 1",
            "3 2 1",                # fully reversed
            "-1 -2 -3",             # negatives
            "0 0 0 0",
            "5 4 3 2 1 0",
            "-5 3 -1 0 2",
            "9 8 7 6 5 4 3 2 1 0",
        ],
    },
{
        "title": "Top K Frequent Words",
        "topic": "heap", "difficulty": "medium",
        "description": "Return the k words that occur most often, most frequent first. Words occurring equally often are placed in alphabetical order.",
        "example_input": "2\n4\ni\nlove\nleetcode\ni",
        "constraints": "Input format: line 1 is k, line 2 is the number of words, followed by that many lowercase words. Output format: the k words, space-separated.",
        "solve": _solve_top_k_frequent_words,
        "sample_inputs": ["2\n4\ni\nlove\nleetcode\ni", "4\n6\nthe\nday\nis\nsunny\nthe\nthe"],
        "hidden_inputs": [
            "1\n1\na",              # a single word
            "1\n2\na\nb",           # a tie broken alphabetically
            "2\n2\na\nb",
            "1\n2\nb\na",
            "1\n3\na\na\nb",
            "2\n4\na\na\nb\nb",
            "3\n3\nc\nb\na",
            "2\n5\nz\nz\ny\ny\nx",
            "1\n4\naa\nab\naa\nab",
            "3\n6\nthe\nthe\nthe\na\na\nb",
        ],
    },
{
        "title": "Sliding Window Median",
        "topic": "heap", "difficulty": "hard",
        "description": "Slide a window of the given size along the values one position at a time and report the middle value of each window. When the window holds an even count, the middle is the average of the two central values.",
        "example_input": "1 3 -1 -3 5 3 6 7\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is the window size. Output format: one median per window, space-separated, each printed as a whole number when exact and otherwise to one decimal.",
        "solve": _solve_sliding_window_median,
        "sample_inputs": ["1 3 -1 -3 5 3 6 7\n3", "1 2 3 4 2 3 1 4 2\n3"],
        "hidden_inputs": [
            "1\n1",                 # a window of one
            "1 2\n1",
            "1 2\n2",               # an average ending in .5
            "1 3\n2",
            "2 2\n2",
            "1 1 1\n2",
            "1 2 3 4\n2",
            "1 2 3 4\n4",           # one window covering everything
            "-1 -2 -3\n2",          # negatives
            "5 5 5 5 5\n3",
        ],
    },
{
        "title": "The Skyline Problem",
        "topic": "heap", "difficulty": "hard",
        "description": "Buildings are rectangles standing on a line, each given by its left edge, right edge and height. Report the outline of their silhouette as the points where its height changes, from left to right.",
        "example_input": "5\n2 9 10\n3 7 15\n5 12 12\n15 20 10\n19 24 8",
        "constraints": "Input format: line 1 is the number of buildings, followed by that many lines each \"left right height\". Output format: one point per line as \"x height\".",
        "solve": _solve_skyline,
        "sample_inputs": ["5\n2 9 10\n3 7 15\n5 12 12\n15 20 10\n19 24 8", "1\n0 2 3"],
        "hidden_inputs": [
            "1\n1 2 1",             # a single building
            "2\n1 2 1\n3 4 1",      # two separate buildings
            "2\n1 3 1\n2 4 1",      # overlapping at the same height
            "2\n1 4 2\n2 3 1",      # one fully inside a taller one
            "2\n1 4 1\n2 3 2",      # a taller one poking out
            "2\n1 2 1\n2 3 1",      # touching at an edge
            "2\n1 2 1\n2 3 2",
            "3\n1 5 3\n2 4 5\n3 6 2",
            "2\n0 5 5\n0 5 5",      # identical buildings
            "3\n1 2 1\n1 2 2\n1 2 3",
        ],
    },
{
        "title": "Trapping Rain Water II",
        "topic": "heap", "difficulty": "hard",
        "description": "A grid gives the height of the ground at each point. After rain, water settles wherever it cannot run off the edge. Return the total volume held.",
        "example_input": "3 6\n1 4 3 1 3 2\n3 2 1 3 2 4\n2 3 3 2 3 1",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of non-negative heights. Output format: a single integer.",
        "solve": _solve_trapping_rain_water_ii,
        "sample_inputs": ["3 6\n1 4 3 1 3 2\n3 2 1 3 2 4\n2 3 3 2 3 1", "5 5\n3 3 3 3 3\n3 2 2 2 3\n3 2 1 2 3\n3 2 2 2 3\n3 3 3 3 3"],
        "hidden_inputs": [
            "1 1\n5",               # nothing can be held
            "1 3\n1 0 1",           # too thin to hold water
            "3 1\n1\n0\n1",
            "2 2\n1 1\n1 1",
            "3 3\n1 1 1\n1 0 1\n1 1 1",     # a single pit
            "3 3\n1 1 1\n1 1 1\n1 1 1",     # flat, holds nothing
            "3 3\n5 5 5\n5 0 5\n5 5 5",
            "3 3\n1 2 3\n4 5 6\n7 8 9",     # slopes away, holds nothing
            "4 4\n9 9 9 9\n9 0 0 9\n9 0 0 9\n9 9 9 9",
            "3 4\n2 2 2 2\n2 1 0 2\n2 2 2 2",
        ],
    },
{
        "title": "Maximum Performance of a Team",
        "topic": "heap", "difficulty": "hard",
        "description": "Choose at most k people. The team's performance is the total of their speeds multiplied by the lowest efficiency among them. Return the greatest performance, modulo 1000000007.",
        "example_input": "6 2\n2 10 3 1 5 8\n5 4 3 9 7 2",
        "constraints": "Input format: line 1 is \"n k\", line 2 is the speeds, line 3 is the efficiencies. Output format: a single integer, the performance modulo 1000000007.",
        "solve": _solve_max_team_performance,
        "sample_inputs": ["6 2\n2 10 3 1 5 8\n5 4 3 9 7 2", "6 3\n2 10 3 1 5 8\n5 4 3 9 7 2"],
        "hidden_inputs": [
            "1 1\n1\n1",            # one person
            "1 1\n5\n3",
            "2 1\n1 2\n2 1",        # only one may be chosen
            "2 2\n1 2\n2 1",        # the lowest efficiency drags it down
            "2 2\n1 1\n1 1",
            "3 2\n1 2 3\n3 2 1",
            "3 3\n1 2 3\n1 1 1",    # every efficiency identical
            "3 1\n10 1 1\n1 10 10",
            "4 2\n4 3 2 1\n1 2 3 4",
            "6 4\n2 10 3 1 5 8\n5 4 3 9 7 2",
        ],
    },
{
        "title": "Maximum Number of Events That Can Be Attended II",
        "topic": "heap", "difficulty": "hard",
        "description": "Each event runs from a start day to an end day and is worth a given value, and attending one takes up every day of its span. Attend at most k events, none overlapping, and return the greatest total value.",
        "example_input": "3\n1 2 4\n3 4 3\n2 3 1\n2",
        "constraints": "Input format: line 1 is the number of events, followed by that many lines each \"start end value\", then a final line holding k. Output format: a single integer.",
        "solve": _solve_max_events_ii,
        "sample_inputs": ["3\n1 2 4\n3 4 3\n2 3 1\n2", "3\n1 2 4\n3 4 3\n2 3 10\n2"],
        "hidden_inputs": [
            "1\n1 1 5\n1",          # one event, taken
            "1\n1 1 5\n0",          # none may be taken
            "2\n1 1 5\n2 2 3\n2",   # both fit
            "2\n1 1 5\n2 2 3\n1",   # only the better one
            "2\n1 2 5\n2 3 9\n2",   # they overlap on day two
            "2\n1 2 5\n2 3 9\n1",
            "3\n1 1 1\n2 2 2\n3 3 3\n2",
            "3\n1 5 10\n2 3 1\n4 5 1\n2",
            "4\n1 2 1\n2 3 1\n3 4 1\n4 5 1\n2",
            "3\n1 1 1\n1 1 2\n1 1 3\n2",
        ],
    },
{
        "title": "Single-Threaded CPU",
        "topic": "heap", "difficulty": "hard",
        "description": "Tasks become available at given times and each takes a given time to run. Whenever the processor is free it takes the shortest available task, breaking ties by the lower task number; if nothing is available it waits. Report the order the tasks are run in.",
        "example_input": "4\n1 2\n2 4\n3 2\n4 1",
        "constraints": "Input format: line 1 is the number of tasks, followed by that many lines each \"availableAt duration\". Output format: the task numbers counting from zero, space-separated.",
        "solve": _solve_single_threaded_cpu,
        "sample_inputs": ["4\n1 2\n2 4\n3 2\n4 1", "5\n7 10\n7 12\n7 5\n7 4\n7 2"],
        "hidden_inputs": [
            "1\n0 1",               # a single task
            "1\n5 1",               # the processor waits first
            "2\n0 1\n0 1",          # a tie broken by task number
            "2\n0 2\n0 1",          # the shorter goes first
            "2\n0 1\n5 1",          # a gap between them
            "3\n0 3\n1 1\n2 1",
            "3\n0 1\n0 2\n0 3",
            "3\n2 2\n1 1\n0 3",
            "4\n0 1\n1 1\n2 1\n3 1",
            "4\n10 1\n10 2\n0 100\n10 3",
        ],
    },
{
        "title": "Swim in Rising Water",
        "topic": "heap", "difficulty": "hard",
        "description": "A grid gives the height of each square. At time t you may stand anywhere with height at most t, and moving between neighbouring squares is instant. Return the earliest time you can get from the top-left square to the bottom-right one.",
        "example_input": "2 2\n0 2\n1 3",
        "constraints": "Input format: line 1 is \"n n\", followed by n lines of n heights. Output format: a single integer.",
        "solve": _solve_swim_in_rising_water,
        "sample_inputs": ["2 2\n0 2\n1 3", "3 3\n0 1 2\n3 4 5\n6 7 8"],
        "hidden_inputs": [
            "1 1\n0",               # already there
            "1 1\n7",               # the starting square's own height counts
            "2 2\n0 1\n2 3",
            "2 2\n0 3\n1 2",        # the lower route wins
            "2 2\n0 1\n1 0",
            "3 3\n0 1 2\n1 2 3\n2 3 4",
            "3 3\n0 9 9\n1 9 9\n2 3 4",     # only one route is passable
            "3 3\n0 1 1\n1 1 1\n1 1 1",
            "4 4\n0 1 2 3\n1 2 3 4\n2 3 4 5\n3 4 5 6",
            "3 3\n8 8 8\n8 0 8\n8 8 0",     # the start height dominates
        ],
    },
]
