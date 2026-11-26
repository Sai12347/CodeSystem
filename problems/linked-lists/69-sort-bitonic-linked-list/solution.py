class Solution:
    def sortBitonicList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        curr = head
        while curr.next is not None and curr.val <= curr.next.val:
            curr = curr.next
        if curr.next is None:
            return head
        second = curr.next
        curr.next = None

        prev = None
        while second is not None:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt

        dummy = ListNode(0)
        tail = dummy
        a, b = head, prev
        while a is not None and b is not None:
            if a.val <= b.val:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        tail.next = a if a is not None else b
        return dummy.next
