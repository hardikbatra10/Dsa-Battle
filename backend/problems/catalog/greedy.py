"""Greedy problems."""

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

def _solve_assign_cookies(lines):
    greed = sorted(map(int, lines[0].split()))
    sizes = sorted(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else []
    i = j = count = 0
    while i < len(greed) and j < len(sizes):
        if sizes[j] >= greed[i]:
            count += 1
            i += 1
        j += 1
    return str(count)


def _solve_lemonade_change(lines):
    bills = list(map(int, lines[0].split()))
    five = ten = 0
    for b in bills:
        if b == 5:
            five += 1
        elif b == 10:
            if five == 0:
                return "false"
            five -= 1
            ten += 1
        else:
            if ten > 0 and five > 0:
                ten -= 1
                five -= 1
            elif five >= 3:
                five -= 3
            else:
                return "false"
    return "true"


def _solve_stock_multiple(lines):
    prices = list(map(int, lines[0].split()))
    return str(sum(max(0, prices[i + 1] - prices[i]) for i in range(len(prices) - 1)))


def _solve_max_units_truck(lines):
    capacity = int(lines[0])
    counts = list(map(int, lines[1].split()))
    units = list(map(int, lines[2].split()))
    total = 0
    for u, c in sorted(zip(units, counts), reverse=True):
        take = min(c, capacity)
        total += take * u
        capacity -= take
        if capacity == 0:
            break
    return str(total)


def _solve_can_place_flowers(lines):
    bed = list(map(int, lines[0].split()))
    n = int(lines[1])
    count = 0
    for i in range(len(bed)):
        if (bed[i] == 0
                and (i == 0 or bed[i - 1] == 0)
                and (i == len(bed) - 1 or bed[i + 1] == 0)):
            bed[i] = 1
            count += 1
    return "true" if count >= n else "false"


def _solve_non_overlapping_intervals(lines):
    k = int(lines[0])
    ivs = sorted((tuple(map(int, lines[1 + i].split())) for i in range(k)),
                 key=lambda x: x[1])
    end = float("-inf")
    keep = 0
    for s, e in ivs:
        if s >= end:
            keep += 1
            end = e
    return str(k - keep)


def _solve_min_arrows(lines):
    k = int(lines[0])
    if k == 0:
        return "0"
    ivs = sorted((tuple(map(int, lines[1 + i].split())) for i in range(k)),
                 key=lambda x: x[1])
    arrows = 0
    last = float("-inf")
    for s, e in ivs:
        if s > last:
            arrows += 1
            last = e
    return str(arrows)


def _solve_partition_labels(lines):
    s = lines[0]
    last = {c: i for i, c in enumerate(s)}
    out = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:
            out.append(str(end - start + 1))
            start = i + 1
    return " ".join(out)


def _solve_task_scheduler(lines):
    tasks = lines[0].split()
    n = int(lines[1])
    from collections import Counter
    counts = Counter(tasks)
    top = max(counts.values())
    ties = sum(1 for v in counts.values() if v == top)
    return str(max(len(tasks), (top - 1) * (n + 1) + ties))


def _solve_refueling_stops(lines):
    target = int(lines[0])
    fuel = int(lines[1])
    k = int(lines[2])
    stations = [tuple(map(int, lines[3 + i].split())) for i in range(k)]
    import heapq
    heap = []
    stops = i = 0
    while fuel < target:
        while i < k and stations[i][0] <= fuel:
            heapq.heappush(heap, -stations[i][1])
            i += 1
        if not heap:
            return "-1"
        fuel += -heapq.heappop(heap)
        stops += 1
    return str(stops)


def _solve_ipo(lines):
    k, capital = map(int, lines[0].split())
    n = int(lines[1])
    projects = sorted((tuple(map(int, lines[2 + i].split())) for i in range(n)),
                      key=lambda x: x[1])
    import heapq
    heap = []
    i = 0
    for _ in range(k):
        while i < n and projects[i][1] <= capital:
            heapq.heappush(heap, -projects[i][0])
            i += 1
        if not heap:
            break
        capital += -heapq.heappop(heap)
    return str(capital)

def _solve_array_partition(lines):
    nums = sorted(map(int, lines[0].split()))
    return str(sum(nums[::2]))


def _solve_maximum_69_number(lines):
    s = lines[0]
    return s.replace("6", "9", 1)


def _solve_split_balanced_strings(lines):
    s = lines[0]
    balance = 0
    count = 0
    for c in s:
        balance += 1 if c == "R" else -1
        if balance == 0:
            count += 1
    return str(count)


def _solve_largest_perimeter_triangle(lines):
    nums = sorted(map(int, lines[0].split()), reverse=True)
    for i in range(len(nums) - 2):
        if nums[i] < nums[i + 1] + nums[i + 2]:
            return str(nums[i] + nums[i + 1] + nums[i + 2])
    return "0"


def _solve_jump_game_ii(lines):
    nums = list(map(int, lines[0].split()))
    jumps = 0
    end = 0
    far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return str(jumps)


def _solve_queue_reconstruction(lines):
    k = int(lines[0])
    people = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    people.sort(key=lambda p: (-p[0], p[1]))
    out = []
    for h, ahead in people:
        out.insert(ahead, (h, ahead))
    return "\n".join(f"{h} {a}" for h, a in out)


def _solve_reduce_array_half(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = sorted(Counter(nums).values(), reverse=True)
    removed = 0
    chosen = 0
    for c in counts:
        removed += c
        chosen += 1
        if removed * 2 >= len(nums):
            break
    return str(chosen)


def _solve_wiggle_subsequence(lines):
    nums = list(map(int, lines[0].split()))
    up = down = 1
    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1
    return str(max(up, down))


def _solve_two_city_scheduling(lines):
    k = int(lines[0])
    costs = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    costs.sort(key=lambda c: c[0] - c[1])
    half = k // 2
    return str(sum(c[0] for c in costs[:half]) + sum(c[1] for c in costs[half:]))


def _solve_hand_of_straights(lines):
    nums = list(map(int, lines[0].split()))
    size = int(lines[1])
    if len(nums) % size:
        return "false"
    from collections import Counter
    counts = Counter(nums)
    for v in sorted(counts):
        n = counts[v]
        if n <= 0:
            continue
        for step in range(size):
            if counts[v + step] < n:
                return "false"
            counts[v + step] -= n
    return "true"


def _solve_min_deletions_unique_freq(lines):
    s = lines[0]
    from collections import Counter
    used = set()
    deletions = 0
    for c in sorted(Counter(s).values(), reverse=True):
        while c > 0 and c in used:
            c -= 1
            deletions += 1
        if c > 0:
            used.add(c)
    return str(deletions)


def _solve_car_pooling(lines):
    capacity = int(lines[0])
    k = int(lines[1])
    events = []
    for i in range(k):
        num, start, end = map(int, lines[2 + i].split())
        events.append((start, num))
        events.append((end, -num))
    events.sort()
    onboard = 0
    for _, delta in events:
        onboard += delta
        if onboard > capacity:
            return "false"
    return "true"


def _solve_max_events_attended(lines):
    k = int(lines[0])
    events = sorted(tuple(map(int, lines[1 + i].split())) for i in range(k))
    import heapq
    heap = []
    i = 0
    attended = 0
    day = 0
    while i < k or heap:
        if not heap:
            day = max(day, events[i][0])
        while i < k and events[i][0] <= day:
            heapq.heappush(heap, events[i][1])
            i += 1
        while heap and heap[0] < day:
            heapq.heappop(heap)
        if heap:
            heapq.heappop(heap)
            attended += 1
        day += 1
    return str(attended)


def _solve_course_schedule_iii(lines):
    k = int(lines[0])
    courses = sorted(tuple(map(int, lines[1 + i].split())) for i in range(k))
    courses.sort(key=lambda c: c[1])
    import heapq
    heap = []
    spent = 0
    for duration, last in courses:
        heapq.heappush(heap, -duration)
        spent += duration
        if spent > last:
            spent += heapq.heappop(heap)
    return str(len(heap))


def _solve_split_consecutive_subsequences(lines):
    nums = list(map(int, lines[0].split()))
    from collections import Counter
    counts = Counter(nums)
    endings = Counter()
    for v in nums:
        if counts[v] == 0:
            continue
        counts[v] -= 1
        if endings[v - 1] > 0:
            endings[v - 1] -= 1
            endings[v] += 1
        elif counts[v + 1] > 0 and counts[v + 2] > 0:
            counts[v + 1] -= 1
            counts[v + 2] -= 1
            endings[v + 2] += 1
        else:
            return "false"
    return "true"


def _solve_min_taps_garden(lines):
    n = int(lines[0])
    ranges = list(map(int, lines[1].split()))
    reach = [0] * (n + 1)
    for i, r in enumerate(ranges):
        left = max(0, i - r)
        reach[left] = max(reach[left], i + r)
    taps = 0
    end = 0
    far = 0
    i = 0
    while end < n:
        while i <= end:
            far = max(far, reach[i])
            i += 1
        if far <= end:
            return "-1"
        taps += 1
        end = far
    return str(taps)


def _solve_patching_array(lines):
    nums = list(map(int, lines[0].split())) if lines[0].strip() else []
    n = int(lines[1])
    patches = 0
    covered = 0
    i = 0
    while covered < n:
        if i < len(nums) and nums[i] <= covered + 1:
            covered += nums[i]
            i += 1
        else:
            covered += covered + 1
            patches += 1
    return str(patches)


def _solve_video_stitching(lines):
    k = int(lines[0])
    clips = [tuple(map(int, lines[1 + i].split())) for i in range(k)]
    time = int(lines[1 + k])
    if time == 0:
        return "0"
    best = [0] * (time + 1)
    for s, e in clips:
        if s <= time:
            for t in range(s, min(e, time) + 1):
                best[t] = max(best[t], e)
    count = 0
    end = 0
    far = 0
    i = 0
    while end < time:
        while i <= min(end, time):
            far = max(far, best[i])
            i += 1
        if far <= end:
            return "-1"
        count += 1
        end = far
    return str(count)


def _solve_create_maximum_number(lines):
    a = list(map(int, lines[0].split()))
    b = list(map(int, lines[1].split()))
    k = int(lines[2])

    def best(nums, size):
        drop = len(nums) - size
        stack = []
        for v in nums:
            while drop and stack and stack[-1] < v:
                stack.pop()
                drop -= 1
            stack.append(v)
        return stack[:size]

    def weave(x, y):
        out = []
        while x or y:
            bigger = x if x > y else y
            out.append(bigger[0])
            del bigger[0]
        return out

    answer = []
    for take in range(max(0, k - len(b)), min(k, len(a)) + 1):
        cand = weave(best(a, take), best(b, k - take))
        if cand > answer:
            answer = cand
    return " ".join(map(str, answer))


PROBLEMS = [
{
        "title": "Jump Game",
        "topic": "greedy",
        "difficulty": "easy",
        "description": "Given an array where each element is the maximum jump length from that position, determine if you can reach the last index starting from index 0.",
        "example_input": "2 3 1 1 4",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: \"true\" or \"false\".",
        "solve": _solve_jump_game,
        "sample_inputs": ["2 3 1 1 4", "3 0 0 1"],
        "hidden_inputs": [
            "0",              # already at the last index
            "1",
            "0 1",            # stuck immediately
            "1 0",
            "0 0 0",
            "2 0 0",
            "1 1 1 1",
            "3 2 1 0 4",      # the classic zero trap
            "2 5 0 0",
            "5 0 0 0 0 0",    # one big jump clears every zero
            "1 2 3 0 0 0 1",  # reach stalls just short of the end
        ],
    },
{
        "title": "Gas Station",
        "topic": "greedy",
        "difficulty": "medium",
        "description": "There are n gas stations in a circuit; gas[i] is the fuel available at station i and cost[i] is the fuel needed to travel from station i to i+1. Return the starting station index that lets you complete the circuit, or -1 if impossible.",
        "example_input": "1 2 3 4 5\n3 4 5 1 2",
        "constraints": "Input format: line 1 is the space-separated gas array, line 2 is the space-separated cost array. Output format: a single integer.",
        "solve": _solve_gas_station,
        "sample_inputs": ["1 2 3 4 5\n3 4 5 1 2", "4 5 2 6\n3 4 3 7"],
        "hidden_inputs": [
            "1\n1",              # single station, exactly enough fuel
            "2\n1",
            "1\n2",              # single station, not enough fuel
            "2 3 4\n3 4 3",
            "3 3 4\n3 4 4",      # total deficit of exactly one
            "3 1 1\n1 2 2",      # only station 0 works
            "1 2 3 3\n2 1 5 1",  # only the last station works
            "5 8 2 8\n6 5 6 6",
            "5 1 2 3 4\n4 4 1 5 1",
            "6 1 4 3 5\n3 8 2 6 5",
            "4 5 2 6 5 3\n3 2 7 3 2 9",
        ],
    },
{
        "title": "Candy",
        "topic": "greedy",
        "difficulty": "hard",
        "description": "Each child is given a rating. Every child must get at least 1 candy, and a child with a higher rating than a neighbor must get more candy than that neighbor. Return the minimum total candies needed.",
        "example_input": "1 0 2",
        "constraints": "Input format: one line of space-separated ratings. Output format: a single integer.",
        "solve": _solve_candy,
        "sample_inputs": ["1 0 2", "1 2 87 87 87 2 1"],
        "hidden_inputs": [
            "1",          # one child
            "1 1",        # equal ratings need no extra candy
            "1 2",
            "2 1",
            "5 5 5 5",    # all equal
            "1 2 2",
            "1 2 3 2 1",  # single peak
            "1 0 2 0 1",  # alternating valleys
            "1 3 2 2 1",
            "1 2 3 4 5",  # strictly increasing
            "5 4 3 2 1",  # strictly decreasing
            "1 3 4 5 2",
        ],
    },
{
        "title": "Assign Cookies",
        "topic": "greedy",
        "difficulty": "easy",
        "description": "Each child will only be satisfied by a cookie at least as large as their appetite, and each cookie can go to at most one child. Return the greatest number of children that can be satisfied.",
        "example_input": "1 2 3\n1 1",
        "constraints": "Input format: line 1 is the space-separated appetites, line 2 is the space-separated cookie sizes. Output format: a single integer.",
        "solve": _solve_assign_cookies,
        "sample_inputs": ["1 2 3\n1 1", "1 2\n1 2 3"],
        "hidden_inputs": [
            "1\n1",                 # an exact fit
            "2\n1",                 # the cookie is too small
            "1\n2",                 # a larger cookie still works
            "1 1 1\n1",             # one cookie, three children
            "1\n1 1 1",             # one child, three cookies
            "5 5 5\n5 5 5",         # everyone satisfied
            "9 9\n1 1",             # nobody satisfied
            "1 2 3\n3",             # the big cookie should go to the small appetite
            "10 9 8 7\n5 6 7 8",
            "1 2 3 4 5\n1 2 3",
        ],
    },
{
        "title": "Lemonade Change",
        "topic": "greedy",
        "difficulty": "easy",
        "description": "Each customer pays for a five-rupee lemonade with a five, ten or twenty note, and must be given the right change immediately. You start with nothing. Decide whether every customer can be served.",
        "example_input": "5 5 5 10 20",
        "constraints": "Input format: one line of space-separated notes, each 5, 10 or 20. Output format: \"true\" or \"false\".",
        "solve": _solve_lemonade_change,
        "sample_inputs": ["5 5 5 10 20", "5 5 10 10 20"],
        "hidden_inputs": [
            "5",                    # no change needed
            "10",                   # the first customer cannot be served
            "20",
            "5 5",
            "5 10",                 # the five pays the change
            "5 20",                 # a twenty needs fifteen in change
            "5 5 5 20",             # three fives make the change
            "5 5 10 20",            # a ten plus a five is preferred
            "5 5 5 5 20 20",
            "5 5 10 10 5 20",
        ],
    },
{
        "title": "Best Time to Buy and Sell Stock II",
        "topic": "greedy",
        "difficulty": "easy",
        "description": "You may buy and sell the same stock as many times as you like, but you can hold at most one share at a time. Given the daily prices, return the largest total profit.",
        "example_input": "7 1 5 3 6 4",
        "constraints": "Input format: one line of space-separated prices. Output format: a single integer.",
        "solve": _solve_stock_multiple,
        "sample_inputs": ["7 1 5 3 6 4", "1 2 3 4 5"],
        "hidden_inputs": [
            "1",                    # a single day, no trade possible
            "1 2",
            "2 1",                  # only a loss available
            "5 5 5 5",              # flat prices
            "7 6 4 3 1",            # falling every day
            "1 2 3 4 5 6",          # rising every day
            "1 5 1 5 1 5",          # repeated cycles
            "3 3 5 0 0 3 1 4",
            "2 1 2 0 1",
            "100 1 100",
        ],
    },
{
        "title": "Maximum Units on a Truck",
        "topic": "greedy",
        "difficulty": "easy",
        "description": "Boxes come in several types; each type has a number of boxes available and a number of units per box. The truck holds a limited number of boxes in total. Return the greatest number of units it can carry.",
        "example_input": "4\n1 2 3\n3 2 1",
        "constraints": "Input format: line 1 is the truck's box capacity, line 2 is the space-separated box counts per type, line 3 is the space-separated units per box for those types. Output format: a single integer.",
        "solve": _solve_max_units_truck,
        "sample_inputs": ["4\n1 2 3\n3 2 1", "10\n5 2 4 1\n10 5 7 9"],
        "hidden_inputs": [
            "1\n1\n1",              # one box of one unit
            "1\n1 1\n1 5",          # the richer box must be chosen
            "0\n5\n5",              # no capacity at all
            "100\n1 2 3\n3 2 1",    # capacity exceeds every box
            "3\n3\n7",              # a single type fills the truck
            "2\n5 5\n1 9",
            "5\n2 2 2\n1 2 3",
            "6\n1 1 1 1\n4 3 2 1",  # capacity beyond the total box count
            "4\n9 9\n2 2",          # equal unit values, order must not matter
            "7\n3 4 5\n5 4 3",
        ],
    },
{
        "title": "Can Place Flowers",
        "topic": "greedy",
        "difficulty": "easy",
        "description": "A flowerbed is a row of plots, some already planted. No two flowers may occupy neighbouring plots. Decide whether n more flowers can be planted.",
        "example_input": "1 0 0 0 1\n1",
        "constraints": "Input format: line 1 is the space-separated bed, using 1 for a planted plot and 0 for an empty one, line 2 is n. Output format: \"true\" or \"false\".",
        "solve": _solve_can_place_flowers,
        "sample_inputs": ["1 0 0 0 1\n1", "1 0 0 0 1\n2"],
        "hidden_inputs": [
            "0\n1",                 # a single empty plot
            "0\n2",                 # only one flower fits
            "1\n0",                 # nothing to plant
            "1\n1",                 # a full bed
            "0 0\n1",               # neighbours block the second
            "0 0\n2",
            "0 0 0\n2",             # the two ends work
            "1 0 0 0 0 1\n2",
            "1 0 1 0 1\n1",         # every gap is blocked
            "0 0 1 0 0\n2",
        ],
    },
{
        "title": "Non-overlapping Intervals",
        "topic": "greedy",
        "difficulty": "medium",
        "description": "Given a collection of intervals, return the fewest that must be removed so that none of the remaining ones overlap. Intervals that merely touch at an endpoint do not overlap.",
        "example_input": "4\n1 2\n2 3\n3 4\n1 3",
        "constraints": "Input format: line 1 is the number of intervals, followed by that many lines each \"start end\". Output format: a single integer.",
        "solve": _solve_non_overlapping_intervals,
        "sample_inputs": ["4\n1 2\n2 3\n3 4\n1 3", "3\n1 2\n1 2\n1 2"],
        "hidden_inputs": [
            "1\n1 2",               # nothing to remove
            "2\n1 2\n2 3",          # touching endpoints are fine
            "2\n1 3\n2 4",          # a genuine overlap
            "2\n1 10\n2 3",         # the long one should go
            "3\n1 2\n3 4\n5 6",     # already disjoint
            "3\n1 5\n2 3\n4 6",
            "4\n1 2\n1 3\n1 4\n1 5",   # all share a start
            "4\n1 100\n11 22\n1 11\n2 12",
            "5\n1 2\n2 3\n3 4\n4 5\n5 6",
            "3\n0 1\n0 1\n0 1",
        ],
    },
{
        "title": "Minimum Number of Arrows to Burst Balloons",
        "topic": "greedy",
        "difficulty": "medium",
        "description": "Balloons occupy horizontal spans. An arrow shot straight up at a position bursts every balloon whose span includes that position, endpoints included. Return the fewest arrows that burst them all.",
        "example_input": "4\n10 16\n2 8\n1 6\n7 12",
        "constraints": "Input format: line 1 is the number of balloons, followed by that many lines each \"start end\". Output format: a single integer.",
        "solve": _solve_min_arrows,
        "sample_inputs": ["4\n10 16\n2 8\n1 6\n7 12", "4\n1 2\n3 4\n5 6\n7 8"],
        "hidden_inputs": [
            "1\n1 2",               # one arrow
            "2\n1 2\n3 4",          # disjoint spans need two
            "2\n1 2\n2 3",          # touching at a point shares an arrow
            "2\n1 10\n2 3",         # one contains the other
            "3\n1 2\n2 3\n3 4",     # a chain shares two arrows
            "3\n1 5\n1 5\n1 5",     # identical spans
            "4\n1 2\n2 3\n1 3\n4 5",
            "5\n1 10\n2 9\n3 8\n4 7\n5 6",   # nested, a single arrow suffices
            "4\n0 1\n1 2\n2 3\n3 4",
            "3\n9 12\n1 10\n4 11",
        ],
    },
{
        "title": "Partition Labels",
        "topic": "greedy",
        "difficulty": "medium",
        "description": "Split a string into as many pieces as possible so that every letter appears in at most one piece. Return the sizes of those pieces in order.",
        "example_input": "ababcbacadefegdehijhklij",
        "constraints": "Input format: one line containing the string (lowercase). Output format: the piece sizes, space-separated.",
        "solve": _solve_partition_labels,
        "sample_inputs": ["ababcbacadefegdehijhklij", "eccbbbbdec"],
        "hidden_inputs": [
            "a",                    # one letter, one piece
            "ab",                   # two independent pieces
            "aa",                   # one piece of two
            "aba",                  # the b is trapped inside
            "abc",
            "aabbcc",               # three clean pieces
            "abcabc",               # one piece covering everything
            "abacbc",
            "qiejxqfnqceocmy",
            "zzzzzzz",
        ],
    },
{
        "title": "Task Scheduler",
        "topic": "greedy",
        "difficulty": "medium",
        "description": "Identical tasks must be separated by at least n slots, during which the processor may run a different task or stay idle. Every task takes one slot. Return the fewest slots needed to run them all.",
        "example_input": "A A A B B B\n2",
        "constraints": "Input format: line 1 is the space-separated task letters, line 2 is n. Output format: a single integer.",
        "solve": _solve_task_scheduler,
        "sample_inputs": ["A A A B B B\n2", "A A A B B B\n0"],
        "hidden_inputs": [
            "A\n0",                 # a single task
            "A\n5",                 # the cooldown never applies
            "A A\n0",               # no cooldown needed
            "A A\n1",
            "A A\n3",               # three idle slots between them
            "A B C\n2",             # all different, no waiting
            "A A A\n2",
            "A A B B\n1",
            "A A A A B C D E\n2",   # the filler tasks absorb the idling
            "A A A B B B C C C\n2", # three tasks tie for most frequent
        ],
    },
{
        "title": "Minimum Number of Refueling Stops",
        "topic": "greedy",
        "difficulty": "hard",
        "description": "A car starts with some fuel and burns one unit per unit of distance. Stations along the route each offer a fixed amount of fuel. Return the fewest stops needed to reach the target, or -1 if it cannot be reached.",
        "example_input": "100\n10\n4\n10 60\n20 30\n30 30\n60 40",
        "constraints": "Input format: line 1 is the target distance, line 2 is the starting fuel, line 3 is the number of stations, followed by that many lines each \"position fuel\", ordered by position. Output format: a single integer, or -1.",
        "solve": _solve_refueling_stops,
        "sample_inputs": ["100\n10\n4\n10 60\n20 30\n30 30\n60 40", "1\n1\n0"],
        "hidden_inputs": [
            "0\n0\n0",              # already there
            "10\n10\n0",            # exactly enough fuel, no stations
            "100\n1\n0",            # no stations and not enough fuel
            "100\n50\n1\n50 50",    # one stop is exactly enough
            "100\n50\n1\n50 49",    # one unit short
            "100\n10\n1\n10 100",
            "100\n10\n2\n10 40\n50 60",
            "100\n10\n2\n60 40\n70 60",   # the first station is out of reach
            "1000\n299\n5\n13 21\n26 115\n100 47\n225 99\n299 141",
            "100\n25\n3\n25 25\n50 25\n75 25",   # three stops, each just enough
        ],
    },
{
        "title": "IPO",
        "topic": "greedy",
        "difficulty": "hard",
        "description": "You may undertake at most k projects, one after another. A project can only be started if your capital is at least its requirement, and finishing it adds its profit to your capital. Return the largest capital you can end up with.",
        "example_input": "2 0\n3\n1 0\n2 1\n3 2",
        "constraints": "Input format: line 1 is \"k startingCapital\", line 2 is the number of projects, followed by that many lines each \"profit capital\". Output format: a single integer.",
        "solve": _solve_ipo,
        "sample_inputs": ["2 0\n3\n1 0\n2 1\n3 2", "3 0\n3\n1 0\n2 1\n3 2"],
        "hidden_inputs": [
            "1 0\n1\n5 0",          # one affordable project
            "1 0\n1\n5 1",          # nothing is affordable
            "0 7\n1\n5 0",          # no projects allowed
            "5 0\n1\n5 0",          # more slots than projects
            "2 0\n2\n1 0\n10 0",    # the richer project should go first
            "1 0\n2\n1 0\n10 0",    # only one slot, take the best
            "2 1\n3\n2 0\n3 1\n5 2",
            "3 0\n4\n1 0\n1 1\n1 2\n1 3",   # each project unlocks the next
            "2 2\n3\n1 5\n2 5\n3 5",        # every project is out of reach
            "4 0\n4\n9 0\n8 1\n7 2\n6 3",
        ],
    },
{
        "title": "Array Partition",
        "topic": "greedy", "difficulty": "easy",
        "description": "Split the values into pairs, then add up the smaller value of each pair. Return the largest total achievable.",
        "example_input": "1 4 3 2",
        "constraints": "Input format: one line of an even count of space-separated integers. Output format: a single integer.",
        "solve": _solve_array_partition,
        "sample_inputs": ["1 4 3 2", "6 2 6 5 1 2"],
        "hidden_inputs": [
            "1 1",                  # one pair
            "1 2",                  # the larger value is wasted
            "2 1",
            "0 0",
            "-1 -2",                # negatives
            "1 1 1 1",
            "1 2 3 4",
            "4 3 2 1",              # order must not matter
            "5 5 5 5 5 5",
            "-1 1 -2 2",
        ],
    },
{
        "title": "Maximum 69 Number",
        "topic": "greedy", "difficulty": "easy",
        "description": "A number is written using only the digits six and nine. Change at most one digit to make it as large as possible, and return the result.",
        "example_input": "9669",
        "constraints": "Input format: one line containing the number, made only of the digits 6 and 9. Output format: the resulting number.",
        "solve": _solve_maximum_69_number,
        "sample_inputs": ["9669", "9996"],
        "hidden_inputs": [
            "6",                    # one digit, changed
            "9",                    # one digit, already best
            "66",                   # only the first is changed
            "69",
            "96",
            "99",                   # nothing to change
            "666",
            "999",
            "9669669",
            "6999999999",
        ],
    },
{
        "title": "Split a String in Balanced Strings",
        "topic": "greedy", "difficulty": "easy",
        "description": "A stretch of the string is balanced when it holds as many L characters as R characters. Cut the string into as many balanced pieces as possible and return how many there are.",
        "example_input": "RLRRLLRLRL",
        "constraints": "Input format: one line made only of the characters L and R, already balanced overall. Output format: a single integer.",
        "solve": _solve_split_balanced_strings,
        "sample_inputs": ["RLRRLLRLRL", "RLLLLRRRLR"],
        "hidden_inputs": [
            "RL",                   # a single piece
            "LR",
            "RLRL",                 # two pieces
            "RRLL",                 # one piece, nested
            "LLRR",
            "RLRLRL",
            "RRRLLL",
            "RLRRLL",
            "LRLRLRLR",
            "RRRRLLLLRL",
        ],
    },
{
        "title": "Largest Perimeter Triangle",
        "topic": "greedy", "difficulty": "easy",
        "description": "Choose three of the given lengths that can form a triangle with a positive area, and return the largest total length possible. Return zero if no three can.",
        "example_input": "2 1 2",
        "constraints": "Input format: one line of space-separated positive lengths. Output format: a single integer.",
        "solve": _solve_largest_perimeter_triangle,
        "sample_inputs": ["2 1 2", "1 2 1 10"],
        "hidden_inputs": [
            "1 1 1",                # an equilateral triangle
            "1 2 3",                # degenerate, so zero
            "1 1 2",                # also degenerate
            "3 2 3 4",
            "1 1 1 1",
            "3 6 2 3",
            "1 2 4 8",              # nothing works
            "5 5 5 5",
            "2 3 4 5 10",
            "100 1 1",
        ],
    },
{
        "title": "Jump Game II",
        "topic": "greedy", "difficulty": "medium",
        "description": "Each value gives the furthest you may jump forward from that position. Starting at the first position, return the fewest jumps needed to reach the last one.",
        "example_input": "2 3 1 1 4",
        "constraints": "Input format: one line of space-separated non-negative integers; the last position is always reachable. Output format: a single integer.",
        "solve": _solve_jump_game_ii,
        "sample_inputs": ["2 3 1 1 4", "2 3 0 1 4"],
        "hidden_inputs": [
            "0",                    # already at the end
            "1 0",                  # a single jump
            "2 0",                  # a jump longer than needed
            "1 1 1",
            "2 1 1",
            "3 1 1 1",              # one jump clears everything
            "1 1 1 1 1",
            "5 1 1 1 1 1",
            "1 2 1 1 1",
            "2 3 1 1 4 2 1",
        ],
    },
{
        "title": "Queue Reconstruction by Height",
        "topic": "greedy", "difficulty": "medium",
        "description": "Each person is described by their height and the number of people at least as tall standing in front of them. Rebuild the queue that fits every description.",
        "example_input": "6\n7 0\n4 4\n7 1\n5 0\n6 1\n5 2",
        "constraints": "Input format: line 1 is the number of people, followed by that many lines each \"height count\". Exactly one queue fits. Output format: one person per line as \"height count\".",
        "solve": _solve_queue_reconstruction,
        "sample_inputs": ["6\n7 0\n4 4\n7 1\n5 0\n6 1\n5 2", "4\n6 0\n5 0\n4 0\n3 2"],
        "hidden_inputs": [
            "1\n1 0",               # a single person
            "2\n1 0\n2 0",          # the taller must come first
            "2\n2 0\n1 1",
            "2\n1 1\n2 0",          # given out of order
            "3\n1 0\n2 0\n3 0",
            "3\n3 0\n2 1\n1 2",
            "3\n2 0\n2 1\n2 2",     # equal heights
            "4\n1 0\n2 0\n3 0\n4 0",
            "4\n4 0\n3 0\n2 2\n1 1",
            "5\n5 0\n4 0\n3 0\n2 0\n1 0",
        ],
    },
{
        "title": "Reduce Array Size to The Half",
        "topic": "greedy", "difficulty": "medium",
        "description": "Choose a set of values and delete every occurrence of them, so that at least half the list is gone. Return the smallest number of different values you need to choose.",
        "example_input": "3 3 3 3 5 5 5 2 2 7",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_reduce_array_half,
        "sample_inputs": ["3 3 3 3 5 5 5 2 2 7", "7 7 7 7 7 7"],
        "hidden_inputs": [
            "1",                    # one value covers everything
            "1 1",
            "1 2",                  # either value reaches half
            "1 1 2 2",
            "1 2 3 4",              # two values are needed
            "1 1 1 2",
            "1 1 2 3",
            "1 2 3 4 5 6",
            "5 5 5 5 1 2 3 4",
            "1 9 7 5 9 1 1 1 1 1",
        ],
    },
{
        "title": "Wiggle Subsequence",
        "topic": "greedy", "difficulty": "medium",
        "description": "A wiggle sequence is one where the differences between neighbours alternate between positive and negative. Return the length of the longest such sequence that can be picked out, keeping the original order.",
        "example_input": "1 7 4 9 2 5",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_wiggle_subsequence,
        "sample_inputs": ["1 7 4 9 2 5", "1 17 5 10 13 15 10 5 16 8"],
        "hidden_inputs": [
            "1",                    # a single value
            "1 1",                  # equal values do not wiggle
            "1 2",
            "2 1",
            "1 1 1",
            "1 2 3",                # a straight rise counts as two
            "3 2 1",
            "1 2 1 2 1",            # every step alternates
            "1 2 2 3",
            "0 0 0 0 0",
        ],
    },
{
        "title": "Two City Scheduling",
        "topic": "greedy", "difficulty": "medium",
        "description": "Each person can be flown to one of two cities at a given cost, and exactly half must go to each. Return the smallest total cost.",
        "example_input": "4\n10 20\n30 200\n400 50\n30 20",
        "constraints": "Input format: line 1 is the number of people, always even, followed by that many lines each \"costToFirst costToSecond\". Output format: a single integer.",
        "solve": _solve_two_city_scheduling,
        "sample_inputs": ["4\n10 20\n30 200\n400 50\n30 20", "6\n259 770\n448 54\n926 667\n184 139\n840 118\n577 469"],
        "hidden_inputs": [
            "2\n1 1\n1 1",          # every choice costs the same
            "2\n1 2\n2 1",          # each goes to their cheaper city
            "2\n2 1\n1 2",
            "2\n1 2\n1 2",          # one must take the dearer option
            "2\n0 0\n0 0",
            "4\n1 1\n1 1\n1 1\n1 1",
            "4\n1 100\n1 100\n1 100\n1 100",
            "4\n100 1\n1 100\n100 1\n1 100",
            "6\n1 2\n3 4\n5 6\n7 8\n9 10\n11 12",
            "4\n515 563\n451 713\n537 709\n343 819",
        ],
    },
{
        "title": "Hand of Straights",
        "topic": "greedy", "difficulty": "medium",
        "description": "Decide whether the cards can be dealt entirely into groups of the given size, each group holding cards that run consecutively.",
        "example_input": "1 2 3 6 2 3 4 7 8\n3",
        "constraints": "Input format: line 1 is the space-separated card values, line 2 is the group size. Output format: \"true\" or \"false\".",
        "solve": _solve_hand_of_straights,
        "sample_inputs": ["1 2 3 6 2 3 4 7 8\n3", "1 2 3 4 5\n4"],
        "hidden_inputs": [
            "1\n1",                 # groups of one always work
            "1 2\n1",
            "1 2\n2",               # one consecutive pair
            "1 3\n2",               # a gap breaks it
            "1 1\n2",               # equal cards are not consecutive
            "1 2 3\n3",
            "1 2 3\n2",             # the count does not divide
            "1 1 2 2 3 3\n3",       # two separate runs
            "1 2 2 3 3 4\n3",
            "8 10 12\n3",
        ],
    },
{
        "title": "Minimum Deletions to Make Character Frequencies Unique",
        "topic": "greedy", "difficulty": "medium",
        "description": "Delete as few letters as possible so that no two different letters occur the same number of times. Return how many deletions are needed.",
        "example_input": "aab",
        "constraints": "Input format: one line containing the lowercase string. Output format: a single integer.",
        "solve": _solve_min_deletions_unique_freq,
        "sample_inputs": ["aab", "aaabbbcc"],
        "hidden_inputs": [
            "a",                    # nothing to do
            "aa",
            "ab",                   # both occur once, one must go
            "aabb",
            "abc",                  # all three tie
            "aaabbb",
            "ceabaacb",
            "aaaa",
            "abcabc",
            "bbcebab",
        ],
    },
{
        "title": "Car Pooling",
        "topic": "greedy", "difficulty": "medium",
        "description": "A car drives east picking up and dropping off passengers at given points. Decide whether it can complete every trip without ever carrying more than its capacity.",
        "example_input": "4\n2\n2 1 5\n3 3 7",
        "constraints": "Input format: line 1 is the capacity, line 2 is the number of trips, followed by that many lines each \"passengers from to\". Output format: \"true\" or \"false\".",
        "solve": _solve_car_pooling,
        "sample_inputs": ["4\n2\n2 1 5\n3 3 7", "5\n2\n2 1 5\n3 3 7"],
        "hidden_inputs": [
            "1\n1\n1 0 1",          # exactly full
            "1\n1\n2 0 1",          # over capacity at once
            "2\n2\n1 0 1\n1 1 2",   # the first leaves as the second boards
            "1\n2\n1 0 1\n1 1 2",   # the same, at capacity one
            "1\n2\n1 0 2\n1 1 3",   # they overlap, so it fails
            "3\n2\n2 1 5\n3 5 7",
            "4\n3\n2 1 5\n3 5 7\n4 7 9",
            "11\n3\n3 2 7\n3 7 9\n8 3 9",
            "16\n3\n9 3 4\n9 1 7\n4 2 4",
            "2\n1\n2 0 100",
        ],
    },
{
        "title": "Maximum Number of Events That Can Be Attended",
        "topic": "greedy", "difficulty": "hard",
        "description": "Each event runs from a start day to an end day, and you may attend only one event per day, on any day within its span. Return the greatest number of events you can attend.",
        "example_input": "3\n1 2\n2 3\n3 4",
        "constraints": "Input format: line 1 is the number of events, followed by that many lines each \"start end\". Output format: a single integer.",
        "solve": _solve_max_events_attended,
        "sample_inputs": ["3\n1 2\n2 3\n3 4", "4\n1 2\n2 3\n3 4\n1 2"],
        "hidden_inputs": [
            "1\n1 1",               # a single one-day event
            "2\n1 1\n1 1",          # both want the same single day
            "2\n1 1\n2 2",          # separate days
            "2\n1 2\n1 2",          # two days, two events
            "3\n1 1\n1 1\n1 1",
            "3\n1 3\n1 3\n1 3",
            "3\n1 2\n1 2\n3 3",
            "4\n1 4\n4 4\n2 2\n3 4",
            "5\n1 5\n1 5\n1 5\n1 5\n1 5",
            "4\n1 1\n2 2\n3 3\n4 4",
        ],
    },
{
        "title": "Course Schedule III",
        "topic": "greedy", "difficulty": "hard",
        "description": "Each course takes a number of days and must be finished by a given day, and courses are taken one after another starting on day one. Return the greatest number of courses that can be completed.",
        "example_input": "4\n100 200\n200 1300\n1000 1250\n2000 3200",
        "constraints": "Input format: line 1 is the number of courses, followed by that many lines each \"duration lastDay\". Output format: a single integer.",
        "solve": _solve_course_schedule_iii,
        "sample_inputs": ["4\n100 200\n200 1300\n1000 1250\n2000 3200", "1\n1 2"],
        "hidden_inputs": [
            "1\n1 1",               # exactly fits
            "1\n2 1",               # cannot be finished in time
            "2\n1 1\n1 2",          # both fit
            "2\n2 2\n2 2",          # only one fits
            "2\n1 2\n2 2",
            "3\n1 1\n1 2\n1 3",
            "3\n3 3\n2 2\n1 1",     # only the shortest fits
            "3\n5 5\n4 6\n2 6",     # dropping a long course lets two in
            "4\n1 2\n2 3\n3 4\n4 5",
            "5\n5 15\n3 19\n6 7\n2 10\n5 16",
        ],
    },
{
        "title": "Split Array into Consecutive Subsequences",
        "topic": "greedy", "difficulty": "hard",
        "description": "Decide whether the values, already in increasing order, can be split entirely into runs of consecutive whole numbers, each run at least three long.",
        "example_input": "1 2 3 3 4 5",
        "constraints": "Input format: one line of space-separated integers in non-decreasing order. Output format: \"true\" or \"false\".",
        "solve": _solve_split_consecutive_subsequences,
        "sample_inputs": ["1 2 3 3 4 5", "1 2 3 3 4 4 5 5"],
        "hidden_inputs": [
            "1 2 3",                # exactly one run
            "1 2",                  # too short
            "1 1 1",                # equal values do not run
            "1 2 3 4",              # a run of four
            "1 2 3 5",              # the five is stranded
            "1 2 3 3 4 5 6",
            "1 2 3 4 4 5 6",
            "1 2 3 3 4 4 5 5 6 6",
            "1 2 3 4 5 6",
            "1 2 3 4 5",
        ],
    },
{
        "title": "Minimum Number of Taps to Open to Water a Garden",
        "topic": "greedy", "difficulty": "hard",
        "description": "A garden stretches from zero to n. Each tap sits at its own point and waters everything within its range on either side. Return the fewest taps that together water the whole garden, or -1 if it cannot be done.",
        "example_input": "5\n3 4 1 1 0 0",
        "constraints": "Input format: line 1 is n, line 2 is the space-separated ranges for the taps at points 0 to n. Output format: a single integer, or -1.",
        "solve": _solve_min_taps_garden,
        "sample_inputs": ["5\n3 4 1 1 0 0", "3\n0 0 0 0"],
        "hidden_inputs": [
            "1\n1 0",               # one tap reaches everything
            "1\n0 1",
            "1\n0 0",               # neither tap reaches, so -1
            "2\n1 0 1",             # the ends cover it between them
            "2\n0 1 0",             # the middle tap covers everything
            "2\n0 0 0",
            "3\n1 1 1 1",
            "3\n0 5 0 0",
            "5\n1 1 1 1 1 1",
            "7\n1 2 1 0 2 1 0 1",
        ],
    },
{
        "title": "Patching Array",
        "topic": "greedy", "difficulty": "hard",
        "description": "Given values in increasing order, add as few extra values as possible so that every whole number from one to n can be formed by adding up some of them. Return how many were added.",
        "example_input": "1 3\n6",
        "constraints": "Input format: line 1 is the space-separated values in increasing order, line 2 is n. Output format: a single integer.",
        "solve": _solve_patching_array,
        "sample_inputs": ["1 3\n6", "1 5 10\n20"],
        "hidden_inputs": [
            "1\n1",                 # nothing to add
            "2\n1",                 # one must be added
            "1\n2",
            "1 2\n3",               # already sufficient
            "1 2 4\n7",
            "1 2 2\n5",
            "1 2 31 33\n2000",
            "1 3\n1",
            "2 3\n6",
            "1 1 1\n5",
        ],
    },
{
        "title": "Video Stitching",
        "topic": "greedy", "difficulty": "hard",
        "description": "Clips each cover a stretch of a recording and may be cut shorter. Return the fewest clips needed to cover everything from time zero to the given end, or -1 if it cannot be covered.",
        "example_input": "6\n0 2\n4 6\n8 10\n1 9\n1 5\n5 9\n10",
        "constraints": "Input format: line 1 is the number of clips, followed by that many lines each \"start end\", then a final line holding the end time. Output format: a single integer, or -1.",
        "solve": _solve_video_stitching,
        "sample_inputs": ["6\n0 2\n4 6\n8 10\n1 9\n1 5\n5 9\n10", "3\n0 1\n1 2\n0 2\n5"],
        "hidden_inputs": [
            "1\n0 1\n1",            # one clip covers it
            "1\n0 1\n2",            # it falls short, so -1
            "1\n1 2\n2",            # nothing starts at zero
            "2\n0 1\n1 2\n2",
            "2\n0 2\n1 3\n3",       # overlapping clips
            "2\n0 1\n2 3\n3",       # a gap in the middle
            "1\n0 5\n0",            # the end time is zero
            "3\n0 4\n2 8\n1 3\n5",
            "4\n0 1\n6 8\n0 2\n5 6\n8",
            "5\n0 1\n1 2\n2 3\n3 4\n4 5\n5",
        ],
    },
{
        "title": "Create Maximum Number",
        "topic": "greedy", "difficulty": "hard",
        "description": "Take exactly k digits in total from two lists, keeping the order within each list, and arrange them to read as large a number as possible. Return that number's digits.",
        "example_input": "3 4 6 5\n9 1 2 5 8 3\n5",
        "constraints": "Input format: line 1 and line 2 are the two space-separated digit lists, line 3 is k. Output format: the k digits, space-separated.",
        "solve": _solve_create_maximum_number,
        "sample_inputs": ["3 4 6 5\n9 1 2 5 8 3\n5", "6 7\n6 0 4\n5"],
        "hidden_inputs": [
            "1\n2\n1",              # take the bigger digit
            "2\n1\n1",
            "1\n2\n2",              # take both
            "1 2\n3 4\n2",
            "9 9\n9 9\n2",          # every digit identical
            "0 0\n0 0\n3",
            "3 9\n8 9\n3",
            "1 2 3\n4 5 6\n3",
            "5 5 5\n5 5 5\n4",
            "2 5 6 4 4\n7 3 8 0 6 5\n8",
        ],
    },
]
