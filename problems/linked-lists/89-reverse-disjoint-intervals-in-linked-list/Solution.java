class Solution {
    public ListNode reverseDisjointIntervals(ListNode head, int[][] intervals) {
        if (head == null || intervals == null || intervals.length == 0) {
            return head;
        }
        int[][] ordered = new int[intervals.length][];
        System.arraycopy(intervals, 0, ordered, 0, intervals.length);
        Arrays.sort(ordered, (a, b) -> Integer.compare(a[0], b[0]));

        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        int pos = 0;
        for (int[] iv : ordered) {
            int l = iv[0];
            int r = iv[1];
            while (pos < l - 1) {
                prev = prev.next;
                pos++;
            }
            ListNode tail = prev.next;
            ListNode curr = tail;
            ListNode rprev = null;
            for (int i = 0; i < r - l + 1; i++) {
                ListNode nxt = curr.next;
                curr.next = rprev;
                rprev = curr;
                curr = nxt;
            }
            prev.next = rprev;
            tail.next = curr;
            prev = tail;
            pos = r;
        }
        return dummy.next;
    }
}
