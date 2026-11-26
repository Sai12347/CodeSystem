class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        curr = head
        while curr is not None:
            vals.append(curr.val)
            curr = curr.next
        dummy = ListNode(0)
        tail = dummy
        for v in reversed(vals):
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
