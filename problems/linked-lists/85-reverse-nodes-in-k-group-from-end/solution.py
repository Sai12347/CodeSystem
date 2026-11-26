class Solution:
    def reverseKGroupFromEnd(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None or k <= 1:
            return head
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next
        if n < k:
            return head
        skip = n % k
        groups = n // k
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(skip):
            prev = prev.next
        for _ in range(groups):
            tail = prev.next
            c = tail
            rprev = None
            for _ in range(k):
                nxt = c.next
                c.next = rprev
                rprev = c
                c = nxt
            prev.next = rprev
            tail.next = c
            prev = tail
        return dummy.next
