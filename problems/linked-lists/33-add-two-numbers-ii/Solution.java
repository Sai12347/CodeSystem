class Solution {
    private ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode r1 = reverse(l1);
        ListNode r2 = reverse(l2);
        int carry = 0;
        ListNode ans = null;
        while (r1 != null || r2 != null || carry != 0) {
            int total = carry;
            if (r1 != null) {
                total += r1.val;
                r1 = r1.next;
            }
            if (r2 != null) {
                total += r2.val;
                r2 = r2.next;
            }
            carry = total / 10;
            ans = new ListNode(total % 10, ans);
        }
        return ans;
    }
}
