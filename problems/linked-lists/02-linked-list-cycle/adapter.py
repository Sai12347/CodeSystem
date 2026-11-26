from judge_lib import ListNode
import solution


def run(inp):
    vals = inp["head"]
    pos = inp["pos"]
    nodes = [ListNode(int(v)) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if nodes and pos >= 0:
        nodes[-1].next = nodes[pos]
    head = nodes[0] if nodes else None
    return bool(solution.Solution().hasCycle(head))
