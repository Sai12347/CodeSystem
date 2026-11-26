class Solution:
    def plusOne(self, head: Optional[ListNode]) -> Optional[ListNode]:
        sentinel = ListNode(0, head)
        not_nine = sentinel
        curr = head
        while curr is not None:
            if curr.val != 9:
                not_nine = curr
            curr = curr.next
        not_nine.val += 1
        curr = not_nine.next
        while curr is not None:
            curr.val = 0
            curr = curr.next
        return sentinel if sentinel.val == 1 else sentinel.next
