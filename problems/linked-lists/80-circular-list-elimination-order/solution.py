class Solution:
    def eliminationOrder(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        nodes = []
        curr = head
        while curr is not None:
            nodes.append(curr)
            curr = curr.next
        n = len(nodes)
        bit = [i & -i for i in range(n + 1)]
        max_pow = 1 << (n.bit_length() - 1)

        dummy = ListNode(0)
        tail = dummy
        pos = 0
        for rem in range(n, 0, -1):
            pos = (pos + k - 1) % rem
            target = pos + 1
            idx = 0
            step = max_pow
            while step > 0:
                nxt = idx + step
                if nxt <= n and bit[nxt] < target:
                    target -= bit[nxt]
                    idx = nxt
                step >>= 1
            chosen = idx + 1
            x = chosen
            while x <= n:
                bit[x] -= 1
                x += x & -x
            node = nodes[chosen - 1]
            tail.next = node
            tail = node
        tail.next = None
        return dummy.next
