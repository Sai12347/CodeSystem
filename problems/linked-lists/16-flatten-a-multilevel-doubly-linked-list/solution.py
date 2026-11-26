class Solution:
    def flatten(self, head: "Optional[Node]") -> "Optional[Node]":
        cur = head
        while cur is not None:
            if cur.child is not None:
                nxt = cur.next
                child = cur.child
                cur.child = None
                cur.next = child
                child.prev = cur

                tail = child
                while tail.next is not None:
                    tail = tail.next

                tail.next = nxt
                if nxt is not None:
                    nxt.prev = tail
            cur = cur.next
        return head
