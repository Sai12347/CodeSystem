class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        if head is None or head.next is None:
            return
        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        second = slow.next
        slow.next = None

        prev = None
        curr = second
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        first = head
        second = prev
        while second is not None:
            t1 = first.next
            t2 = second.next
            first.next = second
            second.next = t1
            first = t1
            second = t2
