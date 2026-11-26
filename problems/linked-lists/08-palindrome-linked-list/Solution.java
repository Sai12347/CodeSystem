class Solution {
    public boolean isPalindrome(ListNode head) {
        if (head == null || head.next == null) {
            return true;
        }
        ListNode slow = head;
        ListNode fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }

        ListNode secondHead = reverse(slow.next);
        ListNode p1 = head;
        ListNode p2 = secondHead;
        boolean ok = true;
        while (p2 != null) {
            if (p1.val != p2.val) {
                ok = false;
                break;
            }
            p1 = p1.next;
            p2 = p2.next;
        }
        slow.next = reverse(secondHead);
        return ok;
    }

    private ListNode reverse(ListNode node) {
        ListNode prev = null;
        ListNode curr = node;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }
}
