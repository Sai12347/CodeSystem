class Solution {
    public ListNode eliminationOrder(ListNode head, int k) {
        List<ListNode> nodes = new ArrayList<>();
        ListNode curr = head;
        while (curr != null) {
            nodes.add(curr);
            curr = curr.next;
        }
        int n = nodes.size();
        int[] bit = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            bit[i] = i & -i;
        }
        int maxPow = Integer.highestOneBit(n);

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        int pos = 0;
        for (int rem = n; rem >= 1; rem--) {
            pos = (int) (((long) pos + k - 1) % rem);
            int target = pos + 1;
            int idx = 0;
            for (int step = maxPow; step > 0; step >>= 1) {
                int nxt = idx + step;
                if (nxt <= n && bit[nxt] < target) {
                    target -= bit[nxt];
                    idx = nxt;
                }
            }
            int chosen = idx + 1;
            for (int x = chosen; x <= n; x += x & -x) {
                bit[x]--;
            }
            ListNode node = nodes.get(chosen - 1);
            tail.next = node;
            tail = node;
        }
        tail.next = null;
        return dummy.next;
    }
}
