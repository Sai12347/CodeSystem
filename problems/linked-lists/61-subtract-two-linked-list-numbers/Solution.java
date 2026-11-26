class Solution {
    private int length(ListNode node) {
        int c = 0;
        while (node != null) {
            c++;
            node = node.next;
        }
        return c;
    }

    private ListNode reverse(ListNode node) {
        ListNode prev = null;
        while (node != null) {
            ListNode nxt = node.next;
            node.next = prev;
            prev = node;
            node = nxt;
        }
        return prev;
    }

    public ListNode subtractTwoNumbers(ListNode l1, ListNode l2) {
        int n1 = length(l1);
        int n2 = length(l2);
        ListNode big;
        ListNode small;
        if (n1 < n2) {
            big = l2;
            small = l1;
        } else if (n1 > n2) {
            big = l1;
            small = l2;
        } else {
            ListNode p1 = l1;
            ListNode p2 = l2;
            while (p1 != null && p1.val == p2.val) {
                p1 = p1.next;
                p2 = p2.next;
            }
            if (p1 == null) {
                return new ListNode(0);
            }
            if (p1.val > p2.val) {
                big = l1;
                small = l2;
            } else {
                big = l2;
                small = l1;
            }
        }

        ListNode r1 = reverse(big);
        ListNode r2 = reverse(small);
        int borrow = 0;
        ListNode res = null;
        while (r1 != null) {
            int v2 = r2 != null ? r2.val : 0;
            int diff = r1.val - v2 - borrow;
            if (diff < 0) {
                diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            res = new ListNode(diff, res);
            r1 = r1.next;
            if (r2 != null) {
                r2 = r2.next;
            }
        }
        while (res != null && res.val == 0 && res.next != null) {
            res = res.next;
        }
        return res;
    }
}
