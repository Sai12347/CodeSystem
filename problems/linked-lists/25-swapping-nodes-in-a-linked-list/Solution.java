class Solution {
    public ListNode swapNodes(ListNode head, int k) {
        ListNode lead = head;
        for (int i = 1; i < k; i++) {
            lead = lead.next;
        }
        ListNode first = lead;
        ListNode second = head;
        while (lead.next != null) {
            lead = lead.next;
            second = second.next;
        }
        int tmp = first.val;
        first.val = second.val;
        second.val = tmp;
        return head;
    }
}
