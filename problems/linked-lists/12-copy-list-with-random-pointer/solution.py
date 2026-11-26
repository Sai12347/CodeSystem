class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if head is None:
            return None

        # Pass 1: interleave cloned nodes right after each original node
        cur = head
        while cur is not None:
            clone = Node(cur.val, cur.next, None)
            cur.next = clone
            cur = clone.next

        # Pass 2: assign random pointers for cloned nodes
        cur = head
        while cur is not None:
            if cur.random is not None:
                cur.next.random = cur.random.next
            cur = cur.next.next

        # Pass 3: separate original list and cloned list
        clone_head = head.next
        cur = head
        while cur is not None:
            clone = cur.next
            cur.next = clone.next
            if clone.next is not None:
                clone.next = clone.next.next
            cur = cur.next

        return clone_head
