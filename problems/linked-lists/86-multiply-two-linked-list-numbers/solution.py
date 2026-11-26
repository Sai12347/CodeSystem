class Solution:
    def multiplyLists(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def to_rev_digits(node: Optional[ListNode]) -> list[int]:
            digs = []
            while node is not None:
                digs.append(node.val)
                node = node.next
            digs.reverse()
            return digs

        a = to_rev_digits(l1)
        b = to_rev_digits(l2)
        if (len(a) == 1 and a[0] == 0) or (len(b) == 1 and b[0] == 0):
            return ListNode(0)

        res = [0] * (len(a) + len(b))
        for i, da in enumerate(a):
            for j, db in enumerate(b):
                res[i + j] += da * db
        carry = 0
        for i in range(len(res)):
            total = res[i] + carry
            res[i] = total % 10
            carry = total // 10
        while len(res) > 1 and res[-1] == 0:
            res.pop()

        head = None
        for d in res:
            head = ListNode(d, head)
        return head
