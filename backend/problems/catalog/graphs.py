"""Graphs problems."""

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

def _cgrid(lines, rows, start=1):
    return [lines[start + i].split() for i in range(rows)]


def _igrid(lines, rows, start=1):
    return [list(map(int, lines[start + i].split())) for i in range(rows)]


def _solve_surrounded_regions(lines):
    m, n = map(int, lines[0].split())
    g = _cgrid(lines, m)
    stack = []
    for i in range(m):
        for j in (0, n - 1):
            if g[i][j] == "O":
                stack.append((i, j))
    for j in range(n):
        for i in (0, m - 1):
            if g[i][j] == "O":
                stack.append((i, j))
    safe = set()
    while stack:
        i, j = stack.pop()
        if (i, j) in safe or not (0 <= i < m and 0 <= j < n) or g[i][j] != "O":
            continue
        safe.add((i, j))
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            stack.append((i + di, j + dj))
    out = []
    for i in range(m):
        out.append(" ".join(
            g[i][j] if (i, j) in safe else ("X" if g[i][j] == "O" else g[i][j])
            for j in range(n)))
    return "\n".join(out)


def _solve_walls_and_gates(lines):
    m, n = map(int, lines[0].split())
    g = _cgrid(lines, m)
    INF = float("inf")
    dist = [[INF] * n for _ in range(m)]
    queue = []
    for i in range(m):
        for j in range(n):
            if g[i][j] == "G":
                dist[i][j] = 0
                queue.append((i, j))
    head = 0
    while head < len(queue):
        i, j = queue[head]
        head += 1
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and g[ni][nj] == "." and dist[ni][nj] == INF:
                dist[ni][nj] = dist[i][j] + 1
                queue.append((ni, nj))
    out = []
    for i in range(m):
        row = []
        for j in range(n):
            if g[i][j] == "W":
                row.append("W")
            elif dist[i][j] == INF:
                row.append("-")
            else:
                row.append(str(dist[i][j]))
        out.append(" ".join(row))
    return "\n".join(out)


def _solve_max_area_island(lines):
    m, n = map(int, lines[0].split())
    g = _igrid(lines, m)
    seen = set()
    best = 0
    for i in range(m):
        for j in range(n):
            if g[i][j] != 1 or (i, j) in seen:
                continue
            area = 0
            stack = [(i, j)]
            seen.add((i, j))
            while stack:
                a, b = stack.pop()
                area += 1
                for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    na, nb = a + da, b + db
                    if 0 <= na < m and 0 <= nb < n and g[na][nb] == 1 and (na, nb) not in seen:
                        seen.add((na, nb))
                        stack.append((na, nb))
            best = max(best, area)
    return str(best)


def _solve_battleships(lines):
    m, n = map(int, lines[0].split())
    g = _cgrid(lines, m)
    count = 0
    for i in range(m):
        for j in range(n):
            if g[i][j] != "X":
                continue
            if i > 0 and g[i - 1][j] == "X":
                continue
            if j > 0 and g[i][j - 1] == "X":
                continue
            count += 1
    return str(count)


def _solve_pacific_atlantic(lines):
    m, n = map(int, lines[0].split())
    g = _igrid(lines, m)

    def flood(starts):
        seen = set(starts)
        stack = list(starts)
        while stack:
            i, j = stack.pop()
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if (0 <= ni < m and 0 <= nj < n and (ni, nj) not in seen
                        and g[ni][nj] >= g[i][j]):
                    seen.add((ni, nj))
                    stack.append((ni, nj))
        return seen

    pacific = flood([(0, j) for j in range(n)] + [(i, 0) for i in range(m)])
    atlantic = flood([(m - 1, j) for j in range(n)] + [(i, n - 1) for i in range(m)])
    both = sorted(pacific & atlantic)
    return "\n".join(f"{i} {j}" for i, j in both)


def _solve_course_schedule_ii(lines):
    n, m = map(int, lines[0].split())
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        adj[b].append(a)
        indeg[a] += 1
    import heapq
    heap = [i for i in range(n) if indeg[i] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nb in adj[node]:
            indeg[nb] -= 1
            if indeg[nb] == 0:
                heapq.heappush(heap, nb)
    return " ".join(map(str, order)) if len(order) == n else ""


def _solve_min_height_trees(lines):
    n, m = map(int, lines[0].split())
    if n == 1:
        return "0"
    adj = [set() for _ in range(n)]
    for i in range(m):
        u, v = map(int, lines[1 + i].split())
        adj[u].add(v)
        adj[v].add(u)
    leaves = [i for i in range(n) if len(adj[i]) == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        nxt = []
        for leaf in leaves:
            nb = adj[leaf].pop()
            adj[nb].discard(leaf)
            if len(adj[nb]) == 1:
                nxt.append(nb)
        leaves = nxt
    return " ".join(map(str, sorted(leaves)))


def _solve_loud_and_rich(lines):
    n, m = map(int, lines[0].split())
    richer = [[] for _ in range(n)]
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        richer[b].append(a)
    quiet = list(map(int, lines[1 + m].split()))
    answer = [-1] * n

    def solve(x):
        if answer[x] != -1:
            return answer[x]
        answer[x] = x
        for y in richer[x]:
            cand = solve(y)
            if quiet[cand] < quiet[answer[x]]:
                answer[x] = cand
        return answer[x]

    return " ".join(str(solve(i)) for i in range(n))


def _solve_alien_dictionary(lines):
    n = int(lines[0])
    words = [lines[1 + i] for i in range(n)]
    letters = set("".join(words))
    adj = {c: set() for c in letters}
    indeg = {c: 0 for c in letters}
    for a, b in zip(words, words[1:]):
        if len(a) > len(b) and a.startswith(b):
            return ""
        for x, y in zip(a, b):
            if x != y:
                if y not in adj[x]:
                    adj[x].add(y)
                    indeg[y] += 1
                break
    import heapq
    heap = [c for c in letters if indeg[c] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        c = heapq.heappop(heap)
        order.append(c)
        for nb in sorted(adj[c]):
            indeg[nb] -= 1
            if indeg[nb] == 0:
                heapq.heappush(heap, nb)
    return "".join(order) if len(order) == len(letters) else ""


def _solve_parallel_courses(lines):
    n, m = map(int, lines[0].split())
    adj = [[] for _ in range(n + 1)]
    indeg = [0] * (n + 1)
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        adj[a].append(b)
        indeg[b] += 1
    frontier = [i for i in range(1, n + 1) if indeg[i] == 0]
    done = 0
    semesters = 0
    while frontier:
        semesters += 1
        nxt = []
        for node in frontier:
            done += 1
            for nb in adj[node]:
                indeg[nb] -= 1
                if indeg[nb] == 0:
                    nxt.append(nb)
        frontier = nxt
    return str(semesters) if done == n else "-1"


def _solve_word_ladder(lines):
    begin = lines[0]
    end = lines[1]
    n = int(lines[2])
    words = set(lines[3 + i] for i in range(n))
    if end not in words:
        return "0"
    frontier = {begin}
    seen = {begin}
    steps = 1
    letters = "abcdefghijklmnopqrstuvwxyz"
    while frontier:
        nxt = set()
        for w in frontier:
            if w == end:
                return str(steps)
            for i in range(len(w)):
                for c in letters:
                    cand = w[:i] + c + w[i + 1:]
                    if cand in words and cand not in seen:
                        seen.add(cand)
                        nxt.add(cand)
        frontier = nxt
        steps += 1
    return "0"


def _solve_words_within_two_edits(lines):
    q = int(lines[0])
    queries = [lines[1 + i] for i in range(q)]
    d = int(lines[1 + q])
    dictionary = [lines[2 + q + i] for i in range(d)]
    out = []
    for w in queries:
        for cand in dictionary:
            if len(cand) == len(w) and sum(a != b for a, b in zip(w, cand)) <= 2:
                out.append(w)
                break
    return " ".join(out)


def _solve_network_delay(lines):
    n, m, k = map(int, lines[0].split())
    adj = [[] for _ in range(n + 1)]
    for i in range(m):
        u, v, w = map(int, lines[1 + i].split())
        adj[u].append((v, w))
    import heapq
    dist = {}
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        for nb, w in adj[node]:
            if nb not in dist:
                heapq.heappush(heap, (d + w, nb))
    return str(max(dist.values())) if len(dist) == n else "-1"


def _solve_shortest_path_binary_matrix(lines):
    n = int(lines[0].split()[0])
    g = _igrid(lines, n)
    if g[0][0] != 0 or g[n - 1][n - 1] != 0:
        return "-1"
    if n == 1:
        return "1"
    seen = {(0, 0)}
    frontier = [(0, 0)]
    steps = 1
    while frontier:
        nxt = []
        for i, j in frontier:
            if (i, j) == (n - 1, n - 1):
                return str(steps)
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    ni, nj = i + di, j + dj
                    if (0 <= ni < n and 0 <= nj < n and g[ni][nj] == 0
                            and (ni, nj) not in seen):
                        seen.add((ni, nj))
                        nxt.append((ni, nj))
        frontier = nxt
        steps += 1
    return "-1"


def _solve_remove_methods(lines):
    n, k, m = map(int, lines[0].split())
    adj = [[] for _ in range(n)]
    edges = []
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        adj[a].append(b)
        edges.append((a, b))
    suspicious = set()
    stack = [k]
    suspicious.add(k)
    while stack:
        node = stack.pop()
        for nb in adj[node]:
            if nb not in suspicious:
                suspicious.add(nb)
                stack.append(nb)
    for a, b in edges:
        if a not in suspicious and b in suspicious:
            return " ".join(str(i) for i in range(n))
    return " ".join(str(i) for i in range(n) if i not in suspicious)


def _solve_path_minimum_effort(lines):
    m, n = map(int, lines[0].split())
    g = _igrid(lines, m)
    import heapq
    effort = [[float("inf")] * n for _ in range(m)]
    effort[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        e, i, j = heapq.heappop(heap)
        if (i, j) == (m - 1, n - 1):
            return str(e)
        if e > effort[i][j]:
            continue
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                cand = max(e, abs(g[ni][nj] - g[i][j]))
                if cand < effort[ni][nj]:
                    effort[ni][nj] = cand
                    heapq.heappush(heap, (cand, ni, nj))
    return "0"


def _solve_min_time_last_room(lines):
    m, n = map(int, lines[0].split())
    g = _igrid(lines, m)
    import heapq
    best = [[float("inf")] * n for _ in range(m)]
    best[0][0] = 0
    heap = [(0, 0, 0)]
    while heap:
        t, i, j = heapq.heappop(heap)
        if (i, j) == (m - 1, n - 1):
            return str(t)
        if t > best[i][j]:
            continue
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                arrive = max(t, g[ni][nj]) + 1
                if arrive < best[ni][nj]:
                    best[ni][nj] = arrive
                    heapq.heappush(heap, (arrive, ni, nj))
    return "-1"


def _solve_min_obstacle_removal(lines):
    m, n = map(int, lines[0].split())
    g = _igrid(lines, m)
    from collections import deque
    dist = [[float("inf")] * n for _ in range(m)]
    dist[0][0] = g[0][0]
    dq = deque([(0, 0)])
    while dq:
        i, j = dq.popleft()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                cand = dist[i][j] + g[ni][nj]
                if cand < dist[ni][nj]:
                    dist[ni][nj] = cand
                    if g[ni][nj] == 0:
                        dq.appendleft((ni, nj))
                    else:
                        dq.append((ni, nj))
    return str(dist[m - 1][n - 1])


def _solve_shortest_path_obstacles_k(lines):
    m, n = map(int, lines[0].split())
    g = _igrid(lines, m)
    k = int(lines[1 + m])
    if k >= m + n - 2:
        return str(m + n - 2)
    start = (0, 0, k - g[0][0])
    if start[2] < 0:
        return "-1"
    seen = {(0, 0): k - g[0][0]}
    frontier = [start]
    steps = 0
    while frontier:
        nxt = []
        for i, j, rem in frontier:
            if (i, j) == (m - 1, n - 1):
                return str(steps)
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    left = rem - g[ni][nj]
                    if left >= 0 and seen.get((ni, nj), -1) < left:
                        seen[(ni, nj)] = left
                        nxt.append((ni, nj, left))
        frontier = nxt
        steps += 1
    return "-1"


def _solve_smallest_black_rectangle(lines):
    m, n = map(int, lines[0].split())
    g = _igrid(lines, m)
    x, y = map(int, lines[1 + m].split())
    seen = {(x, y)}
    stack = [(x, y)]
    while stack:
        i, j = stack.pop()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n and g[ni][nj] == 1 and (ni, nj) not in seen:
                seen.add((ni, nj))
                stack.append((ni, nj))
    rows = [a for a, b in seen]
    cols = [b for a, b in seen]
    return str((max(rows) - min(rows) + 1) * (max(cols) - min(cols) + 1))


def _solve_equality_equations(lines):
    n = int(lines[0])
    eqs = [lines[1 + i] for i in range(n)]
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in eqs:
        if e[1] == "=":
            parent[find(e[0])] = find(e[3])
    for e in eqs:
        if e[1] == "!" and find(e[0]) == find(e[3]):
            return "false"
    return "true"

def _solve_find_center_star(lines):
    n = int(lines[0])
    a = list(map(int, lines[1].split()))
    b = list(map(int, lines[2].split()))
    # edge 0 is (a[0], b[0]) and edge 1 is (a[1], b[1]); the centre is
    # whichever endpoint of edge 0 also appears in edge 1.
    return str(a[0] if a[0] in (a[1], b[1]) else b[0])


def _solve_find_town_judge(lines):
    n, m = map(int, lines[0].split())
    trusts = [0] * (n + 1)
    trusted_by = [0] * (n + 1)
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        trusts[a] += 1
        trusted_by[b] += 1
    for p in range(1, n + 1):
        if trusts[p] == 0 and trusted_by[p] == n - 1:
            return str(p)
    return "-1"


def _solve_number_of_provinces(lines):
    n = int(lines[0])
    grid = [list(map(int, lines[1 + i].split())) for i in range(n)]
    seen = set()
    count = 0
    for i in range(n):
        if i in seen:
            continue
        count += 1
        stack = [i]
        seen.add(i)
        while stack:
            v = stack.pop()
            for w in range(n):
                if grid[v][w] == 1 and w not in seen:
                    seen.add(w)
                    stack.append(w)
    return str(count)


def _solve_rotting_oranges(lines):
    m, n = map(int, lines[0].split())
    grid = [list(map(int, lines[1 + i].split())) for i in range(m)]
    frontier = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == 2]
    fresh = sum(row.count(1) for row in grid)
    minutes = 0
    while fresh and frontier:
        nxt = []
        for i, j in frontier:
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n and grid[ni][nj] == 1:
                    grid[ni][nj] = 2
                    fresh -= 1
                    nxt.append((ni, nj))
        if not nxt:
            break
        frontier = nxt
        minutes += 1
    return str(-1 if fresh else minutes)


def _solve_keys_and_rooms(lines):
    n = int(lines[0])
    keys = []
    for i in range(n):
        parts = lines[1 + i].split()
        keys.append([int(x) for x in parts[1:]])
    seen = {0}
    stack = [0]
    while stack:
        r = stack.pop()
        for k in keys[r]:
            if k not in seen:
                seen.add(k)
                stack.append(k)
    return "true" if len(seen) == n else "false"


def _solve_redundant_connection(lines):
    m = int(lines[0])
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    answer = ""
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        ra, rb = find(a), find(b)
        if ra == rb:
            answer = f"{a} {b}"
        else:
            parent[ra] = rb
    return answer


def _solve_critical_connections(lines):
    n, m = map(int, lines[0].split())
    adj = [[] for _ in range(n)]
    for i in range(m):
        a, b = map(int, lines[1 + i].split())
        adj[a].append(b)
        adj[b].append(a)
    disc = [-1] * n
    low = [0] * n
    bridges = []
    timer = [0]

    def dfs(v, parent):
        disc[v] = low[v] = timer[0]
        timer[0] += 1
        skipped = False
        for w in adj[v]:
            if w == parent and not skipped:
                skipped = True
                continue
            if disc[w] == -1:
                dfs(w, v)
                low[v] = min(low[v], low[w])
                if low[w] > disc[v]:
                    bridges.append((min(v, w), max(v, w)))
            else:
                low[v] = min(low[v], disc[w])

    for v in range(n):
        if disc[v] == -1:
            dfs(v, -1)
    return "\n".join(f"{a} {b}" for a, b in sorted(bridges))


def _solve_cheapest_flights_k_stops(lines):
    n, m, src, dst, k = map(int, lines[0].split())
    edges = []
    for i in range(m):
        u, v, w = map(int, lines[1 + i].split())
        edges.append((u, v, w))
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        nxt = list(dist)
        for u, v, w in edges:
            if dist[u] + w < nxt[v]:
                nxt[v] = dist[u] + w
        dist = nxt
    return str(dist[dst]) if dist[dst] != INF else "-1"


def _solve_reconstruct_itinerary(lines):
    m = int(lines[0])
    from collections import defaultdict
    adj = defaultdict(list)
    for i in range(m):
        a, b = lines[1 + i].split()
        adj[a].append(b)
    for k in adj:
        adj[k].sort(reverse=True)
    route = []
    stack = ["JFK"]
    while stack:
        while adj[stack[-1]]:
            stack.append(adj[stack[-1]].pop())
        route.append(stack.pop())
    return " ".join(reversed(route))


PROBLEMS = [
{
        "title": "Number of Islands",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Given an m x n 2D binary grid representing a map of '1' (land) and '0' (water), return the number of islands (land cells connected horizontally or vertically).",
        "example_input": "4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0",
        "constraints": "Input format: line 1 is \"rows cols\", followed by `rows` lines of `cols` space-separated 0/1 values. Output format: a single integer.",
        "solve": _solve_number_of_islands,
        "sample_inputs": ["4 5\n1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "3 4\n1 1 0 0\n0 1 0 0\n0 0 1 1"],
        "hidden_inputs": [
            "1 1\n0",                    # single water cell
            "1 1\n1",                    # single land cell
            "2 2\n0 0\n0 0",
            "2 2\n1 1\n1 1",
            "1 5\n1 0 1 0 1",            # single row
            "5 1\n1\n0\n1\n1\n0",        # single column
            "3 3\n1 0 1\n0 1 0\n1 0 1",  # diagonal touch does NOT connect
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 3\n1 1 0\n1 0 0\n0 0 1",
            "4 4\n1 0 0 1\n0 0 0 0\n0 0 0 0\n1 0 0 1",
        ],
    },
{
        "title": "Find if Path Exists in Graph",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "Given an undirected graph with n nodes (0-indexed) and a list of edges, determine if there is a valid path from a source node to a destination node.",
        "example_input": "3 2 0 2\n0 1\n1 2",
        "constraints": "Input format: line 1 is \"n m source destination\", followed by `m` lines each \"u v\" describing an edge. Output format: \"true\" or \"false\".",
        "solve": _solve_find_path_exists,
        "sample_inputs": ["3 2 0 2\n0 1\n1 2", "5 4 0 4\n0 1\n1 2\n2 3\n3 4"],
        "hidden_inputs": [
            "1 0 0 0",                           # source is the destination, no edges
            "2 0 0 1",                           # no edges at all
            "2 1 0 1\n0 1",
            "4 2 0 3\n0 1\n2 3",
            "3 3 2 0\n0 1\n1 2\n0 2",            # traversal must work both directions
            "6 3 0 5\n0 1\n1 2\n3 4",            # disconnected components
            "6 5 0 5\n0 1\n1 2\n2 3\n3 4\n4 5",  # long chain
            "5 5 0 4\n0 1\n1 2\n2 0\n3 4\n0 3",  # cycle plus a bridge
            "4 4 1 3\n0 1\n1 2\n2 3\n3 0",
        ],
    },
{
        "title": "Course Schedule",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "There are n courses (0-indexed) and a list of prerequisite pairs [a, b] meaning course b must be taken before course a. Return whether it's possible to finish all courses.",
        "example_input": "2 1\n1 0",
        "constraints": "Input format: line 1 is \"n m\", followed by `m` lines each \"a b\" meaning b is a prerequisite of a. Output format: \"true\" or \"false\".",
        "solve": _solve_course_schedule,
        "sample_inputs": ["2 1\n1 0", "3 2\n1 0\n2 1"],
        "hidden_inputs": [
            "1 0",                      # one course, no prerequisites
            "3 0",                      # no prerequisites at all
            "1 1\n0 0",                 # course is its own prerequisite
            "2 2\n1 0\n0 1",
            "3 3\n0 1\n1 2\n2 0",       # three-node cycle
            "4 3\n1 0\n2 1\n3 2",
            "4 4\n1 0\n2 0\n3 1\n3 2",  # diamond DAG
            "4 3\n1 0\n2 1\n0 2",       # cycle plus an unrelated free node
            "6 4\n1 0\n2 1\n4 3\n5 4",  # two independent chains
            "5 4\n1 0\n2 1\n3 2\n4 3",
        ],
    },
{
        "title": "Surrounded Regions",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "A board holds the letters X and O. Every region of O cells that is entirely surrounded by X cells becomes X. A region touching the border is never captured. Return the resulting board.",
        "example_input": "4 4\nX X X X\nX O O X\nX X O X\nX O X X",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated X and O. Output format: the resulting board in the same layout.",
        "solve": _solve_surrounded_regions,
        "sample_inputs": ["4 4\nX X X X\nX O O X\nX X O X\nX O X X", "1 1\nO"],
        "hidden_inputs": [
            "1 1\nX",               # nothing to do
            "1 2\nO O",             # both touch the border
            "2 2\nO O\nO O",        # every cell is on the border
            "2 2\nX X\nX X",
            "3 3\nX X X\nX O X\nX X X",   # a single enclosed cell
            "3 3\nO O O\nO O O\nO O O",   # nothing is enclosed
            "3 3\nX X X\nX O X\nX O X",   # the region reaches the bottom border
            "4 4\nX X X X\nX O O X\nX O O X\nX X X X",
            "3 4\nX O X X\nX X O X\nX X X X",
            "5 5\nX X X X X\nX O O O X\nX O X O X\nX O O O X\nX X X X X",
        ],
    },
{
        "title": "Walls and Gates",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "A grid holds walls marked W, gates marked G and empty rooms marked with a dot. Fill every empty room with its distance to the nearest gate, moving only up, down, left or right. Rooms that cannot reach a gate stay empty.",
        "example_input": "4 4\n. W G .\n. . . W\n. W . W\nG W . .",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated cells, each W, G or a dot. Output format: the same layout, with each room replaced by its distance, W kept for walls and a dash for an unreachable room.",
        "solve": _solve_walls_and_gates,
        "sample_inputs": ["4 4\n. W G .\n. . . W\n. W . W\nG W . .", "1 3\nG . ."],
        "hidden_inputs": [
            "1 1\nG",               # a gate alone
            "1 1\nW",               # a wall alone
            "1 1\n.",               # an unreachable room
            "1 2\nG .",
            "1 2\n. .",             # no gate at all
            "2 2\nG .\n. .",
            "2 2\nW W\nW W",        # all walls
            "3 3\n. . .\n. G .\n. . .",   # a central gate reaches everything
            "3 3\nG . W\n. . W\nW W .",   # a room sealed behind walls
            "2 4\nG W . .\n. . . G",
        ],
    },
{
        "title": "Max Area of Island",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "An island is a group of 1 cells joined horizontally or vertically. Return the number of cells in the largest island, or 0 if there is none.",
        "example_input": "4 8\n0 0 1 0 0 0 0 0\n0 0 0 0 0 0 0 0\n0 1 1 0 1 0 0 0\n0 1 0 0 1 1 0 0",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated 0 and 1 values. Output format: a single integer.",
        "solve": _solve_max_area_island,
        "sample_inputs": ["4 8\n0 0 1 0 0 0 0 0\n0 0 0 0 0 0 0 0\n0 1 1 0 1 0 0 0\n0 1 0 0 1 1 0 0", "1 1\n1"],
        "hidden_inputs": [
            "1 1\n0",               # no island at all
            "1 4\n0 0 0 0",
            "1 4\n1 1 1 1",         # one island filling the row
            "4 1\n1\n0\n1\n1",      # a single column, two islands
            "2 2\n1 1\n1 1",
            "3 3\n1 0 1\n0 1 0\n1 0 1",   # diagonals do not join
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 4\n1 1 0 0\n0 1 0 1\n0 0 0 1",
            "2 5\n1 0 1 1 0\n1 0 0 1 1",
            "4 4\n0 0 0 0\n0 1 1 0\n0 1 1 0\n0 0 0 0",
        ],
    },
{
        "title": "Battleships in a Board",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "A board holds battleships marked X and empty water marked with a dot. Every battleship occupies a single row or a single column, and no two battleships touch. Count the battleships.",
        "example_input": "4 4\nX . . X\n. . . X\n. . . X\n. . . .",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated X and dot cells. Output format: a single integer.",
        "solve": _solve_battleships,
        "sample_inputs": ["4 4\nX . . X\n. . . X\n. . . X\n. . . .", "1 1\nX"],
        "hidden_inputs": [
            "1 1\n.",               # an empty board
            "1 3\nX . X",           # two separate ships in a row
            "3 1\nX\n.\nX",         # two separate ships in a column
            "1 4\nX X X X",         # one long horizontal ship
            "4 1\nX\nX\nX\nX",      # one long vertical ship
            "2 2\n. .\n. .",
            "3 3\nX . X\n. . .\nX . X",   # four single-cell ships
            "3 5\nX X . . X\n. . . . X\nX . X . .",
            "2 4\n. X X .\n. . . .",
            "5 5\nX . . . X\n. . . . .\nX X X . .\n. . . . .\n. . . X .",
        ],
    },
{
        "title": "Minimum Height Trees",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "Given a tree with n nodes, rooting it at different nodes produces trees of different heights. Return every node that, when chosen as the root, gives the smallest possible height, in increasing order.",
        "example_input": "4 3\n1 0\n1 2\n1 3",
        "constraints": "Input format: line 1 is \"n m\", followed by m lines each \"u v\" describing an undirected edge; the graph is always a tree. Output format: the root labels, space-separated ascending.",
        "solve": _solve_min_height_trees,
        "sample_inputs": ["4 3\n1 0\n1 2\n1 3", "6 5\n3 0\n3 1\n3 2\n3 4\n5 4"],
        "hidden_inputs": [
            "1 0",                  # a single node
            "2 1\n0 1",             # both ends tie
            "3 2\n0 1\n1 2",        # the middle node wins
            "4 3\n0 1\n1 2\n2 3",   # an even path gives two centres
            "5 4\n0 1\n1 2\n2 3\n3 4",
            "5 4\n0 1\n0 2\n0 3\n0 4",   # a star has one centre
            "6 5\n0 1\n1 2\n2 3\n3 4\n4 5",
            "7 6\n0 1\n0 2\n1 3\n1 4\n2 5\n2 6",
            "3 2\n1 0\n1 2",
            "8 7\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7",
        ],
    },
{
        "title": "Shortest Path in Binary Matrix",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "In a square grid of 0 and 1, find the shortest path from the top-left cell to the bottom-right cell that visits only 0 cells and may step to any of the eight neighbours. Return the number of cells on that path, or -1 if none exists.",
        "example_input": "3 3\n0 0 0\n1 1 0\n1 1 0",
        "constraints": "Input format: line 1 is \"n n\", followed by n lines of space-separated 0 and 1 values. Output format: a single integer, or -1.",
        "solve": _solve_shortest_path_binary_matrix,
        "sample_inputs": ["3 3\n0 0 0\n1 1 0\n1 1 0", "2 2\n0 1\n1 0"],
        "hidden_inputs": [
            "1 1\n0",               # already at the destination
            "1 1\n1",               # the only cell is blocked
            "2 2\n1 0\n0 0",        # the start is blocked
            "2 2\n0 0\n0 1",        # the destination is blocked
            "2 2\n0 0\n0 0",
            "3 3\n0 0 0\n0 0 0\n0 0 0",   # the diagonal is shortest
            "3 3\n0 1 0\n1 1 0\n0 0 0",
            "3 3\n0 1 1\n1 1 1\n1 1 0",   # completely walled off
            "4 4\n0 0 0 0\n1 1 1 0\n0 0 0 0\n0 1 1 0",
            "5 5\n0 1 0 0 0\n0 1 0 1 0\n0 0 0 1 0\n1 1 1 1 0\n0 0 0 0 0",
        ],
    },
{
        "title": "Satisfiability of Equality Equations",
        "topic": "graphs",
        "difficulty": "easy",
        "description": "Each equation compares two single lowercase letters, either asserting they are equal or asserting they differ. Decide whether letters can be assigned values so that every equation holds.",
        "example_input": "2\na==b\nb!=a",
        "constraints": "Input format: line 1 is the number of equations, followed by that many lines each exactly four characters. Output format: \"true\" or \"false\".",
        "solve": _solve_equality_equations,
        "sample_inputs": ["2\na==b\nb!=a", "2\nb==a\na==b"],
        "hidden_inputs": [
            "1\na==a",              # trivially satisfiable
            "1\na!=a",              # immediately contradictory
            "1\na==b",
            "1\na!=b",
            "3\na==b\nb==c\na==c",  # a consistent chain
            "3\na==b\nb==c\na!=c",  # the chain makes the last impossible
            "4\nc==c\nb==d\nx!=z\na==b",
            "4\na==b\nc==d\na!=c\nb!=d",
            "5\na==b\nb==c\nc==d\nd==e\na!=e",
            "2\nf!=g\ng!=f",
        ],
    },
{
        "title": "Course Schedule II",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "There are n courses numbered from 0 and a list of prerequisite pairs. Return an order in which every course can be taken; when several orders work, return the one that is smallest when read as a sequence of numbers. If no order exists, return nothing.",
        "example_input": "4 4\n1 0\n2 0\n3 1\n3 2",
        "constraints": "Input format: line 1 is \"n m\", followed by m lines each \"a b\" meaning b must come before a. Output format: the course order, space-separated, or an empty line if impossible.",
        "solve": _solve_course_schedule_ii,
        "sample_inputs": ["4 4\n1 0\n2 0\n3 1\n3 2", "2 1\n1 0"],
        "hidden_inputs": [
            "1 0",                  # one course, no prerequisites
            "3 0",                  # no constraints, plain ascending order
            "1 1\n0 0",             # a course requiring itself
            "2 2\n1 0\n0 1",        # a two-node cycle
            "3 3\n0 1\n1 2\n2 0",
            "3 2\n1 0\n2 1",        # a forced chain
            "4 2\n1 0\n3 2",        # two independent chains interleave
            "5 4\n1 0\n2 1\n3 2\n4 3",
            "4 3\n1 0\n2 1\n0 2",   # a cycle plus a free node
            "6 4\n2 0\n3 1\n4 2\n5 3",
        ],
    },
{
        "title": "Loud and Rich",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Each person has an amount of money and a quietness value. Given pairs stating that one person has more money than another, report for every person the quietest person among everyone known to have at least as much money as they do, including themselves.",
        "example_input": "8 6\n1 0\n2 1\n2 5\n0 6\n3 6\n3 7\n3 2 5 4 6 1 7 0",
        "constraints": "Input format: line 1 is \"n m\", followed by m lines each \"a b\" meaning a has more money than b, then a final line of n quietness values, which are all distinct so the answer is unique. Output format: n answers, space-separated.",
        "solve": _solve_loud_and_rich,
        "sample_inputs": ["8 6\n1 0\n2 1\n2 5\n0 6\n3 6\n3 7\n3 2 5 4 6 1 7 0", "2 1\n0 1\n1 0"],
        "hidden_inputs": [
            "1 0\n0",               # one person answers themselves
            "2 0\n0 1",             # nobody is richer than anybody
            "2 1\n1 0\n0 1",
            "3 0\n2 1 0",           # no edges, each answers themselves
            "3 2\n0 1\n1 2\n0 1 2", # a chain, richest is quietest
            "3 2\n0 1\n1 2\n2 1 0", # a chain, poorest is quietest
            "4 3\n0 1\n0 2\n0 3\n3 0 1 2",
            "4 2\n1 0\n3 2\n1 2 3 0",
            "5 4\n0 1\n1 2\n2 3\n3 4\n4 3 2 1 0",
            "3 3\n0 1\n1 2\n0 2\n0 1 2",   # the richest is also the quietest
        ],
    },
{
        "title": "Parallel Courses",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Courses are numbered from 1 to n, with relations saying one must be studied before another. In each semester you may take any number of courses whose prerequisites are already done. Return the fewest semesters needed, or -1 if some course can never be taken.",
        "example_input": "3 2\n1 3\n2 3",
        "constraints": "Input format: line 1 is \"n m\", followed by m lines each \"a b\" meaning a must come before b. Output format: a single integer, or -1.",
        "solve": _solve_parallel_courses,
        "sample_inputs": ["3 2\n1 3\n2 3", "3 3\n1 2\n2 3\n3 1"],
        "hidden_inputs": [
            "1 0",                  # one course, one semester
            "3 0",                  # everything at once
            "1 1\n1 1",             # a course before itself
            "2 1\n1 2",
            "2 2\n1 2\n2 1",        # a two-course cycle
            "4 3\n1 2\n2 3\n3 4",   # a strict chain
            "4 2\n1 2\n3 4",        # two chains run in parallel
            "5 4\n1 2\n1 3\n2 4\n3 4",
            "6 5\n1 2\n2 3\n4 5\n5 6\n1 4",
            "5 5\n1 2\n2 3\n3 4\n4 5\n5 3",
        ],
    },
{
        "title": "Words Within Two Edits of Dictionary",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "Every word has the same length. A query word is acceptable when some dictionary word can be obtained from it by changing at most two letters in place. Return the acceptable queries, keeping their original order.",
        "example_input": "3\nword\note\npit\n3\nwood\njoke\npool",
        "constraints": "Input format: line 1 is the number of queries, then that many query words, then a line with the dictionary size, then that many dictionary words. Output format: the acceptable queries, space-separated (empty if none).",
        "solve": _solve_words_within_two_edits,
        "sample_inputs": ["3\nword\note\npit\n3\nwood\njoke\npool", "2\nyes\nnot\n1\nyes"],
        "hidden_inputs": [
            "1\nab\n1\nab",         # an exact match needs no edits
            "1\nab\n1\ncd",         # two edits is still acceptable
            "1\nabc\n1\nxyz",       # three edits is too many
            "1\nab\n1\nabc",        # different lengths never match
            "2\naa\nbb\n1\naa",
            "3\nabc\nabd\nxyz\n1\nabc",
            "2\nhello\nworld\n2\nhallo\nwurld",
            "2\nhello\nworld\n1\nxxxxx",
            "4\ncat\nbat\nrat\ndog\n1\ncot",
            "2\nabcd\nefgh\n2\nabxy\nefzz",
        ],
    },
{
        "title": "Network Delay Time",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "A signal starts at one node of a directed weighted network and travels along every edge it can. Return how long until all n nodes have received it, or -1 if some node never does.",
        "example_input": "4 3 2\n2 1 1\n2 3 1\n3 4 1",
        "constraints": "Input format: line 1 is \"n m k\" where k is the starting node, followed by m lines each \"u v w\". Nodes are numbered from 1. Output format: a single integer, or -1.",
        "solve": _solve_network_delay,
        "sample_inputs": ["4 3 2\n2 1 1\n2 3 1\n3 4 1", "2 1 1\n1 2 1"],
        "hidden_inputs": [
            "1 0 1",                # one node, already reached
            "2 0 1",                # the second node is unreachable
            "2 1 2\n1 2 1",         # the edge points the wrong way
            "2 1 1\n1 2 5",
            "3 2 1\n1 2 1\n2 3 1",  # a chain
            "3 2 1\n1 2 1\n1 3 4",  # the slowest branch decides
            "3 3 1\n1 2 5\n1 3 1\n3 2 1",   # a detour is faster than the direct edge
            "4 4 1\n1 2 1\n2 3 1\n3 4 1\n1 4 9",
            "4 2 1\n1 2 1\n3 4 1",  # a disconnected component
            "5 6 1\n1 2 2\n1 3 4\n2 3 1\n3 4 3\n2 5 7\n4 5 1",
        ],
    },
{
        "title": "Path With Minimum Effort",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "A grid holds heights. Travelling from the top-left cell to the bottom-right cell, moving only up, down, left or right, the effort of a route is the largest height difference between any two consecutive cells on it. Return the smallest possible effort.",
        "example_input": "3 3\n1 2 2\n3 8 2\n5 3 5",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of integers. Output format: a single integer.",
        "solve": _solve_path_minimum_effort,
        "sample_inputs": ["3 3\n1 2 2\n3 8 2\n5 3 5", "3 3\n1 2 3\n3 8 4\n5 3 5"],
        "hidden_inputs": [
            "1 1\n5",               # nowhere to move, zero effort
            "1 2\n1 1",             # a flat step
            "1 2\n1 9",             # a single large step
            "2 1\n1\n4",
            "2 2\n1 1\n1 1",        # a flat grid
            "2 2\n1 2\n3 4",
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 3\n1 9 1\n1 9 1\n1 1 1",   # a long flat detour beats the short climb
            "3 3\n1 2 3\n4 5 6\n7 8 9",
            "4 4\n1 10 6 7\n1 1 1 1\n9 9 9 1\n1 1 1 1",
        ],
    },
{
        "title": "Minimum Obstacle Removal to Reach Corner",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "A grid holds empty cells marked 0 and obstacles marked 1. Moving only up, down, left or right from the top-left cell to the bottom-right cell, return the fewest obstacles that must be removed to make the journey possible.",
        "example_input": "3 3\n0 1 1\n1 1 0\n1 1 0",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of space-separated 0 and 1 values. Output format: a single integer.",
        "solve": _solve_min_obstacle_removal,
        "sample_inputs": ["3 3\n0 1 1\n1 1 0\n1 1 0", "3 3\n0 1 0\n0 0 0\n0 1 0"],
        "hidden_inputs": [
            "1 1\n0",               # already there, nothing to remove
            "1 1\n1",               # the only cell is an obstacle
            "1 3\n0 1 0",           # one obstacle blocks the row
            "3 1\n0\n1\n0",
            "2 2\n0 0\n0 0",        # a clear path
            "2 2\n0 1\n1 0",        # either route costs one
            "3 3\n0 0 0\n0 0 0\n0 0 0",
            "3 3\n0 1 1\n1 1 1\n1 1 0",   # every route is obstructed
            "3 4\n0 0 0 0\n1 1 1 0\n0 0 0 0",   # a free detour exists
            "4 4\n0 1 0 1\n0 1 0 1\n0 1 0 1\n0 0 0 0",
        ],
    },
{
        "title": "Smallest Rectangle Enclosing Black Pixels",
        "topic": "graphs",
        "difficulty": "medium",
        "description": "A grid holds white pixels marked 0 and black pixels marked 1, and all the black pixels are connected horizontally or vertically. Given the position of one black pixel, return the area of the smallest axis-aligned rectangle that contains every black pixel.",
        "example_input": "4 5\n0 0 1 0 0\n0 1 1 0 0\n0 1 0 0 0\n0 0 0 0 0\n1 2",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many grid lines, then a final line \"x y\" giving a black pixel's row and column. Output format: a single integer, the area.",
        "solve": _solve_smallest_black_rectangle,
        "sample_inputs": ["4 5\n0 0 1 0 0\n0 1 1 0 0\n0 1 0 0 0\n0 0 0 0 0\n1 2", "1 1\n1\n0 0"],
        "hidden_inputs": [
            "1 2\n1 1\n0 0",        # a horizontal pair
            "2 1\n1\n1\n0 0",       # a vertical pair
            "3 3\n0 0 0\n0 1 0\n0 0 0\n1 1",    # a lone pixel
            "3 3\n1 1 1\n0 0 0\n0 0 0\n0 0",    # a full top row
            "3 3\n1 0 0\n1 0 0\n1 0 0\n0 0",    # a full left column
            "3 3\n1 1 1\n1 1 1\n1 1 1\n1 1",    # the whole grid
            "4 4\n0 0 0 0\n0 1 1 0\n0 1 1 0\n0 0 0 0\n1 1",
            "3 4\n0 1 0 0\n0 1 1 0\n0 0 1 0\n0 1",   # an L shape
            "2 4\n0 0 1 1\n0 0 0 1\n0 2",
            "5 5\n0 0 0 0 0\n0 0 1 0 0\n0 1 1 1 0\n0 0 1 0 0\n0 0 0 0 0\n2 2",
        ],
    },
{
        "title": "Pacific Atlantic Water Flow",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "Rain falling on a grid of heights flows to a neighbouring cell of equal or lower height. The Pacific borders the top and left edges, the Atlantic the bottom and right. Report every cell from which water can reach both oceans.",
        "example_input": "5 5\n1 2 2 3 5\n3 2 3 4 4\n2 4 5 3 1\n6 7 1 4 5\n5 1 1 2 4",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of heights. Output format: one cell per line as \"row col\", ordered by row then column.",
        "solve": _solve_pacific_atlantic,
        "sample_inputs": ["5 5\n1 2 2 3 5\n3 2 3 4 4\n2 4 5 3 1\n6 7 1 4 5\n5 1 1 2 4", "1 1\n1"],
        "hidden_inputs": [
            "1 2\n1 2",             # a single row touches both oceans
            "2 1\n1\n2",            # a single column
            "2 2\n1 1\n1 1",        # a flat grid, every cell qualifies
            "2 2\n1 2\n3 4",
            "3 3\n1 1 1\n1 1 1\n1 1 1",
            "3 3\n1 2 3\n8 9 4\n7 6 5",   # a spiral of heights
            "3 3\n3 2 1\n2 1 2\n1 2 3",   # a basin in the middle
            "2 3\n1 2 3\n4 5 6",
            "3 2\n5 4\n3 2\n1 1",
            "4 4\n1 2 3 4\n2 3 4 5\n3 4 5 6\n4 5 6 7",
        ],
    },
{
        "title": "Alien Dictionary",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "A list of words is sorted according to an unknown alphabet that uses only the letters appearing in those words. Work out that alphabet. When several orderings fit, return the one that comes first alphabetically in ordinary English order. Return nothing if the list contradicts itself.",
        "example_input": "5\nwrt\nwrf\ner\nett\nrftt",
        "constraints": "Input format: line 1 is the number of words, followed by that many lowercase words. Output format: the letters in order as a single string, or an empty line if no ordering fits.",
        "solve": _solve_alien_dictionary,
        "sample_inputs": ["5\nwrt\nwrf\ner\nett\nrftt", "2\nz\nx"],
        "hidden_inputs": [
            "1\na",                 # a single letter
            "1\nab",                # one word fixes nothing but the alphabet
            "2\nab\nab",            # identical words give no constraint
            "2\nz\nz",
            "2\nabc\nab",           # a prefix after its extension is invalid
            "2\nab\nabc",           # the same pair the valid way round
            "3\nz\nx\nz",           # a contradictory cycle
            "3\nba\nbc\nac",
            "4\nwrt\nwrf\ner\nett",
            "3\nac\nab\nzc",        # several orders fit, the smallest is chosen
        ],
    },
{
        "title": "Word Ladder",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "Change one letter at a time, keeping every intermediate word in the given list, to turn the first word into the second. Return the number of words in the shortest such sequence counting both ends, or 0 if it cannot be done.",
        "example_input": "hit\ncog\n6\nhot\ndot\ndog\nlot\nlog\ncog",
        "constraints": "Input format: line 1 is the start word, line 2 is the target, line 3 is the list size, followed by that many words. Output format: a single integer.",
        "solve": _solve_word_ladder,
        "sample_inputs": ["hit\ncog\n6\nhot\ndot\ndog\nlot\nlog\ncog", "hit\ncog\n5\nhot\ndot\ndog\nlot\nlog"],
        "hidden_inputs": [
            "a\nb\n1\nb",           # one change away
            "a\na\n1\na",           # start equals target
            "a\nb\n1\nc",           # the target is not in the list
            "ab\ncd\n2\nad\ncd",    # two changes through one intermediate
            "ab\ncd\n1\ncd",        # no single-letter route exists
            "hot\ndog\n3\nhot\ndog\ndot",
            "hot\ndog\n2\nhot\ndog", # the two ends differ by two letters
            "red\ntax\n5\nted\ntex\nred\ntax\ntad",
            "leet\ncode\n6\nlest\nleet\nlose\ncode\nlode\nrobe",
            "cat\ndog\n4\ncat\ncot\ncog\ndog",
        ],
    },
{
        "title": "Remove Methods From Project",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "Methods are numbered from 0 and some invoke others. One method is known to be faulty, and it plus everything it can reach is to be removed. If any method outside that group invokes one inside it, nothing can safely be removed. Report the surviving methods in increasing order.",
        "example_input": "4 1 3\n1 0\n0 2\n0 3",
        "constraints": "Input format: line 1 is \"n k m\" where k is the faulty method, followed by m lines each \"a b\" meaning a invokes b. Output format: the surviving method numbers, space-separated (empty if none survive).",
        "solve": _solve_remove_methods,
        "sample_inputs": ["4 1 3\n1 0\n0 2\n0 3", "5 0 4\n1 0\n2 0\n3 0\n4 0"],
        "hidden_inputs": [
            "1 0 0",                # the only method is faulty
            "2 0 0",                # no invocations, one is removed
            "2 1 1\n0 1",           # an outside method invokes the faulty one
            "3 0 2\n0 1\n1 2",      # the fault reaches everything
            "3 2 0",                # an isolated faulty method
            "3 1 1\n1 2",
            "4 1 2\n1 2\n3 0",      # two independent groups
            "4 0 3\n0 1\n1 2\n2 3",
            "5 2 3\n2 3\n3 4\n0 1",
            "4 2 2\n2 3\n1 3",      # a survivor reaches into the removed group
        ],
    },
{
        "title": "Find Minimum Time to Reach Last Room",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "Each room carries the earliest moment you are allowed to enter it. Starting in the top-left room at time zero, each move to an adjacent room takes one second, and you may wait as long as you like before moving. Return the earliest time you can reach the bottom-right room.",
        "example_input": "2 2\n0 4\n4 4",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of earliest-entry times. Output format: a single integer.",
        "solve": _solve_min_time_last_room,
        "sample_inputs": ["2 2\n0 4\n4 4", "2 3\n0 0 0\n0 0 0"],
        "hidden_inputs": [
            "1 1\n0",               # already in the last room
            "1 1\n9",               # the start's own time never applies
            "1 2\n0 0",             # one move, no waiting
            "1 2\n0 5",             # one move after a wait
            "2 1\n0\n3",
            "2 2\n0 0\n0 0",
            "2 2\n0 9\n1 1",        # the longer route avoids the wait
            "3 3\n0 0 0\n0 0 0\n0 0 0",
            "3 3\n0 1 2\n3 4 5\n6 7 8",
            "3 3\n0 9 9\n9 9 9\n9 9 0",   # waiting is unavoidable
        ],
    },
{
        "title": "Shortest Path in a Grid with Obstacles Elimination",
        "topic": "graphs",
        "difficulty": "hard",
        "description": "A grid holds empty cells marked 0 and obstacles marked 1. Moving only up, down, left or right, travel from the top-left cell to the bottom-right cell while removing at most k obstacles. Return the fewest steps needed, or -1 if it cannot be done.",
        "example_input": "3 3\n0 0 0\n1 1 0\n0 0 0\n1",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many grid lines, then a final line holding k. Output format: a single integer, or -1.",
        "solve": _solve_shortest_path_obstacles_k,
        "sample_inputs": ["3 3\n0 0 0\n1 1 0\n0 0 0\n1", "3 3\n0 1 1\n1 1 1\n1 0 0\n1"],
        "hidden_inputs": [
            "1 1\n0\n0",            # already at the destination
            "1 2\n0 0\n0",          # a clear single step
            "1 2\n0 1\n0",          # blocked with no budget
            "1 2\n0 1\n1",          # the same wall with budget
            "2 2\n0 0\n0 0\n0",
            "2 2\n0 1\n1 0\n1",
            "2 2\n0 1\n1 0\n0",     # no budget, no route
            "3 3\n0 0 0\n1 1 1\n0 0 0\n1",
            "3 3\n0 1 0\n1 1 0\n0 0 0\n2",
            "4 4\n0 1 1 1\n1 1 1 1\n1 1 1 1\n1 1 1 0\n3",   # budget too small
        ],
    },
{
        "title": "Find Center of Star Graph",
        "topic": "graphs", "difficulty": "easy",
        "description": "Every edge of the graph joins one particular node to some other node. Return that central node.",
        "example_input": "4\n1 2 4\n2 3 2",
        "constraints": "Input format: line 1 is the number of nodes, line 2 is the space-separated first endpoints of the edges, line 3 is the matching second endpoints. Output format: a single integer.",
        "solve": _solve_find_center_star,
        "sample_inputs": ["4\n1 2 4\n2 3 2", "3\n1 2\n2 3"],
        "hidden_inputs": [
            "3\n2 3\n1 2",          # the centre is the second endpoint
            "4\n1 3 3\n3 2 4",      # the centre is shared by edges 0 and 1
            "4\n1 2 3\n4 4 4",      # the centre is always second
            "4\n4 4 4\n1 2 3",      # and always first
            "5\n1 1 1 1\n2 3 4 5",
            "5\n2 3 4 5\n1 1 1 1",
            "3\n3 3\n1 2",
            "4\n2 2 2\n1 3 4",
            "6\n5 5 5 5 5\n1 2 3 4 6",
            "4\n1 4 4\n4 2 3",      # the centre appears on both sides
        ],
    },
{
        "title": "Find the Town Judge",
        "topic": "graphs", "difficulty": "easy",
        "description": "The judge trusts nobody, and everybody else trusts the judge. Given who trusts whom, return the judge, or -1 if there is none.",
        "example_input": "2 1\n1 2",
        "constraints": "Input format: line 1 is \"n m\", followed by m lines each \"a b\" meaning a trusts b. People are numbered from 1. Output format: a single integer.",
        "solve": _solve_find_town_judge,
        "sample_inputs": ["2 1\n1 2", "3 3\n1 3\n2 3\n3 1"],
        "hidden_inputs": [
            "1 0",                  # one person is trivially the judge
            "2 0",                  # nobody trusts anybody
            "2 1\n2 1",             # the other direction
            "2 2\n1 2\n2 1",        # mutual trust leaves no judge
            "3 2\n1 3\n2 3",
            "3 1\n1 3",             # not everyone trusts them
            "3 3\n1 2\n2 3\n3 1",   # a trust cycle
            "4 3\n1 3\n2 3\n4 3",
            "4 4\n1 4\n2 4\n3 4\n4 1",
            "3 2\n1 2\n2 3",
        ],
    },
{
        "title": "Number of Provinces",
        "topic": "graphs", "difficulty": "medium",
        "description": "A grid records which cities are directly connected. A province is a group of cities reachable from one another, directly or indirectly. Count the provinces.",
        "example_input": "3\n1 1 0\n1 1 0\n0 0 1",
        "constraints": "Input format: line 1 is the number of cities, followed by that many lines of 0 and 1 values; the grid is symmetric with ones on the diagonal. Output format: a single integer.",
        "solve": _solve_number_of_provinces,
        "sample_inputs": ["3\n1 1 0\n1 1 0\n0 0 1", "3\n1 0 0\n0 1 0\n0 0 1"],
        "hidden_inputs": [
            "1\n1",                 # one city, one province
            "2\n1 0\n0 1",          # two separate
            "2\n1 1\n1 1",          # two joined
            "3\n1 1 1\n1 1 1\n1 1 1",
            "4\n1 1 0 0\n1 1 0 0\n0 0 1 1\n0 0 1 1",
            "4\n1 0 0 1\n0 1 1 0\n0 1 1 0\n1 0 0 1",
            "4\n1 0 0 0\n0 1 0 0\n0 0 1 0\n0 0 0 1",
            "5\n1 1 0 0 0\n1 1 1 0 0\n0 1 1 0 0\n0 0 0 1 1\n0 0 0 1 1",
            "3\n1 1 0\n1 1 1\n0 1 1",   # joined through the middle
            "5\n1 0 0 0 1\n0 1 0 0 0\n0 0 1 0 0\n0 0 0 1 0\n1 0 0 0 1",
        ],
    },
{
        "title": "Rotting Oranges",
        "topic": "graphs", "difficulty": "medium",
        "description": "A grid holds empty cells marked 0, fresh oranges marked 1 and rotten ones marked 2. Each minute every fresh orange touching a rotten one on an edge becomes rotten. Return the minutes until none are fresh, or -1 if some never rot.",
        "example_input": "3 3\n2 1 1\n1 1 0\n0 1 1",
        "constraints": "Input format: line 1 is \"rows cols\", followed by that many lines of 0, 1 and 2 values. Output format: a single integer, or -1.",
        "solve": _solve_rotting_oranges,
        "sample_inputs": ["3 3\n2 1 1\n1 1 0\n0 1 1", "3 3\n2 1 1\n0 1 1\n1 0 1"],
        "hidden_inputs": [
            "1 1\n0",               # nothing to rot
            "1 1\n2",               # already rotten
            "1 1\n1",               # never rots, -1
            "1 2\n2 1",             # one minute
            "1 2\n1 2",             # the other direction
            "1 3\n2 1 1",           # two minutes
            "2 2\n2 1\n1 1",
            "2 2\n0 2\n1 0",
            "3 3\n2 2 2\n2 2 2\n2 2 2",     # all rotten already
            "3 3\n1 1 1\n1 1 1\n1 1 1",     # none rotten, -1
        ],
    },
{
        "title": "Keys and Rooms",
        "topic": "graphs", "difficulty": "medium",
        "description": "Every room but the first is locked. Each room contains keys to other rooms. Starting in room zero, decide whether every room can be entered.",
        "example_input": "4\n1 1\n1 2\n1 3\n0",
        "constraints": "Input format: line 1 is the number of rooms, followed by that many lines, each holding a count then that many room numbers. Output format: \"true\" or \"false\".",
        "solve": _solve_keys_and_rooms,
        "sample_inputs": ["4\n1 1\n1 2\n1 3\n0", "4\n1 1\n1 2\n1 3\n1 0"],
        "hidden_inputs": [
            "1\n0",                 # only one room, already in it
            "2\n1 1\n0",            # a key to the second room
            "2\n0\n0",              # no keys at all
            "3\n2 1 2\n0\n0",       # both keys in the first room
            "3\n1 1\n0\n0",         # the third is unreachable
            "3\n1 2\n0\n1 1",       # reachable the long way round
            "4\n1 3\n1 3\n1 3\n0",  # rooms 1 and 2 unreachable
            "4\n2 1 2\n1 3\n0\n0",
            "5\n1 1\n1 2\n1 3\n1 4\n0",     # a chain through every room
            "3\n0\n1 2\n1 1",
        ],
    },
{
        "title": "Redundant Connection",
        "topic": "graphs", "difficulty": "medium",
        "description": "A tree has had one extra edge added, creating exactly one cycle. Return the edge that can be removed to restore the tree, choosing the one that appears last in the input if several would work.",
        "example_input": "3\n1 2\n1 3\n2 3",
        "constraints": "Input format: line 1 is the number of edges, followed by that many lines each \"a b\". Output format: the edge as \"a b\".",
        "solve": _solve_redundant_connection,
        "sample_inputs": ["3\n1 2\n1 3\n2 3", "5\n1 2\n2 3\n3 4\n1 4\n1 5"],
        "hidden_inputs": [
            "1\n1 1",               # a self loop
            "3\n1 2\n2 3\n1 3",     # a triangle
            "3\n1 2\n1 3\n3 2",     # the same triangle, edge reversed
            "4\n1 2\n2 3\n3 4\n1 4",
            "4\n1 2\n1 3\n1 4\n2 3",    # a star plus one chord
            "5\n1 2\n2 3\n3 4\n4 5\n1 5",   # a long cycle
            "5\n1 2\n1 3\n2 4\n3 5\n4 5",
            "6\n1 2\n1 3\n2 4\n4 5\n5 6\n2 6",
            "4\n2 1\n3 1\n4 2\n1 4",
            "5\n1 2\n2 3\n1 3\n4 5\n1 4",   # the cycle comes before a tree edge
        ],
    },
{
        "title": "Critical Connections in a Network",
        "topic": "graphs", "difficulty": "hard",
        "description": "An edge is critical when removing it would leave some pair of nodes unable to reach one another. Report every critical edge, each with its smaller endpoint first, ordered by that endpoint and then the other.",
        "example_input": "4 4\n0 1\n1 2\n2 0\n1 3",
        "constraints": "Input format: line 1 is \"n m\", followed by m lines each \"a b\" describing an undirected edge. Output format: one edge per line as \"a b\" (empty if none).",
        "solve": _solve_critical_connections,
        "sample_inputs": ["4 4\n0 1\n1 2\n2 0\n1 3", "2 1\n0 1"],
        "hidden_inputs": [
            "1 0",                  # a lone node, no edges
            "2 0",                  # two nodes, disconnected
            "3 2\n0 1\n1 2",        # a path, every edge critical
            "3 3\n0 1\n1 2\n2 0",   # a triangle, none critical
            "4 3\n0 1\n1 2\n2 3",
            "4 4\n0 1\n1 2\n2 3\n3 0",      # a square, none critical
            "5 4\n0 1\n0 2\n0 3\n0 4",      # a star, every edge critical
            "5 5\n0 1\n1 2\n2 0\n2 3\n3 4",
            "6 6\n0 1\n1 2\n2 0\n3 4\n4 5\n5 3",   # two separate triangles
            "6 7\n0 1\n1 2\n2 0\n1 3\n3 4\n4 5\n5 3",
        ],
    },
{
        "title": "Cheapest Flights Within K Stops",
        "topic": "graphs", "difficulty": "hard",
        "description": "Find the cheapest route from one city to another using at most k intermediate stops, and return its price, or -1 if no such route exists.",
        "example_input": "4 4 0 3 1\n0 1 100\n1 2 100\n2 3 100\n0 2 500",
        "constraints": "Input format: line 1 is \"n m src dst k\", followed by m lines each \"from to price\". Output format: a single integer, or -1.",
        "solve": _solve_cheapest_flights_k_stops,
        "sample_inputs": ["4 4 0 3 1\n0 1 100\n1 2 100\n2 3 100\n0 2 500", "3 3 0 2 1\n0 1 100\n1 2 100\n0 2 500"],
        "hidden_inputs": [
            "1 0 0 0 0",            # already there, price zero
            "2 0 0 1 0",            # no route at all
            "2 1 0 1 0\n0 1 5",     # a direct flight, no stops needed
            "2 1 0 1 5\n0 1 5",     # more stops allowed than needed
            "3 2 0 2 0\n0 1 1\n1 2 1",      # one stop needed but none allowed
            "3 2 0 2 1\n0 1 1\n1 2 1",      # the same route, now allowed
            "3 3 0 2 0\n0 1 100\n1 2 100\n0 2 500",     # the dear direct flight
            "4 4 0 3 2\n0 1 1\n1 2 1\n2 3 1\n0 3 10",
            "5 6 0 4 2\n0 1 1\n1 2 1\n2 3 1\n3 4 1\n0 2 5\n2 4 5",
            "3 2 2 0 5\n0 1 1\n1 2 1",      # the edges point the wrong way
        ],
    },
{
        "title": "Reconstruct Itinerary",
        "topic": "graphs", "difficulty": "hard",
        "description": "Given a set of one-way tickets, arrange a journey that starts at JFK and uses every ticket exactly once. When several journeys are possible, return the one that comes first alphabetically.",
        "example_input": "4\nMUC LHR\nJFK MUC\nSFO SJC\nLHR SFO",
        "constraints": "Input format: line 1 is the number of tickets, followed by that many lines each \"from to\" using three-letter codes. A valid journey is guaranteed. Output format: the airports in order, space-separated.",
        "solve": _solve_reconstruct_itinerary,
        "sample_inputs": ["4\nMUC LHR\nJFK MUC\nSFO SJC\nLHR SFO", "5\nJFK SFO\nJFK ATL\nSFO ATL\nATL JFK\nATL SFO"],
        "hidden_inputs": [
            "1\nJFK ATL",           # a single ticket
            "2\nJFK ATL\nATL JFK",  # returning home
            "2\nJFK ATL\nATL SFO",  # a simple chain
            "3\nJFK SFO\nJFK ATL\nATL JFK",   # two choices, alphabetical wins
            "3\nJFK ATL\nATL JFK\nJFK SFO",
            "3\nJFK AAA\nJFK BBB\nAAA JFK",
            "4\nJFK KUL\nJFK NRT\nNRT JFK\nKUL AAA",    # the greedy trap
            "4\nJFK AAA\nAAA JFK\nJFK BBB\nBBB JFK",
            "5\nJFK ATL\nATL JFK\nJFK SFO\nSFO ATL\nATL SFO",
            "3\nJFK AAA\nAAA BBB\nBBB CCC",
        ],
    },
]
