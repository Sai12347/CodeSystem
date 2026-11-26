class Solution {
    public ListNode sortByFrequency(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        Map<Integer, Integer> freq = new HashMap<>();
        List<ListNode> nodes = new ArrayList<>();
        ListNode curr = head;
        while (curr != null) {
            freq.merge(curr.val, 1, Integer::sum);
            nodes.add(curr);
            curr = curr.next;
        }
        nodes.sort((a, b) -> {
            int cmp = Integer.compare(freq.get(b.val), freq.get(a.val));
            return cmp != 0 ? cmp : Integer.compare(a.val, b.val);
        });
        for (int i = 0; i < nodes.size() - 1; i++) {
            nodes.get(i).next = nodes.get(i + 1);
        }
        nodes.get(nodes.size() - 1).next = null;
        return nodes.get(0);
    }
}
