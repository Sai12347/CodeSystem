class Solution {
    private long inv;

    private ListNode sortCount(ListNode node, int length) {
        if (length <= 1 || node == null) {
            return node;
        }
        int leftLen = length / 2;
        int rightLen = length - leftLen;
        ListNode mid = node;
        for (int i = 0; i < leftLen - 1; i++) {
            mid = mid.next;
        }
        ListNode rightHead = mid.next;
        mid.next = null;

        ListNode left = sortCount(node, leftLen);
        ListNode right = sortCount(rightHead, rightLen);
        int leftRem = leftLen;

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (left != null && right != null) {
            if (left.val <= right.val) {
                tail.next = left;
                left = left.next;
                leftRem--;
            } else {
                tail.next = right;
                right = right.next;
                inv += leftRem;
            }
            tail = tail.next;
        }
        tail.next = left != null ? left : right;
        return dummy.next;
    }

    public long countInversions(ListNode head) {
        inv = 0L;
        int n = 0;
        ListNode curr = head;
        while (curr != null) {
            n++;
            curr = curr.next;
        }
        sortCount(head, n);
        return inv;
    }
}
