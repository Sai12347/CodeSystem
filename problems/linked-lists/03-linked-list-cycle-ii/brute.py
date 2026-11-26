class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        seen = set()
        curr = head
        while curr is not None:
            if curr in seen:
                return curr
            seen.add(curr)
            curr = curr.next
        return None
