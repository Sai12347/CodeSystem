class Solution:
    def interleaveHalves(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        slow = head
        fast = head.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        first = head
        while second is not None:
            nxt1 = first.next
            nxt2 = second.next
            first.next = second
            second.next = nxt1
            first = nxt1
            second = nxt2
        return head
