class Solution {
    public int[] nodesBetweenCriticalPoints(ListNode head) {
        int firstIdx = -1;
        int prevIdx = -1;
        int minDist = Integer.MAX_VALUE;
        ListNode prev = head;
        ListNode curr = head.next;
        int idx = 1;
        while (curr != null && curr.next != null) {
            ListNode nxt = curr.next;
            if ((curr.val > prev.val && curr.val > nxt.val) || (curr.val < prev.val && curr.val < nxt.val)) {
                if (firstIdx == -1) {
                    firstIdx = idx;
                } else {
                    minDist = Math.min(minDist, idx - prevIdx);
                }
                prevIdx = idx;
            }
            prev = curr;
            curr = nxt;
            idx++;
        }
        if (minDist == Integer.MAX_VALUE) {
            return new int[]{-1, -1};
        }
        return new int[]{minDist, prevIdx - firstIdx};
    }
}
