class Solution {
    public ListNode reverseKGroup(ListNode head, int k) {
        if (k <= 1 || head == null) {
            return head;
        }
        ListNode dummy = new ListNode(0, head);
        ListNode groupPrev = dummy;

        while (true) {
            ListNode kth = groupPrev;
            for (int i = 0; i < k; i++) {
                kth = kth.next;
                if (kth == null) {
                    return dummy.next;
                }
            }

            ListNode groupNext = kth.next;
            ListNode prev = groupNext;
            ListNode cur = groupPrev.next;
            while (cur != groupNext) {
                ListNode nxt = cur.next;
                cur.next = prev;
                prev = cur;
                cur = nxt;
            }

            ListNode newTail = groupPrev.next;
            groupPrev.next = kth;
            groupPrev = newTail;
        }
    }
}
