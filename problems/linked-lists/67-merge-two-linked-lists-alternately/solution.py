class Solution:
    def mergeAlternately(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while l1 is not None and l2 is not None:
            n1 = l1.next
            n2 = l2.next
            tail.next = l1
            l1.next = l2
            tail = l2
            l1 = n1
            l2 = n2
        tail.next = l1 if l1 is not None else l2
        return dummy.next
