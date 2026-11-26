class Solution {
    public ListNode doubleIt(ListNode head) {
        if (head.val >= 5) {
            head = new ListNode(0, head);
        }
        ListNode curr = head;
        while (curr != null) {
            int carry = (curr.next != null && curr.next.val >= 5) ? 1 : 0;
            curr.val = (curr.val * 2) % 10 + carry;
            curr = curr.next;
        }
        return head;
    }
}
