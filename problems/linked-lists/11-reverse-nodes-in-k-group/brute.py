class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        nodes = []
        cur = head
        while cur is not None:
            nodes.append(cur)
            cur = cur.next
        for i in range(0, len(nodes) - k + 1, k):
            nodes[i:i + k] = reversed(nodes[i:i + k])
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        if nodes:
            nodes[-1].next = None
            return nodes[0]
        return None
