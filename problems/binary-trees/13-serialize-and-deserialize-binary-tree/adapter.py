from collections import deque
from judge_lib import build_tree, tree_to_json
import solution


def _collect_ids(root):
    ids = set()
    if root is None:
        return ids
    q = deque([root])
    while q:
        node = q.popleft()
        ids.add(id(node))
        if node.left is not None:
            q.append(node.left)
        if node.right is not None:
            q.append(node.right)
    return ids


def run(inp):
    orig = build_tree(inp["root"])
    orig_json = tree_to_json(orig)
    orig_ids = _collect_ids(orig)

    ser = solution.Codec().serialize(orig)
    if not isinstance(ser, str):
        return f"ERROR: serialize must return str, got {type(ser).__name__}"
    if tree_to_json(orig) != orig_json:
        return "ERROR: serialize must not modify the input tree"

    deser = solution.Codec().deserialize(ser)
    if deser is not None:
        seen = set()
        q = deque([deser])
        while q:
            node = q.popleft()
            nid = id(node)
            if nid in orig_ids:
                return "ERROR: deserialize must construct new TreeNode objects, not reuse original nodes"
            if nid in seen:
                return "ERROR: deserialized tree contains a cycle or shared node"
            if len(seen) > 100_000:
                return "ERROR: deserialized tree is too large"
            seen.add(nid)
            if node.left is not None:
                q.append(node.left)
            if node.right is not None:
                q.append(node.right)

    return tree_to_json(deser)
