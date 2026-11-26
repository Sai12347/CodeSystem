class Solution:
    def deleteMiddleK(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if k == 0 or head is None:
            return head
        dummy = ListNode(0, head)
        cut_end = dummy
        for _ in range(k):
            cut_end = cut_end.next
        slow = dummy
        fast = cut_end
        while fast.next is not None and fast.next.next is not None:
            fast = fast.next.next
            slow = slow.next
            cut_end = cut_end.next
        slow.next = cut_end.next
        return dummy.next
