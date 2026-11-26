class Solution:
    def unionSortedLists(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while l1 is not None or l2 is not None:
            if l2 is None or (l1 is not None and l1.val <= l2.val):
                node = l1
                l1 = l1.next
            else:
                node = l2
                l2 = l2.next
            if tail is dummy or node.val != tail.val:
                tail.next = node
                tail = node
        tail.next = None
        return dummy.next
