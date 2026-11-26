class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        cur = head
        while cur is not None:
            vals.append(cur.val)
            cur = cur.next
        vals.sort()
        dummy = ListNode(0)
        cur = dummy
        for v in vals:
            cur.next = ListNode(v)
            cur = cur.next
        return dummy.next
