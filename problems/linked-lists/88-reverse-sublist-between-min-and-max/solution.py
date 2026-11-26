class Solution:
    def reverseBetweenMinMax(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        min_val = head.val
        max_val = head.val
        min_pos = 1
        max_pos = 1
        pos = 1
        curr = head
        while curr is not None:
            if curr.val < min_val:
                min_val = curr.val
                min_pos = pos
            if curr.val > max_val:
                max_val = curr.val
                max_pos = pos
            curr = curr.next
            pos += 1
        left = min(min_pos, max_pos)
        right = max(min_pos, max_pos)
        if left == right:
            return head

        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next
        tail = prev.next
        curr = tail
        rprev = None
        for _ in range(right - left + 1):
            nxt = curr.next
            curr.next = rprev
            rprev = curr
            curr = nxt
        prev.next = rprev
        tail.next = curr
        return dummy.next
