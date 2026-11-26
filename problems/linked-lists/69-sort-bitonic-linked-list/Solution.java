class Solution {
    public ListNode sortBitonicList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode curr = head;
        while (curr.next != null && curr.val <= curr.next.val) {
            curr = curr.next;
        }
        if (curr.next == null) {
            return head;
        }
        ListNode second = curr.next;
        curr.next = null;

        ListNode prev = null;
        while (second != null) {
            ListNode nxt = second.next;
            second.next = prev;
            prev = second;
            second = nxt;
        }

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        ListNode a = head;
        ListNode b = prev;
        while (a != null && b != null) {
            if (a.val <= b.val) {
                tail.next = a;
                a = a.next;
            } else {
                tail.next = b;
                b = b.next;
            }
            tail = tail.next;
        }
        tail.next = a != null ? a : b;
        return dummy.next;
    }
}
