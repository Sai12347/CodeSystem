class Solution:
    def splitListToParts(self, head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next
        base, rem = divmod(n, k)
        res: List[Optional[ListNode]] = [None] * k
        curr = head
        for i in range(k):
            part_len = base + (1 if i < rem else 0)
            if part_len == 0 or curr is None:
                continue
            res[i] = curr
            for _ in range(part_len - 1):
                curr = curr.next
            nxt = curr.next
            curr.next = None
            curr = nxt
        return res
