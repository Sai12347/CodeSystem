class Solution {
    public ListNode sortKSortedList(ListNode head, int k) {
        if (head == null || head.next == null || k == 0) {
            return head;
        }
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
        ListNode curr = head;
        for (int i = 0; i <= k && curr != null; i++) {
            pq.offer(curr);
            curr = curr.next;
        }
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (!pq.isEmpty()) {
            ListNode node = pq.poll();
            tail.next = node;
            tail = node;
            if (curr != null) {
                pq.offer(curr);
                curr = curr.next;
            }
        }
        tail.next = null;
        return dummy.next;
    }
}
