class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        n = 0
        cur = head
        while cur is not None:
            n += 1
            cur = cur.next

        def split(node: Optional[ListNode], size: int) -> Optional[ListNode]:
            for _ in range(size - 1):
                if node is None:
                    break
                node = node.next
            if node is None:
                return None
            rest = node.next
            node.next = None
            return rest

        def merge(l1: Optional[ListNode], l2: Optional[ListNode], tail: ListNode) -> ListNode:
            cur_tail = tail
            while l1 is not None and l2 is not None:
                if l1.val <= l2.val:
                    cur_tail.next = l1
                    l1 = l1.next
                else:
                    cur_tail.next = l2
                    l2 = l2.next
                cur_tail = cur_tail.next
            cur_tail.next = l1 if l1 is not None else l2
            while cur_tail.next is not None:
                cur_tail = cur_tail.next
            return cur_tail

        dummy = ListNode(0, head)
        step = 1
        while step < n:
            tail = dummy
            cur = dummy.next
            while cur is not None:
                left = cur
                right = split(left, step)
                cur = split(right, step)
                tail = merge(left, right, tail)
            step <<= 1

        return dummy.next
