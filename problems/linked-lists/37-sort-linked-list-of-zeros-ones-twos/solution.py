class Solution:
    def sortZeroOneTwo(self, head: Optional[ListNode]) -> Optional[ListNode]:
        z_head = ListNode(0)
        o_head = ListNode(0)
        t_head = ListNode(0)
        z, o, t = z_head, o_head, t_head
        curr = head
        while curr is not None:
            if curr.val == 0:
                z.next = curr
                z = z.next
            elif curr.val == 1:
                o.next = curr
                o = o.next
            else:
                t.next = curr
                t = t.next
            curr = curr.next
        t.next = None
        o.next = t_head.next
        z.next = o_head.next if o_head.next is not None else t_head.next
        return z_head.next
