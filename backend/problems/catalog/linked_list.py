"""Linked List problems."""

from .helpers import _build_linked_list, _linked_list_to_str, _LNode


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

def _solve_middle_node(lines):
    vals = lines[0].split()
    return " ".join(vals[len(vals) // 2:])


def _solve_remove_duplicates_sorted_list(lines):
    head = _build_linked_list(lines[0].split())
    node = head
    while node and node.next:
        if node.next.val == node.val:
            node.next = node.next.next
        else:
            node = node.next
    return _linked_list_to_str(head)


def _solve_remove_elements(lines):
    head = _build_linked_list(lines[0].split())
    target = int(lines[1])
    dummy = _LNode(0)
    dummy.next = head
    node = dummy
    while node.next:
        if node.next.val == target:
            node.next = node.next.next
        else:
            node = node.next
    return _linked_list_to_str(dummy.next)


def _solve_palindrome_linked_list(lines):
    vals = [n for n in lines[0].split()]
    return "true" if vals == vals[::-1] else "false"


def _solve_binary_list_to_int(lines):
    head = _build_linked_list(lines[0].split())
    total = 0
    while head:
        total = total * 2 + head.val
        head = head.next
    return str(total)


def _solve_remove_nth_from_end(lines):
    head = _build_linked_list(lines[0].split())
    n = int(lines[1])
    dummy = _LNode(0)
    dummy.next = head
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return _linked_list_to_str(dummy.next)


def _solve_odd_even_list(lines):
    head = _build_linked_list(lines[0].split())
    if not head or not head.next:
        return _linked_list_to_str(head)
    odd = head
    even = head.next
    even_head = even
    while even and even.next:
        odd.next = even.next
        odd = odd.next
        even.next = odd.next
        even = even.next
    odd.next = even_head
    return _linked_list_to_str(head)


def _solve_rotate_list(lines):
    head = _build_linked_list(lines[0].split())
    k = int(lines[1])
    if not head or not head.next:
        return _linked_list_to_str(head)
    length = 1
    tail = head
    while tail.next:
        tail = tail.next
        length += 1
    k %= length
    if k == 0:
        return _linked_list_to_str(head)
    tail.next = head
    steps = length - k
    new_tail = head
    for _ in range(steps - 1):
        new_tail = new_tail.next
    new_head = new_tail.next
    new_tail.next = None
    return _linked_list_to_str(new_head)


def _solve_add_two_numbers(lines):
    a = _build_linked_list(lines[0].split())
    b = _build_linked_list(lines[1].split()) if len(lines) > 1 else None
    dummy = _LNode(0)
    tail = dummy
    carry = 0
    while a or b or carry:
        total = carry
        if a:
            total += a.val
            a = a.next
        if b:
            total += b.val
            b = b.next
        carry, digit = divmod(total, 10)
        tail.next = _LNode(digit)
        tail = tail.next
    return _linked_list_to_str(dummy.next)


def _solve_reverse_k_group(lines):
    head = _build_linked_list(lines[0].split())
    k = int(lines[1])

    def length(node):
        n = 0
        while node:
            n += 1
            node = node.next
        return n

    dummy = _LNode(0)
    dummy.next = head
    group_prev = dummy
    remaining = length(head)
    while remaining >= k:
        node = group_prev.next
        prev = group_prev.next.next
        for _ in range(k - 1):
            nxt = prev.next
            prev.next = node
            node = prev
            prev = nxt
        tail = group_prev.next
        tail.next = prev
        group_prev.next = node
        group_prev = tail
        remaining -= k
    return _linked_list_to_str(dummy.next)


def _solve_sort_list(lines):
    head = _build_linked_list(lines[0].split())

    def split(node):
        slow = node
        fast = node.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        return node, second

    def merge(a, b):
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
        return dummy.next

    def sort(node):
        if not node or not node.next:
            return node
        left, right = split(node)
        return merge(sort(left), sort(right))

    return _linked_list_to_str(sort(head))

def _solve_merge_nodes_between_zeros(lines):
    vals = list(map(int, lines[0].split()))
    out = []
    total = 0
    for v in vals[1:]:
        if v == 0:
            out.append(total)
            total = 0
        else:
            total += v
    return " ".join(map(str, out))


def _solve_delete_middle_node(lines):
    vals = list(map(int, lines[0].split()))
    if len(vals) == 1:
        return ""
    del vals[len(vals) // 2]
    return " ".join(map(str, vals))


def _solve_swap_nodes_in_pairs(lines):
    head = _build_linked_list(lines[0].split())
    dummy = _LNode(0)
    dummy.next = head
    prev = dummy
    while prev.next and prev.next.next:
        first = prev.next
        second = first.next
        first.next = second.next
        second.next = first
        prev.next = second
        prev = first
    return _linked_list_to_str(dummy.next)


def _solve_max_twin_sum(lines):
    vals = list(map(int, lines[0].split()))
    n = len(vals)
    return str(max(vals[i] + vals[n - 1 - i] for i in range(n // 2)))


def _solve_partition_list(lines):
    head = _build_linked_list(lines[0].split())
    x = int(lines[1])
    small = _LNode(0)
    big = _LNode(0)
    s, b = small, big
    while head:
        if head.val < x:
            s.next = head
            s = s.next
        else:
            b.next = head
            b = b.next
        head = head.next
    b.next = None
    s.next = big.next
    return _linked_list_to_str(small.next)


def _solve_reorder_list(lines):
    vals = list(map(int, lines[0].split()))
    out = []
    lo, hi = 0, len(vals) - 1
    while lo <= hi:
        out.append(vals[lo])
        if lo != hi:
            out.append(vals[hi])
        lo += 1
        hi -= 1
    return " ".join(map(str, out))


def _solve_insertion_sort_list(lines):
    head = _build_linked_list(lines[0].split())
    dummy = _LNode(0)
    while head:
        nxt = head.next
        cur = dummy
        while cur.next and cur.next.val < head.val:
            cur = cur.next
        head.next = cur.next
        cur.next = head
        head = nxt
    return _linked_list_to_str(dummy.next)


def _solve_split_linked_list(lines):
    vals = list(map(int, lines[0].split())) if lines[0].strip() else []
    k = int(lines[1])
    n = len(vals)
    size, extra = divmod(n, k)
    out = []
    i = 0
    for part in range(k):
        take = size + (1 if part < extra else 0)
        chunk = vals[i:i + take]
        i += take
        out.append(" ".join(map(str, chunk)) if chunk else "empty")
    return "\n".join(out)


def _solve_swapping_nodes(lines):
    vals = list(map(int, lines[0].split()))
    k = int(lines[1])
    vals[k - 1], vals[len(vals) - k] = vals[len(vals) - k], vals[k - 1]
    return " ".join(map(str, vals))


def _solve_merge_in_between(lines):
    first = list(map(int, lines[0].split()))
    a, b = map(int, lines[1].split())
    second = list(map(int, lines[2].split()))
    return " ".join(map(str, first[:a] + second + first[b + 1:]))


def _solve_next_greater_node(lines):
    vals = list(map(int, lines[0].split()))
    res = [0] * len(vals)
    stack = []
    for i, v in enumerate(vals):
        while stack and vals[stack[-1]] < v:
            res[stack.pop()] = v
        stack.append(i)
    return " ".join(map(str, res))


def _solve_remove_duplicates_ii(lines):
    head = _build_linked_list(lines[0].split())
    dummy = _LNode(0)
    dummy.next = head
    prev = dummy
    while head:
        if head.next and head.next.val == head.val:
            value = head.val
            while head and head.val == value:
                head = head.next
            prev.next = head
        else:
            prev = head
            head = head.next
    return _linked_list_to_str(dummy.next)


def _solve_reverse_between(lines):
    vals = list(map(int, lines[0].split()))
    left, right = map(int, lines[1].split())
    vals[left - 1:right] = vals[left - 1:right][::-1]
    return " ".join(map(str, vals))


def _solve_add_two_numbers_ii(lines):
    a = int("".join(lines[0].split()))
    b = int("".join(lines[1].split())) if len(lines) > 1 and lines[1].strip() else 0
    return " ".join(str(a + b))


def _solve_linked_list_cycle_ii(lines):
    vals = list(map(int, lines[0].split()))
    pos = int(lines[1])
    nodes = [_LNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos != -1:
        nodes[-1].next = nodes[pos]
    slow = fast = nodes[0]
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            finder = nodes[0]
            while finder is not slow:
                finder = finder.next
                slow = slow.next
            return str(nodes.index(finder))
    return "-1"


def _solve_lru_cache(lines):
    capacity = int(lines[0])
    q = int(lines[1])
    order = []
    store = {}
    out = []
    for i in range(2, 2 + q):
        parts = lines[i].split()
        if parts[0] == "put":
            key, value = int(parts[1]), int(parts[2])
            if key in store:
                order.remove(key)
            elif len(store) >= capacity:
                oldest = order.pop(0)
                del store[oldest]
            store[key] = value
            order.append(key)
        else:
            key = int(parts[1])
            if key in store:
                order.remove(key)
                order.append(key)
                out.append(str(store[key]))
            else:
                out.append("-1")
    return " ".join(out)


def _solve_design_linked_list(lines):
    q = int(lines[0])
    data = []
    out = []
    for i in range(1, 1 + q):
        parts = lines[i].split()
        op = parts[0]
        if op == "addAtHead":
            data.insert(0, int(parts[1]))
        elif op == "addAtTail":
            data.append(int(parts[1]))
        elif op == "addAtIndex":
            index, value = int(parts[1]), int(parts[2])
            if index <= len(data):
                data.insert(index, value)
        elif op == "deleteAtIndex":
            index = int(parts[1])
            if 0 <= index < len(data):
                del data[index]
        else:
            index = int(parts[1])
            out.append(str(data[index]) if 0 <= index < len(data) else "-1")
    return " ".join(out)


def _solve_remove_zero_sum_sublists(lines):
    vals = list(map(int, lines[0].split()))
    changed = True
    while changed:
        changed = False
        for i in range(len(vals)):
            total = 0
            for j in range(i, len(vals)):
                total += vals[j]
                if total == 0:
                    del vals[i:j + 1]
                    changed = True
                    break
            if changed:
                break
    return " ".join(map(str, vals))


def _solve_reverse_even_length_groups(lines):
    vals = list(map(int, lines[0].split()))
    out = []
    i = 0
    size = 1
    while i < len(vals):
        group = vals[i:i + size]
        if len(group) % 2 == 0:
            group = group[::-1]
        out.extend(group)
        i += size
        size += 1
    return " ".join(map(str, out))


PROBLEMS = [
{
        "title": "Reverse Linked List",
        "topic": "linked_list",
        "difficulty": "easy",
        "description": "Given the head of a singly linked list, reverse the list and return the reversed list.",
        "example_input": "1 2 3 4 5",
        "constraints": "Input format: one line, space-separated list values head-to-tail. Output format: space-separated reversed values.",
        "solve": _solve_reverse_linked_list,
        "sample_inputs": ["1 2 3 4 5", "10 20 30"],
        "hidden_inputs": [
            "1",         # single node
            "0",
            "1 2",
            "7 7",       # duplicate values
            "1 2 3",
            "5 5 5",
            "-1 -2 -3",  # negative values
            "100 -100",
            "1 2 3 4 5 6 7 8 9 10",
        ],
    },
{
        "title": "Merge Two Sorted Lists",
        "topic": "linked_list",
        "difficulty": "medium",
        "description": "Given the heads of two sorted linked lists, merge them into one sorted list and return its head.",
        "example_input": "1 2 4\n1 3 4",
        "constraints": "Input format: line 1 and line 2 are the two sorted lists, space-separated. Output format: the merged sorted list, space-separated.",
        "solve": _solve_merge_two_lists,
        "sample_inputs": ["1 2 4\n1 3 4", "2 6 8\n1 5 9"],
        "hidden_inputs": [
            "1\n2",              # one node each
            "2\n1",
            "1 2 3\n",           # second list empty
            "\n1 2 3",           # first list empty
            "5\n1 2 4",
            "1 3\n2",
            "1 1 1\n1 1 1",      # every value duplicated across both lists
            "1 2 3\n4 5 6",      # disjoint, first entirely before second
            "4 5 6\n1 2 3",      # disjoint, reversed
            "-5 -3\n-4 -2",      # negatives
            "1 3 5 7\n2 4 6 8",  # strict interleave
        ],
    },
{
        "title": "Linked List Cycle",
        "topic": "linked_list",
        "difficulty": "hard",
        "description": "Given the head of a linked list and the index (0-based) the tail connects back to (-1 if it doesn't), determine if the list has a cycle.",
        "example_input": "3 2 0 -4\n1",
        "constraints": "Input format: line 1 is the space-separated node values, line 2 is the 0-indexed position the tail connects to (-1 for no cycle). Output format: \"true\" or \"false\".",
        "solve": _solve_linked_list_cycle,
        "sample_inputs": ["3 2 0 -4\n1", "1 2 3 4\n-1"],
        "hidden_inputs": [
            "1\n-1",         # single node, no cycle
            "1\n0",          # single node pointing at itself
            "1 2\n0",
            "1 2\n1",        # tail links to itself
            "1 2 3\n-1",
            "1 2 3 4 5\n-1",
            "1 2 3 4 5\n0",  # cycle spans the whole list
            "1 2 3 4 5\n4",  # cycle is just the last node
            "-1 -2 -3\n2",
        ],
    },
{
        "title": "Middle of the Linked List",
        "topic": "linked_list",
        "difficulty": "easy",
        "description": "Return the list starting from its middle node. When the list has an even number of nodes, start from the second of the two middle ones.",
        "example_input": "1 2 3 4 5",
        "constraints": "Input format: one line of space-separated values, head first. Output format: the values from the middle node onwards, space-separated.",
        "solve": _solve_middle_node,
        "sample_inputs": ["1 2 3 4 5", "1 2 3 4 5 6"],
        "hidden_inputs": [
            "1",                    # a single node is its own middle
            "1 2",                  # the second of two
            "1 2 3",
            "1 2 3 4",
            "5 5 5",                # duplicate values
            "-1 -2 -3",             # negatives
            "1 2 3 4 5 6 7",
            "1 2 3 4 5 6 7 8",
            "9 8 7 6 5 4 3 2 1",
            "0 0",
        ],
    },
{
        "title": "Remove Duplicates from Sorted List",
        "topic": "linked_list",
        "difficulty": "easy",
        "description": "Given a list whose values are in non-decreasing order, delete the repeats so that every value appears once, and return the resulting list.",
        "example_input": "1 1 2",
        "constraints": "Input format: one line of space-separated values in non-decreasing order. Output format: the deduplicated list, space-separated.",
        "solve": _solve_remove_duplicates_sorted_list,
        "sample_inputs": ["1 1 2", "1 1 2 3 3"],
        "hidden_inputs": [
            "1",                    # nothing to remove
            "1 1",                  # everything collapses to one node
            "1 2",                  # no duplicates at all
            "1 1 1 1",
            "1 2 3",
            "-2 -2 -1 0 0",         # negatives
            "0 0 0 1 1 2",
            "5 5 5 5 5 5 5 5",
            "1 1 2 2 3 3 4 4",
            "1 2 2 3 4 4 5",
        ],
    },
{
        "title": "Remove Linked List Elements",
        "topic": "linked_list",
        "difficulty": "easy",
        "description": "Delete every node holding the given value and return the resulting list.",
        "example_input": "1 2 6 3 4 5 6\n6",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is the value to remove. Output format: the resulting list, space-separated (empty if nothing remains).",
        "solve": _solve_remove_elements,
        "sample_inputs": ["1 2 6 3 4 5 6\n6", "7 7 7 7\n7"],
        "hidden_inputs": [
            "1\n1",                 # the only node goes
            "1\n2",                 # nothing matches
            "1 1\n1",               # the list empties
            "1 2\n1",               # the head goes
            "1 2\n2",               # the tail goes
            "1 2 1\n1",             # both ends go, the middle stays
            "2 1 2\n2",
            "-1 -1 0\n-1",          # negatives
            "1 2 3 4 5\n3",
            "6 6 1 6 6 2 6\n6",
        ],
    },
{
        "title": "Palindrome Linked List",
        "topic": "linked_list",
        "difficulty": "easy",
        "description": "Decide whether the list reads the same from the head as it does from the tail.",
        "example_input": "1 2 2 1",
        "constraints": "Input format: one line of space-separated values. Output format: \"true\" or \"false\".",
        "solve": _solve_palindrome_linked_list,
        "sample_inputs": ["1 2 2 1", "1 2"],
        "hidden_inputs": [
            "1",                    # a single node
            "1 1",                  # the shortest true case of length two
            "1 2 1",                # odd length with a centre
            "1 2 3",
            "1 2 2 1 1",            # nearly a palindrome
            "0 0 0 0",
            "-1 0 -1",              # negatives
            "1 2 3 2 1",
            "1 2 3 3 2 1",
            "1 0 1 0 1",
        ],
    },
{
        "title": "Convert Binary Number in a Linked List to Integer",
        "topic": "linked_list",
        "difficulty": "easy",
        "description": "The list holds the binary digits of a number, most significant first. Return the value of that number in ordinary decimal.",
        "example_input": "1 0 1",
        "constraints": "Input format: one line of space-separated values, each 0 or 1. Output format: a single integer.",
        "solve": _solve_binary_list_to_int,
        "sample_inputs": ["1 0 1", "1 1 0 1"],
        "hidden_inputs": [
            "0",                    # a single zero
            "1",                    # a single one
            "0 0",                  # leading zeros
            "0 1",
            "1 0",
            "1 1",
            "0 0 0 1",              # several leading zeros
            "1 1 1 1 1 1 1 1",      # 255
            "1 0 0 0 0 0 0 0 0 0",  # 512
            "1 0 1 0 1 0 1 0 1 0",
        ],
    },
{
        "title": "Remove Nth Node From End of List",
        "topic": "linked_list",
        "difficulty": "medium",
        "description": "Delete the node that sits n places from the end of the list and return what remains.",
        "example_input": "1 2 3 4 5\n2",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is n (1 <= n <= list length). Output format: the resulting list, space-separated (empty if nothing remains).",
        "solve": _solve_remove_nth_from_end,
        "sample_inputs": ["1 2 3 4 5\n2", "1 2\n1"],
        "hidden_inputs": [
            "1\n1",                 # the list empties
            "1 2\n2",               # the head goes
            "1 2 3\n1",             # the tail goes
            "1 2 3\n3",             # the head again, longer list
            "1 2 3\n2",             # the middle
            "1 1 1\n2",             # duplicate values
            "-1 -2 -3\n2",          # negatives
            "1 2 3 4\n4",
            "1 2 3 4 5 6\n3",
            "5 4 3 2 1\n5",
        ],
    },
{
        "title": "Odd Even Linked List",
        "topic": "linked_list",
        "difficulty": "medium",
        "description": "Reorder the list so that the nodes in odd positions come first, followed by those in even positions, counting positions from one. Within each half the original order is kept.",
        "example_input": "1 2 3 4 5",
        "constraints": "Input format: one line of space-separated values. Output format: the reordered list, space-separated.",
        "solve": _solve_odd_even_list,
        "sample_inputs": ["1 2 3 4 5", "2 1 3 5 6 4 7"],
        "hidden_inputs": [
            "1",                    # nothing moves
            "1 2",                  # already in the right shape
            "1 2 3",
            "1 2 3 4",
            "1 1 1 1",              # duplicate values
            "1 2 3 4 5 6",
            "1 2 3 4 5 6 7",
            "-1 -2 -3 -4",          # negatives
            "0 1 0 1 0 1",
            "9 8 7 6 5 4 3 2",
        ],
    },
{
        "title": "Rotate List",
        "topic": "linked_list",
        "difficulty": "medium",
        "description": "Move every node k places towards the end, wrapping the ones that fall off the end back round to the front, and return the resulting list.",
        "example_input": "1 2 3 4 5\n2",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is k (k >= 0). Output format: the rotated list, space-separated.",
        "solve": _solve_rotate_list,
        "sample_inputs": ["1 2 3 4 5\n2", "0 1 2\n4"],
        "hidden_inputs": [
            "1\n0",                 # nothing to do
            "1\n5",                 # a single node rotates onto itself
            "1 2\n0",
            "1 2\n1",
            "1 2\n2",               # a full turn restores the list
            "1 2 3\n3",             # k equal to the length
            "1 2 3\n4",             # k just past the length
            "1 2 3\n100",           # k far beyond the length
            "1 2 3 4 5\n5",
            "5 5 5\n1",             # duplicate values
        ],
    },
{
        "title": "Add Two Numbers",
        "topic": "linked_list",
        "difficulty": "medium",
        "description": "Two numbers are stored as lists of single digits, least significant digit first. Return their sum stored the same way.",
        "example_input": "2 4 3\n5 6 4",
        "constraints": "Input format: line 1 and line 2 are the two digit lists, least significant first. Output format: the sum as a digit list, least significant first.",
        "solve": _solve_add_two_numbers,
        "sample_inputs": ["2 4 3\n5 6 4", "9 9 9 9\n9 9 9"],
        "hidden_inputs": [
            "0\n0",                 # zero plus zero
            "1\n1",
            "5\n5",                 # a carry out of a single digit
            "9\n1",                 # the sum grows a digit
            "0\n9",
            "1 2\n3 4",             # no carrying anywhere
            "9 9\n1",               # a carry that ripples
            "9 9 9\n9 9 9",
            "1 0 0 0 1\n9",         # a carry that stops immediately
            "2 4 3\n5 6 4 7",       # different lengths
        ],
    },
{
        "title": "Reverse Nodes in k-Group",
        "topic": "linked_list",
        "difficulty": "hard",
        "description": "Reverse the list in blocks of k consecutive nodes. If fewer than k nodes remain at the end, leave them in their original order.",
        "example_input": "1 2 3 4 5\n2",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is k (k >= 1). Output format: the resulting list, space-separated.",
        "solve": _solve_reverse_k_group,
        "sample_inputs": ["1 2 3 4 5\n2", "1 2 3 4 5\n3"],
        "hidden_inputs": [
            "1\n1",                 # a block of one changes nothing
            "1 2 3\n1",             # k of one never reorders
            "1 2\n2",               # exactly one block
            "1 2 3\n2",             # a leftover node stays put
            "1 2 3\n5",             # k larger than the list
            "1 2 3 4\n2",           # two full blocks
            "1 2 3 4\n4",
            "1 2 3 4 5 6\n3",
            "1 1 2 2\n2",           # duplicate values
            "1 2 3 4 5 6 7\n3",     # a leftover of one after two blocks
        ],
    },
{
        "title": "Sort List",
        "topic": "linked_list",
        "difficulty": "hard",
        "description": "Return the list with its values arranged in non-decreasing order.",
        "example_input": "4 2 1 3",
        "constraints": "Input format: one line of space-separated values. Output format: the sorted list, space-separated.",
        "solve": _solve_sort_list,
        "sample_inputs": ["4 2 1 3", "-1 5 3 4 0"],
        "hidden_inputs": [
            "1",                    # nothing to sort
            "2 1",                  # a single swap
            "1 2",                  # already sorted
            "1 1 1",                # all equal
            "3 2 1",                # fully reversed
            "-1 -2 -3",             # negatives
            "0 0 1 0",
            "5 1 4 2 3",
            "9 8 7 6 5 4 3 2 1 0",
            "2 1 2 1 2 1",          # duplicates interleaved
        ],
    },
{
        "title": "Merge Nodes in Between Zeros",
        "topic": "linked_list", "difficulty": "easy",
        "description": "The list begins and ends with a zero, with more zeroes scattered between. Replace each stretch between two zeroes by a single value holding its total, and drop the zeroes.",
        "example_input": "0 3 1 0 4 5 2 0",
        "constraints": "Input format: one line of space-separated values beginning and ending with 0, with no two zeroes adjacent except as separators. Output format: the resulting list, space-separated.",
        "solve": _solve_merge_nodes_between_zeros,
        "sample_inputs": ["0 3 1 0 4 5 2 0", "0 1 0 3 0 2 2 0"],
        "hidden_inputs": [
            "0 1 0",                # a single stretch
            "0 5 0",
            "0 1 1 0",
            "0 1 0 2 0",            # two stretches
            "0 1 0 1 0",
            "0 9 9 9 0",
            "0 1 2 3 0 4 0",
            "0 1 0 2 0 3 0",
            "0 100 0 200 0",
            "0 1 1 1 1 1 0",
        ],
    },
{
        "title": "Delete the Middle Node of a Linked List",
        "topic": "linked_list", "difficulty": "easy",
        "description": "Remove the node sitting in the middle of the list, counting from zero and taking the later of the two when the length is even, then return what is left.",
        "example_input": "1 3 4 7 1 2 6",
        "constraints": "Input format: one line of space-separated values. Output format: the resulting list, space-separated, or an empty line if nothing remains.",
        "solve": _solve_delete_middle_node,
        "sample_inputs": ["1 3 4 7 1 2 6", "1 2 3 4"],
        "hidden_inputs": [
            "1",                    # the list empties
            "1 2",                  # the later of the two goes
            "2 1",
            "1 2 3",                # the exact middle goes
            "1 1 1",
            "1 2 3 4 5",
            "1 2 3 4 5 6",
            "-1 -2 -3",             # negatives
            "5 5 5 5",
            "1 2 3 4 5 6 7 8",
        ],
    },
{
        "title": "Swap Nodes in Pairs",
        "topic": "linked_list", "difficulty": "easy",
        "description": "Exchange every two neighbouring nodes, leaving a final odd node where it is, and return the result.",
        "example_input": "1 2 3 4",
        "constraints": "Input format: one line of space-separated values. Output format: the resulting list, space-separated.",
        "solve": _solve_swap_nodes_in_pairs,
        "sample_inputs": ["1 2 3 4", "1 2 3"],
        "hidden_inputs": [
            "1",                    # nothing to swap
            "1 2",                  # a single swap
            "2 1",
            "1 1",                  # equal values hide the swap
            "1 2 3 4 5",
            "1 2 3 4 5 6",
            "-1 -2 -3 -4",          # negatives
            "0 0 0",
            "5 4 3 2 1",
            "1 2 3 4 5 6 7",
        ],
    },
{
        "title": "Maximum Twin Sum of a Linked List",
        "topic": "linked_list", "difficulty": "easy",
        "description": "Pair the first node with the last, the second with the second-last, and so on. Return the largest total any such pair has.",
        "example_input": "5 4 2 1",
        "constraints": "Input format: one line of an even count of space-separated values. Output format: a single integer.",
        "solve": _solve_max_twin_sum,
        "sample_inputs": ["5 4 2 1", "4 2 2 3"],
        "hidden_inputs": [
            "1 2",                  # a single pair
            "2 1",
            "0 0",
            "1 1 1 1",              # every pair equal
            "1 2 3 4",
            "4 3 2 1",
            "-1 -2 -3 -4",          # negatives
            "1 100 100 1",          # the inner pair wins
            "100 1 1 100",          # the outer pair wins
            "1 2 3 4 5 6",
        ],
    },
{
        "title": "Partition List",
        "topic": "linked_list", "difficulty": "medium",
        "description": "Rearrange the list so that every value below the given threshold comes before every value at or above it, keeping the original order within each group.",
        "example_input": "1 4 3 2 5 2\n3",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is the threshold. Output format: the rearranged list, space-separated.",
        "solve": _solve_partition_list,
        "sample_inputs": ["1 4 3 2 5 2\n3", "2 1\n2"],
        "hidden_inputs": [
            "1\n1",                 # a single value, at the threshold
            "1\n2",                 # below it
            "1 2\n2",
            "3 1\n2",               # the order must flip
            "1 1 1\n1",             # nothing moves
            "3 3 3\n1",
            "1 2 3\n4",             # everything is below
            "1 2 3\n0",             # everything is above
            "5 1 4 2 3\n3",
            "-1 -2 0 1\n0",         # negatives
        ],
    },
{
        "title": "Reorder List",
        "topic": "linked_list", "difficulty": "medium",
        "description": "Rearrange the list so it reads first node, last node, second node, second-last node, and so on inwards.",
        "example_input": "1 2 3 4",
        "constraints": "Input format: one line of space-separated values. Output format: the reordered list, space-separated.",
        "solve": _solve_reorder_list,
        "sample_inputs": ["1 2 3 4", "1 2 3 4 5"],
        "hidden_inputs": [
            "1",                    # nothing moves
            "1 2",
            "1 2 3",                # the middle node stays put
            "1 1 1 1",
            "1 2 3 4 5 6",
            "1 2 3 4 5 6 7",
            "-1 -2 -3 -4",          # negatives
            "0 0 0",
            "5 4 3 2 1",
            "1 2 3 4 5 6 7 8",
        ],
    },
{
        "title": "Insertion Sort List",
        "topic": "linked_list", "difficulty": "medium",
        "description": "Arrange the list in non-decreasing order by taking each node in turn and placing it where it belongs among those already sorted.",
        "example_input": "4 2 1 3",
        "constraints": "Input format: one line of space-separated values. Output format: the sorted list, space-separated.",
        "solve": _solve_insertion_sort_list,
        "sample_inputs": ["4 2 1 3", "-1 5 3 4 0"],
        "hidden_inputs": [
            "1",                    # nothing to do
            "2 1",
            "1 2",
            "1 1 1",                # equal values
            "3 2 1",                # fully reversed
            "-1 -2 -3",             # negatives
            "0 0 1 0",
            "5 1 4 2 3",
            "1 2 3 4 5",
            "9 8 7 6 5 4 3 2 1",
        ],
    },
{
        "title": "Split Linked List in Parts",
        "topic": "linked_list", "difficulty": "medium",
        "description": "Cut the list into the given number of consecutive parts, as equal as possible, with any longer parts coming first. Some parts may end up holding nothing.",
        "example_input": "1 2 3\n5",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is the number of parts. Output format: one part per line, values space-separated, writing \"empty\" for a part holding nothing.",
        "solve": _solve_split_linked_list,
        "sample_inputs": ["1 2 3\n5", "1 2 3 4 5 6 7 8 9 10\n3"],
        "hidden_inputs": [
            "1\n1",                 # one part holding everything
            "1\n2",                 # the second part is empty
            "1\n3",
            "1 2\n2",
            "1 2\n1",
            "1 2 3\n2",             # the first part gets the extra
            "1 2 3 4\n2",           # an even split
            "1 2 3 4 5\n5",
            "1 2 3 4 5\n2",
            "1 2 3 4 5 6 7\n3",
        ],
    },
{
        "title": "Swapping Nodes in a Linked List",
        "topic": "linked_list", "difficulty": "medium",
        "description": "Exchange the value of the node k places from the start with the value of the node k places from the end, counting both from one, and return the result.",
        "example_input": "1 2 3 4 5\n2",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is k. Output format: the resulting list, space-separated.",
        "solve": _solve_swapping_nodes,
        "sample_inputs": ["1 2 3 4 5\n2", "7 9 6 6 7 8 3 0 9 5\n5"],
        "hidden_inputs": [
            "1\n1",                 # the node swaps with itself
            "1 2\n1",               # the two ends
            "1 2\n2",               # the same swap from the other side
            "1 2 3\n2",             # the middle swaps with itself
            "1 2 3\n1",
            "1 1 1\n2",             # equal values hide the swap
            "1 2 3 4\n2",
            "1 2 3 4 5\n3",
            "-1 -2 -3\n1",          # negatives
            "1 2 3 4 5 6\n3",
        ],
    },
{
        "title": "Merge In Between Linked Lists",
        "topic": "linked_list", "difficulty": "medium",
        "description": "Cut out the nodes of the first list from position a to position b inclusive, counting from zero, and put the whole of the second list in their place.",
        "example_input": "0 1 2 3 4 5\n3 4\n1000000 1000001 1000002",
        "constraints": "Input format: line 1 is the first list, line 2 holds a and b, line 3 is the second list. Output format: the resulting list, space-separated.",
        "solve": _solve_merge_in_between,
        "sample_inputs": ["0 1 2 3 4 5\n3 4\n1000000 1000001 1000002", "0 1 2 3 4 5 6\n2 5\n1000000 1000001 1000002 1000003 1000004"],
        "hidden_inputs": [
            "1 2 3\n1 1\n9",        # one node replaced by one
            "1 2 3\n0 0\n9",        # the head replaced
            "1 2 3\n2 2\n9",        # the tail replaced
            "1 2 3\n0 2\n9",        # the whole list replaced
            "1 2 3 4\n1 2\n9 9",
            "1 2 3 4\n1 2\n9",      # the replacement is shorter
            "1 2 3 4 5\n2 3\n0 0 0 0",
            "1 2\n0 0\n7 8 9",
            "1 2 3 4 5 6\n1 4\n0",
            "1 2 3\n1 2\n4 5 6",
        ],
    },
{
        "title": "Next Greater Node In Linked List",
        "topic": "linked_list", "difficulty": "medium",
        "description": "For each node, report the first value further along the list that is strictly larger than it, or zero if there is none.",
        "example_input": "2 1 5",
        "constraints": "Input format: one line of space-separated values. Output format: one result per node, space-separated.",
        "solve": _solve_next_greater_node,
        "sample_inputs": ["2 1 5", "2 7 4 3 5"],
        "hidden_inputs": [
            "1",                    # nothing follows
            "1 2",
            "2 1",
            "1 1",                  # equal is not greater
            "1 1 1",
            "1 2 3",                # each resolved by its neighbour
            "3 2 1",                # nothing is ever resolved
            "1 7 5 1 9 2 5 1",
            "5 5 5 6",              # one late value resolves the run
            "9 8 7 6 5",
        ],
    },
{
        "title": "Remove Duplicates from Sorted List II",
        "topic": "linked_list", "difficulty": "medium",
        "description": "Given a list whose values are in non-decreasing order, delete every node whose value appears more than once, keeping only the values that appear exactly once.",
        "example_input": "1 2 3 3 4 4 5",
        "constraints": "Input format: one line of space-separated values in non-decreasing order. Output format: the resulting list, space-separated, or an empty line if nothing remains.",
        "solve": _solve_remove_duplicates_ii,
        "sample_inputs": ["1 2 3 3 4 4 5", "1 1 1 2 3"],
        "hidden_inputs": [
            "1",                    # nothing repeats
            "1 1",                  # the list empties
            "1 2",
            "1 1 1",
            "1 1 2",
            "1 2 2",
            "1 1 2 2",              # everything repeats
            "1 2 3",
            "-1 -1 0 1 1",          # negatives
            "1 1 2 3 3 4 5 5",
        ],
    },
{
        "title": "Reverse Linked List II",
        "topic": "linked_list", "difficulty": "hard",
        "description": "Reverse only the stretch of the list from position left to position right, counting from one, and return the result.",
        "example_input": "1 2 3 4 5\n2 4",
        "constraints": "Input format: line 1 is the space-separated values, line 2 holds left and right with left no greater than right. Output format: the resulting list, space-separated.",
        "solve": _solve_reverse_between,
        "sample_inputs": ["1 2 3 4 5\n2 4", "5\n1 1"],
        "hidden_inputs": [
            "1\n1 1",               # a single node, unchanged
            "1 2\n1 1",             # a stretch of one
            "1 2\n1 2",             # the whole list
            "1 2\n2 2",
            "1 2 3\n1 2",           # the front reversed
            "1 2 3\n2 3",           # the back reversed
            "1 2 3\n1 3",
            "1 2 3 4 5\n1 5",
            "1 1 1 1\n2 3",         # equal values hide the change
            "1 2 3 4 5 6\n3 5",
        ],
    },
{
        "title": "Add Two Numbers II",
        "topic": "linked_list", "difficulty": "hard",
        "description": "Two numbers are stored as lists of single digits, most significant digit first. Return their total stored the same way.",
        "example_input": "7 2 4 3\n5 6 4",
        "constraints": "Input format: line 1 and line 2 are the two digit lists, most significant first, without leading zeros unless the number is zero. Output format: the total as a digit list, most significant first.",
        "solve": _solve_add_two_numbers_ii,
        "sample_inputs": ["7 2 4 3\n5 6 4", "2 4 3\n5 6 4"],
        "hidden_inputs": [
            "0\n0",                 # zero plus zero
            "0\n1",
            "1\n0",
            "1\n1",
            "5\n5",                 # a carry grows a digit
            "9\n1",
            "9 9\n1",               # a carry that ripples
            "9 9 9\n9 9 9",
            "1 0 0\n1",
            "1 2 3\n4 5 6",
        ],
    },
{
        "title": "Linked List Cycle II",
        "topic": "linked_list", "difficulty": "hard",
        "description": "Given the values and the position the tail links back to, return the position at which the loop begins, or -1 if the list has no loop.",
        "example_input": "3 2 0 -4\n1",
        "constraints": "Input format: line 1 is the space-separated values, line 2 is the position the tail links to, counting from zero, or -1 for no loop. Output format: a single integer.",
        "solve": _solve_linked_list_cycle_ii,
        "sample_inputs": ["3 2 0 -4\n1", "1 2\n0"],
        "hidden_inputs": [
            "1\n-1",                # no loop
            "1\n0",                 # a node pointing at itself
            "1 2\n-1",
            "1 2\n1",               # the tail points at itself
            "1 2 3\n-1",
            "1 2 3\n0",             # the whole list loops
            "1 2 3\n2",
            "1 2 3 4 5\n2",
            "-1 -2 -3\n1",          # negatives
            "1 2 3 4 5\n4",
        ],
    },
{
        "title": "LRU Cache",
        "topic": "linked_list", "difficulty": "hard",
        "description": "A cache of fixed size answers lookups and stores values. When it is full, storing a new key discards whichever key has gone longest without being looked up or stored. Report the answer to every lookup, using -1 for a key that is absent.",
        "example_input": "2\n7\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\nput 4 4\nget 1",
        "constraints": "Input format: line 1 is the capacity, line 2 is the number of operations, followed by that many lines each \"put key value\" or \"get key\". Output format: the lookup answers, space-separated.",
        "solve": _solve_lru_cache,
        "sample_inputs": ["2\n7\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\nput 4 4\nget 1", "1\n3\nput 1 1\nput 2 2\nget 1"],
        "hidden_inputs": [
            "1\n1\nget 1",                  # nothing stored yet
            "1\n2\nput 1 5\nget 1",
            "1\n3\nput 1 5\nput 1 6\nget 1",    # storing again replaces
            "1\n3\nput 1 1\nput 2 2\nget 2",
            "2\n4\nput 1 1\nput 2 2\nget 1\nget 2",
            "2\n5\nput 1 1\nput 2 2\nput 3 3\nget 1\nget 3",
            "2\n6\nput 1 1\nput 2 2\nget 1\nput 3 3\nget 2\nget 3",
            "3\n5\nput 1 1\nput 2 2\nput 3 3\nput 4 4\nget 1",
            "2\n4\nput 2 1\nput 2 2\nget 2\nget 1",
            "2\n6\nput 1 1\nget 1\nput 2 2\nput 3 3\nget 1\nget 2",
        ],
    },
{
        "title": "Design Linked List",
        "topic": "linked_list", "difficulty": "hard",
        "description": "Simulate a list supporting reading a value by position, adding at the front, adding at the back, adding at a given position and deleting at a given position. Positions count from zero, and reading or deleting outside the list does nothing, with reading reporting -1.",
        "example_input": "6\naddAtHead 1\naddAtTail 3\naddAtIndex 1 2\nget 1\ndeleteAtIndex 1\nget 1",
        "constraints": "Input format: line 1 is the number of operations, followed by that many lines each \"get i\", \"addAtHead v\", \"addAtTail v\", \"addAtIndex i v\" or \"deleteAtIndex i\". Output format: the answers to the reads, space-separated.",
        "solve": _solve_design_linked_list,
        "sample_inputs": ["6\naddAtHead 1\naddAtTail 3\naddAtIndex 1 2\nget 1\ndeleteAtIndex 1\nget 1", "3\naddAtHead 1\nget 0\nget 1"],
        "hidden_inputs": [
            "1\nget 0",                             # reading an empty list
            "2\naddAtHead 5\nget 0",
            "2\naddAtTail 5\nget 0",
            "2\naddAtIndex 0 5\nget 0",
            "2\naddAtIndex 1 5\nget 0",             # the position is past the end
            "3\naddAtHead 1\ndeleteAtIndex 0\nget 0",
            "3\naddAtHead 1\ndeleteAtIndex 5\nget 0",   # deleting past the end
            "4\naddAtHead 1\naddAtHead 2\nget 0\nget 1",
            "5\naddAtTail 1\naddAtTail 2\naddAtIndex 1 3\nget 1\nget 2",
            "6\naddAtHead 7\naddAtHead 2\naddAtHead 1\naddAtIndex 3 0\ndeleteAtIndex 2\nget 2",
        ],
    },
{
        "title": "Remove Zero Sum Consecutive Nodes from Linked List",
        "topic": "linked_list", "difficulty": "hard",
        "description": "Repeatedly delete any run of consecutive nodes whose values add up to zero, until no such run remains, and return what is left.",
        "example_input": "1 2 -3 3 1",
        "constraints": "Input format: one line of space-separated values. Output format: the resulting list, space-separated, or an empty line if nothing remains.",
        "solve": _solve_remove_zero_sum_sublists,
        "sample_inputs": ["1 2 -3 3 1", "1 2 3 -3 4"],
        "hidden_inputs": [
            "1",                    # nothing sums to zero
            "0",                    # a single zero goes
            "1 -1",                 # the list empties
            "0 0",
            "1 2 -3",               # the whole list cancels
            "1 -1 2",
            "2 1 -1",
            "1 2 3 -3 -2",
            "5 -3 -2 1",            # a cancelling run in the middle
            "1 3 2 -3 -2 5 5 -5 1",
        ],
    },
{
        "title": "Reverse Nodes in Even Length Groups",
        "topic": "linked_list", "difficulty": "hard",
        "description": "Split the list into consecutive groups of size one, then two, then three and so on, with the final group holding whatever is left. Reverse the groups whose length is even, leave the rest alone, and return the result.",
        "example_input": "5 2 6 3 9 1 7 3 8 4",
        "constraints": "Input format: one line of space-separated values. Output format: the resulting list, space-separated.",
        "solve": _solve_reverse_even_length_groups,
        "sample_inputs": ["5 2 6 3 9 1 7 3 8 4", "1 1 0 6"],
        "hidden_inputs": [
            "1",                    # one group of one
            "1 2",                  # the second group has one node, odd
            "1 2 3",                # the second group is even, reversed
            "1 2 3 4",
            "1 2 3 4 5",
            "1 2 3 4 5 6",
            "1 1 1 1 1 1",          # equal values hide the change
            "0 0 0",
            "1 2 3 4 5 6 7",
            "-1 -2 -3 -4 -5",       # negatives
        ],
    },
]
