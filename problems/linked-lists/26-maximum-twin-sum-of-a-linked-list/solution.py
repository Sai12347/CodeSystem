class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        slow = head
        fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        prev = None
        curr = slow
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        best = 0
        left = head
        right = prev
        while right is not None:
            s = left.val + right.val
            if s > best:
                best = s
            left = left.next
            right = right.next
        return best
