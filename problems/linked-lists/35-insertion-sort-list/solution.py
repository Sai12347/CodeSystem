class Solution:
    def insertionSortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        dummy = ListNode(0, head)
        last_sorted = head
        curr = head.next
        while curr is not None:
            if last_sorted.val <= curr.val:
                last_sorted = last_sorted.next
            else:
                prev = dummy
                while prev.next.val <= curr.val:
                    prev = prev.next
                last_sorted.next = curr.next
                curr.next = prev.next
                prev.next = curr
            curr = last_sorted.next
        return dummy.next
