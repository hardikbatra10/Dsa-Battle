"""Binary Search problems."""

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

def _solve_koko_bananas(lines):
    piles = list(map(int, lines[0].split()))
    h = int(lines[1])
    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum((p + mid - 1) // mid for p in piles)
        if hours <= h:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_m_bouquets(lines):
    bloom = list(map(int, lines[0].split()))
    m = int(lines[1])
    k = int(lines[2])
    if m * k > len(bloom):
        return "-1"

    def made(day):
        total = run = 0
        for b in bloom:
            if b <= day:
                run += 1
                if run == k:
                    total += 1
                    run = 0
            else:
                run = 0
        return total

    lo, hi = min(bloom), max(bloom)
    while lo < hi:
        mid = (lo + hi) // 2
        if made(mid) >= m:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_aggressive_cows(lines):
    stalls = sorted(map(int, lines[0].split()))
    c = int(lines[1])

    def fits(gap):
        count = 1
        last = stalls[0]
        for s in stalls[1:]:
            if s - last >= gap:
                count += 1
                last = s
        return count >= c

    lo, hi = 0, stalls[-1] - stalls[0]
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if fits(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return str(best)


def _solve_min_time_trips(lines):
    times = list(map(int, lines[0].split()))
    total = int(lines[1])
    lo, hi = 1, min(times) * total
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(mid // t for t in times) >= total:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_successful_pairs(lines):
    spells = list(map(int, lines[0].split()))
    potions = sorted(map(int, lines[1].split()))
    success = int(lines[2])
    n = len(potions)
    out = []
    for s in spells:
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if potions[mid] * s >= success:
                hi = mid
            else:
                lo = mid + 1
        out.append(str(n - lo))
    return " ".join(out)


def _solve_minimize_array_max(lines):
    nums = list(map(int, lines[0].split()))
    # Value can only move left, so the answer is the largest running average.
    best = 0
    total = 0
    for i, n in enumerate(nums):
        total += n
        best = max(best, (total + i) // (i + 1))
    return str(best)


def _solve_max_candies_k_children(lines):
    candies = list(map(int, lines[0].split()))
    k = int(lines[1])
    if sum(candies) < k:
        return "0"
    lo, hi = 1, sum(candies) // k
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if sum(c // mid for c in candies) >= k:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return str(best)


def _solve_minimized_max_products(lines):
    quantities = list(map(int, lines[0].split()))
    n = int(lines[1])
    lo, hi = 1, max(quantities)
    while lo < hi:
        mid = (lo + hi) // 2
        stores = sum((q + mid - 1) // mid for q in quantities)
        if stores <= n:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_allocate_pages(lines):
    pages = list(map(int, lines[0].split()))
    students = int(lines[1])
    if students > len(pages):
        return "-1"

    def need(limit):
        count = 1
        cur = 0
        for p in pages:
            if cur + p <= limit:
                cur += p
            else:
                count += 1
                cur = p
        return count

    lo, hi = max(pages), sum(pages)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= students:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_split_array_largest_sum(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])

    def need(limit):
        count = 1
        cur = 0
        for n in nums:
            if cur + n <= limit:
                cur += n
            else:
                count += 1
                cur = n
        return count

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_ship_within_days(lines):
    weights = list(map(int, lines[0].split()))
    days = int(lines[1])

    def need(cap):
        count = 1
        cur = 0
        for w in weights:
            if cur + w <= cap:
                cur += w
            else:
                count += 1
                cur = w
        return count

    lo, hi = max(weights), sum(weights)
    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_minimize_max_pair_diff(lines):
    nums = sorted(map(int, lines[0].split()))
    p = int(lines[1])
    if p == 0:
        return "0"

    def pairs(limit):
        count = 0
        i = 0
        while i < len(nums) - 1:
            if nums[i + 1] - nums[i] <= limit:
                count += 1
                i += 2
            else:
                i += 1
        return count

    lo, hi = 0, nums[-1] - nums[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if pairs(mid) >= p:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_smallest_divisor(lines):
    nums = list(map(int, lines[0].split()))
    threshold = int(lines[1])
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        total = sum((n + mid - 1) // mid for n in nums)
        if total <= threshold:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


def _solve_magnetic_force(lines):
    positions = sorted(map(int, lines[0].split()))
    m = int(lines[1])

    def fits(gap):
        count = 1
        last = positions[0]
        for p in positions[1:]:
            if p - last >= gap:
                count += 1
                last = p
        return count >= m

    lo, hi = 1, positions[-1] - positions[0]
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if fits(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return str(best)


def _solve_max_tastiness(lines):
    prices = sorted(map(int, lines[0].split()))
    k = int(lines[1])

    def fits(gap):
        count = 1
        last = prices[0]
        for p in prices[1:]:
            if p - last >= gap:
                count += 1
                last = p
        return count >= k

    lo, hi = 0, prices[-1] - prices[0]
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if fits(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return str(best)

def _solve_search_insert_position(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    lo, hi = 0, len(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return str(lo)


def _solve_valid_perfect_square(lines):
    n = int(lines[0])
    lo, hi = 1, n
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid == n:
            return "true"
        if mid * mid < n:
            lo = mid + 1
        else:
            hi = mid - 1
    return "false"


def _solve_arranging_coins(lines):
    n = int(lines[0])
    lo, hi = 0, n
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * (mid + 1) // 2 <= n:
            lo = mid + 1
        else:
            hi = mid - 1
    return str(hi)


def _solve_next_greatest_letter(lines):
    letters = lines[0].split()
    target = lines[1]
    lo, hi = 0, len(letters)
    while lo < hi:
        mid = (lo + hi) // 2
        if letters[mid] <= target:
            lo = mid + 1
        else:
            hi = mid
    return letters[lo % len(letters)]


def _solve_peak_index_mountain(lines):
    nums = list(map(int, lines[0].split()))
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return str(lo)


def _solve_count_negatives_matrix(lines):
    m, n = map(int, lines[0].split())
    total = 0
    for i in range(m):
        row = list(map(int, lines[1 + i].split()))
        lo, hi = 0, n
        while lo < hi:
            mid = (lo + hi) // 2
            if row[mid] < 0:
                hi = mid
            else:
                lo = mid + 1
        total += n - lo
    return str(total)


def _solve_n_and_double_exist(lines):
    nums = list(map(int, lines[0].split()))
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j and nums[i] == 2 * nums[j]:
                return "true"
    return "false"


def _solve_intersection_two_arrays(lines):
    a = set(map(int, lines[0].split()))
    b = set(map(int, lines[1].split()))
    return " ".join(str(v) for v in sorted(a & b))


def _solve_distance_value(lines):
    a = list(map(int, lines[0].split()))
    b = list(map(int, lines[1].split()))
    d = int(lines[2])
    count = 0
    for x in a:
        if all(abs(x - y) > d for y in b):
            count += 1
    return str(count)


def _solve_first_last_position(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    import bisect
    lo = bisect.bisect_left(nums, target)
    hi = bisect.bisect_right(nums, target) - 1
    if lo >= len(nums) or nums[lo] != target:
        return "-1 -1"
    return f"{lo} {hi}"


def _solve_min_rotated(lines):
    nums = list(map(int, lines[0].split()))
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return str(nums[lo])


def _solve_search_2d_matrix(lines):
    m, n = map(int, lines[0].split())
    grid = [list(map(int, lines[1 + i].split())) for i in range(m)]
    target = int(lines[1 + m])
    lo, hi = 0, m * n - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = grid[mid // n][mid % n]
        if v == target:
            return "true"
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return "false"


def _solve_min_rotated_ii(lines):
    nums = list(map(int, lines[0].split()))
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        elif nums[mid] < nums[hi]:
            hi = mid
        else:
            hi -= 1
    return str(nums[lo])


def _solve_search_rotated_ii(lines):
    nums = list(map(int, lines[0].split()))
    target = int(lines[1])
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return "true"
        if nums[lo] == nums[mid] == nums[hi]:
            lo += 1
            hi -= 1
        elif nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return "false"


def _solve_kth_multiplication_table(lines):
    m, n, k = map(int, lines[0].split())
    lo, hi = 1, m * n
    while lo < hi:
        mid = (lo + hi) // 2
        count = 0
        for i in range(1, m + 1):
            count += min(n, mid // i)
        if count >= k:
            hi = mid
        else:
            lo = mid + 1
    return str(lo)


PROBLEMS = [
{
        "title": "Binary Search",
        "topic": "binary_search",
        "difficulty": "easy",
        "description": "Given a sorted array of distinct integers and a target, return the index of target, or -1 if it isn't present.",
        "example_input": "-1 0 3 5 9 12\n9",
        "constraints": "Input format: line 1 is the sorted array, line 2 is the target. Output format: a single integer.",
        "solve": _solve_binary_search,
        "sample_inputs": ["-1 0 3 5 9 12\n9", "2 4 6 8 10\n8"],
        "hidden_inputs": [
            "5\n5",              # single element, found
            "5\n-5",             # single element, absent
            "1 2\n2",
            "1 2 3 4 5\n1",      # first index
            "1 2 3 4 5\n5",      # last index
            "1 2 3 4 5\n3",      # exact middle
            "1 2 3 4 5\n0",      # below the whole range
            "1 2 3 4 5\n6",      # above the whole range
            "1 2 3 4 5 6\n6",    # even length, last index
            "-10 -5 0 5 10\n-10",
            "-10 -5 0 5 10\n0",  # zero as a target among negatives
            "-1 0 3 5 9 12\n2",
            "1 3 5 7 9 11 13\n7",
        ],
    },
{
        "title": "Search in Rotated Sorted Array",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Given a sorted array of distinct integers rotated at an unknown pivot, and a target, return its index, or -1 if not present.",
        "example_input": "4 5 6 7 0 1 2\n0",
        "constraints": "Input format: line 1 is the rotated array, line 2 is the target. Output format: a single integer.",
        "solve": _solve_search_rotated,
        "sample_inputs": ["4 5 6 7 0 1 2\n0", "7 8 1 2 3\n8"],
        "hidden_inputs": [
            "1\n1",              # single element, found
            "1\n0",              # single element, absent
            "3 1\n1",
            "1 3\n3",
            "1 2 3 4 5\n1",      # rotation offset of zero
            "1 2 3 4 5\n5",
            "5 1 2 3 4\n1",      # pivot right after the start
            "2 3 4 5 1\n1",      # pivot at the very end
            "4 5 6 7 0 1 2\n4",  # first index
            "4 5 6 7 0 1 2\n2",  # last index
            "4 5 6 7 0 1 2\n7",  # element just before the pivot
            "4 5 6 7 0 1 2\n3",  # absent, falls inside the rotation gap
            "6 7 8 1 2 3 4 5\n8",
        ],
    },
{
        "title": "Median of Two Sorted Arrays",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Given two sorted arrays, return the median of the combined dataset. Print it as an integer if it's a whole number, otherwise with exactly one decimal place.",
        "example_input": "1 3\n2",
        "constraints": "Input format: line 1 and line 2 are the two sorted arrays, space-separated. Output format: the median, formatted as described above.",
        "solve": _solve_median_two_arrays,
        "sample_inputs": ["1 3\n2", "1 2 5\n3 4"],
        "hidden_inputs": [
            "2\n",               # second array empty
            "\n1",               # first array empty
            "1\n1",
            "1\n2",              # even total, fractional median
            "1 2\n3 4",
            "0 0\n0 0",
            "1 1 1\n1 1 1",      # every value identical
            "1 2 3\n4",          # arrays do not overlap
            "-5 -3 -1\n-2 0 2",  # negative fractional median
            "100000\n100001",
            "1 2 3 4 5\n6 7 8 9 10",
        ],
    },
{
        "title": "Koko Eating Bananas",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "There are piles of bananas and h hours available. Each hour a fixed number of bananas k can be eaten from a single pile; if that pile has fewer than k left, the rest of the hour is wasted. Return the smallest k that finishes every pile within h hours.",
        "example_input": "3 6 7 11\n8",
        "constraints": "Input format: line 1 is the space-separated pile sizes, line 2 is h (h >= number of piles). Output format: a single integer.",
        "solve": _solve_koko_bananas,
        "sample_inputs": ["3 6 7 11\n8", "30 11 23 4 20\n5"],
        "hidden_inputs": [
            "1\n1",                 # one pile, one hour
            "1\n100",               # far more time than needed, k is still 1
            "5\n5",                 # k of 1 exactly fits
            "5\n1",                 # a single hour forces the whole pile
            "2 2\n2",               # one hour per pile
            "1 1 1 1\n4",
            "10 10 10\n3",
            "30 11 23 4 20\n6",
            "312884470\n968709470", # single huge pile, abundant time
            "1000000000\n2",
            "3 6 7 11\n4",          # exactly one hour per pile
        ],
    },
{
        "title": "Minimum Number of Days to Make m Bouquets",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Flower i blooms on day bloom[i]. A bouquet needs k adjacent flowers that have all bloomed. Return the earliest day on which m bouquets can be made, or -1 if it is impossible.",
        "example_input": "1 10 3 10 2\n3\n1",
        "constraints": "Input format: line 1 is the space-separated bloom days, line 2 is m, line 3 is k. Output format: a single integer, or -1.",
        "solve": _solve_m_bouquets,
        "sample_inputs": ["1 10 3 10 2\n3\n1", "1 10 3 10 2\n3\n2"],
        "hidden_inputs": [
            "1\n1\n1",              # smallest possible yes
            "1\n2\n1",              # not enough flowers, impossible
            "1 2\n1\n3",            # k larger than the garden
            "5 5 5\n3\n1",          # all bloom the same day
            "1 2 3\n3\n1",          # last day governs
            "7 7 7 7\n2\n2",
            "1 10 2 9 3 8\n2\n2",   # adjacency matters, not just counts
            "1 10 3 10 2\n2\n2",
            "10 1 10 1 10\n2\n1",
            "9 9 9 9 9 9 9 9 9 9\n5\n2",
            "1 2 4 9 3 4 1\n2\n2",
        ],
    },
{
        "title": "Aggressive Cows",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Given stall positions along a line and c cows, place the cows in distinct stalls so that the smallest distance between any two of them is as large as possible. Return that largest possible minimum distance.",
        "example_input": "1 2 4 8 9\n3",
        "constraints": "Input format: line 1 is the space-separated stall positions, line 2 is c (2 <= c <= number of stalls). Output format: a single integer.",
        "solve": _solve_aggressive_cows,
        "sample_inputs": ["1 2 4 8 9\n3", "1 2 3\n2"],
        "hidden_inputs": [
            "1 2\n2",               # only one placement possible
            "1 1000000\n2",         # far apart
            "5 5 5\n2",             # duplicate positions give distance 0
            "1 2 3 4 5\n5",         # every stall used
            "1 2 3 4 5\n2",         # both ends
            "1 2 3 4 5\n3",
            "0 3 4 7 10 9\n4",
            "10 1 2 7 5\n3",
            "1 2 8 4 9\n3",
            "1 3 5 7 9 11\n4",
            "2 4 6 8 10 12 14\n3",
        ],
    },
{
        "title": "Minimum Time to Complete Trips",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Bus i takes time[i] to complete one trip and starts its next trip immediately. Return the least amount of time needed for the buses to complete at least totalTrips trips between them.",
        "example_input": "1 2 3\n5",
        "constraints": "Input format: line 1 is the space-separated trip times, line 2 is totalTrips. Output format: a single integer.",
        "solve": _solve_min_time_trips,
        "sample_inputs": ["1 2 3\n5", "2\n1"],
        "hidden_inputs": [
            "1\n1",                 # one bus, one trip
            "1\n10",                # one bus, many trips
            "5\n1",                 # one trip on a slow bus
            "2 2\n2",               # both buses finish together
            "1 1 1\n3",
            "3 3 3\n1",             # any single bus suffices
            "1 2 3\n6",
            "5 10 10\n9",
            "10 10 10\n10",
            "2 3 5 7\n100",
            "1 100\n2",             # one very slow bus is never used
        ],
    },
{
        "title": "Successful Pairs of Spells and Potions",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "A spell and a potion form a successful pair when the product of their strengths is at least success. For every spell, report how many potions form a successful pair with it.",
        "example_input": "5 1 3\n1 2 3 4 5\n7",
        "constraints": "Input format: line 1 is the space-separated spell strengths, line 2 is the space-separated potion strengths, line 3 is success. Output format: one count per spell, space-separated.",
        "solve": _solve_successful_pairs,
        "sample_inputs": ["5 1 3\n1 2 3 4 5\n7", "3 1 2\n8 5 8\n16"],
        "hidden_inputs": [
            "1\n1\n1",              # exactly meets the threshold
            "1\n1\n2",              # falls just short
            "1\n1 1 1\n1",          # every potion works
            "5\n1 2 3\n100",        # no potion works
            "1 2 3\n1\n1",          # a single potion
            "10 10\n10 10\n100",    # boundary equality for all
            "2 2 2\n2 2 2\n4",
            "1 2 3 4 5\n5 4 3 2 1\n10",
            "3 1 2\n8 5 8\n17",     # one above the previous threshold
            "100 1\n1 100\n100",
            "1 1 1 1\n1 1 1 1\n2",  # nothing qualifies anywhere
        ],
    },
{
        "title": "Minimize Maximum of Array",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Repeatedly you may take 1 from any element at a positive index and add it to the element immediately before it. Return the smallest possible value of the array's maximum after any number of such moves.",
        "example_input": "3 7 1 6",
        "constraints": "Input format: one line of space-separated non-negative integers. Output format: a single integer.",
        "solve": _solve_minimize_array_max,
        "sample_inputs": ["3 7 1 6", "10 1"],
        "hidden_inputs": [
            "0",                    # single zero
            "5",                    # single element cannot change
            "0 0 0",
            "1 1 1",                # already flat
            "0 10",                 # value flows left and halves
            "10 0",                 # value cannot flow right
            "0 0 9",
            "5 5 5 5",
            "1 2 3 4 5",            # increasing, prefix averages rise
            "5 4 3 2 1",            # decreasing, the first element dominates
            "1000000000 0",
        ],
    },
{
        "title": "Maximum Candies Allocated to K Children",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Each pile of candies may be split into sub-piles of equal size, but piles may not be merged. Every one of the k children must receive the same number of candies from a single pile. Return the largest number each child can get, or 0 if it cannot be done.",
        "example_input": "5 8 6\n3",
        "constraints": "Input format: line 1 is the space-separated pile sizes, line 2 is k. Output format: a single integer.",
        "solve": _solve_max_candies_k_children,
        "sample_inputs": ["5 8 6\n3", "2 5\n11"],
        "hidden_inputs": [
            "1\n1",                 # one pile, one child
            "1\n2",                 # not enough candy, answer 0
            "3 7\n20",              # far too many children
            "10\n1",                # a single child takes the whole pile
            "10\n10",
            "1 1 1\n3",             # exactly one each
            "4 4 4\n3",
            "5 8 6\n4",
            "100\n7",               # does not divide evenly
            "9 9 9 9\n6",
            "1000000000\n1000",
        ],
    },
{
        "title": "Minimized Maximum of Products Distributed to Any Store",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "There are n stores and several product types, with quantities[i] units of type i. Each store may receive units of at most one product type. Distribute everything so that the largest number of units given to any single store is as small as possible, and return that number.",
        "example_input": "11 6\n6",
        "constraints": "Input format: line 1 is the space-separated quantities, line 2 is n (n >= number of product types). Output format: a single integer.",
        "solve": _solve_minimized_max_products,
        "sample_inputs": ["11 6\n6", "15 10 10\n7"],
        "hidden_inputs": [
            "1\n1",                 # one product, one store
            "10\n1",                # one store takes everything
            "10\n10",               # one unit per store
            "10\n100",              # more stores than units
            "1 1 1\n3",
            "2 2 2\n3",             # each type to its own store
            "100 100\n2",
            "11 6\n7",
            "15 10 10\n8",
            "7 7 7 7\n8",
            "1000000000\n1000",
        ],
    },
{
        "title": "Allocate Minimum Number of Pages",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Books are arranged in a row and must be handed out to students as contiguous blocks, each student getting at least one book. Minimise the largest number of pages any single student receives, and return that number. Return -1 if there are more students than books.",
        "example_input": "12 34 67 90\n2",
        "constraints": "Input format: line 1 is the space-separated page counts, line 2 is the number of students. Output format: a single integer, or -1.",
        "solve": _solve_allocate_pages,
        "sample_inputs": ["12 34 67 90\n2", "15 17 20\n2"],
        "hidden_inputs": [
            "10\n1",                # one book, one student
            "10\n2",                # more students than books
            "10 20\n2",             # one book each
            "10 20\n1",             # one student takes both
            "5 5 5 5\n2",
            "1 1 1 1 1\n5",
            "12 34 67 90\n3",
            "12 34 67 90\n4",       # every student gets one book
            "100 1 1 1\n2",         # one dominant book sets the floor
            "1 2 3 4 5 6 7 8 9\n3",
            "20 20 20 20 20\n3",
        ],
    },
{
        "title": "Split Array Largest Sum",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Split the array into exactly k non-empty contiguous subarrays so that the largest subarray sum is as small as possible, and return that sum.",
        "example_input": "7 2 5 10 8\n2",
        "constraints": "Input format: line 1 is the space-separated non-negative integers, line 2 is k (1 <= k <= array length). Output format: a single integer.",
        "solve": _solve_split_array_largest_sum,
        "sample_inputs": ["7 2 5 10 8\n2", "1 2 3 4 5\n2"],
        "hidden_inputs": [
            "1\n1",                 # single element
            "5 5\n1",               # one part, the whole sum
            "5 5\n2",               # one element each
            "1 1 1 1\n4",
            "0 0 0\n2",             # zeros
            "1 4 4\n3",
            "7 2 5 10 8\n3",
            "7 2 5 10 8\n5",        # k equals the length, answer is the max
            "100 1 1 1\n2",         # one dominant element sets the floor
            "2 3 1 2 4 3\n3",
            "1 2 3 4 5 6 7 8 9 10\n4",
        ],
    },
{
        "title": "Capacity to Ship Packages Within D Days",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Packages must be shipped in their given order within d days. Each day the ship loads packages in sequence without exceeding its capacity. Return the smallest capacity that gets everything shipped in time.",
        "example_input": "1 2 3 4 5 6 7 8 9 10\n5",
        "constraints": "Input format: line 1 is the space-separated package weights, line 2 is d (1 <= d <= number of packages). Output format: a single integer.",
        "solve": _solve_ship_within_days,
        "sample_inputs": ["1 2 3 4 5 6 7 8 9 10\n5", "3 2 2 4 1 4\n3"],
        "hidden_inputs": [
            "1\n1",                 # single package
            "10\n1",
            "5 5\n2",               # one per day
            "5 5\n1",               # both in one day
            "1 1 1 1 1\n5",
            "1 2 3 4 5\n1",         # capacity is the total
            "1 2 3 4 5\n5",         # capacity is the max element
            "3 2 2 4 1 4\n4",
            "10 1 1 1\n2",          # one heavy package sets the floor
            "1 2 3 1 1\n4",
            "1 2 3 4 5 6 7 8 9 10\n7",
        ],
    },
{
        "title": "Minimize the Maximum Difference of Pairs",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Choose p disjoint pairs of indices from the array. Minimise the largest absolute difference within any chosen pair, and return that value.",
        "example_input": "10 1 2 7 1 3\n2",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is p (0 <= p <= half the array length). Output format: a single integer.",
        "solve": _solve_minimize_max_pair_diff,
        "sample_inputs": ["10 1 2 7 1 3\n2", "4 2 1 2\n1"],
        "hidden_inputs": [
            "1 2\n0",               # zero pairs required
            "1\n0",                 # single element, nothing to pair
            "1 1\n1",               # identical values pair at zero cost
            "1 5\n1",               # only one possible pair
            "1 2 3 4\n2",           # pair the neighbours
            "1 1 1 1\n2",
            "0 5 0 5\n2",
            "10 1 2 7 1 3\n3",      # every element used
            "1 100 2 99\n2",        # greedy adjacency beats the obvious split
            "3 4 2 3 2 1 2\n3",
            "1 2 3 4 5 6 7 8\n4",
        ],
    },
{
        "title": "Find the Smallest Divisor Given a Threshold",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Pick a positive integer divisor, divide every element by it rounding each result up, and sum those results. Return the smallest divisor for which that sum is at most the given threshold.",
        "example_input": "1 2 5 9\n6",
        "constraints": "Input format: line 1 is the space-separated positive integers, line 2 is the threshold (threshold >= array length). Output format: a single integer.",
        "solve": _solve_smallest_divisor,
        "sample_inputs": ["1 2 5 9\n6", "44 22 33 11 1\n5"],
        "hidden_inputs": [
            "1\n1",                 # divisor of 1 already fits
            "10\n1",                # must divide down to a single unit
            "5\n5",
            "1 1 1\n3",             # threshold equals the length
            "2 2 2\n3",             # rounding up forces a bigger divisor
            "9\n2",
            "1 2 5 9\n4",           # threshold equals the array length
            "1 2 5 9\n17",          # loosest possible threshold
            "21212 10101 12121 30202\n1000000",
            "19 19 19\n3",
            "1000000 1\n2",
        ],
    },
{
        "title": "Magnetic Force Between Two Balls",
        "topic": "binary_search",
        "difficulty": "hard",
        "description": "Given basket positions along a line, place m balls in distinct baskets so that the smallest distance between any two balls is as large as possible. Return that largest possible minimum distance.",
        "example_input": "1 2 3 4 7\n3",
        "constraints": "Input format: line 1 is the space-separated basket positions, line 2 is m (2 <= m <= number of baskets). Output format: a single integer.",
        "solve": _solve_magnetic_force,
        "sample_inputs": ["1 2 3 4 7\n3", "5 4 3 2 1 1000000000\n2"],
        "hidden_inputs": [
            "1 2\n2",               # only one placement
            "1 1000000000\n2",      # extreme span
            "1 2 3\n3",             # every basket used
            "1 2 3\n2",             # both ends
            "1 2 3 4 5 6\n3",
            "1 2 3 4 7\n2",
            "1 2 3 4 7\n4",
            "0 10 20 30 40\n3",
            "1 5 6 9 13\n3",
            "2 4 8 16 32\n4",
            "1 3 5 7 9 11 13\n5",
        ],
    },
{
        "title": "Maximum Tastiness of Candy Basket",
        "topic": "binary_search",
        "difficulty": "medium",
        "description": "Choose k different candies from the given prices. The tastiness of the basket is the smallest absolute price difference between any two chosen candies. Return the largest tastiness achievable.",
        "example_input": "13 5 1 8 21 2\n3",
        "constraints": "Input format: line 1 is the space-separated prices, line 2 is k (2 <= k <= number of candies). Output format: a single integer.",
        "solve": _solve_max_tastiness,
        "sample_inputs": ["13 5 1 8 21 2\n3", "1 3 1\n2"],
        "hidden_inputs": [
            "1 2\n2",               # only one choice
            "5 5\n2",               # identical prices give 0
            "1 1 1\n3",             # all identical
            "1 2 3\n3",             # every candy chosen
            "1 2 3\n2",             # the two extremes
            "7 7 7 7\n2",
            "13 5 1 8 21 2\n2",
            "13 5 1 8 21 2\n4",
            "1 10 100 1000\n3",     # widely spread prices
            "2 4 6 8 10\n4",
            "1 2 4 8 16 32\n3",
        ],
    },
{
        "title": "Search Insert Position",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Given a sorted list of distinct values and a target, return the position of the target, or the position where it would have to be inserted to keep the list sorted.",
        "example_input": "1 3 5 6\n5",
        "constraints": "Input format: line 1 is the sorted distinct integers, line 2 is the target. Output format: a single integer.",
        "solve": _solve_search_insert_position,
        "sample_inputs": ["1 3 5 6\n5", "1 3 5 6\n2"],
        "hidden_inputs": [
            "1\n1",                 # found, single element
            "1\n0",                 # insert before
            "1\n2",                 # insert after
            "1 3\n2",               # insert between
            "1 3 5 6\n7",           # past the end
            "1 3 5 6\n0",           # before the start
            "1 3 5 6\n6",           # the last element
            "1 3 5 6\n1",           # the first element
            "-5 -3 -1\n-2",         # negatives
            "2 4 6 8 10\n7",
        ],
    },
{
        "title": "Valid Perfect Square",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Decide whether a positive integer is the square of some whole number, without using any built-in square-root function.",
        "example_input": "16",
        "constraints": "Input format: one line containing a positive integer. Output format: \"true\" or \"false\".",
        "solve": _solve_valid_perfect_square,
        "sample_inputs": ["16", "14"],
        "hidden_inputs": [
            "1",                    # one is a square
            "2",
            "3",
            "4",
            "8",
            "9",
            "15",                   # one below a square
            "25",
            "808201",               # a large exact square
            "2147395600",           # the largest square inside 32-bit
        ],
    },
{
        "title": "Arranging Coins",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Coins are stacked in rows, the first row holding one coin, the second two, and so on. Return how many rows can be filled completely with the coins available.",
        "example_input": "5",
        "constraints": "Input format: one line containing the number of coins (at least 0). Output format: a single integer.",
        "solve": _solve_arranging_coins,
        "sample_inputs": ["5", "8"],
        "hidden_inputs": [
            "0",                    # no coins, no rows
            "1",                    # exactly one row
            "2",                    # the second row is short
            "3",                    # two complete rows
            "4",
            "6",                    # three complete rows
            "9",
            "10",                   # four complete rows
            "1000000",
            "2147483647",           # the 32-bit maximum
        ],
    },
{
        "title": "Find Smallest Letter Greater Than Target",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Given letters in alphabetical order and a target letter, return the smallest letter in the list that comes strictly after the target. The letters wrap around, so if none does, return the first letter.",
        "example_input": "c f j\na",
        "constraints": "Input format: line 1 is the space-separated letters in order, line 2 is the target letter. Output format: a single letter.",
        "solve": _solve_next_greatest_letter,
        "sample_inputs": ["c f j\na", "c f j\nj"],
        "hidden_inputs": [
            "a b\nz",               # wraps to the first letter
            "a b\na",
            "c f j\nc",             # the target itself is skipped
            "c f j\nd",
            "c f j\ng",
            "c f j\nk",             # past every letter, wraps
            "x x y y\nx",           # duplicates are skipped together
            "e e e e\ne",           # every letter equals the target
            "a c f h\nb",
            "a a b b c c\nb",
        ],
    },
{
        "title": "Peak Index in a Mountain Array",
        "topic": "binary_search", "difficulty": "easy",
        "description": "The values rise strictly to a single highest point and then fall strictly away from it. Return the position of that highest point.",
        "example_input": "0 1 0",
        "constraints": "Input format: one line of space-separated integers forming a single rise then fall. Output format: a single integer.",
        "solve": _solve_peak_index_mountain,
        "sample_inputs": ["0 1 0", "0 2 1 0"],
        "hidden_inputs": [
            "1 2 1",                # the smallest mountain
            "0 10 5 2",             # the peak sits early
            "3 4 5 1",
            "1 3 5 7 2",            # the peak sits late
            "0 1 2 3 4 5 1",
            "5 6 0",
            "24 69 100 99 79 78 67 36 26 19",
            "1 2 3 4 5 4 3 2 1",    # the peak is exactly central
            "-5 -1 -3",             # negatives
            "0 1 2 3 4 5 6 7 8 9 1",
        ],
    },
{
        "title": "Count Negative Numbers in a Sorted Matrix",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Every row and every column of a grid is in non-increasing order. Count how many of its values are below zero.",
        "example_input": "4 4\n4 3 2 -1\n3 2 1 -1\n1 1 -1 -2\n-1 -1 -2 -3",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of integers in non-increasing order both across and down. Output format: a single integer.",
        "solve": _solve_count_negatives_matrix,
        "sample_inputs": ["4 4\n4 3 2 -1\n3 2 1 -1\n1 1 -1 -2\n-1 -1 -2 -3", "2 2\n3 2\n1 0"],
        "hidden_inputs": [
            "1 1\n1",               # nothing negative
            "1 1\n-1",              # everything negative
            "1 1\n0",               # zero does not count
            "1 4\n3 2 -1 -2",       # a single row
            "4 1\n3\n2\n-1\n-2",    # a single column
            "2 2\n0 0\n0 0",
            "2 2\n-1 -1\n-1 -1",
            "3 3\n5 4 3\n2 1 0\n-1 -2 -3",
            "3 2\n1 -1\n0 -2\n-3 -4",
            "2 4\n5 1 0 -1\n-1 -2 -3 -4",
        ],
    },
{
        "title": "Check If N and Its Double Exist",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Decide whether the list holds two values at different positions where one is exactly twice the other.",
        "example_input": "10 2 5 3",
        "constraints": "Input format: one line of space-separated integers. Output format: \"true\" or \"false\".",
        "solve": _solve_n_and_double_exist,
        "sample_inputs": ["10 2 5 3", "3 1 7 11"],
        "hidden_inputs": [
            "1",                    # a single value cannot pair
            "0",                    # zero alone
            "0 0",                  # zero is its own double
            "1 2",
            "2 1",                  # order must not matter
            "1 3",
            "-2 -4",                # negatives work too
            "-10 12 -20 -8 15",
            "7 1 14 11",
            "3 1 4 1 5",            # no doubling pair
        ],
    },
{
        "title": "Intersection of Two Arrays",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Return the values that appear in both lists, each listed once, in increasing order.",
        "example_input": "1 2 2 1\n2 2",
        "constraints": "Input format: line 1 and line 2 are the two space-separated lists. Output format: the shared values ascending, space-separated (empty if none).",
        "solve": _solve_intersection_two_arrays,
        "sample_inputs": ["1 2 2 1\n2 2", "4 9 5\n9 4 9 8 4"],
        "hidden_inputs": [
            "1\n1",                 # a single shared value
            "1\n2",                 # nothing shared
            "1 1\n1 1",             # repeats collapse to one
            "1 2\n2 3",
            "1 2 3\n3 2 1",         # the same set, reordered
            "0 0\n0",               # zero
            "-1 -2\n-2 -3",         # negatives
            "1 2 3\n4 5 6",
            "5 5 5 5\n5",
            "1 2 3 4 5\n5 4 3 2 1",
        ],
    },
{
        "title": "Find the Distance Value Between Two Arrays",
        "topic": "binary_search", "difficulty": "easy",
        "description": "Count the values in the first list for which no value in the second list lies within the given distance.",
        "example_input": "4 5 8\n10 9 1 8\n2",
        "constraints": "Input format: line 1 and line 2 are the two space-separated lists, line 3 is the distance. Output format: a single integer.",
        "solve": _solve_distance_value,
        "sample_inputs": ["4 5 8\n10 9 1 8\n2", "1 4 2 3\n-4 -3 6 10 20 30\n3"],
        "hidden_inputs": [
            "1\n1\n0",              # the same value, distance zero
            "1\n2\n0",              # differ by one, distance zero
            "1\n1\n1",
            "1\n5\n1",              # far enough apart
            "0 0\n0\n0",
            "1 2 3\n10\n1",         # nothing is close
            "1 2 3\n1 2 3\n0",      # every value is matched
            "-1 -2\n1 2\n1",        # negatives
            "2 1 100 3\n-5 -2 10 -3 7\n6",
            "1 4 2 3\n-4 -3 6 10 20 30\n2",
        ],
    },
{
        "title": "Find First and Last Position of Element in Sorted Array",
        "topic": "binary_search", "difficulty": "medium",
        "description": "Given a sorted list which may repeat values, return the first and last positions at which the target appears, or -1 -1 if it does not appear at all.",
        "example_input": "5 7 7 8 8 10\n8",
        "constraints": "Input format: line 1 is the sorted integers, line 2 is the target. Output format: two integers, space-separated.",
        "solve": _solve_first_last_position,
        "sample_inputs": ["5 7 7 8 8 10\n8", "5 7 7 8 8 10\n6"],
        "hidden_inputs": [
            "1\n1",                 # a single match
            "1\n2",                 # absent
            "1 1\n1",               # both positions
            "1 2\n1",               # the first only
            "1 2\n2",               # the last only
            "2 2 2\n2",             # the whole list
            "1 2 3\n0",             # below the range
            "1 2 3\n4",             # above the range
            "-3 -1 -1 0\n-1",       # negatives
            "1 1 2 2 3 3 3 4\n3",
        ],
    },
{
        "title": "Find Minimum in Rotated Sorted Array",
        "topic": "binary_search", "difficulty": "medium",
        "description": "A sorted list of distinct values has been rotated some number of places. Return its smallest value.",
        "example_input": "3 4 5 1 2",
        "constraints": "Input format: one line of space-separated distinct integers, sorted then rotated. Output format: a single integer.",
        "solve": _solve_min_rotated,
        "sample_inputs": ["3 4 5 1 2", "4 5 6 7 0 1 2"],
        "hidden_inputs": [
            "1",                    # a single value
            "1 2",                  # not rotated at all
            "2 1",                  # rotated by one
            "1 2 3",
            "3 1 2",
            "2 3 1",                # the minimum sits last
            "1 2 3 4 5",
            "5 1 2 3 4",            # the minimum sits second
            "-5 -3 -1",             # negatives
            "11 13 15 17 1 3 5",
        ],
    },
{
        "title": "Search a 2D Matrix",
        "topic": "binary_search", "difficulty": "medium",
        "description": "Each row of a grid is in increasing order, and the first value of every row is larger than the last value of the row above. Decide whether the target appears anywhere in it.",
        "example_input": "3 4\n1 3 5 7\n10 11 16 20\n23 30 34 60\n3",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many grid lines, then a final line holding the target. Output format: \"true\" or \"false\".",
        "solve": _solve_search_2d_matrix,
        "sample_inputs": ["3 4\n1 3 5 7\n10 11 16 20\n23 30 34 60\n3", "3 4\n1 3 5 7\n10 11 16 20\n23 30 34 60\n13"],
        "hidden_inputs": [
            "1 1\n1\n1",            # found, single cell
            "1 1\n1\n2",            # absent, single cell
            "1 3\n1 2 3\n2",        # a single row
            "3 1\n1\n2\n3\n3",      # a single column
            "2 2\n1 2\n3 4\n1",     # the very first value
            "2 2\n1 2\n3 4\n4",     # the very last value
            "2 2\n1 2\n3 4\n0",     # below everything
            "2 2\n1 2\n3 4\n5",     # above everything
            "2 3\n1 3 5\n7 9 11\n7",    # the first value of a later row
            "3 3\n-9 -6 -3\n0 3 6\n9 12 15\n0",
        ],
    },
{
        "title": "Find Minimum in Rotated Sorted Array II",
        "topic": "binary_search", "difficulty": "hard",
        "description": "A sorted list, which may repeat values, has been rotated some number of places. Return its smallest value.",
        "example_input": "2 2 2 0 1",
        "constraints": "Input format: one line of space-separated integers, sorted then rotated, possibly with repeats. Output format: a single integer.",
        "solve": _solve_min_rotated_ii,
        "sample_inputs": ["2 2 2 0 1", "1 3 5"],
        "hidden_inputs": [
            "1",                    # a single value
            "1 1",                  # every value identical
            "1 1 1",
            "3 1",                  # rotated by one
            "1 3 3",
            "3 3 1 3",              # repeats straddle the rotation
            "10 1 10 10 10",        # the minimum is hidden among repeats
            "2 2 2 2 2 2 1",        # the minimum is last
            "1 2 2 2 2 2 2",        # not rotated, heavy repeats
            "4 5 6 7 0 1 4",
        ],
    },
{
        "title": "Search in Rotated Sorted Array II",
        "topic": "binary_search", "difficulty": "hard",
        "description": "A sorted list, which may repeat values, has been rotated some number of places. Decide whether the target appears in it.",
        "example_input": "2 5 6 0 0 1 2\n0",
        "constraints": "Input format: line 1 is the rotated integers, line 2 is the target. Output format: \"true\" or \"false\".",
        "solve": _solve_search_rotated_ii,
        "sample_inputs": ["2 5 6 0 0 1 2\n0", "2 5 6 0 0 1 2\n3"],
        "hidden_inputs": [
            "1\n1",                 # found, single element
            "1\n0",                 # absent, single element
            "1 1\n1",
            "1 1 1\n2",             # all identical, absent
            "1 0 1 1 1\n0",         # the classic duplicate trap
            "1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 1\n0",
            "2 2 2 3 2 2 2\n3",
            "3 1\n1",
            "1 3\n3",
            "4 5 6 7 0 1 2\n5",
        ],
    },
{
        "title": "Kth Smallest Number in Multiplication Table",
        "topic": "binary_search", "difficulty": "hard",
        "description": "In a grid where the value at row i and column j is their product, return the kth smallest value, counting repeats separately.",
        "example_input": "3 3 5",
        "constraints": "Input format: one line holding the number of rows, the number of columns, and k. Output format: a single integer.",
        "solve": _solve_kth_multiplication_table,
        "sample_inputs": ["3 3 5", "2 3 6"],
        "hidden_inputs": [
            "1 1 1",                # a single cell
            "1 5 1",                # a single row, the smallest
            "1 5 5",                # a single row, the largest
            "5 1 3",                # a single column
            "2 2 1",
            "2 2 4",                # the largest in a small table
            "3 3 1",
            "3 3 9",                # the largest overall
            "9 9 41",
            "42 34 401",
        ],
    },
]
