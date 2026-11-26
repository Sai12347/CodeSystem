class Solution {
    private int gcd(int a, int b) {
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    public ListNode insertGreatestCommonDivisors(ListNode head) {
        ListNode curr = head;
        while (curr != null && curr.next != null) {
            ListNode nxt = curr.next;
            ListNode node = new ListNode(gcd(curr.val, nxt.val), nxt);
            curr.next = node;
            curr = nxt;
        }
        return head;
    }
}
