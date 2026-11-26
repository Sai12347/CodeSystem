class Solution:
    def zigzagList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head
        expect_less = True
        while curr is not None and curr.next is not None:
            if expect_less:
                if curr.val > curr.next.val:
                    curr.val, curr.next.val = curr.next.val, curr.val
            else:
                if curr.val < curr.next.val:
                    curr.val, curr.next.val = curr.next.val, curr.val
            expect_less = not expect_less
            curr = curr.next
        return head
