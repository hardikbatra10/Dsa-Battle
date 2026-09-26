"""Trees problems."""

from .helpers import _build_tree, _serialize_tree, _Node


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

def _levels(root):
    """Node values grouped by depth, left to right."""
    out = []
    level = [root] if root else []
    while level:
        out.append([n.val for n in level])
        level = [c for n in level for c in (n.left, n.right) if c]
    return out


def _solve_reverse_odd_levels(lines):
    root = _build_tree(lines[0].split())
    if not root:
        return "null"
    level = [root]
    depth = 0
    while level:
        if depth % 2 == 1:
            vals = [n.val for n in level][::-1]
            for node, v in zip(level, vals):
                node.val = v
        level = [c for n in level for c in (n.left, n.right) if c]
        depth += 1
    return _serialize_tree(root)


def _solve_balanced_tree(lines):
    root = _build_tree(lines[0].split())

    def height(node):
        if not node:
            return 0
        l = height(node.left)
        if l < 0:
            return -1
        r = height(node.right)
        if r < 0 or abs(l - r) > 1:
            return -1
        return 1 + max(l, r)

    return "true" if height(root) >= 0 else "false"


def _solve_right_side_view(lines):
    root = _build_tree(lines[0].split())
    return " ".join(str(lv[-1]) for lv in _levels(root))


def _solve_next_right_pointers(lines):
    root = _build_tree(lines[0].split())
    return "\n".join(" ".join(map(str, lv)) for lv in _levels(root))


def _solve_count_good_nodes(lines):
    root = _build_tree(lines[0].split())
    count = [0]

    def walk(node, best):
        if not node:
            return
        if node.val >= best:
            count[0] += 1
            best = node.val
        walk(node.left, best)
        walk(node.right, best)

    walk(root, float("-inf"))
    return str(count[0])


def _solve_delete_leaves(lines):
    root = _build_tree(lines[0].split())
    target = int(lines[1])

    def prune(node):
        if not node:
            return None
        node.left = prune(node.left)
        node.right = prune(node.right)
        if not node.left and not node.right and node.val == target:
            return None
        return node

    return _serialize_tree(prune(root))


def _solve_bottom_view(lines):
    root = _build_tree(lines[0].split())
    if not root:
        return ""
    seen = {}
    queue = [(root, 0)]
    while queue:
        node, hd = queue.pop(0)
        seen[hd] = node.val
        if node.left:
            queue.append((node.left, hd - 1))
        if node.right:
            queue.append((node.right, hd + 1))
    return " ".join(str(seen[h]) for h in sorted(seen))


def _solve_vertical_order(lines):
    root = _build_tree(lines[0].split())
    if not root:
        return ""
    items = []

    def walk(node, row, col):
        if not node:
            return
        items.append((col, row, node.val))
        walk(node.left, row + 1, col - 1)
        walk(node.right, row + 1, col + 1)

    walk(root, 0, 0)
    items.sort()
    out = []
    current = None
    for col, row, val in items:
        if col != current:
            out.append([])
            current = col
        out[-1].append(str(val))
    return "\n".join(" ".join(g) for g in out)


def _solve_nodes_distance_k(lines):
    root = _build_tree(lines[0].split())
    target = int(lines[1])
    k = int(lines[2])
    parent = {}

    def link(node, par):
        if not node:
            return
        parent[node.val] = par
        link(node.left, node)
        link(node.right, node)

    link(root, None)

    start = None
    stack = [root] if root else []
    while stack:
        n = stack.pop()
        if n.val == target:
            start = n
        for c in (n.left, n.right):
            if c:
                stack.append(c)
    if start is None:
        return ""

    seen = {start.val}
    frontier = [start]
    for _ in range(k):
        nxt = []
        for node in frontier:
            for nb in (node.left, node.right, parent[node.val]):
                if nb and nb.val not in seen:
                    seen.add(nb.val)
                    nxt.append(nb)
        frontier = nxt
    return " ".join(str(v) for v in sorted(n.val for n in frontier))


def _solve_time_to_infect(lines):
    root = _build_tree(lines[0].split())
    start = int(lines[1])
    adj = {}
    stack = [root] if root else []
    while stack:
        n = stack.pop()
        adj.setdefault(n.val, [])
        for c in (n.left, n.right):
            if c:
                adj.setdefault(c.val, []).append(n.val)
                adj[n.val].append(c.val)
                stack.append(c)
    seen = {start}
    frontier = [start]
    minutes = 0
    while True:
        nxt = [nb for v in frontier for nb in adj[v] if nb not in seen]
        nxt = list(dict.fromkeys(nxt))
        for v in nxt:
            seen.add(v)
        if not nxt:
            return str(minutes)
        frontier = nxt
        minutes += 1


def _solve_boundary(lines):
    root = _build_tree(lines[0].split())
    if not root:
        return ""
    if not root.left and not root.right:
        return str(root.val)

    left_bound = []
    node = root.left
    while node:
        if node.left or node.right:
            left_bound.append(node.val)
        node = node.left if node.left else node.right

    leaves = []

    def collect(n):
        if not n:
            return
        if not n.left and not n.right:
            leaves.append(n.val)
            return
        collect(n.left)
        collect(n.right)

    collect(root)

    right_bound = []
    node = root.right
    while node:
        if node.left or node.right:
            right_bound.append(node.val)
        node = node.right if node.right else node.left

    return " ".join(map(str, [root.val] + left_bound + leaves + right_bound[::-1]))


def _solve_house_robber_iii(lines):
    root = _build_tree(lines[0].split())

    def rob(node):
        if not node:
            return (0, 0)          # (with node, without node)
        l = rob(node.left)
        r = rob(node.right)
        take = node.val + l[1] + r[1]
        skip = max(l) + max(r)
        return (take, skip)

    return str(max(rob(root)))


def _solve_path_sum_iii(lines):
    root = _build_tree(lines[0].split())
    target = int(lines[1])
    from collections import defaultdict
    prefix = defaultdict(int)
    prefix[0] = 1
    count = [0]

    def walk(node, running):
        if not node:
            return
        running += node.val
        count[0] += prefix[running - target]
        prefix[running] += 1
        walk(node.left, running)
        walk(node.right, running)
        prefix[running] -= 1

    walk(root, 0)
    return str(count[0])


def _solve_average_of_levels(lines):
    root = _build_tree(lines[0].split())
    out = []
    for lv in _levels(root):
        out.append("%.5f" % (sum(lv) / len(lv)))
    return " ".join(out)


def _solve_nodes_equal_subtree_average(lines):
    root = _build_tree(lines[0].split())
    count = [0]

    def walk(node):
        if not node:
            return (0, 0)
        ls, lc = walk(node.left)
        rs, rc = walk(node.right)
        total = ls + rs + node.val
        n = lc + rc + 1
        if total // n == node.val:
            count[0] += 1
        return (total, n)

    walk(root)
    return str(count[0])


def _solve_check_completeness(lines):
    root = _build_tree(lines[0].split())
    if not root:
        return "true"
    queue = [root]
    seen_gap = False
    while queue:
        node = queue.pop(0)
        if node is None:
            seen_gap = True
            continue
        if seen_gap:
            return "false"
        queue.append(node.left)
        queue.append(node.right)
    return "true"


def _solve_delete_nodes_forest(lines):
    root = _build_tree(lines[0].split())
    to_delete = set(map(int, lines[1].split())) if len(lines) > 1 and lines[1].strip() else set()
    roots = []

    def walk(node, is_root):
        if not node:
            return None
        deleted = node.val in to_delete
        if is_root and not deleted:
            roots.append(node)
        node.left = walk(node.left, deleted)
        node.right = walk(node.right, deleted)
        return None if deleted else node

    walk(root, True)
    roots.sort(key=lambda n: n.val)
    return "\n".join(_serialize_tree(r) for r in roots)


def _solve_tree_pruning(lines):
    root = _build_tree(lines[0].split())

    def prune(node):
        if not node:
            return None
        node.left = prune(node.left)
        node.right = prune(node.right)
        if node.val == 0 and not node.left and not node.right:
            return None
        return node

    return _serialize_tree(prune(root))


def _solve_count_complete_nodes(lines):
    root = _build_tree(lines[0].split())

    def depth_left(node):
        d = 0
        while node:
            d += 1
            node = node.left
        return d

    def depth_right(node):
        d = 0
        while node:
            d += 1
            node = node.right
        return d

    def count(node):
        if not node:
            return 0
        dl = depth_left(node)
        dr = depth_right(node)
        if dl == dr:
            return (1 << dl) - 1
        return 1 + count(node.left) + count(node.right)

    return str(count(root))


def _solve_max_ancestor_diff(lines):
    root = _build_tree(lines[0].split())
    if not root:
        return "0"
    best = [0]

    def walk(node, lo, hi):
        if not node:
            return
        best[0] = max(best[0], abs(node.val - lo), abs(node.val - hi))
        lo = min(lo, node.val)
        hi = max(hi, node.val)
        walk(node.left, lo, hi)
        walk(node.right, lo, hi)

    walk(root, root.val, root.val)
    return str(best[0])


def _solve_max_product_split(lines):
    root = _build_tree(lines[0].split())
    sums = []

    def total(node):
        if not node:
            return 0
        s = node.val + total(node.left) + total(node.right)
        sums.append(s)
        return s

    whole = total(root)
    best = max((s * (whole - s) for s in sums[:-1]), default=0)
    return str(best % (10 ** 9 + 7))

def _solve_invert_tree(lines):
    root = _build_tree(lines[0].split())

    def flip(node):
        if not node:
            return None
        node.left, node.right = flip(node.right), flip(node.left)
        return node

    return _serialize_tree(flip(root))


def _solve_same_tree(lines):
    a = _build_tree(lines[0].split())
    b = _build_tree(lines[1].split())

    def same(x, y):
        if not x and not y:
            return True
        if not x or not y or x.val != y.val:
            return False
        return same(x.left, y.left) and same(x.right, y.right)

    return "true" if same(a, b) else "false"


def _solve_symmetric_tree(lines):
    root = _build_tree(lines[0].split())

    def mirror(x, y):
        if not x and not y:
            return True
        if not x or not y or x.val != y.val:
            return False
        return mirror(x.left, y.right) and mirror(x.right, y.left)

    return "true" if not root or mirror(root.left, root.right) else "false"


def _solve_min_depth(lines):
    root = _build_tree(lines[0].split())
    if not root:
        return "0"
    level = [root]
    depth = 1
    while level:
        nxt = []
        for n in level:
            if not n.left and not n.right:
                return str(depth)
            for c in (n.left, n.right):
                if c:
                    nxt.append(c)
        level = nxt
        depth += 1
    return str(depth)


def _solve_sum_left_leaves(lines):
    root = _build_tree(lines[0].split())
    total = [0]

    def walk(node, is_left):
        if not node:
            return
        if not node.left and not node.right:
            if is_left:
                total[0] += node.val
            return
        walk(node.left, True)
        walk(node.right, False)

    walk(root, False)
    return str(total[0])


def _solve_range_sum_bst(lines):
    root = _build_tree(lines[0].split())
    low, high = map(int, lines[1].split())
    total = [0]

    def walk(node):
        if not node:
            return
        if low <= node.val <= high:
            total[0] += node.val
        if node.val > low:
            walk(node.left)
        if node.val < high:
            walk(node.right)

    walk(root)
    return str(total[0])


def _solve_merge_two_trees(lines):
    a = _build_tree(lines[0].split())
    b = _build_tree(lines[1].split())

    def merge(x, y):
        if not x:
            return y
        if not y:
            return x
        x.val += y.val
        x.left = merge(x.left, y.left)
        x.right = merge(x.right, y.right)
        return x

    return _serialize_tree(merge(a, b))


def _solve_max_path_sum(lines):
    root = _build_tree(lines[0].split())
    best = [float("-inf")]

    def gain(node):
        if not node:
            return 0
        left = max(0, gain(node.left))
        right = max(0, gain(node.right))
        best[0] = max(best[0], node.val + left + right)
        return node.val + max(left, right)

    gain(root)
    return str(best[0]) if root else "0"


def _solve_build_from_preorder_inorder(lines):
    preorder = lines[0].split()
    inorder = lines[1].split()
    pos = {v: i for i, v in enumerate(inorder)}
    idx = [0]

    def build(lo, hi):
        if lo > hi:
            return None
        val = preorder[idx[0]]
        idx[0] += 1
        node = _Node(int(val))
        mid = pos[val]
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    if not preorder or preorder == [""]:
        return "null"
    return _serialize_tree(build(0, len(inorder) - 1))


def _solve_recover_bst(lines):
    root = _build_tree(lines[0].split())
    order = []

    def walk(node):
        if not node:
            return
        walk(node.left)
        order.append(node)
        walk(node.right)

    walk(root)
    first = second = None
    for i in range(len(order) - 1):
        if order[i].val > order[i + 1].val:
            if first is None:
                first = order[i]
            second = order[i + 1]
    if first and second:
        first.val, second.val = second.val, first.val
    return _serialize_tree(root)


def _solve_lowest_common_ancestor(lines):
    root = _build_tree(lines[0].split())
    p, q = map(int, lines[1].split())

    def walk(node):
        if not node or node.val == p or node.val == q:
            return node
        left = walk(node.left)
        right = walk(node.right)
        if left and right:
            return node
        return left or right

    return str(walk(root).val)


PROBLEMS = [
{
        "title": "Binary Tree Inorder Traversal",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Given the root of a binary tree, return the inorder traversal of its nodes' values.",
        "example_input": "1 null 2 3",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: space-separated inorder values.",
        "solve": _solve_binary_tree_inorder,
        "sample_inputs": ["1 null 2 3", "2 1 3"],
        "hidden_inputs": [
            "null",               # empty tree
            "1",                  # single node
            "1 2 3",
            "3 2 null 1",         # left-skewed
            "1 null 2 null 3",    # right-skewed
            "1 2 null 3 null 4",  # deep left chain
            "-1 -2 -3",           # negative values
            "4 2 6 1 3 5 7",      # complete tree
            "5 3 8 1 4 7 9",
            "10 5 15 2 7 12 20",
        ],
    },
{
        "title": "Maximum Depth of Binary Tree",
        "topic": "trees",
        "difficulty": "easy",
        "description": "Given the root of a binary tree, return its maximum depth (the number of nodes along the longest path from the root to a leaf).",
        "example_input": "3 9 20 null null 15 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_max_depth,
        "sample_inputs": ["3 9 20 null null 15 7", "1 2 3 4"],
        "hidden_inputs": [
            "null",               # empty tree -> 0
            "1",
            "1 2",
            "1 2 3",
            "1 null 2 null 3",    # right-skewed
            "1 2 null 3 null 4",  # left-skewed
            "1 2 3 4 5 6 7",
            "5 4 8 11 null 13 4 7 2",
        ],
    },
{
        "title": "Diameter of Binary Tree",
        "topic": "trees",
        "difficulty": "hard",
        "description": "Given the root of a binary tree, return the length (in edges) of the diameter of the tree: the longest path between any two nodes, which may or may not pass through the root.",
        "example_input": "1 2 3 4 5",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_diameter,
        "sample_inputs": ["1 2 3 4 5", "1 2 3 null null 4 5"],
        "hidden_inputs": [
            "null",                     # empty tree -> 0
            "1",                        # single node -> 0 edges
            "1 2",
            "1 2 3",                    # path through the root
            "1 2 null 3 null 4",        # skewed, path does not fork
            "1 2 3 4 5 null null 6 7",  # longest path avoids the root's right side
            "4 -7 -3 null null -9 -3 9 -7 null null 8",
            "1 null 2 null 3 null 4",   # right-skewed, every edge on one path
        ],
    },
{
        "title": "Reverse Odd Levels of Binary Tree",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Given a perfect binary tree, reverse the node values at every odd-numbered level, counting the root as level 0. Return the resulting tree.",
        "example_input": "2 3 5 8 13 21 34",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: the resulting tree in the same encoding.",
        "solve": _solve_reverse_odd_levels,
        "sample_inputs": ["2 3 5 8 13 21 34", "7 13 11"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1",                    # root only, no odd level exists
            "1 2 3",                # a single odd level
            "1 2 2",                # symmetric values, reversal is invisible
            "5 5 5 5 5 5 5",
            "1 2 3 4 5 6 7",
            "0 1 2 3 4 5 6",
            "-1 -2 -3",             # negatives
            "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
            "9 1 8 2 7 3 6",
        ],
    },
{
        "title": "Balanced Binary Tree",
        "topic": "trees",
        "difficulty": "easy",
        "description": "A binary tree is height-balanced when, for every node, the depths of its two subtrees differ by at most one. Decide whether the given tree is height-balanced.",
        "example_input": "3 9 20 null null 15 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: \"true\" or \"false\".",
        "solve": _solve_balanced_tree,
        "sample_inputs": ["3 9 20 null null 15 7", "1 2 2 3 3 null null 4 4"],
        "hidden_inputs": [
            "null",                 # empty tree is balanced
            "1",                    # single node
            "1 2",                  # difference of exactly one
            "1 2 null 3",           # difference of two, unbalanced
            "1 null 2 null 3",      # right-skewed
            "1 2 3",
            "1 2 3 4 5 6 7",        # perfect tree
            "1 2 3 4 null null null 5",
            "1 2 2 3 null null 3 4 null null 4",
            "1 null 2 3",           # imbalance only on the right
        ],
    },
{
        "title": "Binary Tree Right Side View",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Imagine standing to the right of a binary tree. Return the values of the nodes you can see, ordered from the top down.",
        "example_input": "1 2 3 null 5 null 4",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: the visible values, space-separated top to bottom.",
        "solve": _solve_right_side_view,
        "sample_inputs": ["1 2 3 null 5 null 4", "1 null 3"],
        "hidden_inputs": [
            "null",                 # empty tree, empty output
            "1",                    # single node
            "1 2",                  # only a left child is still visible
            "1 null 2",
            "1 2 3",
            "1 2 null 3",           # deep left chain seen from the right
            "1 null 2 null 3",
            "1 2 3 4 5 6 7",
            "1 2 3 null null null 4",
            "-1 -2 -3",             # negatives
        ],
    },
{
        "title": "Populating Next Right Pointers in Each Node",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Link every node to the node immediately to its right on the same level, then report the resulting chains. Print one line per level, listing that level's nodes from left to right.",
        "example_input": "1 2 3 4 5 6 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: one line per level, values space-separated left to right.",
        "solve": _solve_next_right_pointers,
        "sample_inputs": ["1 2 3 4 5 6 7", "1 2 3"],
        "hidden_inputs": [
            "null",                 # empty tree, no output
            "1",                    # single level
            "1 2",
            "1 null 2",
            "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
            "1 2 3 null 5 null 7",  # gaps within a level
            "1 null 2 null 3",      # one node per level
            "0 0 0 0 0 0 0",
            "-1 -2 -3 -4 -5 -6 -7",
            "5 4 6 3 7 2 8",
        ],
    },
{
        "title": "Count Good Nodes in Binary Tree",
        "topic": "trees",
        "difficulty": "medium",
        "description": "A node is good when no node on the path from the root down to it holds a larger value. Count the good nodes in the tree.",
        "example_input": "3 1 4 3 null 1 5",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_count_good_nodes,
        "sample_inputs": ["3 1 4 3 null 1 5", "3 3 null 4 2"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1",                    # the root is always good
            "1 2",                  # a larger child is good
            "2 1",                  # a smaller child is not
            "2 2",                  # equal values still count as good
            "1 2 3 4 5 6 7",        # every node is good
            "9 8 7 6 5 4 3",        # only the root is good
            "5 5 5 5 5",
            "-1 -2 -3",             # negatives
            "3 1 4 3 null 1 5 null null null null null null 6",
        ],
    },
{
        "title": "Delete Leaves With a Given Value",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Repeatedly delete every leaf whose value equals the target, including leaves that only become leaves after earlier deletions. Return the resulting tree.",
        "example_input": "1 2 3 2 null 2 4\n2",
        "constraints": "Input format: line 1 is the tree in level-order encoding, line 2 is the target value. Output format: the resulting tree in the same encoding.",
        "solve": _solve_delete_leaves,
        "sample_inputs": ["1 2 3 2 null 2 4\n2", "1 3 3 3 2\n3"],
        "hidden_inputs": [
            "null\n1",              # empty tree
            "1\n1",                 # the root itself is a matching leaf
            "1\n2",                 # nothing matches
            "1 2\n2",
            "2 2 2\n2",             # the whole tree collapses
            "1 2 2\n2",
            "1 2 null 2\n2",        # cascading deletion up a chain
            "1 1 1\n1",
            "1 2 3 2 null 2 4\n4",
            "5 5 5 5 5 5 5\n5",     # every node deleted
        ],
    },
{
        "title": "Bottom View of Binary Tree",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Assign the root horizontal distance 0, a left child one less than its parent and a right child one more. For each horizontal distance, the bottom view shows the last node encountered in level order. Report the view from leftmost distance to rightmost.",
        "example_input": "20 8 22 5 3 null 25",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: the visible values, space-separated left to right.",
        "solve": _solve_bottom_view,
        "sample_inputs": ["20 8 22 5 3 null 25", "1 2 3"],
        "hidden_inputs": [
            "null",                 # empty tree, empty output
            "1",                    # single node
            "1 2",
            "1 null 2",
            "1 2 3 4 5 6 7",
            "1 2 null 3 null 4",    # left chain spreads leftwards
            "1 null 2 null 3",
            "20 8 22 5 3 4 25",     # two nodes share a horizontal distance
            "1 2 3 null 4 5",       # a deeper node overwrites a shallower one
            "-1 -2 -3",
        ],
    },
{
        "title": "Vertical Order Traversal of a Binary Tree",
        "topic": "trees",
        "difficulty": "hard",
        "description": "Assign the root column 0 and row 0, a left child column-1 row+1, a right child column+1 row+1. Report the nodes column by column from left to right; within a column order by row, and nodes sharing a row and column are ordered by value.",
        "example_input": "3 9 20 null null 15 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: one line per column, values space-separated.",
        "solve": _solve_vertical_order,
        "sample_inputs": ["3 9 20 null null 15 7", "1 2 3 4 5 6 7"],
        "hidden_inputs": [
            "null",                 # empty tree, no output
            "1",                    # single column
            "1 2",
            "1 null 2",
            "1 2 3",
            "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
            "3 1 4 0 2 2",          # a row/column tie broken by value
            "1 2 3 null null 4 5",  # two nodes collide in the middle column
            "0 2 1 3 null null null 4 5 null 7 6",
            "-1 -2 -3",
        ],
    },
{
        "title": "All Nodes Distance K in Binary Tree",
        "topic": "trees",
        "difficulty": "hard",
        "description": "Given a tree with distinct values, a target node's value and an integer k, return the values of every node exactly k edges away from the target, in increasing order.",
        "example_input": "3 5 1 6 2 0 8 null null 7 4\n5\n2",
        "constraints": "Input format: line 1 is the tree in level-order encoding (values are distinct), line 2 is the target value, line 3 is k. Output format: the values, space-separated ascending (empty if none).",
        "solve": _solve_nodes_distance_k,
        "sample_inputs": ["3 5 1 6 2 0 8 null null 7 4\n5\n2", "1\n1\n3"],
        "hidden_inputs": [
            "1\n1\n0",              # distance zero is the target itself
            "1 2\n1\n1",
            "1 2\n2\n1",            # walking upward to the parent
            "1 2 3\n1\n1",
            "1 2 3\n2\n2",          # across the root to the sibling
            "1 2 3\n1\n5",          # k larger than the tree, empty output
            "1 2 3 4 5 6 7\n4\n3",
            "1 2 3 4 5 6 7\n1\n2",
            "0 1 null 2 null 3\n3\n3",   # a skewed chain
            "3 5 1 6 2 0 8 null null 7 4\n5\n1",
        ],
    },
{
        "title": "Amount of Time for Binary Tree to Be Infected",
        "topic": "trees",
        "difficulty": "medium",
        "description": "An infection starts at the node holding the given value. Each minute it spreads from every infected node to its parent and its children. Return how many minutes pass before the whole tree is infected.",
        "example_input": "1 5 3 null 4 10 6 9 2\n3",
        "constraints": "Input format: line 1 is the tree in level-order encoding (values are distinct), line 2 is the starting value. Output format: a single integer.",
        "solve": _solve_time_to_infect,
        "sample_inputs": ["1 5 3 null 4 10 6 9 2\n3", "1\n1"],
        "hidden_inputs": [
            "1 2\n1",               # spreads down one edge
            "1 2\n2",               # spreads up one edge
            "1 2 3\n1",
            "1 2 3\n2",             # must travel through the root
            "1 2 3 4 5 6 7\n1",
            "1 2 3 4 5 6 7\n4",     # a corner leaf is the slowest start
            "1 null 2 null 3\n1",   # a right-skewed chain
            "1 null 2 null 3\n3",
            "1 2 null 3 null 4\n1",
            "5 1 9 null 2 8 null null 3\n5",
        ],
    },
{
        "title": "Boundary of Binary Tree",
        "topic": "trees",
        "difficulty": "hard",
        "description": "Report the boundary of the tree anticlockwise: the root, then the left boundary from the top down excluding leaves, then every leaf from left to right, then the right boundary from the bottom up excluding leaves. No node appears twice.",
        "example_input": "1 null 2 3 4",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: the boundary values, space-separated.",
        "solve": _solve_boundary,
        "sample_inputs": ["1 null 2 3 4", "1 2 3 4 5 6 7"],
        "hidden_inputs": [
            "null",                 # empty tree, empty output
            "1",                    # the root alone is the whole boundary
            "1 2",                  # root plus one leaf
            "1 null 2",
            "1 2 3",
            "1 2 null 3",           # a left chain ending in a leaf
            "1 null 2 null 3",      # a right chain
            "1 2 3 4 5 6 7 8 9",
            "1 2 null 3 4",         # left boundary follows the right child
            "1 2 3 null 4 5 null",
        ],
    },
{
        "title": "House Robber III",
        "topic": "trees",
        "difficulty": "hard",
        "description": "Each node holds an amount of money, but two directly connected nodes cannot both be taken. Return the largest total that can be taken.",
        "example_input": "3 2 3 null 3 null 1",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_house_robber_iii,
        "sample_inputs": ["3 2 3 null 3 null 1", "3 4 5 1 3 null 1"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1",                    # only the root
            "1 2",                  # the child alone beats the root
            "2 1",                  # the root alone wins
            "0 0 0",                # zeros
            "1 1 1",
            "4 1 null 2 null 3",    # skipping a level down a chain
            "1 2 3 4 5 6 7",
            "10 1 1 10 10 10 10",   # taking the grandchildren beats the root
            "5 null 5 null 5",
        ],
    },
{
        "title": "Path Sum III",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Count the downward paths whose values add up to the target. A path must run from a node to one of its descendants, but need not start at the root or end at a leaf.",
        "example_input": "10 5 -3 3 2 null 11 3 -2 null 1\n8",
        "constraints": "Input format: line 1 is the tree in level-order encoding, line 2 is the target sum. Output format: a single integer.",
        "solve": _solve_path_sum_iii,
        "sample_inputs": ["10 5 -3 3 2 null 11 3 -2 null 1\n8", "5 4 8 11 null 13 4 7 2 null null 5 1\n22"],
        "hidden_inputs": [
            "null\n0",              # empty tree
            "1\n1",                 # a single matching node
            "1\n2",                 # no match
            "0\n0",                 # a zero-valued node against a zero target
            "1 2 3\n3",             # two separate matching paths
            "0 0 0\n0",             # zeros create overlapping paths
            "1 -1\n0",              # negatives cancel
            "1 2 null 3\n6",        # the path runs down a chain
            "-1 -2 -3\n-3",
            "10 5 -3 3 2 null 11 3 -2 null 1\n3",
        ],
    },
{
        "title": "Average of Levels in Binary Tree",
        "topic": "trees",
        "difficulty": "easy",
        "description": "Return the average value of the nodes on each level of the tree, from the top down.",
        "example_input": "3 9 20 null null 15 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: one average per level, space-separated, each printed with exactly five decimal places.",
        "solve": _solve_average_of_levels,
        "sample_inputs": ["3 9 20 null null 15 7", "3 9 20 15 7"],
        "hidden_inputs": [
            "null",                 # empty tree, empty output
            "1",                    # single node
            "1 2",
            "1 2 3",                # an average that is not a whole number
            "2 1 3",                # an average that is exactly whole
            "0 0 0",
            "-1 -2 -3",             # negative averages
            "1 2 3 4 5 6 7",
            "1 null 2 null 3",      # one node per level
            "5 2 8 1 3 7 9",
        ],
    },
{
        "title": "Count Nodes Equal to Average of Subtree",
        "topic": "trees",
        "difficulty": "medium",
        "description": "For each node, take the average of every value in its subtree, rounded down to the nearest integer. Count the nodes whose own value equals that average.",
        "example_input": "4 8 5 0 1 null 6",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_nodes_equal_subtree_average,
        "sample_inputs": ["4 8 5 0 1 null 6", "1"],
        "hidden_inputs": [
            "null",                 # empty tree
            "0",                    # a single zero
            "5",                    # every leaf always qualifies
            "1 2",                  # rounding down decides the root
            "2 1",
            "0 0 0",                # all zeros qualify
            "1 1 1",
            "1 2 3",                # the root averages to itself
            "7 3 9 1 5 8 10",       # a balanced tree where only leaves qualify
            "10 3 null 2 null 1",   # a skewed chain
        ],
    },
{
        "title": "Check Completeness of a Binary Tree",
        "topic": "trees",
        "difficulty": "medium",
        "description": "A binary tree is complete when every level except possibly the last is entirely filled, and the last level's nodes are packed as far left as possible. Decide whether the given tree is complete.",
        "example_input": "1 2 3 4 5 6",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: \"true\" or \"false\".",
        "solve": _solve_check_completeness,
        "sample_inputs": ["1 2 3 4 5 6", "1 2 3 4 5 null 7"],
        "hidden_inputs": [
            "null",                 # empty tree counts as complete
            "1",                    # single node
            "1 2",                  # a lone left child is complete
            "1 null 2",             # a lone right child is not
            "1 2 3",
            "1 2 3 4",
            "1 2 3 null 4",         # a gap before a filled slot
            "1 2 3 4 5 6 7",        # perfect tree
            "1 2 3 4 null 6 7",
            "1 2 null 3",           # a gap followed by a deeper node
        ],
    },
{
        "title": "Delete Nodes And Return Forest",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Delete every node whose value appears in the delete list. The remaining nodes form a forest. Report each remaining tree, one per line, ordered by the value at its root.",
        "example_input": "1 2 3 4 5 6 7\n3 5",
        "constraints": "Input format: line 1 is the tree in level-order encoding (values are distinct), line 2 is the space-separated values to delete. Output format: one tree per line in the same encoding, ordered by root value.",
        "solve": _solve_delete_nodes_forest,
        "sample_inputs": ["1 2 3 4 5 6 7\n3 5", "1 2 3\n2"],
        "hidden_inputs": [
            "1\n1",                 # the whole tree disappears
            "1\n2",                 # nothing is deleted
            "1 2 3\n1",             # deleting the root splits the tree in two
            "1 2 3\n1 2 3",         # everything deleted, empty output
            "1 2 3\n3",
            "1 2 null 3\n2",        # a chain broken in the middle
            "1 2 3 4 5 6 7\n1",
            "1 2 3 4 5 6 7\n2 6",
            "1 2 3 4 5 6 7\n4 5 6 7",    # only leaves removed
            "5 3 8 1 4 7 9\n3 8",
        ],
    },
{
        "title": "Binary Tree Pruning",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Every node holds 0 or 1. Remove every subtree that contains no 1 at all, and return what remains.",
        "example_input": "1 null 0 0 1",
        "constraints": "Input format: one line, space-separated level-order values of 0 and 1, with \"null\" for a missing child. Output format: the resulting tree in the same encoding.",
        "solve": _solve_tree_pruning,
        "sample_inputs": ["1 null 0 0 1", "1 0 1 0 0 0 1"],
        "hidden_inputs": [
            "null",                 # empty tree
            "0",                    # the root itself is pruned away
            "1",                    # the root survives alone
            "1 0",                  # a zero leaf goes
            "0 1",                  # the root is kept by its child
            "0 0 0",                # everything is pruned
            "1 1 1",                # nothing is pruned
            "0 0 null 0 null 1",    # a deep 1 keeps the whole chain
            "1 0 0 0 0 0 0",
            "0 null 0 null 0",      # a right chain of zeros
        ],
    },
{
        "title": "Count Complete Tree Nodes",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Given a complete binary tree, count its nodes. Every level except possibly the last is entirely filled, and the last level's nodes are packed as far left as possible.",
        "example_input": "1 2 3 4 5 6",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child; the tree is guaranteed complete. Output format: a single integer.",
        "solve": _solve_count_complete_nodes,
        "sample_inputs": ["1 2 3 4 5 6", "1 2 3"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1",                    # single node
            "1 2",                  # last level holds one node
            "1 2 3 4",
            "1 2 3 4 5",
            "1 2 3 4 5 6 7",        # a perfect tree
            "1 2 3 4 5 6 7 8",
            "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15",
            "1 2 3 4 5 6 7 8 9",
            "1 2 3 4 5 6 7 8 9 10 11 12",
        ],
    },
{
        "title": "Maximum Difference Between Node and Ancestor",
        "topic": "trees",
        "difficulty": "medium",
        "description": "Consider every pair where one node is an ancestor of the other. Return the largest absolute difference between the two values in any such pair.",
        "example_input": "8 3 10 1 6 null 14 null null 4 7 13",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_max_ancestor_diff,
        "sample_inputs": ["8 3 10 1 6 null 14 null null 4 7 13", "1 null 2 null 0 3"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1",                    # no ancestor pair exists, so 0
            "1 2",                  # the only pair
            "2 1",
            "5 5",                  # equal values give 0
            "1 2 3",
            "1 null 2 null 3",      # a chain, the extremes are furthest apart
            "0 null 10 null 5",     # the largest gap skips a level
            "-1 -5 3",              # negatives
            "8 3 10 1 6 null 14",
        ],
    },
{
        "title": "Maximum Product of Splitted Binary Tree",
        "topic": "trees",
        "difficulty": "hard",
        "description": "Remove one edge to split the tree into two parts. Maximise the product of the two parts' sums, then report that product modulo 1000000007.",
        "example_input": "1 2 3 4 5 6",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer, the maximum product modulo 1000000007.",
        "solve": _solve_max_product_split,
        "sample_inputs": ["1 2 3 4 5 6", "1 null 2 3 4 null null 5 6"],
        "hidden_inputs": [
            "null",                 # empty tree, no edge to remove
            "1",                    # no edge exists, so 0
            "1 1",                  # the only possible split
            "1 2",
            "0 0",                  # zeros give a zero product
            "1 2 3",
            "2 3 9 10 7 8 6 5 4 11 1",
            "1 null 2 null 3",      # a chain has only two split points
            "5 5 5 5 5 5 5",
            "1 2 3 4 5 6 7 8 9 10",
        ],
    },
{
        "title": "Invert Binary Tree",
        "topic": "trees", "difficulty": "easy",
        "description": "Swap the left and right child of every node in the tree, and return the result.",
        "example_input": "4 2 7 1 3 6 9",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: the resulting tree in the same encoding.",
        "solve": _solve_invert_tree,
        "sample_inputs": ["4 2 7 1 3 6 9", "2 1 3"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1",                    # a single node is unchanged
            "1 2",                  # a left child becomes a right child
            "1 null 2",
            "1 2 2",                # symmetric values hide the swap
            "1 2 3 4 5 6 7",
            "1 2 null 3",           # a left chain becomes a right chain
            "1 null 2 null 3",
            "-1 -2 -3",             # negatives
            "5 3 8 1 4 7 9",
        ],
    },
{
        "title": "Same Tree",
        "topic": "trees", "difficulty": "easy",
        "description": "Decide whether two binary trees have the same shape and hold the same values in the same places.",
        "example_input": "1 2 3\n1 2 3",
        "constraints": "Input format: line 1 and line 2 are the two trees in level-order encoding. Output format: \"true\" or \"false\".",
        "solve": _solve_same_tree,
        "sample_inputs": ["1 2 3\n1 2 3", "1 2\n1 null 2"],
        "hidden_inputs": [
            "null\nnull",           # both empty
            "1\nnull",              # one empty
            "null\n1",
            "1\n1",
            "1\n2",                 # same shape, different value
            "1 2\n1 2",
            "1 2 3\n1 2 4",         # a difference deep in the tree
            "1 2 3 4\n1 2 3",       # one has an extra node
            "1 null 2\n1 2",        # mirrored, so not the same
            "5 3 8 1 4\n5 3 8 1 4",
        ],
    },
{
        "title": "Symmetric Tree",
        "topic": "trees", "difficulty": "easy",
        "description": "Decide whether a tree is a mirror image of itself about its centre line.",
        "example_input": "1 2 2 3 4 4 3",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: \"true\" or \"false\".",
        "solve": _solve_symmetric_tree,
        "sample_inputs": ["1 2 2 3 4 4 3", "1 2 2 null 3 null 3"],
        "hidden_inputs": [
            "null",                 # an empty tree is symmetric
            "1",                    # a single node
            "1 2",                  # one side only
            "1 null 2",
            "1 2 2",                # a matching pair
            "1 2 3",                # values differ
            "1 2 2 3 null null 3",
            "1 2 2 null 3 3",       # shapes mirror but values sit wrongly
            "1 2 2 2 null 2",
            "2 3 3 4 5 5 4",
        ],
    },
{
        "title": "Minimum Depth of Binary Tree",
        "topic": "trees", "difficulty": "easy",
        "description": "Return the number of nodes along the shortest path from the root down to any leaf. A node with one child is not a leaf.",
        "example_input": "3 9 20 null null 15 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_min_depth,
        "sample_inputs": ["3 9 20 null null 15 7", "2 null 3 null 4 null 5 null 6"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1",                    # the root is a leaf
            "1 2",                  # the single child is the nearest leaf
            "1 null 2",             # the root is not a leaf
            "1 2 3",
            "1 2 3 4 5 6 7",
            "1 2 null 3",           # a left chain
            "1 null 2 null 3",
            "1 2 3 null null 4 5",  # the shallow leaf is on the left
            "1 2 3 4 null null null 5",
        ],
    },
{
        "title": "Sum of Left Leaves",
        "topic": "trees", "difficulty": "easy",
        "description": "Add together the values of every leaf that is the left child of its parent.",
        "example_input": "3 9 20 null null 15 7",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_sum_left_leaves,
        "sample_inputs": ["3 9 20 null null 15 7", "1"],
        "hidden_inputs": [
            "null",                 # empty tree
            "1 2",                  # the only leaf is a left child
            "1 null 2",             # the only leaf is a right child
            "1 2 3",
            "1 2 null 3",           # the left child is not itself a leaf
            "1 null 2 3",           # a left leaf under a right child
            "1 2 3 4 5 6 7",
            "-1 -2 -3",             # negatives
            "0 0 0",                # zeroes
            "5 3 8 1 4 7 9",
        ],
    },
{
        "title": "Range Sum of BST",
        "topic": "trees", "difficulty": "easy",
        "description": "In a binary search tree, add together every value that lies between the two given bounds, both included.",
        "example_input": "10 5 15 3 7 null 18\n7 15",
        "constraints": "Input format: line 1 is the tree in level-order encoding, line 2 holds the low and high bounds. Output format: a single integer.",
        "solve": _solve_range_sum_bst,
        "sample_inputs": ["10 5 15 3 7 null 18\n7 15", "10 5 15 3 7 13 18 1 null 6\n6 10"],
        "hidden_inputs": [
            "null\n1 10",           # empty tree
            "1\n1 1",               # the single node is inside
            "1\n2 3",               # the single node is outside
            "2 1 3\n1 3",           # everything is inside
            "2 1 3\n2 2",           # only the root
            "2 1 3\n4 5",           # nothing is inside
            "5 3 8 1 4 7 9\n3 7",
            "5 3 8 1 4 7 9\n1 9",
            "-5 -10 0\n-10 0",      # negatives
            "10 5 15 3 7 null 18\n18 18",
        ],
    },
{
        "title": "Merge Two Binary Trees",
        "topic": "trees", "difficulty": "easy",
        "description": "Lay one tree over the other. Where both have a node, add the values; where only one does, keep that node as it stands. Return the result.",
        "example_input": "1 3 2 5\n2 1 3 null 4 null 7",
        "constraints": "Input format: line 1 and line 2 are the two trees in level-order encoding. Output format: the merged tree in the same encoding.",
        "solve": _solve_merge_two_trees,
        "sample_inputs": ["1 3 2 5\n2 1 3 null 4 null 7", "1\n1 2"],
        "hidden_inputs": [
            "null\nnull",           # both empty
            "1\nnull",              # one empty
            "null\n1",
            "1\n1",
            "1 2\n1 null 3",        # the children sit on opposite sides
            "1 2 3\n4 5 6",
            "1 2 3\n1",             # one tree stops early
            "-1 -2\n1 2",           # values cancel
            "0 0 0\n0 0 0",
            "1 2 null 3\n1 null 2 null 3",
        ],
    },
{
        "title": "Binary Tree Maximum Path Sum",
        "topic": "trees", "difficulty": "hard",
        "description": "A path is any run of connected nodes that visits none of them twice and need not pass through the root. Return the largest total a path can have.",
        "example_input": "1 2 3",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: a single integer.",
        "solve": _solve_max_path_sum,
        "sample_inputs": ["1 2 3", "-10 9 20 null null 15 7"],
        "hidden_inputs": [
            "1",                    # a single node
            "-3",                   # a single negative node
            "-1 -2 -3",             # all negative, the best is one node
            "1 2",
            "2 -1",                 # the negative child is skipped
            "-2 1",                 # the positive child alone wins
            "0 0 0",
            "1 2 3 4 5 6 7",
            "5 4 8 11 null 13 4 7 2 null null null 1",
            "-10 -9 -20 null null -15 -7",
        ],
    },
{
        "title": "Construct Binary Tree from Preorder and Inorder Traversal",
        "topic": "trees", "difficulty": "hard",
        "description": "Rebuild a binary tree from the order its nodes are visited root-first and the order they are visited left-first. All values are different.",
        "example_input": "3 9 20 15 7\n9 3 15 20 7",
        "constraints": "Input format: line 1 is the root-first order, line 2 is the left-first order, both space-separated with distinct values. Output format: the tree in level-order encoding.",
        "solve": _solve_build_from_preorder_inorder,
        "sample_inputs": ["3 9 20 15 7\n9 3 15 20 7", "1 2\n2 1"],
        "hidden_inputs": [
            "1\n1",                 # a single node
            "1 2\n1 2",             # a right chain
            "2 1\n1 2",             # a right chain, root first
            "1 2 3\n2 1 3",         # a balanced tree
            "1 2 3\n3 2 1",         # a left chain of three
            "1 2 3\n1 2 3",         # a right chain of three
            "3 1 2\n1 2 3",
            "1 2 4 5 3\n4 2 5 1 3",
            "-1 -2 -3\n-2 -1 -3",   # negatives
            "5 3 1 4 8 7 9\n1 3 4 5 7 8 9",
        ],
    },
{
        "title": "Recover Binary Search Tree",
        "topic": "trees", "difficulty": "hard",
        "description": "At most two nodes of a binary search tree have had their values exchanged by mistake. Put them back without changing the tree's shape, and return the result; a tree that is already correct is returned unchanged.",
        "example_input": "1 3 null null 2",
        "constraints": "Input format: one line, space-separated level-order values with \"null\" for a missing child. Output format: the corrected tree in the same encoding.",
        "solve": _solve_recover_bst,
        "sample_inputs": ["1 3 null null 2", "3 1 4 null null 2"],
        "hidden_inputs": [
            "2 1",                  # already correct, nothing swapped
            "1 2",                  # the two nodes are adjacent
            "2 3 1",
            "4 2 6 7 3 5 1",       # two far-apart leaves exchanged
            "1 2 3",
            "2 1 3",                # a correct tree of three
            "5 3 8 1 4 7 9",        # a correct larger tree
            "5 3 8 1 9 7 4",        # two leaves exchanged
            "10 5 15 3 7 13 18",
            "-5 -10 0",
        ],
    },
{
        "title": "Lowest Common Ancestor of a Binary Tree",
        "topic": "trees", "difficulty": "hard",
        "description": "Given two values present in the tree, return the value of the deepest node that has both of them somewhere below it, counting a node as being below itself.",
        "example_input": "3 5 1 6 2 0 8 null null 7 4\n5 1",
        "constraints": "Input format: line 1 is the tree in level-order encoding with distinct values, line 2 holds the two values. Output format: a single integer.",
        "solve": _solve_lowest_common_ancestor,
        "sample_inputs": ["3 5 1 6 2 0 8 null null 7 4\n5 1", "3 5 1 6 2 0 8 null null 7 4\n5 4"],
        "hidden_inputs": [
            "1\n1 1",               # the node is its own ancestor
            "1 2\n1 2",             # one is an ancestor of the other
            "1 2\n2 2",
            "1 2 3\n2 3",           # the root joins both sides
            "1 2 3\n1 3",
            "1 2 null 3\n2 3",      # a left chain
            "1 null 2 null 3\n2 3", # a right chain
            "1 2 3 4 5 6 7\n4 5",
            "1 2 3 4 5 6 7\n4 7",   # the answer is the root
            "5 3 8 1 4 7 9\n1 4",
        ],
    },
]
