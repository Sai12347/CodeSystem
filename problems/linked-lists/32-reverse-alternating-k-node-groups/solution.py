class Solution:
    def reverseAlternatingKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None or k <= 1:
            return head
        dummy = ListNode(0, head)
        prev = dummy
        curr = head
        should_reverse = True
        while curr is not None:
            if should_reverse:
                group_tail = curr
                rprev = None
                count = 0
                while curr is not None and count < k:
                    nxt = curr.next
                    curr.next = rprev
                    rprev = curr
                    curr = nxt
                    count += 1
                prev.next = rprev
                group_tail.next = curr
                prev = group_tail
            else:
                count = 0
                while curr is not None and count < k:
                    prev = curr
                    curr = curr.next
                    count += 1
            should_reverse = not should_reverse
        return dummy.next
