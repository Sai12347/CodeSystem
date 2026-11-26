class Solution {
    public int kthFromMiddle(ListNode head, int k) {
        ListNode fast = head;
        ListNode lag = (k == 0) ? head : null;
        int steps = 0;
        while (fast != null && fast.next != null) {
            fast = fast.next.next;
            steps++;
            if (steps == k) {
                lag = head;
            } else if (steps > k) {
                lag = lag.next;
            }
        }
        return lag != null ? lag.val : -1;
    }
}
