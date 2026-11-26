"""CodeSystem judge library (Python): shared node classes and JSON <-> typed value conversion.

Type strings use the Java spelling from the problem signature, e.g. "int[]", "List<List<Integer>>",
"TreeNode", "char[][]". Problem adapters may import and reuse convert()/serialize().
"""
from collections import deque
from typing import Any, List, Optional

MAX_LIST_NODES = 1_000_000


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:
        return f"ListNode({self.val})"


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None, right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


_INT_TYPES = {"int", "Integer", "long", "Long"}
_FLOAT_TYPES = {"double", "Double"}
_BOOL_TYPES = {"boolean", "Boolean"}
_STR_TYPES = {"String", "char", "Character"}


def build_list(vals):
    if vals is None:
        return None
    dummy = ListNode(0)
    cur = dummy
    for v in vals:
        cur.next = ListNode(int(v))
        cur = cur.next
    return dummy.next


def list_to_json(head):
    out = []
    while head is not None:
        if len(out) >= MAX_LIST_NODES:
            raise ValueError("Returned linked list is too long or contains a cycle")
        out.append(int(head.val))
        head = head.next
    return out


def build_tree(vals):
    if not vals or vals[0] is None:
        return None
    root = TreeNode(int(vals[0]))
    q = deque([root])
    i = 1
    while q and i < len(vals):
        node = q.popleft()
        if i < len(vals):
            v = vals[i]
            i += 1
            if v is not None:
                node.left = TreeNode(int(v))
                q.append(node.left)
        if i < len(vals):
            v = vals[i]
            i += 1
            if v is not None:
                node.right = TreeNode(int(v))
                q.append(node.right)
    return root


def tree_to_json(root):
    out = []
    if root is None:
        return out
    q = deque([root])
    count = 0
    while q:
        node = q.popleft()
        count += 1
        if count > 4 * MAX_LIST_NODES:
            raise ValueError("Returned tree is too large or contains a cycle")
        if node is None:
            out.append(None)
            continue
        out.append(int(node.val))
        q.append(node.left)
        q.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def _inner(t: str) -> str:
    return t[5:-1]


def convert(j: Any, t: str) -> Any:
    if t.endswith("[]"):
        if j is None:
            return None
        comp = t[:-2]
        return [convert(x, comp) for x in j]
    if t.startswith("List<"):
        if j is None:
            return None
        inner = _inner(t)
        return [convert(x, inner) for x in j]
    if j is None and t not in ("ListNode", "TreeNode"):
        return None
    if t in _INT_TYPES:
        return int(j)
    if t in _FLOAT_TYPES:
        return float(j)
    if t in _BOOL_TYPES:
        return bool(j)
    if t in _STR_TYPES:
        return str(j)
    if t == "ListNode":
        return build_list(j)
    if t == "TreeNode":
        return build_tree(j)
    raise ValueError(f"Unsupported type {t}")


def generic(v: Any) -> Any:
    if v is None or isinstance(v, (bool, str)):
        return v
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return v
    if isinstance(v, ListNode):
        return list_to_json(v)
    if isinstance(v, TreeNode):
        return tree_to_json(v)
    if isinstance(v, dict):
        return {str(k): generic(x) for k, x in v.items()}
    if isinstance(v, (list, tuple, set, frozenset, deque)):
        return [generic(x) for x in v]
    if hasattr(v, "val") and hasattr(v, "next"):
        return list_to_json(v)
    if hasattr(v, "val") and hasattr(v, "left") and hasattr(v, "right"):
        return tree_to_json(v)
    return str(v)


def serialize(v: Any, t: str) -> Any:
    if t == "void":
        return None
    if v is None:
        return None
    if t.endswith("[]") or t.startswith("List<"):
        comp = t[:-2] if t.endswith("[]") else _inner(t)
        if isinstance(v, (str, bytes)) and comp in _STR_TYPES:
            return [str(c) for c in v]
        return [serialize(x, comp) for x in v]
    if t in _INT_TYPES:
        if isinstance(v, float) and not v.is_integer():
            raise TypeError(f"Expected an integer return value but got {v!r}")
        return int(v)
    if t in _FLOAT_TYPES:
        return float(v)
    if t in _BOOL_TYPES:
        return bool(v)
    if t in _STR_TYPES:
        return str(v)
    if t == "ListNode":
        return list_to_json(v)
    if t == "TreeNode":
        return tree_to_json(v)
    return generic(v)
