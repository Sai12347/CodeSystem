class Solution {
    public ListNode zigzagList(ListNode head) {
        ListNode curr = head;
        boolean expectLess = true;
        while (curr != null && curr.next != null) {
            if (expectLess) {
                if (curr.val > curr.next.val) {
                    int tmp = curr.val;
                    curr.val = curr.next.val;
                    curr.next.val = tmp;
                }
            } else {
                if (curr.val < curr.next.val) {
                    int tmp = curr.val;
                    curr.val = curr.next.val;
                    curr.next.val = tmp;
                }
            }
            expectLess = !expectLess;
            curr = curr.next;
        }
        return head;
    }
}
