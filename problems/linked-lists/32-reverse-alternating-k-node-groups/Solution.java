class Solution {
    public ListNode reverseAlternatingKGroup(ListNode head, int k) {
        if (head == null || k <= 1) {
            return head;
        }
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        ListNode curr = head;
        boolean shouldReverse = true;
        while (curr != null) {
            if (shouldReverse) {
                ListNode groupTail = curr;
                ListNode rprev = null;
                int count = 0;
                while (curr != null && count < k) {
                    ListNode nxt = curr.next;
                    curr.next = rprev;
                    rprev = curr;
                    curr = nxt;
                    count++;
                }
                prev.next = rprev;
                groupTail.next = curr;
                prev = groupTail;
            } else {
                int count = 0;
                while (curr != null && count < k) {
                    prev = curr;
                    curr = curr.next;
                    count++;
                }
            }
            shouldReverse = !shouldReverse;
        }
        return dummy.next;
    }
}
