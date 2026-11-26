class Solution:
    def symmetricDifference(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while l1 is not None and l2 is not None:
            if l1.val < l2.val:
                tail.next = l1
                tail = l1
                l1 = l1.next
            elif l2.val < l1.val:
                tail.next = l2
                tail = l2
                l2 = l2.next
            else:
                l1 = l1.next
                l2 = l2.next
        tail.next = l1 if l1 is not None else l2
        return dummy.next
