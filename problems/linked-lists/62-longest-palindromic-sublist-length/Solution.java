class Solution {
    private int countCommon(ListNode a, ListNode b) {
        int c = 0;
        while (a != null && b != null && a.val == b.val) {
            c++;
            a = a.next;
            b = b.next;
        }
        return c;
    }

    public int maxPalindromeLength(ListNode head) {
        int ans = 0;
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            ans = Math.max(ans, 2 * countCommon(prev, nxt) + 1);
            ans = Math.max(ans, 2 * countCommon(curr, nxt));
            prev = curr;
            curr = nxt;
        }
        return ans;
    }
}
