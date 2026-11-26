class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        vals = []
        curr = head
        while curr is not None:
            vals.append(curr.val)
            curr = curr.next
        del vals[-n]
        dummy = ListNode(0)
        tail = dummy
        for v in vals:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
