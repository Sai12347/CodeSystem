class Solution:
    def doubleIt(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head.val >= 5:
            head = ListNode(0, head)
        curr = head
        while curr is not None:
            carry = 1 if (curr.next is not None and curr.next.val >= 5) else 0
            curr.val = (curr.val * 2) % 10 + carry
            curr = curr.next
        return head
