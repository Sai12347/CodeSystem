class Solution {
    public ListNode sortLinkedList(ListNode head) {
        if (head == null) {
            return null;
        }
        ListNode curr = head;
        while (curr.next != null) {
            if (curr.next.val < 0) {
                ListNode node = curr.next;
                curr.next = node.next;
                node.next = head;
                head = node;
            } else {
                curr = curr.next;
            }
        }
        return head;
    }
}
