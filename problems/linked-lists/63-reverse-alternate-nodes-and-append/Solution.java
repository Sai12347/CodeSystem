class Solution {
    public ListNode reverseAlternateAndAppend(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode odd = head;
        ListNode revEven = null;
        while (odd.next != null) {
            ListNode even = odd.next;
            odd.next = even.next;
            even.next = revEven;
            revEven = even;
            if (odd.next != null) {
                odd = odd.next;
            }
        }
        odd.next = revEven;
        return head;
    }
}
