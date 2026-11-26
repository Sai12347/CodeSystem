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

    def _merge(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while l1 is not None and l2 is not None:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 if l1 is not None else l2
        return dummy.next

    def sortAlternatingList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        asc_head = head
        desc_head = head.next
        asc = asc_head
        desc = desc_head
        while desc is not None and desc.next is not None:
            asc.next = desc.next
            asc = asc.next
            desc.next = asc.next
            desc = desc.next
        asc.next = None
        desc_sorted = self._reverse(desc_head)
        return self._merge(asc_head, desc_sorted)
