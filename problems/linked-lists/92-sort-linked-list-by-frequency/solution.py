class Solution:
    def sortByFrequency(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        freq: dict[int, int] = {}
        nodes: list[ListNode] = []
        curr = head
        while curr is not None:
            freq[curr.val] = freq.get(curr.val, 0) + 1
            nodes.append(curr)
            curr = curr.next
        nodes.sort(key=lambda node: (-freq[node.val], node.val))
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        nodes[-1].next = None
        return nodes[0]
