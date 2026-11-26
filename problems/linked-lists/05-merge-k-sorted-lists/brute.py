class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        vals = []
        for head in lists:
            curr = head
            while curr is not None:
                vals.append(curr.val)
                curr = curr.next
        vals.sort()
        dummy = ListNode(0)
        tail = dummy
        for v in vals:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
