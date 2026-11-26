class Solution:
    def threeWayPartition(self, head: Optional[ListNode], low: int, high: int) -> Optional[ListNode]:
        less_d = ListNode(0)
        mid_d = ListNode(0)
        high_d = ListNode(0)
        less_t, mid_t, high_t = less_d, mid_d, high_d
        curr = head
        while curr is not None:
            if curr.val < low:
                less_t.next = curr
                less_t = curr
            elif curr.val <= high:
                mid_t.next = curr
                mid_t = curr
            else:
                high_t.next = curr
                high_t = curr
            curr = curr.next
        high_t.next = None
        mid_t.next = high_d.next
        less_t.next = mid_d.next
        return less_d.next
