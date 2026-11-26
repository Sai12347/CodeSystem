class Solution {
    public int kthSmallestInLists(ListNode[] lists, int k) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
        for (ListNode head : lists) {
            if (head != null) {
                pq.offer(head);
            }
        }
        int ans = 0;
        for (int i = 0; i < k; i++) {
            ListNode node = pq.poll();
            ans = node.val;
            if (node.next != null) {
                pq.offer(node.next);
            }
        }
        return ans;
    }
}
