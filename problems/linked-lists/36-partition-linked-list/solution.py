class Solution:
    def partition(self, head: Optional[ListNode], x: int) -> Optional[ListNode]:
        before_dummy = ListNode(0)
        after_dummy = ListNode(0)
        before = before_dummy
        after = after_dummy
        curr = head
        while curr is not None:
            if curr.val < x:
                before.next = curr
                before = before.next
            else:
                after.next = curr
                after = after.next
            curr = curr.next
        after.next = None
        before.next = after_dummy.next
        return before_dummy.next
