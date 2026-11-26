class Solution {
    public long maxSumPath(ListNode l1, ListNode l2) {
        ListNode p1 = l1;
        ListNode p2 = l2;
        long sum1 = 0L;
        long sum2 = 0L;
        long ans = 0L;
        while (p1 != null && p2 != null) {
            if (p1.val < p2.val) {
                sum1 += p1.val;
                p1 = p1.next;
            } else if (p2.val < p1.val) {
                sum2 += p2.val;
                p2 = p2.next;
            } else {
                ans += Math.max(sum1, sum2) + p1.val;
                sum1 = 0L;
                sum2 = 0L;
                p1 = p1.next;
                p2 = p2.next;
            }
        }
        while (p1 != null) {
            sum1 += p1.val;
            p1 = p1.next;
        }
        while (p2 != null) {
            sum2 += p2.val;
            p2 = p2.next;
        }
        return ans + Math.max(sum1, sum2);
    }
}
