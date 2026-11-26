class Solution {
    public ListNode symmetricDifference(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) {
                tail.next = l1;
                tail = l1;
                l1 = l1.next;
            } else if (l2.val < l1.val) {
                tail.next = l2;
                tail = l2;
                l2 = l2.next;
            } else {
                l1 = l1.next;
                l2 = l2.next;
            }
        }
        tail.next = l1 != null ? l1 : l2;
        return dummy.next;
    }
}
