class Solution:
    def kthFromMiddle(self, head: Optional[ListNode], k: int) -> int:
        fast = head
        lag = head if k == 0 else None
        steps = 0
        while fast is not None and fast.next is not None:
            fast = fast.next.next
            steps += 1
            if steps == k:
                lag = head
            elif steps > k:
                lag = lag.next
        return lag.val if lag is not None else -1
