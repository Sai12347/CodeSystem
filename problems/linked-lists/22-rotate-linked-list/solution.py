class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None or head.next is None or k == 0:
            return head
        n = 1
        tail = head
        while tail.next is not None:
            tail = tail.next
            n += 1
        k %= n
        if k == 0:
            return head
        tail.next = head
        steps = n - k
        new_tail = tail
        for _ in range(steps):
            new_tail = new_tail.next
        new_head = new_tail.next
        new_tail.next = None
        return new_head
