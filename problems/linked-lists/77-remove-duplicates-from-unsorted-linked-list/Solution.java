class Solution {
    public ListNode removeUnsortedDuplicates(ListNode head) {
        if (head == null) {
            return null;
        }
        Set<Integer> seen = new HashSet<>();
        seen.add(head.val);
        ListNode prev = head;
        ListNode curr = head.next;
        while (curr != null) {
            if (seen.contains(curr.val)) {
                prev.next = curr.next;
            } else {
                seen.add(curr.val);
                prev = curr;
            }
            curr = curr.next;
        }
        return head;
    }
}
