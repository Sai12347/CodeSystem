class Solution:
    def subtractSecondHalf(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        def reverse(node: Optional[ListNode]) -> Optional[ListNode]:
            prev = None
            curr = node
            while curr is not None:
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt
            return prev

        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        rev = reverse(slow.next)
        p1 = head
        p2 = rev
        while p2 is not None:
            p1.val -= p2.val
            p1 = p1.next
            p2 = p2.next
        slow.next = reverse(rev)
        return head
