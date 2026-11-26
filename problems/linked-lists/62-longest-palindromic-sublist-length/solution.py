class Solution:
    def maxPalindromeLength(self, head: Optional[ListNode]) -> int:
        def count_common(a: Optional[ListNode], b: Optional[ListNode]) -> int:
            c = 0
            while a is not None and b is not None and a.val == b.val:
                c += 1
                a = a.next
                b = b.next
            return c

        ans = 0
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            odd = 2 * count_common(prev, nxt) + 1
            even = 2 * count_common(curr, nxt)
            if odd > ans:
                ans = odd
            if even > ans:
                ans = even
            prev = curr
            curr = nxt
        return ans
