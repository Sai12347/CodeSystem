class Solution:
    def removeUnsortedDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        seen = {head.val}
        prev = head
        curr = head.next
        while curr is not None:
            if curr.val in seen:
                prev.next = curr.next
            else:
                seen.add(curr.val)
                prev = curr
            curr = curr.next
        return head
