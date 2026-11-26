class Solution:
    def reverseDisjointIntervals(self, head: Optional[ListNode], intervals: List[List[int]]) -> Optional[ListNode]:
        if head is None or not intervals:
            return head
        ordered = sorted(intervals, key=lambda x: x[0])
        dummy = ListNode(0, head)
        prev = dummy
        pos = 0
        for l, r in ordered:
            while pos < l - 1:
                prev = prev.next
                pos += 1
            tail = prev.next
            curr = tail
            rprev = None
            for _ in range(r - l + 1):
                nxt = curr.next
                curr.next = rprev
                rprev = curr
                curr = nxt
            prev.next = rprev
            tail.next = curr
            prev = tail
            pos = r
        return dummy.next
