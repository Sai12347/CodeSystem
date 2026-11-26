from judge_lib import ListNode
import solution


def _verify_intact(head, expected_nodes, expected_vals):
    cur = head
    for node, val in zip(expected_nodes, expected_vals):
        if cur is not node or cur.val != val:
            return False
        cur = cur.next
    return cur is None


def run(inp):
    listA = inp["listA"]
    listB = inp["listB"]
    skipA = int(inp["skipA"])
    skipB = int(inp["skipB"])

    prefA = [ListNode(int(v)) for v in listA[:skipA]]
    prefB = [ListNode(int(v)) for v in listB[:skipB]]
    shared = []
    if skipA < len(listA) and skipB < len(listB):
        shared = [ListNode(int(v)) for v in listA[skipA:]]

    nodesA = prefA + shared
    nodesB = prefB + shared
    for i in range(len(nodesA) - 1):
        nodesA[i].next = nodesA[i + 1]
    for i in range(len(nodesB) - 1):
        nodesB[i].next = nodesB[i + 1]

    headA = nodesA[0] if nodesA else None
    headB = nodesB[0] if nodesB else None
    expected_node = shared[0] if shared else None

    ans = solution.Solution().getIntersectionNode(headA, headB)

    if not _verify_intact(headA, nodesA, listA) or not _verify_intact(headB, nodesB, listB):
        return "ERROR: input linked lists were modified"
    if ans is None:
        return None
    if ans is not expected_node:
        return f"ERROR: returned wrong node reference (val={getattr(ans, 'val', None)})"
    return int(ans.val)
