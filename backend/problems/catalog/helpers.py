"""Shared decoders for the structured stdin formats the catalog uses.

Trees arrive as one line of space-separated level-order values with
"null" for a missing child. Linked lists arrive as one line of
space-separated values.
"""


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


def _serialize_tree(root):
    """Inverse of _build_tree: level-order values with "null" for a missing
    child, trailing nulls trimmed. An empty tree serializes to "null".

    Problems that hand a whole tree back (pruning, leaf deletion, reversing
    levels) print their answer through this, so input and output share one
    encoding and a solution can be checked by re-reading its own output.
    """
    if root is None:
        return "null"
    out = []
    queue = [root]
    while queue:
        node = queue.pop(0)
        if node is None:
            out.append("null")
            continue
        out.append(str(node.val))
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] == "null":
        out.pop()
    return " ".join(out)
