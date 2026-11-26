class Solution:
    def reverseBetweenZeros(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        while prev.next is not None:
            if prev.next.val == 0:
                prev = prev.next
            else:
                seg_tail = prev.next
                curr = seg_tail
                rprev = None
                while curr is not None and curr.val != 0:
                    nxt = curr.next
                    curr.next = rprev
                    rprev = curr
                    curr = nxt
                prev.next = rprev
                seg_tail.next = curr
                prev = seg_tail
        return dummy.next
