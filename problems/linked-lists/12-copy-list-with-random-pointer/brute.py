class Solution:
    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if head is None:
            return None
        old_to_new = {}
        cur = head
        while cur is not None:
            old_to_new[cur] = Node(cur.val)
            cur = cur.next
        cur = head
        while cur is not None:
            clone = old_to_new[cur]
            clone.next = old_to_new.get(cur.next)
            clone.random = old_to_new.get(cur.random)
            cur = cur.next
        return old_to_new[head]
