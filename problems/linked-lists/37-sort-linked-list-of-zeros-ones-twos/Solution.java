class Solution {
    public ListNode sortZeroOneTwo(ListNode head) {
        ListNode zHead = new ListNode(0);
        ListNode oHead = new ListNode(0);
        ListNode tHead = new ListNode(0);
        ListNode z = zHead, o = oHead, t = tHead;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val == 0) {
                z.next = curr;
                z = z.next;
            } else if (curr.val == 1) {
                o.next = curr;
                o = o.next;
            } else {
                t.next = curr;
                t = t.next;
            }
            curr = curr.next;
        }
        t.next = null;
        o.next = tHead.next;
        z.next = (oHead.next != null) ? oHead.next : tHead.next;
        return zHead.next;
    }
}
