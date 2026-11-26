class Solution {
    public ListNode sortList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }

        int n = 0;
        for (ListNode cur = head; cur != null; cur = cur.next) {
            n++;
        }

        ListNode dummy = new ListNode(0, head);
        for (int step = 1; step < n; step <<= 1) {
            ListNode tail = dummy;
            ListNode cur = dummy.next;
            while (cur != null) {
                ListNode left = cur;
                ListNode right = split(left, step);
                cur = split(right, step);
                tail = merge(left, right, tail);
            }
        }
        return dummy.next;
    }

    private ListNode split(ListNode node, int size) {
        for (int i = 1; node != null && i < size; i++) {
            node = node.next;
        }
        if (node == null) {
            return null;
        }
        ListNode rest = node.next;
        node.next = null;
        return rest;
    }

    private ListNode merge(ListNode l1, ListNode l2, ListNode tail) {
        ListNode cur = tail;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                cur.next = l1;
                l1 = l1.next;
            } else {
                cur.next = l2;
                l2 = l2.next;
            }
            cur = cur.next;
        }
        cur.next = (l1 != null) ? l1 : l2;
        while (cur.next != null) {
            cur = cur.next;
        }
        return cur;
    }
}
