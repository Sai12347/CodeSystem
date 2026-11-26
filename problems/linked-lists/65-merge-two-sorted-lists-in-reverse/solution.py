class Solution:
    def mergeReverse(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        res = None
        while l1 is not None and l2 is not None:
            if l1.val <= l2.val:
                nxt = l1.next
                l1.next = res
                res = l1
                l1 = nxt
            else:
                nxt = l2.next
                l2.next = res
                res = l2
                l2 = nxt
        rem = l1 if l1 is not None else l2
        while rem is not None:
            nxt = rem.next
            rem.next = res
            res = rem
            rem = nxt
        return res
