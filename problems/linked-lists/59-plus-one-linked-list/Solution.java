class Solution {
    public ListNode plusOne(ListNode head) {
        ListNode sentinel = new ListNode(0, head);
        ListNode notNine = sentinel;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val != 9) {
                notNine = curr;
            }
            curr = curr.next;
        }
        notNine.val++;
        curr = notNine.next;
        while (curr != null) {
            curr.val = 0;
            curr = curr.next;
        }
        return sentinel.val == 1 ? sentinel : sentinel.next;
    }
}
