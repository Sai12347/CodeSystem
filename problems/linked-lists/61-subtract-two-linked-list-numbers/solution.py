class Solution:
    def subtractTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def length(node: Optional[ListNode]) -> int:
            c = 0
            while node is not None:
                c += 1
                node = node.next
            return c

        def reverse(node: Optional[ListNode]) -> Optional[ListNode]:
            prev = None
            while node is not None:
                nxt = node.next
                node.next = prev
                prev = node
                node = nxt
            return prev

        n1, n2 = length(l1), length(l2)
        if n1 < n2:
            big, small = l2, l1
        elif n1 > n2:
            big, small = l1, l2
        else:
            p1, p2 = l1, l2
            while p1 is not None and p1.val == p2.val:
                p1 = p1.next
                p2 = p2.next
            if p1 is None:
                return ListNode(0)
            big, small = (l1, l2) if p1.val > p2.val else (l2, l1)

        r1 = reverse(big)
        r2 = reverse(small)
        borrow = 0
        res = None
        while r1 is not None:
            v2 = r2.val if r2 is not None else 0
            diff = r1.val - v2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            res = ListNode(diff, res)
            r1 = r1.next
            if r2 is not None:
                r2 = r2.next

        while res is not None and res.val == 0 and res.next is not None:
            res = res.next
        return res
