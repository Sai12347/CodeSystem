class Solution {
    public ListNode mergeReverse(ListNode l1, ListNode l2) {
        ListNode res = null;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                ListNode nxt = l1.next;
                l1.next = res;
                res = l1;
                l1 = nxt;
            } else {
                ListNode nxt = l2.next;
                l2.next = res;
                res = l2;
                l2 = nxt;
            }
        }
        ListNode rem = l1 != null ? l1 : l2;
        while (rem != null) {
            ListNode nxt = rem.next;
            rem.next = res;
            res = rem;
            rem = nxt;
        }
        return res;
    }
}
