class Solution {
    public ListNode reverseBetweenMinMax(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        int minVal = head.val;
        int maxVal = head.val;
        int minPos = 1;
        int maxPos = 1;
        int pos = 1;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val < minVal) {
                minVal = curr.val;
                minPos = pos;
            }
            if (curr.val > maxVal) {
                maxVal = curr.val;
                maxPos = pos;
            }
            curr = curr.next;
            pos++;
        }
        int left = Math.min(minPos, maxPos);
        int right = Math.max(minPos, maxPos);
        if (left == right) {
            return head;
        }

        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        for (int i = 0; i < left - 1; i++) {
            prev = prev.next;
        }
        ListNode tail = prev.next;
        curr = tail;
        ListNode rprev = null;
        for (int i = 0; i < right - left + 1; i++) {
            ListNode nxt = curr.next;
            curr.next = rprev;
            rprev = curr;
            curr = nxt;
        }
        prev.next = rprev;
        tail.next = curr;
        return dummy.next;
    }
}
