class Solution:
    def reverseDecreasingRuns(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev_tail = dummy
        curr = head
        while curr is not None:
            run_tail = curr
            rev_head = curr
            last_val = curr.val
            nxt = curr.next
            curr.next = None
            while nxt is not None and nxt.val < last_val:
                last_val = nxt.val
                after = nxt.next
                nxt.next = rev_head
                rev_head = nxt
                nxt = after
            prev_tail.next = rev_head
            prev_tail = run_tail
            curr = nxt
        return dummy.next
