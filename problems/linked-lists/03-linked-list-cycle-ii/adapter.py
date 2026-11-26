from judge_lib import ListNode
import solution


def run(inp):
    vals = [int(v) for v in inp["head"]]
    pos = int(inp["pos"])
    nodes = [ListNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    head = nodes[0] if nodes else None
    ret = solution.Solution().detectCycle(head)
    for i, node in enumerate(nodes):
        if node.val != vals[i]:
            return "linked list values were modified"
        expected_next = nodes[i + 1] if i + 1 < len(nodes) else (nodes[pos] if pos >= 0 else None)
        if node.next is not expected_next:
            return "linked list next pointers were modified"
    if ret is None:
        return -1
    for i, node in enumerate(nodes):
        if node is ret:
            return i
    return "returned node is not in the original list"
