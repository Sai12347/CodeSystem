class Solution {
    public ListNode reverseDecreasingRuns(ListNode head) {
        ListNode dummy = new ListNode(0, head);
        ListNode prevTail = dummy;
        ListNode curr = head;
        while (curr != null) {
            ListNode runTail = curr;
            ListNode revHead = curr;
            int lastVal = curr.val;
            ListNode nxt = curr.next;
            curr.next = null;
            while (nxt != null && nxt.val < lastVal) {
                lastVal = nxt.val;
                ListNode after = nxt.next;
                nxt.next = revHead;
                revHead = nxt;
                nxt = after;
            }
            prevTail.next = revHead;
            prevTail = runTail;
            curr = nxt;
        }
        return dummy.next;
    }
}
