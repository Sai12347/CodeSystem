class Solution:
    def maxSumPath(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> int:
        p1, p2 = l1, l2
        sum1 = 0
        sum2 = 0
        ans = 0
        while p1 is not None and p2 is not None:
            if p1.val < p2.val:
                sum1 += p1.val
                p1 = p1.next
            elif p2.val < p1.val:
                sum2 += p2.val
                p2 = p2.next
            else:
                ans += max(sum1, sum2) + p1.val
                sum1 = 0
                sum2 = 0
                p1 = p1.next
                p2 = p2.next
        while p1 is not None:
            sum1 += p1.val
            p1 = p1.next
        while p2 is not None:
            sum2 += p2.val
            p2 = p2.next
        return ans + max(sum1, sum2)
