class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        if head is None or head.next is None:
            return True
        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        second_head = self._reverse(slow.next)
        p1 = head
        p2 = second_head
        ok = True
        while p2 is not None:
            if p1.val != p2.val:
                ok = False
                break
            p1 = p1.next
            p2 = p2.next
        slow.next = self._reverse(second_head)
        return ok

    def _reverse(self, node: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = node
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev
