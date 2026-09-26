"""Stack Queue problems."""

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

def _solve_remove_duplicate_letters(lines):
    s = lines[0]
    last = {ch: i for i, ch in enumerate(s)}
    stack = []
    seen = set()
    for i, ch in enumerate(s):
        if ch in seen:
            continue
        while stack and stack[-1] > ch and last[stack[-1]] > i:
            seen.discard(stack.pop())
        stack.append(ch)
        seen.add(ch)
    return "".join(stack)


def _solve_decode_string(lines):
    s = lines[0]
    counts = []
    parts = [""]
    num = ""
    for ch in s:
        if ch.isdigit():
            num += ch
        elif ch == "[":
            counts.append(int(num))
            num = ""
            parts.append("")
        elif ch == "]":
            chunk = parts.pop() * counts.pop()
            parts[-1] += chunk
        else:
            parts[-1] += ch
    return parts[0]


def _solve_freq_stack(lines):
    q = int(lines[0])
    from collections import defaultdict
    freq = defaultdict(int)
    groups = defaultdict(list)
    max_freq = 0
    out = []
    for i in range(1, q + 1):
        parts = lines[i].split()
        if parts[0] == "push":
            v = int(parts[1])
            freq[v] += 1
            max_freq = max(max_freq, freq[v])
            groups[freq[v]].append(v)
        else:
            v = groups[max_freq].pop()
            freq[v] -= 1
            if not groups[max_freq]:
                max_freq -= 1
            out.append(str(v))
    return " ".join(out)


def _solve_simplify_path(lines):
    path = lines[0]
    stack = []
    for part in path.split("/"):
        if part == "" or part == ".":
            continue
        if part == "..":
            if stack:
                stack.pop()
        else:
            stack.append(part)
    return "/" + "/".join(stack)


def _solve_car_fleet(lines):
    target = int(lines[0])
    pos = list(map(int, lines[1].split()))
    speed = list(map(int, lines[2].split()))
    cars = sorted(zip(pos, speed), reverse=True)
    fleets = 0
    # -inf, not 0: a car already standing on the target arrives at t=0 and is
    # still a fleet of its own. Seeding 0.0 here silently swallows it.
    slowest = float("-inf")
    for p, s in cars:
        t = (target - p) / s
        if t > slowest:
            fleets += 1
            slowest = t
    return str(fleets)


def _solve_asteroid_collision(lines):
    asteroids = list(map(int, lines[0].split()))
    stack = []
    for a in asteroids:
        alive = True
        while alive and a < 0 and stack and stack[-1] > 0:
            if stack[-1] < -a:
                stack.pop()
                continue
            if stack[-1] == -a:
                stack.pop()
            alive = False
        if alive:
            stack.append(a)
    return " ".join(map(str, stack))


def _solve_eval_rpn(lines):
    tokens = lines[0].split()
    stack = []
    for t in tokens:
        if t in ("+", "-", "*", "/"):
            b = stack.pop()
            a = stack.pop()
            if t == "+":
                stack.append(a + b)
            elif t == "-":
                stack.append(a - b)
            elif t == "*":
                stack.append(a * b)
            else:
                # truncate toward zero, not floor
                stack.append(int(a / b))
        else:
            stack.append(int(t))
    return str(stack[0])


def _solve_132_pattern(lines):
    nums = list(map(int, lines[0].split()))
    stack = []
    third = float("-inf")
    for n in reversed(nums):
        if n < third:
            return "true"
        while stack and stack[-1] < n:
            third = stack.pop()
        stack.append(n)
    return "false"


def _solve_max_width_ramp(lines):
    nums = list(map(int, lines[0].split()))
    stack = []
    for i, n in enumerate(nums):
        if not stack or nums[stack[-1]] > n:
            stack.append(i)
    best = 0
    for j in range(len(nums) - 1, -1, -1):
        while stack and nums[stack[-1]] <= nums[j]:
            best = max(best, j - stack.pop())
    return str(best)

def _solve_baseball_game(lines):
    n = int(lines[0])
    stack = []
    for i in range(1, n + 1):
        op = lines[i]
        if op == "C":
            stack.pop()
        elif op == "D":
            stack.append(2 * stack[-1])
        elif op == "+":
            stack.append(stack[-1] + stack[-2])
        else:
            stack.append(int(op))
    return str(sum(stack))


def _solve_remove_adjacent_duplicates(lines):
    stack = []
    for c in lines[0]:
        if stack and stack[-1] == c:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


def _solve_queue_using_stacks(lines):
    q = int(lines[0])
    data = []
    out = []
    for i in range(1, q + 1):
        parts = lines[i].split()
        if parts[0] == "push":
            data.append(int(parts[1]))
        elif parts[0] == "pop":
            out.append(str(data.pop(0)))
        elif parts[0] == "peek":
            out.append(str(data[0]))
        else:
            out.append("true" if not data else "false")
    return " ".join(out)


def _solve_backspace_compare(lines):
    def build(s):
        stack = []
        for c in s:
            if c == "#":
                if stack:
                    stack.pop()
            else:
                stack.append(c)
        return "".join(stack)

    return "true" if build(lines[0]) == build(lines[1]) else "false"


def _solve_daily_temperatures(lines):
    temps = list(map(int, lines[0].split()))
    res = [0] * len(temps)
    stack = []
    for i, t in enumerate(temps):
        while stack and temps[stack[-1]] < t:
            j = stack.pop()
            res[j] = i - j
        stack.append(i)
    return " ".join(map(str, res))


def _solve_stock_span(lines):
    q = int(lines[0])
    prices = [int(lines[1 + i]) for i in range(q)]
    stack = []
    out = []
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] <= p:
            stack.pop()
        out.append(str(i + 1 if not stack else i - stack[-1]))
        stack.append(i)
    return " ".join(out)


def _solve_basic_calculator_ii(lines):
    s = lines[0]
    stack = []
    num = 0
    op = "+"
    for c in s + "+":
        if c.isdigit():
            num = num * 10 + int(c)
        elif c in "+-*/":
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                prev = stack.pop()
                stack.append(int(prev / num))
            num = 0
            op = c
    return str(sum(stack))


def _solve_remove_k_digits(lines):
    num = lines[0]
    k = int(lines[1])
    stack = []
    for c in num:
        while k and stack and stack[-1] > c:
            stack.pop()
            k -= 1
        stack.append(c)
    if k:
        stack = stack[:-k]
    return "".join(stack).lstrip("0") or "0"


def _solve_sum_subarray_minimums(lines):
    nums = list(map(int, lines[0].split()))
    MOD = 10 ** 9 + 7
    n = len(nums)
    left = [0] * n
    right = [0] * n
    stack = []
    for i in range(n):
        while stack and nums[stack[-1]] > nums[i]:
            stack.pop()
        left[i] = i - (stack[-1] if stack else -1)
        stack.append(i)
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and nums[stack[-1]] >= nums[i]:
            stack.pop()
        right[i] = (stack[-1] if stack else n) - i
        stack.append(i)
    total = 0
    for i in range(n):
        total = (total + nums[i] * left[i] * right[i]) % MOD
    return str(total)


def _solve_maximal_rectangle(lines):
    m, n = map(int, lines[0].split())
    grid = [list(map(int, lines[1 + i].split())) for i in range(m)]
    heights = [0] * n
    best = 0
    for row in grid:
        for j in range(n):
            heights[j] = heights[j] + 1 if row[j] == 1 else 0
        stack = []
        for i, h in enumerate(heights + [0]):
            while stack and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                best = max(best, height * width)
            stack.append(i)
    return str(best)


def _solve_shortest_subarray_at_least_k(lines):
    nums = list(map(int, lines[0].split()))
    k = int(lines[1])
    from collections import deque
    n = len(nums)
    prefix = [0] * (n + 1)
    for i, v in enumerate(nums):
        prefix[i + 1] = prefix[i] + v
    dq = deque()
    best = n + 1
    for i in range(n + 1):
        while dq and prefix[i] - prefix[dq[0]] >= k:
            best = min(best, i - dq.popleft())
        while dq and prefix[dq[-1]] >= prefix[i]:
            dq.pop()
        dq.append(i)
    return str(best) if best <= n else "-1"

def _solve_recent_calls(lines):
    q = int(lines[0])
    window = []
    out = []
    for i in range(1, q + 1):
        t = int(lines[i])
        window.append(t)
        while window[0] < t - 3000:
            window.pop(0)
        out.append(str(len(window)))
    return " ".join(out)


def _solve_final_prices(lines):
    prices = list(map(int, lines[0].split()))
    out = []
    for i, p in enumerate(prices):
        discount = 0
        for j in range(i + 1, len(prices)):
            if prices[j] <= p:
                discount = prices[j]
                break
        out.append(str(p - discount))
    return " ".join(out)


def _solve_make_string_great(lines):
    stack = []
    for c in lines[0]:
        if stack and stack[-1] != c and stack[-1].lower() == c.lower():
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)


def _solve_crawler_log_folder(lines):
    n = int(lines[0])
    depth = 0
    for i in range(1, n + 1):
        op = lines[i]
        if op == "../":
            depth = max(0, depth - 1)
        elif op != "./":
            depth += 1
    return str(depth)


def _solve_next_greater_element_ii(lines):
    nums = list(map(int, lines[0].split()))
    n = len(nums)
    res = [-1] * n
    stack = []
    for i in range(2 * n):
        v = nums[i % n]
        while stack and nums[stack[-1]] < v:
            res[stack.pop()] = v
        if i < n:
            stack.append(i)
    return " ".join(map(str, res))


def _solve_validate_stack_sequences(lines):
    pushed = list(map(int, lines[0].split()))
    popped = list(map(int, lines[1].split()))
    stack = []
    i = 0
    for v in pushed:
        stack.append(v)
        while stack and i < len(popped) and stack[-1] == popped[i]:
            stack.pop()
            i += 1
    return "true" if not stack else "false"


def _solve_design_circular_queue(lines):
    k = int(lines[0])
    q = int(lines[1])
    data = []
    out = []
    for i in range(2, 2 + q):
        parts = lines[i].split()
        op = parts[0]
        if op == "enQueue":
            if len(data) < k:
                data.append(int(parts[1]))
                out.append("true")
            else:
                out.append("false")
        elif op == "deQueue":
            if data:
                data.pop(0)
                out.append("true")
            else:
                out.append("false")
        elif op == "Front":
            out.append(str(data[0]) if data else "-1")
        elif op == "Rear":
            out.append(str(data[-1]) if data else "-1")
        elif op == "isEmpty":
            out.append("true" if not data else "false")
        else:
            out.append("true" if len(data) == k else "false")
    return " ".join(out)


def _solve_visible_people_queue(lines):
    heights = list(map(int, lines[0].split()))
    n = len(heights)
    res = [0] * n
    stack = []
    for i in range(n - 1, -1, -1):
        count = 0
        while stack and stack[-1] < heights[i]:
            stack.pop()
            count += 1
        if stack:
            count += 1
        res[i] = count
        stack.append(heights[i])
    return " ".join(map(str, res))


def _solve_min_add_parentheses(lines):
    s = lines[0]
    open_needed = 0
    close_needed = 0
    for c in s:
        if c == "(":
            close_needed += 1
        else:
            if close_needed:
                close_needed -= 1
            else:
                open_needed += 1
    return str(open_needed + close_needed)


def _solve_basic_calculator_iii(lines):
    s = lines[0].replace(" ", "")
    pos = [0]

    def expr():
        stack = []
        num = 0
        op = "+"
        while pos[0] <= len(s):
            c = s[pos[0]] if pos[0] < len(s) else "+"
            pos[0] += 1
            if c.isdigit():
                num = num * 10 + int(c)
                continue
            if c == "(":
                num = expr()
                continue
            if op == "+":
                stack.append(num)
            elif op == "-":
                stack.append(-num)
            elif op == "*":
                stack.append(stack.pop() * num)
            else:
                prev = stack.pop()
                stack.append(int(prev / num))
            num = 0
            op = c
            if c == ")":
                break
        return sum(stack)

    return str(expr())


PROBLEMS = [
{
        "title": "Next Greater Element",
        "topic": "stack_queue",
        "difficulty": "easy",
        "description": "Given an array nums, for each element find the next element to its right that is greater than it. If none exists, use -1.",
        "example_input": "2 1 2 4 3",
        "constraints": "Input format: one line of space-separated integers. Output format: space-separated results, one per input element.",
        "solve": _solve_next_greater_element,
        "sample_inputs": ["2 1 2 4 3", "3 1 4 1 5"],
        "hidden_inputs": [
            "1",          # single element has no greater neighbour
            "5 5 5",      # equal values do not count as greater
            "1 1 2",
            "1 2",
            "2 1",
            "1 2 3 4",    # every element resolved by its neighbour
            "4 3 2 1",    # nothing is ever resolved
            "-1 -2 0",    # negatives
            "1 3 2 4",
            "10 9 8 11",  # one late element resolves the whole stack
            "2 7 3 5 4 6 8",
        ],
    },
{
        "title": "Min Stack Operations",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "Simulate a stack that supports push(x), pop() and getMin() (returns the current minimum). Given a sequence of operations, output the result of every getMin call, in order.",
        "example_input": "5\npush 5\npush 3\ngetMin\npop\ngetMin",
        "constraints": "Input format: line 1 is the operation count Q, followed by Q lines each \"push x\", \"pop\", or \"getMin\". Output format: space-separated results of every getMin call.",
        "solve": _solve_min_stack,
        "sample_inputs": ["5\npush 5\npush 3\ngetMin\npop\ngetMin", "4\npush 8\ngetMin\npush 2\ngetMin"],
        "hidden_inputs": [
            "1\npush 5",                                       # no getMin at all
            "3\npush 1\npush 2\ngetMin",
            "4\npush 10\npush 20\ngetMin\ngetMin",             # repeated getMin
            "4\npush 100\ngetMin\npush 50\ngetMin",
            "5\npush 0\npush 0\ngetMin\npop\ngetMin",          # duplicate minimum
            "6\npush 5\npop\npush 3\ngetMin\npush 1\ngetMin",  # stack emptied then reused
            "6\npush -2\npush 0\npush -3\ngetMin\npop\ngetMin",
            "7\npush 2\npush 2\ngetMin\npop\ngetMin\npop\npush 3",
            "8\npush -1\ngetMin\npush -2\ngetMin\npop\ngetMin\npush -5\ngetMin",
            "10\npush 3\npush 1\npush 4\ngetMin\npop\ngetMin\npop\ngetMin\npop\npush 9",
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
        "sample_inputs": ["2 1 5 6 2 3", "4 2 3 1"],
        "hidden_inputs": [
            "0",          # zero-height bar
            "5",          # single bar
            "0 0 0",
            "2 4",
            "2 1 2",
            "3 3 3",
            "1 1 1 1",
            "1 0 1 0 1",  # zeros split the histogram
            "1 2 3 4 5",  # increasing
            "5 4 3 2 1",  # decreasing
            "6 2 5 4 5 1 6",
        ],
    },
{
        "title": "Remove Duplicate Letters",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Given a string s of lowercase letters, remove letters so that every letter appears exactly once, and among all such results return the one that is smallest in alphabetical order.",
        "example_input": "bcabc",
        "constraints": "Input format: one line containing s (lowercase letters only). Output format: the resulting string.",
        "solve": _solve_remove_duplicate_letters,
        "sample_inputs": ["bcabc", "cbacdcbc"],
        "hidden_inputs": [
            "a",                    # single letter
            "aa",                   # one letter repeated
            "ab",                   # already unique and sorted
            "ba",                   # already unique, must not reorder illegally
            "aaaa",
            "abc",
            "cba",                  # descending, nothing can be dropped
            "bbcaac",
            "cdadabcc",
            "abacb",
            "leetcode",
            "zyxwvutsrqponmlkjihgfedcba",
        ],
    },
{
        "title": "Decode String",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "Given an encoded string where k[encoded] means the bracketed part repeats k times, return the decoded string. Brackets may be nested and k is always a positive integer.",
        "example_input": "3[a]2[bc]",
        "constraints": "Input format: one line containing the encoded string. Output format: the decoded string.",
        "solve": _solve_decode_string,
        "sample_inputs": ["3[a]2[bc]", "3[a2[c]]"],
        "hidden_inputs": [
            "a",                    # no encoding at all
            "1[a]",                 # repeat count of one
            "2[a]",
            "10[a]",                # multi-digit count
            "abc",
            "2[abc]3[cd]ef",        # literals after the brackets
            "2[2[2[a]]]",           # triple nesting
            "xy2[z]",               # literal before the bracket
            "2[ab3[cd]]ef",
            "100[x]",               # large multi-digit count
        ],
    },
{
        "title": "Maximum Frequency Stack",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Simulate a stack where pop() removes the most frequent value, breaking ties in favour of the value pushed most recently. Given a sequence of operations, output the result of every pop, in order.",
        "example_input": "8\npush 5\npush 7\npush 5\npush 7\npush 4\npush 5\npop\npop",
        "constraints": "Input format: line 1 is the operation count Q, followed by Q lines each \"push x\" or \"pop\". Output format: space-separated results of every pop.",
        "solve": _solve_freq_stack,
        "sample_inputs": [
            "8\npush 5\npush 7\npush 5\npush 7\npush 4\npush 5\npop\npop",
            "3\npush 1\npush 2\npop",
        ],
        "hidden_inputs": [
            "1\npush 9",                    # no pops, empty output
            "2\npush 3\npop",               # single element
            "4\npush 1\npush 1\npop\npop",  # same value twice
            "5\npush 1\npush 2\npush 3\npop\npop",   # all tied, most recent wins
            "6\npush 4\npush 4\npush 5\npop\npop\npop",
            "6\npush -1\npush -1\npush -2\npop\npop\npop",   # negatives
            "6\npush 0\npush 0\npush 0\npop\npop\npop",
            "9\npush 1\npush 2\npush 1\npush 2\npush 1\npop\npop\npop\npop",
            "10\npush 5\npush 7\npush 5\npush 7\npush 4\npush 5\npop\npop\npop\npop",
        ],
    },
{
        "title": "Simplify Path",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "Given an absolute Unix-style file path, return its canonical form: a single slash between names, no trailing slash, '.' meaning the current directory and '..' meaning the parent directory.",
        "example_input": "/home//foo/",
        "constraints": "Input format: one line containing the path, always starting with '/'. Output format: the canonical path.",
        "solve": _solve_simplify_path,
        "sample_inputs": ["/home//foo/", "/a/./b/../../c/"],
        "hidden_inputs": [
            "/",                    # root only
            "/.",                   # current directory at root
            "/..",                  # parent of root is still root
            "/../",
            "/...",                 # three dots is an ordinary name
            "/a",
            "/a/",                  # trailing slash removed
            "/a//b",                # repeated separators collapse
            "/a/b/../c",
            "/a/../../b",           # climbing above root
            "/a/./b/./c/.",
            "/home/user/Documents/../Pictures",
        ],
    },
{
        "title": "Car Fleet",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "Cars drive toward a target at given positions and speeds. A faster car catches a slower one ahead and then travels at the slower speed, forming a fleet. Return how many fleets arrive at the target.",
        "example_input": "12\n10 8 0 5 3\n2 4 1 1 3",
        "constraints": "Input format: line 1 is the target, line 2 is the space-separated positions, line 3 is the space-separated speeds. Output format: a single integer.",
        "solve": _solve_car_fleet,
        "sample_inputs": ["12\n10 8 0 5 3\n2 4 1 1 3", "10\n3\n3"],
        "hidden_inputs": [
            "10\n0\n1",             # single car
            "10\n0 1\n1 1",         # equal speeds never merge
            "10\n0 1\n2 1",         # faster car behind catches the slower one
            "10\n1 0\n1 2",
            "100\n0 2 4\n4 2 1",    # cascade into one fleet
            "10\n4 6 8\n1 1 1",
            "10\n9 8 7\n1 1 1",
            "12\n12 8\n2 4",       # a car already standing on the target
            "20\n0 5 10 15\n5 4 3 2",
            "100\n0 10 20 30 40\n1 1 1 1 1",
        ],
    },
{
        "title": "Asteroid Collision",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "Each value is an asteroid: its size is the absolute value and its sign is the direction (positive moves right, negative moves left). When two collide the smaller explodes; if equal, both explode. Asteroids moving the same way never meet. Return the final state.",
        "example_input": "5 10 -5",
        "constraints": "Input format: one line of space-separated non-zero integers. Output format: the surviving asteroids, space-separated (empty if none survive).",
        "solve": _solve_asteroid_collision,
        "sample_inputs": ["5 10 -5", "8 -8"],
        "hidden_inputs": [
            "1",                    # single asteroid
            "-1",
            "1 2",                  # same direction, no collision
            "-1 -2",
            "-1 1",                 # moving apart, never meet
            "1 -1",                 # equal sizes, both explode
            "10 2 -5",
            "-2 -1 1 2",
            "1 1 -2",               # one big asteroid clears two small ones
            "2 -1 1 -2",
        ],
    },
{
        "title": "Evaluate Reverse Polish Notation",
        "topic": "stack_queue",
        "difficulty": "easy",
        "description": "Evaluate an arithmetic expression in Reverse Polish Notation. Valid operators are +, -, * and /. Division between two integers truncates toward zero.",
        "example_input": "2 1 + 3 *",
        "constraints": "Input format: one line of space-separated tokens. Output format: a single integer.",
        "solve": _solve_eval_rpn,
        "sample_inputs": ["2 1 + 3 *", "4 13 5 / +"],
        "hidden_inputs": [
            "5",                    # a lone operand
            "-5",
            "1 2 +",
            "2 1 -",                # order of operands matters
            "1 2 -",                # negative result
            "3 4 *",
            "7 2 /",                # truncation
            "-7 2 /",               # truncates toward zero, not down
            "7 -2 /",
            "0 5 +",
            "10 6 9 3 + -11 * / * 17 + 5 +",
        ],
    },
{
        "title": "132 Pattern",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Given an array of integers, decide whether there are three indices i < j < k such that nums[i] < nums[k] < nums[j].",
        "example_input": "3 1 4 2",
        "constraints": "Input format: one line of space-separated integers. Output format: \"true\" or \"false\".",
        "solve": _solve_132_pattern,
        "sample_inputs": ["3 1 4 2", "1 2 3 4"],
        "hidden_inputs": [
            "1",                    # too short to hold a pattern
            "1 2",
            "1 2 3",                # increasing has no 132
            "3 2 1",                # decreasing has no 132
            "1 3 2",                # the minimal example
            "1 1 1",                # equal values, strict inequality fails
            "-1 3 2 0",
            "3 5 0 3 4",
            "1 4 0 -1 -2 -3 -1 -2",
            "1 0 1 -4 -3",          # no valid pattern despite the shape
        ],
    },
{
        "title": "Maximum Width Ramp",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "A ramp is a pair of indices i < j where nums[i] <= nums[j]. Return the largest possible width j - i, or 0 if no ramp exists.",
        "example_input": "6 0 8 2 1 5",
        "constraints": "Input format: one line of space-separated integers. Output format: a single integer.",
        "solve": _solve_max_width_ramp,
        "sample_inputs": ["6 0 8 2 1 5", "9 8 1 0 1 9 4 0 4 1"],
        "hidden_inputs": [
            "1",                    # single element, no ramp
            "2 1",                  # strictly decreasing, no ramp
            "1 2",
            "1 1",                  # equal values still count as a ramp
            "5 5 5 5",              # whole array is one ramp
            "3 2 1",
            "1 2 3 4",              # ends form the widest ramp
            "4 3 2 1 5",            # ramp spans the entire array
            "2 2 1 4 5 0",
            "9 8 7 6 5 4 3 2 1 0",
        ],
    },
{
        "title": "Baseball Game",
        "topic": "stack_queue",
        "difficulty": "easy",
        "description": "Scores are recorded one at a time. A number records that score, C cancels the previous score, D records double the previous score, and + records the sum of the previous two. Return the total of everything still recorded at the end.",
        "example_input": "5\n5\n2\nC\nD\n+",
        "constraints": "Input format: line 1 is the number of operations, followed by that many lines each an integer, C, D or +. Output format: a single integer.",
        "solve": _solve_baseball_game,
        "sample_inputs": ["5\n5\n2\nC\nD\n+", "3\n1\n2\n3"],
        "hidden_inputs": [
            "1\n5",                 # a single score
            "1\n-5",                # a negative score
            "2\n5\nC",              # everything cancelled, total zero
            "2\n5\nD",              # doubling
            "3\n1\n2\n+",
            "4\n1\n1\nC\nC",
            "4\n0\nD\n+\n+",        # zeroes throughout
            "5\n-1\n-2\nD\n+\nC",
            "6\n5\n-2\n4\nC\nD\n9",
            "7\n1\n2\nD\n+\nC\nD\n+",
        ],
    },
{
        "title": "Remove All Adjacent Duplicates In String",
        "topic": "stack_queue",
        "difficulty": "easy",
        "description": "Repeatedly delete any two identical letters standing next to each other, including pairs that only become adjacent after earlier deletions. Return what is left.",
        "example_input": "abbaca",
        "constraints": "Input format: one line containing the lowercase string. Output format: the resulting string, or an empty line if nothing remains.",
        "solve": _solve_remove_adjacent_duplicates,
        "sample_inputs": ["abbaca", "azxxzy"],
        "hidden_inputs": [
            "a",                    # nothing to remove
            "aa",                   # the string empties
            "ab",
            "aaa",                  # one letter survives
            "aaaa",
            "abba",                 # a cascading collapse
            "abccba",               # collapses entirely
            "abcddcba",
            "aabbcc",
            "abcdefg",              # no adjacent pair at all
        ],
    },
{
        "title": "Implement Queue using Stacks",
        "topic": "stack_queue",
        "difficulty": "easy",
        "description": "Simulate a queue supporting push, pop, peek and empty, where pop and peek act on the value that has been waiting longest. Report the result of every pop, peek and empty, in order.",
        "example_input": "6\npush 1\npush 2\npeek\npop\nempty\nempty",
        "constraints": "Input format: line 1 is the number of operations, followed by that many lines each \"push x\", \"pop\", \"peek\" or \"empty\". Output format: the results space-separated, with empty reported as \"true\" or \"false\".",
        "solve": _solve_queue_using_stacks,
        "sample_inputs": ["6\npush 1\npush 2\npeek\npop\nempty\nempty", "3\npush 5\npop\nempty"],
        "hidden_inputs": [
            "1\npush 1",                    # no reported operation, empty output
            "1\nempty",                     # empty before anything arrives
            "2\npush 1\npop",
            "2\npush 1\npeek",              # peek does not remove
            "4\npush 1\npeek\npeek\npop",   # repeated peeks
            "4\npush 1\npush 2\npop\npop",  # first in, first out
            "5\npush 1\npop\npush 2\npop\nempty",
            "6\npush 1\npush 2\npush 3\npop\npeek\npop",
            "5\npush -1\npush -2\npop\npeek\nempty",
            "7\npush 1\npop\nempty\npush 2\npush 3\npeek\npop",
        ],
    },
{
        "title": "Backspace String Compare",
        "topic": "stack_queue",
        "difficulty": "easy",
        "description": "In both strings a hash character means the previous character was deleted, and a hash with nothing before it does nothing. Decide whether the two strings end up the same.",
        "example_input": "ab#c\nad#c",
        "constraints": "Input format: line 1 and line 2 are the two strings, each made of lowercase letters and hashes. Output format: \"true\" or \"false\".",
        "solve": _solve_backspace_compare,
        "sample_inputs": ["ab#c\nad#c", "a#c\nb"],
        "hidden_inputs": [
            "a\na",                 # no deletions at all
            "a\nb",
            "a#\nb#",               # both reduce to nothing
            "##\n#",                # a hash with nothing to delete
            "a##\nb##",
            "ab##\nc#d#",
            "abc#\nab",             # the same result by different routes
            "xywrrmp\nxywrrmu#p",
            "bxj##tw\nbxo#j##tw",
            "nzp#o#g\nb#nzp#o#g",
        ],
    },
{
        "title": "Daily Temperatures",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "For each day, report how many days you must wait for a warmer temperature. Where no warmer day ever comes, report zero.",
        "example_input": "73 74 75 71 69 72 76 73",
        "constraints": "Input format: one line of space-separated temperatures. Output format: one waiting time per day, space-separated.",
        "solve": _solve_daily_temperatures,
        "sample_inputs": ["73 74 75 71 69 72 76 73", "30 40 50 60"],
        "hidden_inputs": [
            "50",                   # a single day, never warmer
            "50 50",                # equal is not warmer
            "50 51",
            "51 50",
            "30 60 90",             # warmer every day
            "90 60 30",             # colder every day
            "50 50 50 50",
            "70 60 80",             # one late day resolves two
            "34 80 80 34 34 80 80 80 34 34",
            "89 62 70 58 47 47 46 76 100 70",
        ],
    },
{
        "title": "Online Stock Span",
        "topic": "stack_queue",
        "difficulty": "medium",
        "description": "Prices arrive one per day. For each day report how many consecutive days up to and including that day had a price no higher than it.",
        "example_input": "7\n100\n80\n60\n70\n60\n75\n85",
        "constraints": "Input format: line 1 is the number of days, followed by that many lines each holding that day's price. Output format: one span per day, space-separated.",
        "solve": _solve_stock_span,
        "sample_inputs": ["7\n100\n80\n60\n70\n60\n75\n85", "3\n1\n2\n3"],
        "hidden_inputs": [
            "1\n5",                 # the first day always spans one
            "2\n5\n5",              # equal prices count
            "2\n5\n4",
            "2\n4\n5",
            "3\n3\n2\n1",           # falling every day
            "4\n1\n2\n3\n4",
            "4\n10\n10\n10\n10",
            "5\n5\n4\n3\n2\n10",    # one day swallows all before it
            "6\n31\n41\n48\n59\n79\n2",
            "5\n100\n1\n100\n1\n100",
        ],
    },
{
        "title": "Basic Calculator II",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Work out the value of an expression made of whole numbers and the four operators, with multiplication and division binding tighter than addition and subtraction. Division between whole numbers discards any remainder, rounding towards zero.",
        "example_input": "3+2*2",
        "constraints": "Input format: one line containing the expression, which may contain spaces but has none at either end. Output format: a single integer.",
        "solve": _solve_basic_calculator_ii,
        "sample_inputs": ["3+2*2", "3/2"],
        "hidden_inputs": [
            "1",                    # a lone number
            "0",
            "1+1",
            "2-3",                  # a negative result
            "2*3",
            "7/2",                  # truncation
            "2-7/2",                # forces int(-7/2): toward zero, not floored
            "1+2*3-4/2",            # every operator at once
            "14-3/2",
            "100000/3/3",           # repeated division
        ],
    },
{
        "title": "Remove K Digits",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Delete exactly k digits from the given number so that what remains, read in the same order, is as small as possible. Leading zeroes are dropped, and an empty result is written as zero.",
        "example_input": "1432219\n3",
        "constraints": "Input format: line 1 is the number as a string of digits, line 2 is k (0 <= k <= number of digits). Output format: the resulting number.",
        "solve": _solve_remove_k_digits,
        "sample_inputs": ["1432219\n3", "10200\n1"],
        "hidden_inputs": [
            "1\n0",                 # nothing removed
            "1\n1",                 # everything removed, zero
            "10\n1",                # the result is a bare zero
            "10\n2",
            "112\n1",               # the largest digit goes
            "321\n1",               # descending, the front goes
            "123\n1",               # ascending, the back goes
            "10001\n4",             # leading zeroes must be dropped
            "1234567890\n9",
            "9876543210\n5",
        ],
    },
{
        "title": "Sum of Subarray Minimums",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "For every run of consecutive values, take the smallest value in that run. Return the total of all those smallest values, modulo 1000000007.",
        "example_input": "3 1 2 4",
        "constraints": "Input format: one line of space-separated positive integers. Output format: a single integer, the total modulo 1000000007.",
        "solve": _solve_sum_subarray_minimums,
        "sample_inputs": ["3 1 2 4", "11 81 94 43 3"],
        "hidden_inputs": [
            "1",                    # one run, one minimum
            "5",
            "1 2",
            "2 1",
            "1 1",                  # equal values must not be double counted
            "2 2 2",
            "1 2 3",                # increasing
            "3 2 1",                # decreasing
            "2 1 2 1 2",            # repeated minima
            "71 55 82 55 55 55",
        ],
    },
{
        "title": "Maximal Rectangle",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Find the largest rectangle made entirely of ones inside a grid of zeroes and ones, and return its area.",
        "example_input": "4 5\n1 0 1 0 0\n1 0 1 1 1\n1 1 1 1 1\n1 0 0 1 0",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated 0 and 1 values. Output format: a single integer.",
        "solve": _solve_maximal_rectangle,
        "sample_inputs": ["4 5\n1 0 1 0 0\n1 0 1 1 1\n1 1 1 1 1\n1 0 0 1 0", "2 2\n0 1\n1 0"],
        "hidden_inputs": [
            "1 1\n0",               # no ones at all
            "1 1\n1",
            "1 4\n1 1 1 1",         # a single row
            "4 1\n1\n1\n1\n1",      # a single column
            "2 2\n1 1\n1 1",
            "3 3\n0 0 0\n0 0 0\n0 0 0",
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 4\n1 1 0 1\n1 1 0 1\n1 1 1 1",   # a wide block beats a tall one
            "2 4\n1 1 1 0\n0 1 1 1",
            "4 4\n0 1 1 0\n1 1 1 1\n1 1 1 1\n0 1 1 0",
        ],
    },
{
        "title": "Shortest Subarray with Sum at Least K",
        "topic": "stack_queue",
        "difficulty": "hard",
        "description": "Return the length of the shortest run of consecutive values adding up to at least k, or -1 if no run does. Values may be negative.",
        "example_input": "2 -1 2\n3",
        "constraints": "Input format: line 1 is the space-separated integers, line 2 is k. Output format: a single integer, or -1.",
        "solve": _solve_shortest_subarray_at_least_k,
        "sample_inputs": ["2 -1 2\n3", "1 2\n4"],
        "hidden_inputs": [
            "1\n1",                 # the single value suffices
            "1\n2",                 # it does not
            "-1\n1",                # a negative value alone
            "1 2\n3",               # the whole list is needed
            "2 1\n3",
            "1 1 1\n2",             # any adjacent pair
            "-1 5 -1\n5",           # the negatives must be skipped
            "84 -37 32 40 95\n167", # a long run beats several short ones
            "-28 81 -20 28 -29\n89",
            "17 85 93 -45 -21\n150",
        ],
    },
{
        "title": "Number of Recent Calls",
        "topic": "stack_queue", "difficulty": "easy",
        "description": "Calls arrive at given times. After each one, report how many calls have arrived within the last three thousand time units, counting the one just received.",
        "example_input": "4\n1\n100\n3001\n3002",
        "constraints": "Input format: line 1 is the number of calls, followed by that many lines each holding an arrival time in increasing order. Output format: one count per call, space-separated.",
        "solve": _solve_recent_calls,
        "sample_inputs": ["4\n1\n100\n3001\n3002", "2\n1\n2"],
        "hidden_inputs": [
            "1\n1",                 # the first call always counts as one
            "1\n5000",
            "2\n1\n3001",           # exactly on the boundary, still counted
            "2\n1\n3002",           # one unit too late
            "3\n0\n1\n2",
            "3\n1\n3001\n6002",
            "4\n1\n2\n3\n4",
            "5\n0\n3000\n6000\n9000\n12000",
            "4\n1\n1000\n2000\n3000",
            "5\n1\n2\n3\n3001\n3002",
        ],
    },
{
        "title": "Final Prices With a Special Discount in a Shop",
        "topic": "stack_queue", "difficulty": "easy",
        "description": "Each item is discounted by the price of the first later item costing no more than it. Items with no such later item keep their price. Return the final prices.",
        "example_input": "8 4 6 2 3",
        "constraints": "Input format: one line of space-separated positive prices. Output format: the final prices, space-separated.",
        "solve": _solve_final_prices,
        "sample_inputs": ["8 4 6 2 3", "1 2 3 4 5"],
        "hidden_inputs": [
            "1",                    # nothing later, no discount
            "1 1",                  # an equal price still discounts
            "2 1",
            "1 2",                  # the later item is dearer
            "5 5 5",
            "1 2 3 4",              # prices only rise, no discounts
            "4 3 2 1",              # every item is discounted
            "10 1 1 6",
            "3 1 3 1 3",
            "8 7 4 2 8 1 7 7 10 1",
        ],
    },
{
        "title": "Make The String Great",
        "topic": "stack_queue", "difficulty": "easy",
        "description": "Repeatedly delete any two neighbouring characters that are the same letter in opposite cases, including pairs that only become neighbours after earlier deletions. Return what is left.",
        "example_input": "leEeetcode",
        "constraints": "Input format: one line containing the string of letters. Output format: the resulting string, or an empty line if nothing remains.",
        "solve": _solve_make_string_great,
        "sample_inputs": ["leEeetcode", "abBAcC"],
        "hidden_inputs": [
            "a",                    # nothing to remove
            "aA",                   # the string empties
            "Aa",
            "aa",                   # the same case is not a pair
            "AA",
            "abBA",                 # a cascading collapse
            "aAbBcC",
            "s",
            "Pp",
            "mMnNoOpP",
        ],
    },
{
        "title": "Crawler Log Folder",
        "topic": "stack_queue", "difficulty": "easy",
        "description": "Starting in the main folder, each entry either moves into a subfolder, moves back to the parent, or stays put. Moving back from the main folder does nothing. Return how many steps back are needed to return to the main folder.",
        "example_input": "3\nd1/\nd2/\n../",
        "constraints": "Input format: line 1 is the number of entries, followed by that many lines each a folder name ending in a slash, \"../\" or \"./\". Output format: a single integer.",
        "solve": _solve_crawler_log_folder,
        "sample_inputs": ["3\nd1/\nd2/\n../", "4\nd1/\nd2/\n./\nd3/"],
        "hidden_inputs": [
            "1\nd1/",               # one level deep
            "1\n../",               # already at the top, stays there
            "1\n./",                # staying put
            "2\nd1/\n../",          # back where it started
            "2\n../\n../",          # cannot go above the top
            "3\n./\n./\n./",
            "3\nd1/\nd2/\nd3/",
            "4\nd1/\n../\n../\nd2/",
            "5\na/\nb/\n../\nc/\n./",
            "6\nd1/\nd2/\n../\nd3/\n../\n../",
        ],
    },
{
        "title": "Next Greater Element II",
        "topic": "stack_queue", "difficulty": "medium",
        "description": "The values are arranged in a circle. For each one, report the first larger value found by moving forward, wrapping past the end if necessary, or -1 if none exists.",
        "example_input": "1 2 1",
        "constraints": "Input format: one line of space-separated integers. Output format: one result per value, space-separated.",
        "solve": _solve_next_greater_element_ii,
        "sample_inputs": ["1 2 1", "1 2 3 4 3"],
        "hidden_inputs": [
            "1",                    # nothing is larger
            "1 1",                  # equal values do not count
            "1 2",                  # the wrap finds nothing for the larger
            "2 1",                  # the wrap resolves the smaller
            "5 5 5",
            "1 2 3",
            "3 2 1",                # the wrap resolves everything but the max
            "-1 -2 -3",             # negatives
            "5 4 3 2 1",
            "100 1 11 1 120 111 123 1 -1 -100",
        ],
    },
{
        "title": "Validate Stack Sequences",
        "topic": "stack_queue", "difficulty": "medium",
        "description": "Given the order values are pushed onto a stack and the order they come off it, decide whether that pairing is possible.",
        "example_input": "1 2 3 4 5\n4 5 3 2 1",
        "constraints": "Input format: line 1 is the push order, line 2 is the pop order, both permutations of the same distinct values. Output format: \"true\" or \"false\".",
        "solve": _solve_validate_stack_sequences,
        "sample_inputs": ["1 2 3 4 5\n4 5 3 2 1", "1 2 3 4 5\n4 3 5 1 2"],
        "hidden_inputs": [
            "1\n1",                 # the only possible pairing
            "1 2\n1 2",             # pop each straight away
            "1 2\n2 1",             # push both, then pop both
            "1 2 3\n3 2 1",
            "1 2 3\n1 2 3",
            "1 2 3\n2 1 3",
            "1 2 3\n3 1 2",         # impossible, 1 is buried under 2
            "1 2 3 4\n2 4 3 1",
            "1 2 3 4\n4 1 2 3",     # impossible
            "2 1 0\n1 2 0",
        ],
    },
{
        "title": "Design Circular Queue",
        "topic": "stack_queue", "difficulty": "medium",
        "description": "Simulate a queue of fixed capacity supporting adding at the back, removing from the front, reading either end, and testing whether it is empty or full. Report the result of every operation.",
        "example_input": "3\n6\nenQueue 1\nenQueue 2\nenQueue 3\nenQueue 4\nRear\nisFull",
        "constraints": "Input format: line 1 is the capacity, line 2 is the number of operations, followed by that many lines each \"enQueue x\", \"deQueue\", \"Front\", \"Rear\", \"isEmpty\" or \"isFull\". Output format: the results space-separated, using \"true\"/\"false\" and -1 for reading an empty queue.",
        "solve": _solve_design_circular_queue,
        "sample_inputs": ["3\n6\nenQueue 1\nenQueue 2\nenQueue 3\nenQueue 4\nRear\nisFull", "1\n3\nenQueue 5\nFront\nisFull"],
        "hidden_inputs": [
            "1\n1\nisEmpty",                # empty from the start
            "1\n1\nFront",                  # reading an empty queue
            "1\n1\ndeQueue",                # removing from an empty queue
            "1\n2\nenQueue 1\nenQueue 2",   # the second does not fit
            "2\n4\nenQueue 1\nenQueue 2\nFront\nRear",
            "2\n4\nenQueue 1\ndeQueue\nisEmpty\nFront",
            "3\n5\nenQueue 1\nenQueue 2\ndeQueue\nFront\nRear",
            "1\n4\nenQueue 1\ndeQueue\nenQueue 2\nFront",   # reuse after removal
            "2\n6\nenQueue 1\nenQueue 2\nisFull\ndeQueue\nisFull\nRear",
            "3\n6\nisEmpty\nenQueue 7\nisEmpty\nFront\nRear\nisFull",
        ],
    },
{
        "title": "Number of Visible People in a Queue",
        "topic": "stack_queue", "difficulty": "medium",
        "description": "Each person can see the people to their right, but only until someone at least as tall as themselves blocks the view; that blocker is still seen. Report how many each person can see.",
        "example_input": "10 6 8 5 11 9",
        "constraints": "Input format: one line of space-separated heights. Output format: one count per person, space-separated.",
        "solve": _solve_visible_people_queue,
        "sample_inputs": ["10 6 8 5 11 9", "5 1 2 3 10"],
        "hidden_inputs": [
            "1",                    # nobody to the right
            "1 2",                  # the taller neighbour is seen
            "2 1",
            "1 1",                  # an equal height blocks immediately
            "3 3 3",
            "1 2 3",                # each sees only the next
            "3 2 1",                # the first sees everyone
            "5 5 5 5",
            "1 3 2 5 4",
            "9 1 8 2 7 3 6 4 5",
        ],
    },
{
        "title": "Minimum Add to Make Parentheses Valid",
        "topic": "stack_queue", "difficulty": "medium",
        "description": "Return the fewest brackets that must be inserted anywhere in the string so that every closing bracket matches an earlier opening one and none are left over.",
        "example_input": "())",
        "constraints": "Input format: one line containing only the characters ( and ). Output format: a single integer.",
        "solve": _solve_min_add_parentheses,
        "sample_inputs": ["())", "((("],
        "hidden_inputs": [
            "(",                    # one closing bracket needed
            ")",                    # one opening bracket needed
            "()",                   # already valid
            ")(",                   # two needed despite matching counts
            "(())",
            "))((",                 # four needed
            "()()",
            "(()",
            "())(",
            "((((((((((",
        ],
    },
{
        "title": "Basic Calculator III",
        "topic": "stack_queue", "difficulty": "hard",
        "description": "Work out the value of an expression made of whole numbers, the four operators and brackets, with multiplication and division binding tighter than addition and subtraction. Division discards any remainder, rounding towards zero.",
        "example_input": "2*(5+5*2)/3+(6/2+8)",
        "constraints": "Input format: one line containing the expression, which may contain spaces but has none at either end. Output format: a single integer.",
        "solve": _solve_basic_calculator_iii,
        "sample_inputs": ["2*(5+5*2)/3+(6/2+8)", "1+1"],
        "hidden_inputs": [
            "1",                    # a lone number
            "0",
            "(1)",                  # redundant brackets
            "((2))",
            "2*3",
            "7/2",                  # truncation
            "2-7/2",                # truncation towards zero, not down
            "(2+6*3+5-(3*14/7+2)*5)+3",
            "6-4/2",
            "2*(1+2)*3",
        ],
    },
]
