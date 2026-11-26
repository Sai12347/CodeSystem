class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def to_int(node):
            val = 0
            place = 1
            while node:
                val += node.val * place
                place *= 10
                node = node.next
            return val

        s = to_int(l1) + to_int(l2)
        if s == 0:
            return ListNode(0)
        dummy = ListNode(0)
        cur = dummy
        while s > 0:
            cur.next = ListNode(s % 10)
            cur = cur.next
            s //= 10
        return dummy.next
