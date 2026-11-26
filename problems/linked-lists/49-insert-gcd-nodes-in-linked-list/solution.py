import math


class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head
        while curr is not None and curr.next is not None:
            nxt = curr.next
            node = ListNode(math.gcd(curr.val, nxt.val), nxt)
            curr.next = node
            curr = nxt
        return head
