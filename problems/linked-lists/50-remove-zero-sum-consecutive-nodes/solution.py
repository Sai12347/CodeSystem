class Solution:
    def removeZeroSumSublists(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        last: dict[int, ListNode] = {}
        prefix = 0
        curr: Optional[ListNode] = dummy
        while curr is not None:
            prefix += curr.val
            last[prefix] = curr
            curr = curr.next
        prefix = 0
        curr = dummy
        while curr is not None:
            prefix += curr.val
            curr.next = last[prefix].next
            curr = curr.next
        return dummy.next
