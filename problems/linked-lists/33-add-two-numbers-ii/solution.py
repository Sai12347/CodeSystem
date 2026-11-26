class Solution:
    def _reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        r1 = self._reverse(l1)
        r2 = self._reverse(l2)
        carry = 0
        ans = None
        while r1 is not None or r2 is not None or carry:
            total = carry
            if r1 is not None:
                total += r1.val
                r1 = r1.next
            if r2 is not None:
                total += r2.val
                r2 = r2.next
            carry, digit = divmod(total, 10)
            ans = ListNode(digit, ans)
        return ans
