class Solution:
    def getIntersectionNode(self, headA: Optional[ListNode], headB: Optional[ListNode]) -> Optional[ListNode]:
        pA, pB = headA, headB
        while pA is not pB:
            pA = pA.next if pA is not None else headB
            pB = pB.next if pB is not None else headA
        return pA
