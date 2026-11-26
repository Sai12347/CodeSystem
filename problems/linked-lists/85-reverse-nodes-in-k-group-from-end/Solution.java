class Solution {
    public ListNode reverseKGroupFromEnd(ListNode head, int k) {
        if (head == null || k <= 1) {
            return head;
        }
        int n = 0;
        ListNode curr = head;
        while (curr != null) {
            n++;
            curr = curr.next;
        }
        if (n < k) {
            return head;
        }
        int skip = n % k;
        int groups = n / k;
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        for (int i = 0; i < skip; i++) {
            prev = prev.next;
        }
        for (int g = 0; g < groups; g++) {
            ListNode tail = prev.next;
            ListNode c = tail;
            ListNode rprev = null;
            for (int i = 0; i < k; i++) {
                ListNode nxt = c.next;
                c.next = rprev;
                rprev = c;
                c = nxt;
            }
            prev.next = rprev;
            tail.next = c;
            prev = tail;
        }
        return dummy.next;
    }
}
