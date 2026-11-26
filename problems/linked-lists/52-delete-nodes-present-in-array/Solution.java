class Solution {
    public ListNode modifiedList(int[] nums, ListNode head) {
        Set<Integer> ban = new HashSet<>();
        for (int x : nums) {
            ban.add(x);
        }
        ListNode dummy = new ListNode(0, head);
        ListNode curr = dummy;
        while (curr.next != null) {
            if (ban.contains(curr.next.val)) {
                curr.next = curr.next.next;
            } else {
                curr = curr.next;
            }
        }
        return dummy.next;
    }
}
