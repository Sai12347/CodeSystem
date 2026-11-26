class Solution:
    def _reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        rev = self._reverse(head)
        max_val = rev.val
        curr = rev
        while curr.next is not None:
            if curr.next.val < max_val:
                curr.next = curr.next.next
            else:
                curr = curr.next
                max_val = curr.val
        return self._reverse(rev)
