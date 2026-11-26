class Solution {
    public ListNode unionSortedLists(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null || l2 != null) {
            ListNode node;
            if (l2 == null || (l1 != null && l1.val <= l2.val)) {
                node = l1;
                l1 = l1.next;
            } else {
                node = l2;
                l2 = l2.next;
            }
            if (tail == dummy || node.val != tail.val) {
                tail.next = node;
                tail = node;
            }
        }
        tail.next = null;
        return dummy.next;
    }
}
