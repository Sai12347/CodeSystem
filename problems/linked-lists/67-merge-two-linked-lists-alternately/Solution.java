class Solution {
    public ListNode mergeAlternately(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null && l2 != null) {
            ListNode n1 = l1.next;
            ListNode n2 = l2.next;
            tail.next = l1;
            l1.next = l2;
            tail = l2;
            l1 = n1;
            l2 = n2;
        }
        tail.next = l1 != null ? l1 : l2;
        return dummy.next;
    }
}
