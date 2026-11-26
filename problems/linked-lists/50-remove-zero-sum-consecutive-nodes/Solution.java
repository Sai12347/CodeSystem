class Solution {
    public ListNode removeZeroSumSublists(ListNode head) {
        ListNode dummy = new ListNode(0, head);
        Map<Integer, ListNode> last = new HashMap<>();
        int prefix = 0;
        for (ListNode curr = dummy; curr != null; curr = curr.next) {
            prefix += curr.val;
            last.put(prefix, curr);
        }
        prefix = 0;
        for (ListNode curr = dummy; curr != null; curr = curr.next) {
            prefix += curr.val;
            curr.next = last.get(prefix).next;
        }
        return dummy.next;
    }
}
