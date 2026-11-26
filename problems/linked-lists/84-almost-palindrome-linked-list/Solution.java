class Solution {
    public boolean isAlmostPalindrome(ListNode head) {
        if (head == null || head.next == null) {
            return true;
        }
        ListNode slow = head;
        ListNode fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        boolean isOdd = (fast.next == null);

        ListNode second = slow.next;
        slow.next = null;
        ListNode rev = null;
        while (second != null) {
            ListNode nxt = second.next;
            second.next = rev;
            rev = second;
            second = nxt;
        }

        ListNode p1 = head;
        ListNode p2 = rev;
        while (p2 != null && p1.val == p2.val) {
            p1 = p1.next;
            p2 = p2.next;
        }
        if (p2 == null) {
            return true;
        }

        // Option 1: delete p1 from left half
        ListNode a = p1.next;
        ListNode b = p2;
        boolean ok1 = true;
        while (a != null) {
            if (a.val != b.val) {
                ok1 = false;
                break;
            }
            a = a.next;
            b = b.next;
        }
        if (ok1) {
            return true;
        }

        // Option 2: delete p2 from right half
        a = p1;
        b = p2.next;
        while (b != null) {
            if (a.val != b.val) {
                return false;
            }
            a = a.next;
            b = b.next;
        }
        if (isOdd) {
            return a.val == a.next.val;
        }
        return true;
    }
}
