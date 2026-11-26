class Solution {
    public ListNode reverseBetweenZeros(ListNode head) {
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        while (prev.next != null) {
            if (prev.next.val == 0) {
                prev = prev.next;
            } else {
                ListNode segTail = prev.next;
                ListNode curr = segTail;
                ListNode rprev = null;
                while (curr != null && curr.val != 0) {
                    ListNode nxt = curr.next;
                    curr.next = rprev;
                    rprev = curr;
                    curr = nxt;
                }
                prev.next = rprev;
                segTail.next = curr;
                prev = segTail;
            }
        }
        return dummy.next;
    }
}
