class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        n = len(lists)
        interval = 1
        while interval < n:
            for i in range(0, n - interval, interval * 2):
                lists[i] = self._merge(lists[i], lists[i + interval])
            interval *= 2
        return lists[0]

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
