class Solution {
    public ListNode[] splitListToParts(ListNode head, int k) {
        int n = 0;
        ListNode curr = head;
        while (curr != null) {
            n++;
            curr = curr.next;
        }
        int base = n / k;
        int rem = n % k;
        ListNode[] res = new ListNode[k];
        curr = head;
        for (int i = 0; i < k; i++) {
            int partLen = base + (i < rem ? 1 : 0);
            if (partLen == 0 || curr == null) {
                continue;
            }
            res[i] = curr;
            for (int j = 0; j < partLen - 1; j++) {
                curr = curr.next;
            }
            ListNode nxt = curr.next;
            curr.next = null;
            curr = nxt;
        }
        return res;
    }
}
