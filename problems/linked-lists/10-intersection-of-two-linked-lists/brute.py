class Solution:
    def getIntersectionNode(self, headA: Optional[ListNode], headB: Optional[ListNode]) -> Optional[ListNode]:
        seen = set()
        cur = headA
        while cur is not None:
            seen.add(cur)
            cur = cur.next
        cur = headB
        while cur is not None:
            if cur in seen:
                return cur
            cur = cur.next
        return None
