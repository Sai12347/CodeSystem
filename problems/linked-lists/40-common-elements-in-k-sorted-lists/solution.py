class Solution:
    def _intersect_two(self, a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while a is not None and b is not None:
            if a.val == b.val:
                tail.next = a
                tail = tail.next
                a = a.next
                b = b.next
            elif a.val < b.val:
                a = a.next
            else:
                b = b.next
        tail.next = None
        return dummy.next

    def commonElementsKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        min_idx = 0
        min_len = 10**18
        for i, node in enumerate(lists):
            length = 0
            curr = node
            while curr is not None:
                length += 1
                curr = curr.next
            if length == 0:
                return None
            if length < min_len:
                min_len = length
                min_idx = i
        res = lists[min_idx]
        for i, node in enumerate(lists):
            if i == min_idx:
                continue
            res = self._intersect_two(res, node)
            if res is None:
                return None
        return res
